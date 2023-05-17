# """
# @author: xinkuncai
# @license: (C) Copyright 2020-2099, Node Supply Chain Manager Corporation Limited.
# @contact:
# @software:
# @file: test_reverage
# @time: 2023-05-11
# @desc:
# """
# import pytest
# import requests
# import json
#
# from utils.read_files_tools.get_yaml_data_analysis import CaseData
# from utils.request_tool.request_control import RequestControl
#
# re_data=CaseData().yaml_data("D:/code/qkex_api_master/newqkex5/newqkex/data/perpetual/reverage.yaml")
# print("re_data:",re_data)
# class TestReverage:
#
#     re_data = CaseData().yaml_data("D:/code/qkex_api_master/newqkex5/newqkex/data/perpetual/reverage.yaml")
#     print(re_data)
#     @pytest.mark.parametrize('in_data',re_data,ids=[i["detail"] for i in re_data])
#     def test_reverage(self,in_data):
#         res=RequestControl(in_data).http_request()
#         print(res.json())
#
#     re_data=CaseData().yaml_data("D:/code/qkex_api_master/newqkex5/newqkex/data/perpetual/reverage_info.yaml")
#     @pytest.mark.parametrize("in_data",re_data)
#     def test_reverage(self,in_data):
#         res=RequestControl(in_data).http_request()
#         print(res.json())
#
# if __name__ == '__main__':
#     pytest.main(["-s","-v","test_reverage.py"])