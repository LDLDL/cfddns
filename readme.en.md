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

## Add new domain

If you want to add more domain, Just follow this guide:

1. Stop the service.`systemctl cfddns stop`
2. Enter this project's folder. For example cd cfddns
3. Run `python3 ./init.py`
4. Press 3, Just add the domain likes new install.
5. Input `cat conf.json > /srv/cfddns/conf.json`
6. Start the service. `systemctl cfddns start`

## Possibly issues

If when you run the install_as_service.sh and got some errors, Please search how to install systemd service with your system name. and copy the cfddns.service to your systemd folder.

If it display the python3 is not exist, you can try to modify the python3's path which in cfddns.service
