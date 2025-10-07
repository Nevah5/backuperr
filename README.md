# Backuperr

A simple backup script that backs up folders to a specified backup location and sends email notifications on errors.

## Setup

The project is fully run on Docker. You can deploy it with the following `docker-compose.yaml` file.

```yaml
version: '3.8'

services:
  backuperr:
    image: ghcr.io/nevah5/backuperr:latest
    container_name: backuperr
    env_file:
      - .env
    volumes:
      - ./config.yaml:/app/config.yaml:ro
      - /example:/backup/example
      - /mnt/example:/backups
    environment:
      - TZ=Europe/Zurich
    restart: unless-stopped
```

### Config File

The `config.yaml` file should be structured as follows:

```yaml
folders:
  - path: immich/
    files:
      - .env
      - postgres/
      - model-cache/
    location: /mnt/example/immich/
    schedule: "0 2 * * *"
    retention: 7d
    compress: false
  - path: jellyfin/
    files:
      - .env
      - media/
    location: /mnt/example/jellyfin/
    schedule: "0 2 * * *"
    retention: '3'
    compress: true
```
