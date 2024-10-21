cd /rero/iot_bot

. ./venv/bin/activate

export PATH=$PATH:/rero/iot_bot/app/controller

uvicorn app.main:app --host 0.0.0.0 --port 8082