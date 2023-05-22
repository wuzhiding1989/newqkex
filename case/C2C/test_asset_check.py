# """
# @author: xinkuncai
# @license: (C) Copyright 2020-2099, Node Supply Chain Manager Corporation Limited.
# @contact:
# @software:
# @file: test_asset_check
# @time: 2023-05-04
# @desc:
# """
# import allure
# import pytest
#
# from utils.assertion.assert_control import Assert
# from utils.read_files_tools.get_yaml_data_analysis import GetTestCase
# from utils.read_files_tools.regular_control import regular
# from utils.requests_tool.request_control import RequestControl
# from utils.requests_tool.teardown_control import TearDownHandler
#
# case_id = ['ctc_asset_01']
# TestData = GetTestCase.case_data(case_id)
# re_data = regular(str(TestData))
# print("re_data:",re_data)
#
# @allure.epic("交易平台接口")
# @allure.feature("CTC模块")
# class TestAssetCheck:
#
#     @allure.story("获取资产接口")
#     @pytest.mark.parametrize('in_data', eval(re_data), ids=[i['detail'] for i in TestData])
#     def test_asset_Check(self, in_data, case_skip):
#         """
#         :param :
#         :return:
#         """
#         res = RequestControl(in_data).http_request()
#         print("res:",res)
#         TearDownHandler(res).teardown_handle()
#         Assert(assert_data=in_data['assert_data'],
#                sql_data=res.sql_data,
#                request_data=res.body,
#                response_data=res.response_data,
#                status_code=res.status_code).assert_type_handle()
#
#
# if __name__ == '__main__':
#     pytest.main(['ctc_advertise_check.py', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])