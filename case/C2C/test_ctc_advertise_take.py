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

from utils.assertion.assert_control import Assert
from utils.read_files_tools.get_yaml_data_analysis import GetTestCase
from utils.read_files_tools.regular_control import regular
from utils.requests_tool.request_control import RequestControl
from utils.requests_tool.teardown_control import TearDownHandler

case_id = ['ctc_consumer_take_01']
TestData = GetTestCase.case_data(case_id)
re_data = regular(str(TestData))
# print("re_data:",re_data)

@allure.epic("交易平台接口")
@allure.feature("CTC模块")
class TestCTCConsumerTake:

    @allure.story("用户C2C广告下单接口")
    @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
    def test_ctc_consumer_take_01(self,in_data):
        """
        :param :
        :return:
        """

        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(assert_data=in_data['assert_data'],
               sql_data=res.sql_data,
               request_data=res.body,
               response_data=res.response_data,
               status_code=res.status_code).assert_type_handle()

    case_id = ['ctc_consumer_take_02','ctc_consumer_take_03']
    TestData = GetTestCase.case_data(case_id)
    re_data = regular(str(TestData))
    @allure.story("用户C2C广告下单接口")
    @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
    def test_ctc_consumer_take_02(self,in_data):
        """
        :param :
        :return:
        """

        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(assert_data=in_data['assert_data'],
               sql_data=res.sql_data,
               request_data=res.body,
               response_data=res.response_data,
               status_code=res.status_code).assert_type_handle()

    case_id = ['ctc_consumer_take_04','ctc_consumer_take_05']
    TestData = GetTestCase.case_data(case_id)
    re_data = regular(str(TestData))
    @allure.story("用户C2C广告下单接口")
    @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
    def test_ctc_consumer_take_03(self,in_data):
        """
        :param :
        :return:
        """

        res = RequestControl(in_data).http_request()
        TearDownHandler(res).teardown_handle()
        Assert(assert_data=in_data['assert_data'],
               sql_data=res.sql_data,
               request_data=res.body,
               response_data=res.response_data,
               status_code=res.status_code).assert_type_handle()

if __name__ == '__main__':
    pytest.main(['test_ctc_advertise_take.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])