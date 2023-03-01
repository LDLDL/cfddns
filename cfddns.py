#!/usr/bin/python3
# -*- coding: utf8 -*-

import logging
import os
import time
import json
import pathlib
from argparse import ArgumentParser

import requests
from func_timeout import func_set_timeout

import sources


parser = ArgumentParser(description='CloudFlare DDNS')
parser.add_argument('--conf', type=pathlib.Path, default='conf.json')
parser.add_argument('--log', type=pathlib.Path)
parser.add_argument('--onetime', action='store_true')
parser.add_argument('--usedns', action='store_true')
parser.add_argument('--nolog', action='store_true')
args = parser.parse_args()

conf = dict()
if not os.path.exists(args.conf):
    print("Config file not exists, exiting.")
    exit(1)
with open(args.conf, "r", encoding="utf-8") as fp:
    conf = json.load(fp)

zones = conf.get('zones')
email = conf.get('email')
apikey = conf.get('apikey')

if not (zones or email or apikey or conf.get('A') or conf.get('AAAA')):
    print('Incorrect config file, exiting.')
    exit(1)

headers = {
    'X-Auth-Email': email,
    'X-Auth-Key': apikey,
    'cache-control': 'no-cache'
}

ip_sources = {
    'A': [
        sources.cf_trace('cf-ns.com', 4),
        sources.ipip(4),
        sources.cf_trace('162.159.36.1'),
        sources.simple('https://v4.ident.me/'),
        sources.cf_trace('1.1.1.1'),
        sources.simple('https://api.ipify.org/'),
    ],

    'AAAA': [
        sources.cf_trace('cf-ns.com', 6),
        sources.ipip(6),
        sources.cf_trace('2606:4700:4700::1111'),
        sources.simple('https://v6.ident.me/'),
        sources.cf_trace('2606:4700:4700::64'),
    ]
}

logger = logging.getLogger()
logger.setLevel(logging.INFO)

if not args.nolog and (not args.onetime or args.log):
    if args.log:
        log_path = args.log
    elif os.path.exists('/tmp'):
        log_path = '/tmp/cfddns.log'
    else:
        log_path = os.path.join(os.getcwd(), 'cfddns.log')
    log_file = logging.FileHandler(log_path, mode='a')
    log_file.setLevel(logging.INFO)
    log_file.setFormatter(logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"))
    logger.addHandler(log_file)

log_console = logging.StreamHandler()
log_console.setLevel(logging.INFO)
log_console.setFormatter(logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"))
logger.addHandler(log_console)


@func_set_timeout(30)
def get_domain_record_cfapi(domain: dict, typ: str):
    url = f"https://api.cloudflare.com/client/v4/zones/{zones}/dns_records"
    response = json.loads(requests.get(url, {
        "type": typ,
        "name": domain.get("name"),
    }, headers=headers).content)
    for i in response["result"]:
        logger.info(f'Domain: {domain.get("name")}, typ: {typ} record ip is {i["content"]}.')
        return i["content"]
    logger.error(f'Failed to resolve domain: {domain.get("name")}, typ: {typ}.')


@func_set_timeout(30)
def get_domain_record_dns(domain: dict, typ: str):
    ans = resolver.resolve(domain.get("name"), typ, search=True)
    for i in ans.response.answer:
        for j in i.items:
            logger.info(f'Domain: {domain.get("name")}, typ: {typ} record ip is {j.address}.')
            return j.address
    logger.error(f'Failed ro resolve domain: {domain.get("name")}, typ:{typ}.')


get_domain_record = get_domain_record_cfapi
if args.usedns:
    from dns import resolver
    get_domain_record = get_domain_record_dns


@func_set_timeout(60)
def get_current_ip(typ: str):
    for source in ip_sources[typ]:
        try:
            current_ip = source(10)
            if typ == 'A':
                logger.info(f'Current ipv4 address is {current_ip}.')
            elif typ == 'AAAA':
                logger.info(f'Current ipv6 address is {current_ip}.')
            return current_ip
        except Exception as err:
            logger.warning(f'Failed to get ip by using {source}, err: "{err}"')
    logger.error('Failed to get ip after using all sources.')
    return False


@func_set_timeout(30)
def update_domain(domain: dict, typ: str, ip: str):
    data = {
        "type": typ,
        "name": domain.get('name'),
        "content": ip,
        "ttl": 60,
        "proxied": False
    }
    url = f"https://api.cloudflare.com/client/v4/zones/{zones}/dns_records/{domain.get('dns_record')}"
    response = json.loads(requests.put(url, headers=headers, data=json.dumps(data)).text)
    if response.get('success'):
        logger.info(f'Updated domain record of {domain.get("name")}, typ: {typ} success')
    else:
        logger.error(f'Failed to update domain record of {domain.get("name")}, typ: {typ}')
    return response.get('success')


def try_func(times, func, *args):
    result = False
    while (result == False) and (times > 0):
        try:
            logger.debug(f'Calling function "{func.__name__}".')
            result = func(*args)
        except BaseException as e:
            logger.warning(f'Calling function "{func.__name__}" timeout or receive a exception: "{e}", kill it.')
            result = False
        times -= 1
    return result


def check_domain():
    logger.info('Checking your domains.')

    if len(conf.get('A')):
        current_ipv4 = try_func(5, get_current_ip, 'A')
        if current_ipv4:
            for domain in conf.get('A'):
                domain_record_ipv4 = try_func(5, get_domain_record, domain, 'A')
                if not domain_record_ipv4:
                    logger.warning(f'Ignore domain {domain.get("name")}, typ: A')
                    continue
                if current_ipv4 != domain_record_ipv4:
                    logger.info('IPv4 address changed.')
                    try_func(5, update_domain, domain, 'A', current_ipv4)

    if len(conf.get('AAAA')):
        current_ipv6 = try_func(5, get_current_ip, 'AAAA')
        if current_ipv6:
            for domain in conf.get('AAAA'):
                domain_record_ipv6 = try_func(5, get_domain_record, domain, 'AAAA')
                if not domain_record_ipv6:
                    logger.warning(f'Ignore domain {domain.get("name")}, typ: AAAA')
                    continue
                if current_ipv6 != domain_record_ipv6:
                    logger.info('IPv6 address changed.')
                    try_func(5, update_domain, domain, 'AAAA', current_ipv6)


if __name__ == "__main__":
    sleeptime = 600 # sleep seconds

    if args.onetime:
        check_domain()
    else:
        while True:
            check_domain()
            logger.info(f'sleep {sleeptime} seconds')
            time.sleep(sleeptime)

