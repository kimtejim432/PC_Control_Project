from tkinter import *

win = Tk() #창 생성

win.geometry("500x400")
win.title("GF-01")
win.option_add("*Font","함초롬돋움 14 bold")
win.configure(bg='#fff')
win.resizable(width=False,height=False)

lab = Label(win, text="ID/PW 찾기", fg='#9ABAA3', bg='#fff', font="맑은고딕 28 bold") # 라벨 내 텍스트 지정
lab.place(relx = 0.32, rely = 0.15)

lab1 = Label(win, text=" E-mail ", bg='#9ABAA3', fg='#fff') # 라벨 내 텍스트 지정
lab1.place(relx = 0.255, rely = 0.42)

ent1 = Entry(win, font="함초롬돋움 14", width=16)
ent1.insert(0, "E-mail")
def clear(event):
    if ent1.get() == "E-mail":
        ent1.delete(0,len(ent1.get()))
ent1.bind("<Button-1>", clear)
ent1.place(relx = 0.405, rely = 0.42)

btn1 = Button(win, font='함초롬돋움 11 bold',text='E-mail로 ID/PW 받기',width=17,relief=FLAT)
def Email():
    my_email = ent1.get() # email 입력창 내용
    print(my_email)
btn1.config(command = Email)
btn1.configure(bg='#9ABAA3',fg='#fff')
btn1.place(relx = 0.165, rely = 0.7)

btn2 = Button(win, text='돌아가기', font='함초롬돋움 11 bold',width=17,relief=FLAT)
btn2.configure(bg='#EAEAEA',fg='black')
btn2.place(relx = 0.525, rely = 0.7)

win.mainloop() #창 실행