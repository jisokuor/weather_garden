# Change to the project directory
Set-Location -Path "G:\Pycharm\Pycharmprojects\Agents"

# Activate the virtual environment
& .\venv\Scripts\Activate.ps1

# Run the Python script
python .\openweather_api_test7.py

# Deactivate the virtual environment
deactivate

# Pull the latest changes, add, commit, and push the updates
git pull origin main --allow-unrelated-histories
git add -A
git commit -m "Daily weather and gardening tips update"
git push origin main

# Clean up Git repository
git gc --prune=now
