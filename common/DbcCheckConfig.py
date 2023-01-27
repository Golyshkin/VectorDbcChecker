# Configuration file for Vector DBCChecker

APP_VER: float = 1.2
APP_TITLE: str = "Vector DBCChecker Application"
APP_ABOUT_INFO: str = "This is application checks a vector based DBC files on consistency and messages duplicates.\n\n(c) Alexander.Golyshkin 2023"
APP_CONFIG_XML_PATH: str = "configuration.xml"
APP_WIN_SIZE_APP_WIDTH: int = 800
APP_WIN_SIZE_APP_HEIGHT: int = 600
APP_WIN_SIZE_SETTINGS_WIDTH: int = 380
APP_WIN_SIZE_SETTINGS_HEIGHT: int = 250

CONF_CHECK_MSG_DUPLICATION: bool = True
CONF_CHECK_SIG_SPN_DUPLICATION: bool = True
CONF_IGNORE_MSG_DUP_WITH_SAME_SIGNALS: bool = False
CONF_CHECK_OVERLAP_SIGNALS: bool = True
CONF_CHECK_MISSED_NETWORK_NODES: bool = True
CONF_CHECK_DB_VERSION: bool = True
CONF_USE_POLARION_INTEGRATIONS_FOR_CHECK_SIGNALS: bool = False
CONF_LOG_FILE_NAME: str = "dbc-check.log"
CONF_PAD_DX: int = 5
CONF_PAD_DY: int = 5
# By default, is expected an Intel byte order in signals
SIGNAL_BYTE_ORDER: str = "little_endian"
