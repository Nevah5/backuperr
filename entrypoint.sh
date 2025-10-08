#!/bin/bash

CONFIG_PATH="/app/config.yaml"
CRON_FILE="/etc/cron.d/backup_jobs"
ENV_FILE="/app/.env"

if [ -f "$ENV_FILE" ]; then
    export $(grep -v '^#' "$ENV_FILE" | xargs)
fi

if [ -z "$EMAIL_HOST" ] || [ -z "$EMAIL_PORT" ] || [ -z "$EMAIL_USERNAME" ] || [ -z "$EMAIL_PASSWORD" ] || [ -z "$EMAIL_FROM" ] || [ -z "$ERROR_EMAIL_TO" ]; then
    echo "WARNING: Email configuration is incomplete. Email notifications will not be available."
    echo "Please refer to the documentation for required email environment variables:"
    echo "  EMAIL_HOST, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_FROM, ERROR_EMAIL_TO"
    echo "Email notifications are disabled for this session."
else
    echo "Email configuration found. Error notifications will be sent to: $ERROR_EMAIL_TO"
fi

> $CRON_FILE

mkdir -p /var/log/backuperr

python3 -c "
import yaml
import os

CONFIG_PATH = os.getenv('CONFIG_PATH', '/app/config.yaml')

with open(CONFIG_PATH, 'r') as file:
    config = yaml.safe_load(file)

for folder in config['folders']:
    schedule = folder['schedule']
    path = folder['path']

    command = f'cd /app && python3 /app/backup.py --path {path}'

    log_file = f'/var/log/backuperr/backup_{path.replace(\"/\", \"_\")}.log'
    cron_line = f'{schedule} {command} >> {log_file} 2>&1' # Log file to capture script errors that are not handled by the logger

    print(f'Adding backup job of {path} with schedule {schedule}')
    print(f'  Logs will be written to {log_file}')

    with open('$CRON_FILE', 'a') as cron:
        cron.write(cron_line + '\\n')
"

chmod 0644 $CRON_FILE

echo "Starting cron..."
cron -f
