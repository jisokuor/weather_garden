@echo off
cd /d G:\Pycharm\Pycharmprojects\Agents

REM Activate the virtual environment
call G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\activate.bat

REM Run the Python script
python openweather_api_test7.py

REM Deactivate the virtual environment
call deactivate

REM Commit and push changes to the Git repository
git pull origin main --allow-unrelated-histories
git add -A
git commit -m "Daily weather and gardening tips update"
git push origin main

REM Clean up Git repository
git gc --prune=now
