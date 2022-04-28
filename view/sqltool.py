import pymysql

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

# ID/PW 유효성 검사
import re

def pwdValidation(pwd):

    if len(pwd) < 8:
        print('비밀번호는 최소 8자 이상이어야 함')

    elif re.search('[0-9]+', pwd) is None:
        print('비밀번호는 최소 1개 이상의 숫자가 포함되어야 함')
        return False

    elif re.search('[a-zA-Z]+', pwd) is None:
        print('비밀번호는 최소 1개 이상의 영문 대소문자가 포함되어야 함')
        return False

    elif re.search('[`~!@#$%^&*(),<.>/?;]+', pwd) is None:
        print('비밀번호는 최소 1개 이상의 특수문자가 포함되어야 함')
        return False

    else :
        print('비밀번호 기준에 적합합니다')
        return True


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
        print('아이디 기준에 적합합니다')
        return True