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
### 3.运行init.py并输入相关信息
```bash
python3 ./init.py
```
### 4.运行脚本
```bash
python3 ./cfddns.py
```

## 使用服务
### 以root用户运行install_as_service.sh
```bash
sudo bash install_as_service.sh
```