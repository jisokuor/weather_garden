@echo off
cd /d G:\Pycharm\Pycharmprojects\Agents

echo Cleaning up old lock files
del .git\index.lock 2>nul

echo Activating virtual environment
call G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\activate.bat

echo Checking Python interpreter
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe --version

echo Checking installed packages
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe -m pip list

echo Upgrading pip, setuptools, and wheel
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel


echo Running Python script
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe openweather_api_test7.py

REM Stashing uncommitted changes
echo Stashing uncommitted changes
git add -A
git stash -u

REM Updating main branch
echo Pulling latest changes from main branch
git checkout main
git pull origin main --rebase

REM Popping stash and resolving conflicts automatically
git stash pop || git stash drop

REM Adding and committing changes if there are any
git add -A

IF %ERRORLEVEL% NEQ 0 (
    echo No changes to commit in main branch
) ELSE (
    git commit -m "Update from openweather_api_test7.py"
    git push origin main
)

echo Cleaning up Git repository
git gc --prune=now

pause
