import tkinter as tk  # 导入tkinter库
import os  # 导入os库

os.system("ECHO OFF")

win = tk.Tk()  # 创建窗口
win.geometry("300x300")  # 窗口大小
win.resizable(False, False)  # 设置窗口不可变化大小
win.title("进制转换")  # 设置窗口标题
tk.Label(win, text="10以上进制请输入大写字母").pack()  # 创建标签并显示

frame1 = tk.Frame(win)  # 创建容器frame1
tk.Label(frame1, text="原始数字:").pack(side=tk.LEFT)  # 创建标签并显示
in_num = tk.Entry(frame1)  # 创建输入栏 >> line 35 初始值
in_num.pack(side=tk.LEFT)  # 显示输入栏，左对齐
frame1.pack()  # 显示容器1

in_num.focus_set()

frame2 = tk.Frame(win)  # 创建容器frame2
tk.Label(frame2, text="原始进制:").pack(side=tk.LEFT)  # 创建标签并显示
in_jz1 = tk.Entry(frame2)  # 创建输入栏 >> line 35 初始进制
in_jz1.pack(side=tk.LEFT)  # 显示输入栏，左对齐
frame2.pack()  # 显示容器2

frame3 = tk.Frame(win)  # 创建容器frame3
tk.Label(frame3, text="转换进制:").pack(side=tk.LEFT)  # 创建标签并显示
in_jz2 = tk.Entry(frame3)  # 创建输入栏 >> line 35 转换进制
in_jz2.pack(side=tk.LEFT)  # 显示输入栏，左对齐
frame3.pack()  # 显示容器3
abc_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
            'V', 'W', 'X', 'Y', 'Z']  # 创建字母列表


# 创建进制转换主函数
def main():
    try:  # 检测输入值错误异常 >> line 74
        in_num_get = ""
        have_float = 0
        out_float_list = []
        if "." in in_num.get():
            num = in_num.get()[0:in_num.get().index(".")]
            num_float = in_num.get()[in_num.get().index(".") + 1:]
            have_float = 1
        else:
            num = in_num.get()
            num_float = ""
        jz1, jz2 = int(in_jz1.get()), int(in_jz2.get())  # 将初始值，初始进制，转换进制，分别赋值给num,jz1,jz2
        i0, i1, i2, i3, = 0, 0, -1, 0  # 创建变量 >> line 39-64
        out_list = []  # 设置输出列表
        y_n_break = 0  # 创建变量
        if jz1 > 36 or jz1 < 2:  # 判断输入进制是否合规
            out_label.config(text="原始进制请输入2~36即以内进制!", fg="red")  # 改变标签进行警告
            in_jz1.focus_set()
        if jz2 > 36 or jz2 < 2:  # 判断输入进制是否合规
            out_label.config(text="转换进制请输入2~36即以内进制!", fg="red")  # 改变标签进行警告
            in_jz2.focus_set()
        else:
            while len(num) + i2 != -1:  # 判断字符串是否读取完毕
                if num[i2] in abc_list:  # 判断字符是否是字母 >> line 47
                    num_in = 10 + abc_list.index(num[i2])  # 将字母转换为数字并赋值给num_in
                else:
                    num_in = int(num[i2])  # 将字符转为数字赋值给num_in
                if num_in >= jz1:  # 判断数字是否大于进制从而不合规
                    out_label.config(text="请输入正确数字!\n(整数中数字大于进制)", fg="red")
                    in_num.focus_set()
                    y_n_break = 1
                    break
                i1 = num_in * (jz1 ** i0) + i1
                i2 = i2 - 1
                i0 = i0 + 1
            if y_n_break == 1:
                pass
            else:
                while i1 != 0:

                    i3 = i1 % jz2
                    i1 = int(i1 / jz2)
                    if jz2 > 10 and i3 >= 10:
                        out_list.append(abc_list[i3 - 10])
                    else:
                        out_list.append(str(i3))
                    if len(in_num.get()) > 10:
                        in_num_get = in_num.get()[0:10] + "..."
                    else:
                        in_num_get = in_num.get()
                    # 计算小数部分
                    if have_float == 1:
                        f0, f1, f2, f3 = -1, 0, 0, 0
                        while len(num_float) - f2 != 0:  # 判断字符串是否读取完毕
                            if num_float[f2] in abc_list:  # 判断字符是否是字母 >> line 47
                                num_float_in = 10 + abc_list.index(num_float[f2])  # 将字母转换为数字并赋值给num_float_in
                            else:
                                num_float_in = int(num_float[f2])  # 将字符转为数字赋值给num_float_in
                            if num_float_in >= jz1:  # 判断数字是否大于进制从而不合规
                                out_label.config(text="请输入正确数字!\n(小数中数字大于进制)", fg="red")
                                in_num.focus_set()
                                y_n_break = 1
                                break
                            f1 = num_float_in * (jz1 ** f0) + f1
                            f2 = f2 + 1
                            f0 = f0 - 1
                        if y_n_break == 1:
                            pass
                        else:
                            while f1 % 1 != 0.0:

                                f3 = int(f1 * jz2)
                                f1 = (f1 * jz2) % 1
                                if jz2 > 10 and f3 >= 10:
                                    out_float_list.append(abc_list[f3 - 10])
                                else:
                                    out_float_list.append(str(f3))
                    out_label.config(text=f"{in_num_get}的{jz1}进制转换为{jz2}进制为:\n", fg="#000000")
                    if have_float == 1:
                        out_str = "".join(out_list[::-1]) + "." + "".join(out_float_list[:])
                    else:
                        out_str = "".join(out_list[::-1])
                    out_text.delete(0.0, tk.END)
                    out_text.insert(tk.INSERT, out_str)
                    in_num.focus_set()
    except ValueError:
        out_label.config(text="请输入正确数字!\n(输入空或错误字符)", fg="red")
        in_num.focus_set()


def num_bind(event):
    in_jz1.focus_set()


def jz1_bind(event):
    in_jz2.focus_set()


def main_bind(event):
    main()


tk.Button(win, text="开始转换(回车)", command=main).pack()
out_label = tk.Label(win, text="\n")
out_label.pack()

frame4 = tk.Frame(win)  # 创建容器frame4

out_text = tk.Text(frame4, width=25, height=6)
out_text_jdt = tk.Scrollbar(frame4)
out_text_jdt.pack(side=tk.RIGHT, fill=tk.Y)

# 滚动条与text联动
out_text_jdt.config(command=out_text.yview)
# text与滚动条联动
out_text.config(yscrollcommand=out_text_jdt.set)

frame4.pack()  # 显示容器4

in_num.bind("<Return>", num_bind)
in_jz1.bind("<Return>", jz1_bind)
in_jz2.bind("<Return>", main_bind)
out_text.pack()
win.mainloop()
