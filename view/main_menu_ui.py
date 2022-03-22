import tkinter as tk
from tkinter import *

class MainMenuUi(tk.Frame):
    def __init__(self,app):
        tk.Frame.__init__(self,app)

        tk.Label(self, text="VoEyes", font="HY헤드라인M 28 bold").grid(row=1,column=2,pady=45)

        from focus_setting_ui import FocusSettingUi
        tk.Button(self, text='초점 재설정',bg='#9ABAA3',width=15,relief=FLAT,command=lambda: app.switch_frame(FocusSettingUi)).grid(row=2,column=2,pady=10)

        tk.Button(self, text='PC/랩탑 제어 실행',bg='#9ABAA3',width=15,relief=FLAT).grid(row=3,column=2,pady=10)

        from user_setting_ui import UserSettingUi
        tk.Button(self, text='사용자 설정',bg='#9ABAA3',width=15,relief=FLAT,command=lambda: app.switch_frame(UserSettingUi)).grid(row=4,column=2,pady=10)

        from system_setting_ui import SystemSettingUi
        tk.Button(self, text='시스템 설정',bg='#9ABAA3',width=15,relief=FLAT,command=lambda: app.switch_frame(SystemSettingUi)).grid(row=5,column=2,pady=10)