FROM python:3.11-alpine

WORKDIR /src

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD [ "fastapi", "run", "main.py" ]
