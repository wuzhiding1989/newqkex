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

case_id = ['trade_web_user_allSymbol_01']
TestData = GetTestCase.case_data(case_id)
re_data = regular(str(TestData))
print("re_data:",re_data)


list2=generateData(eval(re_data)[0],"pre_trade_web_user_allSymbol.yaml")
@allure.epic("交易平台接口")
@allure.feature("futures模块")
class TestTradeWebUserAllSymbol:

    @allure.story("单个撤单")
    @pytest.mark.parametrize('in_data', list2, ids=[i['detail'] for i in list2])
    def test_trade_web_user_allSymbol_01(self, in_data, case_skip):
        """
        :param :
        :return:
        """
        print("in_data:",in_data)
        res = RequestControl(in_data).http_request()


        res_data = json.loads(res.response_data)
        assert_data = in_data['assert_data']

        assert res_data['code'] == assert_data['errorCode']['value']
        assert assert_data['errorCode']['message'] in res_data['msg']


if __name__ == '__main__':
    pytest.main(['test_trade_web_order.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])