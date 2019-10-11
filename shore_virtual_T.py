#!/usr/bin/env python3
#-*- coding:gbk -*-

from socket import *
import sys
import time
import threading
import struct
import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox
import configparser
from tkinter import messagebox
import pymysql


#GUI
top = tk.Tk(className='��������վ�ڼ��ģ����')
top.geometry('700x550')
#�����ı���
ti = ScrolledText(top, width=95, height=24, background='#ffffff')
#ti.see(END);
ti.place(x=10,y=180)

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

#��ȡ�����ļ�
cf = configparser.ConfigParser()
cf.read('conf.ini')
HOST = cf.get("TCP", "Host")#ip
PORT = int(cf.get("TCP", "Port"))#�˿ں�
STATION = int(cf.get("STATION", "ID")) - 1
jian = int(cf.get("CALC", "Jian"))#��
feng = int(cf.get("CALC", "Feng"))#��
ping = int(cf.get("CALC", "Ping"))#ƽ
gu = int(cf.get("CALC", "Gu"))#��
zong = int(cf.get("CALC", "Zong"))#��
unit = int(cf.get("CALC", "Unit"))#��������
stake_port = []
send_all_status_tt = 0

#վ��
station_array = ['\x01','\x02','\x03','\x04','\x05','\x06','\x07','\x08'];
station_array_d = [0x01,0x02,0x03,0x04,0x05,0x06];

def destroy_top():
    time.sleep(6)
    top.destroy()

#��ȡʱ��
def get_time():
    return time.strftime('%H:%M:%S',time.localtime(time.time()))

#ʱ��ת��
def time_conver():
    s_time = time.strftime("%m%d%H%M%S", time.localtime())
    h_time = [0x00,0x00,0x00,0x00,0x00,0x00,0x00]
    h_time[5] = int(bytes.fromhex(s_time[0:2]).hex())
    h_time[4] = int(bytes.fromhex(s_time[2:4]).hex())
    h_time[3] = int(bytes.fromhex(s_time[4:6]).hex())
    h_time[2] = int(bytes.fromhex(s_time[6:8]).hex())
    sec = hex(int(s_time[8:10])*1000)
    sec = sec[2:6].zfill(4)
    h_time[1] = int('0x' + sec[0:2],16)
    h_time[0] = int('0x' + sec[2:4],16)
    h_time[6] = 0x13
    return h_time

#����ֵ����
def calc_calc_count(start,unit,count):
    result = clac_calc((start + unit*count))
    return result

def clac_calc(val):
    value = hex(val)
    result = [0x00,0x00,0x00,0x00]
    if(len(value) == 6):
        result[1] = int('0x' + value[2:4], 16)
        result[0] = int('0x' + value[4:6], 16)
        #for i in range(0,2):
        #   print ('0x%2x'%result[i])
    elif(len(value) == 7):
        result[2] = int('0x' + value[2], 16)
        result[1] = int('0x' + value[3:5], 16)
        result[0] = int('0x' + value[5:7], 16)
    elif (len(value) == 8):
        result[2] = int('0x' + value[2:4], 16)
        result[1] = int('0x' + value[4:6], 16)
        result[0] = int('0x' + value[6:8], 16)
    return result

#ң������
metet_unit = []
m_num = int(cf.get("METER","Num"))
for i in range(0,m_num):
    Ua = clac_calc(int(cf.get("METER", "Ua").split(";")[i])) + clac_calc(int(cf.get("METER", "Ub").split(";")[i])) + clac_calc(int(cf.get("METER", "Uc").split(";")[i]))
    Ua = Ua + clac_calc(int(cf.get("METER", "Ia").split(";")[i])) + clac_calc(int(cf.get("METER", "Ib").split(";")[i])) + clac_calc(int(cf.get("METER", "Ic").split(";")[i]))
    Ua = Ua + clac_calc(int(cf.get("METER", "Rate"))) + clac_calc(int(cf.get("METER", "Pp").split(";")[i])) + clac_calc(int(cf.get("METER", "Qp").split(";")[i])) + clac_calc(int(cf.get("METER", "Temp")))
    Ua = Ua + [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00];
    metet_unit.append(Ua)

#����
def send_calc_start(stake_no, port):
    calc_start = [0x68, 0x31, 0x00, 0x70, 0x00, 0x02, 0x00, 0x82, 0x85, 0x06, 0x00, 0x00, 0x08, 0x00, 0x00] + stake_no + port + [0x01]
    calc_start = calc_start + time_conver()
    calc_start = calc_start + calc_calc_count(jian, 0, 0)
    calc_start = calc_start + calc_calc_count(feng, 0, 0)
    calc_start = calc_start + calc_calc_count(ping, unit, 0)
    calc_start = calc_start + calc_calc_count(gu, 0, 0)
    calc_start = calc_start + calc_calc_count(zong, unit, 0)
    date = struct.pack("%dB" % (len(calc_start)), *calc_start)
    tctimeClient.send(date)
    time.sleep(0.01)

#ֹ��
def send_calc_end(stake_no, port,count):
    calc_end = [0x68, 0x31, 0x00, 0x70, 0x00, 0x02, 0x00, 0x82, 0x85, 0x06, 0x00, 0x00, 0x08, 0x00,0x00] + stake_no + port + [0x02]
    calc_end = calc_end + time_conver()
    calc_end = calc_end + calc_calc_count(jian, 0,count + 1)
    calc_end = calc_end + calc_calc_count(feng, 0, count + 1)
    calc_end = calc_end + calc_calc_count(ping, unit, count + 1)
    calc_end = calc_end + calc_calc_count(gu, 0, count + 1)
    calc_end = calc_end + calc_calc_count(zong, unit, count + 1)
    date = struct.pack("%dB" % (len(calc_end)), *calc_end)
    tctimeClient.send(date)
    time.sleep(0.01)

#������
def send_calc(stake_no,port,count):
    calc_end = [0x68, 0x30, 0x00, 0x74, 0x00, 0x02, 0x00, 0x86, 0x85, 0x01, 0x00, 0x00, 0x03, 0x00, 0x00] + stake_no + port
    calc_end = calc_end + time_conver()
    calc_end = calc_end + calc_calc_count(jian, 0, count + 1)
    calc_end = calc_end + calc_calc_count(feng, 0, count + 1)
    calc_end = calc_end + calc_calc_count(ping, unit, count + 1)
    calc_end = calc_end + calc_calc_count(gu, 0, count + 1)
    calc_end = calc_end + calc_calc_count(zong, unit, count + 1)
    date = struct.pack("%dB" % (len(calc_end)), *calc_end)
    tctimeClient.send(date)
    time.sleep(0.01)

def metet_send(stake_no,port,count):
    meter = [0x68, 0x58, 0x00, 0x7A, 0x00, 0x02, 0x00, 0x86, 0x85, 0x01, 0x00, 0x00, 0x02, 0x00, 0x00] + stake_no + port
    meter = meter + time_conver() + metet_unit[count % m_num]
    date = struct.pack("%dB" % (len(meter)), *meter)
    tctimeClient.send(date)
    time.sleep(0.01)

def signal_send(stake_no,port,type):
    yx = [0x68, 0x31, 0x00, 0x80, 0x00, 0x02, 0x00, 0x86, 0x89, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00] + stake_no + port
    if type == 2:
        yx = yx + time_conver() + [0x02, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    elif type == 3:
        yx = yx + time_conver() + [0x03, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    elif type == 5:
        yx = yx + time_conver() + [0x05, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                           0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    elif type == 0:
        yx = yx + time_conver() + [0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    date = struct.pack("%dB" % (len(yx)), *yx)
    tctimeClient.send(date)
    time.sleep(0.01)

stake_e = StringVar(top,value = '4240990100000012')
port_e = StringVar(top,value = '6')
Label(top, text="׮��:").place(x=170,y=16)
tk.Entry(top,bd =2,textvariable = stake_e).place(x=210,y=16)
Label(top, text="�˿ں�:").place(x=370,y=16)
tk.Entry(top,bd =2,textvariable = port_e).place(x=420,y=16)
text1 = Text(top, width = 5, height = 1)
text1.place(x=620,y=16)
#.place(x=610,y=16)
text1.insert(INSERT, "վ:" + str(STATION + 1))

def deviceStrToHexXX(deviceStr,devLen):
    deviceHex = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    if devLen == 16:
        deviceHex[0] = int('0x' + deviceStr[14:16], 16)
        deviceHex[1] = int('0x' + deviceStr[12:14], 16)
        deviceHex[2] = int('0x' + deviceStr[10:12], 16)
        deviceHex[3] = int('0x' + deviceStr[8:10], 16)
        deviceHex[4] = int('0x' + deviceStr[6:8], 16)
        deviceHex[5] = int('0x' + deviceStr[4:6], 16)
        deviceHex[6] = int('0x' + deviceStr[2:4], 16)
        deviceHex[7] = int('0x' + deviceStr[0:2], 16)
    if devLen == 1:
        deviceHex[0] = int(deviceStr)#intStrtoHex(deviceStr)
        print("1112312321:::::",intStrtoHex(deviceStr))
    print('1111',deviceHex)
    return deviceHex

def intStrtoHex(intstr):
    hex1 = (int(intstr)//16)*10 + int(intstr)%16
    return (hex1//16)*10 + (hex1%16)

def link_button():
    stake_no = str(stake_e.get())
    port = str(port_e.get())
    if len(stake_no) < 16:
        tk.messagebox.showerror('�������', '׮�ų��Ȳ���16λ')
        return
    elif len(stake_no) >16:
        tk.messagebox.showerror('�������', '׮�ų��ȴ���16λ')
        return
    if len(port) < 1:
        tk.messagebox.showerror('�������', '�˿ںų���С��1λ')
        return
    signal_send(deviceStrToHexXX(stake_no,len(stake_no)),[deviceStrToHexXX(port,len(port))[0]],2)
    ti.insert(END, get_time() + "+++������������\n")
    ti.see(END);

def free_button():
    stake_no = stake_e.get()
    port = port_e.get()
    if len(stake_no) < 16:
        tk.messagebox.showerror('�������', '׮�ų��Ȳ���16λ')
    elif len(stake_no) > 16:
        tk.messagebox.showerror('�������', '׮�ų��ȴ���16λ')
    if len(port) < 1:
        tk.messagebox.showerror('�������', '�˿ںų���С��1λ')
    signal_send(deviceStrToHexXX(stake_no,len(stake_no)),[deviceStrToHexXX(port,len(port))[0]],0)
    ti.insert(END, get_time() + "+++���ͶϿ�����\n")
    ti.see(END);

def start_distribution():
    while TRUE:
        #���ң��
        #d_yx = [0x68,0x31,0x00,0x54,0x00,0x00,0x00,0x87,0x8F,0x01,0x00,0x00,0x01,0x00,0x00] + [0x02,0x00,0x00,0x09,0x24,0x04,0x00,0x00] + time_conver()
        #d_yx = d_yx + [0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01,0x01]
        #date = struct.pack("%dB" % (len(d_yx)), *d_yx)
        #tctimeClient.send(date)
        #time.sleep(0.01)
        #������
        if DIST_FLAG.get() == 1 :
            d_jl = [0x68,0x2F,0x00,0x54,0x00,0x00,0x00,0x87,0x8f,0x01,0x00,0x00,0x03,0x00,0x00] + [0x02,0x00,0x00,0x09,0x24,0x04,0x00,0x00] + time_conver()
            d_jl = d_jl + [0x02,0x00,0x00,0x00,0x05,0x00,0x00,0x00,0x06,0x00,0x00,0x00,0x07,0x00,0x00,0x00,0x08,0x00,0x00,0x00]
            date = struct.pack("%dB" % (len(d_jl)), *d_jl)
            tctimeClient.send(date)
            time.sleep(0.01)
            d_yc = [0x68,0x77,0x00,0xA6,0x05,0x02,0x00,0x87,0x8F,0x01,0x00,0x00,0x02,0x00,0x00] + [0x02,0x00,0x00,0x09,0x24,0x04,0x00,0x00] + time_conver()
            d_yc = d_yc + [0x94,0x11,0x00,0x00,0x4C,0x04,0x00,0x00,0x58,0x02,0x00,0x00,0xB0,0x04,0x00,0x00,0xBC,0x02,0x00,0x00,0xF4,0x01,0x00,0x00,0x14,0x05,0x00,0x00,0xFC,0x08,0x00,0x00,0x84,0x03,0x00,0x00,0x60,0x09,0x00,0x00,0x4C,0x04,0x00,0x00,0x4C,0x04,0x00,0x00,0x80,0x0C,0x00,0x00,0x14,0x05,0x00,0x00,0x08,0x07,0x00,0x00,0x01,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x05,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x02,0x00,0x00,0x00,0x03,0x00,0x00,0x00,0x04,0x00,0x00,0x00,0x04,0x00,0x00,0x00]
            date = struct.pack("%dB" % (len(d_yc)), *d_yc)
            tctimeClient.send(date)
            time.sleep(0.01)
            time.sleep(6);

def send_signals():
    stake_no = str(stake_e.get())
    port = str(port_e.get())
    print('port>>>',deviceStrToHexXX(port,1))
    ti.insert(END, get_time() + "+++SEND����ң������\n")
    ti.see(END);
    yx = [0x68, 0x31, 0x00, 0x80, 0x00, 0x02, 0x00, 0x86, 0x89, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00] + deviceStrToHexXX(stake_no,len(stake_no)) + [deviceStrToHexXX(port,1)[0]]
    yx = yx + time_conver() + [int('0x' + str(workstate.get()),16)] + [0x00,0x01] + [int('0x' + str(relay_state.get()),16)]\
        + [int('0x' + str(ov_warn.get()),16)] + [int('0x' + str(uv_warn.get()),16)] + [int('0x' + str(lp_warn.get()),16)] + \
         [int('0x' + str(oc_warn.get()), 16)] + [int('0x' + str(spd_error.get()),16)] + [int('0x' + str(scram_error.get()),16)] + \
         [int('0x' + str(leakage_elec.get()), 16)] + [int('0x' + str(drum_error.get()),16)] + [int('0x' + str(meter_error.get()),16)] + \
         [int('0x' + str(access_error.get()), 16)] + [int('0x' + str(oc_error.get()),16)] + [int('0x' + str(water_error.get()),16)] + \
         [int('0x' + str(dump_error.get()), 16)] + [int('0x' + str(short_circuit.get()),16)] + [int('0x' + str(m_short_circuit.get()),16)] + \
         [int('0x' + str(m_relay_state.get()), 16)] + [int('0x' + str(m_switch_state.get()),16)]
    date = struct.pack("%dB" % (len(yx)), *yx)
    tctimeClient.send(date)
    time.sleep(0.01)

def heatbeatrequest():
    heartbeat = [0x68, 0x04, 0x00, 0x43, 0x00, 0x00, 0x00]
    date = struct.pack("%dB" % (len(heartbeat)), *heartbeat)
    tctimeClient.send(date)
    time.sleep(0.01)
    ti.insert(END, get_time() + "+++������������\n")
    ti.see(END);

def heatbeatrespone():
    heartbeat = [0x68, 0x04, 0x00, 0x83, 0x00, 0x00, 0x00]
    date = struct.pack("%dB" % (len(heartbeat)), *heartbeat)
    tctimeClient.send(date)
    time.sleep(0.01)
    ti.insert(END, get_time() + "+++����������Ӧ\n")
    ti.see(END);

def select_all():
    state = 1
    workstate.set(state)
    relay_state.set(state)
    ov_warn.set(state)
    uv_warn.set(state)
    lp_warn.set(state)
    oc_warn.set(state)
    spd_error.set(state)
    scram_error.set(state)
    leakage_elec.set(state)
    drum_error.set(state)
    meter_error.set(state)
    access_error.set(state)
    oc_error.set(state)
    water_error.set(state)
    dump_error.set(state)
    short_circuit.set(state)
    m_short_circuit.set(state)
    m_relay_state.set(state)
    m_switch_state.set(state)

def no_select_all():
    state = 0
    workstate.set(state)
    relay_state.set(state)
    ov_warn.set(state)
    uv_warn.set(state)
    lp_warn.set(state)
    oc_warn.set(state)
    spd_error.set(state)
    scram_error.set(state)
    leakage_elec.set(state)
    drum_error.set(state)
    meter_error.set(state)
    access_error.set(state)
    oc_error.set(state)
    water_error.set(state)
    dump_error.set(state)
    short_circuit.set(state)
    m_short_circuit.set(state)
    m_relay_state.set(state)
    m_switch_state.set(state)

def warn_end():
    d_yx = [0x68, 0x31, 0x00, 0x54, 0x00, 0x00, 0x00, 0x87, 0x8F, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00] + [0x02,0x00, 0x00,0x09,0x24,0x04,0x00,0x00] + time_conver()
    d_yx = d_yx + [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    date = struct.pack("%dB" % (len(d_yx)), *d_yx)
    tctimeClient.send(date)
    time.sleep(0.01)
def warn_start():
    d_yx = [0x68, 0x31, 0x00, 0x54, 0x00, 0x00, 0x00, 0x87, 0x8F, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00] + [0x02,0x00, 0x00,0x09,0x24,0x04,0x00,0x00] + time_conver()
    d_yx = d_yx + [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01]
    date = struct.pack("%dB" % (len(d_yx)), *d_yx)
    tctimeClient.send(date)
    time.sleep(0.01)

def dist_1():
    DIST_FLAG.set(1)

def dist_0():
    DIST_FLAG.set(0)

tk.Button(top,text='��������',command=link_button,width=8,background='blue').place(x=20,y=16)
tk.Button(top,text='�Ͽ�����',command=free_button,width=8,background='red').place(x=100,y=16)
tk.Button(top,text='SEND',command=send_signals,width=6,height=3,background='yellow').place(x=20,y=110)
tk.Button(top,text='������������',command=heatbeatrequest,width=11,background='yellow').place(x=20,y=510)
tk.Button(top,text='����������Ӧ',command=heatbeatrespone,width=11,background='yellow').place(x=585,y=510)
tk.Radiobutton(top,text='ȫѡ',variable=workstate, value=1,command=select_all,width=4,background='pink').place(x=250,y=510)
tk.Radiobutton(top,text='��ѡ',variable=workstate, value=2,command=no_select_all,width=4,background='pink').place(x=310,y=510)
tk.Radiobutton(top,text='��1',variable=DIST_FLAG, value=1,command=dist_1,width=4,background='blue').place(x=120,y=510)
tk.Radiobutton(top,text='��0',variable=DIST_FLAG, value=0,command=dist_0,width=4,background='blue').place(x=180,y=510)
tk.Button(top,text='���澯ȡ��',command=warn_end,width=12,background='red').place(x=470,y=510)
tk.Button(top,text='���澯����',command=warn_start,width=11,background='blue').place(x=390,y=510)

def send_all_status_t():
    for it in stake_port:
        stake_no_a = deviceStrToHexXX(it[0], len(it[0]))  # ׮��
        signal_send(stake_no_a, [deviceStrToHexXX(it[1], len(it[1]))[0]], 2)
    ti.insert(END, get_time() + "��������׮״̬���\n")
    ti.see(END);

def send_all_status():
    ti.insert(END, get_time() + ".......����׮״̬�� ��ȴ� ��.....................\n")
    ti.see(END);
    time.sleep(0.01)
    send_all_status_tt = threading.Thread(target=send_all_status_t(),name='send_all_status_t')
    send_all_status_tt.start()

#����״̬
v = IntVar()
v.set(0)
workstatey = 48
Label(top, text="����״̬:").place(x=20,y=workstatey)
tk.Radiobutton(top,text='����',variable=workstate, value=2,width=4,background='green').place(x=80,y=workstatey)
tk.Radiobutton(top,text='����',variable=workstate, value=3,width=4,background='green').place(x=140,y=workstatey)
tk.Radiobutton(top,text='���',variable=workstate, value=5,width=4,background='green').place(x=200,y=workstatey)
tk.Radiobutton(top,text='�澯',variable=workstate, value=1,width=4,background='green').place(x=260,y=workstatey)
tk.Radiobutton(top,text='����',variable=workstate, value=4,width=4,background='green').place(x=320,y=workstatey)
tk.Button(top,text='����״̬(ȫ)',command=send_all_status,width=28,background='red').place(x=450,y=workstatey)

#�澯
warnstatey = 81
warnbasex = 80
Label(top, text = "�澯:").place(x = 20,y = warnstatey)
Checkbutton(top,text='�̵���״̬',variable=relay_state,width=8,background='gray').place(x = warnbasex,y = warnstatey)
tk.Checkbutton(top,text='��ѹ�澯',variable=ov_warn,width=7,background='gray').place(x = warnbasex + 90,y = warnstatey)
warnbasex += 90
tk.Checkbutton(top,text='Ƿѹ�澯',variable=uv_warn,width=7,background='gray').place(x = warnbasex + 83,y = warnstatey)
warnbasex += 83
tk.Checkbutton(top,text='ȱ��澯',variable=lp_warn, width=7,background='gray').place(x = warnbasex + 83,y = warnstatey)
warnbasex += 83
tk.Checkbutton(top,text='�����澯',variable=oc_warn, width=7,background='gray').place(x = warnbasex + 83,y = warnstatey)
warnbasex += 83
tk.Checkbutton(top,text='����������',variable=spd_error, width=8,background='gray').place(x=warnbasex + 83,y = warnstatey)
warnbasex += 90
tk.Checkbutton(top,text='��ͣ����',variable=scram_error, width=7,background='gray').place(x=warnbasex + 83,y = warnstatey)
warnbasex = 81
warnstatey = 114
tk.Checkbutton(top,text='©�籣��',variable=leakage_elec, width=7,background='gray').place(x=warnbasex,y = warnstatey)
tk.Checkbutton(top,text='��Ͳ����',variable=drum_error, width=7,background='gray').place(x=warnbasex + 83,y = warnstatey)
warnbasex += 83
tk.Checkbutton(top,text='���ͨѶ����',variable=meter_error, width=11,background='gray').place(x=warnbasex + 83,y = warnstatey)
warnbasex += 83
tk.Checkbutton(top,text='�Ž�����',variable=access_error, width=7,background='gray').place(x=warnbasex + 111,y = warnstatey)
warnbasex += 111
tk.Checkbutton(top,text='��������',variable=oc_error, width=7,background='gray').place(x=warnbasex + 83,y = warnstatey)
warnbasex += 83
tk.Checkbutton(top,text='ˮ������',variable=water_error, width=7,background='gray').place(x=warnbasex + 83,y = warnstatey)
warnbasex += 83
tk.Checkbutton(top,text='�㵹����',variable=dump_error, width=7,background='gray').place(x=warnbasex + 83,y = warnstatey)
warnbasex = 81
warnstatey = 147
tk.Checkbutton(top,text='����/׮���·',variable=short_circuit, width=11,background='gray').place(x=warnbasex,y = warnstatey)
tk.Checkbutton(top,text='ĸ�߶�·',variable=m_short_circuit, width=7,background='gray').place(x=warnbasex + 111,y = warnstatey)
warnbasex += 111
tk.Checkbutton(top,text='ĸ�߿�������̵���״̬',variable=m_relay_state, width=19,background='gray').place(x=warnbasex + 83,y = warnstatey)
warnbasex += 83
tk.Checkbutton(top,text='ĸ�߿�������ȷ��״̬',variable=m_switch_state, width=17,background='gray').place(x=warnbasex + 167,y = warnstatey)

#T����
class shore_T():
    #����
    def __init__(self,deviceId,t_id,port):
        self.deivceId = deviceId
        self.t_id = t_id
        self.port = port
        self.flag = TRUE
        self.count = 0

    #����ң������
    def charge_send(self):
        #self.count = 0
        self.flag = TRUE
        while True:
            time.sleep(5)
            if self.flag:
                metet_send(self.deivceId, self.t_id, self.count)
                ti.insert(END, get_time() + "+++>>T����" + str(self.deivceId) + str(self.t_id) + "����ң������\n")
                ti.see(END);
                #T����
                send_calc(self.deivceId, self.t_id, self.count)
                ti.insert(END,get_time() + "+++>>T����" + str(self.deivceId) + str(self.t_id) + "���ͳ���м�������\n")
                ti.see(END);
                if self.port[0] < 10:
                    send_calc(self.deivceId , self.port, self.count)
                    ti.insert(END, get_time() + "+++>>T����(׮)" + str(self.deivceId) + str(self.port) + "���ͳ���м�������\n")
                    ti.see(END);
                    metet_send(self.deivceId,self.port,self.count)
                    ti.insert(END,get_time() + "+++>>T����(׮)" + str(self.deivceId) + str(self.port) + "����ң������\n")
                    ti.see(END);
                self.count = self.count + 1
            else:
                break;
     #�����̷߳�������
    def calcThreadStart(self):
        self.ThreadStart = threading.Thread(target=self.charge_send,name='charge_send')
        self.ThreadStart.start()
    def calcStop(self):
        self.flag = FALSE
        self.count = 0
    def calcThreadStop(self):
        self.ThreadStop = threading.Thread(target=self.send_calcend, name='send_calcend')
        self.ThreadStop.start()
    def send_calcend(self):
        count = self.count
        self.calcStop()
        time.sleep(6)
        send_calc_end(self.deivceId, self.t_id, count)
        ti.insert(END, get_time() + "#######>>T����" + str(self.deivceId) + str(self.t_id) + "����ֹ��\n")
        ti.see(END);
        signal_send(self.deivceId, self.t_id, 5)
        ti.insert(END, get_time() + "#######>>T����" + str(self.deivceId) + str(self.t_id) + "����ң�����\n")
        ti.see(END);
        if (self.port[0] < 10):
            # ֹ��T��
            send_calc_end(self.deivceId, self.port, count)
            ti.insert(END, get_time() + "#######>>T����(׮)" + str(self.deivceId) + str(self.port) + "����ֹ��\n")
            ti.see(END);
            signal_send(self.deivceId, self.port, 5)
            ti.insert(END, get_time() + "#######>>T����(׮)" + str(self.deivceId) + str(self.port) + "����ң�����\n")
            ti.see(END);

# ����׮
class shore():
    # ����
    def __init__(self, deviceId,port):
        self.deivceId = deviceId
        self.port = port
        self.flag = TRUE
        self.count = 0

    # ����ң������
    def charge_send(self):
        self.count = 0
        self.flag = TRUE
        while True:
            time.sleep(5)
            if self.flag:
                metet_send(self.deivceId, self.port, self.count)
                ti.insert(END, get_time() + "+++>>�ӵ���" + str(self.deivceId) + str(self.port) + "����ң������\n")
                ti.see(END);
                # T����
                send_calc(self.deivceId, self.port, self.count)
                ti.insert(END, get_time() + "+++>>�ӵ���" + str(self.deivceId) + str(self.port) + "���ͳ���м�������\n")
                ti.see(END);
                self.count = self.count + 1
            else:
                break;
                # �����̷߳�������

    def calcThreadStart(self):
        self.ThreadStart = threading.Thread(target=self.charge_send, name='charge_send')
        self.ThreadStart.start()

    def calcStop(self):
        self.flag = FALSE
        self.count = 0

    def calcThreadStop(self):
        self.ThreadStop = threading.Thread(target=self.send_calcend, name='send_calcend')
        self.ThreadStop.start()

    def send_calcend(self):
        count = self.count
        self.calcStop()
        time.sleep(6)
        send_calc_end(self.deivceId, self.port, count)
        ti.insert(END, get_time() + "#######>>�ӵ���" + str(self.deivceId) + str(self.port) + "����ֹ��\n")
        ti.see(END);
        signal_send(self.deivceId, self.port, 5)
        ti.insert(END, get_time() + "#######>>�ӵ���" + str(self.deivceId) + str(self.port) + "����ң�����\n")
        ti.see(END);

#����tcp����
tctimeClient = socket(AF_INET, SOCK_STREAM)
BUFFSIZE=204800
def tcp_init():
    _rf = 0
    ADDR = (HOST,PORT)
    try:
        _rf = tctimeClient.connect(ADDR)
    except Exception as err:
        ti.insert(END, "����ǰ�û�ʧ��,����ip��ַ���˿������Ƿ���ȷ\n")
        ti.see(END);
        top_destroy = threading.Thread(target=destroy_top, name='destroy_top')
        top_destroy.start()
        top.mainloop()
        exit()
    if _rf != 0:
        ti.insert(END, "����ǰ�û��ɹ�:\n   --->IP��ַΪ" + str(HOST) + "\n   --->�˿�Ϊ" + str(PORT)+ "\n")
        ti.see(END);

def deviceStrToHex(deviceStr):
    deviceHex = [0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00];
    print(deviceStr[0])
    print(deviceStr[1])
    deviceHex[0] = int(str(hex(deviceStr[0])), 16)
    deviceHex[1] = int(str(hex(deviceStr[1])), 16)
    deviceHex[2] = int(str(hex(deviceStr[2])), 16)
    deviceHex[3] = int(str(hex(deviceStr[3])), 16)
    deviceHex[4] = int(str(hex(deviceStr[4])), 16)
    deviceHex[5] = int(str(hex(deviceStr[5])), 16)
    deviceHex[6] = int(str(hex(deviceStr[6])), 16)
    deviceHex[7] = int(str(hex(deviceStr[7])), 16)
    return deviceHex

def start_recv():
    stake_no = [];
    t_id = [];
    port = [];
    t_start_elec = {};
    while (1):
        recv = tctimeClient.recv(BUFFSIZE)
        if (len(recv) >= 25):
            stake_no = deviceStrToHex(recv[15:23]) #׮��
            t_id = [int(str(hex(recv[24])), 16)] #T��ID
            port = [int(str(hex(recv[23])), 16)] #�˿ں�
            print('stake_no:',stake_no)
            #T�ӹ���
            if (len(recv) == 26):
                #��������
                if (not (str(int(recv[15:23].hex())) + str(recv[23]) + str(recv[24]) in t_start_elec) ):
                    print(get_time() + '----- new T�ӹ���')
                    t_start_elec[str(int(recv[15:23].hex())) + str(recv[23]) + str(recv[24])] = shore_T(stake_no, t_id, port)
                if ((recv[7] == 0x85) & (recv[12] == 0x08) & (recv[13] == 0x00) & (recv[14] == 0x00) & (recv[25] == 0x01)):
                    ti.insert(END, get_time() + "<<<#######����T�ӹ���ָ��\n")
                    ti.see(END);
                    control_start = [0x68, 0x18, 0x00, 0xAA, 0x02, 0x02, 0x00, 0x82, 0x10, 0x07, 0x00, 0x00, 0x0A, 0x00,
                                     0x00] + stake_no + port + t_id + [0x01, 0x00]
                    date = struct.pack("%dB" % (len(control_start)), *control_start)
                    tctimeClient.send(date)
                    time.sleep(0.01)
                    ti.insert(END, get_time() + "#######>>T����" + str(recv[15:24].hex()) + "���͹���ȷ��\n")
                    ti.see(END);
                    ti.see(END);
                    # #����T��
                    send_calc_start(stake_no,t_id)
                    ti.insert(END, get_time() + "#######>>T����" + str(recv[15:24].hex()) + "��������\n")
                    ti.see(END);
                    signal_send(stake_no,t_id,3)
                    ti.insert(END, get_time() + "#######>>T����" + str(recv[15:24].hex()) + "����ң�Ź�����\n")
                    ti.see(END);
                    if port[0] < 10:
                        send_calc_start(stake_no, port)
                        ti.insert(END, get_time() + "#######>>T����(׮)" + str(recv[15:24].hex()) + "��������\n")
                        ti.see(END);
                        signal_send(stake_no, port, 3)
                        ti.insert(END, get_time() + "#######>>T����" + str(recv[15:24].hex()) + "����ң�Ź�����\n")
                        ti.see(END);
                    t_start_elec[str(int(recv[15:23].hex())) + str(recv[23]) + str(recv[24])].calcThreadStart()
                # T�Ӷϵ�
                elif ((recv[7] == 0x85) & (recv[12] == 0x08) & (recv[13] == 0x00) & (recv[14] == 0x00) & (recv[25] == 0x02)):
                    ti.insert(END, get_time() + "<<<#######����T�Ӷϵ�ָ��\n")
                    ti.see(END);
                    control_end = [0x68, 0x18, 0x00, 0xAA, 0x02, 0x02, 0x00, 0x82, 0x10, 0x07, 0x00, 0x00, 0x0A, 0x00,
                                   0x00] + stake_no + port + t_id + [0x02, 0x00]
                    date = struct.pack("%dB" % (len(control_end)), *control_end)
                    tctimeClient.send(date)
                    time.sleep(0.01)
                    ti.insert(END, get_time() + "#######>>T����" + str(recv[15:24].hex()) + "���Ͷϵ�ȷ��\n")
                    ti.see(END);
                    t_start_elec[str(int(recv[15:23].hex())) + str(recv[23]) + str(recv[24])].calcThreadStop()
            # ֱ������
            if (len(recv) == 25):
                if (not (str(int(recv[15:23].hex())) + str(recv[23]) in t_start_elec) ):
                    print(get_time() + '----- new ֱ������')
                    t_start_elec[str(int(recv[15:23].hex())) + str(recv[23])] = shore(stake_no, port)
                if ((recv[7] == 0x85) & (recv[12] == 0x05) & (recv[13] == 0x00) & (recv[14] == 0x00) & (recv[24] == 0x01)):
                    ti.insert(END, get_time() + "<<<#######����ֱ������ָ��\n")
                    ti.see(END);
                    control_start = [0x68, 0x17, 0x00, 0xAA, 0x02, 0x02, 0x00, 0x82, 0x10, 0x07, 0x00, 0x00, 0x07, 0x00,
                                     0x00] + stake_no + port + [0x01, 0x00]
                    date = struct.pack("%dB" % (len(control_start)), *control_start)
                    tctimeClient.send(date)
                    time.sleep(0.01)
                    ti.insert(END, get_time()  + "#######>>�ӵ���" + str(recv[15:24].hex()) + "���͹���ȷ��\n")
                    ti.see(END);
                    # #����ֱ��
                    send_calc_start(stake_no, port)
                    ti.insert(END, get_time() + "#######>>T����" + str(recv[15:24].hex()) + "��������\n")
                    ti.see(END);
                    signal_send(stake_no, port, 3)
                    ti.insert(END, get_time() + "#######>>T����" + str(recv[15:24].hex()) + "����ң�Ź�����\n")
                    ti.see(END);
                    t_start_elec[str(int(recv[15:23].hex())) + str(recv[23])].calcThreadStart()

                # ֱ���ϵ�
                elif ((recv[7] == 0x85) & (recv[12] == 0x05) & (recv[13] == 0x00) & (recv[14] == 0x00) & (recv[24] == 0x02)):
                    ti.insert(END, get_time() + "<<<#######����ֱ���ϵ�ָ��\n")
                    ti.see(END);
                    control_end = [0x68, 0x17, 0x00, 0xAA, 0x02, 0x02, 0x00, 0x82, 0x10, 0x07, 0x00, 0x00, 0x07, 0x00,
                                   0x00] + stake_no + port + [0x02, 0x00]
                    date = struct.pack("%dB" % (len(control_end)), *control_end)
                    tctimeClient.send(date)
                    time.sleep(0.01)
                    ti.insert(END, get_time() + "#######>>�ӵ���" + str(recv[15:24].hex()) + "���Ͷϵ�ȷ��\n")
                    ti.see(END);
                    t_start_elec[str(int(recv[15:23].hex())) + str(recv[23])].calcThreadStop()
        if len(recv) == 7:
            if recv[3] == 0x43:
                hbrespone = [0x68, 0x04, 0x00, 0x83, 0x00, 0x00, 0x00]
                date = struct.pack("%dB" % (len(hbrespone)), *hbrespone)
                tctimeClient.send(date)
                time.sleep(0.01)
                ti.insert(END, get_time() + "#######>>����֡��Ӧ\n")
                ti.see(END);
def on_closing():
    if messagebox.askokcancel("�˳�", "����Ҫ�˳�������?"):
        tctimeClient.close()
        top.destroy()

def OperatorDb():
    host = cf.get("DB", "Host")  # ip
    port = int(cf.get("DB", "Port"))  # �˿ں�
    user = cf.get("DB", "User") # user
    password = cf.get("DB", "Password")  # password
    db = cf.get("DB", "Db") # db
    stationId = cf.get("STATION", "ID")
    stationNum = "424090000"
    if (len(stationId) == 1):
        station = stationNum + "0" + stationId
    else:
        station = stationNum + stationId

    print(station)

    # �����ݿ�����
    db = pymysql.connect(host=host, user=user, password=password, db=db, port=port)
    # ʹ��cursor()������ȡ�����α�
    cur = db.cursor()
    # 1.��ѯ����
    # ��дsql ��ѯ���  user ��Ӧ�ҵı���
    sql = "select ass.STAKE_NO ,po.chargeNo from (SELECT ASP.CHARGER_NO as chargeNo, ASP.STAKE_UUID as stake_uuid FROM ASSET_PORT ASP LEFT JOIN ASSET_STATION AST ON AST.UUID = ASP.STATION_UUID WHERE AST.STATION_NO = "+ station + ") as po left join asset_stake as ass on po.stake_uuid = ass.uuid order by STAKE_NO"
    try:
        cur.execute(sql)  # ִ��sql���
        results = cur.fetchall()  # ��ȡ��ѯ�����м�¼
        print("id", "name", "password")
        # �������
        for row in results:
            id = row[0]
            name = row[1]
            stake_port.append([row[0], row[1]]);
            #password = row[2]
            #print(id, name)
    except Exception as e:
        raise e
    finally:
        db.close()  # �ر�����
    print (stake_port)

if __name__ == '__main__':
    tcp_init()
    protocol = '\x68\x02' + station_array[STATION] + '\x00\x00\x09\x24\x04\x00\x00\x00\x00'  # ���վ�ڼ��
    tctimeClient.send(protocol.encode())
    t_recv = threading.Thread(target=start_recv, name='start_recv')
    t_recv.start()
    t_distribution = threading.Thread(target=start_distribution,name='start_distribution')
    t_distribution.start();
    top.protocol("WM_DELETE_WINDOW", on_closing)
    OperatorDb();
    top.mainloop()