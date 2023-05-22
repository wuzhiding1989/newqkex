from BU.futures.api import webapi as wb
# import HTMLTestRunner
import unittest,time,pytest

symbol = 'BTCUSDT';tradeType = 'linearPerpetual';side = 'buy';marginType = 'cross';positionSide = 'long'
postOnly = None;reduceOnly = None;orderType = 'limit';priceType=None;pageNum = '1';pageSize = '10';timeInForce='GTC'
fromAccountType='funding';toAccountType='futures';currency='USDT';amount=20

from BU.futures.api import webapi as wb
class TestWebTransfer():
    web = wb.webapi(2, 'test')

    @pytest.mark.parametrize("params, expected_code, expected_msg", [
        ({'toAccountType': toAccountType, 'currency': currency, 'fromAccountType': fromAccountType, 'amount': amount}, '0', ''),
        ({'fromAccountType': fromAccountType, 'toAccountType': toAccountType, 'amount': amount, 'currency':None }, '1047', 'currency字段不能为空,请重新输入'),
        ({'fromAccountType': fromAccountType, 'currency': currency, 'amount': amount,'toAccountType':None}, '1047', 'toAccountType字段不能为空,请重新输入'),
        ({'toAccountType': toAccountType, 'currency': currency, 'amount': amount,'fromAccountType':None}, '1047', 'fromAccountType字段不能为空,请重新输入'),
        ({'toAccountType': toAccountType, 'currency': currency, 'fromAccountType': fromAccountType,'amount':None}, '1047', 'amount字段不能为空,请重新输入')
    ])#批量校验code和msg
    def test_web_transfer(self, params, expected_code, expected_msg):
        res = self.web.web_transfer(**params)
        assert res['code'] == expected_code
        assert res['msg'] == expected_msg

class TestwebtradingAccount():
    web = wb.webapi(2, 'test')

    @pytest.mark.parametrize("params, expected_code, expected_msg", [
        ({'currency': currency}, '0', ''),
        ({'currency':None }, '0', ''),
    ])#批量校验code和msg
    def test_web_tradingaccount(self,params,expected_code,expected_msg):
        res = self.web.web_tradingAccount(**params)
        assert res['code'] ==expected_code
        assert res['msg'] == expected_msg

def format_data(data):
    """
    将数据格式化为指定格式
    """
    return f"Name: {data['name']}, Age: {data['age']}"

def test_format_data():
    """
    测试format_data函数的返回结果是否为指定格式
    """
    web = wb.webapi(2, 'test')
    c=10*3+20-20-1
    name='John';age=c
    data = {'name': name, 'age': age}
    result = format_data(data)
    assert result == "Name: John, Age: 30"

