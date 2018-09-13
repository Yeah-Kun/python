class Rectangular:
    long = 0
    wide = 0
    def setRect(self):
        self.long = float(input("长："))
        self.wide = float(input("宽："))
    def getRect(self):
        print("这个矩形的长是：%.1f，宽是：%.1f"%(self.long,self.wide))
    def getArea(self):
        area = float(self.long * self.wide)
        return area
