from openpyxl import load_workbook
from common import slacksend
#coding:utf-8
import pygsheets
import openpyxl
from BU.futures.api import webapi as web
#user = wb.webapi(5, 'test')
excel_path = "cccda12.xlsx"
sheet_name = "计算";tradeType='linearPerpetual';gear='depth-3';limit=1000;Price='1800';symbol='ETHUSDT'

def update_data(symbol,Price):#将用户的资产，交易对配置等填充到表格
    user = web.webapi(5, 'test')
    res=user.web_instruments(tradeType=tradeType,symbol=symbol)
    takerRate=res['data'][0]['takerRate'];makerRate=res['data'][0]['makerRate']
    markPriceGreaterRatio = res['data'][0]['markPriceGreaterRatio'];maintMarginRatio = res['data'][0]['maintMarginRatio']
    res1=user.web_position(tradeType=tradeType,symbol=symbol,marginType='cross')
    avgEntryPrice=res1['data'][0]['avgEntryPrice'];leverage=res1['data'][0]['leverage']
    markPrice=res1['data'][0]['markPrice'];liquidationPrice=res1['data'][0]['liquidationPrice']
    posMargin = res1['data'][0]['posMargin'];marginRate=res1['data'][0]['marginRate']
    unrealisedPnl = res1['data'][0]['unrealisedPnl'];earningRate = res1['data'][0]['earningRate']
    res2=user.web_tradingAccount(currency='USDT')
    marginAvailable = res2['data'][0]['marginAvailable'];marginFrozen = res2['data'][0]['marginFrozen']
    marginEquity = res2['data'][0]['marginEquity']
    ak = user.web_market_depth(tradeType=tradeType, gear=gear, symbol=symbol, limit=limit)
    buy1 = ak['data']['bids'][0][0]
    sell1 =ak['data']['asks'][0][0]
    # 读取 Excel 表格数据
    wb = load_workbook(excel_path)
    ws = wb[sheet_name]
    # 更新 data1 和 data2 属性值
    ws["A2"] = symbol;ws["B6"] = symbol;ws["A11"] = symbol;ws["B8"] = symbol
    ws["B2"] = Price
    ws["C2"] = avgEntryPrice
    ws["D2"] = maintMarginRatio
    ws["E2"] = leverage
    ws["F2"] = 26040 #avgPrice
    ws["G2"] = takerRate
    ws["H2"] = 0.001  #Amount
    ws["I2"] = marginEquity#汇总资产
    ws["J2"] = marginAvailable
    ws["K2"] = marginFrozen
    ws["L2"] = markPrice
    ws["M2"] = buy1
    ws["N2"] = sell1
    ws["O2"] = markPriceGreaterRatio
    ws['p2'] = makerRate

    ws['C8'] = liquidationPrice;ws['D8'] = posMargin;ws['E8'] = marginRate;ws['F8'] = None#维持保证金
    ws['H8'] = unrealisedPnl
    ws['I8'] = unrealisedPnl
    ws['J8'] = earningRate
    # 将数据写入 Excel 表格
    wb.save(excel_path)
    ############写入完数据后需要手动保存一下文件，否则无法生效

def str_add_one(s):
    # 将字符串最后一位字符转成 ASCII 码
    ascii_code = ord(s[-1])
    # 判断如果是 '9'，则进位到 'A'
    if ascii_code == 57:
        return s[:-1] + 'A'
    # 判断如果是 'Z'，则进位到 'AA'
    elif ascii_code == 90:
        return str_add_one(s[:-1]) + 'A'
    # 其他情况直接将最后一位字符+1即可
    else:
        return s[:-1] + chr(ascii_code + 1)

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

def java_read_cell_value():#后端计算相关值
    # 读取 Excel 表格数据
    book = load_workbook(excel_path,data_only=True)
    sheet = book[sheet_name]
    result = []
    ac = ['A5','B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5', 'J5', 'K5', 'L5']
    for i in range(len(ac)):
        acc=str_add_one(ac[i])
        #读取结果的单元格值（假设结果单元格为 A1）
        result_1 = sheet[ac[i]].value
        result_2 = sheet[acc].value
        result.append('%s:%s' % (result_1, result_2))
        #print(result_1,result_2,result)
    return result

def api_read_cell_value():#打印后端计算的值
    # 读取 Excel 表格数据
    book = load_workbook(excel_path,data_only=True)
    sheet = book[sheet_name]
    result = []
    ac = ['A5','B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5', 'J5', 'K5', 'L5']
    for i in range(len(ac)):
        acc=str_add_n(ac[i],3)
        #读取结果的单元格值（假设结果单元格为 A1）
        result_1 = sheet[ac[i]].value
        result_2 = sheet[acc].value
        result.append('%s:%s' % (result_1, result_2))
        #print(result_1,result_2,result)
    return result
def web_read_cell_value():#前段计算值
    # 读取 Excel 表格数据
    book = load_workbook(excel_path,data_only=True)
    sheet = book[sheet_name]
    result = []
    ac = ['A10','B10', 'C10', 'D10', 'E10', 'F10', 'G10', 'H10', 'I10']
    for i in range(len(ac)):
        acc=str_add_one(ac[i])
        #读取结果的单元格值（假设结果单元格为 A1）
        result_1 = sheet[ac[i]].value
        result_2 = sheet[acc].value
        result.append('%s:%s' % (result_1, result_2))
        #print(result_1,result_2,result)
    return result





if __name__ == '__main__':
    #print(update_data(symbol,Price))
    # slacksend.send_Slack(java_read_cell_value())
    # slacksend.send_Slack(web_read_cell_value())
    print(java_read_cell_value())
    print(api_read_cell_value())

