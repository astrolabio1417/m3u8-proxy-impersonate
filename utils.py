import json
from urllib.parse import quote, urlparse, parse_qs, urlencode
from .configs import ALLOWED_ORIGINS


def get_proxied_url(url: str, proxy_url: str, headers: dict):
    proxy_url = urlparse(proxy_url)
    proxy_params = parse_qs({})
    proxy_params["url"] = url
    proxy_params["headers"] = quote(json.dumps(headers))
    proxy_url = proxy_url._replace(query=urlencode(proxy_params, doseq=True))
    return proxy_url.geturl()


def get_filename_from_url(url: str):
    return url.split("/")[-1]


def replace_last_segment(url: str, new_value: str):
    s = url.rstrip("/").split("/")
    s[-1] = new_value
    return "/".join(s)


if __name__ == "__main__":
    a = get_proxied_url(
        "https://google.com", "https://proxy.com", {"referer": "https://referer.com"}
    )
    print(a)
