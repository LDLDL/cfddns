import requests
import re

from ._with_str import _WithStr

IPV4SEG = r'(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])'
ipv4_re = re.compile(r'(?:(?:' + IPV4SEG + r'\.){3}' + IPV4SEG + r')')

IPV6SEG = r'(?:(?:[0-9a-fA-F]){1,4})'
IPV6GROUPS = (
    r'(?:' + IPV6SEG + r':){7}' + IPV6SEG,  # 1:2:3:4:5:6:7:8
    r'(?:' + IPV6SEG + r':){1,7}:',  # 1::                                 1:2:3:4:5:6:7::
    r'(?:' + IPV6SEG + r':){1,6}:' + IPV6SEG,  # 1::8               1:2:3:4:5:6::8   1:2:3:4:5:6::8
    r'(?:' + IPV6SEG + r':){1,5}(?::' + IPV6SEG + r'){1,2}',  # 1::7:8             1:2:3:4:5::7:8   1:2:3:4:5::8
    r'(?:' + IPV6SEG + r':){1,4}(?::' + IPV6SEG + r'){1,3}',  # 1::6:7:8           1:2:3:4::6:7:8   1:2:3:4::8
    r'(?:' + IPV6SEG + r':){1,3}(?::' + IPV6SEG + r'){1,4}',  # 1::5:6:7:8         1:2:3::5:6:7:8   1:2:3::8
    r'(?:' + IPV6SEG + r':){1,2}(?::' + IPV6SEG + r'){1,5}',  # 1::4:5:6:7:8       1:2::4:5:6:7:8   1:2::8
    IPV6SEG + r':(?:(?::' + IPV6SEG + r'){1,6})',  # 1::3:4:5:6:7:8     1::3:4:5:6:7:8   1::8
    r':(?:(?::' + IPV6SEG + r'){1,7}|:)',  # ::2:3:4:5:6:7:8    ::2:3:4:5:6:7:8  ::8       ::
)
ipv6_re = re.compile('|'.join(['(?:{})'.format(g) for g in IPV6GROUPS[::-1]]))  # Reverse rows for greedy match


def source(family):
    if family == 4:
        def fetch(timeout):
            response = requests.get('https://myip4.ipip.net', timeout=timeout).text
            return ipv4_re.search(response).group()
    elif family == 6:
        def fetch(timeout):
            response = requests.get('https://myip6.ipip.net', timeout=timeout).text
            return ipv6_re.search(response).group()
    else:
        raise ValueError(f'Invalid family: {family}, should be 4 or 6')

    return _WithStr(fetch, f"<IPIP source; family={family}>")
