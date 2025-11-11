@echo off
echo Starting Gesture Detector...
echo.

REM --- Try to find and use Conda ---
set "CONDA_FOUND=0"

REM Method 1: Check if conda is in PATH
where conda >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Found conda in PATH
    call conda activate PythonProject
    if %ERRORLEVEL% EQU 0 (
        set "CONDA_FOUND=1"
        echo Successfully activated PythonProject environment
    ) else (
        echo Failed to activate PythonProject environment
    )
)

REM Method 2: Try E:\Conda directly (your specific case)
if %CONDA_FOUND% EQU 0 (
    if exist "E:\Conda\condabin\conda.bat" (
        echo Found Conda at E:\Conda
        call "E:\Conda\condabin\conda.bat" activate PythonProject
        if %ERRORLEVEL% EQU 0 (
            set "CONDA_FOUND=1"
            echo Successfully activated PythonProject environment
        ) else (
            echo Failed to activate PythonProject environment from E:\Conda
        )
    )
)

REM Method 3: Try other common locations
if %CONDA_FOUND% EQU 0 (
    if exist "%USERPROFILE%\anaconda3\condabin\conda.bat" (
        echo Found Conda in user Anaconda3
        call "%USERPROFILE%\anaconda3\condabin\conda.bat" activate PythonProject
        if %ERRORLEVEL% EQU 0 set "CONDA_FOUND=1"
    )
)

if %CONDA_FOUND% EQU 0 (
    if exist "%USERPROFILE%\Miniconda3\condabin\conda.bat" (
        echo Found Conda in user Miniconda3
        call "%USERPROFILE%\Miniconda3\condabin\conda.bat" activate PythonProject
        if %ERRORLEVEL% EQU 0 set "CONDA_FOUND=1"
    )
)

REM Final fallback: try to run Python directly
if %CONDA_FOUND% EQU 0 (
    echo WARNING: Could not find or activate Conda environment
    echo Trying to run with current Python interpreter...
    python --version >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: No Python interpreter found
        echo Please either:
        echo   1. Run setup.bat to create the Conda environment
        echo   2. Manually activate a Python environment
        echo   3. Install Python and add it to PATH
        pause
        exit /b 1
    )
)

REM Run the application
python main.py

echo.
echo Application closed.
pause
