import os
import random
import shutil
import sys

from tqdm import tqdm


def renames(path: str, new_name: str, show_log: bool = False):
    if os.path.exists(path):
        os.chdir(path)
        if show_log:
            items = tqdm(os.listdir(path), desc='重命名中:')
        else:
            items = os.listdir(path)
        count = 1
        for file in items:
            try:
                file_suffix = file.split('.')[-1]
                os.renames(file, new_name + str(count) + f'.{file_suffix}')
                count = count + 1
            except FileExistsError:
                continue
        if show_log:
            print("批量重命名完成")


def del_same_files(path: str, show_log: bool = False) -> bool:
    """
    Delete the same files in bulk
    批量删除相同的文件
    :param show_log: 是否显示日志
    :param path:批量删除相同文件的路径
    :return: 是否成功删除 成功返回True,失败返回False
    """
    if not show_log:
        sys.stdout = open(os.devnull, 'w')
    if os.path.exists(path):
        print(f'文件目录 {path} 存在')
        os.chdir(path)
        dir_list = os.listdir(path)
        file_dict = dict()

        if show_log:
            items1 = tqdm(dir_list, desc='文件加载中')
        else:
            items1 = dir_list

        for file_name in items1:
            try:
                with open(file_name, 'rb') as f:
                    file_dict[f.read()] = file_name
            except PermissionError:
                continue

        temp_name = 'temp$' + str(random.randint(10000, 99999))
        os.mkdir(temp_name)
        os.chdir(temp_name)

        if show_log:
            items2 = tqdm(file_dict.items(), desc='文件写入中')
        else:
            items2 = file_dict.items()

        for new_file, new_name in items2:
            with open(new_name, 'wb') as f:
                f.write(new_file)

        os.chdir(path)

        if show_log:
            items3 = tqdm(dir_list, desc='文件删除中')
        else:
            items3 = dir_list

        for file_name in items3:
            try:
                os.remove(file_name)
            except OSError:
                continue

        os.chdir(temp_name)
        new_file_list = os.listdir()

        if show_log:
            items4 = tqdm(new_file_list, desc='文件移动中')
        else:
            items4 = new_file_list

        for file_name in items4:
            shutil.move(file_name, path)

        os.chdir(path)
        shutil.rmtree(temp_name)

        sys.stdout = sys.__stdout__
        return True
    sys.stdout = sys.__stdout__
    return False
