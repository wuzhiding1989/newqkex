# from slack_sdk import WebClient

# from slack_sdk.errors import SlackApiError
#用户token
headers4 = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5","Cookie":"token=c7ebd817-d668-46eb-a80f-d5de9cd2f866; expire_time=20211029155728",
               "Accept": "application/json, text/plain, */*","Content-Type":"application/x-www-form-urlencoded","Connection":"close","Accept-Language":"zh-CN","X-Authorization":"","language":"Chinese"}
Authorization4='eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyZWVkYmNiYi00ZDQyLTRlYzMtODRkYS00YWEwMDM1MjUxNGU3NzE1NjkzNDQiLCJ1aWQiOiJoMGxVdmJHS3ZKR2R0ZWxwZjFBZFlRPT0iLCJiaWQiOiJtV09PN0YyenNOMFR3UkF5UURsaytBPT0iLCJpcCI6InRFVmY2ZjY4TStDUm1QOVYrN0FIV1E9PSIsImRldiI6IkE4b0xOZVJWdkZHb3hMOVBaZWhrcEE9PSIsInN0cyI6MCwiaWF0IjoxNjgwODM1MzI1LCJleHAiOjE2ODA5MjE3MjUsImlzcyI6IndjcyJ9.gFkIM-HF-EEEmKpHFWw4B5W94R-AyOlZRyO06ItWgKw'
headers4['X-Authorization']=Authorization4
s_user='shangjia001@testcc.com';s_key='DBBGNEM3POXAYRSO';password='q123456'
y_user='yonghu001@testcc.com';y_key='2K6E7WL5S3J2JSP7'
posword='q123456'
user_secret_key='KVPO2AOTEHGCTBHO';mer_secret_key='IGMOVAGVYASVT52N';mer_email='125@gmail.com'
user_email='1255@gmail.com'
import json
import requests
# token='xoxb-5068079133173-5118181219971-y15tDTXdWjGHxWDDY3W4kBob'  #slack的token

token ='xoxb-5068079133173-5104401884982-qltWjSPtETvZ3gHiWMcvu3wU'
###'xoxb-5068079133173-5104401884982-ns0mCO4XoEbpamyLMmMip6CP'  'xoxb-5068079133173-5280684352613-ErmBxURkLmwUHovRB8XzjijU'
channel1='C05373RARLJ'  #slack的频道ID  D05KC16BDR7    test-api:C05373RARLJ   henry:D0584SW4JMU

def send_Slack(message):
    # token = 'xoxb-5068079133173-5280684352613-b5BYGOxC06kXzxyDq6E6skIt'
    # channel1 = 'C05373RARLJ' #slack的频道ID
    message=f'{message}'
    payload = {"text": message,"channel": channel1}
    data = json.dumps(payload).encode("utf8")
    url = 'https://slack.com/api/chat.postMessage'
    header = {"Content-Type": "application/json; charset=utf-8", "Authorization": "Bearer " + token}
    response = requests.post(url, data=data, headers=header)
    print(response.text)
if __name__ == "__main__":
    message = "测试 world11111 ! " #发送的消息
    send_Slack(message)