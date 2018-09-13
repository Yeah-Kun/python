"""
    create by Ian in 2017-12-28 17:17:28
    形势与政策刷题
"""
import requests
import re
import time
from lxml import html

class User(object):
    def __init__(self, sid, pwd):
        self.sid = sid
        self.pwd = pwd
        self.spl = None  # 成功登录后的特殊字符串
        self.name = None # 学生姓名

    def getVcode(self):
        """访问登录界面
        获取并解析vcode，保存cookied

        输入：网址，str
        输出：vcode，str
                cookies，class 'requests.cookies.RequestsCookieJar'
        """
        url = "http://course.wyu.cn/xsyzc/stlogon/getpage.asp?url=http%3A//jwc.wyu.cn/logonuser/st_logon.asp"
        r = requests.post(url)
        self.cookies = r.cookies
        match_pat = "(?<=value%3D%22)\w+(?=%22)"
        match_obj = re.search(match_pat, r.text)
        self.vcode = match_obj.group(0)
        return self.vcode

    def login_check(self):
        """登录验证，并获取成功登录的信息

        输入：账号密码拼接成的网址，str
        输出：一个特别的字符串，str
        """
        url = r"http://course.wyu.cn/xsyzc/stlogon/postpage.asp?url=http%3A//jwc.wyu.cn/logonuser/st_login.asp::::vcode%7E%7E"
        self.getVcode()
        self.loginurl = url + self.vcode + r"%40%40id%7E%7E6221" + r"%40%40u%7E%7E" + \
            self.sid + r"%40%40p%7E%7E" + self.pwd + r"%40%40v%7E%7E%40%40b%7E%7E"
        r = requests.get(self.loginurl, cookies=self.cookies)
        if r.text != "Error":
            self.spl = r.text
            return True
        else:
            return False

    def login(self):
        """登录主页面，可以进行查分和做题操作
        """
        if self.login_check():
            url = "http://course.wyu.cn/xsyzc/stlogon/mylogon.asp"
            self.spl = re.sub("%\d{2}|%\d[A-Z]", u"/", self.spl)
            print(self.spl)
            data = {"vd": self.spl}
            r = requests.post(url, cookies=self.cookies,
                              data = data)
            r.encoding = "utf8"
            print(r.status_code, r.text)
            u = "http://course.wyu.cn/xsyzc/eoexam/t_mark.asp"
            r = requests.get(u, cookies=self.cookies)
            self.tree = html.fromstring(r.text)
            r.encoding = "utf8"
            print(r.text)

    def search(self):
        """查分
        """
        if self.login_check():
            url = "http://course.wyu.cn/xsyzc/eoexam/t_mark.asp"
            r = requests.get(url, cookies=self.cookies)
            print(r.text)

    def paper(self):
        """做题
        """
        url = "http://course.wyu.cn/xsyzc/eoexam/t_paper.asp"
        r = requests.get(url, cookies=self.cookies)
        r.encoding = "utf8"
        print(r.text)

    def testLxml(self):
        r = self.tree.xpath("//td[@class='Text_TD']")
        for i in r:
            print(i.text)


if __name__ == '__main__':
    u = User("3115001780", "SS525358")
    text = u.login()
    u.testLxml()
    

