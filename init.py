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
    email = input("Email:")
    zones = input("Zones:")
    apikey = input("API key:")
    conf['zones'] = zones
    conf['email'] = email
    conf['apikey'] = apikey

def show_api(conf):
    print()
    print(f"Zone: {conf.get('zones')}")
    print(f"Email: {conf.get('email')}")
    print(f"API key: {conf.get('apikey')}")

def add_domian(conf):
    if not (conf.get('zones') or conf.get('email') or conf.get('apikey')):
        print('Please setup api key first.')
        return
    domain = input("domain:")
    type = input("domain record type(A for v4, AAAA for v6):")
    if type != "A" and type != "AAAA":
        print("Type must be A or AAAA")
        return
    domain_id = get_domain_id(domain, conf.get('zones'), conf.get('email'), conf.get('apikey'), type)
    if domain_id:
        conf.get(type).append({
            "name": domain,
            "dns_record": domain_id,
        })
    else:
        print('No such domain name, please add it first.')

def list_domains(conf):
    i = 1
    for domain in conf.get('A'):
        print(f'{i}. Name: {domain.get("name")}, Type: A')
        print()
        i += 1
    for domain in conf.get('AAAA'):
        print(f'{i}. Name: {domain.get("name")}, Type: AAAA')
        print()
        i += 1

def del_domain(conf):
    list_domains(conf)
    fn = input("Input delete index, input 0 to cancel:")
    if fn == '0':
        return
    try:
        index = int(fn) - 1
        if index >= len(conf.get('A')):
            conf.get('AAAA').pop(index - len(conf.get('A')))
        else:
            conf.get('A').pop(index)
    except:
        print('Index not valid.')

if __name__ == "__main__":
    conf = {
        "zones": "",
        "email": "",
        "apikey": "",

        "A": [],
        "AAAA": []
    }
    if os.path.exists('conf.json'):
        with open('conf.json', 'r', encoding='utf-8') as fp:
            conf = json.load(fp)
    while True:
        print()
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
        elif fn == '3':
            add_domian(conf)
        elif fn == '4':
            del_domain(conf)
        elif fn == 'q':
            if os.path.exists('conf.json'):
                os.remove('conf.json')
            with open('conf.json', 'w', encoding='utf-8') as fp:
                json.dump(conf, fp)
            exit(0)
        else:
            continue
            