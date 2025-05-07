import logging
import logging.config
from pathlib import Path
from datetime import datetime
import json

def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"error_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "simple": {
                "format": "%(levelname)s %(message)s"
            }
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "filename": log_file,
                "level": "ERROR",
                "formatter": "detailed"
            },
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple"
            }
        },
        "loggers": {
            "": {
                "handlers": ["file", "console"],
                "level": "DEBUG"
            }
        }
    })
    
    # Логирование конфигурации
    logger = logging.getLogger(__name__)
    logger.info("Logging setup complete")