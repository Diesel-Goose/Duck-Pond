#!/bin/bash
# Diesel-Goose Heartbeat Runner
# Wrapper script to ensure proper execution

cd /Users/dieselgoose/Honk-Node/Duck-Pond
/opt/homebrew/bin/python3 System/telegram_heartbeat.py >> /Users/dieselgoose/.openclaw/logs/heartbeat.log 2>&1