import speech_recognition as sr

r =  sr.Recognizer()

with sr.Microphone() as source:

    print('Speak Anything')
    audio = r.listen(source)

    try:
        text = r.recognize_google(audio,language='ko-KR,en-US')
        print('당신이 한 말 : {}'.format(text))
    except:
        print('죄송합니다. 알아듣지 못했습니다.')