@echo off
echo ========================================
echo  Gesture Detector - Setup Script
echo ========================================
echo.

REM --- Try to find and use Conda ---
set "CONDA_FOUND=0"
set "CONDA_EXE="

REM Method 1: Check if conda is in PATH
where conda >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Found conda in PATH
    set "CONDA_EXE=conda"
    set "CONDA_FOUND=1"
)

REM Method 2: Try E:\Conda directly (your specific case)
if %CONDA_FOUND% EQU 0 (
    if exist "E:\Conda\condabin\conda.bat" (
        echo Found Conda at E:\Conda
        set "CONDA_EXE=E:\Conda\condabin\conda.bat"
        set "CONDA_FOUND=1"
    )
)

REM Method 3: Try other common locations
if %CONDA_FOUND% EQU 0 (
    if exist "%USERPROFILE%\anaconda3\condabin\conda.bat" (
        echo Found Conda in user Anaconda3
        set "CONDA_EXE=%USERPROFILE%\anaconda3\condabin\conda.bat"
        set "CONDA_FOUND=1"
    )
)

if %CONDA_FOUND% EQU 0 (
    if exist "%USERPROFILE%\Miniconda3\condabin\conda.bat" (
        echo Found Conda in user Miniconda3
        set "CONDA_EXE=%USERPROFILE%\Miniconda3\condabin\conda.bat"
        set "CONDA_FOUND=1"
    )
)

if %CONDA_FOUND% EQU 0 (
    if exist "C:\ProgramData\Miniconda3\condabin\conda.bat" (
        echo Found Conda in system Miniconda3
        set "CONDA_EXE=C:\ProgramData\Miniconda3\condabin\conda.bat"
        set "CONDA_FOUND=1"
    )
)

REM Final check
if %CONDA_FOUND% EQU 0 (
    echo ERROR: Conda not found in PATH or common locations!
    echo.
    echo Please either:
    echo   1. Add Conda to your PATH
    echo   2. Install Miniconda from: https://docs.conda.io/en/latest/miniconda.html
    echo   3. If Conda is installed elsewhere, modify this script to include your path
    echo.
    pause
    exit /b 1
)

echo Using Conda: %CONDA_EXE%


REM Create Conda environment if it doesn't exist
echo Checking for PythonProject environment...
"%CONDA_EXE%" env list | findstr "PythonProject" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Creating new Conda environment 'PythonProject' with Python 3.12...
    "%CONDA_EXE%" create -n PythonProject python=3.12 -y
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to create Conda environment
        pause
        exit /b 1
    )
)

REM Activate Conda environment
echo Activating Conda environment...
call "%CONDA_EXE%" activate PythonProject
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to activate Conda environment
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
echo.

REM Install required packages
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Add your custom images to the 'assets' folder
echo 2. Run 'run.bat' to start the application
echo.
pause
