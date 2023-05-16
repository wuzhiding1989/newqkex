import json
import time,urllib
from urllib import parse
from common.util import request_http,printc,countCaseNumber as u,unquote,quote,printl
import common.util as ut
import datetime,decimal

compareResult=True
def compare(schema,r,title=None,_s=None,New=None):
    global compareResult;
    if New: compareResult=True

    if type(title)==list: title_print=title[0]+title[1]+' '+title[2]+' '
    else:  title_print=title
    S=1
    if compareResult:
        if schema:
            for i in schema.keys():
                if i in r:
                    # print(schema[i],type(schema[i]))
                    if type(schema[i]) == int:
                        if not r[i] == schema[i]:     printc(title_print, i, '=', r[i], ' 预期:', str(schema[i])+'(int)', ' 实际:',r[i],type(r[i]));compareResult = False;S=0;
                    if type(schema[i]) == decimal.Decimal:
                        if  not float(r[i])== float(schema[i]):
                            if abs(float(r[i])-float(schema[i])) >0.000000000001:
                                printc(title_print, i, '=', r[i], ' 预期:',str(schema[i]) + '(decimal)', ' 实际:', r[i],type(r[i]));compareResult = False;S = 0;
                    if type(schema[i]) == float:
                        if not r[i] == schema[i]:     printc(title_print, i, '=', r[i], ' 预期:', str(schema[i])+'(float)', ' 实际:',r[i],type(r[i]));compareResult = False;S=0
                    if type(schema[i]) == str:   #预期结果为字符串则直接对比，不符合预期则抛出
                        if not r[i] == schema[i]:     printc(title_print,i,'=',r[i],' 预期:',schema[i],' 实际:',r[i]);compareResult=False;S=0
                    if type(schema[i]) == type:  #预期结果为数据类型则用类型对比，不符合预期则抛出
                        if not type(r[i]) == schema[i]: printc(title_print,i,'=',r[i],' 预期:',schema[i],' 实际:',type(r[i]));compareResult=False;S=0
                    if not S : return S #printc(str(r).replace('\'','"'),p_type='yellow');
                    if type(schema[i]) == dict and S:
                        if not type(schema[i])==type(r[i]): printc(title_print,' 预期:',i+str(type(schema[i])),' 实际:',type(r[i]));compareResult=False;S=0
                        compare(schema[i],r[i],title=title,_s=S)
                    if type(schema[i]) == tuple:
                        special=0;
                        if r[i] in schema[i]: special=1;
                        if type(r[i]) in schema[i]: special = 1;
                        #特殊断言场景：len-校验长度
                        if schema[i].__len__()==3:
                            if schema[i][1]=='len':
                                if len(str(r[i]))==schema[i][2]:special = 1;
                                else: special=False;
                        if not special: compareResult=False;S=0;printc(title_print,i,'=',r[i],' 预期:',schema[i],' 实际:',r[i]);
                        else: compareResult=True
                        # if type(r[i]) not in schema[i]: printc(title_print,i,'=',r[i],' 预期:',schema[i],' 实际:',type(r[i]));compareResult=False
                    if type(schema[i]) == list and S:     #预期结果为数组
                        if not type(schema[i]) == type(r[i]): printc(title_print, ' 预期:', i + str(type(schema[i])), ' 实际:',type(r[i]));compareResult = False;S = 0;break;
                        for k in range(r[i].__len__()):      #实际的数据可能存在多个数组需要遍历
                            if type(schema[i]) == list:
                                for j in range(schema[i].__len__()):     #每个基础数组中对应的数据
                                    if type(schema[i][j])==list:
                                        if schema[i][j].count(type(r[i][k][j]))>0:pass         #预期类型为多个类型
                                        else: printc(title_print,k+1,schema[i][j],r[i][k][j]); compareResult=False;#exit()
                                    elif type(schema[i][j])==dict: compareResult=compare(schema[i][j],r[i][k],title=title);    #           #预期类型为字典
                                    else:
                                        # print(schema[i][j],r[i][k],j)
                                        if schema[i][j]==type(r[i][k][j]):pass               #预期类型为单个类型
                                        else: printc(title_print,k+1,schema[i][j],r[i][k][j]); compareResult=False; return False;
                                if not compareResult:break
                                    # if type(r[i][0][j]) in schema[i][j]:pass
                                    # else:print(2,schema[i],schema[i][j],r[i][0])
                            elif  type(schema[i]) == dict:  print(1111)#compare(schema[i],r[i])
                else:
                    printc(title_print,'Key不存在',i,'实际:',r,p_type='green');compareResult=False;return False;
    else : return compareResult
    return compareResult

def compareLength(r,title=None,log_level=None):
    compareLengthResult=True
    for res in r:
        if not len(str(res[0]))==res[1]:
            printc(title+res[2]+' : 预期:',res[1],' 实际: ',len(str(res[0])),res[0]);u(0,all=-1,pass_=-1);compareLengthResult=False;return False;
    if compareLengthResult and log_level:   print(title,' 成功.');u(1,all=-1,pass_=-1)
    return True
#连续性校验
def continuityAssert(r,title):
    # kline_time = datetime.datetime.fromtimestamp(t['id']);
    # current_time = datetime.datetime.now();
    period=title[2];Assert=True
    if 'min' in period: x = int(period[:-3]) * 60;
    if 'hour' in period: x = int(period[:-4]) * 60 * 60;
    if 'day' in period: x = int(period[:-3]) * 60 * 60 * 24;
    if 'week' in period: x = int(period[:-4]) * 60 * 60 * 24 * 7;
    if 'mon' in period: x = int(period[:-3]) * 60 * 60 * 24 * 30;
    # print()
    if r.__len__()!=int(float(title[3])):
        printc(title[4]+'quantityAssert Fail:'+title[1] + period + ' expect:',title[3],' fact:',r.__len__(),' start&end:',datetime.datetime.fromtimestamp(r[0]['id']),datetime.datetime.fromtimestamp(r[r.__len__()-1]['id']));Assert=False
    if r.__len__()>=2:
        for i in range(r.__len__()):
            # if 'mon' in period: print(r[id])#datetime.datetime.fromtimestamp(r['id'])
            if i <= r.__len__() - 2:
                if r[i + 1]['id'] - r[i]['id'] == x:    pass
                elif r[i + 1]['id'] - r[i]['id'] == 2678400 and 'mon' in period:    pass  # 月线既包括30天，也包括31天
                elif r[i + 1]['id'] - r[i]['id'] == 2419200 and 'mon' in period and str(datetime.datetime.fromtimestamp(r[i]['id']))[5:7] == '02': pass  # 2月份默认用28天
                else:
                   Assert=False
                   printc(title[4]+'ContinuityAssert Fail: ' + title[1] + period + ' ', i + 1, '  ',datetime.datetime.fromtimestamp(r[i]['id']),datetime.datetime.fromtimestamp(r[i + 1]['id']),(r[i + 1]['id'] - r[i]['id']) / (60 * 60 * 24))
        return Assert
#Kline画横线校验
def straightLineAssert(r,title):
    straightLineAssert=True;t=0
    for i in range(r.__len__()):  # ['open']
        j = r.__len__() - i;klinePriceAll=r[j-1]
        # print(i,j,j-1)
        klineOpenPrice = klinePriceAll['open']; klineClosePrice = klinePriceAll['close'];klineLowPrice = klinePriceAll['low'];klineHighPrice = klinePriceAll['high'];
        if klineOpenPrice == klineClosePrice == klineLowPrice == klineHighPrice and klineOpenPrice ==r[j - 2]['open'] and klineOpenPrice == r[j - 3]['open']:
            t = t + 1
            timeStamp = r[j - 1]['id'];dateArray = datetime.datetime.fromtimestamp(timeStamp);StartTime = dateArray.strftime("%Y-%m-%d %H:%M")
            if t <= 5:printc('Kline straightLineAssert Fail: No.',i+1,'根 ',title[2],title[1],StartTime,' Price is ',klineOpenPrice);straightLineAssert=False  #连续5根画横线，则打印
    return straightLineAssert
def basicAssert(r,title):
    basicAssert=True
    if '503 Service Temporarily Unavailable' in str(r) or '<head><title>' in str(r):
        printc(title[4],'basicAssert Fail: ',title[2]+title[3], r);basicAssert=False
    return basicAssert
#@: 时效性校验
def timeAssert(r,title):
    if title.__len__()>=6:
        currentTime=u.StampToTime(title[5])+'.000000'; #print(currentTime);#time.sleep(1000)
        # print(title[5] , int(time.time()))
        if int(title[5]) - int(time.time()) > 0: currentTime = datetime.datetime.now()
    else:currentTime = datetime.datetime.now();

    # print(currentTime,datetime.datetime.now(),u.StampToTime(title[5])+'.000000')
    #用最后一根K线和当前时间进行比较
    if type(r) == dict : klineTime=datetime.datetime.fromtimestamp(r['id'])
    else: klineTime=datetime.datetime.fromtimestamp(r[r.__len__()-1]['id']);
    period = title[2];timeAssert=True
    if 'min' in period and '[]' not in str(r):
        klineTimeStamp = int(str(klineTime)[11:13]) * 60 + int(str(klineTime)[14:16])  # K线时间
        currentTimeStamp= int(str(currentTime)[11:13]) * 60 + int(str(currentTime)[14:16])  # 当前时间
        if abs(klineTimeStamp - currentTimeStamp) < int(period[:-3]):b3 = 1  #
        else:
            # if log_level == 5: core.printc('log: ', kline_time, current_time, m1, m2, m1 - m2, p_type='yellow')
            timeAssert=False
            printc('Kline TimeAssert Fail: ' +title[1] + '→ws→' + period, ' klineTime:', klineTime, ' LocalTime: ', currentTime,'差值=', klineTimeStamp - currentTimeStamp)
    elif '1day' in period:
        if str(klineTime)[8:10] != str(currentTime)[8:10]:printc('Kline TimeAssert Fail: ' +title[1]  + 'ws' + period,'klineTime:', klineTime, 'LocalTime: ', currentTime)
    elif '1mon' in period:
        if str(klineTime)[5:7] != str(currentTime)[5:7]:printc('Kline TimeAssert Fail: ' +title[1]  + 'ws' + period,'klineTime:', klineTime, 'LocalTime: ', currentTime)
    elif '1week' in period: #str(klineTime)[:10].replace('-','')
        klineTimeWeeks=klineTime,datetime.datetime.strptime(str(klineTime),"%Y-%m-%d %H:%M:%S").isocalendar()[1]
        currentTimeWeeks = klineTime, datetime.datetime.strptime(str(currentTime)[:-7], "%Y-%m-%d %H:%M:%S").isocalendar()[1]
        if klineTimeWeeks!=currentTimeWeeks: printc('Kline TimeAssert Fail: ' +title[1]  + 'ws' + period,'klineTime:', klineTime, 'LocalTime: ', currentTime)
    return timeAssert
#功能：http请求 返回码标准化 断言   用途：主要用于异常参数测试结果验证   Author: Brian 2022-09-08
def responseCodeAssert1(r,param,title,title2,log_level=None):
    print(2222)
    # if not r['code'] == param[1]:
    #     printc(title2+'Fail: ', title + ':' + str(param[2]), ' 预期:' + str(param[1]), ' 实际:', r);u(0)
    # else:
    #     u(1, p=title2 + title+ ':' + str(param[2]) + ' 验证', log_level=log_level)

#公共断言方法：适用于错误码的校验. Author: Brian.Ji
def responseCodeAssert(r,param,title,title2,log_level=None,timeFlag=None):
    printTitle=title2 + title + ' ' + str(param[2])
    if 'code' in str(r) and type(r)!=list: #正常返回的结果
        if not r['code'] == param[1]:
            printc(title2+'Fail: ', title + ' ' + str(param[2]), ' 预期:' + str(param[1]), ' 实际:', r);u(0);return False;
        else:
            if timeFlag:
                if 'data' not in r :
                    printc(printTitle+'异常返回 无法校验：',r)
                    return False
                if r['data']['pageNum']==1 and r['data']['pageSize']==10 and r['data']['totalSize']>0 and r['data']['totalPage']>0:
                    u(1);printl(log_level,printTitle+' 验证成功');return True;
                else: printc(printTitle, ' 预期>0 实际:', r['data']['pageNum'],r['data']['totalSize'],r['data']['totalPage']);u(0);return False;
            else: u(1);printl(log_level,printTitle+' 验证成功');return True;

    else:#异常结果：403,401,503等
        printc(title2+'Fail: ', title + ' ' + str(param[2]), ' 预期:' + str(param[1]), ' 实际:', r);u(0);return False;

#公共断言方法：校验code=1，返回内容为空的. Author: owen.wu
def responseAssert(r,param,title,title2,log_level=None,timeFlag=None):
    printTitle=title2 + title + ':' + str(param[2])
    if 'code' in str(r) and type(r)!=list: #正常返回的结果
        if not r['code'] == param[1] and len(r['data']['list'])==0:
            printc(title2+'Fail: ', title + ':' + str(param[2]), ' 预期:' + str(param[1]), ' 实际:', r);u(0);return False;
        else:
            if timeFlag:
                if 'data' not in r : printc('异常返回 无法校验：',r)
                if r['data']['pageNum']==1 and r['data']['pageSize']==10 and r['data']['totalSize']>0 and r['data']['totalPage']>0:
                    u(1, p=printTitle+ ' 验证', log_level=log_level);return True;
                else: printc(printTitle, ' 预期:' + str(param[1]), ' 实际:', r);u(0);return False;
            else: u(1, p=printTitle + ' 验证', log_level=log_level);return True;

    else:#异常结果：403,401,503等
        printc(title2+'Fail: ', title + ':' + str(param[2]), ' 预期:' + str(param[1]), ' 实际:', r);u(0);return False;

