#!/bin/bash

CONFIG_PATH="/app/config.yaml"
CRON_FILE="/etc/cron.d/backup_jobs"

> $CRON_FILE

python3 -c "
import yaml
with open('$CONFIG_PATH', 'r') as file:
    config = yaml.safe_load(file)

for folder in config['folders']:
    schedule = folder['schedule']
    path = folder['path']
    print(f'{schedule} python3 /app/backup.py --path {path}')
" >> $CRON_FILE

chmod 0644 $CRON_FILE

cron -f