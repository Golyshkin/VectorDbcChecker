import DbcCheckConfig

from DbcCheckerInterface import *

class DbcBaseChecker( DbcCheckerInterface ):
    def processDbcFile( self, aDataBase: candb.Database, aDbcPath: str ):
        if DbcCheckConfig.CONF_CHECK_DB_VERSION and (aDataBase.version is None or len( aDataBase.version )) == 0:
            DbcCheckConfig.LOGGER.error( "DBC version is not defined." )

    def onStart( self ):
        DbcCheckConfig.LOGGER.info( "DBC Base Checker Registered." )

    def onFinish( self ):
        pass
