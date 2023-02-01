from pathlib import Path

from common.DbcCheckUtils import LOGGER
from interfaces.DbcCheckerInterface import *

class DbcSigDuplicatesChecker( DbcCheckerInterface ):

    def __init__( self ):
        self.__signalsDict = dict()
        self.__dbcPath: str = "N/A"
        self.__currentMsg: str = "N/A"

    def processDbcFile( self, aDataBase: candb.Database, aDbcPath: str ) -> None:
        self.__dbcPath = Path( aDbcPath ).absolute()

    def printReport( self ) -> None:
        LOGGER.info( "" )
        LOGGER.info( f"START {self.getName()} REPORT" )
        isSpnDuplicationFound: bool = False

        for spn, infoDict in self.__signalsDict.items():
            if len( infoDict ) > 1:
                isSpnDuplicationFound = True
                LOGGER.info( "" )
                LOGGER.info( str.format( "SPN {} duplication for:", spn ) )

                for path, infoList in infoDict.items():
                    for signalName in infoList:
                        LOGGER.info( str.format( "{} in {}", signalName, path ) )

        if not isSpnDuplicationFound:
            LOGGER.info( "No duplicates found." )

        LOGGER.info( f"END {self.getName()} REPORT" )

    def onFinish( self ) -> None:
        self.printReport()

    def onStart( self ) -> None:
        LOGGER.info( f"{self.getName()} Registered." )

    def processMessage( self, aMessage: Message ) -> None:
        self.__currentMsg = aMessage.name

    def processSignal( self, aSignal: Signal ) -> None:
        if aSignal.spn is not None:
            try:
                self.__signalsDict[ aSignal.spn ]
            except KeyError:
                self.__signalsDict[ aSignal.spn ] = dict()

            if self.__dbcPath not in self.__signalsDict[ aSignal.spn ].keys():
                self.__signalsDict[ aSignal.spn ][ self.__dbcPath ] = list()

            self.__signalsDict[ aSignal.spn ][ self.__dbcPath ].append( str.format( "{}->{}", self.__currentMsg, aSignal.name ) )

    def getName( self ) -> str:
        return "DBC Signals Duplicate Checker"
