import chardet


def yes_no(Q: str) -> bool:
    yes_list = ['Y', 'y', 'Yes', 'yes', '是', '是的', '1']
    if input(Q) in yes_list:
        return True
    else:
        return False


def if_values_in_item(values: list, item) -> bool:
    true_count = 0
    for value in values:
        if value in item:
            true_count += 1
        else:
            return False
    if true_count == len(values):
        return True


# 获取文件编码类型
def get_encoding(file) -> str:
    """
    获取文件编码类型
    :param file: 文件路径
    :return: 文件的编码
    """
    # 二进制方式读取，获取字节数据，检测类型
    with open(file, 'rb') as f:
        data = f.read()
        return chardet.detect(data)['encoding']


def fab_iter(n: int):
    """
    生成斐波那契數列可迭代对象
    :param n: 输出斐波那契數列前 N 个数
    """
    n, a, b, c = 0, 0, 1, 0
    while n < n:
        yield b
        a, b = b, a + b
        n = n + 1


def fab(n: int):
    """
    输出斐波那契數列
    :param n: 输出斐波那契數列前 N 个数
    """
    n, a, b, c = 0, 0, 1, 0
    while n < n:
        print(b)
        a, b = b, a + b
        n = n + 1
