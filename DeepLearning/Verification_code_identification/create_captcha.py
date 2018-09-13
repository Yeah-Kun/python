'''
	学校验证码自动生成工具
	create by Ian in 2018-3-5 10:31:47
'''
import random
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os


class MyGaussianBlur(ImageFilter.Filter):
    name = "GaussianBlur"

    def __init__(self, radius=2, bounds=None):
        self.radius = radius
        self.bounds = bounds

    def filter(self, image):
        if self.bounds:
            clips = image.crop(self.bounds).gaussian_blur(self.radius)
            image.paste(clips, self.bounds)
            return image
        else:
            return image.gaussian_blur(self.radius)


class Captcha(object):
    """docstring for Captcha

    size：验证码尺寸，二元组
    number：验证码字符数，数字
    """

    def __init__(self, size=(140, 60), number=4):
        self._size = size  # 验证码尺寸
        self._width, self._height = size
        self._number = number  # 验证码字符数
        self.img = Image.new('RGB', self._size, (255,)*3)
        self.font = ImageFont.truetype('C:\Windows\Fonts\Arial.ttf', 45)
        self.draw = ImageDraw.Draw(self.img)

    def gen_text(self):
        """生成验证码文本内容"""
        text = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z']

        return ''.join(random.sample(text, self._number))

    def gen_line(self):
        """绘制干扰元素"""
        head = (15, random.randint(0, self._height))
        end = (self._width - 10, random.randint(0, self._height))
        head2 = (15, random.randint(0, self._height))
        end2 = (40, random.randint(0, self._height))
        self.draw.line([head, end], fill="black", width=3)
        self.draw.line([head2, end2], fill="black", width=3)

    def gen_code(self):
        """生成验证码"""
        self.text = self.gen_text()
        font_width, font_height = self.font.getsize(self.text)
        self.draw.text((10 + (self._width - font_width) / self._number, (self._height -
                                                                          font_height) / self._number), self.text, font=self.font, fill="black")
        self.gen_line()  # 绘制干扰线
        #self.img = self.img.transform((self._width + 30, self._height + 10), Image.AFFINE, (1,-0.3,0,-0.1,1,0),Image.BILINEAR)
        self.img = self.img.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 滤镜，边界加强
        #self.img = self.img.crop((30,10,170,70))
        self.img = self.img.filter(
            (MyGaussianBlur(radius=1, bounds=(30, 10, 100, 50))))

    def save_code(self, path=""):
        self.img.save(path + "/" + self.text + ".jpg")


if __name__ == '__main__':
    path = "test_unit2"
    if not os.path.exists(path):
        os.makedirs(path)
    for i in range(1):
    	c = Captcha()
    	c.gen_code()
    	c.save_code(path)
