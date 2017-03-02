class Turtle:
    def __init__(self,x):
        self.num = x

class Fish:
    def __init__(self,x):
        self.num = x

class Pool:
    def __init__(self,x,y):
        self.turtle = Turtle(x)
        self.Fish = Fish(y)

    def print_num(self):
        print("水池里面总共有乌龟%d只，小鱼%d条！"%(self.turtle.num,self.Fish.num))
