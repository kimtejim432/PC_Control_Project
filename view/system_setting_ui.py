from tkinter import *

win = Tk() #창 생성

win.geometry("500x400")
win.title("GF-01")
win.option_add("*Font","함초롬돋움 14 bold")
win.configure(bg='#fff')
win.resizable(width=False,height=False)

lab = Label(win, text="설정", fg='#9ABAA3', bg='#fff', font="맑은고딕 28 bold") # 라벨 내 텍스트 지정
lab.place(relx = 0.42, rely = 0.17)

btn1 = Button(win, text='로그아웃',width=15)
btn1.configure(bg='#9ABAA3',fg='#fff')
btn1.place(relx = 0.328, rely = 0.5)

btn2 = Button(win, text='회원탈퇴',width=15)
btn2.configure(bg='#9ABAA3',fg='#fff')
btn2.place(relx = 0.328, rely = 0.65)


win.mainloop() #창 실행