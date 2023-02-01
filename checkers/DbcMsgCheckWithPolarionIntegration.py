import xml.etree.ElementTree as ET
from collections import defaultdict
from enum import Enum
from os import path
from pathlib import Path
from typing import cast

from polarion import polarion
from polarion.workitem import Workitem

from common import DbcCheckConfig
from common.DbcCheckUtils import LOGGER
from exceptions.DbcCheckException import DbcCheckException
from interfaces.DbcCheckerInterface import *

class DbcMsgCheckWithPolarionIntegration( DbcCheckerInterface ):
    class CHECK_STATUS( Enum ):
        OK = 0x0
        NOK = 0x1

    DBC_FILE_KEY = "dbcFile"
    DBC_MSG_KEY = "dbcMsg"
    DBC_SIG_KEY = "dbcSig"
    DBC_CHECK_STATUS_KEY = "checkStatus"

    m_SystemIntegrationType = "sysIntegration"
    m_PlrnProjectId = "ADP"

    CONFIG: dict = { }
    m_IsActive: bool = True
    m_CurDbcName: str = ""
    m_CurMsgName: str = ""

    """
    Default PLRN dictionary structure is following
    {
       "<documentId>":
       {
          "<workitemId>":
          {
             "dbcFile": ""
             "dbcMsg": ""
             "dbcSig": ""
             "checkStatus":
             {
                 "dbcFile": CHECK_STATUS value
                 "dbcMsg": CHECK_STATUS value
                 "dbcSig": CHECK_STATUS value
             }
          }
       }
    }
    """
    m_PlrInfo: dict = defaultdict( lambda: defaultdict( lambda: defaultdict() ) )

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
        return "DBC Polarion Integrations Checker"

    def processDbcFile( self, aDataBase: candb.Database, aDbcPath: str ) -> None:
        self.m_CurDbcName = Path( aDbcPath ).name

        for docDictValue in self.m_PlrInfo.values():
            for wiNameDictValue in docDictValue.values():
                if wiNameDictValue[ self.DBC_FILE_KEY ] == self.m_CurDbcName:
                    wiNameDictValue[ self.DBC_CHECK_STATUS_KEY ][ self.DBC_FILE_KEY ] = self.CHECK_STATUS.OK

    def processMessage( self, aMessage: Message ) -> None:
        self.m_CurMsgName = aMessage.name

        for docDictValue in self.m_PlrInfo.values():
            for wiNameDictValue in docDictValue.values():
                if wiNameDictValue[ self.DBC_MSG_KEY ] == self.m_CurMsgName and wiNameDictValue[ self.DBC_FILE_KEY ] == self.m_CurDbcName:
                    wiNameDictValue[ self.DBC_CHECK_STATUS_KEY ][ self.DBC_MSG_KEY ] = self.CHECK_STATUS.OK

    def processSignal( self, aSignal: Signal ) -> None:
        for docDictValue in self.m_PlrInfo.values():
            for wiNameDictValue in docDictValue.values():
                if wiNameDictValue[ self.DBC_MSG_KEY ] == self.m_CurMsgName and wiNameDictValue[ self.DBC_FILE_KEY ] == self.m_CurDbcName and wiNameDictValue[ self.DBC_SIG_KEY ] == aSignal.name:
                    wiNameDictValue[ self.DBC_CHECK_STATUS_KEY ][ self.DBC_SIG_KEY ] = self.CHECK_STATUS.OK

    def printReport( self ) -> None:
        LOGGER.info( "" )
        LOGGER.info( f"START {self.getName()} REPORT" )

        for docDictKey, docDictValue in self.m_PlrInfo.items():
            LOGGER.info( f"\t{docDictKey} Report" )
            for wiNameDictKey, wiNameDictValue in docDictValue.items():
                LOGGER.info( f"\t\t{wiNameDictKey} WorkItem Report" )
                LOGGER.info( f"\t\t\t{wiNameDictValue[ self.DBC_FILE_KEY ]} -> {wiNameDictValue[ self.DBC_CHECK_STATUS_KEY ][ self.DBC_FILE_KEY ]}" )
                LOGGER.info( f"\t\t\t{wiNameDictValue[ self.DBC_MSG_KEY ]} -> {wiNameDictValue[ self.DBC_CHECK_STATUS_KEY ][ self.DBC_MSG_KEY ]}" )
                LOGGER.info( f"\t\t\t{wiNameDictValue[ self.DBC_SIG_KEY ]} -> {wiNameDictValue[ self.DBC_CHECK_STATUS_KEY ][ self.DBC_SIG_KEY ]}" )
            LOGGER.info( "" )

        LOGGER.info( f"END {self.getName()} REPORT" )

    def onFinish( self ) -> None:
        self.printReport()

    def onStart( self ) -> None:
        LOGGER.info( f"{self.getName()} Registered." )
        plrn = polarion.Polarion( polarion_url=DbcMsgCheckWithPolarionIntegration.CONFIG[ "polarionUrl" ], user=DbcMsgCheckWithPolarionIntegration.CONFIG[ "polarionLogin" ], password=DbcMsgCheckWithPolarionIntegration.CONFIG[ "polarionPwd" ] )
        prj = plrn.getProject( project_id=self.m_PlrnProjectId )
        for documentLocation in DbcMsgCheckWithPolarionIntegration.CONFIG[ "documentLocations" ]:
            LOGGER.info( f"Start polarion [{documentLocation}] document processing." )
            try:
                for sysIntegrationWiRaw in prj.searchWorkitemFullItem( query=f"type:{self.m_SystemIntegrationType} AND '{documentLocation}'" ):

                    sysIntegrationWi: Workitem = cast( Workitem, sysIntegrationWiRaw )
                    syssIntegartionContent: str = sysIntegrationWi.getCustomField( "implementation" ).__getattribute__( "content" )
                    try:
                        type, dbc, msg, sig = syssIntegartionContent.split( '\n', maxsplit=3 )
                    except ValueError as exception:
                        LOGGER.error( f"Ignoring the {sysIntegrationWi.__getattribute__( 'type' ).id} since format is unknown : {syssIntegartionContent}" )

                    if cast( str, type ).__contains__( "CAN" ):
                        self.m_PlrInfo[ documentLocation ][ sysIntegrationWi.__getattribute__( "id" ) ][ self.DBC_FILE_KEY ] = cast( str, dbc ).split( ':' )[ 1 ].strip()
                        self.m_PlrInfo[ documentLocation ][ sysIntegrationWi.__getattribute__( "id" ) ][ self.DBC_MSG_KEY ] = cast( str, msg ).split( ':' )[ 1 ].strip()
                        self.m_PlrInfo[ documentLocation ][ sysIntegrationWi.__getattribute__( "id" ) ][ self.DBC_SIG_KEY ] = cast( str, sig ).split( ':' )[ 1 ].strip()
                        self.m_PlrInfo[ documentLocation ][ sysIntegrationWi.__getattribute__( "id" ) ][ self.DBC_CHECK_STATUS_KEY ]: dict = { }
                        self.m_PlrInfo[ documentLocation ][ sysIntegrationWi.__getattribute__( "id" ) ][ self.DBC_CHECK_STATUS_KEY ][ self.DBC_FILE_KEY ] = self.CHECK_STATUS.NOK
                        self.m_PlrInfo[ documentLocation ][ sysIntegrationWi.__getattribute__( "id" ) ][ self.DBC_CHECK_STATUS_KEY ][ self.DBC_MSG_KEY ] = self.CHECK_STATUS.NOK
                        self.m_PlrInfo[ documentLocation ][ sysIntegrationWi.__getattribute__( "id" ) ][ self.DBC_CHECK_STATUS_KEY ][ self.DBC_SIG_KEY ] = self.CHECK_STATUS.NOK
            except Exception as exception:
                LOGGER.error( f"{self.getName()} plugin is deactivated due exception \"{exception}\"" )
                self.m_IsActive = False
