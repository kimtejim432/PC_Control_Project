import tkinter as tk
from tkinter import *

class UserSettingUi(tk.Frame):
    def __init__(self,app):
        tk.Frame.__init__(self,app)
        tk.Label(self, text="언어 설정", font="HY헤드라인M 28 bold").grid(row=1,column=2,columnspan=2,pady=60)

        ra = tk.IntVar()
        Ra1 = tk.Radiobutton(self, text="한국어", variable=ra, value=1)
        Ra1.grid(row=2,column=2,pady=10,padx=10)
        Ra1.select()

        Ra2 = tk.Radiobutton(self, text="영어", variable=ra, value=0)
        Ra2.grid(row=2,column=3,pady=10,padx=10)
        
        def btnradio():
            print(ra.get())
            app.switch_frame(MainMenuUi)

        from main_menu_ui import MainMenuUi
        tk.Button(self, text='저장하기',bg='#9ABAA3',font="함초롬돋움 12 bold",width=15,relief=FLAT,command=lambda: btnradio()).grid(row=3,column=2,columnspan=2,pady=60)