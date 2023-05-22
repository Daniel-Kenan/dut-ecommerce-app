@echo on

REM Check if virtualenv is installed
python -c "import virtualenv" 2>NUL

IF %ERRORLEVEL% NEQ 0 (
    REM virtualenv is not installed, install it
    echo Installing virtualenv...
    python -m pip install virtualenv

    REM Check the installation status by verifying the virtualenv module import
    python -c "import virtualenv" 2>NUL
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to install virtualenv.
        exit /b 1
    )
    echo virtualenv installed successfully.
) ELSE (
    echo virtualenv is already installed.
)

REM Create a new virtual environment named "venv"
python -m venv ./venv

REM Activate the virtual environment
cd venv/Scripts && activate && cd ../../

REM Install packages from requirements.txt
pip install -r requirements.txt

REM Display completion message
echo Installation completed.

exit /b 0
