from tkinter import *
import tkinter as tk
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText #滚动文本框
from tkinter import ttk # 导入ttk模块，因为下拉菜单控件在ttk中
import shorePowerProtocol
import sys

class layout(object):
    # 桩号端口号集合, 站号, socket文件描述符
    def __init__(self, StakePortSet, StationId,cf,db):
        self.cf = cf
        self.db = db;
        self.StakePortSet = StakePortSet
        self.top = tk.Tk(className='岸电云网站内监控模拟器')
        self.setTitle("站内监控模拟软件")
        self.top.geometry('700x550')
        self.ScrolledText()
        self.inputStake(StakePortSet)
        self.inputPort()
        self.setStationId(StationId)
        self.workState()
        self.calcException()
        self.selectWarn()
        self.distMeterButton()
        self.selectAllWarn()

    def mainloop(self):
       self.top.mainloop()

    #设置title
    def setTitle(self,str):
        self.top.title(str);

    #滚动文本框
    def ScrolledText(self):
        self.ti = ScrolledText(self.top, width=95, height=24, background='#ffffff')
        self.ti.place(x=10, y=180)

    #获取滚动文本框
    def getScrolledText(self):
        return self.ti

    #输入桩号
    def inputStake(self,StakePortSet):
        StakeY = 16
        # 输入桩号
        Label(self.top, text="桩号:").place(x=180, y=StakeY)
        # 创建下拉菜单
        self.StakeNoCombox = ttk.Combobox(self.top)
        self.StakeNoCombox.place(x=220, y=StakeY)
        StakeId = []
        # 设置下拉菜单中的值为桩编号
        for it in StakePortSet:
            StakeId.append(it[0])
        # 设置下拉菜单中的值为桩编号
        self.StakeNoCombox['value'] = StakeId
        # 设置默认值，即默认下拉框中的内容
        self.StakeNoCombox.current(0)

    #输入端口号
    def inputPort(self):
        PortY = 16
        self.port_e = StringVar(self.top, value='1')
        Label(self.top, text="端口号:").place(x=400, y=PortY)
        tk.Entry(self.top, bd=2, textvariable=self.port_e, width=5).place(x=450, y=PortY)

    #设置站号
    def setStationId(self,StationId):
        StationY = 16
        # text1 = Text(self.top, width=24, height=1)
        # text1.place(x=520, y=StationY)
        # text1.insert(INSERT, self.db.QueryStationName(self.cf, StationId))
        Label(self.top, width = 24, text = self.db.QueryStationName(self.cf, StationId),background = 'green').place(x=520,y=StationY)

    #连接线缆按钮
    def connect(self, link_button):
        Button(self.top, text='连接线缆', command=link_button, width=8, background='blue').place(x=20, y=16)

    #断开线缆按钮
    def disconnect(self, free_button):
        Button(self.top, text='断开线缆', command=free_button, width=8, background='red').place(x=100, y=16)

    #工作状态
    def workState(self):
        WorkStateY = 48
        Label(self.top, text="工作状态:").place(x=20, y=WorkStateY)
        self.WorkStateComBox = ttk.Combobox(self.top, width=6)
        self.WorkStateComBox.place(x=80, y=WorkStateY)
        # 设置下拉菜单中的值为桩编号
        self.WorkStateComBox['value'] = ['待机[2]', '工作[3]', '完成[5]', '告警[1]', '离线[4]']
        # 设置默认值，即默认下拉框中的内容
        self.WorkStateComBox.current(0)

    #获取工作状态
    def getWorkStateComBox(self):
        return self.WorkStateComBox

    #发送全部桩的状态
    def sendAllState(self,sendall_status):
        WorkStateY = 48
        Button(self.top, text='发送状态(全)', command=sendall_status, width=12, background='red').place(x=600, y=WorkStateY)

    #计量异常绑定
    # def calcExceptionBind(self,*args):
    #     if self.CalcWarnComBox.get() != "正常":
    #         self.WorkStateComBox.current(1)
    #     else:
    #         self.WorkStateComBox.current(0)

    #异常计量
    def calcException(self):
        CalcWarnY = 48
        Label(self.top, text="计量异常:").place(x=180, y=CalcWarnY)
        self.CalcWarnComBox = ttk.Combobox(self.top,width = 32)
        self.CalcWarnComBox.place(x=240, y=CalcWarnY)
        # 设置下拉菜单中的值为桩编号
        self.CalcWarnComBox['value'] = ['正常', '电表飞走[过程中]', '电表倒走[过程中]', '示值采集异常(尖峰平谷的和与总不等)[过程中]',
                                        '电表飞走[止码]', '电表倒走[止码]', '示值采集异常(尖峰平谷的和与总不等)[止码]'] #无起码,无止码,订单负数
        # 设置默认值，即默认下拉框中的内容
        self.CalcWarnComBox.current(0)
        # self.CalcWarnComBox.bind("<<ComboboxSelected>>", self.calcExceptionBind)

    #发送异常计量按钮
    def sendCalcExceptionButton(self,sendCalcException):
        CalcExceptionY = 48
        Button(self.top, text='发送异常', command=sendCalcException, width=12, background='blue').place(x=500, y=CalcExceptionY)

    #告警选择
    def selectWarn(self):
        warnstatey = 81
        warnbasex = 80
        self.warnArray=[IntVar(),IntVar(),IntVar(),IntVar(),
                        IntVar(),IntVar(),IntVar(),IntVar(),
                        IntVar(),IntVar(),IntVar(),IntVar(),
                        IntVar(),IntVar(),IntVar(),IntVar(),
                        IntVar(),IntVar()]
        Label(self.top, text="告警:").place(x=20, y=warnstatey)
        Checkbutton(self.top, text='继电器状态', variable=self.warnArray[0], width=8, background='gray').place(x=warnbasex,
                                                                                                    y=warnstatey)
        tk.Checkbutton(self.top, text='过压告警', variable=self.warnArray[1], width=7, background='gray').place(x=warnbasex + 90,
                                                                                                  y=warnstatey)
        warnbasex += 90
        tk.Checkbutton(self.top, text='欠压告警', variable=self.warnArray[2], width=7, background='gray').place(x=warnbasex + 83,
                                                                                                  y=warnstatey)
        warnbasex += 83
        tk.Checkbutton(self.top, text='缺相告警', variable=self.warnArray[3], width=7, background='gray').place(x=warnbasex + 83,
                                                                                                  y=warnstatey)
        warnbasex += 83
        tk.Checkbutton(self.top, text='过流告警', variable=self.warnArray[4], width=7, background='gray').place(x=warnbasex + 83,
                                                                                                  y=warnstatey)
        warnbasex += 83
        tk.Checkbutton(self.top, text='防雷器故障', variable=self.warnArray[5], width=8, background='gray').place(x=warnbasex + 83,
                                                                                                     y=warnstatey)
        warnbasex += 90
        tk.Checkbutton(self.top, text='急停故障', variable=self.warnArray[6], width=7, background='gray').place(x=warnbasex + 83,
                                                                                                      y=warnstatey)
        warnbasex = 81
        warnstatey = 114
        tk.Checkbutton(self.top, text='漏电保护', variable=self.warnArray[7], width=7, background='gray').place(x=warnbasex,
                                                                                                       y=warnstatey)
        tk.Checkbutton(self.top, text='卷筒故障', variable=self.warnArray[8], width=7, background='gray').place(x=warnbasex + 83,
                                                                                                     y=warnstatey)
        warnbasex += 83
        tk.Checkbutton(self.top, text='电表通讯故障', variable=self.warnArray[9], width=11, background='gray').place(
            x=warnbasex + 83, y=warnstatey)
        warnbasex += 83
        tk.Checkbutton(self.top, text='门禁故障', variable=self.warnArray[10], width=7, background='gray').place(
            x=warnbasex + 111, y=warnstatey)
        warnbasex += 111
        tk.Checkbutton(self.top, text='过流故障', variable=self.warnArray[11], width=7, background='gray').place(x=warnbasex + 83,
                                                                                                   y=warnstatey)
        warnbasex += 83
        tk.Checkbutton(self.top, text='水浸故障', variable=self.warnArray[12], width=7, background='gray').place(x=warnbasex + 83,
                                                                                                      y=warnstatey)
        warnbasex += 83
        tk.Checkbutton(self.top, text='倾倒故障', variable=self.warnArray[13], width=7, background='gray').place(x=warnbasex + 83,
                                                                                                     y=warnstatey)
        warnbasex = 81
        warnstatey = 147
        tk.Checkbutton(self.top, text='本船/桩体短路', variable=self.warnArray[14], width=11, background='gray').place(x=warnbasex,
                                                                                                            y=warnstatey)
        tk.Checkbutton(self.top, text='母线短路', variable=self.warnArray[15], width=7, background='gray').place(
            x=warnbasex + 111, y=warnstatey)
        warnbasex += 111
        tk.Checkbutton(self.top, text='母线开关输出继电器状态', variable=self.warnArray[16], width=19, background='gray').place(
            x=warnbasex + 83, y=warnstatey)
        warnbasex += 83
        tk.Checkbutton(self.top, text='母线开关连接确认状态', variable=self.warnArray[17], width=17, background='gray').place(
            x=warnbasex + 167, y=warnstatey)

    #
    def sendButton(self,send_signals,heatbeatrequest,heatbeatrespone):
        Button(self.top, text='SEND', command=send_signals, width=6, height=3, background='yellow').place(x=20, y=110)
        Button(self.top, text='发送心跳请求', command=heatbeatrequest, width=11, background='yellow').place(x=20, y=510)
        Button(self.top, text='发送心跳响应', command=heatbeatrespone, width=11, background='yellow').place(x=585, y=510)

    #配电遥信
    def distMeterButton(self):
        self.DIST_METER_FLAG = IntVar()
        Radiobutton(self.top, text='配1', command=lambda :distMeterEnable(self.ti), variable=self.DIST_METER_FLAG, value=1, width=4, background='blue').place(
            x=120, y=510)
        Radiobutton(self.top, text='配0', command=lambda :distMeterDisable(self.ti), variable=self.DIST_METER_FLAG, value=0, width=4, background='blue').place(
            x=180, y=510)

    #配电告警
    def distWarnButton(self,warn_end,warn_start):
        Button(self.top, text='配电告警取消', command=warn_end, width=12, background='red').place(x=470, y=510)
        Button(self.top, text='配电告警产生', command=warn_start, width=11, background='blue').place(x=390, y=510)

    #
    def selectAllWarn(self):
        workstate = 5
        Radiobutton(self.top, variable=workstate,text='全选',command=lambda :select_all(self.warnArray),value=1,width=4,
                       background='pink').place(x=250, y=510)
        Radiobutton(self.top, text='反选',variable=workstate,command=lambda :no_select_all(self.warnArray), value=2,width=4,
                        background='pink').place(x=310, y=510)

    #获取告警状态
    def getWarnArray(self):
        return self.warnArray

    def getTop(self):
        return self.top

    #关闭程序时进行的操作
    def closeWindows(self,tcpClient):
        self.top.protocol("WM_DELETE_WINDOW", lambda :self.on_closing(tcpClient))

    def on_closing(self,tcpClient):
        if tk.messagebox.askokcancel("退出", "你想要退出程序吗?"):
            tcpClient.close()
            self.top.destroy()

    def setProtocol(self, protocol):
        self.protocol = protocol

#全选按钮
def select_all(warnArray):
    state = 1
    for i in range(0,18):
        print(i)
        warnArray[i].set(state)
#反选按钮
def no_select_all(warnArray):
    state = 0
    for i in range(0, 18):
        print(i)
        warnArray[i].set(state)

#配1
def distMeterEnable(ti):
    ti.insert(END, shorePowerProtocol.get_time() + "-->配电遥测计量数据开始上送\n")
    ti.see(END);
#配1
def distMeterDisable(ti):
    ti.insert(END, shorePowerProtocol.get_time() + "-->配电遥测计量数据停止上送\n")
    ti.see(END);