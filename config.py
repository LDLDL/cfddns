#！/usr/bin/env python3
# -*- coding: utf8 -*-

import requests
import json
import os
import platform

global_timeout = 30


if platform.system().lower() != 'linux':
    conf_file_path = '/srv/cfddns/conf.json'
else:
    conf_file_path = './conf.json'


def get_domain_id(domain, zones, email, apikey, record_type):
    try:
        url = f'https://api.cloudflare.com/client/v4/zones/{zones}/dns_records?type={record_type}&domain={domain}'
        headers = {
            'X-Auth-Email': email,
            'X-Auth-Key': apikey,
            'cache-control': 'no-cache'
        }
        response = json.loads(requests.get(url, headers=headers, timeout=global_timeout).text)
        for record in response['result']:
            if record.get('name') == domain:
                return record.get('id')
        return None
    except Exception as e:
        print(f'Fail to get domain ID from CloudFlare API with reason:{e}')
        return None

def set_api(conf):
    try:
        print()
        email = input("Email:")
        zones = input("Zones:")
        apikey = input("Global API key:")

        url = f'https://api.cloudflare.com/client/v4/zones/{zones}'
        headers = {
            'X-Auth-Email': email,
            'X-Auth-Key': apikey,
            'cache-control': 'no-cache'
        }
        response = json.loads(requests.get(url, headers=headers, timeout=global_timeout).text)
        if response.get('success'):
            conf['zones'] = zones
            conf['email'] = email
            conf['apikey'] = apikey
            print('\nSuccess.　Press ENTER to continue.')
        else:
            print('\nGlobal API key or Email or Zone not valid.')
        print()
        input()
    except Exception as e:
        print(f'Fail to set API information with reason: {e}')

def show_api(conf):
    print(f"\nZone: {conf.get('zones')}\nEmail: {conf.get('email')}\nGlobal API key: {conf.get('apikey')}")
    input()

def add_domain(conf):
    print()
    if not (conf.get('zones') or conf.get('email') or conf.get('apikey')):
        print('Please setup Global API key first.\n')
        input()
        return
    domain = input("Domain:")
    record_type = input("Domain record type(A for v4, AAAA for v6):")
    if record_type != "A" and record_type != "AAAA":
        print("\nType must be A or AAAA.\n")
        input()
        return
    domain_id = get_domain_id(domain, conf.get('zones'), conf.get('email'), conf.get('apikey'), record_type)
    if domain_id:
        conf.get(record_type).append({
            "name": domain,
            "dns_record": domain_id,
        })
        print('\nSuccess.　Press ENTER to continue.\n')
    else:
        print('\nNo such domain name, please set it first, then re-add it.\n')
    input()

def list_domains(conf):
    print()
    if not (conf.get('A') or conf.get('AAAA')):
        print('Empty.\n')
        return
    i = 1
    for domain in conf.get('A'):
        print(f'{i}. Name: {domain.get("name")}, Type: A')
        i += 1
    for domain in conf.get('AAAA'):
        print(f'{i}. Name: {domain.get("name")}, Type: AAAA')
        i += 1

def del_domain(conf):
    if not (conf.get('A') or conf.get('AAAA')):
        print('\nEmpty.\n')
        input()
        return
    list_domains(conf)
    user_input = input("Input delete index, input 0 to cancel:")
    if user_input == '0' or user_input == '':
        return
    try:
        index = int(user_input) - 1
        if index >= len(conf.get('A')):
            conf.get('AAAA').pop(index - len(conf.get('A')))
        else:
            conf.get('A').pop(index)
        print('\nSuccess.　Press ENTER to continue.\n')
    except Exception as e:
        print(f'\nIndex not valid.\nAdditional error message: {e}')
    input()

if __name__ == "__main__":
    config = {
        "zones": "",
        "email": "",
        "apikey": "",

        "A": [],
        "AAAA": []
    }
    if os.path.exists(conf_file_path):
        with open(conf_file_path, 'r', encoding='utf-8') as fp:
            config = json.load(fp)
    while True:
        print("0 Set API key\n1 Show API key\n2 List domains\n3 Add domain\n4 Delete domain\nq Save and quit\n")
        fn = input("Please Input:")
        if fn == '0':
            set_api(config)
        elif fn == '1':
            show_api(config)
        elif fn == '2':
            list_domains(config)
            input()
        elif fn == '3':
            add_domain(config)
        elif fn == '4':
            del_domain(config)
        elif fn == 'q':
            if os.path.exists(conf_file_path):
                os.remove(conf_file_path)
            with open(conf_file_path, 'w', encoding='utf-8') as fp:
                json.dump(config, fp)
            exit(0)
        else:
            continue
            
