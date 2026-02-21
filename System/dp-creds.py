#!/usr/bin/env python3
"""
Duck Pond Credential Manager

Secure storage for API keys, passwords, and tokens.
All data stays local in Duck-Pond/.credentials/ (never synced to cloud/GitHub)

Usage:
  dp-creds add <service> <key> <value>    # Add/update credential
  dp-creds get <service> <key>            # Get credential value
  dp-creds list                           # List all services
  dp-creds show <service>                 # Show service details (masked)
  dp-creds delete <service>               # Remove service

Author: Diesel-Goose AI
Born: Feb 21, 2026 at 4:20 PM, Cheyenne, Wyoming
"""

import json
import os
import sys
import getpass
from pathlib import Path
from datetime import datetime

# Configuration
DUCK_POND = Path.home() / "Documents" / "HonkNode" / "Duck-Pond"
CREDENTIALS_DIR = DUCK_POND / ".credentials"
CREDENTIALS_FILE = CREDENTIALS_DIR / "credentials.json"

def ensure_credentials_dir():
    """Ensure credentials directory exists with proper permissions."""
    CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
    # Set permissions to 700 (owner only)
    os.chmod(CREDENTIALS_DIR, 0o700)

def load_credentials():
    """Load credentials from secure storage."""
    if CREDENTIALS_FILE.exists():
        try:
            with open(CREDENTIALS_FILE, 'r') as f:
                return json.load(f)
        except:
            return {"version": "1.0", "credentials": {}}
    return {"version": "1.0", "credentials": {}}

def save_credentials(data):
    """Save credentials with secure permissions."""
    ensure_credentials_dir()
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    # Set file permissions to 600 (owner read/write only)
    os.chmod(CREDENTIALS_FILE, 0o600)

def mask_value(value, visible=4):
    """Mask sensitive value showing only last N characters."""
    if not value:
        return ""
    if len(value) <= visible:
        return "*" * len(value)
    return "*" * (len(value) - visible) + value[-visible:]

def add_credential(service, key, value):
    """Add or update a credential."""
    data = load_credentials()
    
    if service not in data["credentials"]:
        data["credentials"][service] = {}
    
    data["credentials"][service][key] = value
    data["credentials"][service]["last_updated"] = datetime.now().isoformat()
    
    save_credentials(data)
    print(f"✅ Added: {service}.{key}")

def get_credential(service, key):
    """Get a credential value."""
    data = load_credentials()
    
    if service in data["credentials"] and key in data["credentials"][service]:
        return data["credentials"][service][key]
    return None

def list_services():
    """List all credential services."""
    data = load_credentials()
    
    if not data["credentials"]:
        print("📭 No credentials stored")
        return
    
    print("🔐 Stored Credential Services:\n")
    for service, creds in sorted(data["credentials"].items()):
        last_updated = creds.get("last_updated", "Unknown")
        key_count = len([k for k in creds.keys() if k != "last_updated"])
        print(f"  {service:20} ({key_count} keys) - Updated: {last_updated[:10]}")

def show_service(service):
    """Show service credentials (masked)."""
    data = load_credentials()
    
    if service not in data["credentials"]:
        print(f"❌ Service not found: {service}")
        return
    
    creds = data["credentials"][service]
    print(f"\n🔐 {service}:\n")
    
    for key, value in sorted(creds.items()):
        if key == "last_updated":
            continue
        if isinstance(value, str) and len(value) > 8:
            display = mask_value(value)
        else:
            display = value
        print(f"  {key:20}: {display}")
    
    if "last_updated" in creds:
        print(f"\n  Last updated: {creds['last_updated']}")

def delete_service(service):
    """Delete a service and all its credentials."""
    data = load_credentials()
    
    if service not in data["credentials"]:
        print(f"❌ Service not found: {service}")
        return
    
    confirm = input(f"Delete all credentials for '{service}'? Type 'yes' to confirm: ")
    if confirm.lower() == "yes":
        del data["credentials"][service]
        save_credentials(data)
        print(f"🗑️  Deleted: {service}")
    else:
        print("Cancelled")

def import_from_openclaw():
    """Import credentials from OpenClaw storage."""
    openclaw_creds = Path.home() / ".openclaw" / "credentials" / "gmail-app-password.json"
    
    if openclaw_creds.exists():
        try:
            with open(openclaw_creds, 'r') as f:
                gmail_creds = json.load(f)
            
            data = load_credentials()
            data["credentials"]["gmail"] = {
                "service": "Gmail IMAP",
                "email": gmail_creds.get("email", ""),
                "app_password": gmail_creds.get("app_password", ""),
                "imap_server": gmail_creds.get("imap_server", "imap.gmail.com"),
                "imap_port": gmail_creds.get("imap_port", 993),
                "type": "app_password",
                "last_updated": datetime.now().isoformat(),
                "notes": "Imported from OpenClaw storage"
            }
            save_credentials(data)
            print("✅ Imported Gmail credentials from OpenClaw")
            return True
        except Exception as e:
            print(f"⚠️  Could not import: {e}")
    return False

def main():
    if len(sys.argv) < 2:
        print("🔐 Duck Pond Credential Manager")
        print("\nUsage:")
        print("  dp-creds add <service> <key> <value>    # Add credential")
        print("  dp-creds get <service> <key>            # Get credential")
        print("  dp-creds list                           # List all services")
        print("  dp-creds show <service>                 # Show service (masked)")
        print("  dp-creds delete <service>               # Delete service")
        print("  dp-creds import                         # Import from OpenClaw")
        print("\nExamples:")
        print("  dp-creds add google client_id abc123")
        print("  dp-creds get gmail app_password")
        print("  dp-creds show gmail")
        return
    
    command = sys.argv[1].lower()
    
    if command == "add":
        if len(sys.argv) < 5:
            # Interactive mode
            service = input("Service name: ")
            key = input("Key name: ")
            value = getpass.getpass("Value (hidden): ")
        else:
            service = sys.argv[2]
            key = sys.argv[3]
            value = sys.argv[4]
        add_credential(service, key, value)
    
    elif command == "get":
        if len(sys.argv) < 4:
            print("❌ Usage: dp-creds get <service> <key>")
            return
        service = sys.argv[2]
        key = sys.argv[3]
        value = get_credential(service, key)
        if value:
            print(value)
        else:
            print(f"❌ Not found: {service}.{key}")
            sys.exit(1)
    
    elif command == "list":
        list_services()
    
    elif command == "show":
        if len(sys.argv) < 3:
            print("❌ Usage: dp-creds show <service>")
            return
        show_service(sys.argv[2])
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("❌ Usage: dp-creds delete <service>")
            return
        delete_service(sys.argv[2])
    
    elif command == "import":
        if import_from_openclaw():
            print("\n✅ Import complete")
        else:
            print("\n📭 No OpenClaw credentials found to import")
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Use: add, get, list, show, delete, import")

if __name__ == "__main__":
    main()
