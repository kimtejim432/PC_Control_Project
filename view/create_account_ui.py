from enum import Flag
from tkinter import *

win = Tk() #창 생성

win.geometry("500x400")
win.title("GF-01")
win.option_add("*Font","함초롬돋움 15 bold")
win.configure(bg='#fff')
win.resizable(width=False,height=False)

lab = Label(win, text="회원가입", fg='#9ABAA3', bg='#fff', font="맑은고딕 28 bold") # 라벨 내 텍스트 지정
lab.place(relx = 0.35, rely = 0.12)

lab1 = Label(win, text=" ID ", bg='#9ABAA3', fg='#fff', width=6) # 라벨 내 텍스트 지정
lab1.place(relx = 0.249, rely = 0.34)

lab2 = Label(win, text=" PW ", bg='#9ABAA3', fg='#fff',width=6) # 라벨 내 텍스트 지정
lab2.place(relx = 0.249, rely = 0.44)

lab3 = Label(win, text=" E-mail ", bg='#9ABAA3', fg='#fff',width=6) # 라벨 내 텍스트 지정
lab3.place(relx = 0.249, rely = 0.54)

ent1 = Entry(win, font="함초롬돋움 15", width=16)
ent1.insert(0, "이메일")
def clear(event):
    if ent1.get() == "이메일":
        ent1.delete(0,len(ent1.get()))
ent1.bind("<Button-1>", clear)
ent1.place(relx = 0.405, rely = 0.34)

ent2 = Entry(win, font="함초롬돋움 15", width=16)
ent2.insert(0, "이메일")
def clear(event):
    if ent2.get() == "이메일":
        ent2.delete(0,len(ent2.get()))
ent2.bind("<Button-1>", clear)
ent2.place(relx = 0.405, rely = 0.44)

ent3 = Entry(win, font="함초롬돋움 15", width=16)
ent3.insert(0, "이메일")
def clear(event):
    if ent3.get() == "이메일":
        ent3.delete(0,len(ent1.get()))
ent3.bind("<Button-1>", clear)
ent3.place(relx = 0.405, rely = 0.54)

btn1 = Button(win, font='함초롬돋움 10 bold',text='가입하기',width=17,relief=FLAT)
def Email():
    my_email = ent1.get()
    print(my_email)
btn1.config(command = Email)
btn1.configure(bg='#9ABAA3',fg='#fff')
btn1.place(relx = 0.205, rely = 0.7)

btn2 = Button(win, text='돌아가기', font='함초롬돋움 10 bold',width=17,relief=FLAT)
btn2.configure(bg='#EAEAEA',fg='black')
btn2.place(relx = 0.52, rely = 0.7)

win.mainloop() #창 실행