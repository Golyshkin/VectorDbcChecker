from common import DbcCheckConfig
from common.DbcCheckUtils import LOGGER
from interfaces.DbcCheckerInterface import *

class DbcBaseChecker( DbcCheckerInterface ):
    def processDbcFile( self, aDataBase: candb.Database, aDbcPath: str ):
        if DbcCheckConfig.CONF_CHECK_DB_VERSION and (aDataBase.version is None or len( aDataBase.version )) == 0:
            LOGGER.error( "DBC version is not defined." )

    def onStart( self ):
        LOGGER.info( f"{self.getName()} Registered." )

    def onFinish( self ):
        pass

    def processMessage( self, aMessage: Message ) -> None:
        pass

    def processSignal( self, aSignal: Signal ) -> None:
        pass

    def printReport( self ) -> None:
        pass

    def getName( self ) -> str:
        return "DBC Base Checker"
