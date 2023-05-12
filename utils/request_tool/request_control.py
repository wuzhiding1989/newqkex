"""
@author: xinkuncai
@license: (C) Copyright 2020-2099, Node Supply Chain Manager Corporation Limited.
@contact:  
@software: 
@file: request_control
@time: 2023-05-11 
@desc: 
"""
import requests

from utils.other_tools.models import TestCase, ResponseData
from utils.read_files_tools.get_yaml_data_analysis import CaseData


class RequestControl:
    """ 封装请求 """
    def __init__(self, yaml_case):
        #获取请求参数
        self.__yaml_case = TestCase(**yaml_case)
        # print("self.__yaml_case:",self.__yaml_case)
    def http_request(self):
        res = requests.request(
            method=self.__yaml_case.method,
            url=self.__yaml_case.url,
            json=self.__yaml_case.data,
            data={},
            headers=self.__yaml_case.headers,
            verify=False,
            params=None
        )
        # print(res.json())
        _res_data=self._check_params(res,self.__yaml_case)
        print("_res_data",_res_data)
        return _res_data


    def _check_params(
            self,
            res,
            yaml_data: "TestCase",
    ) -> "ResponseData":
        _data = {
            "url": res.url,
            "response_data": res.text,
            # 这个用于日志专用，判断如果是get请求，直接打印url
            "request_body": self.__yaml_case.data,
            "method": res.request.method,
            "yaml_data": yaml_data,
            "headers": res.request.headers,
            "cookie": res.cookies,
            "status_code": res.status_code,
            # "data": self.__yaml_case.data
            "assert_data": self.__yaml_case.assert_data
        }
        # 抽离出通用模块，判断 http_request 方法中的一些数据校验
        return ResponseData(**_data)
if __name__ == '__main__':
    RequestControl(CaseData().yaml_data("D:/code/new_qkex_api/data/perpetual/reverage.yaml")[0]).http_request()