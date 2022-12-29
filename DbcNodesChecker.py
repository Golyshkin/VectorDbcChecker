import DbcCheckConfig

from DbcCheckerInterface import *

class DbcNodesChecker( DbcCheckerInterface ):
    def processDbcFile( self, aDataBase: candb.Database, aDbcPath: str ):
        if len( aDataBase.nodes ) == 0:
            DbcCheckConfig.LOGGER.error( "Missed network nodes detected." )

    def onFinish( self ):
        pass
