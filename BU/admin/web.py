import requests
import sys
from common import googleCode as gc
headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5","Cookie":"token=c7ebd817-d668-46eb-a80f-d5de9cd2f866; expire_time=20211029155728",
               "Accept": "application/json, text/plain, */*","Content-Type":"application/json","Connection":"close","Accept-Language":"zh-CN","X-Authorization":"","language":"Chinese"}
# Authorization='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI5MmU0Y2Y4ZC1hODdmLTQ4MTgtODJmMS0xNDgxYjYwOTRhMTAxMTEyODg0ODYzIiwidWlkIjoic1F6S2RTODJUN0dDeEluck1XSDBpUT09IiwiYmlkIjoibVdPTzdGMnpzTjBUd1JBeVFEbGsrQT09IiwiaXAiOiI4NFJ2dzRsWUo3SUZUamdLTDFZbjJ3PT0iLCJkZXYiOiJBOG9MTmVSVnZGR294TDlQWmVoa3BBPT0iLCJzdHMiOjAsImlhdCI6MTY3ODE4MDg3NywiZXhwIjoxNjc4MjY3Mjc3LCJpc3MiOiJ3Y3MifQ.mZjUU6EYebXG-NijCZ80bMKeCE_1f24sMnR89tIgEUo'
# headers['X-Authorization']=Authorization
url = 'https://test-public-rest.qkex.com'
account='10089@qq.com'
password='aa123456'
secret ='22CQPSL3ROAAN53K'


#登录
def userLoginVerify(account,password):
    params = {
        'account':account,
        'password':password,
    }
    path='/user/login/verify'
    # session = requests.Session()
    # session.post(url + path, data=params)
    # request_cookies = session.cookies.get_dict()
    # request_cookies = 'JSESSIONID=' + request_cookies['JSESSIONID']
    # headers['Cookie']=request_cookies
    res =requests.post(url=url+path,json=params,headers=headers).json()
    return res
def userLogin(account,password,verifyCode):
    params = {
        'account': account,
        'password': password,
        'verifyCode':verifyCode
    }
    path = '/user/login'
    res = requests.post(url=url + path, json=params, headers=headers).json()
    return res

#https://test.qkex.com/exchange/exchange
def exchange():
    path = '/exchange/exchange'
    params = {"baseSymbol":"ABC","googleVerifyCode":"411767","quoteSymbol":"USDT","amount":"2000"}



def getAccessToken(account,password,secret=None):
    res = userLoginVerify(account,password)
    if res['code']==0:
        if res['data']['verifyType']=='google' and secret !=None:
            code = gc.read_google_authenticator_code(secret)
        else:
            code = 111111
    else:
        print(res['msg'], '，请检查账号密码是否填写正确')
        sys.exit()
    res = userLogin(account,password,verifyCode=code)
    if res['code'] != 0:
        print(res['msg'],f'，请检查账号{account}的谷歌secret是否填写正确')
        sys.exit()
    accessToken = res['data']['accessToken']
    return accessToken

if __name__ == '__main__':
    print(getAccessToken(account,password,secret))
    print(userLoginVerify(account,password))
