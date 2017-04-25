'''
    提取模块，包含：标题，时间，正文内容，用户名，识别楼层数
'''
import re



# 提取标题
def FindTitle(bs0bj, tree):
    titledata = tree.xpath('//*[@id="thread_subject"]/text()')
    if len(titledata) == 0:
        titledata = tree.xpath('//title//text()')
    if len(titledata) == 0:
        title = {'title': 'None'}
    else:
        title = {'title': titledata[0]}
    return title


# 提取正文用户名
def FindAuthor(bs0bj, tree):
    authordata = tree.xpath('//tr[@class="t_f"]/text()')
    if len(authordata) == 0:
        authordata = tree.xpath('//a[@target="_blank" and class="xw1"]/text()')
    if len(authordata) == 0:
        authordata = tree.xpath('//a[@target="_blank"]/text()')
    if len(authordata) == 0:
        author = {'author': 'None'}
    else:
        author = {'author': authordata[0]}
    return author


#  提取时间
def FindDate(bs0bj):
    datedata = re.findall("发表于 (.*?)</em>", bs0bj)
    if len(datedata) == 0:
        datedata = re.findall("发表于 \d{4}-\d{2}-\d{2}", bs0bj)
    if len(datedata) == 0:
        datedata = re.findall("\d{4}-\d{2}-\d{2}", bs0bj)
    if len(datedata) == 0:
        datedata = re.findall("\d{4}/\d{2}/\d{2}", bs0bj)
    if len(datedata) == 0:
        datedata = re.findall("\d{2}-\d{2}-\d{4}", bs0bj)
    if len(datedata) == 0:
        date = {'publish_date': 'None'}
    else:
        date = {'publish_date': datedata[0]}
    return date


# 提取正文
def FindMain(bs0bj):
    standard = 200  # 提取文本阈值
    bs0bj = re.sub("[^\u4e00-\u9fa5，。！“”？\r\n]", "",bs0bj)  # 正则表达式删除非中文，非数字和中文符号的内容
    with open('main_data.txt', 'w', encoding='gb18030') as file_keep:
        file_keep.write(bs0bj)
    with open('main_data.txt', 'r') as file_keep:
        while(standard > 0):
            for line in file_keep.readlines():
                if(len(line) > standard):
                    Line = {'content': line}
                    return Line
            file_keep.seek(0, 0)
            standard = standard - 2
    Line = {'content': 'None'}
    return Line


#  识别楼层数
def StandardValue(bs0bj):
    value = re.findall("发表于", bs0bj)
    value1 = re.findall("只看该作者", bs0bj)
    if(value1 != 0 and value1 < value):
        value = value1
    print('只看该作者：',len(value))
    if len(value) == 0:
        value = re.findall("发表于", bs0bj)
    if len(value) == 0:
        value = re.findall("时间：", bs0bj)
    if len(value) == 0:
        value = re.findall("\d{2}:\d{2}", bs0bj)
    if len(value) == 0:
        value = re.findall("回复", bs0bj)
    if len(value) == 0:
        value = re.findall("\d{4}/\d{2}/\d{2}", bs0bj)
    if len(value) == 0:
        value = re.findall("\d{4}-\d{2}-\d{2}", bs0bj)
    if len(value) == 0:
        value = re.findall("\d{2}-\d{2}-\d{4}", bs0bj)
    return len(value)


# 提取用户名
def FindUserName(tree, path):
    name = tree.xpath(path + '//a[@target="_blank"]/text()')
    if len(name) == 0:
        name = {'author': 'None'}
    else:
        name = {'author': name[0]}
    return name


# 识别楼层时间
def FindFloorDate(tree, path):
    data = tree.xpath(path + '//text()')
    data = str(data)
    datedata = re.findall("\d{4}-.*?(?<=\')", data)
    if len(datedata) == 0:
        datedata = re.findall("发表于(.*?)\'", data)
    if len(datedata) == 0:
        datedata = re.findall("\d{4}/\d{2}/\d{2}", data)
    if len(datedata) == 0:
        datedata = re.findall("\d{2}-\d{2}-\d{4}", data)
    if len(datedata) == 0:
        date = {'publish_date': 'None'}
    else:
        date = {'publish_date': datedata[0]}
    return date


# 识别楼层内容
def FindFloorContent(tree, path):
    content = tree.xpath(path + '//tr[@class="t_f"]//text()')
    if len(content) == 0:
        content = tree.xpath(path + '//td[@id]/text()')
    if len(content) == 0:
        content = tree.xpath(path + '//div[@id]/text()')
    if len(content) == 0:
        content = tree.xpath(path + '//p/text()')
    if len(content) != 0:
        content = re.sub("[\r\n\xa0=]","",content[0]) # 对文本进一步清晰
        content = {'content': content}
    else:
        content = {'content': 'None'}

    return content
