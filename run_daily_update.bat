@echo off
cd /d G:\Pycharm\Pycharmprojects\Agents

echo Activating virtual environment
call G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\activate.bat

echo Checking Python interpreter
where python

echo Checking installed packages
python -m pip list

echo Running Python script
python openweather_api_test7.py

REM Deactivating virtual environment (optional)
REM call deactivate.bat

echo Pulling latest changes and pushing updates
git pull origin main --allow-unrelated-histories
git add -A
git commit -m "Daily weather and gardening tips update"
git push origin main

echo Cleaning up Git repository
git gc --prune=now

pause
