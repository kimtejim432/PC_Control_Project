from tkinter import *

win = Tk() #창 생성

win.geometry("500x400")
win.title("GF-01")
win.option_add("*Font","함초롬돋움 12 bold")
win.configure(bg='#fff')
win.resizable(width=False,height=False)

lab = Label(win, text="Gang of Four", fg='#9ABAA3', bg='#fff', font="HY헤드라인M 28 bold") # 라벨 내 텍스트 지정
lab.place(relx = 0.25, rely = 0.15)

btn1 = Button(win, text='초점 재설정',width=15,relief=FLAT)
btn1.configure(bg='#9ABAA3',fg='#fff')
btn1.place(relx = 0.35, rely = 0.45)

btn2 = Button(win, text='PC/랩탑 제어 실행',width=15,relief=FLAT)
btn2.configure(bg='#9ABAA3',fg='#fff')
btn2.place(relx = 0.35, rely = 0.59)

btn3 = Button(win, text='사용자 설정',width=15,relief=FLAT)
btn3.configure(bg='#9ABAA3',fg='#fff')
btn3.place(relx = 0.35, rely = 0.73)


win.mainloop() #창 실행