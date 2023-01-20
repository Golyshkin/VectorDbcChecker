import threading

from ui.DbcCheckUiApplication import *
from checkers.DbcMsgDuplicatesChecker import *
from checkers.DbcNodesChecker import *
from checkers.DbcSigDuplicatesChecker import DbcSigDuplicatesChecker

def onStartCheckCallback( aSelectedPath: str ):
    thread = threading.Thread( target=startDBCCheckThread, args=[ aSelectedPath ] )
    thread.start()

def startDBCCheckThread( aSelectedPath: str ):
    DbcCheckConfig.LOGGER.info( str.format( "START DBCs CHECK v.{} FOR [{}].", DbcCheckConfig.APP_VER, aSelectedPath ) )

    DbcCheckEngine.initCheckers()
    dbcCheckEngine: DbcCheckEngine = DbcCheckEngine( aSelectedPath, outputCallback, finishCallback )

    if DbcCheckConfig.CONF_CHECK_MISSED_NETWORK_NODES:
        dbcCheckEngine.addChecker( DbcNodesChecker() )

    if DbcCheckConfig.CONF_CHECK_MSG_DUPLICATION:
        dbcCheckEngine.addChecker( DbcMsgDuplicatesChecker() )

    if DbcCheckConfig.CONF_CHECK_SIG_SPN_DUPLICATION:
        dbcCheckEngine.addChecker( DbcSigDuplicatesChecker() )

    dbcCheckEngine.startCheck()

def outputCallback( textOutput ):
    ui.insertOutput( textOutput )

def finishCallback():
    DbcCheckConfig.LOGGER.info( "END DBCs CHECK." )
    DbcCheckConfig.LOGGER.info( "--" )

    ui.onFinish()

if __name__ == '__main__':
    ui = DbcCheckUiApplication( onStartCheckCallback )
    ui.showUI()
