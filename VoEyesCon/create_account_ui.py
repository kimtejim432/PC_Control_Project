from tkinter import *
import tkinter as tk
from tkinter import messagebox
from .validation import *
from .sqltool import insert

# 회원가입UI class 생성
class CreateAccountUi(tk.Frame):
    def __init__(self,app):

        # 회원가입 UI 구현
        tk.Frame.__init__(self,app)

        tk.Label(self, text="회원가입", font="HY헤드라인M 28 bold").grid(row=1,column=1,columnspan=3,pady=50)

        tk.Label(self, text=" ID ", bg='#9ABAA3', width=10).grid(row=3,column=2,pady=10,sticky="e")

        tk.Label(self, text=" PW ", bg='#9ABAA3',width=10).grid(row=4,column=2,pady=13,sticky="e")

        tk.Label(self, text=" E-mail ", bg='#9ABAA3',width=10).grid(row=5,column=2,pady=13,sticky="e")
        
        # ID 입력창
        IDEntry = tk.Entry(self, font="함초롬돋움 12", width=16)
        IDEntry.grid(row=3,column=3,sticky="w")

        # PW 입력창
        PWEntry = tk.Entry(self, font="함초롬돋움 12", width=16,show="*")
        PWEntry.grid(row=4,column=3,sticky="w")

        # Email 입력창
        EmailEntry = tk.Entry(self, font="함초롬돋움 12", width=16)
        EmailEntry.grid(row=5,column=3,sticky="w")

        # ID,PW,Email 입력창 값을 가져오는 print_fields 함수 생성
        def print_fields():
            print("ID : %s\nPW : %s\nE-mail : %s" % (IDEntry.get(),PWEntry.get(),EmailEntry.get()))
            if idValidation(IDEntry.get()) == True and passwordValidation(PWEntry.get()) == True and emailValidation(EmailEntry.get()) == True :
                try :
                    insert(IDEntry.get(),PWEntry.get(),EmailEntry.get())
                except :
                    messagebox.showerror("회원가입 오류","중복된 ID 또는 Email 입니다.")
                else :
                    messagebox.showinfo("회원가입 성공","환영합니다.")
                    print('회원가입 완료')
                    app.switch_frame(LoginUi)
            else:
                pass

        # 가입하기, 돌아가기 버튼 생성 (버튼 클릭 시 로그인 UI로 전환)
        tk.Button(self, font='함초롬돋움 12 bold',text='가입하기',bg="#9ABAA3",width=13,relief=FLAT,command=lambda:print_fields()).grid(row=10,column=2,padx=20,pady=40)
        from .login_ui import LoginUi
        tk.Button(self, text='돌아가기',bg='#EAEAEA', font='함초롬돋움 12 bold',width=13,relief=FLAT,command=lambda: app.switch_frame(LoginUi)).grid(row=10,column=3,padx=30,pady=40)