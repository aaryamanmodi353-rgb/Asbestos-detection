
pip install fastapi uvicorn python-multipart python-jose ultralytics opencv-python numpy

echo.
echo Checking for existing processes on port 8000 to prevent conflicts...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do taskkill /f /pid %%a >nul 2>&1

echo Starting FastAPI server...
python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
pause
