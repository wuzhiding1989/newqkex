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
def read_google_authenticator_code(secret_key):
    """
    读取并返回谷歌身份验证器的动态验证码
    :param secret_key: 谷歌身份验证器的密钥
    :return: 动态验证码
    """
    totp = pyotp.TOTP(secret_key)
    current_time = int(time.time())
    return totp.at(current_time)


if __name__ == '__main__':
    # secret_key = 'KAYMZOHRHT2LO3VY'
    secret_key = '2KYSFNGE3YJCZGTS'

    print(read_google_authenticator_code(secret_key))