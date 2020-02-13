#！/usr/bin/env python3
# -*- coding: utf8 -*-

import time
import requests
import json
from dns import resolver
from func_timeout import func_set_timeout

sleeptime=600#sleep seconds
domain=''#your domain
zones=''#your zone id
dnsrecords=''#your dns records, see cloudflare's dns api document
type='A' # A for v4, AAAA for v6 

headers = {
    'X-Auth-Email': '',#your email
    'X-Auth-Key': '',#your apikey
    'cache-control': 'no-cache'
}

url = 'https://api.cloudflare.com/client/v4/zones/{0}/dns_records/{1}'.format(zones,dnsrecords)

look_ip_web = {
    'A':[
        'http://ipv4.icanhazip.com',
        'https://v4.ident.me/'
    ],

    'AAAA':[
        'http://ipv6.icanhazip.com',
        'https://v6.ident.me'
    ]
}

@func_set_timeout(30)
def get_domain_record():
    ans = resolver.query(domain,type)
    for i in ans.response.answer:
        for j in i.items:
            return j.address

@func_set_timeout(30)
def get_current_ip():
    index=0
    while index < len(look_ip_web[type]) :
        try:
            current_ip = requests.get(look_ip_web[type][index]).text
            if(current_ip[-1] == '\n'):
                current_ip = current_ip[:-1]
                return current_ip
        except:
            index+=1
    return False

@func_set_timeout(30)
def update_domain(ip):
    data = {"type":type,"name":domain,"content":ip,"ttl":120,"proxied":False}
    response = json.loads(requests.put(url,headers=headers,data=json.dumps(data)).text)
    return response['success']

def try_func(times,func,*args):
    result = False
    while (result == False) and (times > 0):
        try:
            result = func(*args)
        except:
            result = False
        times-=1
    return result


if __name__ == '__main__':
    while True:
        print('\n[check your domain, system time is: ' + time.strftime("%H:%M:%S") + ']')

        domain_record_ip = try_func(5,get_domain_record) 
        if(domain_record_ip == False):
            print('fail to resolve your domain, retry next time')
            time.sleep(sleeptime)
            continue

        current_ip = try_func(5,get_current_ip)
        if(current_ip == False):
            print('fail to get your current ip address, retry next time')
            time.sleep(sleeptime)
            continue

        print('your domain record is {0}'.format(domain_record_ip))
        print('your current ip is {0}'.format(current_ip))

        if(current_ip != domain_record_ip):
            print('ip address changed')
            if(try_func(5,update_domain,current_ip)):
                print('domain updated')
            else:
                print('update domain fail, retry next time')
        else:
            print('ip address dose not change')
        time.sleep(sleeptime)