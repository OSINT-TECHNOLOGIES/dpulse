@echo off
set /p UserInput=Do you want to start installer? [Y/N]: 
if /I "%UserInput%" neq "Y" goto End

echo.

:CheckGit
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo Git is not installed. Please install Git first.
    set GIT_NOT_INSTALLED=1
) else (
    set GIT_NOT_INSTALLED=0
)

echo.

:Menu
echo Select appropriate menu item
echo.
echo [1] Clone repository and install requirements (requires installed Git)
echo [2] Only install requirements
echo.
set /p UserChoice=Enter the number: 

echo.

if "%UserChoice%"=="1" (
    if %GIT_NOT_INSTALLED%==1 (
        echo You cannot clone the repository because Git is not installed.
        echo.
        goto Menu
    )
    call :CloneAndInstall
) else if "%UserChoice%"=="2" (
    call :InstallDependencies
) else (
    echo Incorrect choice.
    echo.
    goto Menu
)

goto End

:CloneAndInstall
echo Cloning repository and installing requirements...
git clone https://github.com/OSINT-TECHNOLOGIES/dpulse
cd dpulse
pip install -r requirements.txt

echo.

goto End

:InstallDependencies
echo Installing requirements...
pip install -r requirements.txt

echo.

goto End

:End
echo Installation end.
echo.
pause
