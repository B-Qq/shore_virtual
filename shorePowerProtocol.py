from socket import *
import threading
import time
from tkinter import *
import struct
import tkinter as tk
from shore import *
from shoreT import *

station_array = ['\x00','\x01','\x02','\x03','\x04','\x05','\x06','\x07','\x08'];
BUFFSIZE=204800

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

#获取时间
def get_time():
    return time.strftime('%H:%M:%S',time.localtime(time.time()))

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
        #print("1112312321:::::",intStrtoHex(deviceStr))
    #print('1111',deviceHex)
    return deviceHex

def deviceStrToProtocol(deviceStr):
    device = deviceStr[14:16]
    device += deviceStr[12:14]
    device += deviceStr[10:12]
    device += deviceStr[8:10]
    device += deviceStr[6:8]
    device += deviceStr[4:6]
    device += deviceStr[2:4]
    device += deviceStr[0:2]
    return str(int(device))

def intStrtoHex(intstr):
    hex1 = (int(intstr)//16)*10 + int(intstr)%16
    return (hex1//16)*10 + (hex1%16)

class shorePowerProtocol(object):
    #socket套接字,站号,配置文件,滚动文本框
    def __init__(self,tcpClient,StationId,cf,tk):
        self.tcpClient = tcpClient
        self.cf = cf
        self.ti = tk.getScrolledText()
        self.tk = tk
        self.jian = int(cf.get("CALC", "Jian"))  # 尖
        self.feng = int(cf.get("CALC", "Feng"))  # 峰
        self.ping = int(cf.get("CALC", "Ping"))  # 平
        self.gu = int(cf.get("CALC", "Gu"))  # 谷
        self.zong = int(cf.get("CALC", "Zong"))  # 总
        self.unit = int(cf.get("CALC", "Unit"))  # 增长幅度
        self.m_num = int(self.cf.get("METER", "Num"))
        self.protocolInit(StationId)
        self.protocolRecv()
        threading.Thread(target=self.start_distribution, name='start_distribution').start()

    #协议初始化,发送协议标识帧
    def protocolInit(self,StationId):
        protocol = '\x68\x02' + station_array[StationId] + '\x00\x00\x09\x24\x04\x00\x00\x00\x00'  # 发送协议标识帧
        self.tcpClient.send(protocol.encode())

    def protocolRecv(self):
        p_recv = threading.Thread(target=self.start_recv, name='start_recv').start()

    #数据计算
    def clac_calc(self,val):
        value = hex(val)
        result = [0x00, 0x00, 0x00, 0x00]
        if (len(value) == 6):
            result[1] = int('0x' + value[2:4], 16)
            result[0] = int('0x' + value[4:6], 16)
            # for i in range(0,2):
            #   print ('0x%2x'%result[i])
        elif (len(value) == 7):
            result[2] = int('0x' + value[2], 16)
            result[1] = int('0x' + value[3:5], 16)
            result[0] = int('0x' + value[5:7], 16)
        elif (len(value) == 8):
            result[2] = int('0x' + value[2:4], 16)
            result[1] = int('0x' + value[4:6], 16)
            result[0] = int('0x' + value[6:8], 16)
        return result

    # 遥测数据拼接
    def memterValue(self):
        metet_unit = []
        for i in range(0, self.m_num):
            Meter = self.clac_calc(int(self.cf.get("METER", "Ua").split(";")[i])) + self.clac_calc(
                int(self.cf.get("METER", "Ub").split(";")[i])) + self.clac_calc(int(self.cf.get("METER", "Uc").split(";")[i]))
            Meter = Meter + self.clac_calc(int(self.cf.get("METER", "Ia").split(";")[i])) + self.clac_calc(
                int(self.cf.get("METER", "Ib").split(";")[i])) + self.clac_calc(int(self.cf.get("METER", "Ic").split(";")[i]))
            Meter = Meter + self.clac_calc(int(self.cf.get("METER", "Rate"))) + self.clac_calc(
                int(self.cf.get("METER", "Pp").split(";")[i])) + self.clac_calc(
                int(self.cf.get("METER", "Qp").split(";")[i])) + self.clac_calc(int(self.cf.get("METER", "Temp")))
            Meter = Meter + [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                       0x00, 0x00, 0x00, 0x00];
            metet_unit.append(Meter)
        return metet_unit

    #遥测报文拼接并发送
    def metet_send(self,stake_no, port, count):
        meter = [0x68, 0x58, 0x00, 0x7A, 0x00, 0x02, 0x00, 0x86, 0x85, 0x01, 0x00, 0x00, 0x02, 0x00,
                 0x00] + stake_no + port
        # meterValue = self.memterValue
        meter = meter + self.time_conver() + self.memterValue()[count % self.m_num]
        date = struct.pack("%dB" % (len(meter)), *meter)
        self.tcpClient.send(date)
        time.sleep(0.01)

    # 计量值计算
    def calc_calc_count(self,start, unit, count):
        result = self.clac_calc((start + unit * count))
        return result

    #发送起码
    def send_calc_start(self,stake_no, port):
        calc_start = [0x68, 0x31, 0x00, 0x70, 0x00, 0x02, 0x00, 0x82, 0x85, 0x06, 0x00, 0x00, 0x08, 0x00,
                      0x00] + stake_no + port + [0x01]
        calc_start = calc_start + self.time_conver()
        calc_start = calc_start + self.calc_calc_count(self.jian, 0, 0)
        calc_start = calc_start + self.calc_calc_count(self.feng, 0, 0)
        calc_start = calc_start + self.calc_calc_count(self.ping, self.unit, 0)
        calc_start = calc_start + self.calc_calc_count(self.gu, 0, 0)
        calc_start = calc_start + self.calc_calc_count(self.zong, self.unit, 0)
        date = struct.pack("%dB" % (len(calc_start)), *calc_start)
        self.tcpClient.send(date)
        time.sleep(0.01)

    #发送供电中计量数据
    def send_calc(self,stake_no,port,count):
        calc_end = [0x68, 0x30, 0x00, 0x74, 0x00, 0x02, 0x00, 0x86, 0x85, 0x01, 0x00, 0x00, 0x03, 0x00,
                    0x00] + stake_no + port
        calc_end = calc_end + self.time_conver()
        calc_end = calc_end + self.calc_calc_count(self.jian, 0, count + 1)
        calc_end = calc_end + self.calc_calc_count(self.feng, 0, count + 1)
        calc_end = calc_end + self.calc_calc_count(self.ping, self.unit, count + 1)
        calc_end = calc_end + self.calc_calc_count(self.gu, 0, count + 1)
        calc_end = calc_end + self.calc_calc_count(self.zong, self.unit, count + 1)
        date = struct.pack("%dB" % (len(calc_end)), *calc_end)
        self.tcpClient.send(date)
        time.sleep(0.01)

    #发送异常计量数据
    def send_calc_exception(self,stake_no, port, count,setZong):
        calc_end = [0x68, 0x30, 0x00, 0x74, 0x00, 0x02, 0x00, 0x86, 0x85, 0x01, 0x00, 0x00, 0x03, 0x00,
                    0x00] + stake_no + port
        calc_end = calc_end + self.time_conver()
        calc_end = calc_end + self.calc_calc_count(self.jian, 0, count + 1)
        calc_end = calc_end + self.calc_calc_count(self.feng, 0, count + 1)
        calc_end = calc_end + self.calc_calc_count(self.ping, self.unit, count + 1)
        calc_end = calc_end + self.calc_calc_count(self.gu, 0, count + 1)
        if setZong == 1:
            calc_end = calc_end + self.calc_calc_count(self.zong + 1000, self.unit, count + 1)
        else:
            calc_end = calc_end + self.calc_calc_count(self.zong, self.unit, count + 1)
        date = struct.pack("%dB" % (len(calc_end)), *calc_end)
        self.tcpClient.send(date)
        time.sleep(0.01)


    # 止码
    def send_calc_end(self, stake_no, port, count):
        calc_end = [0x68, 0x31, 0x00, 0x70, 0x00, 0x02, 0x00, 0x82, 0x85, 0x06, 0x00, 0x00, 0x08, 0x00,
                        0x00] + stake_no + port + [0x02]
        calc_end = calc_end + self.time_conver()
        calc_end = calc_end + self.calc_calc_count(self.jian, 0, count + 1)
        calc_end = calc_end + self.calc_calc_count(self.feng, 0, count + 1)
        calc_end = calc_end + self.calc_calc_count(self.ping, self.unit, count + 1)
        calc_end = calc_end + self.calc_calc_count(self.gu, 0, count + 1)
        calc_end = calc_end + self.calc_calc_count(self.zong, self.unit, count + 1)
        date = struct.pack("%dB" % (len(calc_end)), *calc_end)
        self.tcpClient.send(date)
        time.sleep(0.01)

    #发送遥信数据
    def signal_send(self, stake_no, port, type):
        yx = [0x68, 0x31, 0x00, 0x80, 0x00, 0x02, 0x00, 0x86, 0x89, 0x01, 0x00, 0x00, 0x01, 0x00,
              0x00] + stake_no + port
        if type == 2:
            yx = yx + self.time_conver() + [0x02, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                       0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        elif type == 3:
            yx = yx + self.time_conver() + [0x03, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                       0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        elif type == 5:
            yx = yx + self.time_conver() + [0x05, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                       0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        elif type == 0:
            yx = yx + self.time_conver() + [0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                       0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        date = struct.pack("%dB" % (len(yx)), *yx)
        self.tcpClient.send(date)
        time.sleep(0.01)

    #发送配电遥测和计量数据
    def start_distribution(self):
        while True:
            if self.tk.DIST_METER_FLAG.get() == 1:
                d_jl = [0x68, 0x2F, 0x00, 0x54, 0x00, 0x00, 0x00, 0x87, 0x8f, 0x01, 0x00, 0x00, 0x03, 0x00, 0x00] + [
                    0x02, 0x00, 0x00, 0x09, 0x24, 0x04, 0x00, 0x00] + self.time_conver()
                d_jl = d_jl + [0x02, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x06, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00,
                               0x00, 0x08, 0x00, 0x00, 0x00]
                date = struct.pack("%dB" % (len(d_jl)), *d_jl)
                self.tcpClient.send(date)
                time.sleep(0.01)
                d_yc = [0x68, 0x77, 0x00, 0xA6, 0x05, 0x02, 0x00, 0x87, 0x8F, 0x01, 0x00, 0x00, 0x02, 0x00, 0x00] + [
                    0x02, 0x00, 0x00, 0x09, 0x24, 0x04, 0x00, 0x00] + self.time_conver()
                d_yc = d_yc + [0x94, 0x11, 0x00, 0x00, 0x4C, 0x04, 0x00, 0x00, 0x58, 0x02, 0x00, 0x00, 0xB0, 0x04, 0x00,
                               0x00, 0xBC, 0x02, 0x00, 0x00, 0xF4, 0x01, 0x00, 0x00, 0x14, 0x05, 0x00, 0x00, 0xFC, 0x08,
                               0x00, 0x00, 0x84, 0x03, 0x00, 0x00, 0x60, 0x09, 0x00, 0x00, 0x4C, 0x04, 0x00, 0x00, 0x4C,
                               0x04, 0x00, 0x00, 0x80, 0x0C, 0x00, 0x00, 0x14, 0x05, 0x00, 0x00, 0x08, 0x07, 0x00, 0x00,
                               0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00,
                               0x00, 0x02, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00,
                               0x00, 0x00]
                date = struct.pack("%dB" % (len(d_yc)), *d_yc)
                self.tcpClient.send(date)
                time.sleep(0.01)
                time.sleep(6);

    #心跳请求
    def heatbeatrequest(self):
        heartbeat = [0x68, 0x04, 0x00, 0x43, 0x00, 0x00, 0x00]
        date = struct.pack("%dB" % (len(heartbeat)), *heartbeat)
        self.tcpClient.send(date)
        time.sleep(0.01)
        self.ti.insert(END, get_time() + "+++发送心跳请求\n")
        self.ti.see(END)

    #心跳响应
    def heatbeatrespone(self):
        heartbeat = [0x68, 0x04, 0x00, 0x83, 0x00, 0x00, 0x00]
        date = struct.pack("%dB" % (len(heartbeat)), *heartbeat)
        self.tcpClient.send(date)
        time.sleep(0.01)
        self.ti.insert(END, get_time() + "+++发送心跳响应\n")
        self.ti.see(END);

    #连接线缆按钮
    def link_button(self):
        stake_no = str( self.tk.StakeNoCombox.get())
        port = str(self.tk.port_e.get())
        if len(stake_no) < 16:
            tk.messagebox.showerror('输入错误', '桩号长度不足16位')
            return
        elif len(stake_no) > 16:
            tk.messagebox.showerror('输入错误', '桩号长度大于16位')
            return
        if len(port) < 1:
            tk.messagebox.showerror('输入错误', '端口号长度小于1位')
            return
        self.signal_send(deviceStrToHexXX(stake_no, len(stake_no)), [deviceStrToHexXX(port, len(port))[0]], 2)
        self.ti.insert(END, get_time() + "+++发送连接线缆\n")
        self.ti.see(END);

    #断开线缆按钮
    def free_button(self):
        stake_no = self.tk.StakeNoCombox.get()
        port = self.tk.port_e.get()
        if len(stake_no) < 16:
            tk.messagebox.showerror('输入错误', '桩号长度不足16位')
        elif len(stake_no) > 16:
            tk.messagebox.showerror('输入错误', '桩号长度大于16位')
        if len(port) < 1:
            tk.messagebox.showerror('输入错误', '端口号长度小于1位')
        self.signal_send(deviceStrToHexXX(stake_no, len(stake_no)), [deviceStrToHexXX(port, len(port))[0]], 0)
        self.ti.insert(END, get_time() + "+++发送断开线缆\n")
        self.ti.see(END);

    #SEND按钮
    def send_signals(self):
        workStateMap = {'待机[2]':2,'工作[3]':3, '完成[5]':5, '告警[1]':1, '离线[4]':4};
        stake_no = str(self.tk.StakeNoCombox.get())
        warnArray = self.tk.warnArray
        port = str(self.tk.port_e.get())
        #print('port>>>', deviceStrToHexXX(port, 1))
        self.ti.insert(END, get_time() + "+++SEND岸电遥信数据\n")
        self.ti.see(END);
        yx = [0x68, 0x31, 0x00, 0x80, 0x00, 0x02, 0x00, 0x86, 0x89, 0x01, 0x00, 0x00, 0x01, 0x00,
              0x00] + deviceStrToHexXX(stake_no, len(stake_no)) + [deviceStrToHexXX(port, 1)[0]]
        yx = yx + self.time_conver() + [int('0x' + str(workStateMap[self.tk.WorkStateComBox.get()]), 16)] + [0x00, 0x01] + [
            int('0x' + str(warnArray[0].get()), 16)] \
             + [int('0x' + str(warnArray[1].get()), 16)] + [int('0x' + str(warnArray[2].get()), 16)] + [
                 int('0x' + str(warnArray[3].get()), 16)] + \
             [int('0x' + str(warnArray[4].get()), 16)] + [int('0x' + str(warnArray[5].get()), 16)] + [
                 int('0x' + str(warnArray[6].get()), 16)] + \
             [int('0x' + str(warnArray[7].get()), 16)] + [int('0x' + str(warnArray[8].get()), 16)] + [
                 int('0x' + str(warnArray[9].get()), 16)] + \
             [int('0x' + str(warnArray[10].get()), 16)] + [int('0x' + str(warnArray[11].get()), 16)] + [
                 int('0x' + str(warnArray[12].get()), 16)] + \
             [int('0x' + str(warnArray[13].get()), 16)] + [int('0x' + str(warnArray[14].get()), 16)] + [
                 int('0x' + str(warnArray[15].get()), 16)] + \
             [int('0x' + str(warnArray[16].get()), 16)] + [int('0x' + str(warnArray[17].get()), 16)]
        date = struct.pack("%dB" % (len(yx)), *yx)
        self.tcpClient.send(date)
        time.sleep(0.01)
        #self.dealCalcException()

    #异常产生
    def dealCalcException(self):
        stake_no = str(self.tk.StakeNoCombox.get())
        port = str(self.tk.port_e.get())
        calcExceptionMap = {'正常':0, '电表飞走[过程中]':1, '电表倒走[过程中]':2, '示值采集异常(尖峰平谷的和与总不等)[过程中]':3,
                            '电表飞走[止码]': 4, '电表倒走[止码]': 5, '示值采集异常(尖峰平谷的和与总不等)[止码]': 6
                            } #无起码,无止码,订单负数
        if calcExceptionMap[self.tk.CalcWarnComBox.get()] == 1: #电表飞走[过程中]
            if ((deviceStrToProtocol(stake_no) + port) in self.t_start_elec):
                self.send_calc_exception(deviceStrToHexXX(stake_no, len(stake_no)), [deviceStrToHexXX(port, len(port))[0]], 9999,0)
                self.ti.insert(END, get_time() + "+++产生过程中电表飞走\n")
                self.ti.see(END);
            else:
                self.ti.insert(END, get_time() + "+++当前桩未在供电中,无法产生电表飞走\n")
                self.ti.see(END);
        elif calcExceptionMap[self.tk.CalcWarnComBox.get()] == 2: #电表倒走[过程中]
            if ((deviceStrToProtocol(stake_no) + port) in self.t_start_elec):
                self.send_calc_exception(deviceStrToHexXX(stake_no, len(stake_no)), [deviceStrToHexXX(port, len(port))[0]], -1,0)
                self.ti.insert(END, get_time() + "+++产生过程中电表倒走\n")
                self.ti.see(END);
            else:
                self.ti.insert(END, get_time() + "+++当前桩未在供电中,无法产生电表倒走\n")
                self.ti.see(END);
        elif calcExceptionMap[self.tk.CalcWarnComBox.get()] == 3: #示值采集异常(尖峰平谷的和与总不等)[过程中]
            if ((deviceStrToProtocol(stake_no) + port) in self.t_start_elec):
                self.send_calc_exception(deviceStrToHexXX(stake_no, len(stake_no)), [deviceStrToHexXX(port, len(port))[0]]
                                     , self.t_start_elec[deviceStrToProtocol(stake_no) + port].count,1)
                self.ti.insert(END, get_time() + "+++产生过程中示值采集异常(尖峰平谷的和与总不等)\n")
                self.ti.see(END);
            else:
                self.ti.insert(END, get_time() + "+++当前桩未在供电中,无法产生示值采集异常(尖峰平谷的和与总不等)\n")
                self.ti.see(END);
        elif calcExceptionMap[self.tk.CalcWarnComBox.get()] == 4: #电表飞走[止码]
            if ((deviceStrToProtocol(stake_no) + port) in self.t_start_elec):
                self.t_start_elec[deviceStrToProtocol(stake_no) + port].count = 9999
                self.t_start_elec[deviceStrToProtocol(stake_no) + port].calcThreadStop()
                # self.send_calc_exception(deviceStrToHexXX(stake_no, len(stake_no)), [deviceStrToHexXX(port, len(port))[0]], 9999,0)
                self.ti.insert(END, get_time() + "+++产生止码电表飞走\n")
                self.ti.see(END);
            else:
                self.ti.insert(END, get_time() + "+++当前桩未在供电中,无法产生电表飞走\n")
                self.ti.see(END);
        elif calcExceptionMap[self.tk.CalcWarnComBox.get()] == 5: #电表倒走[止码]
            if ((deviceStrToProtocol(stake_no) + port) in self.t_start_elec):
                self.t_start_elec[deviceStrToProtocol(stake_no) + port].count = -1
                self.t_start_elec[deviceStrToProtocol(stake_no) + port].calcThreadStop()
                self.ti.insert(END, get_time() + "+++产生止码电表倒走\n")
                self.ti.see(END);
            else:
                self.ti.insert(END, get_time() + "+++当前桩未在供电中,无法产生电表倒走\n")
                self.ti.see(END);
        elif calcExceptionMap[self.tk.CalcWarnComBox.get()] == 6:  # 示值采集异常(尖峰平谷的和与总不等)[止码]
            if ((deviceStrToProtocol(stake_no) + port) in self.t_start_elec):
                # self.send_calc_exception(deviceStrToHexXX(stake_no, len(stake_no)), [deviceStrToHexXX(port, len(port))[0]]
                #                      , self.t_start_elec[deviceStrToProtocol(stake_no) + port].count,1)
                self.ti.insert(END, get_time() + "+++产生过程中示值采集异常(尖峰平谷的和与总不等)\n")
                self.ti.see(END);
            else:
                self.ti.insert(END, get_time() + "+++当前桩未在供电中,无法产生示值采集异常(尖峰平谷的和与总不等)\n")
                self.ti.see(END);

    def send_all_status_t(self,stake_port):
        for it in stake_port:
            stake_no_a = deviceStrToHexXX(it[0], len(it[0]))  # 桩号
            self.signal_send(stake_no_a, [deviceStrToHexXX(it[1], len(it[1]))[0]], 2)
        self.ti.insert(END, get_time() + "发送所有桩状态完成\n")
        self.ti.see(END);

    #发送全状态按钮
    def send_all_status(self,stake_port):
        self.ti.insert(END, get_time() + ".......发送桩状态中 请等待 勿动.....................\n")
        self.ti.see(END);
        time.sleep(0.01)
        send_all_status_tt = threading.Thread(target=lambda :self.send_all_status_t(stake_port), name='send_all_status_t')
        send_all_status_tt.start()

    def warn_end(self):
        d_yx = [0x68, 0x31, 0x00, 0x54, 0x00, 0x00, 0x00, 0x87, 0x8F, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00] + [0x02, 0x00,
                                                                                                             0x00, 0x09,
                                                                                                             0x24, 0x04,
                                                                                                             0x00,
                                                                                                             0x00] + self.time_conver()
        d_yx = d_yx + [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                       0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        date = struct.pack("%dB" % (len(d_yx)), *d_yx)
        self.tcpClient.send(date)
        time.sleep(0.01)
        self.ti.insert(END, get_time() + "-->配电告警消除\n")
        self.ti.see(END);

    def warn_start(self):
        d_yx = [0x68, 0x31, 0x00, 0x54, 0x00, 0x00, 0x00, 0x87, 0x8F, 0x01, 0x00, 0x00, 0x01, 0x00, 0x00] + [0x02, 0x00,
                                                                                                             0x00, 0x09,
                                                                                                             0x24, 0x04,
                                                                                                             0x00,
                                                                                                             0x00] + self.time_conver()
        d_yx = d_yx + [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01,
                       0x01, 0x01, 0x01, 0x01, 0x01, 0x01]
        date = struct.pack("%dB" % (len(d_yx)), *d_yx)
        self.tcpClient.send(date)
        time.sleep(0.01)
        self.ti.insert(END, get_time() + "-->配电告警产生\n")
        self.ti.see(END);

    # 时间转换
    def time_conver(self):
        s_time = time.strftime("%m%d%H%M%S", time.localtime())
        h_time = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        h_time[5] = int(bytes.fromhex(s_time[0:2]).hex())
        h_time[4] = int(bytes.fromhex(s_time[2:4]).hex())
        h_time[3] = int(bytes.fromhex(s_time[4:6]).hex())
        h_time[2] = int(bytes.fromhex(s_time[6:8]).hex())
        sec = hex(int(s_time[8:10]) * 1000)
        sec = sec[2:6].zfill(4)
        h_time[1] = int('0x' + sec[0:2], 16)
        h_time[0] = int('0x' + sec[2:4], 16)
        h_time[6] = 0x13
        return h_time

    def start_recv(self):
        stake_no = [];
        t_id = [];
        port = [];
        self.t_start_elec = {};
        while (1):
            recv = self.tcpClient.recv(BUFFSIZE)
            if (len(recv) >= 25):
                stake_no = deviceStrToHex(recv[15:23])  # 桩号
                t_id = [int(str(hex(recv[24])), 16)]  # T接ID
                port = [int(str(hex(recv[23])), 16)]  # 端口号
                print('stake_no:', stake_no)
                # T接供电
                if (len(recv) == 26):
                    # 创建对象
                    if (not (str(int(recv[15:23].hex())) + str(recv[23]) + str(recv[24]) in self.t_start_elec)):
                        print(get_time() + '----- new T接供电')
                        self.t_start_elec[str(int(recv[15:23].hex())) + str(recv[23]) + str(recv[24])] = shore_T(stake_no,
                                                                                                            t_id, port,self)
                    if ((recv[7] == 0x85) & (recv[12] == 0x08) & (recv[13] == 0x00) & (recv[14] == 0x00) & (
                        recv[25] == 0x01)):
                        self.ti.insert(END, get_time() + "<<<#######接收T接供电指令\n")
                        self.ti.see(END);
                        control_start = [0x68, 0x18, 0x00, 0xAA, 0x02, 0x02, 0x00, 0x82, 0x10, 0x07, 0x00, 0x00, 0x0A,
                                         0x00,
                                         0x00] + stake_no + port + t_id + [0x01, 0x00]
                        date = struct.pack("%dB" % (len(control_start)), *control_start)
                        self.tcpClient.send(date)
                        time.sleep(0.01)
                        self.ti.insert(END, get_time() + "#######>>T接箱" + str(recv[15:24].hex()) + "发送供电确认\n")
                        self.ti.see(END);
                        self.ti.see(END);
                        # #起码T接
                        self.send_calc_start(stake_no, t_id)
                        self.ti.insert(END, get_time() + "#######>>T接箱" + str(recv[15:24].hex()) + "发送起码\n")
                        self.ti.see(END);
                        self.signal_send(stake_no, t_id, 3)
                        self.ti.insert(END, get_time() + "#######>>T接箱" + str(recv[15:24].hex()) + "发送遥信工作中\n")
                        self.ti.see(END);
                        if port[0] < 10:
                            self.send_calc_start(stake_no, port)
                            self.ti.insert(END, get_time() + "#######>>T接箱(桩)" + str(recv[15:24].hex()) + "发送起码\n")
                            self.ti.see(END);
                            self.signal_send(stake_no, port, 3)
                            self.ti.insert(END, get_time() + "#######>>T接箱" + str(recv[15:24].hex()) + "发送遥信工作中\n")
                            self.ti.see(END);
                        self.t_start_elec[str(int(recv[15:23].hex())) + str(recv[23]) + str(recv[24])].calcThreadStart()
                    # T接断电
                    elif ((recv[7] == 0x85) & (recv[12] == 0x08) & (recv[13] == 0x00) & (recv[14] == 0x00) & (
                        recv[25] == 0x02)):
                        self.ti.insert(END, get_time() + "<<<#######接收T接断电指令\n")
                        self.ti.see(END);
                        control_end = [0x68, 0x18, 0x00, 0xAA, 0x02, 0x02, 0x00, 0x82, 0x10, 0x07, 0x00, 0x00, 0x0A,
                                       0x00,
                                       0x00] + stake_no + port + t_id + [0x02, 0x00]
                        date = struct.pack("%dB" % (len(control_end)), *control_end)
                        self.tcpClient.send(date)
                        time.sleep(0.01)
                        self.ti.insert(END, get_time() + "#######>>T接箱" + str(recv[15:24].hex()) + "发送断电确认\n")
                        self.ti.see(END);
                        self.t_start_elec[str(int(recv[15:23].hex())) + str(recv[23]) + str(recv[24])].calcThreadStop()
                        del self.t_start_elec[str(int(recv[15:23].hex())) + str(recv[23])+ str(recv[24])]
                # 直供供电
                if (len(recv) == 25):
                    if (not (str(int(recv[15:23].hex())) + str(recv[23]) in self.t_start_elec)):
                        print(get_time() + '----- new 直供供电')
                        self.t_start_elec[str(int(recv[15:23].hex())) + str(recv[23])] = shore(stake_no, port,self)
                        print("11111111:::::",str(int(recv[15:23].hex())) + str(recv[23]))
                    if ((recv[7] == 0x85) & (recv[12] == 0x05) & (recv[13] == 0x00) & (recv[14] == 0x00) & (
                        recv[24] == 0x01)):
                        self.ti.insert(END, get_time() + "<<<#######接收直供供电指令\n")
                        self.ti.see(END);
                        control_start = [0x68, 0x17, 0x00, 0xAA, 0x02, 0x02, 0x00, 0x82, 0x10, 0x07, 0x00, 0x00, 0x07,
                                         0x00,
                                         0x00] + stake_no + port + [0x01, 0x00]
                        date = struct.pack("%dB" % (len(control_start)), *control_start)
                        self.tcpClient.send(date)
                        time.sleep(0.01)
                        self.ti.insert(END, get_time() + "#######>>接电箱" + str(recv[15:24].hex()) + "发送供电确认\n")
                        self.ti.see(END);
                        # #起码直供
                        self.send_calc_start(stake_no, port)
                        self.ti.insert(END, get_time() + "#######>>T接箱" + str(recv[15:24].hex()) + "发送起码\n")
                        self.ti.see(END);
                        self.signal_send(stake_no, port, 3)
                        self.ti.insert(END, get_time() + "#######>>T接箱" + str(recv[15:24].hex()) + "发送遥信工作中\n")
                        self.ti.see(END);
                        self.t_start_elec[str(int(recv[15:23].hex())) + str(recv[23])].calcThreadStart()

                    # 直供断电
                    elif ((recv[7] == 0x85) & (recv[12] == 0x05) & (recv[13] == 0x00) & (recv[14] == 0x00) & (
                        recv[24] == 0x02)):
                        self.ti.insert(END, get_time() + "<<<#######接收直供断电指令\n")
                        self.ti.see(END);
                        control_end = [0x68, 0x17, 0x00, 0xAA, 0x02, 0x02, 0x00, 0x82, 0x10, 0x07, 0x00, 0x00, 0x07,
                                       0x00,
                                       0x00] + stake_no + port + [0x02, 0x00]
                        date = struct.pack("%dB" % (len(control_end)), *control_end)
                        self.tcpClient.send(date)
                        time.sleep(0.01)
                        self.ti.insert(END, get_time() + "#######>>接电箱" + str(recv[15:24].hex()) + "发送断电确认\n")
                        self.ti.see(END);
                        self.t_start_elec[str(int(recv[15:23].hex())) + str(recv[23])].calcThreadStop()
                        del self.t_start_elec[str(int(recv[15:23].hex())) + str(recv[23])]
            if len(recv) == 7:
                if recv[3] == 0x43:
                    hbrespone = [0x68, 0x04, 0x00, 0x83, 0x00, 0x00, 0x00]
                    date = struct.pack("%dB" % (len(hbrespone)), *hbrespone)
                    self.tcpClient.send(date)
                    time.sleep(0.01)
                    self.ti.insert(END, get_time() + "#######>>心跳帧响应\n")
                    self.ti.see(END);
