@echo off
cd /d G:\Pycharm\Pycharmprojects\Agents
G:\Pycharm\Pycharmprojects\Agents\Scripts\python.exe openweather_api_test7.py

git pull origin main --allow-unrelated-histories
git add -f index.html forecast.mp3 gardening_tips.mp3 output.md
git commit -m "Daily weather and gardening tips update"
git push origin main
