#!/usr/bin python3
# -*- coding: utf8 -*-

import logging
import os
import time
import requests
import json
from dns import resolver
from func_timeout import func_set_timeout

sleeptime = 600 #sleep seconds
conf = dict()

if not os.path.exists("conf.json"):
        print("Config file not exists, exiting.")
        exit(1)
with open("conf.json", "r", encoding="utf-8") as fp:
    conf = json.load(fp)
    
zones = conf.get('zones')
email = conf.get('email')
apikey = conf.get('apikey')

if not(zones or email or apikey or conf.get('A') or conf.get('AAAA')):
    print('Incorrect config file, exiting.')
    exit(1)

headers = {
    'X-Auth-Email': email,
    'X-Auth-Key': apikey,
    'cache-control': 'no-cache'
}

look_ip_web = {
    'A':[
        'https://api.ipify.org/',
        'https://api-ipv4.ip.sb/ip',
        'https://v4.ident.me/'
    ],

    'AAAA':[
        'https://ipify.org/',
        'https://api-ipv6.ip.sb/ip',
        'https://v6.ident.me/'
    ]
}

logger = logging.getLogger()
logger.setLevel(logging.INFO)

log_path = './cfddns.log'
log_file = logging.FileHandler(log_path, mode='a')
log_file.setLevel(logging.INFO)
log_file.setFormatter(logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"))

log_console = logging.StreamHandler()
log_console.setLevel(logging.INFO)
log_console.setFormatter(logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"))

logger.addHandler(log_file)
logger.addHandler(log_console)

@func_set_timeout(30)
def get_domain_record(domain: dict, type: str):
    ans = resolver.query(domain.get("name"), type)
    for i in ans.response.answer:
        for j in i.items:
            logger.info(f'Domain: {domain.get("name")}, type: {type} record ip is {j.address}.')
            return j.address
    logger.error(f'Failed to resolve domain: {domain.get("name")}, type: {type}.')

@func_set_timeout(60)
def get_current_ip(type: str):
    index=0
    while index < len(look_ip_web[type]) :
        try:
            current_ip = requests.get(look_ip_web[type][index], timeout=15).text
            if current_ip[-1] == '\n':
                current_ip = current_ip[:-1]
            if type == 'A':
                logger.info(f'Current ipv4 address is {current_ip}.')
            elif type == 'AAAA':
                logger.info(f'Current ipv6 address is {current_ip}.')
            return current_ip
        except Exception as err:
            logger.warning(f'Failed to get ip by using {look_ip_web[type][index]}, err: "{err}"')
            index+=1
    logger.error('Failed to get ip after using all web.')
    return False

@func_set_timeout(30)
def update_domain(domain: dict, type: str, ip: str):
    data = {
        "type": type,
        "name": domain.get('name'),
        "content": ip,
        "ttl": 120,
        "proxied": False
    }
    url = f"https://api.cloudflare.com/client/v4/zones/{zones}/dns_records/{domain.get('dns_record')}"
    response = json.loads(requests.put(url, headers=headers, data=json.dumps(data)).text)
    if response.get('success'):
        logger.info(f'Updated domain record of {domain.get("name")}, type: {type} success')
    else:
        logger.error(f'Failed to update domain record of {domain.get("name")}, type: {type}')
    return response.get('success')

def try_func(times,func,*args):
    result = False
    while (result == False) and (times > 0):
        try:
            logger.debug(f'Calling function "{func.__name__}".')
            result = func(*args)
        except BaseException as e:
            logger.warning(f'Calling function "{func.__name__}" timeout or receive a exception: "{e}", kill it.')
            result = False
        times-=1
    return result

def check_domain():
    logger.info('Checking your domains.')

    if len(conf.get('A')):
        current_ipv4 = try_func(5, get_current_ip, 'A')
        if not current_ipv4:
            logger.info('sleep 10 minutes')
            return
        
        for domain in conf.get('A'):
            domain_record_ipv4 = try_func(5, get_domain_record, domain, 'A')
            if not domain_record_ipv4:
                logger.warning(f'Ignore domain {domain.get("name")}, type: A')
                continue
            if current_ipv4 != domain_record_ipv4:
                logger.info('IPv4 address changed.')
                try_func(5, update_domain, domain, 'A', current_ipv4)
    
    if len(conf.get('AAAA')):
        current_ipv6 = try_func(5, get_current_ip, 'AAAA')
        if not current_ipv6:
            logger.info('sleep 10 minutes')
            return
        
        for domain in conf.get('AAAA'):
            domain_record_ipv6 = try_func(5, get_domain_record, domain, 'AAAA')
            if not domain_record_ipv6:
                logger.warning(f'Ignore domain {domain.get("name")}, type: AAAA')
                continue
            if current_ipv6 != domain_record_ipv6:
                logger.info('IPv6 address changed.')
                try_func(5, update_domain, domain, 'AAAA', current_ipv6)
    
    logger.info('sleep 10 minutes')

if __name__ == "__main__":
    while True:
        check_domain()
        time.sleep(sleeptime)
