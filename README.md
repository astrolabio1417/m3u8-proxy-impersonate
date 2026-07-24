# M3U8 Proxy Server using curl impersonate

To install dependencies:

```bash
pip install -r requirements.txt
```

To run:

```bash
fastapi dev run
```

## Docker

### Build

To build the Docker image:

```bash
docker build -t video-proxy-impersonate .
```

### Run

To run the Docker container:

```bash
docker run -p 8000:8000 -e ALLOWED_ORIGINS="http://localhost:8000,http://localhost" video-proxy-impersonate
```

## Environment Variables

-   `ALLOWED_ORIGINS`: Comma-separated list of allowed origins.
-   `HTTP_PROXY`: (Optional) HTTP proxy URL to use for HTTP requests (e.g., `http://proxy.example.com:8080`)
-   `HTTPS_PROXY`: (Optional) HTTPS proxy URL to use for HTTPS requests (e.g., `http://proxy.example.com:8080`)

### Example with Proxy

```bash
docker run -p 8000:8000 \
  -e ALLOWED_ORIGINS="http://localhost:8000,http://localhost" \
  -e HTTP_PROXY="http://proxy.example.com:8080" \
  -e HTTPS_PROXY="http://proxy.example.com:8080" \
  video-proxy-impersonate
```
