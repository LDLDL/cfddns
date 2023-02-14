# CloudFlare DDNS脚本

[English](readme.en.md)|[日本語説明](readme.ja.md)

一个使用python3实现的CloudFlare DDNS脚本

## 系统要求

python >=3.6

## 如何运行

### 1.安装python3.6以上版本

略

### 2.下载本仓库并安装需要的库

```bash
git clone https://github.com/LDLDL/cfddns.git
cd cfddns
pip3 install -r requirements.txt
```
### 3.运行 

#### Linux 

Linux系统用户可以使用一键安装脚本，执行后输入相关信息即可  
脚本作为systemd服务开机自启动  

`sudo bash install_as_service.sh` 

#### Windows / MacOS 

1.在终端内进入本项目目录，运行config.py输入相关信息  

Windows下Python命令很可能是python而不是python3  

`python3 ./config.py` 

2.运行cfddns.py

Windows用户需要配置开机执行脚本

## 配置Windows环境下的自动启动方法

1. 将本项目install_as_service内的ddns.vbs,run.bat放置在cfddns.py同目录下,并且修改ddns.vbs, run,bat内的路径为真实运行的路径，本例为C:\cfddns
2. 编辑cfddns.reg内的路径，wscript.exe后面的是路径，前面的wscript.exe不要动。
3. 双击导入cfddns.reg，添加启动项

## 配置

配置之前需要把想配置的域名都配置好解析记录。

例如想要为ddns.example.com配置A和AAAA记录，需要事先在CloudFlare增加一条A记录和AAAA记录，并且IP不能为本机IP。（虽然可以是本机IP，但无法立即验证脚本是否起作用了）

运行install_as_service.sh后，会自动进入配置菜单。

![g00](https://user-images.githubusercontent.com/81149482/129917531-d499ae47-79ab-44b0-910b-e1f2a98fc68c.png)

Email: 输入CloudFlare的登录邮箱即可。

Zones: 对应域名的Overview界面，右下角的 区域ID，点击复制

API Key: 在[这里](https://dash.cloudflare.com/profile/api-tokens)的Global API Key，点击view，输入密码查看

配置完成后按3添加域名

Domain: 要配置的域名，比如ddns.example.com

domain record type(A for v4, AAAA for v6)：输入类型，A是A记录，AAAA是AAAA记录。

结束后如果报错，说明有配置问题，如果提示成功，说明成功配置完成了。

## 增加域名

### Linux

如果已经配置完成的脚本，需要增加其他域名，可按以下步骤操作。

1. 进入本项目文件夹，例如cfddns
2. 执行`sudo python3 ./config.py`
3. 按3，像第一次安装一样增加域名。
4. 重新启动服务，输入`systemctl cfddns restart`

### Windows / MacOS

1.结束cfddns.py运行  
2.执行config.py  
3.运行cfddns.py  

## 可能的问题

若install_as_service.sh出现无法安装到系统服务时，请搜索正在使用着的系统systemd文件存放位置，并将cfddns.service复制进对应的文件夹。

若提示python3不存在，可尝试修改cfddns.service内的python3绝对路径（为确保兼容性，请书写绝对路径，尽管有些系统相对路径依旧可以执行）
