from tkinter import *
import tkinter as tk
from VoEyesCon.login_ui import SampleApp

if __name__ == "__main__":
    app = SampleApp()
    app.geometry("500x400")
    app.title("VoEyes")
    app.option_add("*Font","HY헤드라인M 14")
    
    app.resizable(width=False,height=False)
    app.mainloop()
