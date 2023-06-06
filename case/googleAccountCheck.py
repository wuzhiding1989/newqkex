import base64
import random
import urllib
from io import BytesIO
from time import sleep

import ddddocr
import exifread
import requests
import pytesseract
import selenium
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
import pytesseract
class GoogleAccountCheck:

    def get_captcha(self):
        url="https://iforgot.apple.com/captcha?captchaType=IMAGE"
        data={"captchaType":"IMAGE"}
        headers={"Accept":"application/json, text/javascript, */*; q=0.01",
                 "Host":"iforgot.apple.com",
                 # "Referer":"https://iforgot.apple.com/",
                 # "cookie":"X-Apple-I-Web-Token=AAAAKzI3fDFmMzZhNDc0OGZhOTcwMzE5MmRkMWM0YTMwNTdjNmE5AAABiGbVdxvCldheD1Cu8+CkuKqht4mjefqFiGxxuVnDzUOzJgae1xtMaJ8TWQActOBmEvFVgGLyB3RDkvVwJx6HbSP7zpp+kr0Jilb+7T7C9kUuAl0=; dslang=CN-ZH; site=CHN; idclient=web; ifs=A7FF8BA292D6D4B4748029C5164A70AB06C746440E6F2205DCB61E370AB8B39D621E66C1723969123229003D2F34E1592A46E68454A91E2AD6E35BECEC36F22A1502E7C16BBBA2CAF4A3481E774C4031276B3F3B40E06718F1D1A719EED1755FAFD2974834BD8211E97E18444F68271BC69F746DBEECCCF27F324F277D5EFEE6655E5DFD3C738FDDC0EACD2FCA9FBA8C9F27D7D5383E1E30AA0FD22C1E4A4B94698E7E038E4E4BEBB6339E34256BF8250048170349F963FD63C10FD1149E63CF3DFAB16FE512C619F7396353E4E2868669F45151A1E59518ABF7A3A5D4531806CAEE7786FEB6F7A5595A2A7244DE866E6FC4A70DFA6B81B1ABA633973AFF5AD0; ifssp=DF2B4C3E4EE3F5A506B3D75FE2B2CC3E2B6E04EB871234AA7254702CCA12F7E5A1BD63E69890886F6FF6EDB8B65C3480446860964A3CC68D5C44E62C5253AB3D93DB57578F8A5F26EA6E4CBA9049B7B641BD411BB44F959EF42FA6F85ABCCD66F8E175BDC2E936161158DC016DE66BECE895EC4DA1870D5F"
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
                 }
        res=requests.request(method="get",url=url,headers=headers,verify=False)
        print("res:",res.json())
        print("res.content:",res.content)
        return res

    def get_captcha2(self):

        url="data:image/jpeg;base64, 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"
        # with open("captcha1.jpeg",'wb')as f:
        #     f.write(url)
        #     f.close()

        # headers={
        #     # "Accept":"application/json, text/javascript, */*; q=0.01",
        #     #      "Host":"iforgot.apple.com",
        #          # "Referer":"https://iforgot.apple.com/",
        #          # "cookie":"X-Apple-I-Web-Token=AAAAKzI3fDFmMzZhNDc0OGZhOTcwMzE5MmRkMWM0YTMwNTdjNmE5AAABiGbVdxvCldheD1Cu8+CkuKqht4mjefqFiGxxuVnDzUOzJgae1xtMaJ8TWQActOBmEvFVgGLyB3RDkvVwJx6HbSP7zpp+kr0Jilb+7T7C9kUuAl0=; dslang=CN-ZH; site=CHN; idclient=web; ifs=A7FF8BA292D6D4B4748029C5164A70AB06C746440E6F2205DCB61E370AB8B39D621E66C1723969123229003D2F34E1592A46E68454A91E2AD6E35BECEC36F22A1502E7C16BBBA2CAF4A3481E774C4031276B3F3B40E06718F1D1A719EED1755FAFD2974834BD8211E97E18444F68271BC69F746DBEECCCF27F324F277D5EFEE6655E5DFD3C738FDDC0EACD2FCA9FBA8C9F27D7D5383E1E30AA0FD22C1E4A4B94698E7E038E4E4BEBB6339E34256BF8250048170349F963FD63C10FD1149E63CF3DFAB16FE512C619F7396353E4E2868669F45151A1E59518ABF7A3A5D4531806CAEE7786FEB6F7A5595A2A7244DE866E6FC4A70DFA6B81B1ABA633973AFF5AD0; ifssp=DF2B4C3E4EE3F5A506B3D75FE2B2CC3E2B6E04EB871234AA7254702CCA12F7E5A1BD63E69890886F6FF6EDB8B65C3480446860964A3CC68D5C44E62C5253AB3D93DB57578F8A5F26EA6E4CBA9049B7B641BD411BB44F959EF42FA6F85ABCCD66F8E175BDC2E936161158DC016DE66BECE895EC4DA1870D5F"
        #          # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        #          }
        res=requests.request(method="get",url=url)
        print(res)
        print("res.content:",res.content)
        # print(res)
    def verify_appleid(self,id,answer,token):
        url="https://iforgot.apple.com/password/verify/appleid"
        headers = {"Accept": "application/json, text/javascript, */*; q=0.01",
                   "Host": "iforgot.apple.com",
                   # "Referer":"https://iforgot.apple.com/",
                   # "cookie":"X-Apple-I-Web-Token=AAAAKzI3fDFmMzZhNDc0OGZhOTcwMzE5MmRkMWM0YTMwNTdjNmE5AAABiGbVdxvCldheD1Cu8+CkuKqht4mjefqFiGxxuVnDzUOzJgae1xtMaJ8TWQActOBmEvFVgGLyB3RDkvVwJx6HbSP7zpp+kr0Jilb+7T7C9kUuAl0=; dslang=CN-ZH; site=CHN; idclient=web; ifs=A7FF8BA292D6D4B4748029C5164A70AB06C746440E6F2205DCB61E370AB8B39D621E66C1723969123229003D2F34E1592A46E68454A91E2AD6E35BECEC36F22A1502E7C16BBBA2CAF4A3481E774C4031276B3F3B40E06718F1D1A719EED1755FAFD2974834BD8211E97E18444F68271BC69F746DBEECCCF27F324F277D5EFEE6655E5DFD3C738FDDC0EACD2FCA9FBA8C9F27D7D5383E1E30AA0FD22C1E4A4B94698E7E038E4E4BEBB6339E34256BF8250048170349F963FD63C10FD1149E63CF3DFAB16FE512C619F7396353E4E2868669F45151A1E59518ABF7A3A5D4531806CAEE7786FEB6F7A5595A2A7244DE866E6FC4A70DFA6B81B1ABA633973AFF5AD0; ifssp=DF2B4C3E4EE3F5A506B3D75FE2B2CC3E2B6E04EB871234AA7254702CCA12F7E5A1BD63E69890886F6FF6EDB8B65C3480446860964A3CC68D5C44E62C5253AB3D93DB57578F8A5F26EA6E4CBA9049B7B641BD411BB44F959EF42FA6F85ABCCD66F8E175BDC2E936161158DC016DE66BECE895EC4DA1870D5F"
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
                   }
        data={"id": "qakuncai@163.com123", "captcha": {"id": id, "answer": answer,
                                    "token": token}}
        va_res=requests.request(method="post",url=url,headers=headers,json=data)
        print(va_res)
        return va_res
    def demo(self):
        driver=webdriver.Chrome()
        driver.get("https://iforgot.apple.com/password/verify/appleid")
        res=GoogleAccountCheck().get_captcha()
        res.json()
        id=res.json()['id']
        token=res.json()['token']
        print("demores,",res.json())
        driver.maximize_window()
        sleep(3)

        element=driver.find_element(By.XPATH,'/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/global-v2/div/idms-flow/div/forgot-password/div/div/div[1]/idms-step/div/div/div/div[2]/div/div[1]/div[2]/div/iforgot-captcha/div/div/div[2]/div/div[1]/idms-captcha/div/div')
        print(element)
        png=element.screenshot_as_png
        print(png)
        # t=element.get_attribute("screenshot_as_png")
        # print(t)
        sleep(2)
        with(open("text.png","wb")) as f :
            f.write(png)
            f.close()
        #识别验证码
        ocr=ddddocr.DdddOcr()
        code_text=ocr.classification(png)
        print(code_text)
        # driver.find_element(By.XPATH,"/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/global-v2/div/idms-flow/div/forgot-password/div/div/div[1]/idms-step/div/div/div/div[2]/div/div[1]/div[1]/div/idms-textbox/idms-error-wrapper/div/div/input").send_keys("82934893025")
        # driver.find_element(By.XPATH,"/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/global-v2/div/idms-flow/div/forgot-password/div/div/div[1]/idms-step/div/div/div/div[2]/div/div[1]/div[2]/div/iforgot-captcha/div/div/div[1]/idms-textbox/idms-error-wrapper/div/div/input").send_keys(code_text)
        # sleep(2)
        # driver.find_element(By.XPATH,"/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/global-v2/div/idms-flow/div/forgot-password/div/div/div[1]/idms-step/div/div/div/div[3]/idms-toolbar/div/div/div/button").click()
        # sleep(1)
        # try:
        #     ele=driver.find_element(By.XPATH,"/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/global-v2/div/idms-flow/div/forgot-password/div/div/div[1]/idms-step/div/div/div/div[2]/div/div[1]/div[1]/div/idms-textbox/idms-error-wrapper/div/idms-error/div/div/span")
        #     print("APPID 不通过")
        # except Exception as e:
        #     print("APPID 通过")
        res=GoogleAccountCheck().verify_appleid(id=id,answer=code_text,token=token)
        print(res.text)




    def check_appid(self):
        res=GoogleAccountCheck().get_captcha()
        # print("res.content:",res.json()["payload"]["content"])
        id=res.json()['id']
        token=res.json()['token']
        image_Data=res.json()["payload"]["content"]
        #解码图片
        image_Data=base64.urlsafe_b64decode(image_Data)
        ocr=ddddocr.DdddOcr()
        code_text=ocr.classification(image_Data)
        print(code_text)
        res=GoogleAccountCheck().verify_appleid(id=id,token=token,answer=code_text)
        print(res.json())

if __name__ == '__main__':
    # GoogleAccountCheck().get_captcha()
    # GoogleAccountCheck().demo()
    # GoogleAccountCheck().get_captcha2()
    # GoogleAccountCheck().get_gdd()
    # GoogleAccountCheck().get_captab()
    # GoogleAccountCheck().get_getHtmlcontent()
    GoogleAccountCheck().check_appid()