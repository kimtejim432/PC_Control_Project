from tkinter import *

win = Tk() #창 생성

win.geometry("500x400")
win.title("GF-01")
win.option_add("*Font","함초롬돋움 15 bold")
win.configure(bg='#fff')

lab = Label(win, text="Gang of Four", fg='#9ABAA3', bg='#fff', font="맑은고딕 28 bold") # 라벨 내 텍스트 지정
lab.place(relx = 0.25, rely = 0.15)

# ID 라벨
lab1 = Label(win, text=" ID ", bg='#9ABAA3', fg='#fff') # 라벨 내 텍스트 지정
lab1.place(relx = 0.27, rely = 0.4)

# ID 입력창
ent1 = Entry(win, font="함초롬돋움 15", width=16)
ent1.insert(0, "아이디")
def clear(event):
    if ent1.get() == "아이디":
        ent1.delete(0,len(ent1.get()))
ent1.bind("<Button-1>", clear)
ent1.place(relx = 0.35, rely = 0.4)

# Password 라벨
lab2 = Label(win, text="PW", bg='#9ABAA3', fg='#fff')
lab2.place(relx = 0.27, rely = 0.5)

# Password 입력창
ent2 = Entry(win, width=16)
ent2.config(show = '*')
ent2.place(relx = 0.35, rely = 0.5)

btn1 = Button(win, text='로그인',width=13)
def login():
    my_id = ent1.get() # ID 입력창 내용
    my_pw = ent2.get() # Password 입력창 내용
    print(my_id, my_pw)
btn1.config(command = login)
btn1.configure(bg='#9ABAA3',fg='#fff')
btn1.place(relx = 0.33, rely = 0.66)

btn2 = Button(win, text='회원가입', font='함초롬돋움 10 bold', width=10)
btn2.configure(bg='#fff',fg='black')
btn2.place(relx = 0.285, rely = 0.8)

btn3 = Button(win, text='ID/PW 찾기', font='함초롬돋움 10 bold',width=10)
btn3.configure(bg='#fff',fg='black')
btn3.place(relx = 0.515, rely = 0.8)


win.mainloop() #창 실행