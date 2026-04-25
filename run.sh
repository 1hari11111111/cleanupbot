#!/bin/bash

cd /root/auto_delete_bot

pip install -r requirements.txt

uvicorn bot.main:app --host 0.0.0.0 --port 8080
