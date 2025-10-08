FROM python:3.9-slim

WORKDIR /app

COPY ./app /app
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./app/backup.py /app/backup.py

ENTRYPOINT ["/entrypoint.sh"]

CMD ["cron", "-f"]