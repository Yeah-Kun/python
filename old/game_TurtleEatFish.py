import random

class Turtle:

    enargy = 100
    x = 0
    y = 0
    def __init__(self,num):
        self.num = int(num)
        
    def movestep(self):
        self.movestep = randint(1,2)#随机生成步数

    def movedir(self):
        self.x = randint(-self.movestep,self.movestep)#随机生成x轴的步数
        if(self.x == 0):
            while(self.y != self.movestep or self.y != -self.movestep):
                self.y = randint(-self.movestep,self.movestep)
        elif(self.x != self.movestep or self.x != self.movestep):
            while(self.y == 0):
                self.y = randint(-1,1)
        return (self.x,self.y)

class Fish:

    movestep = 1
    
    def __init__(self,num):
        self.num = int(num)

    def movedir(self):
        self.x = randint(-self.movestep,self.movestep)
        if(self.x == 0):
            while(self.y == 0):
                self.y = randint(-self.movestep,self.movestep)
        return (self.x,self.y)

    

    
    
        
    
