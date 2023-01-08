# Configuration file for Vector DBCChecker
import logging

APP_TITLE: str = "Vector DBCChecker Application"
APP_ABOUT_INFO: str = "This is application checks a vector based DBC files on consistency and messages duplicates.\n\n(c) Alexander.Golyshkin 2022"
APP_WIN_SIZE_APP: str = "800x600"
APP_WIN_SIZE_SETTINGS: str = "400x240"

CONF_CHECK_MSG_DUPLICATION: bool = True
CONF_CHECK_SIG_SPN_DUPLICATION: bool = True
CONF_IGNORE_MSG_DUP_WITH_SAME_SIGNALS: bool = False
CONF_CHECK_OVERLAP_SIGNALS: bool = True
CONF_CHECK_MISSED_NETWORK_NODES: bool = True
CONF_CHECK_DB_VERSION: bool = True
CONF_LOG_FILE_NAME: str = "dbc-check.log"
CONF_PAD_DX: int = 5
CONF_PAD_DY: int = 5
# By default, is expected an Intel byte order in signals
SIGNAL_BYTE_ORDER: str = "little_endian"

logging.basicConfig( level=logging.INFO, filename=CONF_LOG_FILE_NAME, filemode="w", format="%(asctime)s %(levelname)s: %(message)s" )
LOGGER = logging.getLogger( __name__ )
