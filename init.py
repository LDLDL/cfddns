#！/usr/bin/env python3
# -*- coding: utf8 -*-

import requests
import json
import os

def get_domain_id(domain,zones,email,apikey,type):
    url = 'https://api.cloudflare.com/client/v4/zones/{0}/dns_records?type={1}&domain={2}'.format(zones,type,domain)
    headers = {
    'X-Auth-Email': email,
    'X-Auth-Key': apikey,
    'cache-control': 'no-cache'
    }
    response = json.loads(requests.get(url,headers=headers).text)
    return response['result'][0]['id']

domain = input("domain:")
email = input("email:")
zones = input("zones:")
apikey = input("apikey:")
type = input("domain record type(A for v4, AAAA for v6):")

domain_id = get_domain_id(domain,zones,email,apikey,type)

conf = "domain='{0}'\nzones='{1}'\ndnsrecords='{2}'\ntype='{3}'\nheaders = {{'X-Auth-Email': '{4}', 'X-Auth-Key': '{5}', 'cache-control': 'no-cache'}}".format(domain,zones,domain_id,type,email,apikey)

with open('./config.py','w') as c:
    c.write(conf)