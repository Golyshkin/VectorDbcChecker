from tkinter import *

import DbcCheckConfig

class DbcAppSettings:

    def __init__( self, aRoot: Tk ):
        self.rootFrame = aRoot
        self.frame = Toplevel( aRoot )
        self.frame.minsize( 300, 200 )
        self.frame.geometry( DbcCheckConfig.APP_WIN_SIZE_SETTINGS )
        self.frame.title( DbcCheckConfig.APP_TITLE + " Settings" )
        self.frame.rowconfigure( 7, weight=1 )
        self.isIgnoreMsgDupWithSameSignalsValue = BooleanVar( value=DbcCheckConfig.CONF_IGNORE_MSG_DUP_WITH_SAME_SIGNALS )
        self.isCheckOverlapSignalsValue = BooleanVar( value=DbcCheckConfig.CONF_CHECK_OVERLAP_SIGNALS )
        self.isCheckMissedNetworkNodesValue = BooleanVar( value=DbcCheckConfig.CONF_CHECK_MISSED_NETWORK_NODES )
        self.isCheckMsgDuplicationValue = BooleanVar( value=DbcCheckConfig.CONF_CHECK_MSG_DUPLICATION )
        self.isCheckSigSpnDuplicationValue = BooleanVar( value=DbcCheckConfig.CONF_CHECK_SIG_SPN_DUPLICATION )
        self.isCheckDbVersionValue = BooleanVar( value=DbcCheckConfig.CONF_CHECK_DB_VERSION )
        self.signalByteOrder = StringVar( value=DbcCheckConfig.SIGNAL_BYTE_ORDER )

    def configureUi( self ) -> None:
        self.checkMsgDuplicationCheckBox = Checkbutton( master=self.frame, text="Check Messages Duplication", variable=self.isCheckMsgDuplicationValue, command=self.onSettingsChange )
        self.checkMsgDuplicationCheckBox.grid( row=0, column=0, padx=DbcCheckConfig.CONF_PAD_DX, sticky="W" )

        self.checkMsgDuplicationCheckBox = Checkbutton( master=self.frame, text="Check Signals SPN Duplication", variable=self.isCheckSigSpnDuplicationValue, command=self.onSettingsChange )
        self.checkMsgDuplicationCheckBox.grid( row=1, column=0, padx=DbcCheckConfig.CONF_PAD_DX, sticky="W" )

        self.ignoreMsgDupWithSameSignalsCheckBox = Checkbutton( master=self.frame, text="Ignore Messages Duplication for the Same Signals", variable=self.isIgnoreMsgDupWithSameSignalsValue, command=self.onSettingsChange )
        self.ignoreMsgDupWithSameSignalsCheckBox.grid( row=2, column=0, padx=DbcCheckConfig.CONF_PAD_DX, sticky="W" )

        self.checkOverlapSignalsCheckBox = Checkbutton( master=self.frame, text="Check Overlap Signals in Messages", variable=self.isCheckOverlapSignalsValue, command=self.onSettingsChange )
        self.checkOverlapSignalsCheckBox.grid( row=3, column=0, padx=DbcCheckConfig.CONF_PAD_DX, sticky="W" )

        self.checkMissedNetworkNodesCheckBox = Checkbutton( master=self.frame, text="Check Missed Network Nodes", variable=self.isCheckMissedNetworkNodesValue, command=self.onSettingsChange )
        self.checkMissedNetworkNodesCheckBox.grid( row=4, column=0, padx=DbcCheckConfig.CONF_PAD_DX, sticky="W" )

        self.checkDbVersionCheckBox = Checkbutton( master=self.frame, text="Check Missed Database version", variable=self.isCheckDbVersionValue, command=self.onSettingsChange )
        self.checkDbVersionCheckBox.grid( row=5, column=0, padx=DbcCheckConfig.CONF_PAD_DX, sticky="W" )

        radioFrame = Frame( self.frame )
        radioFrame.grid( sticky="NEWS" )

        self.signalByteOrderLabel = Label( master=radioFrame, text="Expected Signal Byte Order" )
        self.signalByteOrderLabel.grid( row=0, column=0, columnspan=2, padx=DbcCheckConfig.CONF_PAD_DX, sticky="W" )

        self.radioByteOrderBigEndian = Radiobutton( master=radioFrame, value="big_endian", text="Moto (Big Endian)", variable=self.signalByteOrder, command=self.onSettingsChange )
        self.radioByteOrderBigEndian.grid( row=1, column=0, padx=DbcCheckConfig.CONF_PAD_DX, sticky="W" )

        self.radioByteOrderLittleEndian = Radiobutton( master=radioFrame, value="little_endian", text="Intel (Little Endian)", variable=self.signalByteOrder, command=self.onSettingsChange )
        self.radioByteOrderLittleEndian.grid( row=1, column=1, padx=DbcCheckConfig.CONF_PAD_DX, sticky="W" )

        self.applyButton = Button( master=self.frame, text="Apply", command=lambda: self.onApplySettings() )
        self.applyButton.grid( row=7, column=2, padx=DbcCheckConfig.CONF_PAD_DX, pady=DbcCheckConfig.CONF_PAD_DY, sticky="ES" )
        self.closeButton = Button( master=self.frame, text="Close", command=lambda: self.frame.destroy() )
        self.closeButton.grid( row=7, column=3, padx=DbcCheckConfig.CONF_PAD_DX, pady=DbcCheckConfig.CONF_PAD_DY, sticky="WS" )

    def onSettingsChange( self ) -> None:
        DbcCheckConfig.CONF_IGNORE_MSG_DUP_WITH_SAME_SIGNALS = self.isIgnoreMsgDupWithSameSignalsValue.get()
        DbcCheckConfig.CONF_CHECK_OVERLAP_SIGNALS = self.isCheckOverlapSignalsValue.get()
        DbcCheckConfig.CONF_CHECK_MISSED_NETWORK_NODES = self.isCheckMissedNetworkNodesValue.get()
        DbcCheckConfig.CONF_CHECK_MSG_DUPLICATION = self.isCheckMsgDuplicationValue.get()
        DbcCheckConfig.CONF_CHECK_SIG_SPN_DUPLICATION = self.isCheckSigSpnDuplicationValue.get()
        DbcCheckConfig.isCheckDbVersionValue = self.isCheckDbVersionValue.get()
        DbcCheckConfig.SIGNAL_BYTE_ORDER = self.signalByteOrder.get()

    def onApplySettings( self ) -> None:
        # Do nothing all things are applied automatically now
        self.destroy()

    def showUi( self ) -> None:
        self.configureUi()

    def destroy( self ) -> None:
        self.frame.destroy()
