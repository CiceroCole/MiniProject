from platform import system as sys_type
import tkinter.filedialog as tkf
import tkinter.ttk as ttk
from hashlib import md5
import tkinter as tk
import threading
import os.path
import random
import socket
import time
import sys


def hight_dpi(root: tk.Tk):
    import ctypes

    # 告诉操作系统使用程序自身的dpi适配
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # 获取屏幕的缩放因子
    ScaleFactor = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    # 设置程序缩放
    root.tk.call("tk", "scaling", ScaleFactor / 75)


def show_info(info: str):
    InfoLabel.config(text=info)
    InfoLabel.after(5000, func=lambda: InfoLabel.config(text=""))
    ...


def apply_ToIpPort():
    def __apply_ToIpPort():
        try:
            GetToIp = ToIpEnt.get()
            GetToPort = ToPortEnt.get()
            if not GetToIp or not GetToPort:
                # TODO 提醒值出错
                show_info("请输入目标主机的地址与端口")
            GetToPort = int(GetToPort)
            so = socket.socket(family=socket.AF_INET)
            so.connect((GetToIp, GetToPort))
            so.send(b"<T>")
            so.close()
            global ToIp, ToPort
            ToIp = GetToIp
            ToPort = GetToPort
            InfoLB.delete(4, tk.END)
            for i in ["目标主机地址:", ToIp, "目标主机端口:", ToPort]:
                InfoLB.insert(tk.END, i)
        except socket.error:
            # TODO 提醒连接出错
            show_info("无法连接至目标主机")
            ...
        except ValueError:
            # TODO 提醒值出错
            show_info("端口值出错")
            ...

    task = threading.Thread(target=__apply_ToIpPort)
    task.start()
    ...


def AddMsgLog(msg: str):
    index = 0
    width = 30
    msg = time.strftime("<%H:%M:%S> ") + msg
    for _i in range(len(msg) // width + 1):
        if index + width <= len(msg) - 1:
            MsgLB.insert(tk.END, msg[index : index + width])
            index += width
        else:
            MsgLB.insert(tk.END, msg[index:])
    ...


def StartRecvMsg():
    def __RecvMsg():
        S = socket.socket(family=socket.AF_INET)
        S.bind((FromIp, FromPort))
        S.listen(5)
        while not RootIsClose:
            C, CA = S.accept()
            Frist: bytes = C.recv(3)
            MsgType = Frist.decode("utf-8")
            # print(MsgType)
            if MsgType == "<T>":
                C.close()
                continue
            elif MsgType == "<C>":
                C.close()
                return
            elif MsgType == "<M>":
                data = temp = C.recv(1024)
                while temp:
                    temp = C.recv(1024)
                    data += temp
                C.close()
                AddMsgLog("对方: {}".format(data.decode("utf-8")))
            elif MsgType == "<F>":
                FileNameBytes = b""
                GitOneByte = C.recv(1)
                while b"<" != GitOneByte:
                    FileNameBytes += GitOneByte
                    GitOneByte = C.recv(1)
                FileName = FileNameBytes.decode("utf-8")
                with open(file=os.path.join(MainPath, FileName), mode="wb") as Rf:
                    data = C.recv(1024)
                    while data:
                        Rf.write(data)
                        data = C.recv(1024)
                C.close()
                AddMsgLog(f"<!> 文件 {FileName} 已保存至 {MainPath} 目录下")

    task = threading.Thread(target=__RecvMsg)
    task.start()
    ...


def SelectFile():
    GetFilePath = tkf.askopenfilename(
        title="请选择文件", filetypes=[("任意文件", ".*")]
    )
    if not GetFilePath:
        return
    global SendFilePath, SendFileName
    SendFilePath = GetFilePath
    SendFileName = os.path.basename(SendFilePath)
    MsgEntryText.insert(tk.END, f"<!> 已选择文件: {SendFileName}")
    ...


def SendMsg():
    def __Send():
        global SendFilePath
        GetMsg = MsgEntryText.get("1.0", tk.END)
        if not GetMsg:
            # TODO 提醒值出错
            show_info("请输入要发送的信息")
            return
        if not ToIp or not ToPort:
            # TODO 提醒值出错
            show_info("请输入目标主机的地址与端口")
            return
        if SendFilePath:
            if SendFileName in GetMsg:
                FileSo = socket.socket(family=socket.AF_INET)
                FileSo.connect((ToIp, ToPort))
                FileSo.send(b"<F>")
                SendFileName_AndFlag = SendFileName + "<"
                FileSo.send(SendFileName_AndFlag.encode("utf-8"))
                with open(file=SendFilePath, mode="rb") as Sf:
                    FileSo.sendfile(file=Sf)
                FileSo.close()
                AddMsgLog("<!> 文件 {} 已发送".format(SendFileName))
                MsgEntryText.delete("1.0", tk.END)
            else:
                show_info("<!> 文件 {} 已取消发送".format(SendFileName))
                MsgEntryText.delete("1.0", tk.END)
            SendFilePath = ""
        else:
            MsgSo = socket.socket(family=socket.AF_INET)
            MsgSo.connect((ToIp, ToPort))
            MsgSo.send(b"<M>")
            MsgSo.send(GetMsg.encode("utf-8"))
            MsgSo.close()
            MsgEntryText.delete("1.0", tk.END)
            AddMsgLog("自己: " + GetMsg)

    task = threading.Thread(target=__Send)
    task.start()
    ...


def CloseRoot():
    global RootIsClose
    RootIsClose = True
    try:
        so = socket.socket(family=socket.AF_INET)
        so.connect((FromIp, FromPort))
        so.send(b"<C>")
        so.close()
    except ConnectionRefusedError:
        pass
    root.destroy()
    root.quit()
    sys.exit(0)
    ...


ToIp = ""
ToPort = 0
FromIp = socket.gethostbyname(socket.gethostname())
FromPort = random.randint(49152, 65535)
SendFilePath = ""
SendFileName = ""
RootIsClose = False
MainPath = os.getcwd()

root = tk.Tk()
if sys_type() == "Windows":
    hight_dpi(root)
# root.geometry("500x400")
root.title("LiteMsg")
root.resizable(False, False)
# 对方IP地址与端口控件
ToIpEnt = ttk.Entry(width=32)
ToIpEnt.grid(row=0, column=0)
ToIpEnt.insert(tk.END, "请输入目标主机地址")
ToPortEnt = ttk.Entry(width=6)
ToPortEnt.insert(tk.END, "端口")
ToPortEnt.grid(row=0, column=1)
ttk.Button(text="确认", command=apply_ToIpPort, width=15).grid(row=0, column=2)

# 显示信息记录
MsgLB = tk.Listbox(height=10)
MsgLB.grid(row=1, column=0, columnspan=1, sticky=tk.E + tk.W)
MsgScr = ttk.Scrollbar(command=MsgLB.yview)
MsgLB.config(yscrollcommand=MsgScr.set)
MsgScr.grid(row=1, column=1, columnspan=1, sticky=tk.E + tk.W + tk.N + tk.S)


InfoLB = tk.Listbox(width=10, height=10)
InfoLB.grid(row=1, column=2, sticky=tk.E + tk.W + tk.N + tk.S)
for i in ["本地地址:", FromIp, "本地端口:", FromPort]:
    InfoLB.insert(tk.END, i)


# 消息提示栏
InfoLabel = ttk.Label(foreground="#FF0000")
InfoLabel.grid(row=2, column=0, columnspan=3, sticky=tk.E + tk.W)


# 输入栏
MsgEntryText = tk.Text(width=30, height=2)
MsgEntryText.grid(
    row=3, rowspan=2, column=0, columnspan=2, sticky=tk.E + tk.W + tk.N + tk.S
)
MsgEntryText.bind("<Return>", func=lambda _: SendMsg())
SendBut = ttk.Button(text="发送", command=SendMsg)
SelectFileBut = ttk.Button(text="文件", command=SelectFile)
SendBut.grid(row=3, column=2, sticky=tk.E + tk.W + tk.N + tk.S)
SelectFileBut.grid(row=4, column=2, sticky=tk.E + tk.W + tk.N + tk.S)

# 开启信息接受服务
StartRecvMsg()

# 处理窗口关闭事件
root.protocol("WM_DELETE_WINDOW", func=CloseRoot)

tk.mainloop()
