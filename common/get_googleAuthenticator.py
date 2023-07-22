"""
@author: xinkuncai
@license: (C) Copyright 2020-2099, Node Supply Chain Manager Corporation Limited.
@contact:  
@software: 
@file: get_googleAuthenticator
@time: 2023-05-15 
@desc: 
"""
import pyotp
import time
s_user='s001@cc.com';s_Googlekey='DBBGNEM3POXAYRSO';password='q123456'
y_user='y001@cc.com';y_Googlekey='2K6E7WL5S3J2JSP7';password='q123456'
def read_google_authenticator_code(secret_key):
    """
    读取并返回谷歌身份验证器的动态验证码
    :param secret_key: 谷歌身份验证器的密钥
    :return: 动态验证码
    """
    totp = pyotp.TOTP(secret_key)
    current_time = int(time.time())
    return totp.at(current_time)

# import pyotp
#
# # Replace this with your own secret key
# secret_key = '2KYSFNGE3YJCZGTS'
#
# # Generate a TOTP object
# totp = pyotp.TOTP(secret_key)
#
# # Get the current OTP
# otp = totp.now()
#
# print(otp)


if __name__ == '__main__':
    # secret_key = 'KAYMZOHRHT2LO3VY'
    #secret_key = '2KYSFNGE3YJCZGTS'
    for i in  range(20):
        print('商家',read_google_authenticator_code(s_Googlekey))
        print('用户',read_google_authenticator_code(y_Googlekey))
        time.sleep(20)