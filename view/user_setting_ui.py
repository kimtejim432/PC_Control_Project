from tkinter import *

win = Tk() #창 생성

win.geometry("500x400")
win.title("GF-01")
win.option_add("*Font","함초롬돋움 14 bold")
win.configure(bg='#fff')
win.resizable(width=False,height=False)

lab = Label(win, text="사용자 설정", fg='#9ABAA3', bg='#fff', font="맑은고딕 30 bold") # 라벨 내 텍스트 지정
lab.place(relx = 0.29, rely = 0.16)

lab1 = Label(win, text=" 음성언어 ", bg='#fff')
lab1.place(relx = 0.23, rely = 0.43)

ra = IntVar()
rad1 = Radiobutton(win, text="한국어", variable=ra, value=1, bg='#fff')
rad1.place(relx=0.43, rely=0.42)
rad2 = Radiobutton(win, text="영어", variable=ra, value=2, bg='#fff')
rad2.place(relx=0.63, rely=0.42)


lab2 = Label(win, text="(변경하신 내용은 자동 저장됩니다.)", fg='#F1C40F', bg='#fff')
lab2.place(relx = 0.21, rely = 0.70)

win.mainloop() #창 실행