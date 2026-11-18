FROM python:3.11-alpine AS app

WORKDIR /src

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# `docker build --target cloudflared`: same app + Cloudflare Tunnel client
FROM app AS cloudflared
COPY --from=cloudflare/cloudflared:2026.11.1 /usr/local/bin/cloudflared /usr/local/bin/cloudflared
RUN chmod +x /src/docker-entrypoint.sh
ENTRYPOINT ["/src/docker-entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# default target: plain app, no cloudflared
FROM app
