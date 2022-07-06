import requests

from ._with_str import _WithStr


def source(endpoint):
    def fetch(timeout):
        return requests.get(endpoint, timeout=timeout).text.strip()

    return _WithStr(fetch, f"<Simple source; endpoint='{endpoint}'>")
