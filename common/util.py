import base64,datetime,gzip,hashlib,hmac,json,time,urllib.parse,requests,websocket,decimal,random,os
# from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
# from Crypto.PublicKey import RSA
# import websocket
import time,datetime,random;from decimal import *
from common.lacks import send_slack_message as sendSlack
import math

def request_http(method,url,params,WebToken=None,auth=None,log_level=0,op=None,source=None,token=None):
    if WebToken==None: WebToken='3a7647b9-e835-43c8-ab34-555c76fe1baf'
    #proxies 代理，根据需要放开
    proxies = None #{"http": "http://127.0.0.1:1087", "https": "http://127.0.0.1:1087"}
    #证书问题： 解决unable to get local issuer certificate (_ssl.c:1056) 因此设置False
    verify=False
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5","Accept-Encoding":"gzip, deflate, br","Cookie":"token=c7ebd817-d668-46eb-a80f-d5de9cd2f866; expire_time=20211029155728",
               "Accept": "application/json, text/plain, */*","Content-Type":"application/json","Connection":"close","Accept-Language":"zh-CN","source":"web","Authorization":WebToken,"language":"Chinese"}

    if source=='API': headers['source']=source;del headers['Authorization']
    if op == 'content': headers['Content-Type'] = ''
    if log_level==1 or log_level==3: print(url,json.dumps(params));  #json.dumps(params)
    if method=='get':
        try:
            headers['Content-Type']='application/x-www-form-urlencoded;charset=UTF-8'
            r = requests.get(url, params=params,headers=headers,auth=auth,timeout=5,proxies=proxies,verify=verify) #urllib.parse.urlencode(params) 转码
            # print('get请求:', r)
        except requests.exceptions.ReadTimeout:
            return 'timeout'
        except requests.exceptions.HTTPError:  # HTTP异常
            print('httperror',url,params)
        except Exception as e:
            # print([False,e])
            return [False,e]
        # except requests.exceptions.RequestException:  # 请求异常
        #     print('reqerror',url,params)
    elif method=='post':  #2022-08.15 add list、
        try:
            if type(params) in [dict,list]: r = requests.post(url, json=params,headers=headers,timeout=5,auth=auth,proxies=proxies,verify=verify) #字典和数组类型用json
            else: r = requests.post(url, data=params,headers=headers)#其他类型用data
            E = datetime.datetime.now();
            # print('post请求:', r)
        except requests.exceptions.ReadTimeout:
            print('请求超时: ',url,params)
        except Exception as e:
            print(e)
    elif method=='put': #2022-08.15 add list、
        if source == 'admin':
            headers['secret'] = op[0]
            headers['time'] = op[1]
            headers['Authorization'] = auth
        if type(params)in [dict,list]: r = requests.put(url, json=params,headers=headers,proxies=proxies,verify=verify)
        else: r = requests.put(url, data=params,headers=headers)
        # print('put请求:', r)
    elif method=='delete':
        if type(params)==dict: r = requests.delete(url, json=params,headers=headers,proxies=proxies,verify=verify)
        else: r = requests.delete(url,headers=headers)
    else:
        return '不被接受的方法，只支持get\post\delete'
    if op=='content': return r.content  #特殊需要解压使用的场景
    # print(1111,r.url)
    # print(222, r.request.body,str(r.request.body))
    # return r.json()
    if r.status_code == 200:    return r.json()
    elif r.status_code == 503:return [r.status_code,"<head><title>503 Service Temporarily Unavailable</title></head>"]
    else:   return [r.status_code,r.json()]


def dd(value,y=None,length=None):
    p=len(str(int(float(value))))
    if not length:
        length=28
    mycontext = Context(prec=p+length, rounding=ROUND_DOWN)  # ROUND_UP
    setcontext(mycontext)
    if y !=None:
        digits = y
        factor = 10 ** digits
        result = math.floor(value * factor) / factor
        return result
    return Decimal(value)
def printf(log_level=None):
    if log_level >= 2:
        print( ' 验证成功');
        # if Module: Count(Module, 1, Flag=True, TestResult=response)
        # return True
    else:
        # if Module: Count(Module, 1, Flag=True, TestResult=response)
        return True
def printl(log_level=None,P1='',P2='',response='',title='',Flag=True,RepCode='1',remark=None,Module=None):
    if response!='':
        if not response:
            if Module: Count(Module, 1, Flag=True, TestResult=response)
            printc(P1+' 验证失败,',response);
            LogOut(f'{P1}验证失败', 'py5.log');return False;
        elif  response!=True and response['code']!=RepCode:
            if remark :
                LogOut(remark.path+str(remark.param),'py5.log');
                LogOut(remark.result, 'py5.log');
            if Module: Count(Module, 1, Flag=True, TestResult=response)
            printc(P1 + ' 验证失败,预期',RepCode,'实际', response['code']+' '+response['message']);
            LogOut(f'{P1}验证失败 预期{RepCode} 实际 {response["code"]} {response["message"]}','py5.log')
            return False
        elif log_level>=2:
            print(P1 + ' 验证成功');
            if Module: Count(Module, 1, Flag=True, TestResult=response)
            return True
        else:
            if Module: Count(Module, 1, Flag=True, TestResult=response)
            return True


    #用于打印断言结果
    if log_level and log_level>=2:
        if Flag:
            print(P1,P2);return True
    if log_level:
        if  log_level!=3: print(P1,P2)
        if log_level>=3: print(title,response)
def printc(s=None,s1=None,s2=None,s3=None,s4=None,s5=None,s6=None,s7=None,s8=None,p_type=None):
    if s1 or s1==0: s=str(s)+str(s1)
    if s2 or s2==0: s = s + str(s2)+' '
    if s3 or s3==0: s = s + str(s3)+' '
    if s4 or s4==0: s = s + str(s4)+' '
    if s5 or s5==0: s = s + str(s5)+' '
    if s6 or s6==0: s = s + str(s6)+' '
    if s7 or s7==0: s = s + str(s7)+' '
    if s8 or s8==0: s = s + str(s8)+' '
    if p_type=='green':         print('\033[0;36;2m',s,'\033[0m ');
    elif p_type=='yellow':       print('\033[0;32;3m',s,'\033[0m ');
    else:                        print('\033[0;31;3m',s,'\033[0m ');

def compare(schema, r, title=None):
    compareResult = True;
    title_print = title[0] + title[1] + ' ' + title[2] + ' '
    for i in schema.keys():
        if i in r:
            if type(schema[i]) == str:  # 预期结果为字符串则直接对比，不符合预期则抛出
                if not r[i] == schema[i]:  printc(title_print, i, '=', r[i], ' 预期:', schema[i], ' 实际:',r[i]);compareResult = False
            if type(schema[i]) == type:  # 预期结果为数据类型则用类型对比，不符合预期则抛出
                if not type(r[i]) == schema[i]: printc(title_print, i, '=', r[i], ' 预期:', schema[i], ' 实际:',type(r[i]));compareResult = False
            if type(schema[i]) == dict:  # 预期结果为字典
                compare(schema[i], r[i], title=title)
            if type(schema[i]) == list:  # 预期结果为数组
                # print(title)
                for k in range(r[i].__len__()):  # 实际的数据可能存在多个数组需要遍历
                    if type(schema[i]) == list:
                        for j in range(schema[i].__len__()):  # 每个基础数组中对应的数据
                            if type(schema[i][j]) == list:
                                if schema[i][j].count(type(r[i][k][j])) > 0:
                                    pass  # 预期类型为多个类型
                                else:
                                    printc(title_print, k + 1, schema[i][j], r[i][k][j]); compareResult = False;  # exit()
                            elif type(schema[i][j]) == dict:
                                compareResult = compare(schema[i][j], r[i][k],title=title);  # #预期类型为字典
                            else:
                                # print(schema[i][j],r[i][k],j)
                                if schema[i][j] == type(r[i][k][j]):
                                    pass  # 预期类型为单个类型
                                else:
                                    printc(title_print, k + 1, schema[i][j], r[i][k][j]); compareResult = False;
                        if not compareResult: break
                        # if type(r[i][0][j]) in schema[i][j]:pass
                        # else:print(2,schema[i],schema[i][j],r[i][0])
                    elif type(schema[i]) == dict:
                        print(1111)  # compare(schema[i],r[i])
        else:
            printc(title_print, 'Key不存在', i, '实际:', r, p_type='green');
            compareResult = False;
    return compareResult
def subs(url, wsMsg,keyword=None,p_flag=None,topic=None):
    ws = websocket.create_connection(url)
    # sub_str = json.dumps(wsMsg)
    if type(wsMsg)==list:
        for Msg in wsMsg:
            ws.send(json.dumps(Msg))
    else:ws.send(json.dumps(wsMsg))
    s = 0
    for i in range(9999):
        r = json.loads(gzip.decompress(ws.recv()).decode())
        if  'ping' in r or 'ping' in str(r):
            nowTime = lambda: int(round(time.time() * 1000))
            ts = r['ping']
            ws.send('{"pong":' + str(ts) + '}')
        if 'ping' not in r:
            s=s+1;
            if topic=='req_kline':
                for klineData in r['data']:
                    klineData['id']=StampToTime(klineData['id'])
                    print(klineData)
            else: print(s,r)
def sub(url, subs, keyword=None,p_flag=None):
    try:
        import ssl
        # print(url,subs)#请求地址、订阅内容
        ws = websocket.create_connection(url,sslopt={"cert_reqs":ssl.CERT_NONE})

        sub_str = json.dumps(subs)
        if p_flag: print('\33[0;32;49m%s\33[0m' %f'\n\turl={url},{str(subs)}')
        s=bytes(sub_str,encoding='utf-8')
        a1={"method":"sub.contract","param":{}}
        a2={"method":"sub.personal.user.preference","param":{}};a3={
                "method": "ping"
            }
        s1=bytes(json.dumps(a1),encoding='utf-8')
        s2 = bytes(json.dumps(a2), encoding='utf-8')
        s3=bytes(json.dumps(a3), encoding='utf-8')
        # print(type(s))
        ws.send(s1);ws.send(s2);
        ws.send(s);
        r_status=False;
        for i in range(50):
            sub_result=ws.recv()
            print(sub_result)
            if "error" in sub_result: return (False,sub_result)
            if 'reply' in sub_result:
                if json.loads(sub_result)['status']=='ok':r_status=True
            if 'stream' in sub_result and 'status' not in sub_result: ws.close();return (True,json.loads(sub_result))
            # sub_result = json.loads(gzip.decompress(ws.recv()).decode()) #需要解压的ws数据

            # if keyword:
            #     for i in range(3):
            #         if keyword in str(sub_result):
            #             break
            #         else:
            #             if p_flag: print(f'返回数据中无关键key={keyword},实际结果={sub_result},第{i + 1}次重试……')
            #             sub_result = json.loads(gzip.decompress(ws.recv()).decode())
            #
            # result_info = '请求结果: \t' + str(sub_result)
            # if p_flag : print('\033[1;32;49m%s\033[0m' % result_info)
            ws.send(s3);
        ws.close()
        # return sub_result
    except Exception as e:
        print("Sub failed, detail is:%s" % e)
        return {"status": "fail", "msg": "%s" % e}
# 鉴权订阅
def api_key_sub(url, access_key, secret_key, subs, path='/notification'):
    host_url = urllib.parse.urlparse(url).hostname.lower()
    print(host_url)
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
    data = {
        "AccessKeyId": access_key,
        "SignatureMethod": "HmacSHA256",
        "SignatureVersion": "2",
        "Accept-language": "zh-CN",
        "Timestamp": timestamp
    }
    # sign = createSign(data, "GET", host_url, '/linear_swap_notification', secret_key)
    sign = createSign(data, "GET", host_url, path, secret_key)
    data["op"] = "auth"
    data["type"] = "API"
    data["cid"] = '11433583'
    data["Signature"] = sign
    try:
        ws = websocket.create_connection(url + path)
        msg_str = json.dumps(data)
        print("msg_str is:", msg_str)
        ws.send(msg_str)
        msg_result = json.loads(gzip.decompress(ws.recv()).decode())
        print("msg_result is:", msg_result)
        sub_str = json.dumps(subs)
        print("sub_str is:", sub_str)
        ws.send(sub_str)
        sub_result = json.loads(gzip.decompress(ws.recv()).decode())
        print("sub_result is :", sub_result)
        ws.close()
        return sub_result
    except Exception as e:
        print("Sub failed, detail is:%s" % e)
        return {"status": "fail", "msg": "%s" % e}
def createSign(pParams, method, host_url, request_path, secret_key):
    sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
    encode_params = urllib.parse.urlencode(sorted_params)
    payload = [method, host_url, request_path, encode_params]
    payload = '\n'.join(payload)
    payload = payload.encode(encoding='UTF8')
    secret_key = secret_key.encode(encoding='UTF8')
    digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    return signature
def apiKeyPost(url, request_path, params, ACCESS_KEY, SECRET_KEY):
    method = 'POST'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params_to_sign = {'AccessKeyId': ACCESS_KEY,'SignatureMethod': 'HmacSHA256','SignatureVersion': '2','Timestamp': timestamp}
    host_name = urllib.parse.urlparse(url).hostname
    host_name = host_name.lower()
    params_to_sign['Signature'] = createSign(params_to_sign, method, host_name, request_path, SECRET_KEY)
    url = url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
    return request_http('post',url, params)

def TimeToStamp(time_str):
    timeArray = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

def DatePlus(number=None, times=None, ZeroStart=None, period=None):
    defaultTimeGap = {'min': -1024, 'hour': -120, 'day': -7, 'week': -4, 'mon': -3}
    if not number: number=defaultTimeGap[period]
    if not times: times=datetime.datetime.now()#不传时间,则用当前时间
    else:times=datetime.datetime.strptime(times,"%Y-%m-%d %H:%M:%S")
    #功能2：获取当日凌晨开始
    if ZeroStart:
        if ZeroStart>1: HourInterval=str(ZeroStart-1);
        else: HourInterval=str(0)
        times=str(datetime.datetime.now())[:10]+f' {HourInterval}:00:00';times=datetime.datetime.strptime(times,"%Y-%m-%d %H:%M:%S")
    #获取时间 间隔
    if not period or period=="day":                  next_time=(times+datetime.timedelta(days=number))
    elif period=='hour':        next_time=(times+datetime.timedelta(hours=number))
    elif period == 'min': next_time = (times + datetime.timedelta(minutes=number))
    elif period == 'week':     next_time = (times + datetime.timedelta(weeks=number))
    #时间转换 标准格式
    next_time1=next_time.strftime("%Y-%m-%d %H:%M:%S")
    return next_time1
#调用示例：
#print(DatePlus(1,ZeroStart=True,period="day")) 请求1天后时间，从0点开始算

# 时间戳转换为时间
def StampToTime(timeStamp,type=None):
    if not type:
        dateArray = datetime.datetime.fromtimestamp(int(str(timeStamp)[0:]))  # 获取创建时间戳,并转换
        time = dateArray.strftime("%Y-%m-%d %H:%M:%S")  # 时间再次转换
        return  time
    if type=='MicroSecond':
        dateArray = datetime.datetime.fromtimestamp(int(str(timeStamp)[0:-3]))  # 获取创建时间戳,并转换
        time = dateArray.strftime("%Y-%m-%d %H:%M:%S")  # 时间再次转换
        return  time
def f(value,number):
    return format(value,'.'+str(number)+'f')

#首字母大写
def FirstUpper(str):
    return str[:1].upper()+str[1:]

#截取小数点,函数名称和mysql一致
def truncate(value,number,P=None):
    a=str(value).split('.');
    if number==0: return a[0]
    if len(a)==1: return value
    else:
        if len(a[1])<number: number=len(a[1])
        l=a[1][0:number]
        aa=float(a[0] + '.' + l)
        if P: aa=a[0] + '.' + l
        return aa

def getPeriodStamp(period):
    if 'min' in period: return int(period[:-3])*60
    if 'hour' in period: return int(period[:-4]) * 60*60
    if 'day' in period: return int(period[:-3]) * 60 * 60*24
    if 'week' in period: return int(period[:-4]) * 60 * 60 * 24*7
    if 'mon' in period: return int(period[:-4]) * 60 * 60 * 24 * 30
def log(log_level,url,params,result):
    if log_level in [1, 3]: print(url, params);
    if log_level in [2, 3]: print(json.dumps(result))
    return json.dumps(result)

#转换位大数据类型，解决python精度容易丢失的问题 Author: Brian
#ROUND_CEILING：如果Decimal为正，则做ROUND_UP操作；如果Decimal为负，则做ROUND_DOWN操作；
# ROUND_FLOOR：如果Decimal为负，则做ROUND_UP操作；如果Decimal为正，则做ROUND_DOWN操作；
# 5)ROUND_HALF_DOWN：如果舍弃部分>.5，则做ROUND_UP操作；否则，做ROUND_DOWN操作；
# 6)ROUND_HALF_UP：如果舍弃部分>=.5，则做ROUND_UP操作；否则，做ROUND_DOWN操作；
# 7)ROUND_HALF_EVEN：如果舍弃部分左边的数字是奇数，则做ROUND_HALF_UP操作；若为偶数，则做ROUND_HALF_DOWN操作；
def d(value,length=None):
    p=len(str(int(float(value))))
    if not length: length=28
    mycontext = Context(prec=p+length, rounding=ROUND_DOWN)  # ROUND_UP
    setcontext(mycontext)
    return Decimal(value)

def Json5(json,values):
    for value in values:
        json[value[0]]=value[1]
    return json

def t():
  return  str(datetime.datetime.now())[:-7]
#通过买一,买二价差，获取随机的一个中间价差
def priceSpread(price,precision=2):
    # price = 1.234
    precisionDict={1:0.1,2:0.01,3:0.001,4:0.0001,5:0.00001,6:0.000001}
    if '.' not in str(price): price = float(str(price) + '.0')
    _price_temp = str(price).split('.')
    if _price_temp[0] == '0':
        _priceSpread = random.randint(0, int(_price_temp[1]))
        return float(_priceSpread * precisionDict[precision])
    else:
        _price = random.randint(1, int(price))
        price_little = float('0.' + _price_temp[1])
        price_little2 = random.random()
        return float(truncate(_price - 1 + price_little2, precision))
# ~~ 检查文件夹/文件是否存在，并自动创建
def mk(filename,option=None):
 _filename=''
 # -- 如果传入excel文件的绝对路径，单独处理
 if '.xls' in filename:
     fileSplit=filename.split('/')
     #将绝对路径拆分为：路径、文件名称
     for i in range(fileSplit.__len__()):
         if fileSplit[i]!='' and i!=fileSplit.__len__()-1:
            _filename=_filename+'/'+filename.split('/')[i]
            # 检查路径是否存在，不存在则自动创建
            if not os.path.exists(_filename):
                 os.mkdir(_filename)
                 with open(filename,mode='wb') as f    :  pass
     # with open(_filename+'/'+option+'.'+filename.split('.')[1],mode='w',newline='') as f    :
     #     command='mv '+_filename+'/'+option+'.'+filename.split('.')[1]+' '+_filename+'/'+fileSplit[fileSplit.__len__()-1]
     #     print(command)
     #     os.system(command)
 else:
    if not os.path.exists(filename):
        os.mkdir(filename)
global _all,_pass
_all=0;_pass=0;_block=0;caseNumber=[];current_case_number=0;otherCase={}
CaseSummary={}


def Count(Mode=None,All=None,Pass=None,Fail=None,Block=None,summary=None,log_level=None,SendSlack=None,title='',TestResult=None,Flag=None,ModuleName=''):
    if not summary:
        if Mode not in CaseSummary:
            if not Flag:  CaseSummary[Mode]=[All,Pass,Fail,Block]
            else:
                if TestResult :
                    CaseSummary[Mode]=[All,All,0,0]
                else: CaseSummary[Mode]=[All,0,All,0]
        else:
            if not Flag:
                CaseSummary[Mode][0] = CaseSummary[Mode][0] + All
                CaseSummary[Mode][1] = CaseSummary[Mode][1] + Pass
                CaseSummary[Mode][2] = CaseSummary[Mode][2] + Fail
                CaseSummary[Mode][3] = CaseSummary[Mode][3] + Block
            else:
                if TestResult : #成功时，用例数、成功数在原有基础上增加
                    CaseSummary[Mode][0]=CaseSummary[Mode][0]+All;
                    CaseSummary[Mode][1] = CaseSummary[Mode][1] + All;
                else: #失败时，用例数、失败数在原有基础上增加
                    CaseSummary[Mode][0]=CaseSummary[Mode][0]+All;
                    CaseSummary[Mode][2] = CaseSummary[Mode][2] + All;
    else:
        _All =0;_Pass=0;_Fail=0;_Block=0
        for i in CaseSummary:
            c=CaseSummary[i]
            CaseSummary[i].append(str(truncate(c[1]/c[0] * 100, 2)) + '%')
            if log_level and log_level==2:  print(i,CaseSummary[i])
            _All=_All+CaseSummary[i][0]
            _Pass = _Pass + CaseSummary[i][1]
            _Fail = _Fail + CaseSummary[i][2]
            _Block = _Block + CaseSummary[i][3]
        print(ModuleName+'case总数:',_All,'通过:',_Pass,'失败:',_Fail,'阻塞:',_Block,'通过率:', str(truncate(_Pass / _All * 100, 2)) + '%')
        aa=str(truncate(_Pass / _All * 100, 2))
        if SendSlack:
            testResult = f'case总数:{_All} 通过: {_Pass}, 失败: {_Fail}  阻塞: {_Block} 通过率: {aa}%'
            sendSlack(title+testResult, 'trade-qa-team')
        return [_All,_Pass,_Fail,_Block]
#获取操作系统：Mac、Windows、Linux        Author：Brian
def GetVersion():
    import platform
    #print(platform.uname())#All system Info
    symtem=platform.system().lower()
    if 'darwin' in symtem: return "Mac"
    elif "windows" in symtem : return "Windws"
    elif "linux" in symtem: return "Linux"
    else: return "Unkown Symstem"
def ModeCount(Flag,Mode=None,All=None,Pass=None,Fail=None,Block=None):
    if Flag:
        Count(Mode,1,1,0,0)
    else:
        Count(Mode, 1, 0, 1, 0)

#定向输入日志        Author：Brian
def LogOut(remark,fileName):
    log_path = os.path.join(os.path.split(os.path.split(os.path.realpath(__file__))[0])[0],'log')
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    s = os.getcwd()
    #在其他路径执行时，Mac电脑自动识别出日志路径，Windows暂无
    if not 'py5' in s:
        s=s.split('/')
        s='/Users/'+s[2]+'/py5' if GetVersion()=='Mac' else 12345
    commands='echo ' + str(datetime.datetime.now())[:-3] +'\' '+ str(remark)+'\' >>' + s[:s.find('py5') + 3] + '/log/'+fileName
    a1 = os.system(commands)
# LogOut('1123','py5.log');time.sleep(10000)WWWWWW
def LogOuts(NTS,Title,LogName):
    LogOut(NTS.path + json.dumps(NTS.param),LogName)
    LogOut(json.dumps(NTS.result), LogName)
    if Title !=None:
        LogOut(Title.replace('<','_').replace('>','_'),LogName)

#自增长
def countCaseNumber(Flag,option=None,all=0,pass_=0,block=0,p=None,log_level=None):
    global _all,_pass,_block;_all = _all + 1;_all=_all+all;_block=_block+block;_pass=_pass+pass_
    if Flag:
        _pass=_pass+1
        if option: _all=_all+option;_pass=_pass+option
    elif option:_block=_block+option
    if not log_level: log_level=0;
    if p and log_level>=1 and Flag:
        print(p+'成功')

def currentCaseNumber(title):
    global current_case_number
    if _all - current_case_number>0:
        caseNumber.append([title,_all - current_case_number])
    current_case_number = _all

def 倒计时():
    for K in range(0, 10, 1):
        for i in range(10):
            u(random.choice([1, 0, 0]))
        rate=str(truncate(_pass / _all*100,2))
        print(f'\r 次数:{K + 1} 成功率：{rate}%...', end='')
        time.sleep(3)
#解码
def unquote(string):
    # string1={"code": "1006", "message": "\u4ea4\u6613\u5bf9\u4e0d\u5b58\u5728\uff0c\u8bf7\u4fee\u6539", "ts": 1663757859360}
    # # print(type(string),type(string1))
    # print(urllib.parse.unquote(str(string)),urllib.parse.unquote(string1))
    return urllib.parse.unquote(str(string))

#编码
def quote(string):
    return urllib.parse.quote(string)

#当前时间 毫秒维度
def currentTime(Flag=None):
    return str(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f"))

def decimalLength(number,zeroFlag=True):
    if '.' in str(number):
        number_new=str(number).split('.')
        if float(number_new[1])==0: return 0  #小数点后面全是0，则小数位为0
        else:
            number_new[1]=float('0.'+number_new[1]) #将小数点后面的数值 转换为float类型
            return len(str(number_new[1]))-2 #长度需要去掉0.的长度
    else:
        return 0
def RabbitMq_WebRquest(SymbolList=None,PriceList=None,ForNumer=1):
    SendNumber=0
    for j in range (ForNumer):
        markPrice=[['BTCUSDT',20600,20300],['ETHUSDT',1600,1580]]
        if SymbolList and SymbolList.__len__()>=1:
            for i in range(SymbolList.__len__()):
                markPrice[i][0]=SymbolList[i]
                markPrice[i][1] = str(PriceList[i][0])
                markPrice[i][2] = str(PriceList[i][1])
        for i in markPrice:
            SendNumber+=1
            p={"vhost":"/","name":"qa_mulan_inner_price","properties":{"delivery_mode":1,"headers":{}},"routing_key":"","delivery_mode":"1","payload":"{\"symbol\":\"BTCUSDT\",\"tradeType\":\"linearPerpetual\",\"index\":20000,\"mark\":20600,\"market\":20008.27,\"time\":1663248760,\"scale\":2,\"options\":null,\"quotes\":null,\"fundingRate\":-0.0018830852,\"fundingHours\":2.46,\"fundingRateLimit\":-0.0018830852,\"nextFundingTime\":1663257600000}","headers":{},"props":{},"payload_encoding":"string"}
            url='https://mq.nts.aaxbtc.com/api/exchanges/%2F/qa_mulan_inner_price/publish'
            header['authorization']='Basic YWRtaW46Z3NONnNPRkxnOE5UbFFIMg=='
            p['payload']=p['payload'].replace('20600',str(i[1])).replace('20000',str(i[2])).replace('BTCUSDT',i[0])
            r=requests.post(url,json=p,headers=header)
            print(SendNumber,t(),i,r.text);
            if ForNumer>1: time.sleep(60)
    # print(decimalLength('1.003000000000000000')) 单元测试
if __name__ == '__main__':
    # p={'tradeType': 'linearPerpetual', 'symbol': 'BTCUSDT', 'positionSide': 'long', 'marginType': 'Cross', 'orderType': 'limit', 'side': 'buy', 'price': 2001, 'orderQty': 2, 'clOrdId': 'Brian092916155089381'}
    # header={'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5', 'Accept-Encoding': 'gzip, deflate, br', 'Cookie': 'token=c7ebd817-d668-46eb-a80f-d5de9cd2f866; expire_time=20211029155728', 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json', 'Connection': 'close', 'Accept-Language': 'zh-CN', 'source': 'Interface', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJBVE9NSU5UTCIsInVpZCI6OTcyMDE5NjcsImlhdCI6MTY2NDQzOTQ1NywiZXhwIjoxNjY3MDMxNDU3fQ.juHsGgsWkmymtDvvohrAXbg45cmK3W50j-Dl65OCsqW6Ydeqf1KP2QhGkI_1Ob1UBmho2ZGDKCRpHI-ji-R3tcDaa5jAYlKGH4GcvjsuPxKRy6hGLaZ-6N6I9mZmYt9RI-D89MgB-Owqwxiylz6kur26KH5KqZdooGkWTawAoSMsKl98xE9DiEC6HYSXY9vPcbOwGXoVbMT-oNFyOz9Q0H5USDIWEycRx7IM10ik593xLewzg1e8FGirz_zFryp0u0K3n0m7kVwIQ-Kg2NblsMNm2YT04-CxoXq_xFYc6GumvIaSqG47hBNoMtW68oD4qqu4ABP1XMiPESOFvh05bw'}
    # for i in range(100):
    #     S=datetime.datetime.now()
    #     # print('请求',S)
    #     # r=requests.post('https://qatradeapi.nts.aaxbtc.com/v3/trade/web/orders',json=p,headers=header)
    #     E=datetime.datetime.now()
    #     # print('耗时',str((E - S))[:-3],r.json())
    # RabbitMq_WebRquest(SymbolList=['BTCUSDT'],PriceList=[(16000,19900)],ForNumer=1)  #🀆🀆🀆🀆🀆★★★★★Send Rabbit MQ★★★★★🀆🀆🀆🀆🀆
    # for j in range (999999)
        # markPrice=[['BTCUSDT',19500],['ETHUSDT',1800]]
        # for i in markPrice:
        #     p={"vhost":"/","name":"qa_mulan_inner_price","properties":{"delivery_mode":1,"headers":{}},"routing_key":"","delivery_mode":"1","payload":"{\"symbol\":\"BTCUSDT\",\"tradeType\":\"linearPerpetual\",\"index\":20600,\"mark\":20600,\"market\":20008.27,\"time\":1663248760,\"scale\":2,\"options\":null,\"quotes\":null,\"fundingRate\":-0.0018830852,\"fundingHours\":2.46,\"fundingRateLimit\":-0.0018830852,\"nextFundingTime\":1663257600000}","headers":{},"props":{},"payload_encoding":"string"}
        #     url='https://mq.nts.aaxbtc.com/api/exchanges/%2F/qa_mulan_inner_price/publish'
        #     header['authorization']='Basic YWRtaW46Z3NONnNPRkxnOE5UbFFIMg=='
        #     # p['payload'].replace('20500',str(markPrice))
        #     # print(type(p['payload']))
        #     p['payload']=p['payload'].replace('20600',str(i[1])).replace('BTCUSDT',i[0])
        #     r=requests.post(url,json=p,headers=header)
        #     print(j+1,t(),i[0],r.text)
    #     time.sleep(60)
    c=dd(28001)*10
    print(c)
    a = 21000 + random.uniform(0.12, 0.55)
    aa = int(21000 + random.uniform(0.12, 0.92) * 10)
    print(a, aa)
    print(dd(a,2))
