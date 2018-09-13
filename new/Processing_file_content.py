'''处理文件内容，将文件里面的逗号都换成空格
	create by Ian in 2017-10-13 11:24:49
'''

import re

path = "D:\\code\\otherLanguage\\C\\Compilation Principles\\Experiment Content\\keyword.txt"
with open(path) as file: # 读文件
    buff = file.read()

buff = re.sub(',', ' ', buff) # 逗号换成空格

with open(path, 'w') as file: # 重新写入文件
    file.write(buff)
