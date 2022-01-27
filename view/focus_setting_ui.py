from enum import Flag
from tkinter import *

win = Tk() #창 생성

win.geometry("500x400")
win.title("GF-01")
win.option_add("*Font","HY헤드라인M 28 bold")
win.configure(bg='#fff')
win.resizable(width=False,height=False)

lab = Label(win, text="초점을 맞추시겠어요?", fg='#9ABAA3', bg='#fff') # 라벨 내 텍스트 지정
lab.place(relx = 0.13, rely = 0.26)

lab = Label(win, text="(최초 가입자는 필수)", fg='#F1C40F', bg='#fff', font="HY헤드라인M 15") # 라벨 내 텍스트 지정
lab.place(relx = 0.3, rely = 0.44)

btn1 = Button(win, font='함초롬돋움 11 bold',text='예',width=15,relief=FLAT)
btn1.configure(bg='#9ABAA3',fg='#fff')
btn1.place(relx = 0.2, rely = 0.63)

btn2 = Button(win, text='아니오', font='함초롬돋움 11 bold',width=15,relief=FLAT)
btn2.configure(bg='#EAEAEA',fg='black')
btn2.place(relx = 0.515, rely = 0.63)

win.mainloop() #창 실행