#!/usr/bin/env python3
"""
Diesel-Goose Telegram Heartbeat
Sends automated status updates every 5-15 minutes
"""

import requests
import json
import sys
from datetime import datetime
from pathlib import Path

# Configuration
BOT_TOKEN = "8476304097:AAFOPOzPlJ7uG8rWjAQuJsL8adfj1c7kMO8"
CHAT_ID = "7491205261"  # Nathan's Telegram

def get_system_status():
    """Get current system status"""
    try:
        # Read latest from HEARTBEAT.md (workspace repo with full history)
        heartbeat_file = Path.home() / ".openclaw" / "workspace" / "HEARTBEAT.md"
        
        health = 100
        budget = 96
        mission = 99
        status = "🔥 MAX"
        active = "2050 mode AI-first operations"
        
        if heartbeat_file.exists():
            with open(heartbeat_file, 'r') as f:
                content = f.read()
                # Parse latest entry
                if "⚡️" in content:
                    # Extract values from latest log entry
                    lines = content.split('\n')
                    for line in lines[-20:]:  # Check last 20 lines
                        if '⚡️' in line and '|' in line:
                            # Parse: "⚡️ 100% | 💰 96% | 💡 99% | 🔥 MAX"
                            parts = line.split('|')
                            if len(parts) >= 4:
                                health = parts[0].split('⚡️')[1].strip().replace('%', '')
                                budget = parts[1].split('💰')[1].strip().replace('%', '')
                                mission = parts[2].split('💡')[1].strip().replace('%', '')
                                status = parts[3].strip()
                        if '🎯 Active:' in line:
                            active_full = line.split('🎯 Active:')[1].strip()
                            # Strip the " — Telegram auto-heartbeat" suffix to prevent duplication
                            if ' — Telegram auto-heartbeat' in active_full:
                                active = active_full.split(' — Telegram auto-heartbeat')[0].strip()
                            else:
                                active = active_full
                            break
        
        return {
            "health": health,
            "budget": budget,
            "mission": mission,
            "status": status,
            "active": active
        }
    except Exception as e:
        return {
            "health": 100,
            "budget": 96,
            "mission": 99,
            "status": "🔥 MAX",
            "active": "2050 mode AI-first operations"
        }

def send_heartbeat():
    """Send heartbeat to Telegram"""
    status = get_system_status()
    
    # Format message
    message = f"""🦆 DIESELGOOSE | Founder — Greenhead Labs
⚡️ {status['health']}% | 💰 {status['budget']}% | 💡 {status['mission']}% | {status['status']}
🎯 Active: {status['active']}

📅 {datetime.now().strftime('%H:%M CST')} • Auto-Heartbeat"""
    
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ Heartbeat sent: {datetime.now().strftime('%H:%M:%S')}")
            return True
        else:
            print(f"❌ Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def log_to_heartbeat():
    """Also log to HEARTBEAT.md"""
    try:
        # Write to workspace repo (Diesel-Goose) which has full history
        heartbeat_file = Path.home() / ".openclaw" / "workspace" / "HEARTBEAT.md"
        status = get_system_status()
        
        entry = f"""
📅 {datetime.now().strftime('%Y-%m-%d')} • 🕐 {datetime.now().strftime('%H:%M')} CST • v10.4  
⚡️ {status['health']}% | 💰 {status['budget']}% | 💡 {status['mission']}% | {status['status']}
🎯 Active: {status['active']} — Telegram auto-heartbeat
"""
        
        with open(heartbeat_file, 'a') as f:
            f.write(entry)
        
        print("✅ Logged to HEARTBEAT.md")
    except Exception as e:
        print(f"❌ Log error: {e}")

if __name__ == "__main__":
    if send_heartbeat():
        log_to_heartbeat()
        sys.exit(0)
    else:
        sys.exit(1)
