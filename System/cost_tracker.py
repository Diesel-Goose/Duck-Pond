#!/usr/bin/env python3
"""
Duck Pond Cost Tracker

Tracks all LLM API usage and enforces daily budget.
Saves money by preventing runaway API costs.

Usage:
  python cost_tracker.py status     # Show today's spending
  python cost_tracker.py check      # Check if budget available
  python cost_tracker.py log <service> <cost> <task>  # Log a call
  python cost_tracker.py reset      # Reset today's counter (emergency)

Author: Diesel-Goose AI
Born: Feb 21, 2026 at 4:20 PM, Cheyenne WY
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Configuration
DUCK_POND = Path.home() / "Documents" / "HonkNode" / "Duck-Pond"
COST_LOG = DUCK_POND / ".vault" / "cost_log.json"

# Budget limits
DAILY_BUDGET = 2.00    # $2/day maximum
WEEKLY_BUDGET = 10.00  # $10/week maximum
MONTHLY_BUDGET = 50.00 # $50/month maximum

def ensure_log():
    """Ensure cost log file exists."""
    COST_LOG.parent.mkdir(parents=True, exist_ok=True)
    if not COST_LOG.exists():
        with open(COST_LOG, 'w') as f:
            json.dump({}, f)

def load_log():
    """Load cost log."""
    ensure_log()
    with open(COST_LOG) as f:
        return json.load(f)

def save_log(data):
    """Save cost log."""
    with open(COST_LOG, 'w') as f:
        json.dump(data, f, indent=2)

def get_today():
    """Get today's date string."""
    return datetime.now().strftime("%Y-%m-%d")

def get_week():
    """Get current week string."""
    return datetime.now().strftime("%Y-W%W")

def get_month():
    """Get current month string."""
    return datetime.now().strftime("%Y-%m")

def log_api_call(service, cost, task):
    """Log an API call with cost."""
    data = load_log()
    today = get_today()
    
    if today not in data:
        data[today] = {
            "calls": [],
            "total": 0.0,
            "budget": DAILY_BUDGET
        }
    
    call = {
        "time": datetime.now().isoformat(),
        "service": service,
        "cost": round(cost, 4),
        "task": task[:100]  # Truncate long tasks
    }
    
    data[today]["calls"].append(call)
    data[today]["total"] = round(data[today]["total"] + cost, 4)
    
    save_log(data)
    return data[today]["total"]

def get_spending(period="today"):
    """Get spending for a period."""
    data = load_log()
    
    if period == "today":
        key = get_today()
        return data.get(key, {}).get("total", 0.0)
    
    elif period == "week":
        # Sum all days in current week
        current_week = get_week()
        total = 0.0
        for date, info in data.items():
            try:
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                week_key = date_obj.strftime("%Y-W%W")
                if week_key == current_week:
                    total += info.get("total", 0.0)
            except:
                pass
        return round(total, 2)
    
    elif period == "month":
        # Sum all days in current month
        current_month = get_month()
        total = 0.0
        for date, info in data.items():
            try:
                date_obj = datetime.strptime(date, "%Y-%m-%d")
                month_key = date_obj.strftime("%Y-%m")
                if month_key == current_month:
                    total += info.get("total", 0.0)
            except:
                pass
        return round(total, 2)
    
    return 0.0

def check_budget():
    """Check if we have budget remaining."""
    daily_spent = get_spending("today")
    weekly_spent = get_spending("week")
    monthly_spent = get_spending("month")
    
    daily_remaining = DAILY_BUDGET - daily_spent
    weekly_remaining = WEEKLY_BUDGET - weekly_spent
    monthly_remaining = MONTHLY_BUDGET - monthly_spent
    
    # Check all limits
    if daily_remaining <= 0:
        print(f"🚨 DAILY BUDGET EXCEEDED: ${daily_spent:.2f} / ${DAILY_BUDGET:.2f}")
        return False, 0.0
    
    if weekly_remaining <= 0:
        print(f"🚨 WEEKLY BUDGET EXCEEDED: ${weekly_spent:.2f} / ${WEEKLY_BUDGET:.2f}")
        return False, 0.0
    
    if monthly_remaining <= 0:
        print(f"🚨 MONTHLY BUDGET EXCEEDED: ${monthly_spent:.2f} / ${MONTHLY_BUDGET:.2f}")
        return False, 0.0
    
    return True, min(daily_remaining, weekly_remaining, monthly_remaining)

def show_status():
    """Show current spending status."""
    data = load_log()
    today = get_today()
    
    daily_spent = get_spending("today")
    weekly_spent = get_spending("week")
    monthly_spent = get_spending("month")
    
    print("💰 DUCK POND COST STATUS")
    print("=" * 50)
    print(f"📅 Today ({today}):")
    print(f"   Spent: ${daily_spent:.2f} / ${DAILY_BUDGET:.2f}")
    print(f"   Remaining: ${DAILY_BUDGET - daily_spent:.2f}")
    print(f"   Status: {'🟢 OK' if daily_spent < DAILY_BUDGET else '🔴 EXCEEDED'}")
    print()
    print(f"📊 This Week:")
    print(f"   Spent: ${weekly_spent:.2f} / ${WEEKLY_BUDGET:.2f}")
    print(f"   Remaining: ${WEEKLY_BUDGET - weekly_spent:.2f}")
    print()
    print(f"📈 This Month:")
    print(f"   Spent: ${monthly_spent:.2f} / ${MONTHLY_BUDGET:.2f}")
    print(f"   Remaining: ${MONTHLY_BUDGET - monthly_spent:.2f}")
    print()
    
    # Show today's calls
    if today in data and data[today].get("calls"):
        print("📝 Today's API Calls:")
        for call in data[today]["calls"][-5:]:  # Last 5
            print(f"   ${call['cost']:.4f} | {call['service'][:15]:15} | {call['task'][:40]}...")
    else:
        print("📝 No API calls today")
    
    print()
    print("💡 Tips to save money:")
    print("   • Use Ollama (local) instead of cloud APIs")
    print("   • Batch multiple requests into one")
    print("   • Cache common responses")
    print("   • Use smaller models when possible")

def reset_today():
    """Reset today's counter (emergency only)."""
    data = load_log()
    today = get_today()
    
    if today in data:
        old_total = data[today].get("total", 0.0)
        data[today] = {"calls": [], "total": 0.0, "budget": DAILY_BUDGET}
        save_log(data)
        print(f"🔄 Reset today's counter (was ${old_total:.2f})")
    else:
        print("📭 No spending to reset today")

def main():
    if len(sys.argv) < 2:
        show_status()
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        show_status()
    
    elif command == "check":
        ok, remaining = check_budget()
        if ok:
            print(f"✅ Budget available: ${remaining:.2f}")
        else:
            print("❌ Budget exceeded - use Ollama only")
        sys.exit(0 if ok else 1)
    
    elif command == "log":
        if len(sys.argv) < 5:
            print("Usage: cost_tracker.py log <service> <cost> <task>")
            return
        service = sys.argv[2]
        cost = float(sys.argv[3])
        task = sys.argv[4]
        total = log_api_call(service, cost, task)
        print(f"✅ Logged: ${cost:.4f} | Total today: ${total:.2f}")
    
    elif command == "reset":
        confirm = input("Reset today's spending counter? Type 'yes': ")
        if confirm.lower() == "yes":
            reset_today()
        else:
            print("Cancelled")
    
    else:
        print(f"Unknown command: {command}")
        print("Usage: cost_tracker.py [status|check|log|reset]")

if __name__ == "__main__":
    main()
