#!/usr/bin/env python3
"""
Email Monitor for Chairman Inbox
Checks dieselgoose.ai@gmail.com for emails from nathan@greenhead.io
Can READ full content and SEND replies

Born: February 21, 2026 at 4:20 PM MST in Cheyenne, Wyoming
"""

import imaplib
import email
import smtplib
import os
import json
import sys
from datetime import datetime
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ACCOUNT = "dieselgoose.ai@gmail.com"
SENDER_FILTER = "nathan@greenhead.io"
CHAIRMAN_EMAIL = "nathan@greenhead.io"

# Use credentials from Duck-Pond secure storage (primary) or OpenClaw (fallback)
DUCK_POND_CREDS = Path.home() / "Documents" / "HonkNode" / "Duck-Pond" / ".credentials" / "credentials.json"
OPENCLAW_CREDS = Path.home() / ".openclaw" / "credentials" / "gmail-app-password.json"
STATE_FILE = Path.home() / "Documents" / "HonkNode" / "Duck-Pond" / ".vault" / "email_state.json"
EMAIL_LOG = Path.home() / "Documents" / "HonkNode" / "Duck-Pond" / ".vault" / "email_log.json"

def load_credentials():
    """Load email credentials from secure storage (Duck-Pond primary, OpenClaw fallback)"""
    # Try Duck-Pond first
    if DUCK_POND_CREDS.exists():
        try:
            with open(DUCK_POND_CREDS, 'r') as f:
                data = json.load(f)
                gmail = data.get("credentials", {}).get("gmail", {})
                password = gmail.get("app_password", "")
                if password:
                    return password.replace(" ", "")
        except:
            pass
    
    # Fallback to OpenClaw
    if OPENCLAW_CREDS.exists():
        try:
            with open(OPENCLAW_CREDS, 'r') as f:
                creds = json.load(f)
                return creds.get("app_password", "").replace(" ", "")
        except:
            pass
    
    # Final fallback to env var
    return os.environ.get("DG_EMAIL_PASSWORD", "")

def load_state():
    """Load last checked UID from state file"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"last_uid": 0, "last_check": None, "read_emails": []}
    return {"last_uid": 0, "last_check": None, "read_emails": []}

def save_state(state):
    """Save state to file"""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state["last_check"] = datetime.now().isoformat()
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def log_email(email_data):
    """Log email to history"""
    EMAIL_LOG.parent.mkdir(parents=True, exist_ok=True)
    logs = []
    if EMAIL_LOG.exists():
        try:
            with open(EMAIL_LOG, 'r') as f:
                logs = json.load(f)
        except:
            logs = []
    
    logs.append({
        "timestamp": datetime.now().isoformat(),
        **email_data
    })
    
    with open(EMAIL_LOG, 'w') as f:
        json.dump(logs[-100:], f, indent=2)  # Keep last 100

def get_email_body(msg):
    """Extract email body text"""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                try:
                    body = part.get_payload(decode=True).decode('utf-8')
                    break
                except:
                    pass
            elif content_type == "text/html" and not body:
                try:
                    body = part.get_payload(decode=True).decode('utf-8')
                except:
                    pass
    else:
        try:
            body = msg.get_payload(decode=True).decode('utf-8')
        except:
            body = str(msg.get_payload())
    
    return body[:5000] if len(body) > 5000 else body  # Limit size

def check_emails():
    """Check for new emails from specified sender"""
    print(f"🦆 Checking {EMAIL_ACCOUNT} for emails from {SENDER_FILTER}...")
    
    EMAIL_PASSWORD = load_credentials()
    
    if not EMAIL_PASSWORD:
        print("⚠️  Email password not configured")
        print(f"   Set DG_EMAIL_PASSWORD env var or create credentials file")
        return []
    
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select('inbox')
        
        # Search for emails from sender
        status, messages = mail.search(None, f'FROM "{SENDER_FILTER}"')
        
        if status != 'OK' or not messages[0]:
            print("📭 No new emails")
            mail.logout()
            return []
        
        email_ids = messages[0].split()
        state = load_state()
        last_uid = state.get("last_uid", 0)
        new_emails = []
        
        for e_id in email_ids:
            uid = int(e_id)
            if uid > last_uid:
                status, msg_data = mail.fetch(e_id, '(RFC822)')
                if status == 'OK':
                    raw_email = msg_data[0][1]
                    email_message = email.message_from_bytes(raw_email)
                    
                    subject = email_message['Subject']
                    from_addr = email_message['From']
                    date = email_message['Date']
                    message_id = email_message['Message-ID']
                    body = get_email_body(email_message)
                    
                    new_emails.append({
                        'uid': uid,
                        'subject': subject,
                        'from': from_addr,
                        'date': date,
                        'message_id': message_id,
                        'body': body
                    })
                    
                    if uid > last_uid:
                        last_uid = uid
        
        mail.logout()
        
        # Save updated state
        state["last_uid"] = last_uid
        save_state(state)
        
        if new_emails:
            print(f"📬 Found {len(new_emails)} new email(s) from Chairman:")
            for e in new_emails:
                print(f"   📧 {e['subject']}")
        else:
            print("📭 No new emails from Chairman")
        
        return new_emails
        
    except Exception as e:
        print(f"❌ Error checking emails: {e}")
        return []

def read_latest_email():
    """Read the most recent email content"""
    EMAIL_PASSWORD = load_credentials()
    
    if not EMAIL_PASSWORD:
        print("⚠️  Email password not configured")
        return None
    
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select('inbox')
        
        # Search for emails from sender
        status, messages = mail.search(None, f'FROM "{SENDER_FILTER}"')
        
        if status != 'OK' or not messages[0]:
            print("📭 No emails found")
            mail.logout()
            return None
        
        email_ids = messages[0].split()
        latest_id = email_ids[-1]  # Get most recent
        
        status, msg_data = mail.fetch(latest_id, '(RFC822)')
        if status == 'OK':
            raw_email = msg_data[0][1]
            email_message = email.message_from_bytes(raw_email)
            
            result = {
                'uid': int(latest_id),
                'subject': email_message['Subject'],
                'from': email_message['From'],
                'date': email_message['Date'],
                'message_id': email_message['Message-ID'],
                'body': get_email_body(email_message)
            }
            
            mail.logout()
            return result
        
        mail.logout()
        return None
        
    except Exception as e:
        print(f"❌ Error reading email: {e}")
        return None

def send_reply(subject, body, reply_to_id=None):
    """Send email reply to Chairman"""
    EMAIL_PASSWORD = load_credentials()
    
    if not EMAIL_PASSWORD:
        print("⚠️  Email password not configured")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ACCOUNT
        msg['To'] = CHAIRMAN_EMAIL
        
        # Add Re: if replying
        if subject.startswith("Re:"):
            msg['Subject'] = subject
        else:
            msg['Subject'] = f"Re: {subject}"
        
        if reply_to_id:
            msg['In-Reply-To'] = reply_to_id
            msg['References'] = reply_to_id
        
        # Add signature (Chairman format)
        signature = """

Diesel Goose
Chairman | Greenhead Labs LLC
www.Greenhead.io | dieselgoose.ai@gmail.com | Wyoming, USA
HonkNode Operations Center"""
        
        full_body = body + signature
        
        msg.attach(MIMEText(full_body, 'plain'))
        
        # Send
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        # Log sent email
        log_email({
            "type": "sent",
            "to": CHAIRMAN_EMAIL,
            "subject": msg['Subject'],
            "body_preview": body[:200]
        })
        
        print(f"✅ Reply sent to {CHAIRMAN_EMAIL}")
        print(f"   Subject: {msg['Subject']}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

def list_recent_emails(count=5):
    """List recent email subjects"""
    EMAIL_PASSWORD = load_credentials()
    
    if not EMAIL_PASSWORD:
        print("⚠️  Email password not configured")
        return []
    
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        mail.select('inbox')
        
        status, messages = mail.search(None, f'FROM "{SENDER_FILTER}"')
        
        if status != 'OK' or not messages[0]:
            print("📭 No emails found")
            mail.logout()
            return []
        
        email_ids = messages[0].split()[-count:]  # Last N emails
        emails = []
        
        for e_id in email_ids:
            status, msg_data = mail.fetch(e_id, '(RFC822)')
            if status == 'OK':
                raw_email = msg_data[0][1]
                email_message = email.message_from_bytes(raw_email)
                emails.append({
                    'uid': int(e_id),
                    'subject': email_message['Subject'],
                    'date': email_message['Date'][:20]  # Truncate
                })
        
        mail.logout()
        return emails
        
    except Exception as e:
        print(f"❌ Error listing emails: {e}")
        return []

def main():
    """Main entry point with CLI args"""
    if len(sys.argv) < 2:
        # Default: check for new emails
        new_emails = check_emails()
        if new_emails:
            print("\n🔔 NEW_EMAILS_FOUND")
            for e in new_emails:
                print(f"SUBJECT:{e['subject']}")
        return
    
    command = sys.argv[1]
    
    if command == "--check":
        new_emails = check_emails()
        if new_emails:
            print("\n🔔 NEW_EMAILS_FOUND")
            for e in new_emails:
                print(f"SUBJECT:{e['subject']}")
    
    elif command == "--read":
        email_data = read_latest_email()
        if email_data:
            print(f"\n📧 FROM: {email_data['from']}")
            print(f"📅 DATE: {email_data['date']}")
            print(f"📝 SUBJECT: {email_data['subject']}")
            print(f"\n{'='*50}")
            print(email_data['body'])
            print(f"{'='*50}\n")
            
            # Save to state as read
            state = load_state()
            if "read_emails" not in state:
                state["read_emails"] = []
            state["read_emails"].append({
                "uid": email_data['uid'],
                "subject": email_data['subject'],
                "read_at": datetime.now().isoformat()
            })
            save_state(state)
            
            # Output for automation
            print(f"EMAIL_UID:{email_data['uid']}")
            print(f"EMAIL_SUBJECT:{email_data['subject']}")
            print(f"EMAIL_BODY:{email_data['body'][:500]}")  # First 500 chars
    
    elif command == "--reply" and len(sys.argv) >= 4:
        subject = sys.argv[2]
        body = sys.argv[3]
        reply_to = sys.argv[4] if len(sys.argv) > 4 else None
        send_reply(subject, body, reply_to)
    
    elif command == "--list":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        emails = list_recent_emails(count)
        print(f"\n📬 Last {len(emails)} emails:")
        for e in reversed(emails):
            print(f"  [{e['uid']}] {e['date']} | {e['subject']}")
    
    elif command == "--send":
        # Interactive send
        subject = input("Subject: ")
        print("Body (Ctrl+D when done):")
        body = sys.stdin.read()
        if subject and body:
            send_reply(subject, body)
    
    else:
        print("Usage:")
        print("  python3 email_monitor.py              # Check new emails")
        print("  python3 email_monitor.py --check      # Check new emails")
        print("  python3 email_monitor.py --read       # Read latest email")
        print("  python3 email_monitor.py --list [N]   # List recent emails")
        print("  python3 email_monitor.py --send       # Send email interactively")
        print("  python3 email_monitor.py --reply <subject> <body> [reply_to_id]")

if __name__ == "__main__":
    main()
