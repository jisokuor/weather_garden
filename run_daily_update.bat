@echo off
cd /d G:\Pycharm\Pycharmprojects\Agents

echo Activating virtual environment
call G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\activate.bat

echo Checking Python interpreter
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe --version

echo Checking installed packages
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe -m pip list

python.exe -m pip install --upgrade pip

echo Running Python script
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe openweather_api_test7.py

REM Updating gh-pages branch
echo Switching to gh-pages branch
git checkout gh-pages
git pull origin gh-pages --rebase
git add -A
git commit -m "Update from openweather_api_test7.py"
git push origin gh-pages

REM Updating main branch
echo Switching to main branch
git checkout main
git pull origin main --rebase
git add -A
git commit -m "Update from openweather_api_test7.py"
git push origin main

echo Cleaning up Git repository
git gc --prune=now

pause
