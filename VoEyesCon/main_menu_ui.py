import threading
import tkinter as tk
from tkinter import *

class MainMenuUi(tk.Frame):
    def __init__(self,app):
        tk.Frame.__init__(self,app)

        tk.Label(self, text="VoEyes", font="HY헤드라인M 28 bold").grid(row=1,column=2,pady=30)

        from .focus_setting_ui import FocusSettingUi
        tk.Button(self, text='초점 재설정',bg='#9ABAA3',width=15,relief=FLAT,command=lambda: app.switch_frame(FocusSettingUi)).grid(row=2,column=2,pady=10)

        tk.Button(self, text='PC/랩탑 제어 실행',bg='#9ABAA3',width=15,relief=FLAT,command=lambda: plc_thread()).grid(row=3,column=2,pady=10)

        from .revise_account_ui import ReviseAccountUi
        tk.Button(self, text='회원정보 수정',bg='#9ABAA3',width=15,relief=FLAT,command=lambda: app.switch_frame(ReviseAccountUi)).grid(row=4,column=2,pady=10)

        from .user_setting_ui import UserSettingUi
        tk.Button(self, text='사용자 설정',bg='#9ABAA3',width=15,relief=FLAT,command=lambda: app.switch_frame(UserSettingUi)).grid(row=5,column=2,pady=10)

        from .system_setting_ui import SystemSettingUi
        tk.Button(self, text='시스템 설정',bg='#9ABAA3',width=15,relief=FLAT,command=lambda: app.switch_frame(SystemSettingUi)).grid(row=6,column=2,pady=10)

        # PC/LAPTOP 제어 모듈 실행
        def plc_execution():
            from .pc_laptop_control.src.elg_demo import PLC
            plc = PLC()
            plc.execution()

        # PC/LAPTOP 제어를 별도의 쓰레드로 실행
        def plc_thread():
            plc_execution_thread = threading.Thread(target=plc_execution, name='plc_execution')
            plc_execution_thread.daemon = True
            plc_execution_thread.start()
        
