import configparser #配置文件
import sys
import operatorDb as db
import layout
import tcpclient as tcl
import shorePowerProtocol as protocol
from setConfigLayout import *
from setStationId import *
import time

#配置文件读取
cf = configparser.ConfigParser()
cf.read('conf.ini')

if __name__ == "__main__":
    sf = setConfigLayout(cf)
    stationId = db.QueryStationId(cf)  #查询所有站号
    setStationIdLayout(cf, stationId) #设置模拟的站号
    stake_port = db.QueryStakePort(cf) #查询桩号端口号
    STATION = int(cf.get("STATION", "ID"))
    tk = layout.layout(stake_port,STATION,cf,db)#布局初始化
    tcpClient = tcl.tcp_init(cf,tk.getScrolledText(),tk.getTop()) #tcp连接初始化
    pl = protocol.shorePowerProtocol(tcpClient,lambda :tcl.tcpReConnect(cf),STATION,cf,tk)#协议初始化

    tk.sendButton(pl.send_signals,pl.heatbeatrequest,pl.heatbeatrespone)#发送按键绑定
    tk.sendCalcExceptionButton(pl.dealCalcException)
    tk.connect(pl.link_button)  #连接线缆按钮绑定
    tk.disconnect(pl.free_button) #断开线缆按钮绑定
    tk.sendAllState(lambda :pl.send_all_status(stake_port)) #发送全状态按钮绑定
    tk.distWarnButton(pl.warn_end,pl.warn_start) #配电告警按键绑定

    tk.closeWindows(tcpClient)
    tk.mainloop()

