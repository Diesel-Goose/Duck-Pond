#!/usr/bin/env python3
"""
Email Alert System for Chairman
Proactively checks for new emails and sends Telegram alerts

Run via cron every 5 minutes:
*/5 * * * * cd ~/Honk-Node/Duck-Pond && python3 System/email_alerter.py
"""

import subprocess
import sys
from pathlib import Path

# Add Duck-Pond to path
sys.path.insert(0, str(Path.home() / "Documents" / "HonkNode" / "Duck-Pond" / "System"))

def check_and_alert():
    """Check for new emails and alert if found"""
    try:
        # Run email monitor in check mode
        result = subprocess.run(
            ["python3", "System/email_monitor.py", "--check"],
            cwd=Path.home() / "Documents" / "HonkNode" / "Duck-Pond",
            capture_output=True,
            text=True
        )
        
        output = result.stdout + result.stderr
        
        # Check if new emails found
        if "NEW_EMAILS_FOUND" in output:
            # Extract subjects
            subjects = []
            for line in output.split('\n'):
                if line.startswith("SUBJECT:"):
                    subjects.append(line.replace("SUBJECT:", "").strip())
            
            if subjects:
                # Build alert message
                if len(subjects) == 1:
                    alert_msg = f"📧 New email from Chairman:\n• {subjects[0]}"
                else:
                    alert_msg = f"📧 {len(subjects)} new emails from Chairman:"
                    for s in subjects:
                        alert_msg += f"\n• {s}"
                
                alert_msg += "\n\nReply 'read email' to view."
                
                # Print for Telegram bot to pick up
                print(f"🚨 EMAIL_ALERT")
                print(alert_msg)
                
                # Also write to alert file for external monitoring
                alert_file = Path.home() / "Documents" / "HonkNode" / "Duck-Pond" / ".vault" / "email_alert.txt"
                with open(alert_file, 'w') as f:
                    f.write(alert_msg)
                
                return True
        
        return False
        
    except Exception as e:
        print(f"Error in email alerter: {e}")
        return False

if __name__ == "__main__":
    found = check_and_alert()
    sys.exit(0 if found else 0)  # Always exit 0 for cron
