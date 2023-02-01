from common.DbcCheckEngine import *
from interfaces.DbcCheckerInterface import *
from common.DbcCheckUtils import LOGGER

class DbcMsgDuplicatesChecker( DbcCheckerInterface ):

    def __init__( self ):
        self._messagesDict = dict()
        self._duplicatesInfoDict = dict()
        self._dbcPath: str = "N/A"

    def processDbcFile( self, aDataBase: candb.Database, aDbcPath: str ):
        self._dbcPath = Path( aDbcPath ).absolute()

    def onStart( self ):
        LOGGER.info( f"{self.getName()} Registered." )

    def onFinish( self ):
        self.printReport()

    def printReport( self ):
        LOGGER.info( "" )
        LOGGER.info( f"START {self.getName()} REPORT" )

        if len( self._duplicatesInfoDict ):
            for key in self._duplicatesInfoDict:
                isShowMsgDuplicate: bool = False
                if DbcCheckConfig.CONF_IGNORE_MSG_DUP_WITH_SAME_SIGNALS is True:
                    signalHash: int = 0xDEAD
                    for msgInfo in self._duplicatesInfoDict[ key ]:
                        if signalHash == 0xDEAD:
                            signalHash = msgInfo[ 1 ]
                        isShowMsgDuplicate |= signalHash != msgInfo[ 1 ]
                else:
                    isShowMsgDuplicate = True

                if isShowMsgDuplicate:
                    LOGGER.info( "" )
                    LOGGER.info( "Found duplicate of '{}' message".format( key ) )
                    for msgInfo in self._duplicatesInfoDict[ key ]:
                        LOGGER.info( "for '{0}' with signals hash '{1}'".format( msgInfo[ 0 ], msgInfo[ 1 ] ) )
        else:
            LOGGER.info( "No duplicates found." )
        LOGGER.info( f"END {self.getName()} REPORT" )

    def processMessage( self, aMessage: Message ) -> None:
        if aMessage.frame_id in self._messagesDict:
            try:
                self._duplicatesInfoDict[ aMessage.name ]
            except KeyError:
                self._duplicatesInfoDict[ aMessage.name ] = set()
            self._duplicatesInfoDict[ aMessage.name ].add( (self._dbcPath, aMessage.signals.__str__().__hash__()) )
            self._duplicatesInfoDict[ aMessage.name ].add( (self._messagesDict[ aMessage.frame_id ][ "path" ], self._messagesDict[ aMessage.frame_id ][ "hash" ]) )
        else:
            self._messagesDict[ aMessage.frame_id ] = dict()
            self._messagesDict[ aMessage.frame_id ][ "path" ] = self._dbcPath
            self._messagesDict[ aMessage.frame_id ][ "hash" ] = aMessage.signals.__str__().__hash__()

    def processSignal( self, aSignal: Signal ) -> None:
        pass

    def getName( self ) -> str:
        return "DBC Messages Duplicate Checker"
