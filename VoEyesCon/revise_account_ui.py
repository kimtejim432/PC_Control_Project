from tkinter import *
import tkinter as tk
import re
from tkinter import messagebox
from main_menu_ui import MainMenuUi

class ReviseAccountUi(tk.Frame):
    def __init__(self,app):
        tk.Frame.__init__(self,app)

        tk.Label(self, text="회원정보수정", font="HY헤드라인M 28 bold").grid(row=1,column=1,columnspan=3,pady=50)

        tk.Label(self, text=" PW ", bg='#9ABAA3',width=10).grid(row=4,column=2,pady=13,sticky="e")

        tk.Label(self, text=" E-mail ", bg='#9ABAA3',width=10).grid(row=5,column=2,pady=13,sticky="e")

        def passwordValidation(pwd):
            if len(pwd) < 8 or len(pwd) > 20:
                messagebox.showerror("비밀번호 입력 오류","비밀번호를 8-20자 사이로 정해주세요.")
                return False

            elif re.search('[0-9]+',pwd) is None:
                messagebox.showerror("비밀번호 입력 오류","비밀번호는 최소 1개 이상의 숫자를 포함해야 합니다.")
                return False

            elif re.search('[a-zA-Z]+',pwd) is None:
                messagebox.showerror("비밀번호 입력 오류","비밀번호는 최소 1개 이상의 영문 대소문자가 포함되어야 합니다.")
                return False

            elif re.search('[~!@#$%^&*()<>?/.,:;]+', pwd) is None:
                messagebox.showerror("비밀번호 입력 오류","비밀번호에 최소 1개 이상의 특수문자를 포함해야합니다.")
                return False
                
            else :
                return True

        def emailValidation(email):
            if re.search('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',email) is None:
                messagebox.showerror("이메일 입력 오류","올바른 형식으로 입력해주세요.")
                return False
            else :
                return True

        e2 = tk.Entry(self, font="함초롬돋움 12", width=16,show="*")
        e2.grid(row=4,column=3,sticky="w")

        e3 = tk.Entry(self, font="함초롬돋움 12", width=16)
        e3.grid(row=5,column=3,sticky="w")

        def print_fields():
            print("PW : %s\nE-mail : %s" % (e2.get(),e3.get()))
            if passwordValidation(e2.get()) == True and emailValidation(e3.get()) == True :
                messagebox.showinfo("회원정보 수정 완료","회원정보가 수정되었습니다.")
                app.switch_frame(MainMenuUi)
            else:
                pass
            
        tk.Button(self, font='함초롬돋움 12 bold',text='수정완료',bg="#9ABAA3",width=13,relief=FLAT,command=lambda:print_fields()).grid(row=10,column=2,padx=20,pady=40)
        tk.Button(self, text='돌아가기',bg='#EAEAEA', font='함초롬돋움 12 bold',width=13,relief=FLAT,command=lambda: app.switch_frame(MainMenuUi)).grid(row=10,column=3,padx=30,pady=40)