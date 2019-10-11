import time
from shorePowerProtocol import *

#T接箱
class shore_T():
    #桩号,T接箱号,端口号,shorePowerProcotol类
    def __init__(self,deviceId,t_id,port,protocol):
        self.deivceId = deviceId
        self.t_id = t_id
        self.port = port
        self.flag = True
        self.protocol = protocol
        self.count = 0

    #发送遥测数据
    def charge_send(self):
        #self.count = 0
        self.flag = True
        while True:
            time.sleep(5)
            if self.flag:
                self.protocol.metet_send(self.deivceId, self.t_id, self.count)
                self.protocol.ti.insert(END, get_time() + "+++>>T接箱" + str(self.deivceId) + str(self.t_id) + "发送遥测数据\n")
                self.protocol.ti.see(END);
                #T接箱
                self.protocol.send_calc(self.deivceId, self.t_id, self.count)
                self.protocol.ti.insert(END,get_time() + "+++>>T接箱" + str(self.deivceId) + str(self.t_id) + "发送充电中计量数据\n")
                self.protocol.ti.see(END);
                if self.port[0] < 10:
                    self.protocol.send_calc(self.deivceId , self.port, self.count)
                    self.protocol.ti.insert(END, get_time() + "+++>>T接箱(桩)" + str(self.deivceId) + str(self.port) + "发送充电中计量数据\n")
                    self.protocol.ti.see(END);
                    self.protocol.metet_send(self.deivceId,self.port,self.count)
                    self.protocol.ti.insert(END,get_time() + "+++>>T接箱(桩)" + str(self.deivceId) + str(self.port) + "发送遥测数据\n")
                    self.protocol.ti.see(END);
                self.count = self.count + 1
            else:
                break;
     #开启线程发送数据
    def calcThreadStart(self):
        self.ThreadStart = threading.Thread(target=self.charge_send,name='charge_send')
        self.ThreadStart.start()
    def calcStop(self):
        self.flag = False
        self.count = 0
    def calcThreadStop(self):
        self.ThreadStop = threading.Thread(target=self.send_calcend, name='send_calcend')
        self.ThreadStop.start()
    def send_calcend(self):
        count = self.count
        self.calcStop()
        time.sleep(6)
        self.protocol.send_calc_end(self.deivceId, self.t_id, count)
        self.protocol.ti.insert(END, get_time() + "#######>>T接箱" + str(self.deivceId) + str(self.t_id) + "发送止码\n")
        self.protocol.ti.see(END);
        self.protocol.signal_send(self.deivceId, self.t_id, 5)
        self.protocol.ti.insert(END, get_time() + "#######>>T接箱" + str(self.deivceId) + str(self.t_id) + "发送遥信完成\n")
        self.protocol.ti.see(END);
        if (self.port[0] < 10):
            # 止码T接
            self.protocol.send_calc_end(self.deivceId, self.port, count)
            self.protocol.ti.insert(END, get_time() + "#######>>T接箱(桩)" + str(self.deivceId) + str(self.port) + "发送止码\n")
            self.protocol.ti.see(END);
            self.protocol.signal_send(self.deivceId, self.port, 5)
            self.protocol.ti.insert(END, get_time() + "#######>>T接箱(桩)" + str(self.deivceId) + str(self.port) + "发送遥信完成\n")
            self.protocol.ti.see(END);