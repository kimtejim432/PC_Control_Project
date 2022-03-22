from tkinter import *
import tkinter as tk

class FocusSettingUi(tk.Frame):
    def __init__(self,app):
        tk.Frame.__init__(self,app)

        tk.Label(self, text="초점을 맞추시겠어요?",font="HY헤드라인M 25").grid(row=3,column=1,columnspan=2,pady=10)

        tk.Label(self, text="(최초 가입자는 필수)", font="HY헤드라인M 15").grid(row=2,column=1,columnspan=2,pady=50,sticky="s")

        tk.Button(self, font='함초롬돋움 11 bold',bg='#9ABAA3',text='예',width=15,relief=FLAT).grid(row=4,column=1,pady=45,padx=10)
        
        from main_menu_ui import MainMenuUi
        tk.Button(self, text='아니오', font='함초롬돋움 11 bold',bg='#EAEAEA',width=15,relief=FLAT,command=lambda: app.switch_frame(MainMenuUi)).grid(row=4,column=2,pady=45,padx=10)