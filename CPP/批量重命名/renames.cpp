#include <iostream>
#include <filesystem>
#include <string>
#include <fstream>

/*
    笔记:
    std::stoi : 字符串转数字
    std::ofstream : 文件输出流
    std::filesystem : 文件系统库
    std::filesystem::path : 路径类
    std::filesystem::rename : 重命名文件
    std::filesystem::extension : 获取文件后缀
    std::filesystem::absolute : 获取绝对路径
    std::filesystem::current_path : 获取当前路径
    std::filesystem::path::generic_string : 获取路径字符串
    std::filesystem::temporary_directory_path : 获取临时目录
    std::filesystem::directory_iterator: 遍历文件夹
    std::filesystem::exists : 判断文件是否存在
    std::filesystem::is_directory : 判断是否为文件夹
    std::filesystem::is_symlink : 判断是否为软链接
    std::filesystem::append_directory_options : 追加选项

*/

namespace fs = std::filesystem;

int main(int argc, char const *argv[])
{
    // 参数
    std::string parameters[argc];
    // 日志文件
    std::string LogFilePath = fs::temp_directory_path().append("log.txt").generic_string();
    std::ofstream Logs(LogFilePath);
    int OpenLog = 0;
    // 重命名参数
    std::string BaseName = "";
    std::string TargetExt = "";
    // 输出参数
    fs::path OutDir = fs::current_path();
    // 统计
    int FileCount = -1;

    // 输出帮助信息
    auto OutHelpInfo = []()
    {
        std::cout << "批量重命名文件" << std::endl;
        std::cout << "参数说明:" << std::endl;
        std::cout << "  -h, --Help      显示帮助信息" << std::endl;
        std::cout << "  -b, --Base      设置重命名的基准文件名" << std::endl;
        std::cout << "  -l, --Log       开启日志保存重命名记录" << std::endl;
        std::cout << "  -c, --FileCount 设置重命名文件的个数" << std::endl;
        std::cout << "  -o, --OutDir    设置重命名文件的输出目录" << std::endl;
        std::cout << "  -e, --Ext       指定需要重命名文件的后缀名(含分隔符\".\")" << std::endl;
    };

    auto UpperStr = [](std::string str)
    {
        std::string result;
        for (auto &c : str)
            result += toupper(c);
        return result;
    };
    if (argc < 3)
    {
        OutHelpInfo();
        return -1;
    }
    // 参数解析
    for (int i = 0; i < argc; i++)
    {
        parameters[i] = argv[i];
        if (parameters[i] == "-h" || parameters[i] == "--help")
        {
            OutHelpInfo();
            return 0;
        }
        else if (parameters[i] == "-b" || parameters[i] == "--Base")
        {
            if (i + 1 < argc)
                BaseName = argv[i + 1];
            else
            {
                std::cout << "错误: 参数 -b 缺少参数" << std::endl;
                OutHelpInfo();
                return -1;
            }
        }
        else if (parameters[i] == "-l" || parameters[i] == "--Log")
            OpenLog = 1;
        else if (parameters[i] == "-c" || parameters[i] == "--FileCount")
        {
            if (i + 1 < argc)
                FileCount = std::stoi(argv[i + 1]);
            else
            {
                std::cout << "错误: 参数 -c 缺少参数" << std::endl;
                OutHelpInfo();
                return -1;
            }
        }
        else if (parameters[i] == "-o" || parameters[i] == "--OutDir")
        {
            if (i + 1 < argc)
                OutDir = fs::absolute(argv[i + 1]);
            else
            {
                std::cout << "错误: 参数 -o 缺少参数" << std::endl;
                OutHelpInfo();
                return -1;
            }
        }
        else if (parameters[i] == "-e" || parameters[i] == "--Ext")
        {
            if (i + 1 < argc)
                TargetExt = UpperStr(std::string(argv[i + 1]));
            else
            {
                std::cout << "错误: 参数 -e 缺少参数" << std::endl;
                OutHelpInfo();
                return -1;
            }
        }
    }

    if (!OpenLog)
        Logs.close();

    // 输出参数
    std::cout << "基准文件名: " << BaseName << std::endl;
    if (OpenLog)
        std::cout << "已开启开启日志" << std::endl;
    if (FileCount != -1)
        std::cout << "重命名文件个数: " << FileCount << std::endl;
    if (TargetExt != "")
        std::cout << "目标文件后缀: " << TargetExt << std::endl;
    std::cout << "输出目录: " << OutDir.generic_string() << std::endl;
    std::cout << "是否开始批量重命名文件?(Y/N): ";

    // 确认
    char c;
    std::cin >> c;
    if (c != 'Y' && c != 'y')
        return 0;

    fs::path currentPath = fs::current_path();
    int count = 1, ID = 0;
    // 遍历
    for (auto &file : fs::directory_iterator(currentPath))
    {
        // 达到指定个数退出
        if (FileCount != -1 && count > FileCount)
            break;
        // 跳过文件夹
        if (file.is_directory())
            continue;
        // 确认指定后缀
        std::string Extension = UpperStr(file.path().extension().generic_string());
        if (!TargetExt.empty() && Extension != TargetExt)
            continue;
        // 获取目标文件名
        fs::path ToName = OutDir / (BaseName + std::to_string(ID++) + Extension);
        // 跳过已重命名文件
        if (fs::exists(ToName))
        {
            if (OpenLog)
            {
                std::cout << "文件 \"" << ToName << "\" 已存在, 跳过。" << std::endl;
                ID = ID + 1;
            }
            continue;
        }
        // 跳过软链接
        if (fs::is_symlink(file))
        {
            if (OpenLog)
                std::cout << "文件 \"" << file.path() << "\" 是软链接, 跳过。" << std::endl;
            continue;
        }
        // 输出日志
        if (OpenLog)
        {
            Logs << file.path() << " => " << ToName << std::endl;
            std::cout << "Renaming: " << file.path() << " => " << ToName << std::endl;
        }
        // 重命名
        fs::rename(file.path(), ToName);
        count++;
    }
    // 保存日志
    if (OpenLog)
    {
        Logs.close();
        fs::rename(LogFilePath, currentPath / "log.txt");
        std::cout << "重命名完成,日志保存在: " << (currentPath / "log.txt").generic_string() << std::endl;
    }
    return 0;
}
