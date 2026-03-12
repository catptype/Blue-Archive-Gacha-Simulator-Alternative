from .config import settings
LOG_LEVEL = settings.LOG_LEVEL.upper()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False, # This is crucial to not silence Uvicorn's logs
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s - %(name)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        # Root logger
        "": { 
            "handlers": ["default"],
            "level": LOG_LEVEL,
        },
        # Application logger
        "backend": { 
            "handlers": ["default"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "uvicorn.error": {
            "level": "INFO",
        },
        "uvicorn.access": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },
    },
}