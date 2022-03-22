from tkinter import *
import tkinter as tk

class CreateAccountUi(tk.Frame):
    def __init__(self,app):
        tk.Frame.__init__(self,app)

        tk.Label(self, text="회원가입", font="HY헤드라인M 28 bold").grid(row=1,column=1,columnspan=3,pady=50)

        tk.Label(self, text=" ID ", bg='#9ABAA3', width=10).grid(row=3,column=2,pady=10,sticky="e")

        tk.Label(self, text=" PW ", bg='#9ABAA3',width=10).grid(row=4,column=2,pady=13,sticky="e")

        tk.Label(self, text=" E-mail ", bg='#9ABAA3',width=10).grid(row=5,column=2,pady=13,sticky="e")

        tk.Entry(self, font="함초롬돋움 12", width=16).grid(row=3,column=3,sticky="w")

        tk.Entry(self, font="함초롬돋움 12", width=16).grid(row=4,column=3,sticky="w")

        tk.Entry(self, font="함초롬돋움 12", width=16).grid(row=5,column=3,sticky="w")

        tk.Button(self, font='함초롬돋움 12 bold',text='가입하기',bg="#9ABAA3",width=13,relief=FLAT).grid(row=10,column=2,padx=20,pady=40)
        from login_ui import LoginUi
        tk.Button(self, text='돌아가기',bg='#EAEAEA', font='함초롬돋움 12 bold',width=13,relief=FLAT,command=lambda: app.switch_frame(LoginUi)).grid(row=10,column=3,padx=30,pady=40)