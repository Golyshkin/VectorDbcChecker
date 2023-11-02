# VectorDbcChecker

VectorDBCChecker a Python 3.10x written application (Windows/Linux) for simple checking single or list of DBC files for:

1. Messages duplication (in case of directory for checking was selected)
2. Signals overlap in message
3. Missed network nodes
4. Signal byte order mismatch
5. Signals SPN duplication
6. etc..

Actually, DBC Checker application was designed to simply extend checkers functionality and to easily adding a new DBC
checkers to the project.

The following projects files are responsible for:

1. **checkers** - Folder contains CHECKERs rules
2. **common** - Prohect common files
3. **common/DbcCheckConfig.py** - Project configuration
4. **interfaces** - Project interfaces
5. **ui** - Project UI files
6. **DbcCheckMain.py** - MAIN py script
7. **examples** - Folder contains an examples

An application screenshot is following

![](https://github.com/Golyshkin/VectorDbcChecker/blob/main/examples/vectordbcchecker-screenshot.png#4)

# Build instructions

Actually the project has the following external modules dependency

1. Clone project according to GitHub instructions
2. **$> pip install -r requirements.txt** - need to install required modules before starting a GUI application
3. Since project based on Python is not necessary to compile & link this project
4. Run the application using console command: **py DbcCheckMain.py**

PS. For those people who don't want to install the Python 3.10x, there is compiled EXE for
WINDOWSx64 [located here](https://github.com/Golyshkin/VectorDbcChecker/blob/main/examples/DbcCheckMain-windows64-exe.zip)
