"""
@author: xinkuncai
@license: (C) Copyright 2020-2099, Node Supply Chain Manager Corporation Limited.
@contact:  
@software: 
@file: get_data
@time: 2023-05-11 
@desc: 
"""
import os
import yaml


class GetYamlData:

    def readYamlData(self,filename):
        if os.path.exists(filename):
            with open(file=filename,mode='r',encoding="UTF-8") as file:
                data=file.read()
                result=yaml.load(data,Loader=yaml.FullLoader)
        else:
            raise FileNotFoundError("文件路径不存在")
        return result
if __name__ == '__main__':
    print(GetYamlData().readYamlData("D:/code/new_qkex_api/data/perpetual/reverage.yaml"))