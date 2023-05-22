# const time = new Date().getTime();
#       const signBody = `taskId=${taskId}&payload=${
#         params ? JSON.stringify(params) : JSON.stringify({})
#       }&method=${method}&path=${path}&time=${time}`;
#       headers.append('secret', createSign(signBody));
#       headers.append('time', time.toString());
#
#
#
#
# export function createSign(data) {
#   const sign = crypto.createSign('RSA-SHA1');
#   sign.update(data);
#   sign.end();
#   return sign.sign(FRONT_PRI_KEY).toString('base64')
# }
import base64
from turtledemo.clock import jump

import rsa
import hashlib
import binascii
import json
import time
from common.util import createSign
from common.util import request_http as req, truncate, printc, d, requests, priceSpread, t as _t, countCaseNumber

key = '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'
params = {
  '_id': '6364d9a1defa0b0102652041',
  'uid': '372863',
  'dptId': '5fe436b57c395d009788a84e',
  'remarks': 'admin安全测试F2a  bella',
  'status': '1',
  'asanaLink': 'https://f2c.qa.atomintl.com/zh-CN/convert/',
  'currencyCode': 'USDT',
  'quantity': '1',
  'createdBy': {
    'id': '62aaa89c6cd5c00049c77f4c',
    'loginName': 'bella.wei@atomintl.com'
  },
  'createdAt': '2022-11-04T09:21:37.944Z',
  'updatedAt': '2022-11-04T09:21:37.944Z',
  'dptName': '1224test',
  'id': '6364d9a1defa0b0102652041'

}
token='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJBVE9NSU5UTCIsInVpZCI6MCwiaWF0IjoxNTQ3MDExNTU1LCJleHAiOjE4NjIzNzE1NTV9.OrshYNjmPqSNCfVvFUYSCFJIOnKQntqTPEfW78W0nAY5lp29U5aMn74xaqw_Uux7GilHUu4_yhYhv5pHgrV53ZAcI0bh8A71Mgq5DUC1_4wQEtmHTtSh3ccQj8zhjl2q_ixRx4sPuUxzYYnt5VA4E1_uOr8ZnYiAJWmCZ4ImhW3pKeFcbiUS4RFHt-iJPxz9c9HCc9V9WcCII6S1JrzSj2vy6f0XFVfHVwqw4i9mUjttkLN91q1XtR4TrF56UN3b620kGAdg8uHq-Wu_MHrbMpN54Xo7jUWZKMTQlrFQlrw0ON3HQmRGqmgDgeO7AwwzbTvb-3bI2YoCo7b4LulVAQ'
def adminBudget(key,params):
    id = '6364d9a1defa0b0102652041'
    header=[]
    nowtime = str(int(time.time() * 1000))
    method ='PUT'
    host_url = 'http://192.168.2.25:36030'
    request_path ='/v2/admin/budget/6364d9a1defa0b0102652041'
    secret_key = key
    # params = params.json()
    # sige = createSign(params, method, host_url, request_path, secret_key)
    sige = createSign(id,params,method,request_path,nowtime,secret_key)
    url = host_url + request_path
    header.append(sige)
    header.append(nowtime)
    header.append(id)
    res = req('put',url=url,params=params,auth=token,op=header)
    return res


def createSign(id,params,method,path,nowtime,secret_key):
    data = f'taskId={id}&payload={params}&method={method}&path={path}&time={nowtime}'
    # params = "aaaa"
    a = rsa.sign(str(data), priv_key=secret_key,hash_method='SHA-1')
    return  base64.b64encode(a)

if __name__ == '__main__':
    print(adminBudget(key,params))
    # print(createSign())