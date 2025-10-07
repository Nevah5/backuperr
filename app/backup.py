from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import os
import argparse
from config import load_config
from backup_utils import create_backup, clean_old_backups
from email_utils import send_error_email

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True, help='Path to backup')
    args = parser.parse_args()

    try:
        config = load_config('/app/config.yaml')

        folder_config = next((f for f in config['folders'] if f['path'] == args.path), None)
        if not folder_config:
            raise ValueError(f"No configuration found for path: {args.path}")

        source_path = os.path.join('/backup', folder_config['path'])
        destination_path = folder_config['location']
        compress = folder_config.get('compress', False)
        retention = folder_config['retention']

        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        create_backup(source_path, destination_path, compress)
        clean_old_backups(destination_path, retention)
    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        send_error_email(f"Backup Error - {args.path}", error_message)

if __name__ == "__main__":
    main()