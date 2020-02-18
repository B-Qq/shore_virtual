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
        self.setConfig.geometry('450x190')
        self.inputFrontIp()
        self.inputFrontPort()
        self.inputDBIp()
        self.inputDBPort()
        # self.inputStation()
        self.inputUser()
        self.inputDBpasswd()
        self.inputDB()
        self.connect()
        self.setConfig.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.setConfig.mainloop()

    # 输入前置IP地址
    def inputFrontIp(self):
        PortY = 16
        self.FrontIp = StringVar(self.setConfig, value=self.cf.get("TCP", "Host"))
        Label(self.setConfig, text="前置IP地址:" ,background='green').place(x=10, y=PortY)
        tk.Entry(self.setConfig, bd=2, textvariable=self.FrontIp,width = 22).place(x=80, y=PortY)

    # 输入前置端口号
    def inputFrontPort(self):
        PortY = 16
        self.FrontPort = StringVar(self.setConfig, value=self.cf.get("TCP", "Port"))
        Label(self.setConfig, text="前置端口号:",background='green').place(x=270, y=PortY)
        tk.Entry(self.setConfig, bd=2, textvariable=self.FrontPort,width = 7).place(x=340, y=PortY)

    #输入数据库IP地址
    def inputDBIp(self):
        PortY = 60
        self.DBIp = StringVar(self.setConfig, value=self.cf.get("DB", "Host"))
        Label(self.setConfig, text="数据库IP地址:",background='yellow').place(x=10, y=PortY)
        tk.Entry(self.setConfig, bd=2, textvariable=self.DBIp,width = 22).place(x=90, y=PortY)

    # 输入数据库端口号
    def inputDBPort(self):
        PortY = 60
        self.DBPort = StringVar(self.setConfig, value=self.cf.get("DB", "Port"))
        Label(self.setConfig, text="数据库端口号:",background='yellow').place(x=280, y=PortY)
        tk.Entry(self.setConfig, bd=2, textvariable=self.DBPort,width = 7).place(x=360, y=PortY)

    # 输入数据库用户名
    def inputUser(self):
        PortY = 83
        self.DBUser = StringVar(self.setConfig, value=self.cf.get("DB", "user"))
        Label(self.setConfig, text="数据库用户名:",background='yellow').place(x=10, y=PortY)
        tk.Entry(self.setConfig, bd=2, textvariable=self.DBUser, width=15).place(x=90, y=PortY)

    # 输入数据库密码
    def inputDBpasswd(self):
        PortY = 83
        self.DBPasswd = StringVar(self.setConfig, value=self.cf.get("DB", "password"))
        Label(self.setConfig, text="数据库密码:",background='yellow').place(x=240, y=PortY)
        tk.Entry(self.setConfig, bd=2, textvariable=self.DBPasswd, width=15,show="*").place(x=310, y=PortY)

    #输入数据库
    def inputDB(self):
        PortY = 106
        self.DB= StringVar(self.setConfig, value=self.cf.get("DB", "db"))
        Label(self.setConfig, text="数据库:",background='yellow').place(x=10, y=PortY)
        tk.Entry(self.setConfig, bd=2, textvariable=self.DB, width=15).place(x=90, y=PortY)


    # 输入站号
    def inputStation(self):
        PortY = 150
        self.Station = StringVar(self.setConfig, value=self.cf.get("STATION", "ID"))
        Label(self.setConfig, text="站号:" ,background='blue').place(x=10, y=PortY)
        tk.Entry(self.setConfig, bd=2, textvariable=self.Station,width = 50).place(x=70, y=PortY)

    def connect(self):
        Button(self.setConfig, text='确定', command=self.sureButton, width=55, background='red').place(x=20, y=150)

    def sureButton(self):
        self.cf.set("TCP","Host",self.FrontIp.get())
        self.cf.set("TCP", "Port", self.FrontPort.get())
        self.cf.set("DB", "Host", self.DBIp.get())
        self.cf.set("DB", "Port", self.DBPort.get())
        self.cf.set("DB","user", self.DBUser.get())
        self.cf.set("DB", "password", self.DBPasswd.get())
        self.cf.set("DB", "db", self.DB.get())
        # self.cf.set("STATION", "ID", self.Station.get())

        with open('conf.ini','w') as fw:
            self.cf.write(fw)
        self.close()

    def close(self):
        self.setConfig.destroy()

    def on_closing(self):
        if tk.messagebox.askokcancel("退出", "你想要退出程序吗?"):
            self.close()
            sys.exit()