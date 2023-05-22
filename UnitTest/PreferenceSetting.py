from BU.NTS.WebOrder import n_order
from BU.NTS.ApiOrder import NtsApiOrder
from param.code_list import code_list as code
from common.other import httpCheck as e
import BU.NTS.dataCheck.check as check
import sys
from UnitTest.com import CreateOrders

preview=1;tradeUnit=1;tradeType='linearPerpetual';type='currentOrder';success_code=code["success"][0]

# 获取偏好设置
def get_PreferSetting_P0(NTS,log_level=None,caseLevel=None):

    if caseLevel == 0 and NTS.source =='web':
        casetitle = NTS.source + f'<双向全仓>获取偏好设置-P0'
        r = NTS.QueryFavoriteSetting(tradeType=tradeType,log_level=log_level,com_=1)
        check.Case_result_count(NTS,r,moduleName=NTS.source+"获取偏好设置",casetitle=casetitle,log_level=log_level,_type=0)

# 更新偏好设置
def update_PreferSetting_P0(NTS,log_level=None,caseLevel=None):

    if caseLevel == 0 and NTS.source =='web':
        casetitle = NTS.source + f'<双向全仓>更新偏好设置-P0'
        r = NTS.UpdateFavoriteSetting(tradeType=tradeType,preview=preview,tradeUnit=tradeUnit,log_level=log_level,com_=1)
        check.Case_result_count(NTS,r,moduleName=NTS.source+"更新偏好设置",casetitle=casetitle,log_level=log_level,_type=0)

# 查询用户全部币种
def get_allsymbol_P0(NTS,log_level=None,caseLevel=None):

    # 查询委托类型. currentOrder 当前委托, conditionOrder 条件委托
    if caseLevel == 0 and NTS.source =='web':
        typelist = ['currentOrder','conditionOrder']
        for type in typelist:
            r = NTS.userallSymbol(type=type,log_level=log_level,com_=1)
            if type == 'currentOrder': type ='当前委托'
            if type == 'conditionOrder': type ='条件委托'
            casetitle = NTS.source + f'<双向全仓>{type}-查询用户全部币种>-P0'
            check.Case_result_count(NTS,r,moduleName=NTS.source+"查询用户全部币种",casetitle=casetitle,log_level=log_level,_type=0)

# 下单二次确认
def orderPreview_P0(NTS,log_level=None,caseLevel=None):

    if caseLevel == 0 and NTS.source =='web':
        orderparm = CreateOrders(NTS, Side='buy', marginType="cross", symbol="BTC", price='15000', TradeFlag=False,MarketFlag=False, OpenFlag=True)
        casetitle = NTS.source + f'<双向全仓>下单二次确认-P0'
        r = NTS.orderPreview(caseParam=orderparm,log_level=log_level,com_=1)
        check.Case_result_count(NTS,r,moduleName=NTS.source+"下单二次确认",casetitle=casetitle,log_level=log_level,_type=0)

# 更新偏好设置、查询偏好设置
def PreferSetting_P1(NTS, log_level=None, tradeType=tradeType, preview=preview,tradeUnit=tradeUnit,caseLevel=None):
    if caseLevel == 1 and NTS.source =='web':
       # 更新偏好设置-->查询偏好设置
        update_r = NTS.UpdateFavoriteSetting(tradeType=tradeType,preview=preview,tradeUnit=tradeUnit,log_level=log_level)
        if e(update_r)[0]:
            get_r = NTS.QueryFavoriteSetting(tradeType=tradeType,log_level=log_level)
            if get_r['data']['preview'] == preview and get_r['data']['tradeUnit'] == tradeUnit:
                print('更新偏好设置-->查询偏好设置,验证通过')

def exception_TradeType(NTS,log_level=None):
    Modle = sys._getframe().f_code.co_name;modle1 = Modle[10:]
    errorCode = code['paramnull'][0];errorCode1 = code['paramwrong'][0]
    paramList=[(None,errorCode,'不传'),('',errorCode,'传空字符串'),('@#¥%&*',errorCode1,'传特殊字符@#¥%&*'),('正向永续',errorCode1,'传中文正向永续'),(123,errorCode1,'非String类型tradeType'),
               ('errorTradeType',errorCode1,'传不存在的TradeType'),('inversePerpetual',success_code,'传币本位永续合约'),(' linearPerpetual ',errorCode1,'传U本位永续合约+前后空格')]
    for param in paramList:
        r = NTS.QueryFavoriteSetting(tradeType=param[0], log_level=log_level)
        check.Case_result_count(NTS,r,param=param,moduleName=NTS.source+'获取偏好设置',casetitle=NTS.source+'获取偏好设置-异常入参 '+modle1,log_level=log_level, _type=2)
        r = NTS.UpdateFavoriteSetting(tradeType=param[0], preview=preview,tradeUnit=tradeUnit,log_level=log_level)
        check.Case_result_count(NTS,r,param=param,moduleName=NTS.source+'更新偏好设置',casetitle=NTS.source+'更新偏好设置-异常入参 '+modle1,log_level=log_level, _type=2)

def PreferSettingCaseList(NTS,log_level=None,caseLevel=None):
    if NTS.source =='web':
        if caseLevel == 0: # PO用例 正常请求
            get_PreferSetting_P0(NTS,log_level,caseLevel=0)
            update_PreferSetting_P0(NTS,log_level,caseLevel=0)
            orderPreview_P0(NTS,log_level,caseLevel=0)
            get_allsymbol_P0(NTS,log_level,caseLevel=0)
        if caseLevel == 1: # P1用例 其他正常场景
            PreferSetting_P1(NTS, log_level, caseLevel=1)
        if caseLevel == 2: # P2用例 异常入参校验
            exception_TradeType(NTS, log_level)
        if caseLevel not in(0,1,2,):
            print( "caseLevel值不存在，请重新输入")
    else:
        return print(f'Open Api无 偏好设置、全部币种、二次确认 接口')
if __name__ == '__main__':
    NTS = n_order(5, user_id=97201979)
    NTS_API = NtsApiOrder(5, user_id='97201979')
    for NTS in [NTS, NTS_API]:
        PreferSettingCaseList(NTS, 2, 0)
