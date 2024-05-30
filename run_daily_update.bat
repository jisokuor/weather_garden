@echo off
cd /d G:\Pycharm\Pycharmprojects\Agents

REM Activate the virtual environment
call G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\activate.bat

REM Run the Python script
python openweather_api_test7.py

REM Deactivate the virtual environment (optional, if deactivate.bat exists)
call deactivate.bat

REM Pull the latest changes, add, commit, and push the updates
git pull origin main --allow-unrelated-histories
git add -A
git commit -m "Daily weather and gardening tips update"
git push origin main

REM Clean up Git repository
git gc --prune=now
