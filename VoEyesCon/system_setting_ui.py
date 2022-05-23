import tkinter as tk
from tkinter import *
from tkinter.messagebox import askquestion
import sqltool
import os

class SystemSettingUi(tk.Frame):
    def __init__(self,app):
        tk.Frame.__init__(self,app)

        tk.Label(self  , text="시스템 설정", font="HY헤드라인M 28 bold").grid(row=1,column=2,pady=50)

        from login_ui import LoginUi
        tk.Button(self, text='로그아웃',bg='#9ABAA3',width=15,relief=FLAT,command=lambda: logout()).grid(row=2,column=2,pady=15)

        def logout():
            os.remove('VoEyesCon/id_file.txt')
            app.switch_frame(LoginUi)

        tk.Button(self, text='회원탈퇴',bg='#9ABAA3',width=15,relief=FLAT,command=lambda: user_delete()).grid(row=3,column=2,pady=15)
        def user_delete():
            result=askquestion("회원탈퇴", "회원탈퇴를 하시겠습니까?")
            if result == 'yes':
                try:
                    with open('VoEyesCon/id_file.txt', 'r') as file:
                        id = file.read()
                        
                except FileNotFoundError:
                    print("id 파일이 존재하지 않습니다.")

                else:
                    sqltool.delete(id)
                    os.remove('VoEyesCon/id_file.txt')
                    print(id, "회원탈퇴 완료")
                    app.switch_frame(LoginUi)
            else :
                pass

        from main_menu_ui import MainMenuUi
        tk.Button(self, text='돌아가기',bg='#9ABAA3',width=15,relief=FLAT,command=lambda: app.switch_frame(MainMenuUi)).grid(row=4,column=2,pady=15)