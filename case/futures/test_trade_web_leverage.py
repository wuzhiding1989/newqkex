"""
@author: xinkuncai
@license: (C) Copyright 2020-2099, Node Supply Chain Manager Corporation Limited.
@contact:
@software:
@file: test_asset_check
@time: 2023-05-04
@desc:
"""
import json

import allure
import pytest

from common.yamlData import generateData
from utils.assertion.assert_control import Assert
from utils.read_files_tools.get_yaml_data_analysis import GetTestCase
from utils.read_files_tools.regular_control import regular
from utils.requests_tool.request_control import RequestControl
from utils.requests_tool.teardown_control import TearDownHandler

te={'tradeType': 'linearPerpetual', 'symbol': 'BTCUSDT', 'leverage': '10', 'marginType': 'cross'}
de= {"code":"0","msg":"","data":{"tradeType":"linearPerpetual","symbol":"BTCUSDT","leverage":"10","marginType":"cross","amount":""},"ts":1684635037940,"traceId":"c34273c6220d4e20a2dda4f07565b748"}
lists=[{"key":"tradeType","value":'1',"code":"1046","msg":"字段不合法,请重新输入"},{"key":"tradeType","value":'',"code":"1046","msg":"字段不合法,请重新输入"}]


case_id = ['trade_web_leverage_01']
TestData = GetTestCase.case_data(case_id)
re_data = regular(str(TestData))
print("re_data:",re_data)
data=eval(re_data)[0]

#处理多个异常数据
list2=generateData(eval(re_data)[0],"pre_trade_web_leverage.yaml")

print(list2)
@allure.epic("交易平台接口")
@allure.feature("futures模块")
class TestTradeWebLeverage:

    @allure.story("杠杆切换")
    # @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
    @pytest.mark.parametrize('in_data', list2, ids=[i['detail'] for i in list2])
    def test_trade_web_leverage_01(self, in_data, case_skip):
        """
        :param :
        :return:
        """
        print("in_data:",in_data)
        res = RequestControl(in_data).http_request()

        res_data=json.loads(res.response_data)
        assert_data=in_data['assert_data']

        assert res_data['code']==assert_data['errorCode']['value']
        assert assert_data['errorCode']['message'] in res_data['msg']

if __name__ == '__main__':
    pytest.main(['test_trade_web_order.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])