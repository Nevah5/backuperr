from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import os
import argparse
import sys
from datetime import datetime
from config import load_config
from backup_utils import create_backup, clean_old_backups
from email_utils import send_error_email
from logger import BackupLogger

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True, help='Path to backup')
    args = parser.parse_args()

    # Setup logging using the new logger module
    logger = BackupLogger.get_backup_logger(args.path)

    logger.info(f"Starting backup process for path: {args.path}")

    try:
        config = load_config('/app/config.yaml')
        logger.info("Configuration loaded successfully")

        folder_config = next((f for f in config['folders'] if f['path'] == args.path), None)
        if not folder_config:
            raise ValueError(f"No configuration found for path: {args.path}")

        source_path = os.path.join('/backup', folder_config['path'])
        destination_path = folder_config['location']
        compress = folder_config.get('compress', False)
        retention = folder_config['retention']

        logger.info(f"Source: {source_path}")
        logger.info(f"Destination: {destination_path}")
        logger.info(f"Compression: {'enabled' if compress else 'disabled'}")
        logger.info(f"Retention: {retention} days")

        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
            logger.info(f"Created destination directory: {destination_path}")

        logger.info("Starting backup creation...")
        create_backup(source_path, destination_path, compress)
        logger.info("Backup creation completed successfully")

        logger.info("Starting cleanup of old backups...")
        clean_old_backups(destination_path, retention)
        logger.info("Cleanup completed successfully")

        logger.info(f"Backup process for {args.path} completed successfully")

    except Exception as e:
        error_message = f"An error occurred during backup of {args.path}: {e}"
        logger.error(error_message)
        logger.exception("Full traceback:")
        send_error_email(f"Backup Error - {args.path}", error_message)
        sys.exit(1)

if __name__ == "__main__":
    main()