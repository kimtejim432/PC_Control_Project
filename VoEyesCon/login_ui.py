from tkinter import *
import tkinter as tk
from .find_account_ui import FindAccountUi
from .create_account_ui import CreateAccountUi
from .focus_setting_ui import FocusSettingUi
from tkinter import messagebox
from .sqltool import sql_init

# 로그인UI class 생성
class LoginUi(tk.Frame):
    def __init__(self, app):

        # 로그인 UI 구현
        tk.Frame.__init__(self,app)
        tk.Label(self, text="VoEyes", font="HY헤드라인M 28 bold").grid(row=1,column=6,pady=45)
        tk.Label(self, text=" ID ",font="HY헤드라인M 14", bg='#9ABAA3').grid(row=3,column=5,sticky="e",pady=13)
        tk.Label(self, text="PW",font="HY헤드라인M 14", bg='#9ABAA3').grid(row=4,column=5,sticky="e",pady=13)
        
        # ID 입력창
        IDEntry = tk.Entry(self, font="함초롬돋움 12", width=18)
        IDEntry.grid(row=3,column=6)

        # PW 입력창
        PWEntry = tk.Entry(self, width=18,font="함초롬돋움 12",show="*")
        PWEntry.grid(row=4,column=6)

        # 로그인 버튼(클릭 시 check_account 함수 실행)
        tk.Button(self, text='로그인',font='함초롬돋움 12 bold',bg="#9ABAA3",width=13,relief=FLAT,command=lambda: check_account()).grid(row=10,column=6,pady=30)

        # 회원가입 버튼(클릭 시 회원가입 UI로 전환)
        tk.Button(self, text='회원가입', font='함초롬돋움 10 underline', width=10,relief=FLAT,command=lambda: app.switch_frame(CreateAccountUi)).grid(row=15,column=5,padx=30,pady=20)
        
        # ID/PW 찾기 버튼(클릭 시 회원정보찾기 UI로 전환)
        tk.Button(self, text='ID/PW 찾기', font='함초롬돋움 10 underline',width=10,relief=FLAT,command=lambda: app.switch_frame(FindAccountUi)).grid(row=15,column=7,padx=30,pady=20)

        # 입력한 ID와 PW가 DB에 저장 되어 있는 데이터와 일치하는지 확인하는 check_account()함수 생성
        def check_account():
            print("ID : %s\nPW : %s" % (IDEntry.get(),PWEntry.get()))

            conn = sql_init()
            curs = conn.cursor()

            sql = "SELECT * FROM user.users WHERE BINARY id=%s AND BINARY password=%s" # BINARY는 대소문자 구분
            data = (IDEntry.get(), PWEntry.get())

            curs.execute(sql, data)

            if curs.fetchone():
                print("Successfully")
                
                with open("VoEyesCon/id_file.txt", 'w') as file: # id_file.txt를 생성하여 로그인한 사용자의 ID 기록
                    file.write(IDEntry.get())

                app.switch_frame(FocusSettingUi)
            else:
                print("Invalid Credentials")
                messagebox.showerror("로그인 오류","아이디 또는 패스워드가 일치하지 않습니다.")

    