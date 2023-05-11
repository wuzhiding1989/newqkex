import copy
import requests

headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5","Cookie":"token=c7ebd817-d668-46eb-a80f-d5de9cd2f866; expire_time=20211029155728",
               "Accept": "application/json, text/plain, */*","Content-Type":"application/json","Connection":"close","Accept-Language":"zh-CN","X-Authorization":"","language":"Chinese"}
Authorization='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxNzM3N2IyZi0wZGMwLTQ1MDgtYjBjOS0yNjM2NThiYTVkNmY3MDc5NTQyMTEiLCJ1aWQiOiJPd0FrTmN0WTlHUmlzL0Z6QlpjZGRBPT0iLCJiaWQiOiJtV09PN0YyenNOMFR3UkF5UURsaytBPT0iLCJpcCI6InRFVmY2ZjY4TStDUm1QOVYrN0FIV1E9PSIsImRldiI6IkE4b0xOZVJWdkZHb3hMOVBaZWhrcEE9PSIsInN0cyI6MCwiaWF0IjoxNjgzNzg3NTgyLCJleHAiOjE2ODM4NzM5ODIsImlzcyI6IndjcyJ9.x2poQdysZiXlz5qGPr_p3Tw62fO2FP7PgBjJWgoZYCE'
Authorization1='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJjMWQ0YmU4OC1kMTA4LTRjYmYtYjE4Ny00MzdmOWFmZGNjMzE4MDc2NDg0NzkiLCJ1aWQiOiJsN1ZkOHlLTCswQWxXcUU5TWJXcmpBPT0iLCJiaWQiOiJtV09PN0YyenNOMFR3UkF5UURsaytBPT0iLCJpcCI6ImRGbEkzdHBIV0l0emw2T2tMNEFKUFE9PSIsImRldiI6IkE4b0xOZVJWdkZHb3hMOVBaZWhrcEE9PSIsInN0cyI6MCwiaWF0IjoxNjgzMzQ0NzQ1LCJleHAiOjE2ODM0MzExNDUsImlzcyI6IndjcyJ9.WxpT2f6vHMazjm7EYsdcN4k20lIwl8KnsqoZ39GC4Go'
headers['X-Authorization']=Authorization
url = 'http://qraft-trade-api.qkex.com/v3'
url1 = 'http://172.31.31.223:18080'
account='10081@qq.com'
password='aa123456'
verifyCode='111111'
#/trade/account/transfer
def futures_transfer():
    path = '/trade/account/transfer'
    parems = {
    "fromAccountType": "funding",
    "toAccountType": "futures",
    "currency": "USDT",
    "amount": "2.666666"}
    res = requests.post(url=url+path,json=parems,headers=headers).json()
    return res
#/public/web/instruments
def futures_instruments():
    path ='/v1/public/web/instruments'
    res = requests.get(url=url1+path,headers=headers)
    return res
if __name__ == '__main__':
    print(futures_instruments())