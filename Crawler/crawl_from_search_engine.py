import os
import sys
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from lxml import etree
from bs4 import BeautifulSoup as bs
import urllib.request
from googletrans import Translator
import pickle
# would be really good if you can also add output to the code...

# 搜索url
base_url_part1 = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word='
base_url_part2 = '&oq=bagua&rsp=0'  # base_url_part1以及base_url_part2都是固定不变的，无需更改

# chrome驱动
location_driver = 'C:/vcpkg/chromedriver.exe'


class KeywordGenerator:
    def __init__(self, main_keyword, keywords, main_dir = ""):
        self.__main_keywords = main_keyword
        self.__keywords = keywords
        self.__main_dir = main_dir
        self.__key_dict = dict()
        self.__keywords_backup = os.path.join(main_dir, main_keyword + "_keywords.pkl")

        # 输入判断


        # 加载本地关键字
        if os.path.exists(self.__keywords_backup):
            with open(self.__keywords_backup, "rb") as file:
                file_content = pickle.load(file)
                if self.__keywords == file_content[0]:
                    self.__key_dict = file_content[1]

    def generate(self):
        """
            return: {"Chinese" : "English", ...}
        """
        def format_tranlation(s):
            s = s.capitalize()
            return re.sub(r' \w', lambda x: x.group(0)[1].upper(), s)

        if self.__key_dict != dict():
            return self.__key_dict

        print("出错：" + self.__key_dict)
        # 翻译
        translator = Translator()
        main_keyword_en = format_tranlation(translator.translate(main_keyword, dest='en').text)
        for k in keywords:
            try:
                k_en = format_tranlation(translator.translate(k, dest='en').text)
            except Exception as reason:
                print("Error:" + reason)
            
            self.__key_dict["{} {}".format(main_keyword, k)] = k_en

        # 保存此次生成的值
        with open(self.__keywords_backup, "wb") as pickle_backup:
            pickle.dump([self.__keywords, self.__key_dict], pickle_backup)

        return self.__key_dict


class Crawler:
    def __init__(self, keywords, main_dir):
        self.__main_dir = main_dir
        self.__keywords = keywords

        # 初始化
        chrome_options = Options()
        chrome_options.add_argument("--disable-infobars")
        # 启动Chrome浏览器
        self.__driver = webdriver.Chrome(
            executable_path=location_driver, chrome_options=chrome_options)
        # 最大化窗口，因为每一次爬取只能看到视窗内的图片
        self.__driver.maximize_window()
    
    def __del__(self):
        self.__driver.close()

    def get_main_page_url(self, search_query):
        return base_url_part1 + search_query + base_url_part2

    def get_image(self, main_url, keyword, main_dir, needed_number):
        """
            main_url：搜索页面url
            keyword：关键字（英文）
            main_dir：存储图片的主目录
            needed_number：需要下载的图片数量
        """
        def get_image_urls(html_page):
            # tree = etree.parse(html_page)
            # sub_tree = tree.xpath('//*[@id="imgid"]/div[1]/ul')
            soup = bs(html_page, "html.parser")
            # 通过soup对象中的findAll函数图像信息提取
            return soup.findAll('img', {'src': re.compile(r'https:.*\.(jpg|png)')})
        
        def generate_filename(keyword, number):
            return keyword + '_' + '{:0>8d}'.format(number) + ".jpg"

        # 判断主目录是否存在
        if not os.path.exists(main_dir):
            os.makedirs(main_dir)
        
        # 创建对应类别的子目录
        sub_dir = os.path.join(main_dir, keyword)
        if not os.path.exists(sub_dir):
            os.makedirs(sub_dir)

        # 初始化
        url_set = set()
        save_counter = 0
        pos = 0
        self.__driver.get(main_url)

        # 循环保存
        while(save_counter < needed_number):
            # 读图片
            pos += 500  # 每次下滚500
            js = "document.documentElement.scrollTop=%d" % pos
            self.__driver.execute_script(js)

            # 获得源码
            html_page = self.__driver.page_source
            image_urls = get_image_urls(html_page)

            for url_page in image_urls:
                url = url_page['src']
                if url not in url_set:
                    print("Download url:{}".format(url))
                    url_set.add(url)

                    # 下载到固定目录
                    if(save_counter < needed_number):
                        save_counter += 1
                        filename = generate_filename(keyword, save_counter)
                        print("filename:" + filename)
                        try:
                            urllib.request.urlretrieve(url, os.path.join(sub_dir, filename)) 
                        finally:
                            pass
                    else:
                        return
                    



    def run(self, needed_number):
        print("Start crawl...")
        for Chinese, English in self.__keywords.items():
            self.get_image(self.get_main_page_url(Chinese), English, self.__main_dir, needed_number)
        
        print("Successfully dowmload.")


if __name__ == "__main__":
    main_keyword = "人 表情"
    keywords = ["开心", "愤怒", "悲伤", "恐惧", "平静"]
    k = KeywordGenerator(main_keyword, keywords)
    c = Crawler(k.generate(), "D:/")
    c.run(600)
