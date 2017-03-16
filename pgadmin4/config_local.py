from config import *

# Debug mode
DEBUG = True

# App mode
SERVER_MODE = False

# Enable the test module
MODULE_BLACKLIST.remove('test')

# Log
CONSOLE_LOG_LEVEL = DEBUG
FILE_LOG_LEVEL = DEBUG

DEFAULT_SERVER = '0.0.0.0'

UPGRADE_CHECK_ENABLED = True

# Use a different config DB for each server mode.
if SERVER_MODE == False:
    SQLITE_PATH = os.path.join(
        DATA_DIR,
        'pgadmin4-desktop.db'
    )
else:
    SQLITE_PATH = os.path.join(
        DATA_DIR,
        'pgadmin4-server.db'
    )