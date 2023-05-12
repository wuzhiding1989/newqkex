"""
@author: xinkuncai
@license: (C) Copyright 2020-2099, Node Supply Chain Manager Corporation Limited.
@contact:  
@software: 
@file: models
@time: 2023-05-11 
@desc: 
"""
from pydantic import BaseModel
from typing import Text, Dict, Callable, Union, Optional, List, Any
class TestCase(BaseModel):
    url: Text
    method: Text
    headers: Union[None, Dict, Text] = {}
    data: Any = None
    assert_data: Dict


class ResponseData(BaseModel):
    url: Text
    response_data: Text
    request_body: Any
    method: Text
    yaml_data: "TestCase"
    headers: Dict
    cookie: Dict
    status_code: int
    assert_data: Dict
    # data: Dict
