import imaplib
import email
import re
qq_email='615740359@qq.com'
password='dghxopveoxlobeff'
def get_qq_verification_code(qq_email, password):
    # 邮箱服务器地址
    server = 'imap.qq.com'
    # 连接邮箱服务器
    mail = imaplib.IMAP4_SSL(server)
    mail.login(qq_email, password)
    # 选择收件箱
    mail.select()
    # 搜索最新的邮件
    type, data = mail.search(None, 'ALL')
    latest_email_id = data[0].split()[-1]
    # 获取邮件内容
    type, data = mail.fetch(latest_email_id, '(RFC822)')
    raw_email = data[0][1].decode('utf-8')
    email_message = email.message_from_string(raw_email)
    # 获取验证码
    code = None
    for part in email_message.walk():
        content_type = part.get_content_type()
        if 'text' in content_type:
            text = part.get_payload(decode=True).decode()
            match = re.search(r'\d{6}', text)
            if match:
                code = match.group()
                break
    # 关闭连接
    mail.close()
    mail.logout()
    return code
if __name__ == '__main__':
    print(get_qq_verification_code(qq_email,password))