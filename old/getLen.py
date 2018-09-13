import math

class Point:
    
    def __init__(self,x,y):
        self.x = float(x)
        self.y = float(y)

    def getx(self):
        return self.x

    def gety(self):
        return self.y

class Line(Point):
    
    def __init__(self,point1,point2):
        self.x = point1.getx() - point2.getx()
        self.y = point1.gety() - point2.gety()
        
    def getLen(self):
        self.len = math.sqrt(self.x**2 + self.y**2)
        return self.len
        
