#include <iostream>
#include <fstream>
#include <string>
#include <boost/asio.hpp>
#define OK 0
#define Error -1
#define PORT 5555
#define BUF_SIZE 1024

using namespace std;
using boost::asio::ip::tcp;
/*
tcp::resolver resolver = tcp::resolver(context);           // 解析器
tcp::endpoint ep = *resolver.resolve("127.0.0.1", "5555"); // 解析域名
tcp::resolver resolver(io);                                // 解析器
tcp::resolver::query q("www.baidu.com", "https");          // 查询
tcp::resolver::iterator eq2 = resolver.resolve(q);         // 迭代器
tcp::endpoint ep = *resolver.resolve("127.0.0.1", "5555"); // 解析域名
tcp::resolver resolver(io);                                // 解析器
tcp::resolver::query q("www.baidu.com", "https");          // 查询
tcp::resolver::iterator eq2 = resolver.resolve(q);         // 迭代器
sock.send(...); // 发送数据
sock.write_some(boost::asio::buffer("hello world", sizeof("hello world")));
sock.async_send(...); // 异步
io_context.run();
是一个成员函数，它的作用是启动异步操作的处理循环
sock.shutdown(tcp::socket::shutdown_both); // 关闭连接

*/

bool Confirm(string FileName, size_t FileSize)
{
    cout << "文件名: " << FileName << endl;
    cout << "文件大小: " << FileSize << endl;
    cout << "是否接收文件(Y/N): ";
    char ch;
    cin >> ch;
    if (ch == 'Y' || ch == 'y')
        return 1;
    else
        return 0;
}
int recv_file(tcp::socket &sock, std::string &file_name)
{
    std::ofstream ofs(file_name, std::ios::binary);
    char buf[BUF_SIZE];
    while (true)
    {
        int len = sock.read_some(boost::asio::buffer(buf, BUF_SIZE));
        ofs.write(buf, len);
        if (len < BUF_SIZE)
            break;
    }
    return OK;
};
int main(void)
{
    cout << "开始接收数据!" << endl;
    boost::asio::io_context context;
    tcp::socket sock(context);
    tcp::endpoint ep(boost::asio::ip::address::from_string("0.0.0.0"), PORT);
    tcp::acceptor acceptor(context, ep);
    acceptor.accept(sock);
    char Mode[10] = "FILE MODE";
    string FileName;
    size_t FileSize;
    size_t InfoSize;
    sock.read_some(boost::asio::buffer(Mode, 10));
    // 将整数转换为字节流并存储到字符数组中
    char _InfoSize_buf[sizeof(size_t)];
    sock.read_some(boost::asio::buffer(_InfoSize_buf, sizeof(size_t)));
    std::memcpy(&InfoSize, _InfoSize_buf, sizeof(size_t));
    if (!strcmp("FILE MODE", Mode))
    {
        char _File_NameSzie[InfoSize + 1];
        int Index = 0;
        int len = sock.read_some(boost::asio::buffer(_File_NameSzie, InfoSize));
        _File_NameSzie[len] = '\0';
        for (auto &c : _File_NameSzie)
        {
            Index++;
            if (c == '|')
            {
                string _StrT_FileSize = string(_File_NameSzie).substr(Index, InfoSize);
                FileSize = stoi(_StrT_FileSize);
                break;
            }
            FileName = FileName + c;
        }
        if (Confirm(FileName, FileSize))
        {
            char Is_Confirm = 1;
            sock.send(boost::asio::buffer(&Is_Confirm, sizeof(char)));
            recv_file(sock, FileName);
            cout << "文件接收成功!" << endl;
        }
        else
            return 0;
    }
    else
    {
        cout << "来自 " << sock.remote_endpoint().address() << " 的消息: " << endl;
        char confirm_send = 0;
        sock.send(boost::asio::buffer(&confirm_send, sizeof(char)));
        char _Msg_buf[InfoSize + 1];
        int len = sock.read_some(boost::asio::buffer(_Msg_buf, InfoSize));
        _Msg_buf[len] = '\0';
        cout << _Msg_buf << endl;
    }
    sock.close();
    return 0;
}
