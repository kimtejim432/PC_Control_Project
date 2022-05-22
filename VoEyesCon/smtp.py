def find_account(email):
    import smtplib
    from email.mime.text import MIMEText
    import sqltool


    sqltool.reset_password(email) # 비밀번호 초기화
    id = sqltool.search_ID(email)
    password = sqltool.search_PW(email)


    sender_id = 'ansrua45@gmail.com'
    sender_pw = 'jiehhplojdbzepbs'
    smtp_server = "smtp.gmail.com"

    smtp_info = {
        "smtp_server": smtp_server,  # SMTP 서버 주소
        "smtp_user_id": sender_id,
        "smtp_user_pw": sender_pw,
        "smtp_port": 587 # SMTP 서버 포트
        }

    to = email
    title = "VoEyesCon [ID/PW 찾기]"
    content = ["ID와 초기화된 PW를 전송합니다. \nID = %s \nPW = %s \n" %(id[0], password[0])]

    print('='*50)
    # 리스트로 받은 content를 \n로 조인하여 줄바꿈
    msg = MIMEText('\n'.join(content),_charset="utf8")

    msg['Subject'] = title  # 메일 제목
    msg['From'] = smtp_info['smtp_user_id']  # 송신자
    msg['To'] = to # 수신자
            
    smtp = smtplib.SMTP(smtp_info['smtp_server'], smtp_info['smtp_port'])
    smtp.ehlo # SMTP 식별
    smtp.starttls()  # TLS 보안 처리 (보안강화)
    smtp.login(sender_id , sender_pw)  # 로그인
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())

    smtp.quit()
    print('메일을 성공적으로 보냈습니다.')