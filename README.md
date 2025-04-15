# M3U8 Proxy Server using curl impersonate

To install dependencies:

```bash
pip install -r requirements.txt
```

To run:

```bash
fastapi run main.py
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
docker run -p 8989:8989 -e ALLOWED_ORIGINS="http://localhost:8989,http://localhost" video-proxy-impersonate
```

## Environment Variables

-   `ALLOWED_ORIGINS`: Comma-separated list of allowed origins.
-   `PROXY_LIST`: Comma-separated list of proxy.

## Proxy List alternative to environment vars

Filename: `proxies.txt`

-   The file should contain one proxy entry per line:

```plaintext
192.168.1.100:8080
192.168.1.101:3128
192.168.1.102:9090
```
