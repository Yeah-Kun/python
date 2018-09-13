'''
	create by Ian in 2017-9-5 16:31:50
	帮助老师分配每个班新生班导师带的新生信息
'''
import xlrd


class OptionExcel(object):
    """操作excel表"""

    def __init__(self, path):
        self.path = path

    def teacher_list(self):
        data = xlrd.open_workbook(self.path)
        print(data)


def main():
    path = "E:/AllData/学长事务/新生导师.xls"
    the_teacher = OptionExcel(path)
    the_teacher.teacher_list()


if __name__ == '__main__':
    main()
