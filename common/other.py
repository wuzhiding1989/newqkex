import copy,BU.NTS.comm.params as par
from common.util import d

from param.dict import cumQty, lastPrice, commission,orderStatus, side,positionSide,price,leverage

def http_check(response):
  if 'code' in response:
    if response['code']!=1 : return [False,response['code'],response['message']]
    else:return[True]
  else:
    r=response.split(',')
    return [False,r[0],r[1]]

def bbo(r,flag=None):
  if r['bids']==r['asks']==[]: return False
  if r['asks']==[]:r['asks']=[[0,0],[0,0]]
  if r['bids'].__len__()<2: r['bids'].append([float(r['bids'][0][0])*0.8,0])
  if flag==2: return r['asks'][1]+r['bids'][1]
  else: return r['asks'][0]+r['bids'][0]+r['asks'][1]+r['bids'][1]

#断言http请求响应码 主要用于正常场景
def httpCheck(response):
  if not response: return [False]
  if type(response)==list:
    if not response[0]: return response
    else: response=response[0];#部分api接口直接返回列表


  if 'code' in str(response):
    if type(response)==list: return [False,response[0],response[1]]
    elif response['code'] in ['1',0,'1000'] : return[True]  #正确的code为1000
    else:return [False,response['code'],response['message']]  #
  else:
    # print(response)
    #针对404,503等异常处理
    if type(response)==list:
      return [False, response[0], response[1]]
    elif response==401: return [False,401]
    else:
      r=response.split(',')
      return [False,r[0]]

#断言结果 组装
def OrderRelateInstall(_type=None,caseParam=None,ParamList=None,OrderPrice=None,orderQty=None,Rate=None,ctVal=None,Leverage=None,avgPrice=None,Side=None,Position=None,openPositionFlag=None,CumQty=None,OrderStatus=None,Commission=None,avgPrice_Real=None,RealProfit=None,Profit=None):
  if _type=='HisTrade':
    caseParam_Trade = copy.deepcopy(par.linear_cross_param);
    caseParam_Trade.update(par.HisTradeAssert)
    caseParamAssert = copy.deepcopy(caseParam);
    for p1 in ParamList: caseParam_Trade[p1[0]] = p1[1]
    caseParam_Trade['filledPrice'] = d(OrderPrice);
    caseParam_Trade.pop('timeInForce');
    caseParam_Trade.pop('priceType');
    caseParam_Trade.pop('postOnly');
    return caseParam_Trade
  if _type=='HisOrder':
    if not CumQty: CumQty = orderQty
    if not Commission:  Commission = d(OrderPrice) * d(CumQty) * d(Rate) * d(ctVal)
    import BU.NTS.Calculator as cal
    if not RealProfit:
      realProfit_1 = cal.UnRealisePnl(Position, str(OrderPrice), avgPrice, CumQty, ctVal)
      realProfit = d(realProfit_1) - d(Commission)
    else: realProfit=RealProfit;realProfit_1=Profit
    if openPositionFlag: realProfit_1 = d(0);realProfit=d(0)
    if not OrderStatus: OrderStatus='filled'
    if not avgPrice_Real: avgPrice1=OrderPrice
    else: avgPrice1=avgPrice_Real
    paramListAssert = [[cumQty, d(CumQty)], ['avgPrice', d(avgPrice1)], [lastPrice, d(OrderPrice)],[commission, Commission], [orderStatus, OrderStatus], [leverage, d(Leverage)],['realProfit', realProfit], ['commissionAsset', 'USDT']]
    caseParam[side] = Side;
    caseParam[positionSide] = Position;
    caseParam[price] = d(OrderPrice);
    caseParam['orderQty'] = d(orderQty)
    caseParamAssert = copy.deepcopy(caseParam);
    for p1 in paramListAssert: caseParamAssert[p1[0]] = p1[1]
    return [caseParamAssert,realProfit_1,Commission,realProfit]
