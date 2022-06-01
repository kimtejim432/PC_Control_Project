import tkinter as tk
from tkinter import *
from tkinter.messagebox import askquestion
from .sqltool import delete
import os

class SystemSettingUi(tk.Frame):
    def __init__(self,app):
        tk.Frame.__init__(self,app)

        tk.Label(self  , text="시스템 설정", font="HY헤드라인M 28 bold").grid(row=1,column=2,pady=50)

        from .login_ui import LoginUi
        tk.Button(self, text='로그아웃',bg='#9ABAA3',width=15,relief=FLAT,command=lambda: logout()).grid(row=2,column=2,pady=15)

        # 로그아웃 기능, 폴더 내 id_file.txt 삭제 및 LoginUI로 Frame 변경
        def logout():
            os.remove('VoEyesCon/id_file.txt')
            app.switch_frame(LoginUi)

        tk.Button(self, text='회원탈퇴',bg='#9ABAA3',width=15,relief=FLAT,command=lambda: user_delete()).grid(row=3,column=2,pady=15)

        # 회원탈퇴 기능, 폴더 내 id_file.txt 삭제 및 LoginUI로 Frame 변경
        def user_delete():
            result=askquestion("회원탈퇴", "회원탈퇴를 하시겠습니까?")
            if result == 'yes':
                try:
                    # id_file.txt 파일 내 ID 값 추출
                    with open('VoEyesCon/id_file.txt', 'r') as file:
                        id = file.read()
                        
                        
                #기능 에러, ID 파일이 존재하지 않을시 Error 메시지 출력.
                except FileNotFoundError:
                    print("id 파일이 존재하지 않습니다.")

                # id_file.txt 파일에서 추출한 ID값을 delete(id)를 통해 DB에서 삭제 후 id_file.txt 파일 삭제 및 LoginUI로 Frame 변경
                else: 
                    delete(id)
                    os.remove('VoEyesCon/id_file.txt')
                    print(id, "회원탈퇴 완료")
                    app.switch_frame(LoginUi)
                    
            else :
                pass

        from .main_menu_ui import MainMenuUi
        tk.Button(self, text='돌아가기',bg='#9ABAA3',width=15,relief=FLAT,command=lambda: app.switch_frame(MainMenuUi)).grid(row=4,column=2,pady=15)