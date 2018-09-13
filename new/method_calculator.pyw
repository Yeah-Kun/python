from tkinter import Tk
from tkinter import Frame
from tkinter import Text
from tkinter import Button
from tkinter import INSERT
from tkinter import END
from tkinter import CURRENT
from tkinter import messagebox
from re import findall
from math import factorial
from math import radians
from math import sin
from math import cos
from math import tan
from math import sqrt
from math import log
from math import log10
from math import e



class Calculator():
    def __init__(self):
        self.create_ui()
    def create_ui(self):
        self.root=Tk()
        self.root.title('My Calculator')
        self.root_1=Frame(self.root,height=28,width=40)
        self.root_1.pack(expand='yes')
        self.area_display=Text(self.root_1,height=6,width=40)
        self.area_display.grid(row=0,column=0,columnspan=5)
        self.fac_but=Button(self.root_1,text='!',height=3,width=8,command= lambda:self.display(self.fac_but.cget('text')))                               #阶乘按钮
        self.fac_but.grid(row=1,column=0)
        self.invol_but=Button(self.root_1,text='^',height=3,width=8,command= lambda:self.display(self.invol_but.cget('text')))                             #乘方按钮
        self.invol_but.grid(row=1,column=1)
        self.sqrt_but=Button(self.root_1,text='√(',height=3,width=8,command= lambda:self.display(self.sqrt_but.cget('text')))
        self.sqrt_but.grid(row=1,column=2)
        self.pi_but=Button(self.root_1,text='π',height=3,width=8,command= lambda:self.display(self.pi_but.cget('text')))
        self.pi_but.grid(row=1,column=3)
        self.clear_all_but=Button(self.root_1,text='C',height=3,width=8,command=self.cle_all)
        self.clear_all_but.grid(row=1,column=4)
        self.sin_but=Button(self.root_1,text='sin(',height=3,width=8,command= lambda:self.display(self.sin_but.cget('text')))
        self.sin_but.grid(row=2,column=0)
        self.left_but=Button(self.root_1,text='(',height=3,width=8,command= lambda:self.display(self.left_but.cget('text')))                              #左括号
        self.left_but.grid(row=2,column=1)
        self.right_but=Button(self.root_1,text=')',height=3,width=8,command= lambda:self.display(self.right_but.cget('text')))
        self.right_but.grid(row=2,column=2)
        self.e_but=Button(self.root_1,text='e',height=3,width=8,command= lambda:self.display(self.e_but.cget('text')))
        self.e_but.grid(row=2,column=3)
        self.clear_but=Button(self.root_1,text='□x',height=3,width=8,command=self.cle)
        self.clear_but.grid(row=2,column=4)
        self.cos_but=Button(self.root_1,text='cos(',height=3,width=8,command= lambda:self.display(self.cos_but.cget('text')))
        self.cos_but.grid(row=3,column=0)
        self.seven_but=Button(self.root_1,text='7',height=3,width=8,command= lambda:self.display(self.seven_but.cget('text')))
        self.seven_but.grid(row=3,column=1)
        self.eight_but=Button(self.root_1,text='8',height=3,width=8,command= lambda:self.display(self.eight_but.cget('text')))
        self.eight_but.grid(row=3,column=2)
        self.nine_but=Button(self.root_1,text='9',height=3,width=8,command= lambda:self.display(self.nine_but.cget('text')))
        self.nine_but.grid(row=3,column=3)
        self.s_div_but=Button(self.root_1,text='/',height=3,width=8,command= lambda:self.display(self.s_div_but.cget('text')))                             #除号
        self.s_div_but.grid(row=3,column=4)
        self.tan_but=Button(self.root_1,text='tan(',height=3,width=8,command= lambda:self.display(self.tan_but.cget('text')))
        self.tan_but.grid(row=4,column=0)
        self.four_but=Button(self.root_1,text='4',height=3,width=8,command= lambda:self.display(self.four_but.cget('text')))
        self.four_but.grid(row=4,column=1)
        self.five_but=Button(self.root_1,text='5',height=3,width=8,command= lambda:self.display(self.five_but.cget('text')))
        self.five_but.grid(row=4,column=2)
        self.six_but=Button(self.root_1,text='6',height=3,width=8,command= lambda:self.display(self.six_but.cget('text')))
        self.six_but.grid(row=4,column=3)
        self.s_mul_but=Button(self.root_1,text='*',height=3,width=8,command= lambda:self.display(self.s_mul_but.cget('text')))
        self.s_mul_but.grid(row=4,column=4)
        self.ln_but=Button(self.root_1,text='ln(',height=3,width=8,command= lambda:self.display(self.ln_but.cget('text')))
        self.ln_but.grid(row=5,column=0)
        self.one_but=Button(self.root_1,text='1',height=3,width=8,command= lambda:self.display(self.one_but.cget('text')))
        self.one_but.grid(row=5,column=1)
        self.two_but=Button(self.root_1,text='2',height=3,width=8,command= lambda:self.display(self.two_but.cget('text')))
        self.two_but.grid(row=5,column=2)
        self.three_but=Button(self.root_1,text='3',height=3,width=8,command= lambda:self.display(self.three_but.cget('text')))
        self.three_but.grid(row=5,column=3)
        self.s_sub_but=Button(self.root_1,text='-',height=3,width=8,command= lambda:self.display(self.s_sub_but.cget('text')))                               #减号
        self.s_sub_but.grid(row=5,column=4)
        self.lg_but=Button(self.root_1,text='lg(',height=3,width=8,command= lambda:self.display(self.lg_but.cget('text')))
        self.lg_but.grid(row=6,column=0)
        self.zero_but=Button(self.root_1,text='0',height=3,width=8,command= lambda:self.display(self.zero_but.cget('text')))
        self.zero_but.grid(row=6,column=1)
        self.pot_but=Button(self.root_1,text='.',height=3,width=8,command= lambda:self.display(self.pot_but.cget('text')))
        self.pot_but.grid(row=6,column=2)
        self.s_equal_but=Button(self.root_1,text='=',height=3,width=8,command=self.calculate)
        self.s_equal_but.grid(row=6,column=3)
        self.s_plux_but=Button(self.root_1,text='+',height=3,width=8,command= lambda:self.display(self.s_plux_but.cget('text')))
        self.s_plux_but.grid(row=6,column=4)
        self.root_1.mainloop()
    def display(self,char):
        self.area_display.insert(index=END,chars=char)  # INSERT 的值是 'insert','END'的值是'end'
        self.area_display.focus_force()       # 令该控件，获得焦点（无论如何均获得）
    def cle_all(self):
        self.area_display.delete(index1=1.0,index2=END)          #index 取值的格式应为 x.y，x是第几行，y是第几列,x从1取起，y从0取起
    def cle(self):
        input_string=self.area_display.get(index1=1.0,index2=END)       #input_string最后一个字符是回车字符
        input_string=input_string.rstrip('\n')
        input_string=input_string[:-1]
        self.cle_all()
        self.display(input_string)
        #self.area_display.delete(index1=END,index2=None)
        #self.area_display.replace(index1=END,index2=END,'',)
    def check(self,input_string):
        # 写出匹配模式
        pat_int='-{0,1}[\d]+!{0,1}'                                         # 1
        pat_real='-{0,1}[\d]+'+'\.[\d]+|π|e'                               # 2
        ope_two='[+-/*^]'                                                   # 3
        int_real=pat_int+'|'+pat_real                                       # 4
        complete_digi=int_real+'|'+'\('+'(?:'+int_real+')'+'\)'             # 5
        func_1='(?:sin|cos|tan|lg|ln|√)'                                    # 6
        single='(?:'+complete_digi+'|'+func_1+'\('+'(?:'+complete_digi+')'+'(?:'+ope_two+'(?:'+complete_digi+')'+')*'+'\)'+')'     # 7
        No_sur_func='(?:'+single+')'+'(?:'+ope_two+'(?:'+single+')'+')*'    # 8
        Sur_par_no_func='\('+No_sur_func+'\)'                               # 9
        Comp_no_func_1='(?:'+No_sur_func+'|'+Sur_par_no_func+')'+'(?:'+ope_two+'(?:'+No_sur_func+'|'+Sur_par_no_func+')'+')*'  # 10
        Comp_no_func=Comp_no_func_1+'|'+'\('+Comp_no_func_1+'\)'            # 11
        Sur_func='(?:'+func_1+'\('+')+'+No_sur_func+'\)'+'(?:(?:'+ope_two+'(?:'+single+')'+')*\))*'                       # 12      #被函数包围，
        Complete_no_par='(?:'+Sur_func+'|'+Comp_no_func+')'+'!{0,1}'+'(?:'+ope_two+'(?:'+Sur_func+'|'+Comp_no_func+')'+'!{0,1}'+')*'  # 13
        Complete_sur_par='\('+Complete_no_par+'\)'+'!{0,1}'                                                                  # 14
        Complete='(?:'+Complete_no_par+'|'+Complete_sur_par+')'+'(?:'+ope_two+'(?:'+Complete_no_par+'|'+Complete_sur_par+')'+')*'  # 15
        result=findall(Complete,input_string)
        if result!=[]:
            if len(result[0])==len(input_string):
                if  input_string.count('(')==input_string.count(')'):
                    return True
                else:
                    messagebox.showwarning(title='检查情况',message='左右括号不等')
                    return False
            else:
                return False
        else:
            messagebox.showwarning(title='检查情况',message='表达式不能为空')
            return False
    def calculate(self):
        input_string=self.area_display.get(index1=1.0,index2=END)
        input_string=input_string.rstrip('\n')                             # 对输入串进行脱回车符处理
        if self.check(input_string):
            self.value=[None for i in range(50)]
            self.sign=[None for i in range(50)]
            self.amount_value=0
            self.amount_sign=0
            index_input=0
            length_input=len(input_string)
            while (index_input<length_input):
                if input_string[index_input]=='+':
                    while (self.amount_sign!=0):               # 符号栈不为空，
                        if self.sign[self.amount_sign-1]!='(':
                            result=self.ari_func_operator(self.sign[self.amount_sign-1])           # 符号栈栈顶元素
                            if result=='error':
                                return 
                            self.amount_sign-=1                # 栈顶符号弹栈
                            self.value[self.amount_value]=result    # 运算结果入栈
                            self.amount_value+=1
                        else:
                            break
                    self.sign[self.amount_sign]='+'                 # 运算符入符号栈
                    self.amount_sign+=1                        # 符号数量+1
                    index_input+=1


                elif input_string[index_input]=='-':
                    if (index_input==0) or input_string[index_input-1]=='(':       # '-'代表负号
                        self.sign[self.amount_sign]='M'
                        self.amount_sign+=1
                        index_input+=1
                    elif input_string[index_input-1]==')' or input_string[index_input-1]=='!' or input_string[index_input-1]>='0' and input_string[index_input-1]<='9' or input_string[index_input-1]=='e' or input_string[index_input-1]=='π':  # '-'代表减号
                        while (self.amount_sign!=0):               # 符号栈不为空，
                            if self.sign[self.amount_sign-1]!='(':
                                result=self.ari_func_operator(self.sign[self.amount_sign-1])           # 符号栈栈顶元素
                                if result=='error':
                                    return
                                self.amount_sign-=1                # 栈顶符号弹栈
                                self.value[self.amount_value]=result    # 运算结果入栈
                                self.amount_value+=1
                            else:
                                break
                        self.sign[self.amount_sign]='m'                 # 运算符入符号栈,为区分减号还是负号,'m'表示减号,'M'表示负号
                        self.amount_sign+=1                        # 符号数量+1
                        index_input+=1
                    else:
                        messagebox.showwarning(title='检查情况1',message='表达式有误，请检查')
                        return 

                elif input_string[index_input]=='*' or input_string[index_input]=='/':
                    while (self.amount_sign!=0):                # 符号栈不为空
                        if self.sign[self.amount_sign-1]!='(' and self.sign[self.amount_sign-1]!='+' and self.sign[self.amount_sign-1]!='m':   # 优先级与'*'  '/'相等或高于'*'  '/' 
                            result=self.ari_func_operator(self.sign[self.amount_sign-1])           # 符号栈栈顶元素
                            if result=='error':
                                return
                            self.amount_sign-=1                # 栈顶符号弹栈
                            self.value[self.amount_value]=result    # 运算结果入栈
                            self.amount_value+=1
                        else:
                            break
                    self.sign[self.amount_sign]=input_string[index_input]                 # 运算符入符号栈
                    self.amount_sign+=1                        # 符号数量+1
                    index_input+=1


                elif input_string[index_input]=='^' or input_string[index_input]=='!':
                    while (self.amount_sign!=0):
                        if self.sign[self.amount_sign-1] not in ['(','+','m','M','*','/']:     # 栈顶元素优先级大于或等于'^','!'
                            result=self.ari_func_operator(self.sign[self.amount_sign-1])           # 符号栈栈顶元素
                            if result=='error':
                                return
                            self.amount_sign-=1                # 栈顶符号弹栈
                            self.value[self.amount_value]=result    # 运算结果入栈
                            self.amount_value+=1
                        else:
                            break
                    self.sign[self.amount_sign]=input_string[index_input]                 # 运算符入符号栈
                    self.amount_sign+=1                        # 符号数量+1
                    index_input+=1

                elif input_string[index_input] in['s','c','t']:
                    self.sign[self.amount_sign]=input_string[index_input]
                    self.amount_sign+=1
                    index_input+=3
                elif input_string[index_input]=='l':
                    self.sign[self.amount_sign]=input_string[index_input+1]
                    self.amount_sign+=1
                    index_input+=2
                elif input_string[index_input]=='√':
                    self.sign[self.amount_sign]='√'
                    self.amount_sign+=1
                    index_input+=1


                elif input_string[index_input]=='(':
                    self.sign[self.amount_sign]='('
                    self.amount_sign+=1
                    index_input+=1
                elif input_string[index_input]==')':
                    while self.sign[self.amount_sign-1]!='(':
                        result=self.ari_func_operator(self.sign[self.amount_sign-1])           # 符号栈栈顶元素
                        if result=='error':
                            return
                        self.amount_sign-=1                # 栈顶符号弹栈
                        self.value[self.amount_value]=result    # 运算结果入栈
                        self.amount_value+=1
                    self.amount_sign-=1
                    index_input+=1

                elif (input_string[index_input]<='9') & (input_string[index_input]>='0'):
                    result,index_input=self.find_entire_value(input_string,index_input)
                    self.value[self.amount_value]=result
                    self.amount_value+=1
                elif input_string[index_input]=='π':
                    self.value[self.amount_value]=180
                    self.amount_value+=1
                    index_input+=1
                elif input_string[index_input]=='e':
                    self.value[self.amount_value]=e
                    self.amount_value+=1
                    index_input+=1

            # 符号栈元素全部弹栈
            while(self.amount_sign>0):
                result=self.ari_func_operator(self.sign[self.amount_sign-1])
                if result=='error':
                    messagebox.showwarning(title='检查情况2:error',message='表达式有误，请检查')
                    return
                self.amount_sign-=1
                self.value[self.amount_value]=result    # 运算结果入栈
                self.amount_value+=1
            self.area_display.insert(index=END,chars='\n')
            self.area_display.insert(index=END,chars='\n')
            self.area_display.insert(index=3.0,chars='The result is:'+str(self.value[0]))  

        else:
            messagebox.showwarning(title='检查情况3:error',message='表达式有误，请检查')
    def ari_func_operator(self,ope):
        if ope=='+':
            second=self.value[self.amount_value-1]       # 数值栈顶元素弹栈
            self.amount_value-=1
            first=self.value[self.amount_value-1]
            self.amount_value-=1
            result=first+second
        elif ope=='m':
            second=self.value[self.amount_value-1]       # 数值栈顶元素弹栈
            self.amount_value-=1
            first=self.value[self.amount_value-1]
            self.amount_value-=1
            result=first-second


        elif ope=='*':
            second=self.value[self.amount_value-1]       # 数值栈顶元素弹栈
            self.amount_value-=1
            first=self.value[self.amount_value-1]
            self.amount_value-=1
            result=first*second
        elif ope=='/':
            second=self.value[self.amount_value-1]       # 数值栈顶元素弹栈
            self.amount_value-=1
            first=self.value[self.amount_value-1]
            self.amount_value-=1
            result=first/second


        elif ope=='M':                                    # 负号
            only_one=self.value[self.amount_value-1]
            self.amount_value-=1
            result=-only_one

        elif ope=='!':
            only_one=self.value[self.amount_value-1]
            self.amount_value-=1
            try:
                result=factorial(only_one)
            except ValueError:
                messagebox.showwarning(title='检查情况:error',message='!的对象应为非负整数')
                result='error'
        elif ope=='^':
            second=self.value[self.amount_value-1]       # 数值栈顶元素弹栈
            self.amount_value-=1
            first=self.value[self.amount_value-1]
            self.amount_value-=1
            result=pow(first,second)
            if type(result)==type(1+1j):                  # 为复数
                messagebox.showwarning(title='检查情况:erroe',message='乘方运算的结果为复数')
                result='error'


        elif ope=='s':
            only_one=self.value[self.amount_value-1]
            self.amount_value-=1
            result=sin(radians(only_one))
        elif ope=='c':
            only_one=self.value[self.amount_value-1]
            self.amount_value-=1
            result=cos(radians(only_one))
        elif ope=='t':
            only_one=self.value[self.amount_value-1]
            self.amount_value-=1
            result=tan(radians(only_one))
        elif ope=='√':
            only_one=self.value[self.amount_value-1]
            self.amount_value-=1
            result=sqrt(only_one)
        elif ope=='g':
            only_one=self.value[self.amount_value-1]
            self.amount_value-=1
            result=log10(only_one)
        elif ope=='n':
            only_one=self.value[self.amount_value-1]
            self.amount_value-=1
            result=log(only_one)

        return result
    def find_entire_value(self,input_string,index_input):
        first=index_input
        last=index_input+1
        length_input=len(input_string)
        while (last<length_input) and ((input_string[last]<='9') & (input_string[last]>='0') | (input_string[last]=='.')):
            last+=1
        result=float(input_string[first:last])
        return result,last

if __name__=='__main__':
    one=Calculator()

