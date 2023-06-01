from openpyxl import load_workbook
from BU.futures.api import webapi as wb
user = wb.webapi(2, 'test')
excel_path = "cccda12.xlsx"
sheet_name = "计算";tradeType='linearPerpetual';gear='depth-3';limit=1000;Price='25000';symbol='BTCUSDT'

def update_data(symbol,Price):
    res=user.web_instruments(tradeType=tradeType,symbol=symbol)
    takerRate=res['data'][0]['takerRate'];makerRate=res['data'][0]['makerRate']
    markPriceGreaterRatio = res['data'][0]['markPriceGreaterRatio'];maintMarginRatio = res['data'][0]['maintMarginRatio']
    res1=user.web_position(tradeType=tradeType,symbol=symbol,marginType='cross')
    avgEntryPrice=res1['data'][0]['avgEntryPrice'];leverage=res1['data'][0]['leverage']
    markPrice=res1['data'][0]['markPrice']
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
    ws["A2"] = symbol
    ws["B2"] = Price
    ws["C2"] = avgEntryPrice
    ws["D2"] = maintMarginRatio
    ws["E2"] = leverage
    ws["F2"] = 26000 #avgPrice
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
    # 将数据写入 Excel 表格
    wb.save(filename=excel_path)

def java_read_cell_value(ac):
    # 读取 Excel 表格数据
    book = load_workbook(excel_path,data_only=True)
    sheet = book[sheet_name]
    # 读取结果的单元格值（假设结果单元格为 A1）
    result_cell = sheet[ac].value
    return result_cell
def web_read_cell_value(ac):
    # 读取 Excel 表格数据
    book = load_workbook(excel_path,data_only=True)
    sheet = book[sheet_name]
    # 读取结果的单元格值（假设结果单元格为 A1）
    result_cell = sheet[ac].value
    return result_cell

if __name__ == '__main__':
    #print(update_data(symbol,Price))
    print(java_read_cell_value('C6'))
