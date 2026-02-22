#!/usr/bin/env python3
"""
Morning Journal – Daily Recap Generator

Generates a comprehensive, engaging 2-page daily recap every morning at 8 AM.
Saves as PDF in Duck-Pond/Journal/

Includes:
- Previous day's accomplishments
- Goals hit/missed
- System metrics and uptime
- Tasks completed/pending
- New goals for today
- Interesting narrative format

Author: Diesel-Goose AI
Born: February 21, 2026 at 4:20 PM MST, Cheyenne, Wyoming
"""

import json
import subprocess
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import requests

# Configuration
DUCK_POND = Path.home() / "Documents" / "HonkNode" / "Duck-Pond"
JOURNAL_DIR = DUCK_POND / "Journal"
OLLAMA_API = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3"

sys.path.insert(0, str(DUCK_POND / "System"))
from vault_core import get_vault, store

def get_system_metrics():
    """Gather system metrics from the previous day."""
    metrics = {
        "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "day_of_week": (datetime.now() - timedelta(days=1)).strftime("%A"),
        "today": datetime.now().strftime("%Y-%m-%d"),
        "hostname": "Mac Mini M4",
        "location": "Cheyenne, Wyoming"
    }
    
    # Get uptime
    try:
        uptime_result = subprocess.run(['uptime'], capture_output=True, text=True)
        metrics['uptime'] = uptime_result.stdout.strip()
    except:
        metrics['uptime'] = "Unknown"
    
    # Get document count from Duck Pond
    try:
        vault = get_vault()
        all_docs = vault.list_all()
        metrics['total_documents'] = len(all_docs)
        
        # Docs created yesterday
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        yesterday_docs = [d for d in all_docs if yesterday in d.get('created', '')]
        metrics['docs_created_yesterday'] = len(yesterday_docs)
        
        # Recent doc titles
        recent = sorted(all_docs, key=lambda x: x.get('modified', ''), reverse=True)[:5]
        metrics['recent_docs'] = [d['title'] for d in recent]
    except Exception as e:
        metrics['total_documents'] = 0
        metrics['docs_created_yesterday'] = 0
        metrics['recent_docs'] = []
    
    # Git activity
    try:
        # Check Diesel-Goose repo
        repo_path = Path.home() / "Documents" / "HonkNode" / "Hunters" / "Diesel-Goose"
        git_log = subprocess.run(
            ['git', '-C', str(repo_path), 'log', '--since=24 hours ago', '--oneline'],
            capture_output=True, text=True
        )
        metrics['git_commits'] = len(git_log.stdout.strip().split('\n')) if git_log.stdout.strip() else 0
    except:
        metrics['git_commits'] = 0
    
    return metrics

def get_goals_status():
    """Get goals and their status from Duck Pond."""
    try:
        vault = get_vault()
        
        # Search for goal-related documents
        goal_docs = vault.search(keywords=["goal", "objective", "target"], limit=10)
        
        # Search for completed tasks
        completed = vault.search(tags=["completed", "done"], limit=10)
        
        # Search for pending tasks
        pending = vault.search(tags=["pending", "todo", "in-progress"], limit=10)
        
        return {
            "active_goals": len(goal_docs),
            "completed_yesterday": len(completed),
            "pending_tasks": len(pending),
            "goal_docs": [g['title'] for g in goal_docs[:3]],
            "pending_list": [p['title'] for p in pending[:5]]
        }
    except Exception as e:
        return {
            "active_goals": 0,
            "completed_yesterday": 0,
            "pending_tasks": 0,
            "goal_docs": [],
            "pending_list": []
        }

def generate_journal_content(metrics, goals):
    """Generate engaging journal content using Ollama."""
    
    yesterday = metrics['date']
    day_name = metrics['day_of_week']
    today = metrics['today']
    
    # Build prompt for Ollama
    prompt = f"""You are Diesel-Goose AI, executive assistant to the Chairman of Greenhead Labs.
Write a compelling, professional daily journal entry for {yesterday} ({day_name}).

CONTEXT:
- System: {metrics['hostname']} in {metrics['location']}
- Total documents in Duck Pond: {metrics['total_documents']}
- Documents created yesterday: {metrics['docs_created_yesterday']}
- Recent work: {', '.join(metrics['recent_docs'][:3]) if metrics['recent_docs'] else 'Various strategic planning'}
- Git commits in last 24h: {metrics['git_commits']}
- Active goals tracked: {goals['active_goals']}
- Tasks pending: {goals['pending_tasks']}

Write a 2-page daily recap in this format:

# Morning Journal – {yesterday}
## Executive Summary
Brief overview of the day's significance

## Yesterday's Wins
- Major accomplishments
- Goals achieved
- Key decisions made

## System Health & Metrics
- Document storage status
- Code commits and progress
- Infrastructure uptime

## Active Goals Status
{chr(10).join(['- ' + g for g in goals['goal_docs']]) if goals['goal_docs'] else '- Strategic planning in progress'}

## Pending Tasks Requiring Attention
{chr(10).join(['- ' + p for p in goals['pending_list']]) if goals['pending_list'] else '- Review quarterly objectives'}

## Insights & Observations
Analysis of patterns, opportunities, challenges

## Today's Priorities (New Goals)
- Top 3 focus areas for {today}
- Strategic initiatives to advance

## Chairman's Focus Areas
Recommendations for where the Chairman should direct attention today

Make it professional yet engaging. Use emojis sparingly. Write as if reporting to a billionaire founder. Be concise but comprehensive."""

    try:
        response = requests.post(
            OLLAMA_API,
            json={
                "model": DEFAULT_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.8,
                    "num_ctx": 4096
                }
            },
            timeout=120
        )
        
        if response.status_code == 200:
            return response.json().get("response", "Error generating content")
        else:
            return f"Error: Ollama returned {response.status_code}"
    
    except Exception as e:
        return f"Error generating journal: {e}"

def save_as_markdown(content, date_str):
    """Save journal as Markdown file."""
    filename = f"Journal-{date_str}.md"
    filepath = JOURNAL_DIR / filename
    
    # Add metadata header
    header = f"""---
title: Morning Journal – {date_str}
date: {datetime.now().isoformat()}
category: Journal
tags: ["daily", "journal", "recap"]
author: Diesel-Goose AI
source: automated-generation
---

"""
    
    full_content = header + content
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    return filepath, filename

def store_in_vault(filepath, date_str):
    """Store journal in Duck Pond vault."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        doc = store(
            content=content,
            title=f"Morning Journal – {date_str}",
            category="Personal",
            tags=["journal", "daily", "automated"],
            source="morning-journal-cron"
        )
        
        return doc
    except Exception as e:
        print(f"⚠️  Could not store in vault: {e}")
        return None

def send_telegram_notification(date_str, doc_id=None):
    """Send notification that journal is ready."""
    message = f"""🦆📓 Morning Journal Ready – {date_str}

Your daily recap has been generated and saved.

Location: ~/Honk-Node/Duck-Pond/Journal/
Vault ID: {doc_id if doc_id else 'N/A'}

Today's priorities await your review, Chairman.
"""
    
    # For now, just print (Telegram integration can be added)
    print(message)

def main():
    """Main journal generation function."""
    print("🦆 Generating Morning Journal...")
    print("=" * 50)
    
    # Get yesterday's date
    yesterday = datetime.now() - timedelta(days=1)
    date_str = yesterday.strftime("%Y-%m-%d")
    
    print(f"📅 Date: {date_str} ({yesterday.strftime('%A')})")
    print("📊 Gathering metrics...")
    
    # Gather data
    metrics = get_system_metrics()
    goals = get_goals_status()
    
    print(f"   Documents: {metrics['total_documents']}")
    print(f"   New yesterday: {metrics['docs_created_yesterday']}")
    print(f"   Git commits: {metrics['git_commits']}")
    print(f"   Pending tasks: {goals['pending_tasks']}")
    
    print("\n🤖 Generating content with Ollama...")
    content = generate_journal_content(metrics, goals)
    
    if content.startswith("Error"):
        print(f"❌ {content}")
        # Fallback content
        content = f"""# Morning Journal – {date_str}

## Executive Summary
Daily recap for {yesterday.strftime('%A')}, {date_str}.

## System Status
- Documents: {metrics['total_documents']}
- Created yesterday: {metrics['docs_created_yesterday']}
- Git commits: {metrics['git_commits']}

## Pending Tasks
{chr(10).join(['- ' + p for p in goals['pending_list']]) if goals['pending_list'] else '- Review strategic objectives'}

## Note
Ollama was unavailable for enhanced content generation.
"""
    
    print("💾 Saving journal...")
    filepath, filename = save_as_markdown(content, date_str)
    
    print(f"   File: {filename}")
    
    # Store in vault
    print("📚 Storing in Duck Pond vault...")
    doc = store_in_vault(filepath, date_str)
    
    if doc:
        print(f"   Vault ID: {doc['id']}")
    
    # Notification
    print("\n" + "=" * 50)
    send_telegram_notification(date_str, doc['id'] if doc else None)
    
    print(f"\n✅ Morning Journal complete: {filename}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
