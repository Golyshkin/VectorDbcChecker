# VectorDbcChecker

VectorDBCChecker a Python written application for simple checking single or list of DBC files for:

1. Messages duplication (in case of directory for checking was selected)
2. Signals overlap in message
3. Missed network nodes
4. etc..

Actually application was designed to simple extend checker functionality and easy adding a new DBC checkers to project.

The following projects files are responsible for:

1. **DbcCheckConfig.py** - Project configuration
2. **DbcCheckEngine.py** - Check engine with base check bejavior
3. **DbcCheckerInterface.py** - common interfaces for all available DBC checkers
4. **DbcCheckMain.py** - MAIN enterance
5. **DbcCheckUiApplication.py** - GUI application
6. **DbcCheckUiSettings.py** - GUI application settings
7. **DbcDuplicatesChecker.py** - DBC messages duplication checker
8. **DbcNodesChecker.py** - DBC missed network nodes checker
9. **DbcBaseChecker.py** - DBC base checker
10. **examples/dbc-check.log** - an example of applicaton output for selected directory with some DBC files

An application screenshot is following

![](https://github.com/Golyshkin/VectorDbcChecker/blob/main/examples/vectordbcchecker-screenshot.png#3)

An application output log is [available here](https://github.com/Golyshkin/VectorDbcChecker/blob/main/examples/dbc-check.log)

# Build instructions

Actually the project has following external modules dependency
1. **cantools** - need to install this module before starting a GUI application
2. Clone project according to github instructions
3. Since project based on Python is not necessary to compile & link this project
4. Run the application using conslole command: **py DbcCheckMain.py**
