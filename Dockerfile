FROM python:3.9-slim

WORKDIR /app

COPY ./app /app
COPY requirements.txt /app/
COPY setup.sh /app/

RUN chmod +x /app/setup.sh
RUN /app/setup.sh

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./app/backup.py /app/backup.py

ENTRYPOINT ["/entrypoint.sh"]

CMD ["cron", "-f"]