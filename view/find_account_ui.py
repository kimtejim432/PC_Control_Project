from tkinter import *

win = Tk() #창 생성

win.geometry("500x400")
win.title("GF-01")
win.option_add("*Font","함초롬돋움 15 bold")
win.configure(bg='#fff')
win.resizable(width=False,height=False)

lab = Label(win, text="ID/PW 찾기", fg='#9ABAA3', bg='#fff', font="맑은고딕 28 bold") # 라벨 내 텍스트 지정
lab.place(relx = 0.31, rely = 0.15)

lab1 = Label(win, text=" E-mail ", bg='#9ABAA3', fg='#fff') # 라벨 내 텍스트 지정
lab1.place(relx = 0.25, rely = 0.42)

ent1 = Entry(win, font="함초롬돋움 15", width=16)
ent1.insert(0, "이메일")
def clear(event):
    if ent1.get() == "이메일":
        ent1.delete(0,len(ent1.get()))
ent1.bind("<Button-1>", clear)
ent1.place(relx = 0.405, rely = 0.42)

btn1 = Button(win, font='함초롬돋움 10 bold',text='E-mail로 ID/PW 받기',width=17)
def Email():
    my_email = ent1.get() # email 입력창 내용
    print(my_email)
btn1.config(command = Email)
btn1.configure(bg='#9ABAA3',fg='#fff')
btn1.place(relx = 0.205, rely = 0.7)

btn2 = Button(win, text='돌아가기', font='함초롬돋움 10 bold',width=17)
btn2.configure(bg='#fff',fg='black')
btn2.place(relx = 0.52, rely = 0.7)

win.mainloop() #창 실행