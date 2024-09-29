#include <string>
#include <vector>
#include <map>
using namespace std;

// 比较两个map是否相等
template <typename K_t, typename V_t>
bool maps_equation(map<K_t, V_t> map1, map<K_t, V_t> map2)
{
    if (map1.size() != map2.size())
        return false;
    for (auto it : map1)
    {
        if (map2.count(it.first) == 0)
            return false;
        else if (map2[it.first] != it.second)
            return false;
    }
    return true;
};

// 分割字符串为 vector
vector<string> split(string _str, char _c)
{
    vector<string> out;
    string temp = "";
    for (int i = 0; i <= _str.size(); i++)
    {
        if (i != _str.size() && _str[i] != _c)
            temp += _str[i];
        else
        {
            out.push_back(temp);
            temp.clear();
        }
    }
    return out;
};

// 快速排序
template <typename T>
void sort(T &nums, int left, int right)
{
    if (right - left < 1)
        return;
    int _left = left;
    int _right = right;
    int base_num = nums[left];
    while (_left != _right)
    {
        while (nums[_right] >= base_num && _left != _right)
            _right -= 1;
        nums[_left] = nums[_right];
        while (nums[_left] <= base_num && _left != _right)
            _left += 1;
        nums[_right] = nums[_left];
    }
    nums[_left] = base_num;
    sort(nums, left, _left);
    sort(nums, _left + 1, right);
}