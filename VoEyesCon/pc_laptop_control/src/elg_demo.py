class PLC():

    def __init__(self):
        ##################################### Debug Var #############################################

        self.debug_monitor_index = 1
        self.debug_execute_calibration = True
        self.debug_draw_gaze_arrow = True

        self.debug_full_screen_calibration = True
        self.debug_full_screen_gaze_capture = True

        self.debug_show_visualize_info = False
        self.debug_show_result_info = False
        self.debug_show_current_info = False

        self.debug_display_webcam = True

        self.debug_execute_voice = True

        #############################################################################################

        self.monitor_size = None
        self.recognition = None
        self.cali = None
        self.perform = None

    def execution(self):
        """Main script for gaze direction inference from webcam feed."""
        import argparse
        import os
        import queue
        import threading
        import time

        import coloredlogs
        import cv2 as cv
        import numpy as np
        import tensorflow as tf

        from .datasources import Video, Webcam
        from .models import ELG
        from .util.gaze import draw_monitor_grid, draw_gaze_point, draw_gaze

        from .util.calibration import Calibration
        from .util.perfomance_test import Performance

        import pyautogui # 주석
        import speech_recognition as sr

        pyautogui.FAILSAFE = False
        self.monitor_size = pyautogui.size()

        self.recognition = sr.Recognizer()

        self.cali = Calibration()
        self.perform = Performance(self.cali.Const_Display_X, self.cali.Const_Display_Y)

        if not self.debug_execute_calibration:
            self.cali.is_finish = True

        if self.debug_full_screen_calibration:
            self.cali.is_full_screen = True

        # Set global log level
        parser = argparse.ArgumentParser(description='Demonstration of landmarks localization.')
        parser.add_argument('-v', type=str, help='logging level', default='info',
                            choices=['debug', 'info', 'warning', 'error', 'critical'])
        parser.add_argument('--from_video', type=str, help='Use this video path instead of webcam')
        parser.add_argument('--record_video', type=str, help='Output path of video of demonstration.')
        parser.add_argument('--fullscreen', action='store_true')
        parser.add_argument('--headless', action='store_true')

        parser.add_argument('--fps', type=int, default=60, help='Desired sampling rate of webcam')
        parser.add_argument('--camera_id', type=int, default=0, help='ID of webcam to use')

        args = parser.parse_args()
        coloredlogs.install(datefmt='%d/%m %H:%M', fmt='%(asctime)s %(levelname)s %(message)s', level=args.v.upper(),)

        # Check if GPU is available
        from tensorflow.python.client import device_lib

        session_config = tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True))
        gpu_available = False
        try:
            gpus = [d for d in device_lib.list_local_devices(session_config)
                    if d.device_type == 'GPU']
            gpu_available = len(gpus) > 0
        except:
            pass

        # Initialize Tensorflow session
        tf.logging.set_verbosity(tf.logging.INFO)
        with tf.Session(config=session_config) as session:

            # Declare some parameters
            batch_size = 2

            # Define webcam stream data source
            # Change data_format='NHWC' if not using CUDA
            if args.from_video:
                assert os.path.isfile(args.from_video)
                data_source = Video(args.from_video, tensorflow_session=session, batch_size=batch_size,
                                    data_format='NCHW' if gpu_available else 'NHWC', eye_image_shape=(108, 180))
            else:
                data_source = Webcam(tensorflow_session=session, batch_size=batch_size,
                                    camera_id=args.camera_id, fps=args.fps,
                                    data_format='NCHW' if gpu_available else 'NHWC', eye_image_shape=(36, 60))

            # Define model
            if args.from_video:
                model = ELG(
                    session, train_data={'videostream': data_source},
                    first_layer_stride=3,
                    num_modules=3,
                    num_feature_maps=64,
                    learning_schedule=[
                        {
                            'loss_terms_to_optimize': {'dummy': ['hourglass', 'radius']},
                        },
                    ],
                )
            else:
                model = ELG(
                    session, train_data={'videostream': data_source},
                    first_layer_stride=1,
                    num_modules=2,
                    num_feature_maps=32,
                    learning_schedule=[
                        {
                            'loss_terms_to_optimize': {'dummy': ['hourglass', 'radius']},
                        },
                    ],
                )

            # Record output frames to file if requested
            if args.record_video:
                video_out = None
                video_out_queue = queue.Queue()
                video_out_should_stop = False
                video_out_done = threading.Condition()

                def _record_frame():
                    global video_out
                    last_frame_time = None
                    out_fps = 30
                    out_frame_interval = 1.0 / out_fps
                    while not video_out_should_stop:
                        frame_index = video_out_queue.get()
                        if frame_index is None:
                            break
                        assert frame_index in data_source._frames
                        frame = data_source._frames[frame_index]['bgr']
                        h, w, _ = frame.shape
                        if video_out is None:
                            video_out = cv.VideoWriter(args.record_video, cv.VideoWriter_fourcc(*'H264'),out_fps, (w, h),)
                        now_time = time.time()
                        if last_frame_time is not None:
                            time_diff = now_time - last_frame_time
                            while time_diff > 0.0:
                                video_out.write(frame)
                                time_diff -= out_frame_interval
                        last_frame_time = now_time
                    video_out.release()
                    with video_out_done:
                        video_out_done.notify_all()

                record_thread = threading.Thread(target=_record_frame, name='record')
                record_thread.daemon = True
                record_thread.start()

            # Begin visualization thread
            inferred_stuff_queue = queue.Queue()

            def _visualize_output():

                is_set_fullscreen = False
                is_start_visualize =  False
                last_frame_index = 0
                last_frame_time = time.time()
                fps_history = []
                all_gaze_histories = []
                all_point_histories = []

                # 패턴
                pattern = [1, 3, 9, 7]
                after_history = 0               # 일정시간 응시 후 저장되는 포인트
                pattern_compare = []
                match = 0

                if args.fullscreen :
                    self.cali.is_full_screen = True

                while True:
                    # If no output to visualize, show unannotated frame
                    if inferred_stuff_queue.empty():
                        next_frame_index = last_frame_index + 1
                        if next_frame_index in data_source._frames:
                            next_frame = data_source._frames[next_frame_index]
                            if 'faces' in next_frame and len(next_frame['faces']) == 0:
                                self.cali.is_face_detect = False
                                if not args.headless:
                                    if self.cali.is_finish:
                                        if self.debug_display_webcam:
                                            if not is_start_visualize:
                                                is_start_visualize = True

                                                if self.debug_full_screen_gaze_capture or args.fullscreen:
                                                    cv.namedWindow('vis', cv.WND_PROP_FULLSCREEN)
                                                    cv.setWindowProperty('vis', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

                                            img = next_frame['bgr']

                                            # 그리드 레이아웃 그리기
                                            draw_monitor_grid(img, self.cali.Const_Display_X, self.cali.Const_Display_Y, self.cali.Const_Grid_Count_Y, True)
                                            draw_monitor_grid(img, self.cali.Const_Display_X, self.cali.Const_Display_Y, self.cali.Const_Grid_Count_X, False)

                                            cv.imshow('vis', img)
                                            cv.setMouseCallback('vis', self.perform.mouse_callback, param = self.cali)
                                        else:
                                            if self.cali.current_image is not None:
                                                self.cali.current_image = None
                                                cv.destroyWindow('vis')

                                    else:
                                        if is_set_fullscreen == False:
                                            is_set_fullscreen=True
                                            cv.namedWindow('vis', cv.WND_PROP_FULLSCREEN)
                                            cv.setWindowProperty('vis', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
                                        if self.cali.current_image is not None:
                                            cv.imshow('vis', self.cali.current_image)

                                if args.record_video:
                                    video_out_queue.put_nowait(next_frame_index)
                                last_frame_index = next_frame_index

                            elif not 'faces' in next_frame: # 주석
                                self.cali.is_face_detect = True  ## Detecting Face

                                if self.debug_execute_calibration:

                                    if not self.cali.is_start:  ## Only play once Calibration
                                        calibration_thread = threading.Thread(target=self.cali.start_cali, name='calibration_th2')
                                        calibration_thread.daemon = True
                                        calibration_thread.start()

                        # /////////////////////////////////////////////////////
                        # 종료 조건
                        if self.cali.is_fail:
                            print("Failed Calibration!")
                            return

                        if cv.waitKey(1) & 0xFF == ord('q'):
                            return
                        # /////////////////////////////////////////////////////
                        continue

                    # Get output from neural network and visualize
                    output = inferred_stuff_queue.get()

                    for j in range(batch_size):
                        frame_index = output['frame_index'][j]
                        if frame_index not in data_source._frames:
                            continue
                        frame = data_source._frames[frame_index]

                        # Decide which landmarks are usable
                        heatmaps_amax = np.amax(output['heatmaps'][j, :].reshape(-1, 18), axis=0)
                        can_use_eye = np.all(heatmaps_amax > 0.7)
                        can_use_eyelid = np.all(heatmaps_amax[0:8] > 0.75)
                        can_use_iris = np.all(heatmaps_amax[8:16] > 0.8)

                        start_time = time.time()
                        eye_index = output['eye_index'][j]
                        bgr = frame['bgr']
                        eye = frame['eyes'][eye_index]
                        eye_image = eye['image']
                        eye_side = eye['side']
                        eye_landmarks = output['landmarks'][j, :]
                        eye_radius = output['radius'][j][0]
                        if eye_side == 'left':
                            eye_landmarks[:, 0] = eye_image.shape[1] - eye_landmarks[:, 0]
                            eye_image = np.fliplr(eye_image)

                        # Embed eye image and annotate for picture-in-picture
                        eye_upscale = 2
                        eye_image_raw = cv.cvtColor(cv.equalizeHist(eye_image), cv.COLOR_GRAY2BGR)
                        eye_image_raw = cv.resize(eye_image_raw, (0, 0), fx=eye_upscale, fy=eye_upscale)
                        eye_image_annotated = np.copy(eye_image_raw)
                        if can_use_eyelid:
                            cv.polylines(
                                eye_image_annotated,
                                [np.round(eye_upscale * eye_landmarks[0:8]).astype(np.int32) .reshape(-1, 1, 2)],
                                isClosed=True, color=(255, 255, 0), thickness=1, lineType=cv.LINE_AA,
                            )
                            self.cali.is_face_detect = True
                        else:
                            self.cali.is_face_detect = False
                        if can_use_iris:
                            cv.polylines(
                                eye_image_annotated,
                                [np.round(eye_upscale * eye_landmarks[8:16]).astype(np.int32).reshape(-1, 1, 2)],
                                isClosed=True, color=(0, 255, 255), thickness=1, lineType=cv.LINE_AA,
                            )
                            cv.drawMarker(
                                eye_image_annotated,
                                tuple(np.round(eye_upscale * eye_landmarks[16, :]).astype(np.int32)),
                                color=(0, 255, 255), markerType=cv.MARKER_CROSS, markerSize=4,
                                thickness=1, line_type=cv.LINE_AA,
                            )
                            self.cali.is_face_detect = True
                        else:       # 얼굴인식안됨으로 판별
                            self.cali.is_face_detect = False

                        face_index = int(eye_index / 2)
                        eh, ew, _ = eye_image_raw.shape
                        v0 = face_index * 2 * eh
                        v1 = v0 + eh
                        v2 = v1 + eh
                        u0 = 0 if eye_side == 'left' else ew
                        u1 = u0 + ew
                        bgr[v0:v1, u0:u1] = eye_image_raw
                        bgr[v1:v2, u0:u1] = eye_image_annotated

                        # Visualize preprocessing results
                        frame_landmarks = (frame['smoothed_landmarks']
                                        if 'smoothed_landmarks' in frame
                                        else frame['landmarks'])

                        if self.debug_display_webcam:
                            for f, face in enumerate(frame['faces']):
                                for landmark in frame_landmarks[f][:-1]:
                                    cv.drawMarker(bgr, tuple(np.round(landmark).astype(np.int32)),
                                                color=(0, 0, 255), markerType=cv.MARKER_STAR,
                                                markerSize=2, thickness=1, line_type=cv.LINE_AA)
                                cv.rectangle(
                                    bgr, tuple(np.round(face[:2]).astype(np.int32)),
                                    tuple(np.round(np.add(face[:2], face[2:])).astype(np.int32)),
                                    color=(0, 255, 255), thickness=1, lineType=cv.LINE_AA,
                                )

                        # 눈 중심 개선
                        eye_landmarks = np.concatenate([eye_landmarks, [[eye_landmarks[-1, 0] + eye_radius,
                                                        eye_landmarks[-1, 1]]]])
                        eye_landmarks = np.asmatrix(np.pad(eye_landmarks, ((0, 0), (0, 1)),
                                                        'constant', constant_values=1.0))
                        eye_landmarks = (eye_landmarks * eye['inv_landmarks_transform_mat'].T)[:, :2]
                        eye_landmarks = np.asarray(eye_landmarks)
                        eyelid_landmarks = eye_landmarks[0:8, :]
                        iris_landmarks = eye_landmarks[8:16, :]
                        iris_centre = sum(iris_landmarks) / len(iris_landmarks)
                        eyeball_centre = sum(eye_landmarks) / len(eye_landmarks)

                        gaze_mean = 0
                        point_count = 0

                        eye_size_x = abs(eye_landmarks[12][0] - eye_landmarks[8][0])
                        eye_size_y = eye_landmarks[14][1] - eye_landmarks[10][1]

                        if eye_side == 'left':
                            self.cali.left_iris_centre = iris_centre
                            left_i_x0, left_i_y0 = self.cali.left_iris_centre
                            self.cali.left_eyeball_centre = eyeball_centre
                            left_e_x0, left_e_y0 = self.cali.left_eyeball_centre
                            self.cali.left_eye_size_x = eye_size_x
                            self.cali.left_eye_size_y = eye_size_y
                        else:
                            self.cali.right_iris_centre = iris_centre
                            right_i_x0, right_i_y0 = self.cali.right_iris_centre
                            self.cali.right_eyeball_centre = eyeball_centre
                            right_e_x0, right_e_y0 = self.cali.right_eyeball_centre
                            self.cali.right_eye_size_x = eye_size_x
                            self.cali.right_eye_size_y = eye_size_y

                        # Smooth and visualize gaze direction
                        num_total_eyes_in_frame = len(frame['eyes'])
                        if len(all_gaze_histories) != num_total_eyes_in_frame:
                            all_gaze_histories = [list() for _ in range(num_total_eyes_in_frame)]
                            all_point_histories = [list() for _ in range(num_total_eyes_in_frame)]
                        gaze_history = all_gaze_histories[eye_index]
                        point_history = all_point_histories[eye_index]

                        if can_use_eye:
                            # Visualize landmarks
                            if self.debug_display_webcam:
                                cv.drawMarker(  # Eyeball centre
                                    bgr, tuple(np.round(eyeball_centre).astype(np.int32)),
                                    color=(0, 255, 0), markerType=cv.MARKER_CROSS, markerSize=4,
                                    thickness=1, line_type=cv.LINE_AA,
                                )

                            if self.cali.is_finish:

                                left_gaze_x = left_i_x0 - left_e_x0
                                right_gaze_x = right_i_x0 - right_e_x0
                                left_gaze_y = left_i_y0 - left_e_y0
                                right_gaze_y = right_i_y0 - right_e_y0

                                # 캘리브레이션 가중치 변경
                                def calc_cali(is_left, a):
                                    result = []
                                    box_plot = []
                                    cali_iris = []
                                    iris_eyeball = []

                                    if is_left == 0 :
                                        for i in range(14):
                                            cali_iris.append(self.cali.Cali_Center_Points[i][a] -
                                                            self.cali.left_iris_captured_data[i][a])
                                            iris_eyeball.append(self.cali.left_iris_captured_data[i][a] -
                                                                self.cali.left_eyeball_captured_data[i][a])
                                    else :
                                        for i in range(14):
                                            cali_iris.append(self.cali.Cali_Center_Points[i][a] -
                                                            self.cali.right_iris_captured_data[i][a])
                                            iris_eyeball.append(self.cali.right_iris_captured_data[i][a] -
                                                                self.cali.right_eyeball_captured_data[i][a])

                                    for i in range(14):
                                        result.append(abs(cali_iris[i] / (iris_eyeball[i] * iris_eyeball[i])))

                                    result.sort()

                                    iqr = result[9] - result[4]
                                    box_max = result[9] + 1.5 * iqr
                                    box_min = result[4] - 1.5 * iqr

                                    for i in range(14):
                                        if result[i] > box_min and result[i] < box_max:
                                            box_plot.append(result[i])

                                    return np.median(box_plot)

                                # 눈 크기 가중치
                                def calc_size(is_left, a):
                                    result = []

                                    if is_left == 0 :
                                        if a == 0 :
                                            for i in range(14):
                                                result.append(self.cali.left_save_eye_size_x[i])
                                        else :
                                            for i in range(14):
                                                result.append(self.cali.left_save_eye_size_y[i])
                                    else :
                                        if a == 0 :
                                            for i in range(14):
                                                result.append(self.cali.right_save_eye_size_x[i])
                                        else :
                                            for i in range(14):
                                                result.append(self.cali.right_save_eye_size_y[i])

                                    return np.median(result)

                                left_dx = calc_cali(0, 0) * calc_size(0, 0) / self.cali.left_eye_size_x
                                right_dx = calc_cali(1, 0) * calc_size(1, 0) / self.cali.right_eye_size_x
                                left_dy = calc_cali(0, 1) * calc_size(0, 1) / self.cali.left_eye_size_y
                                right_dy = calc_cali(1, 1) * calc_size(1, 1) / self.cali.right_eye_size_y

                                current_gaze = np.array([((left_i_x0 + left_gaze_x * abs(left_gaze_x) * left_dx) +
                                                        (right_i_x0 + right_gaze_x * abs(right_gaze_x) * right_dx)) / 2,
                                                        ((left_i_y0 + left_gaze_y * abs(left_gaze_y) * left_dy) +
                                                        (right_i_y0 + right_gaze_y * abs(right_gaze_y) * right_dy)) / 2])

                                if current_gaze[0] < self.cali.Const_Display_X / 3 :
                                    left_eye_location = 1
                                elif current_gaze[0] > self.cali.Const_Display_X * 2 / 3 :
                                    left_eye_location = 3
                                else :
                                    left_eye_location = 2

                                if current_gaze[1] < self.cali.Const_Display_Y / 3 :
                                    top_eye_location = 0
                                elif current_gaze[1] > self.cali.Const_Display_Y * 2 / 3 :
                                    top_eye_location = 2
                                else :
                                    top_eye_location = 1

                                point = left_eye_location + top_eye_location * 3

                                point_history.append(point)
                                point_history_max_len = 10
                                if len(point_history) > point_history_max_len:
                                    point_history = point_history[-point_history_max_len:]

                                point_count = np.bincount(point_history).argmax()
                                self.cali.current_point = point_count

                                gaze_history.append(current_gaze)
                                gaze_history_max_len = 10
                                if len(gaze_history) > gaze_history_max_len:
                                    gaze_history = gaze_history[-gaze_history_max_len:]

                                if eye_side == 'left':
                                    self.cali.left_gaze_coordinate = np.mean(gaze_history, axis=0)
                                else:
                                    self.cali.right_gaze_coordinate = np.mean(gaze_history, axis=0)

                                if (self.cali.left_gaze_coordinate is not None) and (self.cali.right_gaze_coordinate is not None):
                                    gaze_mean = (self.cali.left_gaze_coordinate + self.cali.right_gaze_coordinate) / 2.0

                                    # 가운데 원으로 표시 # 주석
                                    draw_gaze_point(bgr, gaze_mean, thickness=1)
                                    # util.mouse_control.mouse_move(gaze_mean) # 주석

                                    def voice_mouse_control(): # 주석
                                        x = gaze_mean[0] / 1280 * self.monitor_size[0]
                                        y = gaze_mean[1] / 720 * self.monitor_size[1]

                                        if x < 0: x = 0
                                        if y < 0: y = 0
                                        if x >= self.monitor_size[0]: x = self.monitor_size[0] - 1
                                        if y >= self.monitor_size[1]: y = self.monitor_size[1] - 1
                                        
                                        pyautogui.moveTo(x, y)

                                        if self.debug_execute_voice:
                                            self.debug_execute_voice = False

                                            with sr.Microphone() as source:
                                                print("Say something!")
                                                audio = self.recognition.listen(source)

                                            try:
                                                transcript = self.recognition.recognize_google(audio, language="ko-KR") # ko-KR, en-US
                                            except sr.UnknownValueError:
                                                print("당신이 한말을 이해하지 못하였습니다.")
                                            except sr.RequestError as e:
                                                print("당신이 한말을 불러올 수 없습니다.; {0}".format(e))
                                            else:
                                                if transcript in ['이중선택', '이중 선택']:
                                                    pyautogui.doubleClick()
                                                print("당신이 했던 말 : " + transcript)
                                            finally:
                                                self.debug_execute_voice = True
                                    
                                    voice_mouse_control_thread = threading.Thread(target=voice_mouse_control, name='voice_mouse_control')
                                    voice_mouse_control_thread.daemon = True
                                    voice_mouse_control_thread.start()

                                    if self.debug_draw_gaze_arrow:
                                        # 왼쪽 화살표로 표시
                                        if eye_side == 'left':
                                            draw_gaze(bgr, iris_centre, self.cali.left_gaze_coordinate, thickness=1)

                                        # 오른쪽 화살표로 표시
                                        if eye_side == 'right':
                                            draw_gaze(bgr, iris_centre, self.cali.right_gaze_coordinate, thickness=1)

                        else:
                            gaze_history.clear()

                        if self.debug_display_webcam:
                            if can_use_eyelid:
                                cv.polylines(
                                    bgr, [np.round(eyelid_landmarks).astype(np.int32).reshape(-1, 1, 2)],
                                    isClosed=True, color=(255, 255, 0), thickness=1, lineType=cv.LINE_AA,
                                )

                            if can_use_iris:
                                cv.polylines(
                                    bgr, [np.round(iris_landmarks).astype(np.int32).reshape(-1, 1, 2)],
                                    isClosed=True, color=(0, 255, 255), thickness=1, lineType=cv.LINE_AA,
                                )
                                cv.drawMarker(
                                    bgr, tuple(np.round(iris_centre).astype(np.int32)),
                                    color=(0, 255, 255), markerType=cv.MARKER_CROSS, markerSize=4,
                                    thickness=1, line_type=cv.LINE_AA,
                                )

                        dtime = 1e3 * (time.time() - start_time)
                        if 'visualization' not in frame['time']:
                            frame['time']['visualization'] = dtime
                        else:
                            frame['time']['visualization'] += dtime

                        def _dtime(before_id, after_id):
                            return int(1e3 * (frame['time'][after_id] - frame['time'][before_id]))

                        def _dstr(title, before_id, after_id):
                            return '%s: %dms' % (title, _dtime(before_id, after_id))

                        if eye_index == len(frame['eyes']) - 1:
                            # Calculate timings
                            frame['time']['after_visualization'] = time.time()
                            fps = int(np.round(1.0 / (time.time() - last_frame_time)))
                            fps_history.append(fps)
                            if len(fps_history) > 60:
                                fps_history = fps_history[-60:]
                            fps_str = '%d FPS' % np.mean(fps_history)
                            last_frame_time = time.time()
                            fh, fw, _ = bgr.shape

                            if self.debug_display_webcam:
                                cv.putText(bgr, fps_str, org=(fw - 110, fh - 20),
                                        fontFace=cv.FONT_HERSHEY_DUPLEX, fontScale=0.8,
                                        color=(0, 0, 0), thickness=1, lineType=cv.LINE_AA)
                                cv.putText(bgr, fps_str, org=(fw - 111, fh - 21),
                                        fontFace=cv.FONT_HERSHEY_DUPLEX, fontScale=0.79,
                                        color=(255, 255, 255), thickness=1, lineType=cv.LINE_AA)

                            if not args.headless:
                                if self.cali.is_finish == True:
                                    if not is_start_visualize:
                                        is_start_visualize = True
                                        if self.debug_full_screen_gaze_capture or args.fullscreen:
                                            cv.namedWindow('vis', cv.WND_PROP_FULLSCREEN)
                                            cv.setWindowProperty('vis', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
                                            cv.resizeWindow(winname='vis', width=500, height=300) # 주석
                                            cv.moveWindow('vis', 1000, 500) # 주석

                                    if self.debug_display_webcam:

                                        # 그리드 레이아웃 그리기
                                        draw_monitor_grid(bgr, self.cali.Const_Display_X, self.cali.Const_Display_Y, self.cali.Const_Grid_Count_Y, True)
                                        draw_monitor_grid(bgr, self.cali.Const_Display_X, self.cali.Const_Display_Y, self.cali.Const_Grid_Count_X, False)

                                        # 성능평가에서 찍은점 그리기
                                        self.perform.draw_real_coordinate_mark(bgr)
                                        self.perform.draw_gaze_coordinate_mark(bgr)

                                        cv.imshow('vis', bgr)

                                        # call back 함수 등록
                                        if self.perform.is_set_callback == False:
                                            self.perform.is_set_callback = True
                                            cv.setMouseCallback('vis', self.perform.mouse_callback, param = self.cali)
                                    else:
                                        if self.cali.current_image is not None:
                                            self.cali.current_image = None
                                            cv.destroyWindow('vis')

                                elif self.cali.is_finish == False:
                                    if is_set_fullscreen == False:
                                        is_set_fullscreen = True
                                        cv.namedWindow('vis', cv.WND_PROP_FULLSCREEN)
                                        cv.setWindowProperty('vis', cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
                                    if self.cali.current_image is not None:
                                        cv.imshow('vis', self.cali.current_image)
                                        pass

                            last_frame_index = frame_index

                            # Record frame?
                            if args.record_video:
                                video_out_queue.put_nowait(frame_index)

                            if self.cali.is_fail:
                                print("Failed Calibration! Exit Program.")
                                return

                            if (cv.waitKey(1) & 0xFF == ord('q')): # or (match == len(pattern)):
                                return

                            # Print timings
                            if frame_index % 10 == 0:
                                latency = _dtime('before_frame_read', 'after_visualization')
                                processing = _dtime('after_frame_read', 'after_visualization')
                                timing_string = ', '.join([
                                    _dstr('read', 'before_frame_read', 'after_frame_read'),
                                    _dstr('preproc', 'after_frame_read', 'after_preprocessing'),
                                    'infer: %dms' % int(frame['time']['inference']),
                                    'vis: %dms' % int(frame['time']['visualization']),
                                    'proc: %dms' % processing,
                                    'latency: %dms' % latency,
                                ])
                                if is_start_visualize :
                                    if self.debug_show_visualize_info:
                                        print('%08d [%s] %s' % (frame_index, fps_str, timing_string))

                                # 결과값 출력
                                if self.debug_show_current_info:
                                    print("current gaze : ", gaze_mean)
                                    print("point_history : ", point_history)
                                    print("point_count : ", point_count)

                                if self.debug_show_result_info:
                                    if self.cali.is_finish:
                                        print("left_dx : ", left_dx)
                                        print("right_dx : ", right_dx)
                                        print("left_dy : ", left_dy)
                                        print("right_dy : ", right_dy)

                                before_history = after_history
                                after_history = point_count
                                match = 0
                                if point_count != 0:
                                    if before_history == after_history:
                                        if after_history in pattern_compare:
                                            # print("xxxxx", pattern_compare) # 주석
                                            pass
                                        else:
                                            pattern_compare.append(after_history)
                                            # print("pattern_compare : ", pattern_compare) # 주석

                                # 매치 알고리즘
                                i = 0
                                while i < len(pattern_compare):
                                    if pattern_compare[i] == pattern[i]:
                                        match = match + 1
                                    else:
                                        match = 0
                                        pattern_compare = []
                                        break
                                    i = i + 1

                                if (match == len(pattern_compare)):
                                    self.cali.correct_point = pattern_compare
                                else:
                                    self.cali.correct_point = []

                                # print("cali.correct_point : ", cali.correct_point) # 주석

            visualize_thread = threading.Thread(target=_visualize_output, name='visualization')
            visualize_thread.daemon = True
            visualize_thread.start()

            # Do inference forever
            infer = model.inference_generator()
            while True:
                output = next(infer)
                for frame_index in np.unique(output['frame_index']):
                    if frame_index not in data_source._frames:
                        continue
                    frame = data_source._frames[frame_index]
                    if 'inference' in frame['time']:
                        frame['time']['inference'] += output['inference_time']
                    else:
                        frame['time']['inference'] = output['inference_time']
                inferred_stuff_queue.put_nowait(output)

                if not visualize_thread.isAlive():
                    break

                if not data_source._open:
                    break

            # Close video recording
            if args.record_video and video_out is not None:
                video_out_should_stop = True
                video_out_queue.put_nowait(None)
                with video_out_done:
                    video_out_done.wait()