from common import DbcCheckConfig
from common.DbcCheckUtils import LOGGER
from interfaces.DbcCheckerInterface import *

class DbcSigByteOrderChecker( DbcCheckerInterface ):

    def __init__( self ):
        self.messageName: str = "None"

    def processDbcFile( self, aDataBase: candb.Database, aDbcPath: str ) -> None:
        pass

    def processMessage( self, aMessage: Message ) -> None:
        self.messageName = aMessage.name

    def processSignal( self, aSignal: Signal ) -> None:
        if aSignal.byte_order != DbcCheckConfig.SIGNAL_BYTE_ORDER:
            LOGGER.error( "Signal '{0}->{1}' has '{2}' byte order, but should be '{3}'".format( aSignal.name, self.messageName, aSignal.byte_order, DbcCheckConfig.SIGNAL_BYTE_ORDER ) )

    def printReport( self ) -> None:
        pass

    def onFinish( self ) -> None:
        pass

    def onStart( self ) -> None:
        LOGGER.info( "DBC Signals Byte Order Checker Registered." )

    def getName( self ) -> str:
        return "DbcSigByteOrderChecker"
