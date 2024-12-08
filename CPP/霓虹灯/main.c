#include <stdio.h>
#include <time.h>
#include <windows.h>
#define MAX_SIZE 10

// 程序堵塞
void time_sleep(float s)
{
    long unsigned int target = GetTickCount() + (int)(s * 1000);
    while (1)
        if (GetTickCount() >= target)
            break;
}

// 输出队列
void out(int *list)
{
    for (int i = 0; i < MAX_SIZE; i++)
    {
        if (list[i])
            putchar('0');
        else
            putchar(' ');
    }
}

// 清除行输出
void clear(void)
{
    for (int i = 0; i < 255; i++)
        putchar('\b');
}

int main(int argc, char const *argv[])
{
    // 队列
    int list[MAX_SIZE];
    // 当前元素索引
    int index = 0;
    // 初始化队列
    for (int i = 0; i < MAX_SIZE; i++)
        list[i] = 0;
    while (1)
    {
        time_sleep(0.2);
        // 当前元素进入队列
        list[index] = 1;
        // 清除元素在队列队列走过的痕迹
        if (index != 0)
            list[index - 1] = 0;
        // 元素到队列末尾时停止移动
        if (index == MAX_SIZE - 1 || list[index + 1] == 1)
            index = 0;
        // 元素未到队列时候向前移动
        else
            index++;
        // 判断队列是否已满
        int is_full = 1;
        for (int i = 0; i < MAX_SIZE; i++)
            if (list[i] == 0)
                is_full = 0;
        if (is_full)
        // 如果队列已满
        {
            // 闪烁效果
            for (int i = 0; i < 3; i++)
            {
                clear();
                for (int i = 0; i < MAX_SIZE; i++)
                    putchar(' ');
                time_sleep(0.2);
                clear();
                out(list);
                time_sleep(0.2);
            }
            // 清空队列
            for (int i = 0; i < MAX_SIZE; i++)
                list[i] = 0;
        }
        // 输出队列
        clear();
        out(list);
    }
    return 0;
}
