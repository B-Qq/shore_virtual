from socket import *
from tkinter.scrolledtext import ScrolledText #滚动文本框
import threading
import time
from tkinter import *

def destroy_top(top):
    time.sleep(6)
    top.destroy()

#配置文件,滚动文本框,tkinter对象
def tcp_init(cf,ti,top):
    _rf = 0
    host = cf.get("TCP", "Host")  # ip
    port = int(cf.get("TCP", "Port"))  # 端口号
    addr = (host,port)
    tctimeClient = socket(AF_INET, SOCK_STREAM)
    try:
        _rf = tctimeClient.connect(addr)
    except Exception as err:
        ti.insert(END, "连接前置机失败,请检查ip地址及端口配置是否正确\n")
        ti.see(END);
        top_destroy = threading.Thread(target=lambda :destroy_top(top), name='destroy_top')
        top_destroy.start()
        top.mainloop()
        exit()
    if _rf != 0:
        ti.insert(END, "连接前置机成功:\n   --->IP地址为" + str(host) + "\n   --->端口为" + str(port)+ "\n")
        ti.see(END);
    return tctimeClient

