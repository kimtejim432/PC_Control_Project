from tkinter import messagebox
import re

def idValidation(id):

    if len(id) < 5:
        print('아이디는 최소 5자 이상이어야 함')

    elif re.search('[`~!@#$%^&*(),<.>/?;]+', id):
        print('아이디에 특수문자를 포함시킬 수 없음')
        return False

    elif re.search('[a-zA-Z]+', id) is None:
        print('아이디는 최소 1개 이상의 영문 대소문자가 포함되어야 함')
        return False

    else :
        return True

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