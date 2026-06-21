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

### Cloudflare Tunnel

The Docker image includes `cloudflared` so it can start a Cloudflare Tunnel alongside the app.

```bash
docker run \
  -e CLOUDFLARE_TUNNEL=true \
  -e CLOUDFLARE_TOKEN="<your-cloudflare-token>" \
  video-proxy-impersonate
```

You can also override the target URL exposed by the tunnel:

```bash
docker run \
  -e CLOUDFLARE_TUNNEL=true \
  -e CLOUDFLARE_TOKEN="<your-cloudflare-token>" \
  -e CLOUDFLARE_TUNNEL_URL="http://127.0.0.1:8000" \
  video-proxy-impersonate
```

## Environment Variables

-   `ALLOWED_ORIGINS`: Comma-separated list of allowed origins.
