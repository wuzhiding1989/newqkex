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

        url="data:image/jpeg;base64,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"
        headers={
            # "Accept":"application/json, text/javascript, */*; q=0.01",
            #      "Host":"iforgot.apple.com",
                 # "Referer":"https://iforgot.apple.com/",
                 # "cookie":"X-Apple-I-Web-Token=AAAAKzI3fDFmMzZhNDc0OGZhOTcwMzE5MmRkMWM0YTMwNTdjNmE5AAABiGbVdxvCldheD1Cu8+CkuKqht4mjefqFiGxxuVnDzUOzJgae1xtMaJ8TWQActOBmEvFVgGLyB3RDkvVwJx6HbSP7zpp+kr0Jilb+7T7C9kUuAl0=; dslang=CN-ZH; site=CHN; idclient=web; ifs=A7FF8BA292D6D4B4748029C5164A70AB06C746440E6F2205DCB61E370AB8B39D621E66C1723969123229003D2F34E1592A46E68454A91E2AD6E35BECEC36F22A1502E7C16BBBA2CAF4A3481E774C4031276B3F3B40E06718F1D1A719EED1755FAFD2974834BD8211E97E18444F68271BC69F746DBEECCCF27F324F277D5EFEE6655E5DFD3C738FDDC0EACD2FCA9FBA8C9F27D7D5383E1E30AA0FD22C1E4A4B94698E7E038E4E4BEBB6339E34256BF8250048170349F963FD63C10FD1149E63CF3DFAB16FE512C619F7396353E4E2868669F45151A1E59518ABF7A3A5D4531806CAEE7786FEB6F7A5595A2A7244DE866E6FC4A70DFA6B81B1ABA633973AFF5AD0; ifssp=DF2B4C3E4EE3F5A506B3D75FE2B2CC3E2B6E04EB871234AA7254702CCA12F7E5A1BD63E69890886F6FF6EDB8B65C3480446860964A3CC68D5C44E62C5253AB3D93DB57578F8A5F26EA6E4CBA9049B7B641BD411BB44F959EF42FA6F85ABCCD66F8E175BDC2E936161158DC016DE66BECE895EC4DA1870D5F"
                 # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
                 }
        res=requests.request(method="get",headers=headers,url=url)
        print("res.content:",res.content)
        print(res)

    def demo(self):
        driver=webdriver.Chrome()
        driver.get("https://iforgot.apple.com/password/verify/appleid")
        res=GoogleAccountCheck().get_captcha()
        print("demores,",res)
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
        driver.find_element(By.XPATH,"/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/global-v2/div/idms-flow/div/forgot-password/div/div/div[1]/idms-step/div/div/div/div[2]/div/div[1]/div[1]/div/idms-textbox/idms-error-wrapper/div/div/input").send_keys("82934893025")
        driver.find_element(By.XPATH,"/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/global-v2/div/idms-flow/div/forgot-password/div/div/div[1]/idms-step/div/div/div/div[2]/div/div[1]/div[2]/div/iforgot-captcha/div/div/div[1]/idms-textbox/idms-error-wrapper/div/div/input").send_keys(code_text)
        sleep(2)
        driver.find_element(By.XPATH,"/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/global-v2/div/idms-flow/div/forgot-password/div/div/div[1]/idms-step/div/div/div/div[3]/idms-toolbar/div/div/div/button").click()
        sleep(1)
        try:
            ele=driver.find_element(By.XPATH,"/html/body/div[1]/iforgot-v2/app-container/div/iforgot-body/global-v2/div/idms-flow/div/forgot-password/div/div/div[1]/idms-step/div/div/div/div[2]/div/div[1]/div[1]/div/idms-textbox/idms-error-wrapper/div/idms-error/div/div/span")
            print("APPID 不通过")
        except Exception as e:
            print("APPID 通过")

    def get(self):
        string=""
        for i in range(256):
            data=random.randint(1,9)
            string=str(data)+string

        print(string)


    def get_captab(self):
        import requests
        from PIL import Image
        # 发送GET请求获取验证码图片数据
        url = "https://iforgot.apple.com/password/verify/appleid"
        response = requests.get(url)
        # 将图片数据解码并保存为本地文件
        with open("captcha.jpg", "wb") as f:
            f.write(response.content)
        # 使用PIL库打开并显示验证码图片
        image = Image.open(r"D:\code\qkex_api_master\newqkex5\newqkex\case\captcha.jpg")
        image.show()

    # def get_getHtmlcontent(self):
    #     url = "https://iforgot.apple.com/password/verify/appleid"
    #     page=urllib.urlopen(url)
    #     text=page.read()
    #

if __name__ == '__main__':
    # GoogleAccountCheck().get_captcha()
    GoogleAccountCheck().demo()
    # GoogleAccountCheck().get_captab()
    # GoogleAccountCheck().get_getHtmlcontent()
