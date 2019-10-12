from tkinter import *
import tkinter as tk
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText #滚动文本框
from tkinter import ttk # 导入ttk模块，因为下拉菜单控件在ttk中
import shorePowerProtocol

class setConfigLayout(object):
    def __init__(self,cf):
        self.cf = cf
        self.setConfig = tk.Tk(className='参数设置')
        self.setConfig.title("参数设置")
        self.setConfig.geometry('450x200')
        self.inputFrontIp()
        self.inputFrontPort()
        self.inputDBIp()
        self.inputDBPort()
        self.inputStation()
        self.connect()
        self.setConfig.mainloop()

    # 输入前置IP地址
    def inputFrontIp(self):
        PortY = 16
        self.FrontIp = StringVar(self.setConfig, value=self.cf.get("TCP", "Host"))
        Label(self.setConfig, text="前置IP地址:").place(x=10, y=PortY)
        tk.Entry(self.setConfig, bd=2, textvariable=self.FrontIp,width = 22).place(x=80, y=PortY)

    # 输入前置端口号
    def inputFrontPort(self):
        PortY = 16
        self.FrontPort = StringVar(self.setConfig, value=self.cf.get("TCP", "Port"))
        Label(self.setConfig, text="前置端口号:").place(x=270, y=PortY)
        tk.Entry(self.setConfig, bd=2, textvariable=self.FrontPort,width = 7).place(x=340, y=PortY)

    #输入数据库IP地址
    def inputDBIp(self):
        PortY = 70
        self.DBIp = StringVar(self.setConfig, value=self.cf.get("DB", "Host"))
        Label(self.setConfig, text="数据库IP地址:").place(x=10, y=PortY)
        tk.Entry(self.setConfig, bd=2, textvariable=self.DBIp,width = 22).place(x=90, y=PortY)

    # 输入数据库端口号
    def inputDBPort(self):
        PortY = 70
        self.DBPort = StringVar(self.setConfig, value=self.cf.get("DB", "Port"))
        Label(self.setConfig, text="数据库端口号:").place(x=280, y=PortY)
        tk.Entry(self.setConfig, bd=2, textvariable=self.DBPort,width = 7).place(x=360, y=PortY)

    # 输入站号
    def inputStation(self):
        PortY = 108
        self.Station = StringVar(self.setConfig, value=self.cf.get("STATION", "ID"))
        Label(self.setConfig, text="站号:").place(x=10, y=PortY)
        tk.Entry(self.setConfig, bd=2, textvariable=self.Station,width = 50).place(x=70, y=PortY)


    def connect(self):
        Button(self.setConfig, text='确定', command=self.sureButton, width=55, background='red').place(x=20, y=145)

    def sureButton(self):
        self.cf.set("TCP","Host",self.FrontIp.get())
        self.close()

    def close(self):
        self.setConfig.destroy()