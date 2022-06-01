from tkinter import *
import tkinter as tk
from VoEyesCon.login_ui import LoginUi

# UI 창 초기화
class SampleApp(tk.Tk):
    def __init__(self): # 초기화 및 로그인 UI 로딩
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginUi)

    def switch_frame(self, frame_class): # 다른 UI로 화면 전환
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

# 앱 실행
if __name__ == "__main__":
    app = SampleApp()
    app.geometry("500x400")
    app.title("VoEyes")
    app.option_add("*Font","HY헤드라인M 14")
    
    app.resizable(width=False,height=False)
    app.mainloop()
