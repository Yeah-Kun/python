from selenium import webdriver
import requests
import re
import PIL
import time

class User(object):
    def __init__(self, sid, pwd):
        self.sid = sid
        self.pwd = pwd
        self.spl = None  # 成功登录后的特殊字符串
        self.driver = webdriver.Ie("C:\\Users\\Yeah_Kun\\Anaconda3\\IEDriverServer.exe")

    def getVcode(self):
        """访问登录界面
        获取并解析vcode，保存cookied

        输入：网址,str
        输出：vcode,str
                cookies,str
        """
        url = "http://course.wyu.cn/xsyzc/stlogon/getpage.asp?url=http%3A//jwc.wyu.cn/logonuser/st_logon.asp"
        r = requests.post(url)
        self.cookies = {r.cookies.keys()[0] : r.cookies.values()[0]}
        match_pat = "(?<=value%3D%22)\w+(?=%22)"
        match_obj = re.search(match_pat, r.text)
        self.vcode = match_obj.group(0)
        return self.vcode

    def processImg(self):
    	"""获取验证码并识别
    	"""
    	self.getVcode()
    	# url = "http://jwc.wyu.cn/logonuser/code.asp?v=" + self.vcode
    	# r = requests.get(url, cookies = self.cookies)
    	# with open("v.BMP","wb") as f:
    	# 	f.write(r.content)

    	#self.driver.add_cookie(self.cookies)
    	self.driver.get("http://course.wyu.cn/xsyzc/stlogon/index.html?hl=zh-CN&tID=(128)")
    	time.sleep(15)
    	with open("v.txt","r") as f:
    		v = str(f.read()) # 验证码
    	self.driver.find_element_by_name("u").send_keys(self.sid)
    	self.driver.find_element_by_name("p").send_keys(self.pwd)
    	self.driver.find_element_by_name("v").send_keys(v)
    	self.driver.find_element_by_name("b").submit()
    	print("Yes！")


if __name__ == '__main__':
	u = User("3115000554","505452")
	u.processImg()
	#u.driver.quit()