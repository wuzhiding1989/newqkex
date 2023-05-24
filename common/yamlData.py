"""
@author: xinkuncai
@license: (C) Copyright 2020-2099, Node Supply Chain Manager Corporation Limited.
@contact:  
@software: 
@file: yamlData
@time: 2023-05-21 
@desc: 
"""
import copy
import os

import yaml

from common.setting import ensure_path_sep

def generateData(re_data,filename):
    if filename is not None:
        path=os.path.join(ensure_path_sep('\\project_data\\prepare_data'),filename)
        f=open(path,"r",encoding="utf-8")
        data_lists=yaml.safe_load(f)
        # print("data_list:",data_lists)
        list2=[re_data]

        n = 0
        detail=""
        for i in data_lists:
            datas = copy.deepcopy(re_data)
            #兼容多个参数不一致时
            for j in i["data"]:
                datas["data"][j['key']] = j['value']
                detail=detail+str(j['key'])+"-"+str(j["value"])+"-"
            datas["assert_data"]['errorCode']['value'] = i['code']
            datas["assert_data"]['errorCode']['message'] = i["msg"]
            datas['detail'] = datas['detail'] + detail
            # print(datas)
            list2.append(datas)
            detail=""
        # print("list:",list2)
        return list2
    else:
        raise FileExistsError("文件不存在")


if __name__ == '__main__':

    data={'url': 'https://test-futures-rest.qkex.com/v1/trade/web/leverage', 'method': 'POST', 'detail': 'futures切换杠杆', 'assert_data': {'errorCode': {'jsonpath': '$.code', 'type': '==', 'value': '0', 'AssertType': None, 'message': ''}}, 'headers': {'source': 'api', 'Accept-Language': 'zh-CN', 'X-Authorization': '$cache{login_futures_user}'}, 'requestType': 'JSON', 'is_run': None, 'data': {'tradeType': 'linearPerpetual', 'symbol': 'BTCUSDT', 'leverage': '10', 'marginType': 'cross'}, 'dependence_case': False, 'dependence_case_data': None, 'sql': None, 'setup_sql': None, 'status_code': None, 'teardown_sql': None, 'teardown': [{'case_id': 'reverage_01', 'param_prepare': None, 'send_request': [{'dependent_type': 'response', 'jsonpath': '$.data', 'cache_data': None, 'set_cache': None, 'replace_key': 'Sql_d'}]}], 'current_request_set_cache': [{'type': 'response', 'jsonpath': '$.data.id', 'name': 'test_sql'}], 'sleep': None}
    generateData(data,filename="pre_trade_web_account_transfer01.yaml")
    # pass
    # print(os.path.join(ensure_path_sep('\prepare_data'), "pre_trade_web_leverage.yaml"))
    #
    # data_lists = yaml.safe_load(open(os.path.join(ensure_path_sep('\prepare_data'), "pre_trade_web_leverage.yaml"),'r',encoding="UTF-8"))
    # print(data_lists)
    # path = os.path.join(ensure_path_sep('\prepare_data'), "pre_trade_web_account_transfer01.yaml")
    # f = open(path, "r", encoding="utf-8")
    # data_lists = yaml.safe_load(f)
    # print(data_lists)
