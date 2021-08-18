# CloudFlare DDNS脚本

[English](#English)|[日本語説明](#日本語説明)

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

Zones: 对应域名的Overview界面，右下角的Zone ID，点击复制

API Key: 在[这里](https://dash.cloudflare.com/profile/api-tokens)的Global API Key，点击view，输入密码查看

配置完成后按3添加域名

Domain: 要配置的域名，比如ddns.example.com

domain record type(A for v4, AAAA for v6)：输入类型，A是A记录，AAAA是AAAA记录。

结束后如果报错，说明有配置问题，如果没有任何提示，说明成功配置完成了。

# English

CloudFlare DDNS Python3 Script.

## System Requirement

python >=3.6

## How to run

### 1.Install python3.6 or newer version.

### 2.Install required package and fetch the code.

```bash
pip3 install requests dnspython func-timeout
git clone https://github.com/LDLDL/cfddns.git
```
### 3.run the install_as_service.sh and configure the script.

`bash install_as_service.sh`

## Configure

Before the configure, You need add records which you want to configure.

For example, Add the ddns.example.com and set A Record and AAAA Record. The record can't be your current IP address.

Then run the install_as_service.sh, it will enter the configure menu.

![g00](https://user-images.githubusercontent.com/81149482/129917531-d499ae47-79ab-44b0-910b-e1f2a98fc68c.png)

Email: CloudFlare's login email.

Zones: on the domain page, click the Overview button, copy the Zone ID

API Key: Click [Here](https://dash.cloudflare.com/profile/api-tokens)and view the Global API Key

When you finished, Input 3 and add domain.

Domain: your domain, For example ddns.example.com

domain record type(A for v4, AAAA for v6)：Input type, A for A record, AAAA for AAAA record.

If error messages shows up, that means somethings wrong in configure, please reconfigure it and run again.

# 日本語説明

Python3で開発したCloudFlare DDNSスクリプト。

## 要件

python >=3.6

## 使用方法

### 1.python3.6以降のバージョンをインスト

略

### 2.下記の通りに実行

```bash
pip3 install requests dnspython func-timeout
git clone https://github.com/LDLDL/cfddns.git
```
### 3.install_as_service.shを実行してから配置します

`bash install_as_service.sh`

## 配置

配置に先立って、配置したいドメイン名を配置しております。

例えばddns.example.comは配置したい場合は、まずAレコードまた和AAAAレコードに追加。そのIPアドレスは自分が使っているIPと同じではいけない。

install_as_service.shを実行すると、配置メニューに入ります。

![g00](https://user-images.githubusercontent.com/81149482/129917531-d499ae47-79ab-44b0-910b-e1f2a98fc68c.png)

Email: CloudFlareで登録したメールアドレスです。

Zones: 対応のドメイン名のOverviewページで、右下にあったZone ID

API Key: [ここ](https://dash.cloudflare.com/profile/api-tokens)をクリック、Global API Keyの右にviewをクリックすると、表示された英数字がAPI Keyです。

配置が完成してから3を入力してドメイン名を追加する。

Domain: 配置したいドメイン名。例えばddns.example.com

domain record type(A for v4, AAAA for v6)：レコードの種類。AはAレコード、AAAAはAAAAレコードです。

全部が完了した後で、もしエラー情報が返したら、もう一度API Tokenなど配置したものをしっかり確認するのが必要だと思います。
