import re  # 正则表达式模块，用于删除标点符号


# 数据清洗函数
def CleanInput(input_str):
    input_str = re.sub("[：“”；（）、，。！~《》\s'.]", "", input_str)   # 正则表达式re的sub函数
    return input_str

# 文本数据清洗
file_material = open("D:\\Users\\YeahKun\\Desktop\\play\\分词材料.txt",
                     "rb").read().decode("utf8", "ignore")
file_material = CleanInput(file_material)
with open("D:\\Users\\YeahKun\\Desktop\\play\\new_分词材料.txt", "a") as file_save:  # 将分好的词放到文件里面
    file_save.write(file_material)
