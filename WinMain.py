# -*- coding: utf-8 -*-
import sys,os
import time
import re
import json
import configparser
import random
import binascii
import wmi
import IPy
# import Queue
from PySide6 import QtCore,QtGui
from PySide6.QtCore import SIGNAL
from PySide6.QtWidgets import QWidget,QApplication
from common.Form_Main import Ui_Form
from common.Global import *
from scapy.all import ARP,ICMP,Ether,IP,UDP,BOOTP,DHCP,Raw,reduce,sniff,sendp,mac2str

# reload(sys)
# sys.setdefaultencoding('utf-8')

class RunThread(QtCore.QThread):
    #把打印的字符串发送给UI主线程
    singal_sendnum= QtCore.Signal(str) # 已发送数据包个数
    def __init__(self, parent=None):
        super(RunThread, self).__init__(parent)
        self.parent = parent
        
    def init_data(self):
        self.iface = self.parent.iface
        self.ack_num = 0
        self.discover_num=0
        self.ack_time = []
        print("")
        # mac = self.parent.macdict[self.parent.iface]['mac']
        mac = self.parent.get_ifaceMapMac(self.iface)
        print("mac", mac)
        self.smac = ":".join(re.findall('[0-9A-F]{2}',mac))
        # self.sip = self.parent.ipdict[self.smac]
        self.sip = self.parent.config['bootp']['routers']
        self.filter="arp or icmp or (udp and src port 68 and dst port 67)"
        self.lease_time = int(self.parent.config['bootp']['leasetime'])
        self.renewal_time = int(int(self.lease_time)/2)
        self.rebinding_time = 7*int(self.lease_time)/8
        self.subnet_mask = self.parent.config['bootp']['submask']
        self.router = self.parent.config['bootp']['routers']
        self.routerlist = self.parent.config['bootp']['routerlist']
        self.name_server = self.parent.config['bootp']['dns']
        self.ippools = self.parent.config['bootp']['ippools']
        self.offer_timeout = self.parent.config['bootp']['waitoffer']
        self.ack_timeout = self.parent.config['bootp']['waitack']
        self.t1 = self.parent.config['bootp']['t1']
        self.t2 = self.parent.config['bootp']['t2']
        self.routeoption = self.parent.static_router_option
        self.clients = {}
        s_ip,e_ip = self.ippools.split(" ")
        self.s_num = self.ip2int(s_ip)
        self.e_num = self.ip2int(e_ip)
        if self.s_num > self.e_num:
            self.s_num,self.e_num = self.e_num,self.s_num
        #print "self.name_server=",self.name_server
    
    def start_test(self):
        self.init_data()
        self.start()
    
    def stop_test(self):
        self.terminate()
        self.wait()
    
    def randomip(self,s_num,e_num):
        iplist =  self.clients.values()
        while True:
            ipaddr = self.num2ip(random.randint(s_num,e_num))
            if ipaddr not in iplist:
                break
        return ipaddr
    
    def poolfree(self,mac):
        if mac in self.clients:
            return self.clients[mac]
        ipaddr = self.randomip(self.s_num,self.e_num)
        return ipaddr
    
    def ip2int(self,ip):
        u"IP地址转换成整数"
        return reduce(lambda a,b: a<<8 | b, map(int, ip.split(".")))
    
    def num2ip(self,ip_num):
        u"整数转换成IP地址"
        return ".".join(map(lambda n: str(ip_num>>n & 0xFF), [24,16,8,0]))
    
    def ipvalid(self,ip):
        curip = self.ip2int(ip)
        if ip == '0.0.0.0':
            return False
        elif curip>self.e_num or curip <self.s_num:
            return True
        return False

    def mac2bin(self,mac):
        return b"".join(map(lambda x:binascii.a2b_hex(x),mac.split(":")))

    def run(self):
        sniff(filter=self.filter,prn=self.detect_parserDhcp,store=0,iface=self.iface)

    def waittimeout(self,num):
        try:
            if isinstance(num,str):
                time.sleep(int(num))
            else:
                time.sleep(int(num))
        except Exception as e:
            pass
        return True

    def detect_parserDhcp(self,pkt):
        print("start parser pkt")
        if DHCP in pkt:
            raw=Ether()/IP()/UDP(sport=67,dport=68)/BOOTP()/DHCP()
            raw[Ether].src,raw[IP].src=self.smac,self.sip
            raw[Ether].dst,raw[IP].dst=pkt[Ether].src,'255.255.255.255'
            send_type="nak"
            #1->Discover 2->OFFER  3->Request 4->Decline 5->ACK  6->NAK  7->Release 8->Inform
            #如果这里不添加DHCP,后面添加DHCP就会报错
            raw[BOOTP]=BOOTP(op=2,xid=pkt[BOOTP].xid,chaddr=self.mac2bin(pkt[Ether].src),yiaddr="0.0.0.0",giaddr='0.0.0.0')/DHCP()
            # DhcpOption=[("server_id",self.sip),('lease_time',self.lease_time),("subnet_mask",self.subnet_mask),("router",self.router),('renewal_time',self.renewal_time),('name_server',self.name_server),('rebinding_time',self.rebinding_time)]
            name_server=self.ip2bin(self.name_server)
            #print "name_server",name_server
            # name_server='\xdf\x01\x02\x03\xdf\x01\x02\x04'
            DhcpOption=[("server_id",self.sip),('lease_time',self.lease_time),("subnet_mask",self.subnet_mask),("router",self.router),('renewal_time',self.renewal_time),(6,name_server),('rebinding_time',self.rebinding_time)]
            type=pkt[DHCP].options[0][1] ;#获取得到option 53字段的内容
            # raw[]
            print("pkt[DHCP].options",pkt[DHCP].options)
            for i in pkt[DHCP].options:
                if i[0] == 'requested_addr':
                    request_ip=i[1]
                    break
                else :
                    request_ip='0.0.0.0'
            if type == 0x01:
                self.discover_num+=1
                dhcpsip = pkt[IP].src
                dhcpsmac = pkt[Ether].src
                cli_mac=pkt[Ether].src
                localxid=pkt[BOOTP].xid
                your_ip=self.poolfree(dhcpsmac)
                raw[BOOTP].yiaddr=your_ip
                #如果请求的IP地址不在地址池中回应NAK报文
                if self.ipvalid(request_ip):
                    #发送Nak报文
                    nak=Ether(src=self.smac,dst="ff:ff:ff:ff:ff:ff")/IP(src=self.sip,dst="255.255.255.255")/UDP(sport=67,dport=68)/BOOTP(yiaddr=your_ip,xid=localxid)/DHCP(options=[("message-type","nak"),("server_id",self.sip),"end"])
                    sendp(nak,verbose=0,iface=self.iface)
                else:
                    #  地址池有地址
                    if type == 1:
                        #判断是否需要添加其他的options 33/121/249字段
                        if request_ip != '0.0.0.0' and not self.ipvalid(request_ip):
                            raw[BOOTP].yiaddr=request_ip
                        else:
                            raw[BOOTP].yiaddr=your_ip
                        DhcpOption.insert(0,("message-type", 2))
                        options_all=self.add_option(DhcpOption)
                        options_all.append("end")
                        options_all.append(mac2str("00")*20)
                        raw[DHCP]=DHCP(options=options_all)
                        print("raw=",raw.show())
                        if self.parent.config['bootp']['relpy_offer']=='on':
                            if self.waittimeout(self.offer_timeout):
                                sendp(raw,iface=self.iface)
                        else:
                            pass
            elif type == 0x03:
                reply=0
                if self.discover_num>=1:
                    self.ack_time.append(pkt.time)
                if len(self.ack_time)!=0:
                    if ((self.ack_time[-1]-self.ack_time[0])-2)<self.rebinding_time<((self.ack_time[-1]-self.ack_time[0])+2):
                        reply =True
                dhcpsip = pkt[IP].src
                dhcpsmac = pkt[Ether].src
                cli_mac=pkt[Ether].src
                localxid=pkt[BOOTP].xid
                your_ip=self.poolfree(dhcpsmac)
                raw[BOOTP].yiaddr=your_ip
                #如果请求的IP地址不在地址池中回应NAK报文
                if self.ipvalid(pkt[BOOTP].ciaddr):
                    #发送Nak报文
                    nak=Ether(src=self.smac,dst="ff:ff:ff:ff:ff:ff")/IP(src=self.sip,dst="255.255.255.255")/UDP(sport=67,dport=68)/BOOTP(yiaddr=your_ip,xid=localxid)/DHCP(options=[("message-type","nak"),("server_id",self.sip),"end"])
                    sendp(nak,verbose=0,iface=self.iface)
                else:
                    #  地址池有地址
                    if type == 3:
                        # raw[Ether].dst,raw[IP].dst=pkt[Ether].src,request_ip
                        if request_ip != '0.0.0.0':
                            raw[Ether].dst,raw[IP].dst=pkt[Ether].src,request_ip
                            raw[BOOTP].yiaddr=request_ip
                        else:
                            raw[Ether].dst,raw[IP].dst=pkt[Ether].src,pkt[BOOTP].ciaddr
                            raw[BOOTP].yiaddr=pkt[BOOTP].ciaddr
                        DhcpOption.insert(0,("message-type","ack"))
                        #注意这里不是*DhcpOption
                        options_all=self.add_option(DhcpOption)
                        options_all.append("end")
                        options_all.append(mac2str("00")*20)
                        raw[DHCP]=DHCP(options=options_all)
                        if self.parent.config['bootp']['relpy_ack']=='on':
                            if pkt[BOOTP].ciaddr == "0.0.0.0":
                                #为回应OFFER的requeest
                                if self.waittimeout(self.ack_timeout):
                                    sendp(raw,verbose=0,iface=self.iface)
                            else:
                                # if pkt[IP].dst == self.sip:
                                if pkt[IP].src == "0.0.0.0":
                                    #为回应OFFER的requeest
                                    sendp(raw,iface=self.iface)
                                    self.ack_num+=1
                                elif pkt[IP].dst == self.sip:
                                    if (self.t2 == 'on' and self.t1 == 'on') or (self.t2 == 'off' and self.t1 == 'on'):
                                        sendp(raw,iface=self.iface)
                                    elif (self.t2 == 'off' and self.t1 == 'off'):
                                        pass
                                elif (self.t2 == 'on' and self.t1 == 'off') and reply:
                                    #request报文出现的时间点为7/8的租约时间时回复ack报文
                                    sendp(raw,verbose=0,iface=self.iface)
                                    reply = 0
                                    self.ack_time = [self.ack_time[-1]]
                            # self.clients[dhcpsmac]=your_ip
                        else:
                            pass

            elif type == 0x08:
                dhcpsip = pkt[IP].src
                dhcpsmac = pkt[Ether].src
                cli_mac=pkt[Ether].src
                localxid=pkt[BOOTP].xid
                your_ip=self.poolfree(dhcpsmac)
                raw[BOOTP].yiaddr=your_ip
                #如果请求的IP地址不在地址池中回应NAK报文
                if self.ipvalid(pkt[BOOTP].ciaddr):
                    #发送Nak报文
                    nak=Ether(src=self.smac,dst="ff:ff:ff:ff:ff:ff")/IP(src=self.sip,dst="255.255.255.255")/UDP(sport=67,dport=68)/BOOTP(yiaddr=your_ip,xid=localxid)/DHCP(options=[("message-type","nak"),("server_id",self.sip),"end"])
                    sendp(nak,verbose=0,iface=self.iface)
                else:
                    #  地址池有地址
                    if type == 8:
                        # raw[Ether].dst,raw[IP].dst=pkt[Ether].src,request_ip
                        if request_ip != '0.0.0.0':
                            raw[Ether].dst,raw[IP].dst=pkt[Ether].src,request_ip
                            raw[BOOTP].yiaddr=request_ip
                        else:
                            raw[Ether].dst,raw[IP].dst=pkt[Ether].src,pkt[BOOTP].ciaddr
                            raw[BOOTP].yiaddr=pkt[BOOTP].ciaddr
                        raw[BOOTP].yiaddr=request_ip
                        DhcpOption.insert(0,("message-type","ack"))
                        #注意这里不是*DhcpOption
                        options_all=self.add_option(DhcpOption)
                        options_all.append("end")
                        options_all.append(mac2str("00")*20)
                        raw[DHCP]=DHCP(options=options_all)
                        if pkt[BOOTP].ciaddr == "0.0.0.0":
                            #为回应OFFER的requeest
                            if self.waittimeout(self.ack_timeout):
                                sendp(raw,verbose=0,iface=self.iface)
                        else:
                            if pkt[IP].src == "0.0.0.0":
                                #回应T2广播包
                                sendp(raw,verbose=0,iface=self.iface)
                            else:
                                #回应T1单播包
                                sendp(raw,iface=self.iface)
                        # self.clients[dhcpsmac]=your_ip

            elif type == 4:
                dhcpsmac = pkt[Ether].src
                options=pkt[DHCP].options
                optionlen=len(options)
                for i in range(optionlen):
                    if options[i][0] == "requested_addr":
                        self.clients[dhcpsmac]=options[i][1]
                        break
            elif type == 7:
                dhcpsip = pkt[IP].src
                dhcpsmac = pkt[Ether].src
                # self.clients.pop(dhcpsmac)
        elif ARP in pkt:
            if pkt[ARP].pdst==self.sip and pkt[ARP].psrc != "0.0.0.0":
                arp_reply=Ether(src=self.smac,dst=pkt.src)/ARP(op=0x0002,hwsrc=self.smac,psrc=self.sip,hwdst=pkt[ARP].hwsrc,pdst=pkt[ARP].psrc)/"001122334455"
                sendp(arp_reply,verbose=0,iface=self.iface)
        elif ICMP in pkt:
            pkt.show()
            print("here")
            print("pkt[ICMP].chksum",pkt[ICMP].chksum)
            if pkt[IP].dst==self.sip :
                ICMP_reply=Ether(src=self.smac,dst=pkt.src)/IP(version=pkt[IP].version,id=pkt[IP].id,ttl=pkt[IP].ttl,src=self.sip,dst=pkt[IP].src)/ICMP(type = 0x0000,code=0,chksum=pkt[ICMP].chksum+2048,id=pkt[ICMP].id,seq=pkt[ICMP].seq)/Raw(load='abcdefghijklmnopqrstuvwabcdefghi')
                sendp(ICMP_reply,verbose=0,iface=self.iface)
        
    def add_option(self,options_all):
        ret_all=options_all
        if self.routeoption in ['options33','options121','options249']:
            optnum = re.findall('([0-9]+)',self.routeoption)[0]
            optionrouterstr = optnum+' '+self.routerlist.strip().replace(","," ")
            optnum = int(optnum)
            ret_all.append((optnum,self.parser_option33(optionrouterstr)))
        return ret_all

    def parser_option33(self,option):
        print("option=",option)
        header= option[:2]
        if header == "33":
            options33str = re.sub(r'(/[0-9]+)','',option[3:])
            return self.ip2bin(options33str)
        elif option[:3] in ["121","249"]:
            ip=self.parser_option121(option[3:])
            return self.ip2bin(ip)

    def parser_option121(self,option):
        #先对传入参数进行
        #传入参数格式为 192.168.1.2/24 192.168.100.1 192.168.2.2/24 192.168.100.1 
        optlist=option.strip().split(" ")
        optlen=len(optlist)
        ret=[]
        for i in range(0,optlen,2):
            opt=self.parser_ipnet(optlist[i],optlist[i+1])
            ret.append(opt)
        print("ret=",ret)
        return ".".join(ret)

    def ip2bin(self,ip,flag=". ,"):
        # 把IP地址转换成字节流 192.168.1.1 =>\xc0\xa8\x01\x01
        hexlist=re.split(r"[%s]" %(flag),ip)
        print("hexlist=",hexlist)
        # hexstr="".join(map(lambda x:"%02x" %(int(x)),hexlist))
        binip="".join(map(lambda x:chr(int(x)),hexlist))
        return binip

    def parser_ipnet(self,ipnet="",gw=""):
        # 主要根据IP和子网掩码得到网络地址
        f=lambda x:(int(x)-1)/8+1
        dst=ipnet.split("/")
        ip,mask=str(IPy.IP(dst[0]).make_net(dst[1])).split("/")
        ip=".".join(ip.split(".")[:f(mask)])
        return ".".join([mask,ip,gw])

class Form(QWidget):  
    def __init__(self, parent=None):  
        super(Form, self).__init__(parent)  
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle(u"Dhcp服务器工具")
        self.index_iface = {}
        self.macdict = {} #用于存放接口mac地址
        self.ipdict = {}  #用于存放MAC地址对应的IP地址
        self.init_iface()
        self.iface = "eth0"
        self.select_staticrouter()
        self.init_cfg()
        # 连接信号与槽函数
        self.connect(self.ui.startbtn,SIGNAL("clicked()"),self.startsend)
        self.connect(self.ui.savecfg,SIGNAL("clicked()"),self.savecfg)
        self.connect(self.ui.staticroute,SIGNAL("currentIndexChanged(int)"),self.select_staticrouter)
        self.runthread = RunThread(self)
        self.runthread.singal_sendnum.connect(self.shownum)

    def shownum(self,num):
        if num == "-1":
            self.runthread.stop_test()
            self.ui.startbtn.setText(u"已停止")
            self.ui.serstatus.setText(u"服务器已经停止运行")
        else:
            self.ui.serstatus.setText(u"服务器正在运行中")

    def startsend(self):
        text=self.ui.startbtn.text()
        if text == u"运行中...":
            self.runthread.stop_test()
            self.ui.startbtn.setText(u"已停止")
            self.ui.serstatus.setText(u"服务器已经停止运行")
        else:
            self.select_iface()
            self.savecfg(False)
            self.ui.startbtn.setText(u"运行中...")
            self.ui.serstatus.setText(u"服务器正在运行中")
            self.runthread.start_test()

    def init_cfg(self):
        self.config=readcfg()
        self.ui.leasetime.setText(self.config['bootp']['leasetime'])
        self.ui.submask.setText(self.config['bootp']['submask'])
        self.ui.gateway.setText(self.config['bootp']['routers'])
        self.ui.ippool.setText(self.config['bootp']['ippools'])
        self.ui.dns.setText(self.config['bootp']['dns'])
        self.ui.waitoffer.setText(self.config['bootp']['waitoffer'])
        self.ui.waitack.setText(self.config['bootp']['waitack'])
        self.ui.replyrequest.setText(self.config['bootp']['relpy_ack'])
        self.ui.replyDiscover.setText(self.config['bootp']['relpy_offer'])
        self.ui.t1.setText(self.config['bootp']['t1'])
        self.ui.t2.setText(self.config['bootp']['t2'])
        routerlist = self.get_staticrouterlist('get')
        self.ui.routers.setPlainText(routerlist)

    def get_staticrouterlist(self,type='get'):
        if type == 'get':
            routerlist = self.config['bootp']['routerlist'].replace(',','\n')
        else:
            routerlist = self.ui.routers.toPlainText()
            routerlist = routerlist.replace('\n',',')
        return routerlist

    def select_staticrouter(self):
        self.static_router_option=self.ui.staticroute.currentText()
        print("routeoption=",self.static_router_option)

    def savecfg(self,flag=True):
        # 保存GUI配置文件
        # 先把以前的信息读取出来,然后保存成字典,然后把GUI上有的参数替换掉,没有的参数不操作
        init_dict = readcfg()
        guidict = {}
        guidict['bootp']={}
        
        cf = configparser.ConfigParser()
        
        guidict['bootp']['leasetime'] = self.ui.leasetime.text()
        guidict['bootp']['submask'] = self.ui.submask.text()
        guidict['bootp']['routers'] = self.ui.gateway.text()
        guidict['bootp']['ippools']= self.ui.ippool.text()
        guidict['bootp']['dns'] = self.ui.dns.text()
        guidict['bootp']['routerlist'] = self.get_staticrouterlist('set')
        guidict['bootp']['waitoffer']=self.ui.waitoffer.text()
        guidict['bootp']['waitack']=self.ui.waitack.text()
        guidict['bootp']['relpy_ack']=self.ui.replyrequest.text()
        guidict['bootp']['relpy_offer']=self.ui.replyDiscover.text()
        guidict['bootp']['t1']=self.ui.t1.text()
        guidict['bootp']['t2']=self.ui.t2.text()
        for key,value in init_dict.items():
            cf.add_section(key)
            for k,v in value.items():
                if key in guidict:
                    if k in guidict[key]:
                        cf.set(key, k, guidict[key][k])
                        continue
                cf.set(key, k, v)
        with open(ConfigFile.replace("\\","/"),"w+") as f:
            cf.write(f)
        self.config=readcfg()
        if flag:
            QtGui.QMessageBox.information(self,"savecfg",u"保存配置成功",QtGui.QMessageBox.Yes)

    def init_iface(self):
        print("start iface")
        ifacelst = self.get_iface()
        for iface in ifacelst:
            self.ui.iface.addItem(iface.strip())
        self.connect(self.ui.iface,SIGNAL("currentIndexChanged(int)"),self.select_iface)

    def select_iface(self):
        cur_iface = self.ui.iface.currentText()
        # self.iface = self.index_iface[cur_iface]
        self.iface = cur_iface
        print("self.iface=",self.iface)

    def get_iface(self):
        # 获取网卡列表，返回list
        iface_list=[]
        wm=wmi.WMI()
        ifaces=wm.Win32_NetworkAdapterConfiguration (IPEnabled=1)
        for iface in ifaces:
            iface_desc=iface.Description
            iface_list.append(iface_desc)
        print(iface_list)
        return iface_list

    def get_ifaceMapMac(self,desc):
        # 获取网卡接口描述与mac地址映射字典
        desc_mac={}
        mac_ip={}
        w=wmi.WMI()
        ifaces=w.Win32_NetworkAdapterConfiguration (IPEnabled=1)
        for iface in ifaces:
            desc_mac[iface.Description]=iface.MACAddress
            mac_ip[iface.MACAddress]=iface.IPADDRESS[0]
            # iface_list.append(iface_desc)
        print(desc_mac[desc])
        return desc_mac[desc]

    def get_macMapDesc(self):
        c = wmi.WMI()
        mac_desc={}
        self.macipdict = {}
        for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=1):
            mac_desc["".join(interface.MACAddress.split(":"))]=interface.Description
            self.ipdict[interface.MACAddress] = interface.IPADDRESS[0]
        return mac_desc

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec())