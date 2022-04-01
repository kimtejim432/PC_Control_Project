from tkinter import *
import tkinter as tk

class CreateAccountUi(tk.Frame):
    def __init__(self,app):
        tk.Frame.__init__(self,app)

        tk.Label(self, text="회원가입", font="HY헤드라인M 28 bold").grid(row=1,column=1,columnspan=3,pady=50)

        tk.Label(self, text=" ID ", bg='#9ABAA3', width=10).grid(row=3,column=2,pady=10,sticky="e")

        tk.Label(self, text=" PW ", bg='#9ABAA3',width=10).grid(row=4,column=2,pady=13,sticky="e")

        tk.Label(self, text=" E-mail ", bg='#9ABAA3',width=10).grid(row=5,column=2,pady=13,sticky="e")

        e1 = tk.Entry(self, font="함초롬돋움 12", width=16)
        e1.grid(row=3,column=3,sticky="w")

        e2 = tk.Entry(self, font="함초롬돋움 12", width=16,show="*")
        e2.grid(row=4,column=3,sticky="w")

        e3 = tk.Entry(self, font="함초롬돋움 12", width=16)
        e3.grid(row=5,column=3,sticky="w")

        def print_fields():
            print("ID : %s\nPW : %s\nE-mail : %s" % (e1.get(),e2.get(),e3.get()))
            app.switch_frame(LoginUi)

        tk.Button(self, font='함초롬돋움 12 bold',text='가입하기',bg="#9ABAA3",width=13,relief=FLAT,command=lambda:print_fields()).grid(row=10,column=2,padx=20,pady=40)
        from login_ui import LoginUi
        tk.Button(self, text='돌아가기',bg='#EAEAEA', font='함초롬돋움 12 bold',width=13,relief=FLAT,command=lambda: app.switch_frame(LoginUi)).grid(row=10,column=3,padx=30,pady=40)