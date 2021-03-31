@echo OFF
echo Windows venv creator will create a Python virtual 
echo environment (venv) and install a list of Python 
echo packages in that venv. 

@echo.

echo After each package is installed, the installer will 
echo pause awaiting a keypress. This will echo enable you 
echo to check the install details as it progresses.

@echo.

echo Before proceeding, make sure that you have 
echo installed Python (suggested location is C:\).

@echo.

echo Second, make sure you are in the root of the 
echo folder you want to work from. Copy this batch 
echo file into that folder.

@echo.

echo Now we will install the virtual environnment
echo (folder = venv).

pause

@echo.

echo creating Python venv
python -m venv venv

@echo.

echo Now we will activete venv.

pause

@echo.

echo Activating venv
venv\Scripts\activate.bat

@echo.

echo Now we will install the Python packages that are
echo listed in this batch file.

pause

REM *** On Linux or macOS ***
REM pip install -U pip     

REM *** On Windows ***

python -m pip install -U pip      

REM pip install pyserial
REM pip install PyQt5
REM pip install PyQt5Designer
REM pip install pyinstaller
REM pip install numpy

pip install jscatter

