from tkinter import *
import tkinter as tk
from tkinter import messagebox
from .main_menu_ui import MainMenuUi
from .sqltool import update_userData
from .validation import *

class ReviseAccountUi(tk.Frame):
    def __init__(self,app):
        tk.Frame.__init__(self,app)

        tk.Label(self, text="회원정보수정", font="HY헤드라인M 28 bold").grid(row=1,column=1,columnspan=3,pady=50)

        tk.Label(self, text=" PW ", bg='#9ABAA3',width=10).grid(row=4,column=2,pady=13,sticky="e")

        tk.Label(self, text=" E-mail ", bg='#9ABAA3',width=10).grid(row=5,column=2,pady=13,sticky="e")

        PWEntry = tk.Entry(self, font="함초롬돋움 12", width=16,show="*")
        PWEntry.grid(row=4,column=3,sticky="w")

        EmailEntry = tk.Entry(self, font="함초롬돋움 12", width=16)
        EmailEntry.grid(row=5,column=3,sticky="w")

        def update_account():   # 회원정보를 수정하는 update_account 함수 생성
            print("PW : %s\nE-mail : %s" % (PWEntry.get(),EmailEntry.get()))
            if passwordValidation(PWEntry.get()) == True and emailValidation(EmailEntry.get()) == True :   # 패스워드, 이메일 유효성 검사
                try :
                    # 현재 로그인 하고 있는 id 값을 'id_file.txt'파일에서 가져와 매개변수로 사용
                    with open('VoEyesCon/id_file.txt', 'r') as file:
                        id = file.read()
                    update_userData(PWEntry.get(), EmailEntry.get(), id)   # 입력받은 이메일 주소와 패스워드 값을 DB에 반영
                except :
                    messagebox.showerror("회원정보 수정 오류","이미 존재하는 이메일입니다.")
                else :
                    messagebox.showinfo("회원정보 수정 완료","회원정보가 수정되었습니다.")
                    app.switch_frame(MainMenuUi)   # 메인메뉴 화면으로 이동

            else:
                pass
            
        tk.Button(self, font='함초롬돋움 12 bold',text='수정완료',bg="#9ABAA3",width=13,relief=FLAT,command=lambda:update_account()).grid(row=10,column=2,padx=20,pady=40)
        tk.Button(self, text='돌아가기',bg='#EAEAEA', font='함초롬돋움 12 bold',width=13,relief=FLAT,command=lambda: app.switch_frame(MainMenuUi)).grid(row=10,column=3,padx=30,pady=40)