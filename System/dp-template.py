#!/usr/bin/env python3
"""
Duck Pond Templates
Create documents from templates for consistency.

Usage:
  dp-template meeting            # Create meeting notes
  dp-template journal            # Create journal entry
  dp-template project            # Create project doc
  dp-template idea               # Create idea doc
  dp-template list               # Show available templates

Author: Diesel-Goose AI
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from vault_core import store, VAULT_ROOT

TEMPLATES = {
    "meeting": {
        "title": "Meeting - {date}",
        "category": "Business",
        "tags": ["meeting", "notes"],
        "content": """# Meeting - {date}

## Attendees
- 

## Agenda
1. 
2. 
3. 

## Notes

## Action Items
- [ ] 
- [ ] 

## Decisions

## Next Steps

"""
    },
    
    "journal": {
        "title": "Journal Entry - {date}",
        "category": "Personal",
        "tags": ["journal", "daily"],
        "content": """# Journal Entry - {date}

## Morning

## Afternoon

## Evening

## Thoughts

## Gratitude

## Tomorrow

"""
    },
    
    "project": {
        "title": "Project - ",
        "category": "Project",
        "tags": ["project", "planning"],
        "content": """# Project: {title}

## Overview

## Goals
- 

## Timeline
- Start: 
- Milestones:
  - 
- Target Completion: 

## Resources
- 

## Risks
- 

## Success Criteria
- 

## Notes

"""
    },
    
    "idea": {
        "title": "Idea: ",
        "category": "Business",
        "tags": ["idea", "brainstorm"],
        "content": """# Idea: {title}

## Problem

## Solution

## Market

## Revenue Model

## Resources Needed
- 

## Next Steps
- [ ] 

## Related Ideas
- 

"""
    },
    
    "decision": {
        "title": "Decision - {date}",
        "category": "Business",
        "tags": ["decision", "strategy"],
        "content": """# Decision Record - {date}

## Context

## Options Considered
1. 
2. 
3. 

## Decision

## Rationale

## Trade-offs

## Implementation

## Review Date

"""
    },
    
    "research": {
        "title": "Research - ",
        "category": "Technical",
        "tags": ["research", "notes"],
        "content": """# Research: {title}

## Topic

## Sources
- 

## Key Findings

## Insights

## Implications

## Related
- 

## Questions Remaining
- 

"""
    },
    
    "weekly": {
        "title": "Weekly Review - Week {week}",
        "category": "Personal",
        "tags": ["weekly", "review"],
        "content": """# Weekly Review - Week {week}, {date}

## Wins This Week
- 

## Challenges
- 

## Key Metrics
- 

## Lessons Learned

## Next Week Priorities
1. 
2. 
3. 

## Reflection

"""
    }
}

def list_templates():
    """Show available templates."""
    print("📝 Available Templates:\n")
    for name, template in TEMPLATES.items():
        print(f"  {name:12} - {template['category']}")
        print(f"               Tags: {', '.join(template['tags'])}")
        print()
    print("Usage: dp-template <template-name> [custom-title]")

def create_from_template(template_name, custom_title=None):
    """Create document from template."""
    if template_name not in TEMPLATES:
        print(f"❌ Unknown template: {template_name}")
        print(f"Available: {', '.join(TEMPLATES.keys())}")
        return
    
    template = TEMPLATES[template_name]
    
    # Format placeholders
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    week_str = now.strftime("%U")
    
    # Get title
    if custom_title:
        title = custom_title
    else:
        title = template["title"].format(date=date_str, week=week_str, title="")
    
    # If title ends with placeholder, ask for input
    if title.endswith(" - ") or title.endswith(": "):
        print(f"Enter {template_name} title: ", end='')
        user_title = input().strip()
        if user_title:
            title = title + user_title
    
    # Format content
    content = template["content"].format(date=date_str, week=week_str, title=title)
    
    # Store
    try:
        doc = store(
            content=content,
            title=title,
            category=template["category"],
            tags=template["tags"],
            source=f"template:{template_name}"
        )
        print(f"✅ Created from template: {title}")
        print(f"   ID: {doc['id']}")
        print(f"   Category: {template['category']}")
        
        # Open in editor if EDITOR is set
        import os
        editor = os.environ.get('EDITOR')
        if editor:
            doc_data = store.__self__ if hasattr(store, '__self__') else None
            if doc_data:
                vault = store.__self__ if hasattr(store, '__self__') else get_vault()
                retrieved = vault.retrieve(doc['id'])
                if retrieved:
                    path = VAULT_ROOT / retrieved['metadata']['path']
                    print(f"✏️  Opening in {editor}...")
                    import subprocess
                    subprocess.run([editor, str(path)])
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Duck Pond Templates')
    parser.add_argument('template', nargs='?', help='Template name')
    parser.add_argument('title', nargs='?', help='Custom title')
    parser.add_argument('--list', '-l', action='store_true', help='List templates')
    
    args = parser.parse_args()
    
    if args.list or not args.template:
        list_templates()
    else:
        create_from_template(args.template, args.title)

if __name__ == "__main__":
    main()
