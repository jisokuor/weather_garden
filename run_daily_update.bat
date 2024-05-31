@echo off
cd /d G:\Pycharm\Pycharmprojects\Agents

echo Activating virtual environment
call G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\activate.bat

echo Running Python script: openweather_api_test7.py
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe openweather_api_test7.py

echo Running Python script: weatherforecast.py
G:\Pycharm\Pycharmprojects\Agents\.venv\Scripts\python.exe weatherforecast.py

echo Deactivating virtual environment
deactivate
