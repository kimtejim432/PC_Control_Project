from tkinter import *
import tkinter as tk
from find_account_ui import FindAccountUi
from create_account_ui import CreateAccountUi
from focus_setting_ui import FocusSettingUi
from tkinter import messagebox
from sqltool import sql_init

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginUi)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class LoginUi(tk.Frame):
    def __init__(self, app):
        tk.Frame.__init__(self,app)
        tk.Label(self, text="VoEyes", font="HY헤드라인M 28 bold").grid(row=1,column=6,pady=45)
        tk.Label(self, text=" ID ",font="HY헤드라인M 14", bg='#9ABAA3').grid(row=3,column=5,sticky="e",pady=13)
        tk.Label(self, text="PW",font="HY헤드라인M 14", bg='#9ABAA3').grid(row=4,column=5,sticky="e",pady=13)

        e1 = tk.Entry(self, font="함초롬돋움 12", width=18)
        e1.grid(row=3,column=6)

        e2 = tk.Entry(self, width=18,font="함초롬돋움 12",show="*")
        e2.grid(row=4,column=6)

        tk.Button(self, text='로그인',font='함초롬돋움 12 bold',bg="#9ABAA3",width=13,relief=FLAT,command=lambda: print_fields()).grid(row=10,column=6,pady=30)

        tk.Button(self, text='회원가입', font='함초롬돋움 10 underline', width=10,relief=FLAT,command=lambda: app.switch_frame(CreateAccountUi)).grid(row=15,column=5,padx=30,pady=20)
        
        tk.Button(self, text='ID/PW 찾기', font='함초롬돋움 10 underline',width=10,relief=FLAT,command=lambda: app.switch_frame(FindAccountUi)).grid(row=15,column=7,padx=30,pady=20)

        def print_fields():
            print("ID : %s\nPW : %s" % (e1.get(),e2.get()))

            conn = sql_init()
            curs = conn.cursor()

            sql = "SELECT * FROM user.users WHERE BINARY id=%s AND BINARY password=%s" # BINARY는 대소문자 구분
            data = (e1.get(), e2.get())

            curs.execute(sql, data)

            if curs.fetchone():
                print("Successfully")
                
                with open("VoEyesCon/id_file.txt", 'w') as file:
                    file.write(e1.get())

                app.switch_frame(FocusSettingUi)
            else:
                print("Invalid Credentials")
                messagebox.showerror("로그인 오류","아이디 또는 패스워드가 일치하지 않습니다.")

if __name__ == "__main__":
    app = SampleApp()
    app.geometry("500x400")
    app.title("VoEyes")
    app.option_add("*Font","HY헤드라인M 14")
    
    app.resizable(width=False,height=False)
    app.mainloop()

    