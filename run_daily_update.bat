REM @echo off
cd /d G:\Pycharm\Pycharmprojects\Agents

echo Activating virtual environment
call G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\activate.bat

echo Checking Python interpreter
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe --version

echo Checking installed packages
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe -m pip list

python.exe -m pip install --upgrade pip

echo Switching to gh-pages  branch
git checkout gh-pages

echo Running Python script
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe openweather_api_test7.py

REM Pulling latest changes from main
git pull origin gh-pages --rebase

REM Adding and committing changes
git add -A
git commit -m "Daily weather and gardening tips update"

REM Pushing changes to main
git push origin gh-pages

echo Cleaning up Git repository
git gc --prune=now

pause
