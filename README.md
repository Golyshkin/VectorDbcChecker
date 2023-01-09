# VectorDbcChecker

VectorDBCChecker a Python 3.10x written application for simple checking single or list of DBC files for:

1. Messages duplication (in case of directory for checking was selected)
2. Signals overlap in message
3. Missed network nodes
4. Signal byte order mismatch
5. Signals SPN duplication
6. etc..

Actually, DBC Checker application was designed to simply extend checkers functionality and to easily adding a new DBC
checkers to the project.

The following projects files are responsible for:

1. **DbcCheckConfig.py** - Project configuration
2. **DbcCheckEngine.py** - Check engine with base check bejavior
3. **DbcCheckerInterface.py** - common interfaces for all available DBC checkers
4. **DbcCheckMain.py** - MAIN entrance
5. **DbcCheckUiApplication.py** - GUI application
6. **DbcCheckUiSettings.py** - GUI application settings
7. **DbcMsgDuplicatesChecker.py** - DBC messages duplication checker
8. **DbcNodesChecker.py** - DBC missed network nodes checker
9. **DbcBaseChecker.py** - DBC base checker
10. **DbcSigDuplicatesChecker.py** - DBC signal duplication checker
11. **DbcSigByteOrderChecker.py** - DBC signal byte order checker
12. **examples/dbc-check.log** - an example of application output for selected directory with some DBC files

An application screenshot is following

![](https://github.com/Golyshkin/VectorDbcChecker/blob/main/examples/vectordbcchecker-screenshot.png#4)

An application output log
is [available here](https://github.com/Golyshkin/VectorDbcChecker/blob/main/examples/dbc-check.log)

# Build instructions

Actually the project has the following external modules dependency

1. **cantools** - need to install this module before starting a GUI application
2. Clone project according to GitHub instructions
3. Since project based on Python is not necessary to compile & link this project
4. Run the application using console command: **py DbcCheckMain.py**

PS. For those people who don't want to install the Python 3.10x, there is compiled EXE for
WINDOWSx64 [located here](https://github.com/Golyshkin/VectorDbcChecker/blob/main/examples/DbcCheckMain-windows64-exe.zip)
