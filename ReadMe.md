# dhcpser-sim

> PyQt and scapy project.

## 介绍

基于PySide6、scapy开发的模拟DHCP服务端的GUI界面测试工具，用于响应DHCP客户端的dhcp协议报文。

### Developer

[FanHao](http://alanfanh.github)

### 项目结构

````text
dhcpser-sim
|
|--common
|  |
|  |---Globals.py       # 获取路径,配置读取
|  |---Form_Main.py     # 界面源码
|
|--WinMain.py           # 界面主线程,工作子线程,核心处理逻辑
|--config.ini           # 配置文件
|
````

## 环境

> python3.9.10 64bit

### 依赖

> 可使用"pip install -r requirements.txt"一键安装所有依赖项

````text
pyside6==6.2.1
wmi==1.5.1
scapy==2.4.5
configparser==5.2.0
````