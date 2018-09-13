'''
	2017年6月25日16:43:39
	一只狗在屏幕上走来走去
'''
import pygame
import sys

size = width, height = 1200, 800
speed = [-2, 1]
bg = (255, 255, 255)  # RGB

# 创建指定大小的窗口 Surface
screen = pygame.display.set_mode(size)

# 设置窗口标题
pygame.display.set_caption("叶坤的第一个pygame")

# 加载图片
dog = pygame.image.load("D:\\Users\\Yeah_Kun\\Desktop\\图片\\dog.png")

# 获得图形位置矩形
position = dog.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

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
