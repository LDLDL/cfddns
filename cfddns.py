#！/usr/bin/env python3
# -*- coding: utf8 -*-

import time
import requests
import json
from dns import resolver

sleeptime=600#sleep seconds
domain=''#your domain
zones=''#your zone id
dnsrecords=''#your dns records

headers = {
    'X-Auth-Email': ''#your email
    'X-Auth-Key': ''#your apikey
    'cache-control': 'no-cache'
}

url = 'https://api.cloudflare.com/client/v4/zones/{0}/dns_records/{1}'.format(zones,dnsrecords)

checkipweblist4=[
    'http://ipv4.icanhazip.com',
    'https://v4.ident.me/',
]

def getdomianrecord():
    try:
        ans = resolver.query(domain,'A')
    except:
        return False
    for i in ans.response.answer:
        for j in i.items:
            return j.address

def getcurrentip():
    index=0
    while(index<len(checkipweblist4)):
        try:
            currentip=requests.get(checkipweblist[index]).text
            if(currentip[-1]=='\n'):
                currentip=currentip[:-1]
            return currentip
        except:
            index+=1
            continue
    return False

def updatedomain(ip):
    data = {"type":"A","name":domain,"content":ip,"ttl":120,"proxied":False}
    response = json.loads(requests.put(url,headers=headers,data=json.dumps(data)).text)
    return response['success']

if __name__ == '__main__':
    retrytimen=0
    retrytimeo=0
    while(1):
        print('\n[check your domain,system time is: ' + time.strftime("%H:%M:%S") + ']')

        domianrecordip=getdomianrecord()
        while(domianrecordip==False and retrytimeo<5):
            print('fail to resolve your domain, retry times:{0}...'.format(retrytimeo+1))
            retrytimeo+=1
            domianrecordip=getdomianrecord()
        if(domianrecordip==False):
            print('fail to resolve your domain, retry next time')
            time.sleep(sleeptime)
            continue

        currentip=getcurrentip()
        while (currentip==False and retrytimen<5):
            print('fail to get your current ip address, retry times:{0}...'.format(retrytimen+1))
            retrytimen+=1
            currentip=getcurrentip()
        if(currentip==False):
            print('fail to get your current ip address, retry next time')
            time.sleep(sleeptime)
            continue

        if(currentip != domianrecordip):
            print('your domain record is {0}'.format(domianrecordip))
            print('your current ip is {0}'.format(currentip))
            print('ip address changed')
            if(updatedomain(currentip)):
                print('domain updated')
            else:
                print('update domain fail, retury next time')
        else:
            print('your domain record is {0}'.format(domianrecordip))
            print('your current ip is {0}'.format(currentip))
            print('ip adress dose not change')
        retrytimen=0
        retrytimeo=0
        time.sleep(sleeptime)
