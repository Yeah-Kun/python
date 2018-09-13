class Nint(int):
    
    def __new__(cls,a=0):
        if isinstance(a,str):
            total = 0
            for each in a:
                total += ord(each)
            a = total
        return int.__new__(cls,a)
    
