from urllib import request

repond = request.urlopen("https://www.baidu.com/")

print(repond.read().decode("utf-8"))