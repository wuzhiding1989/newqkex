from BU.spot.api import webapi as wb
from common import googleCode
import random,time
import BU.spot.api
headers1 = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5","Cookie":"token=c7ebd817-d668-46eb-a80f-d5de9cd2f866; expire_time=20211029155728",
               "Accept": "application/json, text/plain, */*","Content-Type":"multipart/form-data; boundary=----WebKitFormBoundaryDPGBW7MuZLcAyCfJ","Connection":"close","Accept-Language":"zh-CN","X-Authorization":"","language":"Chinese"}
s1='DBBGNEM3POXAYRSO'
y1='2K6E7WL5S3J2JSP7'
ytoken="eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIwNjA3M2ExMi00ZTJhLTRjOTUtYWUyYy04N2ZjNWIzMmU0YTgxMTIwNDMyNTA1IiwidWlkIjoiaDBsVXZiR0t2SkdkdGVscGYxQWRZUT09IiwiYmlkIjoibVdPTzdGMnpzTjBUd1JBeVFEbGsrQT09IiwiaXAiOiIzZU1oTTZVOXJuSllMNzNVQTdMeTl3PT0iLCJkZXYiOiJBOG9MTmVSVnZGR294TDlQWmVoa3BBPT0iLCJzdHMiOjAsImlhdCI6MTY5MTYzNDEwNywiZXhwIjoxNjkxNzIwNTA3LCJpc3MiOiJ3Y3MifQ.HZOfGJlFCa2TxyvWHGSEA9jOmuiZY-lt3R4jQacYU7Q"
stoken="eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJjMmYyZTg2MC0yZTk5LTQ3OTMtOTI3ZC00M2U2ZjYxMjViNDMyMDI3MTk2NDEzIiwidWlkIjoiT3dBa05jdFk5R1Jpcy9GekJaY2RkQT09IiwiYmlkIjoibVdPTzdGMnpzTjBUd1JBeVFEbGsrQT09IiwiaXAiOiIzZU1oTTZVOXJuSllMNzNVQTdMeTl3PT0iLCJkZXYiOiJBOG9MTmVSVnZGR294TDlQWmVoa3BBPT0iLCJzdHMiOjAsImlhdCI6MTY5MTYzNDE4NSwiZXhwIjoxNjkxNzIwNTg1LCJpc3MiOiJ3Y3MifQ.13R9K70nnpg_cChrcMXLmdQEtH0sZVZSTY0YV31gTto"

headers1['X-Authorization']=ytoken
def orderid1(side=None,symbol=None):
    res01 = wb.otc_orders_ads_select()
    oid = res01['data']
    tmpid=[]
    if symbol==None:
        for tmp in oid:
            if tmp['side'] == side :
                tmpid.append(tmp['id'])
        return tmpid
    else:
        for tmp in oid:
            if tmp['side'] == side and tmp['symbol']==symbol:
                tmpid.append(tmp['id'])
        return tmpid
def buy():
    try:
        d = format(random.uniform(0.003, 0.006), '.4f')
        d2 = format(random.uniform(10, 200), '.2f')
        #print(d,d2)
        orde=orderid1(side='sell')
        orde1 = orderid1(side='sell',symbol='USDT')
        orderid = random.choice(orde)
        amount = d2 if orderid == orde1[0] else d
        #print(1,orderid)
        res=wb.consumer_otc_pending(Authorization1=ytoken,orderId=orderid,amount=amount)
        print(res)
        time.sleep(1)
        res3=wb.consumer_my_order(Authorization1=ytoken,status=98,page=1,pageSize=1000)
        id=res3['data']['items'][0]['id']
        time.sleep(1)
        res1=wb.consumer_otc_pendings_paid(Authorization1=ytoken,orderid=id,payment=348)
        time.sleep(1)
        print(res1)
        gool=googleCode.read_google_authenticator_code(s1)
        res2=wb.otc_pendings_complete(orderid=id,googleVerifyCode=gool,tradePassword='q123456')
        print(res2)
    except Exception as e:
        print(e)

def sell():
    try:
        d = format(random.uniform(0.005, 0.009), '.4f')
        d2 = format(random.uniform(23, 200), '.2f')
        #print(d,d2)
        orde=orderid1(side='buy')
        orde1 = orderid1(side='buy',symbol='USDT')
        orderid = random.choice(orde)
        amount = d2 if orderid == orde1[0] else d
        gool = googleCode.read_google_authenticator_code(y1)
        rex=wb.otc_pending(orderId=orderid,amount=amount,tradePassword='q123456',googleVerifyCode=gool)
        print(rex)
        res3 = wb.consumer_my_order(Authorization1=stoken, status=98, page=1, pageSize=1000)
        id = res3['data']['items'][0]['id']
        res1 = wb.consumer_otc_pendings_paid(Authorization1=stoken, orderid=id, payment=353)
        print(res1)
        time.sleep(1)
        gool1 = googleCode.read_google_authenticator_code(y1)
        res2 = wb.otc_pendings_complete01(orderid=id, googleVerifyCode=gool1, tradePassword='q123456',headers=headers1)
        print(res2)
    except Exception as e:
        print(e)

def csf():
    res=wb.otc_bill(page=1,pageSize=100,type=13)
    data=res['data']
    # notes = data["bills"][0]["notes"]
    # amount = data["bills"][0]["amount"]
    # quantity = notes.split("Trade Quantity:")[1].split(",")[0]
    # print(quantity,amount)
    with open("output.txt", "w") as file:
        for bill in data["bills"]:
            notes = bill["notes"]
            amount = bill["amount"]
            quantity = notes.split("Trade Quantity:")[1].split(",")[0]
            file.write(f"{quantity},{amount}\n")

if __name__ == '__main__':
    #print(csf())
    for tm in range(90):
        print(buy())
        time.sleep(2)
        #print(sell())