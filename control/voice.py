import speech_recognition as sr

r =  sr.Recognizer()

with sr.Microphone() as source:

    print('Speak Anything')
    audio = r.listen(source)

try:
    transcript=r.recognize_google(audio, language="ko-KR, en-US") # ko-KR, en-US
    print("당신이 했던 말 : "+transcript)
except sr.UnknownValueError:
    print("당신이 한말을 이해하지 못하였습니다.")
except sr.RequestError as e:
    print("당신이 한말을 불러올 수 없습니다.; {0}".format(e))