# -*- coding: <utf-8> -*-
# 编写者: CYH ——2022/9/14
import tkinter as tk
import math

# 全局变量
num_input = [[]]
operator = []
input_view = ''
outcome = ''


# 更新窗口
def view_config():
    # 处理输入字符过长影响显示
    if len(input_view) <= 30:
        num_input_control.config(text=input_view)
        outcome_control.config(text=outcome)
        calculator_win.update()
    else:
        num_input_control.config(text='...' + input_view[len(input_view) - 30:])
        outcome_control.config(text=outcome)
        calculator_win.update()


# 以类的方法输入值
class add_values:
    def __init__(self, value: str):
        self.value = str(value)

    # 输入值
    def add(self):
        # 全局变量
        global input_view, num_input, operator
        # 如果值为数字
        if self.value.isnumeric():
            num_input[-1].append(self.value)

            input_view = input_view + self.value
            view_config()
        # 如果值为小数点
        elif self.value == '.':
            if '.' not in num_input[-1]:
                num_input[-1].append(self.value)

                input_view = input_view + self.value
                view_config()
            else:
                pass
        # 如果值为根号
        elif self.value == '√':
            if '√' not in num_input[-1]:
                num_input[-1].append(self.value)
                input_view = input_view + self.value
                view_config()
        # 如果值为运算符
        elif self.value in ['+', '-', '*', '/']:
            operator.append(self.value)
            num_input.append([])
            input_view = input_view + self.value
            view_config()
        print(f'添加事件: {self.value}')

    # 退格
    @staticmethod
    def pop():
        # 全局变量
        global input_view, num_input
        try:
            if input_view[-1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
                input_view = input_view[0:-1]
                if not num_input[-1]:  # 当列表末尾为空列表时
                    del num_input[-1]  # 删除空列表 (空列表产生的原因是pop把单个num列表删除至清空)
                num_input[-1].pop()
                view_config()
            else:
                operator.pop()
                input_view = input_view[0:-1]
                view_config()
        except IndexError:  # 处理退格过多
            print('退格过多,超出索引')

    # 清除
    @staticmethod
    def clear():
        # 全局变量
        global num_input, input_view, outcome, operator
        num_input = [[]]
        operator = []
        input_view = ''
        outcome = ''
        view_config()
        print('清除事件')


# 开始运算
def operation():
    # 全局变量
    global num_input, outcome, operator
    num_list = []
    val = ''
    for num in num_input:
        if '√' in num:
            sqrt_index = num.index('√')
            sqrt_num = num[:sqrt_index]
            print(sqrt_num)
            if sqrt_num:
                sqrt_num.append('*')
            _ = ''.join(num[sqrt_index + 1:])
            sqrt_num.append('math.sqrt({})'.format(_))
            num = sqrt_num
            print(num)
        num_list.append(''.join(num))
        # math.sqrt()
    val = ''
    num_index = 0
    operator_index = 0
    num_list_len = len(num_list) - 1
    ope_list_len = len(operator) - 1
    while num_index <= num_list_len:
        num = num_list[num_index]
        if operator_index <= ope_list_len:
            ope = operator[operator_index]
        else:
            ope = ''
        val = val + num + ope
        num_index += 1
        operator_index += 1
    print(f'数字列表: {num_list}')
    print(f'运算符列表: {operator}')
    print(f'转换字符串: {val}')
    try:
        outcome = eval(val)
        print(f'输出结果: {outcome}')
    except SyntaxError:
        outcome = 'SyntaxError'
        print(f'SyntaxError:{val}')
    finally:
        view_config()


# 处理事件绑定
def bind(event):
    if event.char == '\r':  # 回车
        operation()
    elif event.char == '\b':  # 退格
        add_values('').pop()
    elif event.char in ['C', 'c']:  # 清除
        add_values('').clear()
    elif event.char in ['s', 'S']:  # 根号
        add_values('√').add()
    else:
        add_values(event.char).add()  # 其他字符
    print(f'键盘事件: {[event.char]}')


# 控件创建
calculator_win = tk.Tk()
calculator_win.title('简易计算器')
calculator_win.resizable(False, False)
num_input_control = tk.Label(calculator_win, text=input_view)
outcome_control = tk.Label(calculator_win, text=outcome)
num_0_control = tk.Button(calculator_win, text='0', command=add_values('0').add)
num_1_control = tk.Button(calculator_win, text='1', command=add_values('1').add)
num_2_control = tk.Button(calculator_win, text='2', command=add_values('2').add)
num_3_control = tk.Button(calculator_win, text='3', command=add_values('3').add)
num_4_control = tk.Button(calculator_win, text='4', command=add_values('4').add)
num_5_control = tk.Button(calculator_win, text='5', command=add_values('5').add)
num_6_control = tk.Button(calculator_win, text='6', command=add_values('6').add)
num_7_control = tk.Button(calculator_win, text='7', command=add_values('7').add)
num_8_control = tk.Button(calculator_win, text='8', command=add_values('8').add)
num_9_control = tk.Button(calculator_win, text='9', command=add_values('9').add)
# Addition, subtraction, multiplication and division 加减乘除
dot_control = tk.Button(calculator_win, text='.', command=add_values('.').add)
add_control = tk.Button(calculator_win, text='+', command=add_values('+').add)
sub_control = tk.Button(calculator_win, text='-', command=add_values('-').add)
mul_control = tk.Button(calculator_win, text='*', command=add_values('*').add)
div_control = tk.Button(calculator_win, text='/', command=add_values('/').add)
sqrt_control = tk.Button(calculator_win, text='√', command=add_values('√').add)
back_control = tk.Button(calculator_win, text='←', command=add_values('').pop)
clear_control = tk.Button(calculator_win, text='C', command=add_values('').clear)
eq_control = tk.Button(calculator_win, text='=', command=operation)
# 控件布局设置 row:行 column:列
# 输入输出显示控件
num_input_control.grid(row=0, column=0, rowspan=1, columnspan=5, padx=10, sticky=tk.E)
outcome_control.grid(row=1, column=0, rowspan=1, columnspan=5, padx=10, sticky=tk.E)
# 按钮 第1行控件
num_7_control.grid(row=2, column=0, rowspan=1, columnspan=1, ipadx=20, ipady=5)  # 第1列 7
num_8_control.grid(row=2, column=1, rowspan=1, columnspan=1, ipadx=20, ipady=5)  # 第2列 8
num_9_control.grid(row=2, column=2, rowspan=1, columnspan=1, ipadx=20, ipady=5)  # 第3列 9
add_control.grid(row=2, column=3, rowspan=1, columnspan=1, ipadx=20, ipady=5)  # 第4列 +
back_control.grid(row=2, column=4, rowspan=1, columnspan=1, ipadx=20, ipady=5)  # 第5列 ←
# 按钮 第2行控件
num_4_control.grid(row=3, column=0, rowspan=1, columnspan=1, ipadx=20, ipady=5)  # 第1列 4
num_5_control.grid(row=3, column=1, rowspan=1, columnspan=1, ipadx=20, ipady=5)  # 第2列 5
num_6_control.grid(row=3, column=2, rowspan=1, columnspan=1, ipadx=20, ipady=5)  # 第3列 6
sub_control.grid(row=3, column=3, rowspan=1, columnspan=1, ipadx=22, ipady=5)  # 第4列 -
clear_control.grid(row=3, column=4, rowspan=1, columnspan=1, ipadx=22, ipady=5)  # 第5列 C
# 按钮 第3行控件
num_1_control.grid(row=4, column=0, rowspan=1, columnspan=1, ipadx=20, ipady=5)  # 第1列 1
num_2_control.grid(row=4, column=1, rowspan=1, columnspan=1, ipadx=20, ipady=5)  # 第2列 2
num_3_control.grid(row=4, column=2, rowspan=1, columnspan=1, ipadx=20, ipady=5)  # 第3列 3
mul_control.grid(row=4, column=3, rowspan=1, columnspan=1, ipadx=22, ipady=5)  # 第4列 *
eq_control.grid(row=4, column=4, rowspan=2, columnspan=1, ipadx=22, ipady=25)  # 第5列 =
# 按钮 第4行控件
num_0_control.grid(row=5, column=0, rowspan=1, columnspan=1, ipadx=20, ipady=5)  # 第1列 0
dot_control.grid(row=5, column=1, rowspan=1, columnspan=1, ipadx=22, ipady=5)  # 第2列 .
sqrt_control.grid(row=5, column=2, rowspan=1, columnspan=1, ipadx=20, ipady=5)  # 第3列 √
div_control.grid(row=5, column=3, rowspan=1, columnspan=1, ipadx=22, ipady=5)  # 第4列 /

# bind 事件绑定
calculator_win.bind("<Key>", bind)
# 事件主循环
calculator_win.mainloop()
