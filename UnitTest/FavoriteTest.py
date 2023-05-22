from BU.NTS.WebOrder import n_order
from BU.NTS.ApiOrder import NtsApiOrder
from param.code_list import code_list as code
from common.other import httpCheck as e
import BU.NTS.dataCheck.check as check
import sys

symbolList= ["BTCUSDT","ETHUSDT"];tradeType = 'linearPerpetual';success_code = code["success"][0]

# 获取自选列表
def get_favoritelist_P0(NTS,log_level=None,tradeType=None,caseLevel=None):

    if caseLevel == 0 and NTS.source =='web':
        casetitle = NTS.source + f'<获取自选列表>-P0'
        r = NTS.GetFavirite(tradeType=tradeType,log_level=log_level,com_=1)
        check.Case_result_count(NTS,r,moduleName=NTS.source+"获取自选列表",casetitle=casetitle,log_level=log_level,_type=0)

# 新增自选
def add_favoritelist_P0(NTS,log_level=None,tradeType=None,symbolList=None,caseLevel=None):

    if caseLevel == 0 and NTS.source =='web':
        casetitle = NTS.source + f'<新增自选>-P0'
        r = NTS.AddFavirite(tradeType=tradeType, symbolList=symbolList, log_level=log_level,com_=1)
        check.Case_result_count(NTS,r,moduleName=NTS.source+"新增自选",casetitle=casetitle,log_level=log_level,_type=0)

# 取消自选
def cancel_favoritelist_P0(NTS,log_level=None,tradeType=None,symbolList=None,caseLevel=None):

    if caseLevel == 0 and NTS.source =='web':
        casetitle = NTS.source + f'<取消自选>-P0'
        r = NTS.CancelFavirite(tradeType=tradeType, symbolList=symbolList, log_level=log_level,com_=1)
        check.Case_result_count(NTS,r,moduleName=NTS.source+"取消自选",casetitle=casetitle,log_level=log_level,_type=0)

# 获取、新增、取消自选P1
def favoritelist_P1(NTS, log_level=None, tradeType=None, symbolList=None,caseLevel=None):
    if caseLevel == 1 and NTS.source =='web':
       # 先新增自选-->获得自选列表-->取消自选
        add_r = NTS.AddFavirite(tradeType=tradeType, symbolList=symbolList, log_level=log_level)
        if e(add_r)[0]:
            get_r = NTS.GetFavirite(tradeType=tradeType,log_level=log_level)['data']
            if symbolList[0] and symbolList[1] in get_r :
                cancel_r = NTS.CancelFavirite(tradeType=tradeType, symbolList=symbolList, log_level=log_level)
                if e(cancel_r)[0]: print('先新增自选->获得自选列表->取消自选,验证通过')
            else: print('先新增自选->获得自选列表->取消自选,验证失败')

def exception_TradeType(NTS,log_level=None):
    Modle = sys._getframe().f_code.co_name;modle1 = Modle[10:]
    errorCode = code['paramnull'][0];errorCode1 = code['paramwrong'][0]
    paramList=[(None,errorCode,'不传'),('',errorCode,'传空字符串'),('@#¥%&*',errorCode1,'传特殊字符@#¥%&*'),('正向永续',errorCode1,'传中文正向永续'),(123,errorCode,'非String类型tradeType'),
               ('errorTradeType',errorCode,'传不存在的TradeType'),('inversePerpetual',success_code,'传币本位永续合约'),(' linearPerpetual ',errorCode1,'传U本位永续合约+前后空格')]
    for param in paramList:
        r = NTS.GetFavirite(tradeType=param[0], log_level=log_level)
        check.Case_result_count(NTS,r,param=param,moduleName=NTS.source+'获取自选列表',casetitle=NTS.source+'获取自选列表-异常入参 '+modle1,log_level=log_level, _type=2)
        r = NTS.AddFavirite(tradeType=param[0], symbolList=symbolList,log_level=log_level)
        check.Case_result_count(NTS,r,param=param,moduleName=NTS.source+'新增自选',casetitle=NTS.source+'新增自选-异常入参 '+modle1,log_level=log_level, _type=2)
        r = NTS.CancelFavirite(tradeType=param[0],symbolList=symbolList, log_level=log_level)
        check.Case_result_count(NTS,r,param=param,moduleName=NTS.source+'取消自选',casetitle=NTS.source+'取消自选-异常入参 '+modle1,log_level=log_level, _type=2)

def expection_SymbolList(NTS,log_level=None):
    Modle = sys._getframe().f_code.co_name;modle1 = Modle[10:]
    errorCode = code['paramnull'][0];errorCode1 = code['paramwrong'][0]
    paramList=[(None,errorCode,'不传'),('',errorCode,'传空字符串'),('btcc',errorCode1,'异常字符串btcc'),(123,errorCode1,'传Int类型'),('BTCUSDT,ETHUSDT',errorCode1,'传多个symbol逗号隔开'),
               (' BTCUSDT ',errorCode1,'传正常合约+前后空格'),('BCHUSDT',errorCode1,'待上市symbol'),('LINKUSDT',errorCode1,'待开盘symbol'),
               ('DASHUSDT',errorCode1,'暂停交易symbol'),('LINKSUSDT',errorCode1,'结算中symbol'),('LTCUSDT',errorCode1,'已下市symbol'),('CCCUSDT', errorCode1, '不存在的symbol')]
    for param in paramList:
        r = NTS.AddFavirite(symbolList=param[0], tradeType=tradeType, log_level=log_level)
        check.Case_result_count(NTS, r, param=param, moduleName=NTS.source + '新增自选',casetitle=NTS.source + '新增自选-异常入参 ' + modle1, log_level=log_level, _type=2)
        r = NTS.CancelFavirite(symbolList=param[0], tradeType=tradeType, log_level=log_level)
        check.Case_result_count(NTS, r, param=param, moduleName=NTS.source + '取消自选',casetitle=NTS.source + '取消自选-异常入参 ' + modle1, log_level=log_level, _type=2)

def FaviriteCaseList(NTS,log_level=None,caseLevel=None,tradeType=tradeType):
    if NTS.source =='web':
        if caseLevel == 0: # PO用例 正常请求
            get_favoritelist_P0(NTS,log_level,caseLevel=0,tradeType=tradeType)
            add_favoritelist_P0(NTS,log_level,caseLevel=0,tradeType=tradeType,symbolList=symbolList)
            cancel_favoritelist_P0(NTS,log_level,caseLevel=0,tradeType=tradeType,symbolList=symbolList)
        if caseLevel == 1: # P1用例 其他正常场景
            favoritelist_P1(NTS, log_level, caseLevel=1,tradeType=tradeType,symbolList=symbolList)
        if caseLevel == 2: # P2用例 异常入参校验
            exception_TradeType(NTS, log_level)
            expection_SymbolList(NTS, log_level)
        if caseLevel not in(0,1,2,):
            print( "caseLevel值不存在，请重新输入")
    else:
        print(f'Open Api无 自选接口')

if __name__ == '__main__':
    NTS = n_order(5, user_id=97201979)
    NTS_API = NtsApiOrder(6, user_id='10070')
    for NTS in [NTS, NTS_API]:
        FaviriteCaseList(NTS, 2, 0)
        FaviriteCaseList(NTS, 2, 1)
        FaviriteCaseList(NTS, 2, 2)
