"""Logging configuration."""

import logging.config
import re
from collections import OrderedDict

from pythonjsonlogger.jsonlogger import JsonFormatter
from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(JsonFormatter):
    """CustomJsonFormatter."""

    def __init__(self, *args, **kwargs):
        reserved_attrs = ["color_message"] + jsonlogger.RESERVED_ATTRS
        super().__init__(*args, reserved_attrs=reserved_attrs, **kwargs)

    def process_log_record(self, log_record):
        """Process_log_record."""
        record = OrderedDict(((v, None) for v in self.rename_fields.values()))
        record.update(log_record)
        return super().process_log_record(record)


class SensitiveDataFilter(logging.Filter):
    """SensitiveDataFilter."""

    pattern = re.compile(r"\d{4}-\d{4}-\d{4}-\d{4}")

    def filter(self, record):
        """Filter."""
        if isinstance(record.msg, str):
            record.msg = self.mask_sensitive_data(record.msg)
        return True

    def mask_sensitive_data(self, message):
        """Mask_sensitive_data."""
        message = self.pattern.sub("[REDACTED]", message)
        return message


class StdoutFormatter(logging.Formatter):
    """Цветной вывод логов в зависимости от типа события."""

    grey = "\x1b[38;20m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "[%(levelname).3s][%(asctime)s] [%(name)s:%(lineno)d]: %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: blue + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        """Format."""
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
