'''
	主函数，用于运行源代码
'''
from urllib.request import urlopen, HTTPError, URLError
import pickle
import json
from bs4 import BeautifulSoup as bs
import re
from TDcup import tree_algorithm, the_module
from lxml import etree
from socket import timeout
'''
# 打开文件，读取信息，关闭文件
all_url_file = open(
    "C题.pkl", "rb")
html = pickle.load(all_url_file)
all_url_file.close()
'''

html = open('C题-url_verify.txt', 'r')

# 查看进度计数器
n = 1
k = 1


# 主函数
for each in html:
    try:
        req = urlopen(each)
        bs0bj = bs(req)
        bs0bj = str(bs0bj)
        tree = etree.HTML(bs0bj)  # 解析树
        t = tree.getroottree()  # 构造元素树对象
        # 提取主题帖信息
        title = the_module.FindTitle(bs0bj, tree)  # 主题贴标题
        author = the_module.FindAuthor(bs0bj, tree)  # 主题帖作者
        date = the_module.FindDate(bs0bj)  # 主题帖时间
        content = the_module.FindMain(bs0bj)  # 主题帖内容
        dict_all = dict(author, **title, **content, **date)  # 将多个字典合在一起
        dict_all = str(dict_all)
        main_data = {'post': dict_all}
        # 回帖预处理
        standard_value = the_module.StandardValue(bs0bj)
        tag_path = tree_algorithm.TreeAlgotithm(
            bs0bj, standard_value)  # 获取楼层绝对路径容器
        return_data = []  # 回帖容器
        # 提取回帖信息
        if tag_path != None:
            for one_path in tag_path:  # 解析绝对路径容器，获得单个楼层的绝对路径

                date = the_module.FindFloorDate(tree, one_path)  # 时间提取
                author = the_module.FindUserName(tree, one_path)  # 用户名提取
                content = the_module.FindFloorContent(tree, one_path)  # 回帖内容提取
                dict_one_all = dict(author, **content, **date)  # 字典包装
                return_data.append(dict_one_all)
        else:
            pass

        reply = {'replys': return_data}  # 把回帖包裹起来
        final_data = dict(main_data, **reply)
        print(final_data)
        with open("3115000554.txt", 'a') as json_keep:
            json.dump(each, json_keep, indent=1)
            json.dump(final_data, json_keep, ensure_ascii=False, indent=0)
        n = n + 1
        print(n)

    # 异常处理
    except (HTTPError, ConnectionResetError, URLError, AttributeError, TypeError, UnicodeEncodeError, timeout) as reason:
        error_file = open("all_url_error.txt", "a")
        reason = str(k) + '.' + str(reason) + '\n'
        error_file.writelines(reason)
        error_file.close()
        print(reason)
        k += 1
        continue
