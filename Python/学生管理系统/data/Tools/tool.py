import time


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


def item_to_str(item: list | tuple) -> str:
    out_str = ''
    for value in item:
        out_str = out_str + str(value)
    return out_str


def get_f_now_easy() -> str:
    return time.strftime('%Y-%m-%d %H:%M:%S')
