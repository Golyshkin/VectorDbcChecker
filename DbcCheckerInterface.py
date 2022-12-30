from abc import abstractmethod

import cantools.database.can.database as candb

class DbcCheckerInterface:

    @abstractmethod
    def processDbcFile( self, aDataBase: candb.Database, aDbcPath: str ) -> None:
        """
        Start processing a DBC file.

        :param aDataBase: dbc database
        :param aDbcPath: dbc file path
        :return: void
        """
        raise NotImplementedError()

    @abstractmethod
    def printReport( self ) -> None:
        """
        Make a report for finished DBC files.

        :return: void
        """
        raise NotImplementedError()

    @abstractmethod
    def onFinish( self ) -> None:
        """
        This method will be invoked when engine is finished processing all DBC files.

        :return: void
        """
        raise NotImplementedError()

    @abstractmethod
    def onStart( self ) -> None:
        """
        This method will be invoked when engine is started processing DBC files.

        :return: void
        """
        raise NotImplementedError()
