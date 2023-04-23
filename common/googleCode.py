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