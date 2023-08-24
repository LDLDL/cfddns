# Use new CloudFlare DDns Go implement
<br>

[LDLDL/cfddns-go](https://github.com/LDLDL/cfddns-go)  

<br>

# CloudFlare DDNS脚本

[English](readme.en.md)|[日本語説明](readme.ja.md)

一个使用python3实现的CloudFlare DDNS脚本

## 运行要求

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

### 运行参数

- [--conf] 文件路径，用于指定载入的配置文件路径，默认为当前文件夹下的conf.json。
- [--log] 文件路径，用于指定日志文件的保存路径。
- [--onetime] 仅进行一次地址检查后就退出程序。适用于Crontab计划任务。
- [--usedns] 获取当前域名的IP时不使用CloudFlare API方式检查，而是使用DNS解析域名, 使用此选项需要额外安装dnspython库。
- [--nolog] 不记录日志到文件，只对控制台输出日志。

#### Linux Systemd 服务安装

Linux系统用户可以使用一键安装脚本，执行后输入相关信息即可  
脚本作为systemd服务开机自启动  

`sudo bash install_systemd_service.sh` 

脚本会自动运行config.py来配置必须内容。

若系统内没有Systemd，见下述计划任务使用方式。

#### 通用系统

##### 手动运行

1. 在终端内进入本项目目录，运行`python3 config.py`并输入相关信息  
2. 运行cfddns.py

##### 计划任务

1. 在终端内进入本项目目录，运行`python3 config.py`输入相关信息
2. 在计划任务中加入命令

`python3 {path to cfddns.py} --onetime --conf {path to conf.json}`

请替换花括号内的路径(需为绝对路径)  
onetime模式下默认不将日志输出到文件，可用--log参数将日志保存到指定文件  

例如Crontab可以使用以下配置  

`*/10 * * * * /usr/local/bin/python3 /home/user/cfddns/cfddns.py --onetime --conf /home/user/cfddns/conf.json`

含义为每隔十分钟检查一次IP并根据IP变动情况上报地址。  

#### Windows 自启动服务

1. 将本项目Windows service内的ddns.vbs,run.bat放置在cfddns.py同目录下,并且修改ddns.vbs, run,bat内的路径为真实运行的路径，本例为C:\cfddns
2. 编辑cfddns.reg内的路径，wscript.exe后面的是路径，前面的wscript.exe不要动。
3. 双击导入cfddns.reg，添加启动项

## 配置

配置之前需要把想配置的域名都配置好解析记录。

例如想要为ddns.example.com配置A和AAAA记录，需要事先在CloudFlare增加一条A记录和AAAA记录，A和AAAA记录最好不要指向本机IP(虽然可以指向本机IP，但无法立即验证DDNS是否起作用了)

运行`python3 config.py`进入配置菜单。

![g00](https://user-images.githubusercontent.com/81149482/129917531-d499ae47-79ab-44b0-910b-e1f2a98fc68c.png)

输入0配置API Key

Email: 输入CloudFlare的登录邮箱即可。

Zones: 对应域名的Overview界面，右下角的 区域ID，点击复制

API Key: 在[这里](https://dash.cloudflare.com/profile/api-tokens)的Global API Key，点击view，输入密码查看

配置完成后按3添加域名

Domain: 要配置的域名，比如ddns.example.com

domain record type(A for v4, AAAA for v6)：输入类型，A是A记录，AAAA是AAAA记录。

结束后如果报错，说明有配置问题，如果提示成功，说明成功配置完成了。

## 增加域名

### Linux Systemd 服务

如果已经配置完成的脚本，需要增加其他域名，可按以下步骤操作。

1. 执行config.py
2. 增加或删除域名。
3. 重新启动服务，输入`systemctl restart cfddns`

### 计划任务

1. 执行config.py
2. 增加或删除域名。

### 通用使用方法

1. 结束cfddns.py运行  
2. 执行config.py  
3. 重新运行cfddns.py  

## 可能存在的问题

若install_systemd_service.sh出现无法安装到系统服务时，请搜索当前系统的systemd文件存放位置，并将cfddns.service复制进对应的文件夹。

若提示python3不存在，可尝试修改cfddns.service内的python3绝对路径(为确保兼容性，请输入绝对路径，尽管有些系统相对路径依旧可以执行)
