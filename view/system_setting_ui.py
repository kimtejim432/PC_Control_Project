import tkinter as tk
from tkinter import *

class SystemSettingUi(tk.Frame):
    def __init__(self,app):
        tk.Frame.__init__(self,app)

        tk.Label(self  , text="시스템 설정", font="HY헤드라인M 28 bold").grid(row=1,column=2,pady=50)

        from login_ui import LoginUi
        tk.Button(self, text='로그아웃',bg='#9ABAA3',width=15,relief=FLAT,command=lambda: app.switch_frame(LoginUi)).grid(row=2,column=2,pady=15)

        tk.Button(self, text='회원탈퇴',bg='#9ABAA3',width=15,relief=FLAT,command=lambda: app.switch_frame(LoginUi)).grid(row=3,column=2,pady=15)
        
        from main_menu_ui import MainMenuUi
        tk.Button(self, text='돌아가기',bg='#9ABAA3',width=15,relief=FLAT,command=lambda: app.switch_frame(MainMenuUi)).grid(row=4,column=2,pady=15)