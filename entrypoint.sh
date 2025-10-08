#!/bin/bash

CONFIG_PATH="/app/config.yaml"
CRON_FILE="/etc/cron.d/backup_jobs"
ENV_FILE="/app/.env"

# Load environment variables
if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

> $CRON_FILE

python3 -c "
import yaml
import os

CONFIG_PATH = os.getenv('CONFIG_PATH', '/app/config.yaml')

with open(CONFIG_PATH, 'r') as file:
    config = yaml.safe_load(file)

for folder in config['folders']:
    schedule = folder['schedule']
    path = folder['path']

    command = f'python3 /app/backup.py --path {path}'
    cron_line = f'{schedule} {command}'
    print(f'Adding backup job of {path} with schedule {schedule}')

    # Write to cron file
    with open('$CRON_FILE', 'a') as cron:
        cron.write(cron_line + '\\n')
"

chmod 0644 $CRON_FILE

echo "Starting cron..."
cron -f
