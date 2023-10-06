import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    APP_NAME = "AsiaYo-api"
    ENV_SET = "Local"
    DEBUG = True

    JSON_AS_ASCII = False
    SECRET_KEY = "Secret"


    # log setting
    LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
    LOG_PATH_ERROR = os.path.join(LOG_PATH, 'AsiaYo_error.log')
    LOG_PATH_INFO = os.path.join(LOG_PATH, 'AsiaYo_info.log')
    LOG_PATH_DEBUG = os.path.join(LOG_PATH, 'AsiaYo_debug.log')
    LOG_FILE_MAX_BYTES = 100 * 1024 * 1024
    LOG_FILE_BACKUP_COUNT = 10