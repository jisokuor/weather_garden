@echo off
cd /d G:\Pycharm\Pycharmprojects\Agents

echo Activating virtual environment
call G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\activate.bat

echo Running Python script
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe openweather_api_test7.py

