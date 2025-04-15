import os
from urllib.parse import urlparse


M3U8_PROXY_PATH = "/m3u8-proxy"
TS_PROXY_PATH = "/ts-proxy"
ALLOWED_ORIGINS = os.environ.get(
    "ALLOWED_ORIGINS", "http://localhost:8989,https://google.com"
).split(",")
ALLOWED_ORIGINS_WO_SCHEME = [urlparse(origin).netloc for origin in ALLOWED_ORIGINS]

# proxy
PROXY_LIST = os.environ.get("PROXY_LIST")

if PROXY_LIST:
    PROXY_LIST = PROXY_LIST.split(",")
else:
    try:
        with open("proxies.txt", "r") as f:
            PROXY_LIST = f.read().split("\n")
    except FileNotFoundError:
        print("proxies.txt is empty")
