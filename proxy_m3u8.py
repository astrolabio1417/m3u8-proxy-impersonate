import re
from fastapi import HTTPException
from configs import M3U8_PROXY_PATH, TS_PROXY_PATH, PROXY
from urllib.parse import urljoin
from curl_cffi import requests
from utils import get_proxied_url

MEDIA_TEXT = "#EXT-X-MEDIA:"
KEY_TEXT = "#EXT-X-KEY"
URL_REGEX = re.compile(r"URI=\"([^\"]*)\"")


def proxy_m3u8_text(text: str, url: str, custom_headers: dict = {}, cookies: dict = {}):
    lines = filter(None, text.splitlines())
    new_lines = []
    has_res = "RESOLUTION=" in text
    url_path = M3U8_PROXY_PATH if has_res else TS_PROXY_PATH

    for line in lines:
        if line.startswith(MEDIA_TEXT) or line.startswith(KEY_TEXT):
            match = re.search(URL_REGEX, line)
            if not match:
                new_lines.append(line)
                continue

            uri = match.group(1)
            full_url = urljoin(url, uri)
            # EXT-X-MEDIA URIs are playlists (subtitles/audio); EXT-X-KEY is a raw file
            _proxy_url = (
                M3U8_PROXY_PATH if line.startswith(MEDIA_TEXT) else TS_PROXY_PATH
            )
            proxied_url = get_proxied_url(full_url, _proxy_url, custom_headers, cookies)
            new_lines.append(line.replace(uri, proxied_url))
            continue

        if line.startswith("#"):
            new_lines.append(line)
            continue

        full_url = urljoin(url, line)
        proxied_url = get_proxied_url(full_url, url_path, custom_headers, cookies)
        new_lines.append(proxied_url)

    return "\n".join(new_lines)


def proxy_m3u8(url: str, custom_headers: dict = {}, cookies={}):
    res = requests.get(
        url,
        impersonate="chrome",
        headers=custom_headers,
        cookies=cookies,
        proxy=PROXY,
    )

    if not res.ok:
        raise HTTPException(
            status_code=500, detail=f"Fetch failed with status {res.status_code}"
        )

    return proxy_m3u8_text(res.text, url, custom_headers, cookies)
