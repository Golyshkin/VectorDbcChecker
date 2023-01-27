import xml.etree.ElementTree as ET
from os import path

from common import DbcCheckConfig
from common.DbcCheckUtils import LOGGER
from interfaces.DbcCheckerInterface import *

class DbcMsgCheckWithPolarionIntegration( DbcCheckerInterface ):
    CONFIG: dict = { }

    def __init__( self ):
        DbcMsgCheckWithPolarionIntegration.initConfig()

    @staticmethod
    def initConfig() -> None:
        """
        Process configuration.xml file

        :return dictionary
        """
        if path.exists( DbcCheckConfig.APP_CONFIG_XML_PATH ):
            rootNode = ET.parse( DbcCheckConfig.APP_CONFIG_XML_PATH ).getroot()

            DbcMsgCheckWithPolarionIntegration.CONFIG[ "polarionUrl" ] = rootNode.findtext( "polarionUrl" )
            DbcMsgCheckWithPolarionIntegration.CONFIG[ "polarionLogin" ] = rootNode.findtext( "polarionLogin" )
            DbcMsgCheckWithPolarionIntegration.CONFIG[ "polarionPwd" ] = rootNode.findtext( "polarionPwd" )

            documentLocations = [ ]
            for documentLocation in rootNode.findall( 'documentLocations/documentLocation' ):
                documentLocations.append( documentLocation.text )

            DbcMsgCheckWithPolarionIntegration.CONFIG[ "documentLocations" ] = documentLocations
        else:
            LOGGER.error( f"{DbcCheckConfig.APP_CONFIG_XML_PATH} is not exists" )

    def processDbcFile( self, aDataBase: candb.Database, aDbcPath: str ) -> None:
        pass

    def processMessage( self, aMessage: Message ) -> None:
        pass

    def processSignal( self, aSignal: Signal ) -> None:
        pass

    def printReport( self ) -> None:
        pass

    def onFinish( self ) -> None:
        pass

    def onStart( self ) -> None:
        LOGGER.info( "DBC Polarion Integrations Checker Registered." )
