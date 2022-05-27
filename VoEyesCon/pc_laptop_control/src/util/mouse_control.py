import pyautogui

pyautogui.FAILSAFE = False
monitor_size = pyautogui.size()

def mouse_move(gaze_mean):
    x = gaze_mean[0] / 1280 * monitor_size[0]
    y = gaze_mean[1] / 720 * monitor_size[1]

    if x < 0: x = 0
    if y < 0: y = 0
    if x >= monitor_size[0]: x = monitor_size[0] - 1
    if y >= monitor_size[1]: y = monitor_size[1] - 1
    
    pyautogui.moveTo(x, y)
    print(x, y)
