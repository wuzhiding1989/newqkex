"""
@author: xinkuncai
@license: (C) Copyright 2020-2099, Node Supply Chain Manager Corporation Limited.
@contact:
@software:
@file: conftest
@time: 2023-05-15
@desc:
"""
import jsonpath
import pytest
import time
import allure
import requests
import ast

from common.getCookie import login
from common.setting import ensure_path_sep
from utils.requests_tool.request_control import cache_regular
from utils.logging_tool.log_control import INFO, ERROR, WARNING
from utils.other_tools.models import TestCase
from utils.read_files_tools.clean_files import del_file
from utils.other_tools.allure_data.allure_tools import allure_step, allure_step_no
from utils.cache_process.cache_control import CacheHandler, Cache


@pytest.fixture(scope="session", autouse=False)
def clear_report():
    """如clean命名无法删除报告，这里手动删除"""
    del_file(ensure_path_sep("\\report"))


@pytest.fixture(scope="session", autouse=True)
def work_login_init():
    """
    获取登录的cookie
    :return:
    """

    # url = ""
    # data = {
    #     "username": 18800000001,
    #     "password": 123456
    # }
    # headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # # 请求登录接口
    #
    # res = requests.post(url=url, data=data, verify=True, headers=headers)
    # response_cookie = res.cookies
    #
    # cookies = ''
    # for k, v in response_cookie.items():
    #     _cookie = k + "=" + v + ";"
    #     # 拿到登录的cookie内容，cookie拿到的是字典类型，转换成对应的格式
    #     cookies += _cookie
    #     # 将登录接口中的cookie写入缓存中，其中login_cookie是缓存名称
    account = '12345678@qq.com'
    password = 'qa123456'
    verifyCode = '111111'
    res_data = login(account, password, verifyCode)

    CacheHandler.update_cache(cache_name='login_cookie', value=res_data)

    # account = '52345678@qq.com'
    account="72345678@qq.com"
    password = 'qa123456'
    verifyCode = '111111'
    res_data = login(account, password, verifyCode)

    CacheHandler.update_cache(cache_name='login_consumer_cookie', value=res_data)

    account = '42345678@qq.com'
    password = 'qa123456'
    verifyCode = '111111'
    res_data = login(account, password, verifyCode)

    CacheHandler.update_cache(cache_name='login_consumer2_cookie', value=res_data)

    # cookies="eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyN2MwNjE5Zi04N2FlLTQ4ODEtYjFkMi1lODFlZGZjNzcxZmEiLCJ1aWQiOiJXWFAxUS8xa2s5NVQxTjRxOWxuSFRBPT0iLCJiaWQiOiJXWFAxUS8xa2s5NVQxTjRxOWxuSFRBPT0iLCJpcCI6IkdwdHl4M01ZbzBJemNsL3pwN0ZiNXc9PSIsImRldiI6InAva3BIckF3RkJjSUZleXg0U2xkZGc9PSIsInN0cyI6MCwiaWF0IjoxNjcyNTAyNDAwLCJleHAiOjE2ODgxNDA4MDAsImlzcyI6InFrZXgifQ.7HKuzZz-IC0_Zs5hVK420jVbgpsgRP-NlYtxrUiTs0U"
    # cookies="eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI3ZjBiNWZkNS1kZjE2LTQwYTYtYTUxNS0yZDkwYmQ4YTZiZWYyMTAzNzIyMDIzIiwidWlkIjoieUdxdFQwbzMvZmdwN08wRlcvR1pZQT09IiwiYmlkIjoibVdPTzdGMnpzTjBUd1JBeVFEbGsrQT09IiwiaXAiOiJXWU5oVGYvdXNWUkFQb3BFenpra0RnPT0iLCJkZXYiOiJBOG9MTmVSVnZGR294TDlQWmVoa3BBPT0iLCJzdHMiOjAsImlhdCI6MTY4NDcyMTc0OSwiZXhwIjoxNjg0ODA4MTQ5LCJpc3MiOiJ3Y3MifQ.gozTXQlo3CclpyBC7DbC5wqBAN0WbuP8saM7_65p6-U"
    account = '12345678@qq.com'
    password = 'qa123456'
    verifyCode = '111111'
    res_data = login(account, password, verifyCode)
    CacheHandler.update_cache(cache_name="login_futures_user",value=res_data)


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的 item 的 name 和 node_id 的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")

    # 期望用例顺序
    # print("收集到的测试用例:%s" % items)
    appoint_items = []

    # 指定运行顺序
    run_items = []
    for i in appoint_items:
        for item in items:
            module_item = item.name.split("[")[0]
            if i == module_item:
                run_items.append(item)

    for i in run_items:
        run_index = run_items.index(i)
        items_index = items.index(i)

        if run_index != items_index:
            n_data = items[run_index]
            run_index = items.index(n_data)
            items[items_index], items[run_index] = items[run_index], items[items_index]


def pytest_configure(config):
    config.addinivalue_line("markers", 'smoke')
    config.addinivalue_line("markers", '回归测试')


@pytest.fixture(scope="function", autouse=True)
def case_skip(in_data):
    """处理跳过用例"""
    in_data = TestCase(**in_data)
    if ast.literal_eval(cache_regular(str(in_data.is_run))) is False:
        allure.dynamic.title(in_data.detail)
        allure_step_no(f"请求URL: {in_data.is_run}")
        allure_step_no(f"请求方式: {in_data.method}")
        allure_step("请求头: ", in_data.headers)
        allure_step("请求数据: ", in_data.data)
        allure_step("依赖数据: ", in_data.dependence_case_data)
        allure_step("预期数据: ", in_data.assert_data)
        pytest.skip()

# @pytest.fixture(scope="function", autouse=True)
# def case_clean_cache():
#     CacheHandler.clean_cache()


def pytest_terminal_summary(terminalreporter):
    """
    收集测试结果
    """

    _PASSED = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    _ERROR = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    _FAILED = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    _SKIPPED = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    _TOTAL = terminalreporter._numcollected
    _TIMES = time.time() - terminalreporter._sessionstarttime
    INFO.logger.error(f"用例总数: {_TOTAL}")
    INFO.logger.error(f"异常用例数: {_ERROR}")
    ERROR.logger.error(f"失败用例数: {_FAILED}")
    WARNING.logger.warning(f"跳过用例数: {_SKIPPED}")
    INFO.logger.info("用例执行时长: %.2f" % _TIMES + " s")

    try:
        _RATE = _PASSED / _TOTAL * 100
        INFO.logger.info("用例成功率: %.2f" % _RATE + " %")
    except ZeroDivisionError:
        INFO.logger.info("用例成功率: 0.00 %")