# CloudFlare DDNS脚本

一个使用python3实现的CloudFlare DDNS脚本

## 系统要求

python >=3.6

## 如何运行

### 1.安装python3.6以上版本

略

### 2.安装以下包并下载本仓库

```bash
pip3 install requests dnspython func-timeout
git clone https://github.com/LDLDL/cfddns.git
```
### 3.运行install_as_service.sh并输入相关信息

`bash install_as_service.sh`

## 配置

配置之前需要把想配置的域名都配置好解析记录。

例如想要为ddns.example.com配置A和AAAA记录，需要事先增加一条A记录和AAAA记录，并且IP不能为本机IP。

运行install_as_service.sh后，会自动进入配置菜单。

![g00](https://user-images.githubusercontent.com/81149482/129917531-d499ae47-79ab-44b0-910b-e1f2a98fc68c.png)

Email: 输入CloudFlare的登录邮箱即可。

Zones:对应域名的Overview界面，右下角的Zone ID，点击复制

API Key:在[这里](https://dash.cloudflare.com/profile/api-tokens)的Global API Key，点击view，输入密码查看

配置完成后按3添加域名

Domain；要配置的域名，比如ddns.example.com

domain record type(A for v4, AAAA for v6)：输入类型，A是A记录，AAAA是AAAA记录。

结束后如果报错，说明有配置问题，如果没有任何提示，说明成功配置完成了。
