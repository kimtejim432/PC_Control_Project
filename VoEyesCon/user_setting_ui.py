from multiprocessing import Value
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import sqltool

class UserSettingUi(tk.Frame):
    def __init__(self,app):
        tk.Frame.__init__(self,app)
        tk.Label(self, text="사용자 설정", font="HY헤드라인M 25 bold").grid(row=1,column=1,columnspan=7,pady=50)

        tk.Label(self, text="언어 설정", font="HY헤드라인M 18").grid(row=2,column=2,columnspan=2, padx=55, pady=15)

        with open('FileSystem/id_file.txt', 'r') as file:
            id = file.read()
            language, x, y = sqltool.show_usersetting(id)

        ra = tk. StringVar()
        Ra1 = tk.Radiobutton(self, text="한국어", font="HY헤드라인M 12", variable=ra, value="ko")
        Ra1.grid(row=3,rowspan=2,column=2,pady=10,padx=7,sticky="e")

        Ra2 = tk.Radiobutton(self, text="영어", font="HY헤드라인M 12", variable=ra, value="en")
        Ra2.grid(row=3,rowspan=2,column=3,pady=10,padx=7,sticky="w")

        if language == 'ko':
            Ra1.select()
        else:
            Ra2.select()
        
        tk.Label(self, text="초점 설정", font="HY헤드라인M 18").grid(row=2,column=6,columnspan=2,pady=15,padx=65)

        tk.Label(self, text="X값", font="HY헤드라인M 12").grid(row=3,column=6)
        tk.Label(self, text="Y값", font="HY헤드라인M 12").grid(row=3,column=7)

        Cvalues=[i for i in range(-20,21)]

        ComboboxX = ttk.Combobox(self, width=5, values=Cvalues, justify=CENTER)
        ComboboxX.set(x)
        ComboboxX.grid(row=4,column=6,pady=5)
        
        ComboboxY = ttk.Combobox(self, width=5, values=Cvalues, justify=CENTER)
        ComboboxY.set(y)
        ComboboxY.grid(row=4,column=7,pady=5)

        def btnradio():
            with open('FileSystem/id_file.txt', 'r') as file:
                id = file.read()
            sqltool.save_usersetting(ra.get(), ComboboxX.get(), ComboboxY.get(), id)     # 설정값 저장
            print(ra.get())
            print("X : %s\nY : %s" % (ComboboxX.get(),ComboboxY.get()))
            app.switch_frame(MainMenuUi)

        from main_menu_ui import MainMenuUi
        tk.Button(self, text='저장하기',bg='#9ABAA3',font="함초롬돋움 12 bold",width=15,relief=FLAT,command=lambda: btnradio()).grid(row=5,column=1,columnspan=7,pady=40)