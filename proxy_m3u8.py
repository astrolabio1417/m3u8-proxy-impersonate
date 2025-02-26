import re

from fastapi import HTTPException
from .configs import M3U8_PROXY_PATH, TS_PROXY_PATH
from curl_cffi import requests
from .utils import get_proxied_url, replace_last_segment


SUBTITLES_TEXT = "#EXT-X-MEDIA:TYPE=SUBTITLES"
KEY_TEXT = "#EXT-X-KEY"
URL_REGEX = re.compile(r"URI=\"(.*)\"")


def proxy_m3u8_text(text: str, url: str, custom_headers: dict = {}):
    lines = filter(
        lambda x: x != "" and not x.startswith("EXT-X-MEDIA:TYPE=AUDIO"),
        text.split("\n"),
    )
    new_lines = []
    has_res = "RESOLUTION=" in text
    url_path = M3U8_PROXY_PATH if has_res else TS_PROXY_PATH

    for line in lines:
        if line.startswith(SUBTITLES_TEXT) or line.startswith(KEY_TEXT):
            match = re.search(URL_REGEX, line)
            uri = match.group(1) if match else ""
            full_url = uri if uri.startswith("http") else replace_last_segment(url, uri)
            _proxy_url = (
                M3U8_PROXY_PATH if line.startswith(SUBTITLES_TEXT) else TS_PROXY_PATH
            )
            proxied_url = get_proxied_url(full_url, _proxy_url, custom_headers)
            new_lines.append(line.replace(uri, proxied_url))
            continue

        if line.startswith("#"):
            new_lines.append(line)
            continue

        full_url = line if line.startswith("http") else replace_last_segment(url, line)
        proxied_url = get_proxied_url(full_url, url_path, custom_headers)
        new_lines.append(proxied_url)

    return "\n".join(new_lines)


def proxy_m3u8(url: str, custom_headers: dict = {}):
    res = requests.get(url, impersonate="chrome", headers=custom_headers)

    if not res.ok:
        raise HTTPException(
            status_code=500, detail=f"Fetch failed with status {res.status_code}"
        )

    return proxy_m3u8_text(res.text, url, custom_headers)
