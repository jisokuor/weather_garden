@echo off
cd /d G:\Pycharm\Pycharmprojects\Agents

echo Activating virtual environment
call G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\activate.bat

echo Checking Python interpreter
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe --version

echo Checking installed packages
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe -m pip list

echo Installing required packages
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe -m pip install --upgrade pip
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe -m pip install -r requirements.txt

echo Running Python script
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe openweather_api_test7.py

REM Stashing uncommitted changes
echo Stashing uncommitted changes
git add -A
git stash -u

REM Updating gh-pages branch
echo Switching to gh-pages branch
git checkout gh-pages

REM Stashing changes to prevent conflicts
git stash -u

git pull origin gh-pages --rebase

REM Popping stash and resolving conflicts automatically
git stash pop || git stash drop

REM Adding and committing changes if there are any
git add -A

IF ERRORLEVEL 1 (
    echo No changes to commit in gh-pages branch
) ELSE (
    git commit -m "Update from openweather_api_test7.py"
    git push origin gh-pages
)

REM Updating main branch
echo Switching to main branch
git checkout main

REM Stashing changes to prevent conflicts
git stash -u

git pull origin main --rebase

REM Popping stash and resolving conflicts automatically
git stash pop || git stash drop

REM Adding and committing changes if there are any
git add -A

IF ERRORLEVEL 1 (
    echo No changes to commit in main branch
) ELSE (
    git commit -m "Update from openweather_api_test7.py"
    git push origin main
)

echo Cleaning up Git repository
git gc --prune=now

pause

