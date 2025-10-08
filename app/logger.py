import logging
import sys
import os
from datetime import datetime


class BackupLogger:
    """Centralized logging configuration for backup operations."""

    def __init__(self, name='backup'):
        self.name = name
        self._loggers = {}

    def get_logger(self, module_name=None, log_to_file=False, log_file_path=None):
        """
        Get a configured logger instance.

        Args:
            module_name (str): Name for the logger (defaults to class name)
            log_to_file (bool): Whether to also log to a file
            log_file_path (str): Path to log file (if log_to_file is True)

        Returns:
            logging.Logger: Configured logger instance
        """
        if module_name is None:
            module_name = self.name

        # Return existing logger if already configured
        if module_name in self._loggers:
            return self._loggers[module_name]

        logger = logging.getLogger(module_name)
        logger.setLevel(logging.INFO)

        # Avoid adding handlers multiple times
        if not logger.handlers:
            formatter = self._get_formatter()

            # Console handler (stdout)
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            # File handler (optional)
            if log_to_file and log_file_path:
                # Ensure directory exists
                os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
                file_handler = logging.FileHandler(log_file_path)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)

        # Prevent propagation to root logger
        logger.propagate = False

        self._loggers[module_name] = logger
        return logger

    def _get_formatter(self):
        """Get the standard log formatter."""
        return logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    @staticmethod
    def get_backup_logger(path=None):
        """
        Convenience method to get a logger for backup operations.

        Args:
            path (str): Optional path being backed up (for context)

        Returns:
            logging.Logger: Configured backup logger
        """
        backup_logger = BackupLogger()

        if path:
            # Create a sanitized logger name from the path
            safe_path = path.replace('/', '_').replace('\\', '_').strip('_')
            logger_name = f'backup_{safe_path}'
        else:
            logger_name = 'backup'

        return backup_logger.get_logger(logger_name)


# Global instance for easy access
_backup_logger_instance = BackupLogger()


def get_logger(module_name=None, log_to_file=False, log_file_path=None):
    """
    Global function to get a configured logger.

    Args:
        module_name (str): Name for the logger
        log_to_file (bool): Whether to also log to a file
        log_file_path (str): Path to log file (if log_to_file is True)

    Returns:
        logging.Logger: Configured logger instance
    """
    return _backup_logger_instance.get_logger(module_name, log_to_file, log_file_path)