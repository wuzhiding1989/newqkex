"""
@author: xinkuncai
@license: (C) Copyright 2020-2099, Node Supply Chain Manager Corporation Limited.
@contact:  
@software: 
@file: test_reverage
@time: 2023-05-11 
@desc: 
"""
import pytest
import requests
import json

from utils.read_files_tools.get_yaml_data_analysis import CaseData
from utils.request_tool.request_control import RequestControl

re_data=CaseData().yaml_data("D:/code/qkex_api_master/newqkex/data/perpetual/reverage.yaml")
class TestReverage:

    @pytest.mark.parametrize('in_data',re_data)
    def test_reverage(self,in_data):
        res=RequestControl(in_data).http_request()
        print(res.json())


