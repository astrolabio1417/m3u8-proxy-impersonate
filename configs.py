import os
from urllib.parse import urlparse


M3U8_PROXY_PATH = "/m3u8-proxy"
TS_PROXY_PATH = "/ts-proxy"
ALLOWED_ORIGINS = os.environ.get(
    "ALLOWED_ORIGINS", "http://localhost:8989,https://google.com"
).split(",")
ALLOWED_ORIGINS_WO_SCHEME = [urlparse(origin).netloc for origin in ALLOWED_ORIGINS]

# any curl proxy URL, e.g. http://host:8080 or socks5://warp.web:1080
PROXY = os.environ.get("PROXY") or None
# socks5h resolves DNS at the proxy; plain socks5 resolves locally and leaks/fails in containers
PROXY = PROXY.replace("socks5://", "socks5h://", 1) if PROXY else None
