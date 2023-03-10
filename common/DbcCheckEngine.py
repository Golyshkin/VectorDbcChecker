import os
from pathlib import Path

import cantools as can

from checkers.DbcBaseChecker import DbcBaseChecker
from checkers.DbcSigByteOrderChecker import DbcSigByteOrderChecker
from common import DbcCheckConfig
from common.DbcCheckUtils import LOGGER
from interfaces.DbcCheckerInterface import *

class DbcCheckEngine:
    DBC_EXT = "dbc"
    __checkersList: set[ DbcCheckerInterface ] = set()

    def __init__( self, startPath, outputCallback, finishCallback ):
        self.__startPath = startPath
        self.__outputCallback = outputCallback
        self.__finishCallback = finishCallback
        DbcCheckEngine.initCheckers()

    @staticmethod
    def addChecker( aChecker: DbcCheckerInterface ) -> None:
        """
        Add a new checker.
        :param aChecker: new checker

        :return: void
        """
        DbcCheckEngine.__checkersList.add( aChecker )

    @staticmethod
    def initCheckers() -> None:
        """
        Clear all checkers from subscribe list

        :return: void
        """
        DbcCheckEngine.__checkersList.clear()
        DbcCheckEngine.__addDefaultCheckers()

    @staticmethod
    def __addDefaultCheckers() -> None:
        """
        Add default checkers to engine
        :return: void
        """
        DbcCheckEngine.addChecker( DbcBaseChecker() )
        DbcCheckEngine.addChecker( DbcSigByteOrderChecker() )

    @property
    def getStartFolder( self ) -> str:
        return self.__startPath

    def startCheck( self ):
        """
        Start check procedure.

        :return: void
        """
        for checker in DbcCheckEngine.__checkersList:
            if checker.isActive():
                self.__outputCallback( f"Initializing '{checker.getName()}' ..." )
                checker.onStart()

        if os.path.isdir( self.__startPath ):
            for r, d, f in os.walk( self.__startPath ):
                for file in f:
                    file = str( file )
                    if file.lower().endswith( "." + self.DBC_EXT ):
                        self.__processSingleFile( os.path.join( r, file ) )
        else:
            self.__processSingleFile( self.__startPath )

        for checker in DbcCheckEngine.__checkersList:
            if checker.isActive():
                checker.onFinish()

        self.__finishCallback()

    def __processSingleFile( self, aFilePath: str ) -> None:
        """
        Process a single DBC file
        :param aFilePath: a full path to file which need to be processed

        :return: void
        """
        self.__outputCallback( "Processed '{}'".format( Path( aFilePath ).absolute() ) )
        try:
            db = can.db.load_file( aFilePath, strict=DbcCheckConfig.CONF_CHECK_OVERLAP_SIGNALS )
        except Exception as e:
            LOGGER.error( "{}".format( e ) )
            return

        for checker in DbcCheckEngine.__checkersList:
            if checker.isActive():
                checker.processDbcFile( db, aFilePath )

        for message in db.messages:
            for checker in DbcCheckEngine.__checkersList:
                if checker.isActive():
                    checker.processMessage( message )

            for signal in message.signals:
                for checker in DbcCheckEngine.__checkersList:
                    if checker.isActive():
                        checker.processSignal( signal )
