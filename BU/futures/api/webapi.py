import copy
import requests

headers = {"Content-Type": "application/json","Accept-Language":"zh-CN","source":"web","X-Authorization":""}
Authorization='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyN2MwNjE5Zi04N2FlLTQ4ODEtYjFkMi1lODFlZGZjNzcxZmEiLCJ1aWQiOiJXWFAxUS8xa2s5NVQxTjRxOWxuSFRBPT0iLCJiaWQiOiJXWFAxUS8xa2s5NVQxTjRxOWxuSFRBPT0iLCJpcCI6IkdwdHl4M01ZbzBJemNsL3pwN0ZiNXc9PSIsImRldiI6InAva3BIckF3RkJjSUZleXg0U2xkZGc9PSIsInN0cyI6MCwiaWF0IjoxNjcyNTAyNDAwLCJleHAiOjE2ODgxNDA4MDAsImlzcyI6InFrZXgifQ.7HKuzZz-IC0_Zs5hVK420jVbgpsgRP-NlYtxrUiTs0U'
Authorization1='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJjMWQ0YmU4OC1kMTA4LTRjYmYtYjE4Ny00MzdmOWFmZGNjMzE4MDc2NDg0NzkiLCJ1aWQiOiJsN1ZkOHlLTCswQWxXcUU5TWJXcmpBPT0iLCJiaWQiOiJtV09PN0YyenNOMFR3UkF5UURsaytBPT0iLCJpcCI6ImRGbEkzdHBIV0l0emw2T2tMNEFKUFE9PSIsImRldiI6IkE4b0xOZVJWdkZHb3hMOVBaZWhrcEE9PSIsInN0cyI6MCwiaWF0IjoxNjgzMzQ0NzQ1LCJleHAiOjE2ODM0MzExNDUsImlzcyI6IndjcyJ9.WxpT2f6vHMazjm7EYsdcN4k20lIwl8KnsqoZ39GC4Go'
headers['X-Authorization']=Authorization
url = 'http://qraft-trade-api.qkex.com/v1'
url1 = 'http://172.31.31.223:18080'
account='10081@qq.com'
password='aa123456'
verifyCode='111111'
def futures_transfer():
    path = '/trade/web/account/transfer'
    parems = {
    "fromAccountType": "funding",
    "toAccountType": "futures",
    "currency": "USDT",
    "amount": "2.666666"}
    res = requests.post(url=url+path,json=parems,headers=headers).json()
    print(headers)
    print(url+path)
    return res
def futures_instruments():
    path ='/v1/public/web/instruments'
    res = requests.get(url=url+path,headers=headers)
    return res
def futures_instruments():
    path ='/v1/public/web/instruments'
    res = requests.get(url=url+path,headers=headers)
    return res

if __name__ == '__main__':
    print(futures_transfer())