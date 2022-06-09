from distutils.log import debug
import pyautogui # 주석
import speech_recognition as sr
from .sqltool import sql_init

# 모니터 해상도 구하기
#----------------------------------------------------------#
pyautogui.FAILSAFE = False
monitor_size = pyautogui.size() # 모니터 해상도 크기
#----------------------------------------------------------#

# 음성인식 객체
#----------------------------------------------------------#
recognition = sr.Recognizer()
#----------------------------------------------------------#

# 사용자 설정값 불러오기
#----------------------------------------------------------#
with open('VoEyesCon/id_file.txt', 'r') as file:
    id = file.read()

conn = sql_init()
curs = conn.cursor()

 # 사용자 설정값 검색
sql = "SELECT language, x, y FROM user.users WHERE id=%s"
curs.execute(sql, id)

language, x_plus, y_plus = curs.fetchone()

if language == "en": language = "en-US"
elif language == "ko": language = "ko-KR"
else: language = "ko-KR"
#----------------------------------------------------------#

debug_execute_voice = True

# 마우스 Move와 Click, 음성명령 인식
def voice_mouse_control(gaze_mean): # 주석

    # cv창 좌표를 모니터 해상도 좌표로 변경
    x = (gaze_mean[0] / 1280 * monitor_size[0]) + x_plus
    y = (gaze_mean[1] / 720 * monitor_size[1]) + y_plus

    if x < 0: x = 0
    if y < 0: y = 0
    if x >= monitor_size[0]: x = monitor_size[0] - 1
    if y >= monitor_size[1]: y = monitor_size[1] - 1
    
    # 시선방향으로 마우스 Move
    pyautogui.moveTo(x, y)

    global debug_execute_voice

    # 음성인식 준비가 되어있을때 실행
    if debug_execute_voice:
        debug_execute_voice = False # 음성인식이 중복실행되지 않도록 설정

        with sr.Microphone() as source:
            print("Say something!")
            audio = recognition.listen(source)

        try:
            transcript = recognition.recognize_google(audio, language=language) # ko-KR, en-US
        except sr.UnknownValueError:
            print("당신이 한말을 이해하지 못하였습니다.")
        except sr.RequestError as e:
            print("당신이 한말을 불러올 수 없습니다.; {0}".format(e))
        else: # 음성명령에 따라 마우스 제어 실행
            if transcript in ['이중선택', '이중 선택', 'double click', 'Double Click']:
                pyautogui.doubleClick()
            elif transcript in ['왼쪽선택', '왼쪽 선택', 'left click', 'Left Click']:
                pyautogui.click()
            elif transcript in ['오른쪽선택', '오른쪽 선택', 'right click', 'Right Click']:
                pyautogui.rightClick()
            print("당신이 했던 말 : " + transcript)
        finally:
            debug_execute_voice = True # 인식이 끝나면 다시 음성인식 준비상태로 설정
