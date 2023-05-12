"""
@author: xinkuncai
@license: (C) Copyright 2020-2099, Node Supply Chain Manager Corporation Limited.
@contact:  
@software: 
@file: get_yaml_data_analysis
@time: 2023-05-11 
@desc: 
"""
from utils.read_files_tools.get_data import GetYamlData


class CaseData:

    def yaml_data(self,filenamePath):
        data=GetYamlData().readYamlData(filenamePath)
        case_list = []
        for k,v in data.items():
            if k !="common":
                self.case_data=v
                self.case_id=k
                case_date = {
                    'method': self.case_data.get("method"),
                    # 'is_run': self.case_data.get(TestCaseEnum.IS_RUN.value[0]),
                    'url': self.case_data.get("host")+self.case_data.get("url"),
                    # 'detail': self.case_data.get(TestCaseEnum.DETAIL.value[0]),
                    'headers': self.case_data.get("headers"),
                    # 'requestType': super().get_request_type,
                    'data': self.case_data.get("data"),
                    # 'dependence_case': self.case_data.get(TestCaseEnum.DE_CASE.value[0]),
                    # 'dependence_case_data': self.get_dependence_case_data,
                    # "current_request_set_cache": self.case_data.get(TestCaseEnum.CURRENT_RE_SET_CACHE.value[0]),
                    # "sql": self.get_sql,
                    "assert_data": self.case_data.get("assert"),
                    # "setup_sql": self.case_data.get(TestCaseEnum.SETUP_SQL.value[0]),
                    # "teardown": self.case_data.get(TestCaseEnum.TEARDOWN.value[0]),
                    # "teardown_sql": self.case_data.get(TestCaseEnum.TEARDOWN_SQL.value[0]),
                    # "sleep": self.case_data.get(TestCaseEnum.SLEEP.value[0]),
                }
                case_list.append(case_date)
        return case_list
if __name__ == '__main__':
     CaseData().yaml_data("D:/code/new_qkex_api/data/perpetual/reverage.yaml")


