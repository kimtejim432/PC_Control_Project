from enum import Flag
from tkinter import *

win = Tk() #창 생성

win.geometry("500x400")
win.title("GF-01")
win.option_add("*Font","함초롬돋움 14 bold")
win.configure(bg='#fff')
win.resizable(width=False,height=False)

lab = Label(win, text="초점을 맞추시겠어요?", fg='#9ABAA3', bg='#fff', font="맑은고딕 28 bold") # 라벨 내 텍스트 지정
lab.place(relx = 0.14, rely = 0.25)

lab = Label(win, text="(최초 가입자는 필수)", fg='#F1C40F', bg='#fff', font="맑은고딕 15 bold") # 라벨 내 텍스트 지정
lab.place(relx = 0.31, rely = 0.42)

btn1 = Button(win, font='함초롬돋움 11 bold',text='예',width=15,relief=FLAT)
btn1.configure(bg='#9ABAA3',fg='#fff')
btn1.place(relx = 0.2, rely = 0.6)

btn2 = Button(win, text='아니오', font='함초롬돋움 11 bold',width=15,relief=FLAT)
btn2.configure(bg='#EAEAEA',fg='black')
btn2.place(relx = 0.515, rely = 0.6)

win.mainloop() #창 실행