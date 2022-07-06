import contextlib
import socket
import requests
import requests.packages.urllib3.util.connection as urllib3_conn

from ._with_str import _WithStr


@contextlib.contextmanager
def force_family(family):
    if family == 4:
        orig = urllib3_conn.HAS_IPV6
        try:
            urllib3_conn.HAS_IPV6 = False
            yield
        finally:
            urllib3_conn.HAS_IPV6 = orig
    elif family == 6:
        orig = urllib3_conn.allowed_gai_family

        def allowed_gai_family():
            return socket.AF_INET6

        try:
            urllib3_conn.allowed_gai_family = allowed_gai_family
            yield
        finally:
            urllib3_conn.allowed_gai_family = orig
    else:
        yield


def source(endpoint, family=0):
    if endpoint.count(':') > 1 and endpoint[0] != '[':
        # IPv6 address
        endpoint = f'[{endpoint}]'

    def fetch(timeout):
        with force_family(family):
            response = requests.get(f"https://{endpoint}/cdn-cgi/trace", timeout=timeout).text
        for line in response.splitlines():
            if line.startswith('ip='):
                return line[3:].strip()
        raise RuntimeError('no ip provided in cloudflare trace info')

    return _WithStr(fetch, f"<CF-Trace source; endpoint='{endpoint}', family={family}>")
