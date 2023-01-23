from tkinter import Wm, Misc

from common.DbcCheckConfig import *

logging.basicConfig( level=logging.INFO, filename=CONF_LOG_FILE_NAME, filemode="w", format="%(asctime)s %(levelname)s: %(message)s" )
LOGGER = logging.getLogger( __name__ )

def centerWindow( aRoot: (Misc, Wm), width=300, height=200 ):
    # get screen width and height
    screen_width = aRoot.winfo_screenwidth()
    screen_height = aRoot.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    aRoot.geometry( '%dx%d+%d+%d' % (width, height, x, y) )
