import os

class FileObject:
    
    def openfile(self,*path):
        self.file = open(*path)

    def write(self,*path):
        self.file.write(*path)
    
    def __del__(self):
        self.file.close()
        print("文件已被关闭...")

    

