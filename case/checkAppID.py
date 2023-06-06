import base64
import smtplib
from email.mime.text import MIMEText

import ddddocr
import pymysql
import requests


class Check_AppID:

    def get_captcha(self):
        #登录接口
        url="https://iforgot.apple.com/captcha?captchaType=IMAGE"
        data={"captchaType":"IMAGE"}
        headers={"Accept":"application/json, text/javascript, */*; q=0.01",
                 "Host":"iforgot.apple.com",
                 # "Referer":"https://iforgot.apple.com/",
                 # "cookie":"X-Apple-I-Web-Token=AAAAKzI3fDFmMzZhNDc0OGZhOTcwMzE5MmRkMWM0YTMwNTdjNmE5AAABiGbVdxvCldheD1Cu8+CkuKqht4mjefqFiGxxuVnDzUOzJgae1xtMaJ8TWQActOBmEvFVgGLyB3RDkvVwJx6HbSP7zpp+kr0Jilb+7T7C9kUuAl0=; dslang=CN-ZH; site=CHN; idclient=web; ifs=A7FF8BA292D6D4B4748029C5164A70AB06C746440E6F2205DCB61E370AB8B39D621E66C1723969123229003D2F34E1592A46E68454A91E2AD6E35BECEC36F22A1502E7C16BBBA2CAF4A3481E774C4031276B3F3B40E06718F1D1A719EED1755FAFD2974834BD8211E97E18444F68271BC69F746DBEECCCF27F324F277D5EFEE6655E5DFD3C738FDDC0EACD2FCA9FBA8C9F27D7D5383E1E30AA0FD22C1E4A4B94698E7E038E4E4BEBB6339E34256BF8250048170349F963FD63C10FD1149E63CF3DFAB16FE512C619F7396353E4E2868669F45151A1E59518ABF7A3A5D4531806CAEE7786FEB6F7A5595A2A7244DE866E6FC4A70DFA6B81B1ABA633973AFF5AD0; ifssp=DF2B4C3E4EE3F5A506B3D75FE2B2CC3E2B6E04EB871234AA7254702CCA12F7E5A1BD63E69890886F6FF6EDB8B65C3480446860964A3CC68D5C44E62C5253AB3D93DB57578F8A5F26EA6E4CBA9049B7B641BD411BB44F959EF42FA6F85ABCCD66F8E175BDC2E936161158DC016DE66BECE895EC4DA1870D5F"
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
                 }
        res=requests.request(method="get",url=url,headers=headers,verify=False)
        # print("res:",res.json())
        # print("res.content:",res.content)
        return res

    def verify_appleid(self,appid,id,answer,token):
        url="https://iforgot.apple.com/password/verify/appleid"
        headers = {"Accept": "application/json, text/javascript, */*; q=0.01",
                   "Host": "iforgot.apple.com",
                   # "Referer":"https://iforgot.apple.com/",
                   # "cookie":"X-Apple-I-Web-Token=AAAAKzI3fDFmMzZhNDc0OGZhOTcwMzE5MmRkMWM0YTMwNTdjNmE5AAABiGbVdxvCldheD1Cu8+CkuKqht4mjefqFiGxxuVnDzUOzJgae1xtMaJ8TWQActOBmEvFVgGLyB3RDkvVwJx6HbSP7zpp+kr0Jilb+7T7C9kUuAl0=; dslang=CN-ZH; site=CHN; idclient=web; ifs=A7FF8BA292D6D4B4748029C5164A70AB06C746440E6F2205DCB61E370AB8B39D621E66C1723969123229003D2F34E1592A46E68454A91E2AD6E35BECEC36F22A1502E7C16BBBA2CAF4A3481E774C4031276B3F3B40E06718F1D1A719EED1755FAFD2974834BD8211E97E18444F68271BC69F746DBEECCCF27F324F277D5EFEE6655E5DFD3C738FDDC0EACD2FCA9FBA8C9F27D7D5383E1E30AA0FD22C1E4A4B94698E7E038E4E4BEBB6339E34256BF8250048170349F963FD63C10FD1149E63CF3DFAB16FE512C619F7396353E4E2868669F45151A1E59518ABF7A3A5D4531806CAEE7786FEB6F7A5595A2A7244DE866E6FC4A70DFA6B81B1ABA633973AFF5AD0; ifssp=DF2B4C3E4EE3F5A506B3D75FE2B2CC3E2B6E04EB871234AA7254702CCA12F7E5A1BD63E69890886F6FF6EDB8B65C3480446860964A3CC68D5C44E62C5253AB3D93DB57578F8A5F26EA6E4CBA9049B7B641BD411BB44F959EF42FA6F85ABCCD66F8E175BDC2E936161158DC016DE66BECE895EC4DA1870D5F"
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
                   }
        data={"id": appid, "captcha": {"id": id, "answer": answer,
                                    "token": token}}
        va_res=requests.request(method="post",url=url,headers=headers,json=data)
        print(va_res)
        return va_res


    def check_appid(self,appid):
        flag=True
        #获取登录接口
        res=Check_AppID().get_captcha()
        print("res.content:",res.json()["payload"]["content"])
        id=res.json()['id']
        token=res.json()['token']
        image_Data=res.json()["payload"]["content"]
        #解码图片
        image_Data=base64.urlsafe_b64decode(image_Data)

        ocr=ddddocr.DdddOcr()
        #解析成输入字符串
        code=ocr.classification(image_Data)
        # print(code)
        res=Check_AppID().verify_appleid(appid=appid,id=id,token=token,answer=code)
        print(res.json())
        if "This Apple ID is not valid or not supported" in str(res.json()):
            print("APPID已禁用")
            flag=False
            return flag
        #判断验证码没有效再次请求
        if "Please enter the characters you see or hear to continue" in str(res.json()):
            Check_AppID().check_appid(appid)
        if "length must be between 1 and 128" in str(res.json()):
            print("账号长度不规范")
            flag=False
            return flag
        else:
            print("APPID已启用")
            flag=True
            return flag
    def mysqlClient_select(self,sql):
        #链接数据库获取现有的APPID
        host = 'database-1.cnxpymarugg3.ap-southeast-1.rds.amazonaws.com'
        user = 'admin'
        password = '6Gp0iz1ZHNceJKwSpNg6'
        database = 'foundation'
        db = pymysql.connect(host=host, user=user, password=password, database=database)  # 打开数据库连接
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = sql  # 执行SQL语句
        cursor.execute(sql)
        data = cursor.fetchall()
        db.close()  # 关闭数据库连接
        return data

    def send_mail(self, user_list: list, sub, content: str) -> None:
        """

        @param user_list: 发件人邮箱
        @param sub:
        @param content: 发送内容
        @return:
        """
        user = "xinkuncai" + "<" + "759180302@qq.com" + ">"
        message = MIMEText(content, _subtype='plain', _charset='utf-8')
        message['Subject'] = sub
        message['From'] = user
        message['To'] = ";".join(user_list)
        server = smtplib.SMTP()
        server.connect("smtp.qq.com")
        server.login("759180302@qq.com", "bhiqfwrrtcjabdci")
        server.sendmail(user, user_list, message.as_string())
        server.close()


    def run(self):
        #执行方法
        # Check_AppID().check_appid("qakuncai@163.com")
        appId_list=[]
        accounts= Check_AppID().mysqlClient_select("select account from app_store_account where status=1;")
        for account in accounts:
            print(account[0])
            test_data=accounts[0]
            flag=Check_AppID().check_appid(str(account[0]))
            if not flag:
                appId_list.append(str(account[0]))

        content="APPID"+str(appId_list)+"已被禁用"
        send_list=["759180302@qq.com"]
        sub="APPID检测"
        Check_AppID().send_mail(send_list,sub=sub,content=content)


if __name__ == '__main__':
    Check_AppID().run()
    # Check_AppID().send_mail(["759180302@qq.com"],"test","test")