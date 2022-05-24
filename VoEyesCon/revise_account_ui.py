from tkinter import *
import tkinter as tk
from tkinter import messagebox
from main_menu_ui import MainMenuUi
import sqltool
import validation

class ReviseAccountUi(tk.Frame):
    def __init__(self,app):
        tk.Frame.__init__(self,app)

        tk.Label(self, text="회원정보수정", font="HY헤드라인M 28 bold").grid(row=1,column=1,columnspan=3,pady=50)

        tk.Label(self, text=" PW ", bg='#9ABAA3',width=10).grid(row=4,column=2,pady=13,sticky="e")

        tk.Label(self, text=" E-mail ", bg='#9ABAA3',width=10).grid(row=5,column=2,pady=13,sticky="e")

        e2 = tk.Entry(self, font="함초롬돋움 12", width=16,show="*")
        e2.grid(row=4,column=3,sticky="w")

        e3 = tk.Entry(self, font="함초롬돋움 12", width=16)
        e3.grid(row=5,column=3,sticky="w")

        def print_fields():
            print("PW : %s\nE-mail : %s" % (e2.get(),e3.get()))
            if validation.passwordValidation(e2.get()) == True and validation.emailValidation(e3.get()) == True :
                try :
                    with open('VoEyesCon/id_file.txt', 'r') as file:
                        id = file.read()
                    sqltool.update_userData(e2.get(), e3.get(), id)
                except :
                    messagebox.showerror("회원정보 수정 오류","이미 존재하는 이메일입니다.")
                else :
                    messagebox.showinfo("회원정보 수정 완료","회원정보가 수정되었습니다.")
                    app.switch_frame(MainMenuUi)

            else:
                pass
            
        tk.Button(self, font='함초롬돋움 12 bold',text='수정완료',bg="#9ABAA3",width=13,relief=FLAT,command=lambda:print_fields()).grid(row=10,column=2,padx=20,pady=40)
        tk.Button(self, text='돌아가기',bg='#EAEAEA', font='함초롬돋움 12 bold',width=13,relief=FLAT,command=lambda: app.switch_frame(MainMenuUi)).grid(row=10,column=3,padx=30,pady=40)