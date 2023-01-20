from abc import abstractmethod

import cantools.database.can.database as candb
from cantools.database.can.message import Message
from cantools.database.can.signal import Signal

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
    def processMessage( self, aMessage: Message ) -> None:
        """
        Start a new message processing in DBC file.

        :param aMessage: dbc message object
        :return: void
        """
        raise NotImplementedError()

    @abstractmethod
    def processSignal( self, aSignal: Signal ) -> None:
        """
        Start a new signal processing in DBC message.

        :param aSignal: dbc message signal object
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
