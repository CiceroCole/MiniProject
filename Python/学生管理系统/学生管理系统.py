# -*- coding: <utf-8> -*-
# 编写者: CYH ——2022/9/8
import sys
import json
import datetime
import pandas as pd
import os.path
from data.Tools import *
from tkinter.filedialog import asksaveasfilename as tk_f_save
import logging

week_list = ['一', '二', '三', '四', '五', '六', '天']
print(f'Py解释器路径: {sys.executable} 文件编码: {sys.getfilesystemencoding()}')
print(f'今天是 {datetime.datetime.now().date().isoformat()} \
星期{week_list[datetime.datetime.now().isoweekday() - 1]}')
# logging.basicConfig(level=logging.INFO, format='log: %(message)s')
log = logging.getLogger()


class Student:
    def __init__(self, name, sex, birth_date, student_id):
        self.name = name
        self.sex = sex
        self.birth_date = birth_date
        self.student_id = student_id

    def student_dict(self):
        return {
            self.student_id:
                {
                    "名字": self.name,
                    "性别": self.sex,
                    "出生日期": self.birth_date,
                    "学号": self.student_id
                }
        }


# Confirm
class SMS:
    def __init__(self):
        self.menu_list = ['1.添加学生信息', '2.删除学生信息', '3.显示所有学生', '4.查找学生信息', '5.导出存为表格',
                          '6.退出管理系统']
        self.data_file_path = './data/students.json'
        self.type_list = ["名字", "性别", "出生日期", "学号"]

    def main(self):
        choose = self.menu()
        if choose == 1:
            self.add_students()
        elif choose == 2:
            self.del_student()
        elif choose == 3:
            self.show_students()
        elif choose == 4:
            self.find_student_in()
        elif choose == 5:
            self.export_excel()
        elif choose == 6:
            if yes_no(f'<{get_f_now_easy()}:!?>: 是否退出学生管理系统: '):
                exit(0)
        self.main()

    def menu(self):
        print('<' * 20, '欢迎来到学生管理系统', '>' * 20)
        for menu_index in range(0, len(self.menu_list), 2):
            print('{0:^25}{1:^25}'.format(self.menu_list[menu_index], self.menu_list[menu_index + 1]))
        choose_menu = {
            1: ['1', '添加学生信息', '1.添加学生信息', '添加'],
            2: ['2', '删除学生信息', '2.删除学生信息', '删除'],
            3: ['3', '显示所有学生', '3.显示所有学生', '显示'],
            4: ['4', '查找学生信息', '4.查找学生信息', '查找'],
            5: ['5', '导出存为表格', '5.导出存为表格', '导出'],
            6: ['6', '退出管理系统', '6.退出管理系统', '退出'],
        }
        print('—' * 56)
        command = input(f'<{get_f_now_easy()}:in>:\n 请输入要执行的操作: ').strip()
        while True:
            if is_num(command).is_num:
                return int(command)
            elif command in get_dict_values(choose_menu, 2):
                for index, com in choose_menu.items():
                    if command in com:
                        return index
            else:
                command = input(f'<{get_f_now_easy()}:in>:\n 请输入要执行的操作: ').strip()

    def read_data(self):
        if os.path.exists(self.data_file_path):
            with open(self.data_file_path, 'r', encoding='utf-8') as f:
                students = json.load(f)
                return students
        else:
            self.add_data({})
            self.read_data()

    def write_data(self, data):
        with open(self.data_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)

    def add_data(self, data):
        if os.path.exists(self.data_file_path):
            with open(self.data_file_path, 'r', encoding='utf-8') as f:
                students = json.load(f)
            with open(self.data_file_path, 'w', encoding='utf-8') as f:
                for key, val in data.items():
                    students[key] = val
                json.dump(students, f)
        else:
            students = {}
            with open(self.data_file_path, 'w') as f:
                for key, val in data.items():
                    students[key] = val
                json.dump(students, f)

    # 添加学生信息函数(验证学生信息部分)
    @staticmethod
    # 制定返回对象
    def is_student(name: str, name_len: int, sex: str, birth_date: str, student_id: str, student_id_len: int):
        class Is_student:
            def __init__(self):
                self.is_student = None
                self.name = None
                self.name_len = name_len
                self.sex = None
                self.birth_date = None
                self.student_id = None
                self.student_id_len = None

        # 创建判断值
        student = Is_student()
        # 判断名字是否合规
        if len(name) > name_len:
            student.name = False
        else:
            student.name = True
        # 判断性别是否合规
        if sex not in ['男', '女', '男生', '女生', '雄性', '雌性']:
            student.sex = False
        else:
            student.sex = True
        # 判断出生日期是否合规
        if is_num(''.join(birth_date.split('/'))).is_num \
                or is_num(''.join(birth_date.split('\\'))).is_num \
                or is_num(''.join(birth_date.split('-'))).is_num:
            now = datetime.date.today()

            def date_is_ture(birth_date_list_):
                try:
                    eval_list = []
                    for i in birth_date_list_:
                        eval_list.append(int(i))
                    logging.info(eval_list)
                    if eval_list[0] < now.year:
                        datetime.date(*eval_list)
                        log.info(datetime.date(*eval_list).isoformat())
                        return True
                    else:
                        return False
                except ValueError:
                    return False

            if len(birth_date.split('/')) != 1:
                birth_date_list = birth_date.split('/')
                student.birth_date = date_is_ture(birth_date_list)
            elif len(birth_date.split('-')) != 1:
                birth_date_list = birth_date.split('-')
                student.birth_date = date_is_ture(birth_date_list)
            elif len(birth_date.split('\\')) != 1:
                birth_date_list = birth_date.split('\\')
                student.birth_date = date_is_ture(birth_date_list)
            else:
                student.birth_date = False
        else:

            student.birth_date = False

        # 判断学号是否合规
        if not is_num(student_id).is_num and len(student_id) > student_id_len:
            student.student_id = False
        else:
            student.student_id = True
        # 判断是否满足全部条件
        if student.name and student.birth_date \
                and student.student_id and student.sex:
            student.is_student = True
        else:
            student.is_student = False
        return student

    # 添加学生信息函数(交互部分)
    def add_students(self):
        try:

            def if_in_quit_list(obj):
                if obj in ['Q', 'q', '']:
                    if yes_no(f'<{get_f_now_easy()}:?>: 是否取消添加学生(Y/N): '):
                        print('—' * 56)
                        raise NameError

            print('<!> 取消请输入Q:')
            name = input(f"<{get_f_now_easy()}:in>: 请输入学生名字: ").strip()
            if_in_quit_list(name)
            sex = input(f"<{get_f_now_easy()}:in>: 请输入学生性别: ").strip()
            if_in_quit_list(name)
            birth_date = input(f"<{get_f_now_easy()}:in>: 请输入学生出生日期(格式:年/月/日): ").strip()
            if_in_quit_list(name)
            student_id = input(f"<{get_f_now_easy()}:in>: 请输入学生学号: ").strip()
            if_in_quit_list(name)

            while self.is_student(name, 5, sex, birth_date, student_id, 9).is_student is False:

                if_student = self.is_student(name, 5, sex, birth_date, student_id, 9)
                if if_student.name is False:
                    name = input(f'<{get_f_now_easy()}:!>: 名字输入不合规,请重新输入: ').strip()
                    if_in_quit_list(name)
                if if_student.sex is False:
                    sex = input(f'<{get_f_now_easy()}:!>: 性别输入不合规,请重新输入: ').strip()
                    if_in_quit_list(sex)
                if if_student.birth_date is False:
                    birth_date = input(f'<{get_f_now_easy()}:!>: 出生日期输入不合规,请重新输入: ')
                    if_in_quit_list(birth_date)
                if if_student.student_id is False:
                    student_id = input(f'<{get_f_now_easy()}:!>: 学号输入不合规,请重新输入: ')
                    if_in_quit_list(student_id)
        except NameError:
            return None
        student = Student(name, sex, birth_date, student_id)
        self.add_data(student.student_dict())
        print(f"<{get_f_now_easy()}:OK>: 学生 {name} 已添加")
        print('—' * 56)

    # 删除学生信息函数
    def del_student(self):
        students = self.read_data()
        name = input(f"<{get_f_now_easy()}:in>:\n 请输入要删除的学生名字(或者学号): ").strip()
        if is_num(name).is_num:
            if name in students:
                del students[name]
            else:
                print(f'<{get_f_now_easy()}:!>: 学生{name} 不存在')
                print('—' * 56)
                return None
        else:
            del_count = 0
            del_obj = None
            for student in students:
                if students[student]['名字'] == name:
                    del_obj = student
                    del_count += 1
            if del_obj is not None and del_count == 1:
                del students[del_obj]
            elif del_obj is not None and del_count != 1:
                self.find_students('名字', name, True)
                name = input(f'<{get_f_now_easy()}:!>:\n 查询结果不唯一,请输入学号删除:')
                if is_num(name).is_num:
                    if name in students:
                        del students[name]
                    else:
                        print(f'<{get_f_now_easy()}:!>: 学生{name} 不存在')
                        print('—' * 56)
                        return None
                else:
                    print(f'<{get_f_now_easy()}:!>: 学号输入不正确')
                    return None
            else:
                print(f'<{get_f_now_easy()}:!>: 学生{name} 不存在')
                print('—' * 56)
                return None
        self.write_data(students)
        print(f'<{get_f_now_easy()}:OK>:  学生 {name} 已删除')
        print('—' * 56)

    # 查找学生信息函数(查找主函数部分)
    def find_students(self, find_type: str, find_data: str, yn_print: bool = False):
        count = 1
        find_out = []
        students_data = self.read_data()
        for student_id in students_data:
            student = students_data[student_id]
            if find_data == student[find_type] or find_data in student[find_type]:
                student_data_str = '[{0:^5}] | 姓名:{1:<4} | 性别:{2:<} | 学号:{3:<9} | 出生日期:{4:^8} |' \
                    .format(count, student['名字'], student['性别'], student['学号'], student['出生日期'])
                count += 1
                if yn_print:
                    print(student_data_str)
                else:
                    find_out.append(student_data_str)
        if count == 1:
            return 'Not found'
        if not yn_print:
            return find_out

    # 查找学生信息(信息输入部分)
    def find_student_in(self):
        find_type = None
        in_type = input(f'<{get_f_now_easy()}:in>:\n 请输入要查找的数据类型(名字,性别,出生日期,学号): ').strip()
        if in_type in ['名字', '名', '姓名', 'name', '1']:
            find_type = '名字'
        elif in_type in ['性别', '性', 'sex', '男', '女', '2']:
            find_type = '性别'
        elif in_type in ['出生日期', '出生', '日期', '出', '日', '3']:
            find_type = '出生日期'
        elif in_type in ['学号', '学', '号', '4']:
            find_type = '学号'
        else:
            print(f'<{get_f_now_easy()}:!>:没有该类型')
            self.find_student_in()
        in_data = input(f'<{get_f_now_easy()}:in>: 请输入要查找的数据: ')
        find_out = self.find_students(find_type, in_data)
        if find_out == 'Not found':
            print(f'<{get_f_now_easy()}:!>: 未查找到学生信息')
            print('—' * 56)
        else:
            print(f'<{get_f_now_easy()}:OK>: 查询结果如下:')
            for student in find_out:
                print(student)
            print('—' * 56)

    # 显示所有学生信息
    def show_students(self):
        print(f'<{get_f_now_easy()}:~> 所有学生信息如下: ')
        count = 1
        students_data = self.read_data()
        for student_id in students_data:
            student = students_data[student_id]
            student_data_str = '[{0:^5}] | 姓名:{1:<4} | 性别:{2:<} | 学号:{3:<9} | 出生日期:{4:^8} |' \
                .format(count, student['名字'], student['性别'], student['学号'], student['出生日期'])
            count += 1
            print(student_data_str)
        print('—' * 56)

    # 导出学生信息函数
    def export_excel(self):
        """
        学生信息导出到 students.xlsx中
        """
        file_path = tk_f_save(title='选择导出路径', initialfile='学生信息表.xlsx', filetypes=[("*.xlsx", '')])
        if file_path != '':
            students_data = self.read_data()
            df = pd.DataFrame(gdv(students_data))
            df.to_excel(file_path, sheet_name='学生信息表')
            print(f'<{get_f_now_easy()}:OK>: 文件已成功导出 导出目录:{os.path.dirname(file_path)}')
        else:
            print(f'<{get_f_now_easy()}:!>:取消导出')


sms = SMS()
sms.main()
