import xml.etree.ElementTree as ET
from os import path

from common import DbcCheckConfig
from common.DbcCheckUtils import LOGGER
from exceptions.DbcCheckException import DbcCheckException
from interfaces.DbcCheckerInterface import *

class DbcMsgCheckWithPolarionIntegration( DbcCheckerInterface ):
    CONFIG: dict = { }
    m_IsActive: bool = True

    def isActive( self ) -> bool:
        return self.m_IsActive

    def __init__( self ):
        self.initConfig()

    def initConfig( self ) -> None:
        """
        Process configuration.xml file

        :return dictionary
        """
        try:
            if path.exists( DbcCheckConfig.APP_CONFIG_XML_PATH ):
                try:
                    rootNode = ET.parse( DbcCheckConfig.APP_CONFIG_XML_PATH ).getroot()

                    DbcMsgCheckWithPolarionIntegration.CONFIG[ "polarionUrl" ] = rootNode.findtext( "polarionUrl" )
                    DbcMsgCheckWithPolarionIntegration.CONFIG[ "polarionLogin" ] = rootNode.findtext( "polarionLogin" )
                    DbcMsgCheckWithPolarionIntegration.CONFIG[ "polarionPwd" ] = rootNode.findtext( "polarionPwd" )

                    documentLocations = [ ]
                    for documentLocation in rootNode.findall( 'documentLocations/documentLocation' ):
                        documentLocations.append( documentLocation.text )

                    DbcMsgCheckWithPolarionIntegration.CONFIG[ "documentLocations" ] = documentLocations
                except Exception as exception:
                    raise DbcCheckException( exception.__str__() )
            else:
                raise DbcCheckException( f"config {path} is not exists." )
        except DbcCheckException as exception:
            LOGGER.error( f"{self.getName()} plugin is deactivated due exception \"{exception}\"" )
            self.m_IsActive = False

    def getName( self ) -> str:
        return "DbcMsgCheckWithPolarionIntegration"

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
