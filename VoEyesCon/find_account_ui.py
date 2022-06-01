from tkinter import *
import tkinter as tk
from .sqltool import sql_init
from .validation import emailValidation
from .smtp import find_account
from tkinter import messagebox

# 회원정보찾기UI class 생성
class FindAccountUi(tk.Frame) :
    def __init__(self, app):

        # 회원정보찾기UI 구현
        tk.Frame.__init__(self,app)

        tk.Label(self, text="ID/PW 찾기",  font="HY헤드라인M 28 bold").grid(row=1,column=1,columnspan=4,pady=50)
        tk.Label(self, text=" E-mail ",bg="#9ABAA3").grid(row=2,column=1,sticky="e",pady=30)
        
        # Email 입력창
        EmailEntry = tk.Entry(self, font="함초롬돋움 12", width=18)
        EmailEntry.grid(row=2,column=2,columnspan=2)

        # 회원정보를 보내주는 버튼 생성
        AccountSendButton = tk.Button(self, font='함초롬돋움 11 bold',bg="#9ABAA3",text='E-mail로 ID/PW 받기',width=17,relief=FLAT,command=lambda:send_account_imformation())
        AccountSendButton.grid(row=3,column=1,pady=30,padx=20,columnspan=2,sticky="w")

        # 저장된 회원정보를 보내주는 함수 send_account_imformation() 생성
        def send_account_imformation():
            print("E-mail : %s" % (EmailEntry.get()))

            if emailValidation(EmailEntry.get()) == True : # Email 유효성 검사 진행
                conn = sql_init()
                curs = conn.cursor()

                sql = "SELECT * FROM user.users WHERE BINARY email=%s" # BINARY는 대소문자 구분

                curs.execute(sql, EmailEntry.get())
                if curs.fetchone():
                    print("Successfully")
                    find_account(EmailEntry.get())
                    messagebox.showinfo("이메일 전송 완료","해당 이메일로 정보가 전송되었습니다.")
                    app.switch_frame(LoginUi)
                else:
                    print("Invalid Credentials")
                    messagebox.showerror("이메일 입력 오류","존재하지 않는 이메일입니다.")
        
        # 돌아가기 버튼(버튼 클릭 시 로그인 UI로 전환)
        from .login_ui import LoginUi
        tk.Button(self, text="돌아가기",bg='#EAEAEA', font='함초롬돋움 11 bold',width=17,relief=FLAT,command=lambda: app.switch_frame(LoginUi)).grid(row=3,column=3,padx=20,columnspan=2,sticky="e")