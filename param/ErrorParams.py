

errorCode=1001

errorParamsCommon=[['null',1,'传空'],['1E+5',1,'科学计数法']]

Price_ErrorParamList = [[10000000, '1045', '传int类型10000000'], ['一万', errorCode, '传中文一万'], [None, errorCode, '不传price'],
                        ['@#¥%&*', errorCode, '传特殊字符@#¥%&*'], ['10000.000001', '1045', '传不符合ticeSize'],
                        ['10000.091', '1045', 'price超过最小精度'], ['-10000', errorCode, 'price传负数'],
                        ['0', errorCode, 'price传0'], ['1.321e+4', errorCode, 'price传科学计数法'],
                        ['null', errorCode, 'price传null']]
TriggerType_ErrorParamList=[[123, '1045', '传int类型123'],["LastIndex", '1045', '传不存在的触发类型LastIndex'],[None,"1","不传参"],["null","1","传字符串null"],["  ","1","传空字符串"]]

