from multiprocessing import Value
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from .sqltool import show_usersetting, save_usersetting

class UserSettingUi(tk.Frame):
    def __init__(self,app):
        tk.Frame.__init__(self,app)
        tk.Label(self, text="사용자 설정", font="HY헤드라인M 25 bold").grid(row=1,column=1,columnspan=7,pady=50)

        tk.Label(self, text="언어 설정", font="HY헤드라인M 18").grid(row=2,column=2,columnspan=2, padx=55, pady=15)

        #id_file.txt 파일에서 language, x, y 불러오기
        with open('VoEyesCon/id_file.txt', 'r') as file:
            id = file.read()
            language, x, y = show_usersetting(id)

        #변수 입력 창
        SelectLanguage = tk. StringVar()

        #언어 선택 버튼
        KorButton = tk.Radiobutton(self, text="한국어", font="HY헤드라인M 12", variable=SelectLanguage, value="ko")
        KorButton.grid(row=3,rowspan=2,column=2,pady=10,padx=7,sticky="e")

        EngButton = tk.Radiobutton(self, text="영어", font="HY헤드라인M 12", variable=SelectLanguage, value="en")
        EngButton.grid(row=3,rowspan=2,column=3,pady=10,padx=7,sticky="w")

        # language의 value 값이 ko일시 KorButton, 아닐시 EngButton 선택
        if language == 'ko':
            KorButton.select()
        else:
            EngButton.select()
        
        tk.Label(self, text="초점 설정", font="HY헤드라인M 18").grid(row=2,column=6,columnspan=2,pady=15,padx=65)

        tk.Label(self, text="X값", font="HY헤드라인M 12").grid(row=3,column=6)
        tk.Label(self, text="Y값", font="HY헤드라인M 12").grid(row=3,column=7)

        #Values 범위 지정 -20 ~ 21
        Cvalues=[i for i in range(-20,21)]

        #X축 범위 Combobox
        ComboboxX = ttk.Combobox(self, width=5, values=Cvalues, justify=CENTER)
        ComboboxX.set(x)
        ComboboxX.grid(row=4,column=6,pady=5)
        
        #Y축 범위 Combobox
        ComboboxY = ttk.Combobox(self, width=5, values=Cvalues, justify=CENTER)
        ComboboxY.set(y)
        ComboboxY.grid(row=4,column=7,pady=5)

        #선택 언어, X축 범위, Y축 범위 저장 후 MainMenu Frame으로 변경
        def SaveSetting():
            with open('VoEyesCon/id_file.txt', 'r') as file:
                id = file.read()
            save_usersetting(SelectLanguage.get(), ComboboxX.get(), ComboboxY.get(), id)     # 설정값 저장
            print(SelectLanguage.get())
            print("X : %s\nY : %s" % (ComboboxX.get(),ComboboxY.get()))
            app.switch_frame(MainMenuUi)

        from .main_menu_ui import MainMenuUi
        tk.Button(self, text='저장하기',bg='#9ABAA3',font="함초롬돋움 12 bold",width=15,relief=FLAT,command=lambda: SaveSetting()).grid(row=5,column=1,columnspan=7,pady=40)