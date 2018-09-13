"""
	create by Ian in 2017-8-23 13:05:40
	生成验证码图片，用于Django的验证码模块

"""
import random,string
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import os


def getRandomChar():
	'''生成随机字符串'''
	ran = string.ascii_lowercase+string.digits
	char = ""
	for i in range(4):
		char += random.choice(ran)

	return char


def getRandomColor():
	"""生成随机RGB颜色"""
	return (random.randint(50,150),random.randint(50,150),random.randint(50,150))


def create_code(size):
	img = Image.new('RGB',size,(255,255,255)) # 创建图片，模式，大小，颜色
	draw = ImageDraw.Draw(img) # 创建画笔
	font = ImageFont.truetype(os.path.join('timesbi.ttf'),25) # 设置字体，大小

	code = getRandomChar()

	for t in range(4):
		"""将生成的字符放到画布中"""
		draw.text((20*t+5,0),code[t],getRandomColor(),font)

	for i in range(random.randint(0,50)):
		"""生成干扰点"""
		draw.point((random.randint(0, 80), random.randint(0, 30)),fill=getRandomColor())
		
	#img.save(code+".png", "png") # 保存图片
	return img,code

if __name__ == '__main__':
	size = (83,30)
	create_code(size)