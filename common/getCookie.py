"""
@author: xinkuncai
@license: (C) Copyright 2020-2099, Node Supply Chain Manager Corporation Limited.
@contact:  
@software: 
@file: getCookie
@time: 2023-05-04 
@desc: 
"""
import os

import jsonpath
import requests

from common.setting import ensure_path_sep

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
    file_path=ensure_path_sep("\\common\\")
    fileName=file_path+account+"cookie"
    if os.path.exists(fileName):
        print("1")

    else:
        f=open(fileName,"w")
        f.close()

    with open(fileName,"r",encoding="UTF-8") as f :
        cookie=f.readline()
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
               "Cookie": "token=c7ebd817-d668-46eb-a80f-d5de9cd2f866; expire_time=20211029155728",
               "Accept": "application/json, text/plain, */*",
               "Content-Type": "application/json",
               "Connection": "close",
               "Accept-Language": "zh-CN",
               "X-Authorization": cookie,
               "language": "Chinese"}
    url = "https://test-public-rest.qkex.com/wallet/currencies"
    res=requests.request(method="get",url=url,headers=headers)
    if res.json()["code"]==0:
        return cookie
    else:
        email(account)
        params = {
            'account':account,
            'password':password,
            'verifyCode':verifyCode

        }
        headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
                   "Accept": "application/json, text/plain, */*",
                   "Content-Type": "application/json",
                   "Connection": "close",
                   "Accept-Language": "zh-CN",
                   "language": "zh-CN"}
        url = 'https://test-public-rest.qkex.com'
        path='/user/login'
        # print("url",url+path)
        # print("params",params)
        # print("headers",headers)

        res =requests.post(url=url+path,json=params,headers=headers,verify=False).json()
        # print("res:",res)
        accessToken=res["data"]['accessToken']
        #把cookie写入文件
        with open(fileName,"w",encoding="UTF-8") as f:
            f.write(accessToken)
        return accessToken

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
    print("email-res:",res)
    return res



if __name__ == '__main__':
    res_data=login(account="12345678@qq.com",password="qa123456",verifyCode="111111")
    print(res_data)
    # print(jsonpath.jsonpath(res_data, "$.data.accessToken")[0])