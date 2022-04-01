from tkinter import *
import tkinter as tk

from calibration import Calibration
import threading
import time

class FocusSettingUi(tk.Frame):
    
    def __init__(self,app):
        bool = False

        tk.Frame.__init__(self,app)

        tk.Label(self, text="초점을 맞추시겠어요?",font="HY헤드라인M 25").grid(row=3,column=1,columnspan=2,pady=10)

        if bool == False:
            string = "(최초 가입자는 필수)"
        else :
            string = "(적당한 문구)"
    
        L = tk.Label(self, text=string, font="HY헤드라인M 15")
        L.grid(row=2,column=1,columnspan=2,pady=50,sticky="s")

        tk.Button(self, font='함초롬돋움 11 bold',bg='#9ABAA3',text='예',width=15,relief=FLAT,command=lambda: caliMainMove()).grid(row=4,column=1,pady=45,padx=10)

        from main_menu_ui import MainMenuUi
        tk.Button(self, text='아니오', font='함초롬돋움 11 bold',bg='#EAEAEA',width=15,relief=FLAT,command=lambda: app.switch_frame(MainMenuUi)).grid(row=4,column=2,pady=45,padx=10)

        def caliMainMove():
            cali = Calibration()
            calibration_thread = threading.Thread(target=cali.caliExcusion, name='calibration_th2')
            calibration_thread.daemon = True
            calibration_thread.start()
            time.sleep(1)

            app.switch_frame(MainMenuUi)
            
    