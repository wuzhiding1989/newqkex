import time
import urllib.parse
import requests

def send_slack_message(message,channel):
    for i in range(2):
        r = send_messge(message,channel)
        if r.status_code == 200:
            break
def send_messge(content,channel):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    URL_Head='XYZB';URL_Head=URL_Head.replace('X', 'ho').replace('Y', 'oks.s').replace('Z', 'lac').replace('B', 'k.c')
    keyUrl_0 = 'ABCEFG';keyUrl_0= keyUrl_0.replace('ABC', 'T9P1H').replace('EFG', 'GSQP')
    keyUrl_1='ABCEFG';keyUrl_1=keyUrl_1.replace('ABC','B03T47').replace('EFG','DPDU4')
    keyUrl_2 = 'ABCEFG';keyUrl_2=keyUrl_2.replace('ABC','WekzCh7yo2o7').replace('EFG','FzzslEApTtH5')
    url='https://'+URL_Head+'om/services/'+keyUrl_0+'/'+keyUrl_1+'/'+keyUrl_2
    payload={"channel": channel, "username": "webhookbot", "text": " ", "icon_emoji": ":ghost:"}
    payload["text"]=content
    data = urllib.parse.quote(str(payload), encoding='utf-8', errors=None)
    data = 'payload={}'.format(data)
    response = requests.request("POST", url, headers=headers, data=data)
    return response

#单元测试：
# send_slack_message(" hello,world ! \n sun is comming. add 123")
