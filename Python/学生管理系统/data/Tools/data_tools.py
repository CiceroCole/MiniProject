class is_num:
    """
     判断值是否为数字(int,float)
    """

    def __init__(self, obj):
        self.is_num = None
        self.type = None
        self.value = None
        if type(obj) is int:
            self.is_num = True
            self.type = int
            self.value = obj
        elif type(obj) is float:
            self.is_num = True
            self.type = float
            self.value = obj
        elif type(obj) is str:
            try:
                if obj[0] == '0':
                    obj = obj[1:]
                if type(eval(obj)) is int:
                    self.is_num = True
                    self.type = int
                    self.value = obj
                elif type(eval(obj)) is float:
                    self.is_num = True
                    self.type = float
                    self.value = obj
                else:
                    self.is_num = False
            except (NameError, SyntaxError):
                self.is_num = False


def get_dict_values(obj, deep: int = 1) -> list:
    """
    获得序列中每一个值中嵌套的值组成的列表
    """
    values_list = []

    if type(obj) is dict:
        for key in obj.keys():
            values_list.append(obj[key])
    elif type(obj) is list:
        for item in obj:
            item_type = type(item)
            if item_type is list or item_type is tuple:
                for value in item:
                    values_list.append(value)
            if item_type is dict:
                values_list.append(gdv(item))
    if deep == 1:
        return values_list
    else:
        return get_dict_values(values_list, deep - 1)


def gdv(obj, deep: int = 1) -> list:
    """
    获得字典中每一个键所对应的值组成的列表
    """
    return get_dict_values(obj, deep)


def split_date(date: str, return_type=list):
    """
    分割日期
    """
    split_key = None
    split_key_list = ['/', '\\', '-']
    for key in split_key_list:
        if key in date:
            split_key = key
    if split_key:
        return_data = date.split(split_key)
        return return_type(return_data)


def print_iterate(iterate_obj):
    for obj in iterate_obj:
        print(obj)
