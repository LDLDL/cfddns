# cloudflare ddns

一个python3实现的cloundflare ddns脚本

## 系统要求

可运行python3.6以上版本即可

## 如何运行
### 1.安装python3.6以上版本
略
### 2.安装以下包
```bash
pip3 install requests
pip3 install dnspython
sudo pip3 install func-timeout
```
### 3.修改脚本
修改脚本内的 zoneid apikey email dnsrecords domain
### 4.运行脚本

## 使用服务
### 1.修改cfddns.serivce
修改以下语句中的~/cfddns.py为存放cfddns.py的路径
```
ExecStart=python ~/cfddns.py
```
### 2.将cfddns.service移动到/usr/lib/systemd/system

### 3.启动服务并开机运行

```bash
systemctl daemon-reload
systemctl start cfddns
systemctl enable cfddns
```