import json
import logging
import sys
import os


class LogLevel:
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line_no": record.lineno,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


default_formatter = JsonFormatter()
stout_handler = logging.StreamHandler(sys.stdout)
stderr_handler = logging.StreamHandler(sys.stderr)

stout_handler.setFormatter(default_formatter)
stderr_handler.setFormatter(default_formatter)

stout_handler.setLevel(LogLevel.INFO)
stderr_handler.setLevel(LogLevel.ERROR)

logger = logging.getLogger("application")
logger.setLevel(LogLevel.INFO)

logger.addHandler(stout_handler)
logger.addHandler(stderr_handler)
