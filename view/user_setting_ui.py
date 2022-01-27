from tkinter import *

win = Tk() #창 생성

win.geometry("500x400")
win.title("GF-01")
win.option_add("*Font","함초롬돋움 16 bold")
win.configure(bg='#fff')
win.resizable(width=False,height=False)

lab = Label(win, text="언어 설정", fg='#9ABAA3', bg='#fff', font="HY헤드라인M 28 bold") # 라벨 내 텍스트 지정
lab.place(relx = 0.334, rely = 0.17)

ra = IntVar()
rad1 = Radiobutton(win, text="한국어", variable=ra, value=1, bg='#fff')
rad1.place(relx=0.411, rely=0.38)
rad2 = Radiobutton(win, text="영어", variable=ra, value=2, bg='#fff')
rad2.place(relx=0.411, rely=0.5)

btn1 = Button(win, text='저장하기',font="함초롬돋움 12 bold",width=15,relief=FLAT)
btn1.configure(bg='#9ABAA3',fg='#fff')
btn1.place(relx = 0.355, rely = 0.72)

win.mainloop() #창 실행