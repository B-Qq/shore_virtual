import tkinter
from tkinter import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk # 导入ttk模块，因为下拉菜单控件在ttk中
import configparser
import sys
import struct
import operatorDb as db

# workstate = IntVar()
# relay_state =  IntVar()
# ov_warn = IntVar()
# uv_warn = IntVar()
# lp_warn = IntVar()
# oc_warn = IntVar()
# spd_error = IntVar()
# scram_error = IntVar()
# leakage_elec = IntVar()
# drum_error = IntVar()
# meter_error = IntVar()
# access_error = IntVar()
# oc_error = IntVar()
# water_error = IntVar()
# dump_error = IntVar()
# short_circuit = IntVar()
# m_short_circuit = IntVar()
# m_relay_state = IntVar()
# m_switch_state = IntVar()
# DIST_FLAG = IntVar()
# DIST_FLAG.set(0)


#配置文件读取
cf = configparser.ConfigParser()
cf.read('conf.ini')

#GUI
top = tk.Tk(className='岸电云网站内监控模拟器')
top.title("站内监控模拟软件V3.3")
top.geometry('700x550')
#滚动文本框
ti = ScrolledText(top, width=95, height=24, background='#ffffff')
ti.place(x=10,y=180)

StakePortY = 16
#输入桩号
Label(top, text="桩号:").place(x=180,y=StakePortY)
# 创建下拉菜单
StakeNo = ttk.Combobox(top)
StakeNo.place(x=220,y=StakePortY)
#输入端口号
port_e = StringVar(top,value = '1')
Label(top, text="端口号:").place(x=400,y=StakePortY)
tk.Entry(top,bd =2,textvariable = port_e).place(x=450,y=StakePortY)
text1 = Text(top, width = 5, height = 1)
text1.place(x=630,y=StakePortY)
text1.insert(INSERT, "站:" + str( 1))

def link_button():
    #text.insert('insert',cmb.get()+"\n")
    print(StakeNo.get())

def free_button():
    print("断开")

tk.Button(top,text='连接线缆',command=link_button,width=8,background='blue').place(x=20,y=16)
tk.Button(top,text='断开线缆',command=free_button,width=8,background='red').place(x=100,y=16)

#工作状态
v = IntVar()
v.set(0)
WorkStateY = 48
Label(top, text="工作状态:").place(x=20,y=WorkStateY)

def send_all_status():
    print('发送全状态')
WorkState = ttk.Combobox(top,width = 6)
WorkState.place(x=80,y=WorkStateY)
# 设置下拉菜单中的值为桩编号
WorkState['value'] = ['待机','工作','完成','告警','离线']
# 设置默认值，即默认下拉框中的内容
WorkState.current(0)
tk.Button(top,text='发送状态(全)',command=send_all_status,width=18,background='red').place(x=500,y=WorkStateY)

#计量异常
v = IntVar()
v.set(0)
CalcWarnY = 48
Label(top, text="计量异常:").place(x=180,y=WorkStateY)
CalcWarn= ttk.Combobox(top)
CalcWarn.place(x=240,y=WorkStateY)
# 设置下拉菜单中的值为桩编号
CalcWarn['value'] = ['正常','电表飞走','电表倒走','订单负数','无起码','无止码']
# 设置默认值，即默认下拉框中的内容
CalcWarn.current(0)


# #告警
# warnstatey = 81
# warnbasex = 80
# Label(top, text = "告警:").place(x = 20,y = warnstatey)
# Checkbutton(top,text='继电器状态',variable=relay_state,width=8,background='gray').place(x = warnbasex,y = warnstatey)
# tk.Checkbutton(top,text='过压告警',variable=ov_warn,width=7,background='gray').place(x = warnbasex + 90,y = warnstatey)
# warnbasex += 90
# tk.Checkbutton(top,text='欠压告警',variable=uv_warn,width=7,background='gray').place(x = warnbasex + 83,y = warnstatey)
# warnbasex += 83
# tk.Checkbutton(top,text='缺相告警',variable=lp_warn, width=7,background='gray').place(x = warnbasex + 83,y = warnstatey)
# warnbasex += 83
# tk.Checkbutton(top,text='过流告警',variable=oc_warn, width=7,background='gray').place(x = warnbasex + 83,y = warnstatey)
# warnbasex += 83
# tk.Checkbutton(top,text='防雷器故障',variable=spd_error, width=8,background='gray').place(x=warnbasex + 83,y = warnstatey)
# warnbasex += 90
# tk.Checkbutton(top,text='急停故障',variable=scram_error, width=7,background='gray').place(x=warnbasex + 83,y = warnstatey)
# warnbasex = 81
# warnstatey = 114
# tk.Checkbutton(top,text='漏电保护',variable=leakage_elec, width=7,background='gray').place(x=warnbasex,y = warnstatey)
# tk.Checkbutton(top,text='卷筒故障',variable=drum_error, width=7,background='gray').place(x=warnbasex + 83,y = warnstatey)
# warnbasex += 83
# tk.Checkbutton(top,text='电表通讯故障',variable=meter_error, width=11,background='gray').place(x=warnbasex + 83,y = warnstatey)
# warnbasex += 83
# tk.Checkbutton(top,text='门禁故障',variable=access_error, width=7,background='gray').place(x=warnbasex + 111,y = warnstatey)
# warnbasex += 111
# tk.Checkbutton(top,text='过流故障',variable=oc_error, width=7,background='gray').place(x=warnbasex + 83,y = warnstatey)
# warnbasex += 83
# tk.Checkbutton(top,text='水浸故障',variable=water_error, width=7,background='gray').place(x=warnbasex + 83,y = warnstatey)
# warnbasex += 83
# tk.Checkbutton(top,text='倾倒故障',variable=dump_error, width=7,background='gray').place(x=warnbasex + 83,y = warnstatey)
# warnbasex = 81
# warnstatey = 147
# tk.Checkbutton(top,text='本船/桩体短路',variable=short_circuit, width=11,background='gray').place(x=warnbasex,y = warnstatey)
# tk.Checkbutton(top,text='母线短路',variable=m_short_circuit, width=7,background='gray').place(x=warnbasex + 111,y = warnstatey)
# warnbasex += 111
# tk.Checkbutton(top,text='母线开关输出继电器状态',variable=m_relay_state, width=19,background='gray').place(x=warnbasex + 83,y = warnstatey)
# warnbasex += 83
# tk.Checkbutton(top,text='母线开关连接确认状态',variable=m_switch_state, width=17,background='gray').place(x=warnbasex + 167,y = warnstatey)

if __name__ == "__main__":
    stake_port = db.OperatorDb(cf)
    STAKEID = []
    # 设置下拉菜单中的值为桩编号
    for it in stake_port:
        STAKEID.append(it[0])
    StakeNo['value'] = STAKEID
    # 设置默认值，即默认下拉框中的内容
    StakeNo.current(0)
    top.mainloop()

