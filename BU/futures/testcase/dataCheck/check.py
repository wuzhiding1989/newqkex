from UnitTest.com import *
from param.dict import SuccessMessage,FailMessage
from common.asserts import compare
from common.other import httpCheck as e
from common.util import printc,printl, Count, LogOuts
from param.code_list import code_list as code
caseMark=1
success_code = code["success"][0]

#web_api检查当前委托是否存在
def isExit_Order(NTS,order_id=None,openFlag=True,param=None,_type=None,openPositionFlag=None,caseTitle='',Number=None,AllNumber=None):
    # print(param)
    if param: tradeType=param['tradeType'] ; symbol=param['symbol']
    if _type=='OpenOrder':
        r=NTS.OpenOrders(tradeType=tradeType, symbol=symbol, orderId=order_id, log_level=0)
    if _type== 'HisOrder':
        r = NTS.hisOrders(tradeType=tradeType, symbol=symbol, orderId=order_id, log_level=0)
    if _type== 'HisTrade':
        r = NTS.hisTrades(tradeType=tradeType, symbol=symbol, orderId=order_id, log_level=0)
    if not Number: Number = 1;AllNumber=1

    if openFlag:
        if e(r)[0]:
            if r['data']['list'].__len__()>0:
                compareResult=compare(param,r['data']['list'][Number-1],title='',New=1);
            else:
                printc(caseTitle+str(order_id)+' No data');return False;
    if r['data']['list'].__len__()==AllNumber and r['data']['list'][Number-1]['orderId']  == order_id  : #当前委托存在
        if openFlag : return True & compareResult  #预期为False： 则返回False
        else: return False  #预期为True： 则返回True
    else: #当前委托不存在
        if  openFlag: return False  #预期为False： 则返回True
        else: return  True  #预期为True： 则返回False

def checkHisOrder(NTS,order_id=None,param=None,_type=None,caseTitle='',Number=None,AllNumber=None):
    if param:
        tradeType = param['tradeType']; symbol = param['symbol']
    if _type== 'HisOrder':
        r = NTS.hisOrders(tradeType=tradeType, symbol=symbol, orderId=order_id, log_level=0)
    if not Number: Number = 1;AllNumber = 1
    if e(r)[0]:
        if r['data']['list'].__len__() > 0:
            compareResult = compare(param, r['data']['list'][Number - 1], title='', New=1);
            return compareResult
        else:
            printc(caseTitle + str(order_id) + ' No data');
            return False;

def checkHistrade(NTS,order_id=None,param=None,_type=None,caseTitle='',Number=None,AllNumber=None):
    if param:
        tradeType = param['tradeType']; symbol = param['symbol']
    if _type== 'HisTrade':
        r = NTS.hisTrades(tradeType=tradeType, symbol=symbol, orderId=order_id, log_level=0)
    if not Number: Number = 1;AllNumber = 1
    if e(r)[0]:
        if r['data']['list'].__len__() > 0:
            compareResult = compare(param, r['data']['list'][Number - 1], title='', New=1);
            return compareResult
        else:
            printc(caseTitle + str(order_id) + ' No data');
            return False;




#web_api检查当前委托是否存在
def isExit_openOrders(NTS,tradeType=None,symbol=None,order_id=None,openFlag=True,param=None,log_level=None,_type=None):
    if param: tradeType=param['tradeType'] ; symbol=param['symbol']
    if not _type:
        r=NTS.OpenOrders(tradeType=tradeType, symbol=symbol, orderId=order_id, log_level=log_level)
    if _type== 'HisOrder':
        r = NTS.hisOrders(tradeType=tradeType, symbol=symbol, orderId=order_id, log_level=log_level)
    if _type== 'HisTrade':
        r = NTS.hisTrades(tradeType=tradeType, symbol=symbol, orderId=order_id, log_level=log_level)
    if openFlag:
        if e(r)[0]:
            compareResult=compare(param,r['data']['list'][0],title='',New=1)
    if r['data']['list'].__len__()==1 and r['data']['list'][0]['orderId']  == order_id:
        if openFlag : return True & compareResult  #预期为False： 则返回False
        else: return False  #预期为True： 则返回True
    else: #当前委托不存在
        if  openFlag: return False  #预期为False： 则返回True
        else: return  True  #预期为True： 则返回False

#web_api检查历史委托是否存在
def isExit_web_api_historyOrders(NTS,tradeType=None,symbol=None,order_id=None,openFlag=True):
    hisOrders_r=NTS.hisOrders(tradeType=tradeType, symbol=symbol, orderId=order_id)
    if hisOrders_r['data']['list'].__len__() > 0 and hisOrders_r['data']['list'][0]['orderId'] == order_id :
        if not openFlag: return False
        else:return True#True
    else:
        if not openFlag:
            return False  # 预期为True： 则返回False
        else:
            return True  # 预期为False： 则返回True

# web_api检查资金流水是否存在
def isExit_web_api_accountIncome(NTS, tradeType=None, symbol=None,openFlag=True):
    accountIncome_r = NTS.hisAccounts(tradeType=tradeType, symbol=symbol)
    if accountIncome_r['data']['list'].__len__() > 0 and accountIncome_r['data']['list'][0]['incomeType'] == "openFee":
        if not openFlag:
            return False
        else:
            return True  # True
    else:
        if not openFlag:
            return True
        else:
            return False

#open_api检查当前委托是否存在
def isExit_api_openOrders(NTS,tradeType=None,symbol=None,order_id=None,openFlag=True):
    openOrders_r=NTS.OpenOrders(tradeType=tradeType, symbol=symbol, orderId=order_id)
    if type(openOrders_r) != list:
        if openOrders_r['data']['list'].__len__() > 0:
            if openOrders_r['data']['list'][0]['orderId'] == order_id:
                if not openFlag: return False
                else: return True#True
            else:return False

        else: #当前委托不存在
            if not openFlag:
                return False #预期为True： 则返回False
            else:
                return True   #预期为False： 则返回True

#open_api检查历史委托是否存在
def isExit_open_api_historyOrders(NTS,tradeType=None,symbol=None,order_id=None,openFlag=True):
    historyOrders_r=NTS.hisOrders(tradeType=tradeType, symbol=symbol, orderId=order_id)
    if type(historyOrders_r) != list:
        if historyOrders_r['data']['list'].__len__() > 0:
            if historyOrders_r['data']['list'][0]['orderId'] == order_id :
                if not openFlag: return False
                else:return True#True
    else:
        if not openFlag:
            return False  # 预期为True： 则返回False
        else:
            return True  # 预期为False： 则返回True

# web_api检查历史成交是否存在
def isExit_web_api_historyTrades(NTS, tradeType=None, symbol=None,order_id=None,side=None,openFlag=True):
    hisTrades_r = NTS.hisTrades(tradeType=tradeType, symbol=symbol,side=side, orderId=order_id)
    if hisTrades_r['data']['list'].__len__() > 0 and hisTrades_r['data']['list'][0]['orderId'] == order_id:
        if not openFlag:
            return False
        else:
            return True  # True
    else:
        if not openFlag:
            return True
        else:
            return False

# open_api检查历史成交是否存在
def isExit_open_api_historyTrades(NTS, tradeType=None, symbol=None,order_id=None,side=None,openFlag=True):
    hisTrades_r = NTS.hisTrades(tradeType=tradeType, symbol=symbol,side=side, orderId=order_id)
    if hisTrades_r['data']['list'].__len__() > 0 and hisTrades_r['data']['list'][0]['orderId'] == order_id:
        if not openFlag:
            return False
        else:
            return True  # True
    else:
        if not openFlag:
            return True
        else:
            return False

# 用例结果进行判断和统计用例数(通过、失败)
def Case_result_count(NTS,r,param=None,code=None,moduleName=None,casetitle=None,marginType=None,log_level=None, _type=None):
    if _type == 0 : #P0用例日志输出
        if marginType:
            FaceMarginType = GetFaceMarginType(marginType)
            if e(r)[0] and '[]' not in str(r) and FaceMarginType not in str(r):
                Count(moduleName,1,1,0,0);printl(log_level,casetitle + SuccessMessage)
            elif r['data'] == [] :
                Count(moduleName,1,0,1,0);
                errorMsg = printc(casetitle + FailMessage, f' 预期: code=1,{FaceMarginType}不存在,[]不存在', ' 实际:code=', str(r['code']),'data=',str(r['data']));LogOuts(NTS,errorMsg,LogName)
            else:
                Count(moduleName,1,0,1,0);errorMsg = printc(casetitle + FailMessage, f' 预期: code=1,{FaceMarginType}不存在,[]不存在', ' 实际:code=', str(r['code']),'list=',str(r['data']['list']));LogOuts(NTS,errorMsg,LogName)
        else:
            if e(r)[0] and ('[]' not in str(r) or type(r['data'] == dict)) : # type(r['data'] == dict)兼容批量撤单接口返回结构
                Count(moduleName,1,1,0,0);printl(log_level,casetitle + SuccessMessage)
            elif r['data'] == []:
                Count(moduleName,1,0,1,0);errorMsg = printc(casetitle + FailMessage, ' 预期: code=1,[]不存在', ' 实际:code=', str(r['code']),'data=',str(r['data']));LogOuts(NTS,errorMsg,LogName)
            else:
                Count(moduleName,1,0,1,0);errorMsg = printc(casetitle + FailMessage, ' 预期: code=1,[]不存在', ' 实际:code=', str(r['code']),'list=',str(r['data']));LogOuts(NTS,errorMsg,LogName)

    if _type == 1 : #P1用例日志输出
        if type(r) == dict and r['code'] == code:
            Count(moduleName,1,1,0,0);printl(log_level,casetitle + SuccessMessage)
        else:
            if type(r) == list : r=r[1]
            Count(moduleName,1,0,1,0);errorMsg = printc(casetitle + FailMessage, ' 预期:' + str(code), ' 实际:', str(r['code'])+' '+r['message'] or r);LogOuts(NTS,errorMsg,LogName)

    if _type == 2 : #P2用例日志输出
        if type(r) == dict and r['code'] == str(param[1]):
            Count(moduleName,1,1,0,0);printl(log_level,casetitle + ' '+ param[2]+ SuccessMessage)
        else:
            if type(r) == list: r = r[1]
            Count(moduleName,1,0,1,0);errorMsg = printc(casetitle + ' '+ param[2]+ FailMessage,' 预期: '+ str(param[1]), ' 实际:',r or str(r['code'])+' '+r['message'] or r);LogOuts(NTS,errorMsg,LogName)

