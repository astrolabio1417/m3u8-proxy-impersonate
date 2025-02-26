import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse, Response, JSONResponse
from .utils import get_filename_from_url, get_origin_from_allowed_origins
from .proxy_m3u8 import proxy_m3u8
from .configs import (
    M3U8_PROXY_PATH,
    TS_PROXY_PATH,
)
from urllib.parse import unquote
from curl_cffi import requests
from starlette.background import BackgroundTask


app = FastAPI()
client = requests.AsyncSession()


@app.middleware("http")
async def cors_handler(request: Request, call_next):
    origin = (
        request.headers.get("origin")
        or request.headers.get("referer")
        or get_origin_from_allowed_origins(request.headers.get("Host"))
    )

    if not origin:
        return JSONResponse(
            {"error": "Forbidden"},
            status_code=403,
        )

    response: Response = await call_next(request)
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Origin"] = origin or "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"

    return response


@app.get("/")
def read_root():
    return FileResponse("static/sample.html")


@app.get(M3U8_PROXY_PATH)
async def serve_proxy_m3u8(request: Request):
    query = request.query_params
    url = unquote(query.get("url"))
    headers = json.loads(unquote(query.get("headers", "{}")))
    cookies = json.loads(unquote(query.get("cookies", "{}")))

    return Response(
        proxy_m3u8(url, headers, cookies),
        headers={
            "Content-Type": "application/vnd.apple.mpegurl",
            "Content-Disposition": f'attachment; filename="{get_filename_from_url(url)}"',
        },
    )


@app.get(TS_PROXY_PATH)
async def serve_proxy_ts(request: Request):
    query = request.query_params
    url = unquote(query.get("url"))
    headers = json.loads(unquote(query.get("headers", "{}")))
    cookies = json.loads(unquote(query.get("cookies", "{}")))

    # https://www.python-httpx.org/async/
    res = await client.get(
        url, headers=headers, impersonate="chrome", stream=True, cookies=cookies
    )

    if not res.ok:
        res.aclose()
        raise HTTPException(
            status_code=500, detail=f"Fetch failed with status {res.status_code}"
        )

    return StreamingResponse(
        res.aiter_content(),
        headers={
            **res.headers,
        },
        background=BackgroundTask(res.aclose),
    )
