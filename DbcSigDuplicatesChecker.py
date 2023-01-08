from pathlib import Path

from DbcCheckerInterface import *
from VectorDbcChecker import DbcCheckConfig

class DbcSigDuplicatesChecker( DbcCheckerInterface ):

    def __init__( self ):
        self._signalsDict = dict()
        self._duplicatesInfoDict = dict()
        self._dbcPath: str = "N/A"
        self._currentMsg: Message = "N/A"

    def processDbcFile( self, aDataBase: candb.Database, aDbcPath: str ) -> None:
        self._dbcPath = Path( aDbcPath ).absolute()

    def printReport( self ) -> None:
        DbcCheckConfig.LOGGER.info( "" )
        DbcCheckConfig.LOGGER.info( "START SIGNALS DUPLICATE REPORT" )
        isSpnDuplicationFound: bool = False

        for spn, infoDict in self._signalsDict.items():
            if len( infoDict ) > 1:
                isSpnDuplicationFound = True
                DbcCheckConfig.LOGGER.info( "" )
                DbcCheckConfig.LOGGER.info( str.format( "SPN {} duplication for:", spn ) )

                for path, infoList in infoDict.items():
                    for signalName in infoList:
                        DbcCheckConfig.LOGGER.info( str.format( "{} in {}", signalName, path ) )

        if not isSpnDuplicationFound:
            DbcCheckConfig.LOGGER.info( "No duplicates found." )

        DbcCheckConfig.LOGGER.info( "START SIGNALS DUPLICATE REPORT" )

    def onFinish( self ) -> None:
        self.printReport()

    def onStart( self ) -> None:
        DbcCheckConfig.LOGGER.info( "DBC Signals Duplicate Checker Registered." )

    def processMessage( self, aMessage: Message ) -> None:
        self._currentMsg = aMessage.name

    def processSignal( self, aSignal: Signal ) -> None:
        if aSignal.spn is not None:
            try:
                self._signalsDict[ aSignal.spn ]
            except KeyError:
                self._signalsDict[ aSignal.spn ] = dict()

            if self._dbcPath not in self._signalsDict[ aSignal.spn ].keys():
                self._signalsDict[ aSignal.spn ][ self._dbcPath ] = list()

            self._signalsDict[ aSignal.spn ][ self._dbcPath ].append( str.format( "{}->{}", self._currentMsg, aSignal.name ) )
