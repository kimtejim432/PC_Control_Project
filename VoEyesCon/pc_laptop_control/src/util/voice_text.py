import speech_recognition as sr
import pyautogui
import time

recognition = sr.Recognizer()

while True:

    with sr.Microphone() as source:
        print("Say something!")
        audio = recognition.listen(source)

    try:
        transcript = recognition.recognize_google(audio, language="ko-KR") # ko-KR, en-US
        if transcript in ['이중선택', '이중 선택']:
            pyautogui.doubleClick()
        elif transcript == '왼쪽 선택':
            pyautogui.click()
        elif transcript == '오른쪽 선택':
            pyautogui.rightClick()
        print("당신이 했던 말 : " + transcript)
    except sr.UnknownValueError:
        print("당신이 한말을 이해하지 못하였습니다.")
    except sr.RequestError as e:
        print("당신이 한말을 불러올 수 없습니다.; {0}".format(e))
    
                                    
