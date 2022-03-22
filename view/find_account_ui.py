from tkinter import *
import tkinter as tk

class FindAccountUi(tk.Frame) :
    def __init__(self, app):
        tk.Frame.__init__(self,app)

        tk.Label(self, text="ID/PW 찾기",  font="HY헤드라인M 28 bold").grid(row=1,column=1,columnspan=4,pady=50)
        tk.Label(self, text=" E-mail ",bg="#9ABAA3").grid(row=2,column=1,sticky="e",pady=30)
        tk.Entry(self, font="함초롬돋움 12", width=18).grid(row=2,column=2,columnspan=2)

        tk.Button(self, font='함초롬돋움 11 bold',bg="#9ABAA3",text='E-mail로 ID/PW 받기',width=17,relief=FLAT).grid(row=3,column=1,pady=30,padx=20,columnspan=2,sticky="w")


        from login_ui import LoginUi
        tk.Button(self, text="돌아가기",bg='#EAEAEA', font='함초롬돋움 11 bold',width=17,relief=FLAT,command=lambda: app.switch_frame(LoginUi)).grid(row=3,column=3,padx=20,columnspan=2,sticky="e")

        