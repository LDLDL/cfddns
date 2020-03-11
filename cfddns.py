#！/usr/bin/env python3
# -*- coding: utf8 -*-

import logging
import os
import time
import requests
import json
from dns import resolver
from func_timeout import func_set_timeout

import config

sleeptime=600#sleep seconds
domain=config.domain
zones=config.zones
dnsrecords=config.dnsrecords
type=config.type

headers = config.headers

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

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#log_path = os.getcwd() + '/cfddns.log'
log_path = './cfddns.log'
log_file = logging.FileHandler(log_path, mode='w')
log_file.setLevel(logging.INFO)
log_file.setFormatter(logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"))

logger.addHandler(log_file)

@func_set_timeout(30)
def get_domain_record():
    ans = resolver.query(domain,type)
    for i in ans.response.answer:
        for j in i.items:
            logger.info('Domain record ip is {0}.'.format(j.address))
            return j.address
    logger.error('Fail to resolve domain: {0}.'.format(domain))

@func_set_timeout(30)
def get_current_ip():
    index=0
    while index < len(look_ip_web[type]) :
        try:
            current_ip = requests.get(look_ip_web[type][index]).text
            if current_ip[-1] == '\n':
                current_ip = current_ip[:-1]
            logger.info('Current ip address is {0}.'.format(current_ip))
            return current_ip
        except:
            logger.warning('Fail to get ip by using {0}.'.format(look_ip_web[type][index]))
            index+=1
    logger.error('Fail to get ip after using all web.')
    return False

@func_set_timeout(30)
def update_domain(ip):
    data = {"type":type,"name":domain,"content":ip,"ttl":120,"proxied":False}
    response = json.loads(requests.put(url,headers=headers,data=json.dumps(data)).text)
    if response['success']:
        logger.info('Update domain record success')
    else:
        logger.error('Fail to update domain record')
    return response['success']

def try_func(times,func,*args):
    result = False
    while (result == False) and (times > 0):
        try:
            logger.debug('Calling function "{0}".'.format(func.__name__))
            result = func(*args)
        except:
            logger.warning('Calling function "{0}" timeout or receive a exception, kill it.'.format(func.__name__))
            result = False
        times-=1
    return result


if __name__ == '__main__':
    while True:
        print('\n[check your domain, system time is: ' + time.strftime("%H:%M:%S") + ']')
        logger.info('Checking domain.')

        domain_record_ip = try_func(5,get_domain_record) 
        if(domain_record_ip == False):
            logger.info('Sleep 10 minutes.')
            print('fail to resolve your domain, retry next time')
            time.sleep(sleeptime)
            continue

        current_ip = try_func(5,get_current_ip)
        if(current_ip == False):
            logger.info('Sleep 10 minutes.')
            print('fail to get your current ip address, retry next time')
            time.sleep(sleeptime)
            continue

        print('your domain record is {0}'.format(domain_record_ip))
        print('your current ip is {0}'.format(current_ip))

        if(current_ip != domain_record_ip):
            logger.info('Ip address changed.')
            print('ip address changed')
            if(try_func(5,update_domain,current_ip)):
                print('domain updated')
            else:
                print('update domain fail, retry next time')
        else:
            print('ip address dose not change')
        logger.info('Sleep 10 minutes.')
        time.sleep(sleeptime)
