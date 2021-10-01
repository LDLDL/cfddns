#！/usr/bin/env python3
# -*- coding: utf8 -*-

import requests
import json
import os

def get_domain_id(domain, zones, email, apikey, type):
    url = f'https://api.cloudflare.com/client/v4/zones/{zones}/dns_records?type={type}&domain={domain}'
    headers = {
        'X-Auth-Email': email,
        'X-Auth-Key': apikey,
        'cache-control': 'no-cache'
    }
    response = json.loads(requests.get(url, headers=headers).text)
    for record in response['result']:
        if record.get('name') == domain:
            return record.get('id')
    return None

def set_api(conf):
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
    response = json.loads(requests.get(url, headers=headers).text)
    if response.get('success'):
        conf['zones'] = zones
        conf['email'] = email
        conf['apikey'] = apikey
        print('\nSuccess.　Press ENTER to continue.')
    else:
        print('\nGlobal API key or Email or Zone not valid.')
    print()
    input()

def show_api(conf):
    print(f"\nZone: {conf.get('zones')}")
    print(f"Email: {conf.get('email')}")
    print(f"Global API key: {conf.get('apikey')}")
    input()

def add_domain(conf):
    print()
    if not (conf.get('zones') or conf.get('email') or conf.get('apikey')):
        print('Please setup Global API key first.\n')
        input()
        return
    domain = input("Domain:")
    type = input("Domain record type(A for v4, AAAA for v6):")
    if type != "A" and type != "AAAA":
        print("\nType must be A or AAAA\n")
        input()
        return
    domain_id = get_domain_id(domain, conf.get('zones'), conf.get('email'), conf.get('apikey'), type)
    if domain_id:
        conf.get(type).append({
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
    fn = input("Input delete index, input 0 to cancel:")
    if fn == '0' or fn == '':
        return
    try:
        index = int(fn) - 1
        if index >= len(conf.get('A')):
            conf.get('AAAA').pop(index - len(conf.get('A')))
        else:
            conf.get('A').pop(index)
        print('\nSuccess.　Press ENTER to continue.\n')
    except:
        print('\nIndex not valid.\n')
    input()

if __name__ == "__main__":
    conf = {
        "zones": "",
        "email": "",
        "apikey": "",

        "A": [],
        "AAAA": []
    }
    if os.path.exists('/srv/cfddns/conf.json'):
        with open('/srv/cfddns/conf.json', 'r', encoding='utf-8') as fp:
            conf = json.load(fp)
    while True:
        print("0 Set API key")
        print("1 Show API key")
        print("2 List domains")
        print("3 Add domain")
        print("4 Delete domain")
        print("q Save and quit")
        fn = input("Please Input:")
        if fn == '0':
            set_api(conf)
        elif fn == '1':
            show_api(conf)
        elif fn == '2':
            list_domains(conf)
            input()
        elif fn == '3':
            add_domain(conf)
        elif fn == '4':
            del_domain(conf)
        elif fn == 'q':
            if os.path.exists('/srv/cfddns/conf.json'):
                os.remove('/srv/cfddns/conf.json')
            if not os.path.exists('/srv/cfddns'):
                os.mkdir('/srv/cfddns')
            with open('/srv/cfddns/conf.json', 'w', encoding='utf-8') as fp:
                json.dump(conf, fp)
            exit(0)
        else:
            continue
            