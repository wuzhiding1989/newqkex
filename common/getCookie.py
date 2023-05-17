"""
@author: xinkuncai
@license: (C) Copyright 2020-2099, Node Supply Chain Manager Corporation Limited.
@contact:  
@software: 
@file: getCookie
@time: 2023-05-04 
@desc: 
"""
import jsonpath
import requests
headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
           "Cookie":"token=c7ebd817-d668-46eb-a80f-d5de9cd2f866; expire_time=20211029155728",
            "Accept": "application/json, text/plain, */*",
           "Content-Type":"application/json",
           "Connection":"close",
           "Accept-Language":"zh-CN",
           "X-Authorization":"",
           "language":"Chinese"}
Authorization='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI5MmU0Y2Y4ZC1hODdmLTQ4MTgtODJmMS0xNDgxYjYwOTRhMTAxMTEyODg0ODYzIiwidWlkIjoic1F6S2RTODJUN0dDeEluck1XSDBpUT09IiwiYmlkIjoibVdPTzdGMnpzTjBUd1JBeVFEbGsrQT09IiwiaXAiOiI4NFJ2dzRsWUo3SUZUamdLTDFZbjJ3PT0iLCJkZXYiOiJBOG9MTmVSVnZGR294TDlQWmVoa3BBPT0iLCJzdHMiOjAsImlhdCI6MTY3ODE4MDg3NywiZXhwIjoxNjc4MjY3Mjc3LCJpc3MiOiJ3Y3MifQ.mZjUU6EYebXG-NijCZ80bMKeCE_1f24sMnR89tIgEUo'
headers['X-Authorization']=Authorization
url = 'https://test-public-rest.qkex.com'
account='12345678@qq.com'
password='qa123456'
verifyCode='111111'
#登录
def login(account=account,password=password,verifyCode=verifyCode):
    email(account)
    params = {
        'account':account,
        'password':password,
        'verifyCode':verifyCode

    }
    path='/user/login'
    res =requests.post(url=url+path,json=params,headers=headers,verify=False).json()
    # print("res:",res)
    accessToken=res["data"]['accessToken']
    return res

#登录headers
def login_headers(account=account,password=password,verifyCode=verifyCode,ContentType="application/json"):
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
               "Cookie": "token=c7ebd817-d668-46eb-a80f-d5de9cd2f866; expire_time=20211029155728",
               "Accept": "application/json, text/plain, */*",
               "Content-Type": "application/json",
               "Connection": "close",
               "Accept-Language": "zh-CN",
               "X-Authorization": "",
               "language": "Chinese"}
    email(account)
    params = {
        'account':account,
        'password':password,
        'verifyCode':verifyCode

    }
    path='/user/login'
    res =requests.post(url=url+path,json=params,headers=headers,verify=False).json()
    # print("res:",res)
    headers['X-Authorization']=res["data"]['accessToken']
    headers["Content-Type"]=ContentType
    # print("headers:,",headers)
    return headers


#登录时获取邮箱验证码
def email(email):
    params={
        "type": 3,
        "email": email,
        "countdownType": "signinEmail"}
    path='/user/send-code/email'
    res = requests.post(url=url+path,json=params,headers=headers,verify=False).json()
    return res



if __name__ == '__main__':
    res_data=login(account,password,verifyCode)
    # print(jsonpath.jsonpath(res_data, "$.data.accessToken")[0])