import os
import os.path
import platform
import subprocess
import tkinter.filedialog
from tkinter import *
from tkinter import scrolledtext, messagebox
from typing import cast

from pywin.mfc.object import Object

import DbcCheckConfig
import DbcCheckUiSettings

class DbcCheckUiApplication( Object ):
    def __del__( self ):
        pass

    def __init__( self, aOnStartCheckCallback ):
        Object.__init__( self )
        self.resultFolder = None
        self.title = None
        self.output = None
        self.selectFolderBtn = None
        self.strutLabel = None
        self.directoryInput = None
        self.dirLabel = None
        self.menu = None
        self.settingsUi: DbcCheckUiSettings = None

        self.onStartCheckCallback = aOnStartCheckCallback
        self.rootFrame = Tk()
        self.rootFrame.title( DbcCheckConfig.APP_TITLE )
        self.rootFrame.rowconfigure( 3, weight=1 )
        self.rootFrame.columnconfigure( 0, weight=1 )
        self.rootFrame.minsize( width=640, height=480 )
        self.rootFrame.geometry( DbcCheckConfig.APP_WIN_SIZE_APP )

    def configureMenu( self ):
        # File menu
        fileMenu = Menu( tearoff=0 )
        fileMenu.add_command( label="Open File", command=self.onOpenFile )
        fileMenu.add_command( label="Exit", command=lambda: self.rootFrame.destroy() )
        # Main Menu
        self.menu = Menu()
        self.menu.add_cascade( label="File", menu=fileMenu )
        self.menu.add_cascade( label="Settings", command=self.onOpenSettings )
        self.menu.add_cascade( label="About", command=lambda: messagebox.showinfo( "About", DbcCheckConfig.APP_ABOUT_INFO ) )

    def configureLabels( self ):
        self.dirLabel = Label( text="Initial Directory Search Path:" )
        self.dirLabel.grid( row=0, column=0, sticky="NW", padx=DbcCheckConfig.CONF_PAD_DX )
        self.title = Label( text="Results Output:" )
        self.title.grid( row=2, column=0, sticky="NW", padx=DbcCheckConfig.CONF_PAD_DX )

    def configureInputs( self ):
        self.directoryInput = Entry()
        self.directoryInput.grid( row=1, column=0, columnspan=2, sticky="NEWS", padx=DbcCheckConfig.CONF_PAD_DX, ipadx="10" )
        self.strutLabel = Label()
        self.strutLabel.grid( row=1, column=1, padx=DbcCheckConfig.CONF_PAD_DX )

    def configureButtons( self ):
        self.selectFolderBtn = Button( self.rootFrame, text="Select Folder", width="10", command=self.onSelectFolderClick )
        self.selectFolderBtn.grid( row=1, column=2, rowspan=3, sticky="N", padx=DbcCheckConfig.CONF_PAD_DX )

        self.selectFolderBtn = Button( self.rootFrame, text="Start Check", width="10", command=self.onStartCheckClick )
        self.selectFolderBtn.grid( row=3, column=2, rowspan=3, sticky="N", padx=DbcCheckConfig.CONF_PAD_DX )

    def configureOutput( self ):
        self.output = scrolledtext.ScrolledText( self.rootFrame )
        self.output.grid( row=3, column=0, sticky="NEWS", padx=DbcCheckConfig.CONF_PAD_DX, pady=DbcCheckConfig.CONF_PAD_DY )

    def configureStatusBar( self ):
        versionText = StringVar( value=str.format( "v.{}", DbcCheckConfig.APP_VER ) )
        self.statusBarLabel = Label( master=self.rootFrame, anchor="w", textvariable=versionText )
        self.statusBarLabel.grid( row=4, column=0, columnspan=4, sticky="E", padx=DbcCheckConfig.CONF_PAD_DX, pady=DbcCheckConfig.CONF_PAD_DY )

    def onStartCheckClick( self ):
        if len( self.directoryInput.get() ) > 0:
            if os.path.exists( self.directoryInput.get() ):
                cast( scrolledtext.ScrolledText, self.output ).delete( '1.0', "end" )
                self.onStartCheckCallback( self.directoryInput.get() )
            else:
                messagebox.showerror( "Error", "The {} directory is not exists.\n\nPlease select an existing directory for start check procedure.".format( self.directoryInput.get() ) )
        else:
            messagebox.showerror( "Error", "Please select initial directory for start DBC search first." )

    @staticmethod
    def onFinish() -> None:
        if messagebox.askyesno( "Information", "DBC-Check was successfully finished.\n\nDo you want open the created {}?".format( DbcCheckConfig.CONF_LOG_FILE_NAME ) ) is True:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call( ('open', DbcCheckConfig.CONF_LOG_FILE_NAME) )
            elif platform.system() == 'Windows':  # Windows
                os.startfile( DbcCheckConfig.CONF_LOG_FILE_NAME )
            else:  # linux variants
                subprocess.call( ('xdg-open', DbcCheckConfig.CONF_LOG_FILE_NAME) )

    def onSelectFolderClick( self ):
        self.resultFolder = tkinter.filedialog.askdirectory( title="Choose the folder for start search DBC files..." )
        cast( Entry, self.directoryInput ).delete( 0, "end" )
        self.directoryInput.insert( "0", self.resultFolder )

    def onOpenSettings( self ):
        if self.settingsUi is not None:
            self.settingsUi.destroy()

        self.settingsUi = DbcCheckUiSettings.DbcAppSettings( self.rootFrame )
        self.settingsUi.showUi()

    def onOpenFile( self ) -> None:
        selectedFile = tkinter.filedialog.askopenfilename( title="Choose the DBC file for start checking...", filetypes=[ ('DBC Files', '*.dbc') ] )
        cast( Entry, self.directoryInput ).delete( 0, "end" )
        self.directoryInput.insert( "0", selectedFile )
        return

    def configureUi( self ):
        self.configureMenu()
        self.configureLabels()
        self.configureInputs()
        self.configureButtons()
        self.configureOutput()
        self.configureStatusBar()

    def showUI( self ):
        self.configureUi()
        self.rootFrame.config( menu=self.menu )
        self.rootFrame.mainloop()

    def insertOutput( self, text ):
        self.output.insert( tkinter.INSERT, "{}\n".format( text ) )
        cast( scrolledtext.ScrolledText, self.output ).see( "end" )
        DbcCheckConfig.LOGGER.info( text )
