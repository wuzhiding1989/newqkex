import requests

account = 'ceshi';
password = 2222222;
captcha = 123131
url = 'http://13.215.135.141:9999'
headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5",
           "Cookie": "token=c7ebd817-d668-46eb-a80f-d5de9cd2f866; expire_time=20211029155728",
           "Accept": "application/json, text/plain, */*", "Content-Type": "application/json", "Connection": "close",
           "Accept-Language": "zh-CN", "X-Authorization": "", "language": "Chinese"}


class admin:

    def __init__(self, account, password, captcha):
        res = self.login(account, password, captcha)
        headers['Cookie'] = res

    def login(self, account, password, captcha):
        params = {
            'account': account,
            'password': password,
            'captcha': captcha
        }
        path = '/login/auth'
        session = requests.Session()
        session.post(url + path, data=params)
        request_cookies = session.cookies.get_dict()
        request_cookies = 'JSESSIONID=' + request_cookies['JSESSIONID']

        return request_cookies



    # 获取kyc信息level=1是kyc1，level=2是kyc2
    def getKycUser(self, userId, level):
        params = {
            'userId': userId,
            'level': level
        }
        path = '/boss/uCenter/kyc/getKycUser'
        res = requests.post(url + path, params=params, headers=headers).json()
        return res

    # kyc审核通过level=1是kyc1，level=2是kyc2
    def kycpass(self, id, userId, countryCode,level, email, remarks=None, mobile=None):
        params = {
            'id': id,
            'leavingMessage':'Approve.',
            'userId': userId,
            'level': level,
            'countryCode': countryCode,
            'email': email,
            'remarks': remarks,
            'mobile': mobile
        }
        path = '/boss/uCenter/kyc/pass'
        res = requests.post(url+path,data=params,headers=headers).json()
        return res
    #url='http://13.215.135.141:9999/boss/otc/configCurrency/list'
    def configCurrencyList(self):
        params ={

        }
        path = '/boss/otc/configCurrency/list'
        res = requests.get(url+path,data=params,headers=headers).json()
        return res


if __name__ == '__main__':
    ad = admin(account, password, captcha)
    # print(ad.getKycUser(userId=10122033, level=1))
    print(ad.configCurrencyList())
