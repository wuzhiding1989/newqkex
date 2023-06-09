import os,pygsheets
from BU.futures.api import webapi as web
tradeType='linearPerpetual';gear='depth-3';limit=1000;Price=1800;symbol='ETHUSDT'

# 填写您的凭据文件名以及需要更新的工作表 ID 和范围
CREDENTIALS_FILE = 'lively-oxide-388602-33b9719fd3c6.json'
SPREADSHEET_ID = 'testqk'
RANGE_NAME = 'teql!A1:I1000'

def main():
    user = web.webapi(3, 'test')
    res=user.web_instruments(tradeType=tradeType,symbol=symbol)
    takerRate=res['data'][0]['takerRate'];makerRate=res['data'][0]['makerRate']
    markPriceGreaterRatio = res['data'][0]['markPriceGreaterRatio'];maintMarginRatio = res['data'][0]['maintMarginRatio']
    res1=user.web_position(tradeType=tradeType,symbol=symbol,marginType='cross')
    avgEntryPrice=res1['data'][0]['avgEntryPrice'];leverage=res1['data'][0]['leverage']
    markPrice=res1['data'][0]['markPrice'];liquidationPrice=res1['data'][0]['liquidationPrice']
    posMargin = res1['data'][0]['posMargin'];marginRate=res1['data'][0]['marginRate']
    unrealisedPnl = res1['data'][0]['unrealisedPnl'];positionAmt = res1['data'][0]['positionAmt']
    side = res1['data'][0]['side'];earningRate = res1['data'][0]['earningRate']
    res2=user.web_tradingAccount(currency='USDT')
    marginAvailable = res2['data'][0]['marginAvailable'];marginFrozen = res2['data'][0]['marginFrozen']
    marginEquity = res2['data'][0]['marginEquity'];marginPosition=res2['data'][0]['marginPosition']
    ak = user.web_market_depth(tradeType=tradeType, gear=gear, symbol=symbol, limit=limit)
    buy1 = ak['data']['bids'][0][0];buy1=f'{buy1}'
    sell1 =ak['data']['asks'][0][0];sell1=f'{sell1}'
    gc = pygsheets.authorize(service_file="lively-oxide-388602-33b9719fd3c6.json")
    sh = gc.open('testqk')
    # 获取 Sheet
    wks = sh.worksheet_by_title('teql')
    values = [
        ['A2', symbol],
        ['B2', Price],
        ['C2', avgEntryPrice],
        ['D2', side],
        ['E2', leverage],
        ['F2', 26040],
        ['G2', takerRate],
        ['H2', positionAmt],
        ['B6', symbol],
        ['A11', symbol],
        ['B8', symbol],
        ['E21', maintMarginRatio],
        ['B21', marginEquity],
        ['C21', marginAvailable],
        ['F21', marginPosition],
        ['D21', marginFrozen],
        ['L2', markPrice],
        ['M2', buy1],
        ['N2', sell1],
        ['O2', markPriceGreaterRatio],
        ['P2', makerRate],
        ['C8', liquidationPrice],
        ['D8', posMargin],
        ['E8', marginRate],
        ['F8', None],
        ['H8', unrealisedPnl],
        ['I8', earningRate]
    ]
    for tmp in values:
        tmp1=tmp[1]
        tmp0 = tmp[0]
        #print(tmp1,tmp0)
        wks.update_values(tmp0, [[tmp1]])

def str_add_n(s, n):
    # 将字符串最后一位字符转成 ASCII 码
    ascii_code = ord(s[-1])
    # 判断如果是 '9'，则进位到 'A'
    if ascii_code == 57:
        return str_add_n(s[:-1], n) + 'A'
    # 判断如果是 'Z'，则进位到 'AA'
    elif ascii_code == 90:
        return str_add_n(s[:-1], n+1) + 'A'
    # 其他情况直接将最后一位字符+n即可
    else:
        new_char = chr(ascii_code + n)
        # 如果新字符是 '4'，将其替换为 '6'
        if new_char == '4':
            new_char = '6'
        return s[:-1] + new_char

def get_cell_value(worksheet, cell):
    return worksheet.get_value(cell)
def java_read_cell_value():#后端计算相关值
    # 读取 Excel 表格数据
    gc = pygsheets.authorize(service_file="lively-oxide-388602-33b9719fd3c6.json")
    sh = gc.open('testqk')
    # 获取 Sheet
    wks = sh.worksheet_by_title('teql')
    result = []
    ac = ['A5','B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5', 'J5', 'K5', 'L5']
    for i in range(len(ac)):
        acc=str_add_n(ac[i],1)
        #读取结果的单元格值（假设结果单元格为 A1）
        result_1 = get_cell_value(wks, ac[i])
        result_2 = get_cell_value(wks, acc)
        result.append('%s:%s' % (result_1, result_2))
        #print(result_1,result_2,result)
    return result

def api_read_cell_value():#打印后端计算的值
    # 读取 Excel 表格数据
    gc = pygsheets.authorize(service_file="lively-oxide-388602-33b9719fd3c6.json")
    sh = gc.open('testqk')
    # 获取 Sheet
    wks = sh.worksheet_by_title('teql')
    result = []
    ac = ['A5','B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5', 'J5', 'K5', 'L5']
    for i in range(len(ac)):
        acc=str_add_n(ac[i],3)
        result_1 = get_cell_value(wks, ac[i])
        result_2 = get_cell_value(wks, acc)
        result.append('%s:%s' % (result_1, result_2))
        #print(result_1,result_2,result)
    return result

def web_read_cell_value():#前段计算值
    # 读取 Excel 表格数据
    gc = pygsheets.authorize(service_file="lively-oxide-388602-33b9719fd3c6.json")
    sh = gc.open('testqk')
    # 获取 Sheet
    wks = sh.worksheet_by_title('teql')
    result = []
    ac = ['A10','B10', 'C10', 'D10', 'E10', 'F10', 'G10', 'H10', 'I10']
    for i in range(len(ac)):
        acc=str_add_n(ac[i],1)
        result_1 = get_cell_value(wks, ac[i])
        result_2 = get_cell_value(wks, acc)
        result.append('%s:%s' % (result_1, result_2))
        #print(result_1,result_2,result)
    return result

if __name__ == '__main__':
    #print(main())
    print(web_read_cell_value())