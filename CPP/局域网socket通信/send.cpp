#include <iostream>
#include <fstream>
#include <string>
#include <filesystem>
#include <boost/asio.hpp>
#define PORT 5555
#define BUF_SIZE 1024
#define Error -1
using namespace std;
using boost::asio::ip::tcp;

int send_file(tcp::socket &sock, std::string filename)
{
    std::ifstream file(filename, std::ios::binary);
    if (!file)
        return Error;
    char buffer[BUF_SIZE]; // 分配内存
    while (file)
    {
        file.read(buffer, BUF_SIZE); // 读取文件
        if (file.gcount() < BUF_SIZE)
        {
            sock.send(boost::asio::buffer(buffer, file.gcount()));
            return 0;
        }
        sock.send(boost::asio::buffer(buffer, BUF_SIZE));
    }
    return 0;
}

int Parameter_parsing(int argc, char **argv, string &FilenameOrMsg, int &Is_File, boost::asio::ip::address &ip)
{
    if (argc != 3)
        return Error;
    else
    {
        boost::asio::ip::address _ip;
        boost::system::error_code ec;
        _ip = boost::asio::ip::address::from_string(argv[1], ec);
        if (ec)
            return Error;
        ip = _ip;
        FilenameOrMsg = string(argv[2]);
        if (filesystem::exists(FilenameOrMsg) && filesystem::is_regular_file(FilenameOrMsg))
            Is_File = 1;
        return 1;
    }
}

int main(int argc, char **argv)
{
    try
    {

        boost::asio::io_context io_context;
        tcp::socket sock(io_context);
        boost::asio::ip::address TargetIp;
        string FilenameOrMsg;
        string &FileName = FilenameOrMsg;
        string &Msg = FilenameOrMsg;
        int Is_File = 0;
        if (Parameter_parsing(argc, argv, FilenameOrMsg, Is_File, TargetIp) == Error)
        {
            cout << "Usage: ./send <ip> <filename or message>" << endl;
            return -1;
        }
        sock.connect(tcp::endpoint(TargetIp, PORT));
        if (Is_File)
        {
            string _FileSize = std::to_string(std::filesystem::file_size(FileName));
            string _FileName = filesystem::path(FilenameOrMsg).filename().string();
            string _info = _FileName + '|' + _FileSize;
            size_t _info_Size = _info.size();
            char _info_Size_buffer[sizeof(size_t)];
            memcpy(_info_Size_buffer, &_info_Size, sizeof(size_t));
            char Mode[10] = "FILE MODE";
            sock.send(boost::asio::buffer(Mode, 10));
            sock.send(boost::asio::buffer(_info_Size_buffer, sizeof(size_t)));
            sock.send(boost::asio::buffer(_info, _info_Size));
        }
        else
        {
            char Mode[10] = "MSGS MODE";
            sock.send(boost::asio::buffer(Mode, 10));
            size_t _Msg_Size = Msg.size();
            char _Msg_Size_buffer[sizeof(size_t)];
            memcpy(_Msg_Size_buffer, &_Msg_Size, sizeof(size_t));
            int len = sock.send(boost::asio::buffer(_Msg_Size_buffer, sizeof(size_t)));
        }
        char confirm_send = 0;
        sock.read_some(boost::asio::buffer(&confirm_send, sizeof(char)));
        if (Is_File)
            if (confirm_send || sock.is_open())
                send_file(sock, FileName);
            else
                cout << "对方已拒绝接受文件!" << endl;
        else
            sock.send(boost::asio::buffer(Msg, Msg.size()));
        sock.close();
    }
    catch (const boost::system::system_error &e)
    {
        cout << "无法链接至目标主机!" << '\n';
    }
    return 0;
}
