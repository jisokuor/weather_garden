@echo off
cd /d G:\Pycharm\Pycharmprojects\Agents

echo Activating virtual environment
call G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\activate.bat

echo Checking Python interpreter
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe --version

echo Checking installed packages
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe -m pip list

echo Switching to main branch
git checkout main

echo Running Python script
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe openweather_api_test7.py

REM Pulling latest changes from gh-pages
git pull origin gh-pages --rebase

REM Adding and committing changes
git add -A
git commit -m "Daily weather and gardening tips update"

REM Pushing changes to gh-pages
git push origin gh-pages

echo Cleaning up Git repository
git gc --prune=now

pause
