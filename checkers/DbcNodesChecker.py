from common.DbcCheckUtils import LOGGER
from interfaces.DbcCheckerInterface import *

class DbcNodesChecker( DbcCheckerInterface ):
    def processDbcFile( self, aDataBase: candb.Database, aDbcPath: str ):
        if len( aDataBase.nodes ) == 0:
            LOGGER.error( "Missed network nodes detected." )

    def onStart( self ):
        LOGGER.info( "DBC Nodes Checker Registered." )

    def onFinish( self ):
        pass

    def processMessage( self, aMessage: Message ) -> None:
        pass

    def processSignal( self, aSignal: Signal ) -> None:
        pass

    def printReport( self ) -> None:
        pass

    def getName( self ) -> str:
        return "DbcNodesChecker"
