# English

CloudFlare DDNS Python3 Script.

## System Requirement

python >=3.6

## How to run

### 1.Install python3.6 or newer version.

### 2.Fetch the repo and install required packages.

```bash
git clone https://github.com/LDLDL/cfddns.git
cd cfddns
pip3 install -r requirements.txt
```
### 3.Run the script

### Parameter

[--conf] File path. It's use for load the specific config. default is conf.json on current directory.

[--log] File path. It's use for save log file.

[--onetime] Only report IP address one time. It's useful for Crontab.

[--usedns] When checking the IP address of current domain, use DNS instead of CloudFlare API.

[--nolog] Don't write the log. Only output the log to console.

#### Linux systemd service

You can use command: 

`sudo bash install_systemd_service.sh`

to install this script and set it as system service.

#### Common OS

##### Run it manually

1. On the terminal, cd to this project, then run `python3 config.py` to configure.  
2. Run `python3 cfddns.py`

##### Scheduled Tasks

1. On the terminal, cd to this project, then run `python3 config.py` to configure.  
2. Add this command in your scheduled tasks

`python3 {path to cfddns.py} --onetime --conf {path to conf.json}`

Please replace the path to cfddns.py with your real file path.(absolute path)

In the onetime mode, default it won't log to file. You can use --log filename parameter to write it to the specific file.

#### The auto-start on boot of Windows user

1. copy the ddns.vbs,run.bat which on the install_systemd_service folder. then edit the actually path on the ddns.vbs and run.bat. This example is C:\cfddns
2. Edit the cfddns.reg path. the string after wscript.exe is the path, don't edit wscript.exe.
3. double click the cfddns.reg to enable it.

## Configure

Before the configure, You need add records which you want to configure.

For example, Add the ddns.example.com and set A Record and AAAA Record in the CloudFlare control panel. The record can't be your current IP address.(If the IP address are set to your current IP address, You can't know does this program works)

Then run the install_systemd_service.sh, it will enter the configure menu.

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

### Linux

1. Enter this project's folder. For example cd cfddns
2. Run `sudo python3 ./config.py`
3. Press 3, Just add the domain likes new install.
4. Restart the service. `systemctl cfddns restart`

### Common OS

1. Close the cfddns.py
2. Re run config.py
3. Start cfddns.py

## Possibly issues

If when you run the install_systemd_service.sh and got some errors, Please search how to install systemd service with your system name. and copy the cfddns.service to your systemd folder.

If it display the python3 is not exist, you can try to modify the python3's path which in cfddns.service.(If you are using Windows, try to change python3 to python.) There must be input full path of python3. Some system can run with relative path but to keep it stable, full path is recommend.
