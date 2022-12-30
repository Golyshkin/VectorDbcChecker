from DbcCheckEngine import *
from DbcCheckerInterface import *

class DbcCheckDuplicates( DbcCheckerInterface ):

    def __init__( self ):
        self._messagesDict = dict()
        self._duplicatesInfoDict = dict()

    def processDbcFile( self, aDataBase: candb.Database, aDbcPath: str ):
        for message in aDataBase.messages:
            if message.frame_id in self._messagesDict:
                try:
                    self._duplicatesInfoDict[ message.name ]
                except KeyError:
                    self._duplicatesInfoDict[ message.name ] = set()
                self._duplicatesInfoDict[ message.name ].add( (aDbcPath, message.signals.__str__().__hash__()) )
                self._duplicatesInfoDict[ message.name ].add( (self._messagesDict[ message.frame_id ][ "path" ], self._messagesDict[ message.frame_id ][ "hash" ]) )
            else:
                self._messagesDict[ message.frame_id ] = dict()
                self._messagesDict[ message.frame_id ][ "path" ] = aDbcPath
                self._messagesDict[ message.frame_id ][ "hash" ] = message.signals.__str__().__hash__()

    def onStart( self ):
        DbcCheckConfig.LOGGER.info( "DBC Duplicator Checker Registered." )

    def onFinish( self ):
        self.printReport()

    def printReport( self ):
        DbcCheckConfig.LOGGER.info( "START DUPLICATE REPORT" )

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
                    DbcCheckConfig.LOGGER.info( "" )
                    DbcCheckConfig.LOGGER.info( "Found duplicate of '{}' message".format( key ) )
                    for msgInfo in self._duplicatesInfoDict[ key ]:
                        DbcCheckConfig.LOGGER.info( "for '{0}' with signals hash '{1}'".format( msgInfo[ 0 ], msgInfo[ 1 ] ) )
                    DbcCheckConfig.LOGGER.info( "" )
        else:
            DbcCheckConfig.LOGGER.info( "No duplicates found." )
        DbcCheckConfig.LOGGER.info( "END DUPLICATE REPORT" )
