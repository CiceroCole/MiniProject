# 阶乘
factorial = lambda num: 1 if num == 1 else num * factorial(num - 1)
# 生成自然常数近似值公式的前n项和 e = 1 + 1/1! + 1/2! + 1/3! +...
e = lambda n=10: 1 + sum([1 / factorial(i) for i in range(1, n)])
# 使用num (0 < num < 9) 生成一个有规律的列表 如 num = 1,coun = 5 -> [1,11,111,1111,11111]
func = lambda num, count: [(10**i - 1) * (num / 9) for i in range(1, count + 1)]


def factorization(num: int):
    "因式分解"
    out_list = []
    div_num = 2
    while num != 1:
        while num % div_num == 0:
            out_list.append(div_num)
            num = num / div_num
        div_num = div_num + 1
    return out_list


# 3E4 数据集 0.0468750000秒
def __quicklySort(arr: list, left: int, right: int):
    "快速排序"
    o_left, o_right = left, right
    if left == right or left > len(arr) - 1:
        return
    base_num = arr[left]
    while left != right:
        while left != right and arr[right] >= base_num:
            right -= 1
        arr[left] = arr[right]
        while left != right and arr[left] <= base_num:
            left += 1
        arr[right] = arr[left]
    arr[left] = base_num
    __quicklySort(arr, left=o_left, right=left)
    __quicklySort(arr, left=left + 1, right=o_right)
    return arr
    ...


quicklySort = lambda arr: __quicklySort(arr=arr, left=0, right=len(arr) - 1)
"快速排序"


# 3E4 数据集 21.3125000000秒
def insertSort(arr: list):
    "插入排序"
    arr_len = len(arr)
    for outi in range(1, arr_len):
        for ini in range(outi):
            if arr[ini] > arr[outi]:
                arr[outi], arr[ini] = arr[ini], arr[outi]
    return arr


# 3E4 数据集 11.8906250000 秒
def selectSort(arr: list):
    "选择排序"
    for ini in range(len(arr) - 1):
        min_i = ini
        for outi in range(ini + 1, len(arr)):
            if arr[outi] < arr[min_i]:
                min_i = outi
        arr[ini], arr[min_i] = arr[min_i], arr[ini]
    return arr
    ...


# 3E4 数据集 51.3125000000 秒
def bubbleSort(arr: list):
    "冒泡排序"
    for _ in range(len(arr)):
        for i in range(1, len(arr)):
            if arr[i] < arr[i - 1]:
                arr[i], arr[i - 1] = arr[i - 1], arr[i]
    return arr


def TestSortFunc(func):
    from time import time

    # with open("TestData.txt", "r") as Td:
    #     TestData = eval(Td.read())
    TestData = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    TestDataCopy = TestData.copy()
    StartTime = time()
    out = func(TestData)
    OverTime = time()
    TestDataCopy.sort()
    print("验证数据:", out == TestDataCopy)
    print(f"运行时间: {OverTime-StartTime:.10f}")
    ...


TestSortFunc(quicklySort)
