import os
# Get the desired log level from an environment variable.
# Default to "INFO" for production, but you can set it to "DEBUG" for development.
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# This is a standard Python logging configuration dictionary.
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
        "": { # Root logger
            "handlers": ["default"],
            "level": LOG_LEVEL,
        },
        "backend": { # Our application's logger
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