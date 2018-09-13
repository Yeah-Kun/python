'''
	2017年6月25日16:45:38
    一只狗在屏幕上走来走去增强版
    可以通过键盘控制它的方向
'''
import pygame
import sys
from pygame.locals import *

size = width, height = 1200, 800
speed = [-1, 1]
bg = (255, 255, 255)  # RGB

# 创建指定大小的窗口 Surface
screen = pygame.display.set_mode(size)

# 设置窗口标题
pygame.display.set_caption("叶坤的第一个pygame")

# 加载图片
dog = pygame.image.load("D:\\Users\\Yeah_Kun\\Desktop\\图片\\dog.png")

# 获得图形位置矩形
position = dog.get_rect()

# 控制头的转向
l_head = dog
r_head = pygame.transform.flip(dog, True, False)

while True:
    for event in pygame.event.get():
        print(str(event)+'\n')
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_LEFT: # 向左走
                dog = l_head
                speed = [-1, 0]
            if event.key == K_RIGHT:
                dog = r_head
                speed = [1, 0]
            if event.key == K_UP:
                speed = [0, -1]
            if event.key == K_DOWN:
                speed = [0, 1]

    # 移动图像
    position = position.move(speed)

    if position.left < 0 or position.right > width:
        # 翻转图片
        dog = pygame.transform.flip(dog, True, False)
        # 反方向移动
        speed[0] = -speed[0]

    if position.top < 0 or position.bottom > height:
        speed[1] = -speed[1]

    # 填充背景
    screen.fill(bg)
    # 更新图像
    screen.blit(dog, position)
    # 更新界面
    pygame.display.flip()
    # 延迟10毫秒
    pygame.time.delay(10)
