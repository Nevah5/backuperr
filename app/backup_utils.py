import os
import tarfile
from datetime import datetime, timedelta
from logger import get_logger

# Get logger for this module
logger = get_logger('backup_utils')

def create_backup(source_path, destination_path, compress):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    backup_name = f"backup_{timestamp}.tar"
    if compress:
        backup_name += ".gz"

    backup_path = os.path.join(destination_path, backup_name)

    with tarfile.open(backup_path, 'w:gz' if compress else 'w') as tar:
        tar.add(source_path, arcname=os.path.basename(source_path))

    logger.info(f"Backup created: {backup_path}")
    return backup_path

def clean_old_backups(destination_path, retention):
    backups = sorted(
        [f for f in os.listdir(destination_path) if f.startswith('backup_')],
        key=lambda x: os.path.getmtime(os.path.join(destination_path, x))
    )

    if retention.isdigit():
        # Keep the last 'n' backups
        to_delete = backups[:-int(retention)]
    else:
        # Retention based on time (e.g., '7d', '3w')
        unit = retention[-1]
        value = int(retention[:-1])
        if unit == 'd':
            cutoff = datetime.now() - timedelta(days=value)
        elif unit == 'w':
            cutoff = datetime.now() - timedelta(weeks=value)
        else:
            raise ValueError("Unsupported retention unit. Use 'd' for days or 'w' for weeks.")

        to_delete = [
            f for f in backups
            if datetime.fromtimestamp(os.path.getmtime(os.path.join(destination_path, f))) < cutoff
        ]

    for backup in to_delete:
        os.remove(os.path.join(destination_path, backup))
        logger.info(f"Deleted old backup: {backup}")
    
    if to_delete:
        logger.info(f"Cleaned up {len(to_delete)} old backup(s)")
    else:
        logger.info("No old backups to clean up")