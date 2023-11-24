import os
from os import sep
from os.path import expanduser

ACCESS_KEY = "M3SDK_ACCESS_KEY"
SECRET_KEY = "M3SDK_SECRET_KEY"
ADDRESS = "M3SDK_ADDRESS"
SDK_VERSION = 'M3SDK_VERSION'
CONFIGURATION_FOLDER_PATH = 'M3CLI_CONFIGURATION_FOLDER_PATH'
DEBUG_MODE = "M3CLI_DEBUG"
CUSTOM_LOG_PATH = 'LOG_PATH'

CREDENTIALS_FILE = 'default.cr'
M3_PROPERTIES_FILE = 'm3.properties'
FOLDERS_SEPARATOR = sep
POSITIVE_ANSWERS = ['y', 'yes']

HOME_DIRECTORY = expanduser("~")
M3_CLI_RESOURCES_DIR = '.m3cli'
M3_CLI_RESOURCES_PATH = os.path.join(HOME_DIRECTORY, M3_CLI_RESOURCES_DIR)
CREDENTIALS_FILE_PATH = os.path.join(M3_CLI_RESOURCES_PATH, CREDENTIALS_FILE)

SUPPORTED_OS = ['nt', 'posix']

RESERVED_KEYWORDS = [ACCESS_KEY, SECRET_KEY, ADDRESS]

HEALTH_CHECK_CMD_NAME = 'health-check'