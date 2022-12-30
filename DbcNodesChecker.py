import DbcCheckConfig

from DbcCheckerInterface import *

class DbcNodesChecker( DbcCheckerInterface ):
    def processDbcFile( self, aDataBase: candb.Database, aDbcPath: str ):
        if len( aDataBase.nodes ) == 0:
            DbcCheckConfig.LOGGER.error( "Missed network nodes detected." )

    def onStart( self ):
        DbcCheckConfig.LOGGER.info( "DBC Nodes Checker Registered." )

    def onFinish( self ):
        pass
