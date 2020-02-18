from tkinter import *
import tkinter as tk
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText #滚动文本框
from tkinter import ttk # 导入ttk模块，因为下拉菜单控件在ttk中
import shorePowerProtocol

class setStationIdLayout(object):
    def __init__(self,cf,stationId):
        self.cf = cf
        self.stationId = stationId
        self.setConfig = tk.Tk(className='站号选择')
        self.setConfig.title("站号选择")
        self.setConfig.geometry('270x90')
        self.inputStation()
        self.connect()
        self.setConfig.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.setConfig.mainloop()

    # 输入站号
    def inputStation(self):
        PortY = 20
        self.Station = StringVar(self.setConfig, value=self.cf.get("STATION", "ID"))
        Label(self.setConfig, text="站号:" ,background='blue').place(x=10, y=PortY)
        # 创建下拉菜单
        self.StationIdCombox = ttk.Combobox(self.setConfig)
        self.StationIdCombox.place(x=60, y=PortY)
        StationId = []
        # 设置下拉菜单中的值为桩编号
        for it in self.stationId:
            StationId.append(it)
        # 设置下拉菜单中的值为桩编号
        self.StationIdCombox['value'] = StationId
        # 设置默认值，即默认下拉框中的内容
        self.StationIdCombox.current(0)

    def connect(self):
        Button(self.setConfig, text='确定', command=self.sureButton, width=33, background='red').place(x=10, y=50)

    def sureButton(self):
        self.cf.set("STATION", "ID", self.StationIdCombox.get())
        with open('conf.ini','w') as fw:
            self.cf.write(fw)
        self.close()

    def close(self):
        self.setConfig.destroy()

    def on_closing(self):
        if tk.messagebox.askokcancel("退出", "你想要退出程序吗?"):
            self.close()
            sys.exit()