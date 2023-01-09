import os
from pathlib import Path

import cantools as can

import DbcCheckConfig
from DbcBaseChecker import DbcBaseChecker
from DbcCheckerInterface import *
from DbcSigByteOrderChecker import DbcSigByteOrderChecker

class DbcCheckEngine:
    DBC_EXT = "dbc"
    __checkersList: set[ DbcCheckerInterface ] = { DbcBaseChecker() }

    def __init__( self, startPath, outputCallback, finishCallback ):
        self.startPath = startPath
        self.outputCallback = outputCallback
        self.finishCallback = finishCallback

    @staticmethod
    def addChecker( aChecker: DbcCheckerInterface ) -> None:
        """
        Add a new checker.
        :param aChecker: new checker

        :return: void
        """
        DbcCheckEngine.__checkersList.add( aChecker )

    @staticmethod
    def clearCheckers() -> None:
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
        return self.startPath

    def startCheck( self ):
        """
        Start check procedure.

        :return: void
        """
        for checker in DbcCheckEngine.__checkersList:
            checker.onStart()

        if os.path.isdir( self.startPath ):
            for r, d, f in os.walk( self.startPath ):
                for file in f:
                    file = str( file )
                    if file.lower().endswith( "." + self.DBC_EXT ):
                        self.__processSingleFile( os.path.join( r, file ) )
        else:
            self.__processSingleFile( self.startPath )

        for checker in DbcCheckEngine.__checkersList:
            checker.onFinish()

        self.finishCallback()

    def __processSingleFile( self, aFilePath: str ) -> None:
        """
        Process a single DBC file
        :param aFilePath: a full path to file which need to be processed

        :return: void
        """
        self.outputCallback( "Processed '{}'".format( Path( aFilePath ).absolute() ) )
        try:
            db = can.db.load_file( aFilePath, strict=DbcCheckConfig.CONF_CHECK_OVERLAP_SIGNALS )
        except Exception as e:
            DbcCheckConfig.LOGGER.error( "{}".format( e ) )
            return

        for checker in DbcCheckEngine.__checkersList:
            checker.processDbcFile( db, aFilePath )

        for message in db.messages:
            for checker in DbcCheckEngine.__checkersList:
                checker.processMessage( message )

            for signal in message.signals:
                for checker in DbcCheckEngine.__checkersList:
                    checker.processSignal( signal )
