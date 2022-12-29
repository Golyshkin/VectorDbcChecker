from abc import abstractmethod

import cantools.database.can.database as candb

class DbcCheckerInterface:

    @abstractmethod
    def processDbcFile( self, aDataBase: candb.Database, aDbcPath: str ):
        raise NotImplementedError()

    @abstractmethod
    def printReport( self ):
        raise NotImplementedError()

    @abstractmethod
    def onFinish( self ):
        raise NotImplementedError()
