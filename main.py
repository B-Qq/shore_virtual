import tkinter
from tkinter import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk # 导入ttk模块，因为下拉菜单控件在ttk中
import pymysql
import configparser
import sys
import struct


workstate = IntVar()
relay_state =  IntVar()
ov_warn = IntVar()
uv_warn = IntVar()
lp_warn = IntVar()
oc_warn = IntVar()
spd_error = IntVar()
scram_error = IntVar()
leakage_elec = IntVar()
drum_error = IntVar()
meter_error = IntVar()
access_error = IntVar()
oc_error = IntVar()
water_error = IntVar()
dump_error = IntVar()
short_circuit = IntVar()
m_short_circuit = IntVar()
m_relay_state = IntVar()
m_switch_state = IntVar()
DIST_FLAG = IntVar()
DIST_FLAG.set(0)


stake_port = []
STAKEID = []
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


#告警
warnstatey = 81
warnbasex = 80
Label(top, text = "告警:").place(x = 20,y = warnstatey)
Checkbutton(top,text='继电器状态',variable=relay_state,width=8,background='gray').place(x = warnbasex,y = warnstatey)
tk.Checkbutton(top,text='过压告警',variable=ov_warn,width=7,background='gray').place(x = warnbasex + 90,y = warnstatey)
warnbasex += 90
tk.Checkbutton(top,text='欠压告警',variable=uv_warn,width=7,background='gray').place(x = warnbasex + 83,y = warnstatey)
warnbasex += 83
tk.Checkbutton(top,text='缺相告警',variable=lp_warn, width=7,background='gray').place(x = warnbasex + 83,y = warnstatey)
warnbasex += 83
tk.Checkbutton(top,text='过流告警',variable=oc_warn, width=7,background='gray').place(x = warnbasex + 83,y = warnstatey)
warnbasex += 83
tk.Checkbutton(top,text='防雷器故障',variable=spd_error, width=8,background='gray').place(x=warnbasex + 83,y = warnstatey)
warnbasex += 90
tk.Checkbutton(top,text='急停故障',variable=scram_error, width=7,background='gray').place(x=warnbasex + 83,y = warnstatey)
warnbasex = 81
warnstatey = 114
tk.Checkbutton(top,text='漏电保护',variable=leakage_elec, width=7,background='gray').place(x=warnbasex,y = warnstatey)
tk.Checkbutton(top,text='卷筒故障',variable=drum_error, width=7,background='gray').place(x=warnbasex + 83,y = warnstatey)
warnbasex += 83
tk.Checkbutton(top,text='电表通讯故障',variable=meter_error, width=11,background='gray').place(x=warnbasex + 83,y = warnstatey)
warnbasex += 83
tk.Checkbutton(top,text='门禁故障',variable=access_error, width=7,background='gray').place(x=warnbasex + 111,y = warnstatey)
warnbasex += 111
tk.Checkbutton(top,text='过流故障',variable=oc_error, width=7,background='gray').place(x=warnbasex + 83,y = warnstatey)
warnbasex += 83
tk.Checkbutton(top,text='水浸故障',variable=water_error, width=7,background='gray').place(x=warnbasex + 83,y = warnstatey)
warnbasex += 83
tk.Checkbutton(top,text='倾倒故障',variable=dump_error, width=7,background='gray').place(x=warnbasex + 83,y = warnstatey)
warnbasex = 81
warnstatey = 147
tk.Checkbutton(top,text='本船/桩体短路',variable=short_circuit, width=11,background='gray').place(x=warnbasex,y = warnstatey)
tk.Checkbutton(top,text='母线短路',variable=m_short_circuit, width=7,background='gray').place(x=warnbasex + 111,y = warnstatey)
warnbasex += 111
tk.Checkbutton(top,text='母线开关输出继电器状态',variable=m_relay_state, width=19,background='gray').place(x=warnbasex + 83,y = warnstatey)
warnbasex += 83
tk.Checkbutton(top,text='母线开关连接确认状态',variable=m_switch_state, width=17,background='gray').place(x=warnbasex + 167,y = warnstatey)

#操作数据库获取桩号端口号
def OperatorDb():
    host = cf.get("DB", "Host")  # 数据库IP
    port = int(cf.get("DB", "Port"))  # 数据库端口号
    user = cf.get("DB", "User") # 用户名
    password = cf.get("DB", "Password")  # 密码
    db = cf.get("DB", "Db") # DB
    stationId = cf.get("STATION", "ID") #站号
    stationNum = "424090000"
    if (len(stationId) == 1): #拼接字符串 当站号位数不够时用0补齐
        station = stationNum + "0" + stationId
    else:
        station = stationNum + stationId

    print("StationId:",station)

    # 打开数据库连接
    db = pymysql.connect(host=host, user=user, password=password, db=db, port=port)
    # 使用cursor()方法获取操作游标
    cur = db.cursor()
    # 1.查询操作
    # 编写sql 查询语句  user 对应我的表名
    sql = "select ass.STAKE_NO ,po.chargeNo from (SELECT ASP.CHARGER_NO as chargeNo, ASP.STAKE_UUID as stake_uuid FROM ASSET_PORT ASP LEFT JOIN ASSET_STATION AST ON AST.UUID = ASP.STATION_UUID WHERE AST.STATION_NO = "+ station + ") as po left join asset_stake as ass on po.stake_uuid = ass.uuid order by STAKE_NO"
    try:
        cur.execute(sql)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        # 遍历结果
        for row in results:
            id = row[0]
            name = row[1]
            stake_port.append([row[0], row[1]])
            STAKEID.append(row[0])
    except Exception as e:
        raise e
    finally:
        db.close()  # 关闭连接
    print ("STAKE:PORT-->",stake_port)

if __name__ == "__main__":
    OperatorDb()
    # 设置下拉菜单中的值为桩编号
    StakeNo['value'] = STAKEID
    # 设置默认值，即默认下拉框中的内容
    StakeNo.current(0)
    top.mainloop()

