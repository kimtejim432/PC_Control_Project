import pymysql
import random

# mysql 연결 객체 생성
def sql_init():
    conn = pymysql.connect(host='localhost',
                        user='root',
                        password='123123',
                        db='user',
                        charset='utf8')
    return conn

# 데이터베이스 값 전체 출력
def showDB():
    conn = sql_init()

    curs = conn.cursor()

    # users 테이블의 모든 정보를 출력
    sql = "SELECT * FROM user.users"
    curs.execute(sql)
    rows = curs.fetchall()   # sql문을 만족하는 모든 rows를 가져옴
    for row in rows:
        print(row)
    
# usersetting 값 가져오기
def show_usersetting(id):
    conn = sql_init()

    curs = conn.cursor()

    # 매개변수로 받은 변수를 id로 가진 row의 언어, x, y 좌표 설정 출력
    sql = "SELECT language, x, y FROM user.users WHERE id=%s"
    curs.execute(sql, id)
    language, x, y = curs.fetchone()   # sql문을 만족하는 1개의 row를 가져옴

    # 해당 설정값들을 반환하여 사용자의 설정 데이터를 불러옴
    return language, x, y

# 사용자 수 출력
def howmany():
    conn = sql_init()

    curs = conn.cursor()

    # users 테이블의 row 개수를 출력
    sql = "SELECT COUNT(*) FROM user.users"
    curs.execute(sql)
    rows = curs.fetchall()
    print(rows)

# 데이터 삽입 (회원가입)
def insert(id, password, email):
    conn = sql_init()

    curs = conn.cursor()
    
    # 회원가입 시, 사용자의 데이터를 DB에 추가
    sql = "INSERT INTO user.users (id, password, email, learning, language, x, y) VALUES (%s, %s, %s, 0, 'ko', 0, 0)"
    data = (id, password, email)
    curs.execute(sql, data)
    conn.commit()

# 데이터 삭제 (회원탈퇴)
def delete(id):
    conn = sql_init()
    curs = conn.cursor()
    
    # 매개변수값을 id로 가지는 row를 삭제
    sql = "DELETE FROM user.users WHERE id=%s"
    curs.execute(sql, id)
    conn.commit()

# 학습완료 시 학습여부 업데이트
def learning_complete(id):
    conn = sql_init()
    curs = conn.cursor()
    
    # 초점 학습을 완료했을 때 테이블의 learning column값을 1로 업데이트
    sql = "UPDATE user.users SET learning=1 WHERE id=%s"
    curs.execute(sql, id)
    conn.commit()

# ID/PW 찾기 시, 비밀번호를 랜덤 8자리로 초기화
def reset_password(email):
    conn = sql_init()
    curs = conn.cursor()

    password = ''
    password_length = 8

    special_char_bol = False
    number_char_bol = False

    lower_alphabet_list = [chr(x + 97) for x in range(26)]   # a 부터 z까지 소문자 list 생성
    number_char_list = [chr(x + 48) for x in range(10)]   # 0 부터 9까지 list 생성
    special_char_list = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '<', '>', '?', '/', '.', ',', ':', ';']
    total_char_list = lower_alphabet_list + number_char_list + special_char_list

    random.choice(total_char_list)
    for i in range(password_length):
        char = random.choice(total_char_list)   # total_char_list에서 1개의 문자를 가져옴

        if i == password_length - 2 or i == password_length - 1: # 숫자와 특수문자가 포함이 안되었을때를 대비
            if special_char_bol == False: # 특수문자가 하나라도 없을때
                char = random.choice(special_char_list)
                special_char_bol = True
            elif number_char_bol == False: # 숫자가 하나라도 없을때
                char = random.choice(number_char_list)
                number_char_bol = True
            else:
                char = random.choice(lower_alphabet_list)
        elif special_char_bol == False and (char in special_char_list): # char 변수의 값이 특수문자일때
            special_char_bol = True
        elif number_char_bol == False and (char in number_char_list): # char 변수의 값이 숫자일때
            number_char_bol = True
        else:
            char = random.choice(lower_alphabet_list)
        password += char

    # 초기화된 패스워드를 입력 받은 email 주소의 password column에 업데이트
    sql = "UPDATE user.users SET password = %s WHERE email = %s"
    data = (password, email)
    curs.execute(sql, data)
    conn.commit()

# 회원정보 수정
def update_userData(password, email, id):
    conn = sql_init()
    curs = conn.cursor()

    # 입력받은 데이터로 패스워드와 이메일 데이터를 변경
    sql = "UPDATE user.users SET password = %s, email = %s WHERE id = %s"
    data = (password, email, id)
    curs.execute(sql, data)
    conn.commit()

# ID 추출
def search_ID(email):
    conn = sql_init()
    curs = conn.cursor()

    # 입력받은 이메일 주소를 이용하여 id 데이터를 반환
    sql = "SELECT id FROM user.users WHERE email=%s"
    curs.execute(sql, email)
    id = curs.fetchone()

    return id

# PW 추출
def search_PW(email):
    conn = sql_init()
    curs = conn.cursor()

    # 입력받은 이메일 주소를 이용하여 password 데이터를 반환
    sql = "SELECT password FROM user.users WHERE email=%s"
    curs.execute(sql, email)
    password = curs.fetchone()

    return password

# User Setting 값 DB 반영
def save_usersetting(language, x, y, id):
    conn = sql_init()
    curs = conn.cursor()

    # 입력받은 language, x, y 데이터를 DB에 저장
    sql = "UPDATE user.users SET language=%s, x=%s, y=%s WHERE id=%s"
    data = (language, x, y, id)
    curs.execute(sql, data)
    conn.commit()