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

    sql = "SELECT * FROM user.users"
    curs.execute(sql)
    rows = curs.fetchall()
    for row in rows:
        print(row)
    
# usersetting 값 가져오기
def show_usersetting(id):
    conn = sql_init()

    curs = conn.cursor()

    sql = "SELECT language, x, y FROM user.users WHERE id=%s"
    curs.execute(sql, id)
    language, x, y = curs.fetchone()

    return language, x, y

# 사용자 수 출력
def howmany():
    conn = sql_init()

    curs = conn.cursor()

    sql = "SELECT COUNT(*) FROM user.users"
    curs.execute(sql)
    rows = curs.fetchall()
    print(rows)

# 데이터 삽입
def insert(id, password, email):
    conn = sql_init()

    curs = conn.cursor()
    
    sql = "INSERT INTO user.users (id, password, email, learning, language, x, y) VALUES (%s, %s, %s, 0, 'ko', 0, 0)"
    data = (id, password, email)
    curs.execute(sql, data) # try catch 문 사용 (예외처리)
    conn.commit()

# 데이터 삭제 (회원탈퇴 시 사용)
def delete(id):
    conn = sql_init()
    curs = conn.cursor()
    
    sql = "DELETE FROM user.users WHERE id=%s"
    curs.execute(sql, id)
    conn.commit()

# 학습완료 시 학습여부 업데이트
def learning_complete(id):
    conn = sql_init()
    curs = conn.cursor()
    
    sql = "UPDATE user.users SET learning=1 WHERE id=%s"
    curs.execute(sql, id)
    conn.commit()

# 언어 수정
def language_update(language, id):
    conn = sql_init()
    curs = conn.cursor()
    
    sql = "UPDATE user.users SET language=%s WHERE id=%s"
    data = (language, id)
    curs.execute(sql, data)
    conn.commit()

# x, y 좌표 수정
def coordinate_update(x, y, id):
    conn = sql_init()
    curs = conn.cursor()
    
    sql = "UPDATE user.users SET x=%s, y=%s WHERE id=%s"
    data = (x, y, id)
    curs.execute(sql, data)
    conn.commit()

# ID/PW 찾기 시, 비밀번호를 랜덤 8자리로 초기화
def reset_password(email):
    conn = sql_init()
    curs = conn.cursor()

    password = ''
    password_length = 8

    special_char_bol = False
    number_char_bol = False

    lower_alphabet_list = [chr(x + 97) for x in range(26)]
    number_char_list = [chr(x + 48) for x in range(10)]
    special_char_list = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '<', '>', '?', '/', '.', ',', ':', ';']
    total_char_list = lower_alphabet_list + number_char_list + special_char_list

    random.choice(total_char_list)
    for i in range(password_length):
        char = random.choice(total_char_list)

        if i == password_length - 2 or i == password_length - 1:
            if special_char_bol == False:
                char = random.choice(special_char_list)
                special_char_bol = True
            elif number_char_bol == False:
                char = random.choice(number_char_list)
                number_char_bol = True
            else:
                char = random.choice(lower_alphabet_list)
        elif special_char_bol == False and (char in special_char_list):
            special_char_bol = True
        elif number_char_bol == False and (char in number_char_list):
            number_char_bol = True
        else:
            char = random.choice(lower_alphabet_list)
        password += char

    sql = "UPDATE user.users SET password = %s WHERE email = %s"
    data = (password, email)
    curs.execute(sql, data)
    conn.commit()

# 회원정보 수정
def update_userData(password, email, id):
    conn = sql_init()
    curs = conn.cursor()

    sql = "UPDATE user.users SET password = %s, email = %s WHERE id = %s"
    data = (password, email, id)
    curs.execute(sql, data)
    conn.commit()

# ID 추출
def search_ID(email):
    conn = sql_init()
    curs = conn.cursor()

    sql = "SELECT id FROM user.users WHERE email=%s"
    curs.execute(sql, email)
    id = curs.fetchone()

    return id

# PW 추출
def search_PW(email):
    conn = sql_init()
    curs = conn.cursor()

    sql = "SELECT password FROM user.users WHERE email=%s"
    curs.execute(sql, email)
    password = curs.fetchone()

    return password

# User Setting 값 DB 반영
def save_usersetting(language, x, y, id):
    conn = sql_init()
    curs = conn.cursor()

    sql = "UPDATE user.users SET language=%s, x=%s, y=%s WHERE id=%s"
    data = (language, x, y, id)
    curs.execute(sql, data)
    conn.commit()