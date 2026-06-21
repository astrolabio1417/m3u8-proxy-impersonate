FROM python:3.11-alpine

WORKDIR /src

COPY requirements.txt .

RUN apk add --no-cache curl ca-certificates \
    && pip install --no-cache-dir --upgrade -r requirements.txt \
    && curl -fL -o /usr/local/bin/cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
    && chmod +x /usr/local/bin/cloudflared

COPY . .
RUN chmod +x /src/docker-entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/src/docker-entrypoint.sh"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
