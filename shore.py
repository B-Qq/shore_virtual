from shorePowerProtocol import *

def get_time():
    return time.strftime('%H:%M:%S',time.localtime(time.time()))

# 岸电桩
class shore():
    # 桩号, 端口号, shorePowerProtocol类
    def __init__(self, deviceId,port,protocol):
        self.deivceId = deviceId
        self.port = port
        self.flag = True
        self.protocol = protocol
        self.count = 0

    # 发送遥测数据
    def charge_send(self):
        self.count = 0
        self.flag = True
        while True:
            time.sleep(5)
            if self.flag:
                self.protocol.metet_send(self.deivceId, self.port, self.count)
                self.protocol.ti.insert(END, get_time() + "+++>>接电箱" + str(self.deivceId) + str(self.port) + "发送遥测数据\n")
                self.protocol.ti.see(END);
                # T接箱
                self.protocol.send_calc(self.deivceId, self.port, self.count)
                self.protocol.ti.insert(END, get_time() + "+++>>接电箱" + str(self.deivceId) + str(self.port) + "发送充电中计量数据\n")
                self.protocol.ti.see(END);
                self.count = self.count + 1
            else:
                break;
                # 开启线程发送数据

    def calcThreadStart(self):
        self.ThreadStart = threading.Thread(target=self.charge_send, name='charge_send')
        self.ThreadStart.start()

    def calcStop(self):
        self.flag = False
        # self.count = 0

    def calcThreadStop(self):
        self.ThreadStop = threading.Thread(target=self.send_calcend, name='send_calcend')
        self.ThreadStop.start()

    def send_calcend(self):
        count = self.count
        self.calcStop()
        time.sleep(6)
        self.protocol.send_calc_end(self.deivceId, self.port, count)
        self.protocol.ti.insert(END, get_time() + "#######>>接电箱" + str(self.deivceId) + str(self.port) + "发送止码\n")
        self.protocol.ti.see(END);
        self.protocol.signal_send(self.deivceId, self.port, 5)
        self.protocol.ti.insert(END, get_time() + "#######>>接电箱" + str(self.deivceId) + str(self.port) + "发送遥信完成\n")
        self.protocol.ti.see(END);

    def calcThreadStopException(self):
        threading.Thread(target=self.send_calcend_exception, name='send_calcend_exception').start()

    def send_calcend_exception(self):
        count = self.count
        self.calcStop()
        time.sleep(6)
        self.protocol.send_calc_end_exception(self.deivceId, self.port, count)
        self.protocol.ti.insert(END, get_time() + "#######>>接电箱" + str(self.deivceId) + str(self.port) + "发送止码\n")
        self.protocol.ti.see(END);
        self.protocol.signal_send(self.deivceId, self.port, 5)
        self.protocol.ti.insert(END, get_time() + "#######>>接电箱" + str(self.deivceId) + str(self.port) + "发送遥信完成\n")
        self.protocol.ti.see(END);
