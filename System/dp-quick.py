#!/usr/bin/env python3
"""
Duck Pond Quick Capture
Ultra-fast note storage without interactive prompts.

Usage:
  dp-quick "Your note text here" [--category Business] [--tags "tag1,tag2"]
  dp-quick --clipboard           # Store clipboard content
  dp-quick --file notes.txt      # Store file content
  echo "Note" | dp-quick          # Pipe input

Author: Diesel-Goose AI
"""

import sys
import argparse
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from vault_core import store

def get_clipboard():
    """Get clipboard content on macOS."""
    try:
        result = subprocess.run(['pbpaste'], capture_output=True, text=True)
        return result.stdout
    except:
        return None

def main():
    parser = argparse.ArgumentParser(description='Quick note capture for Duck Pond')
    parser.add_argument('content', nargs='?', help='Note content')
    parser.add_argument('--category', '-c', default='Quick', help='Category')
    parser.add_argument('--tags', '-t', default='', help='Tags (comma-separated)')
    parser.add_argument('--title', default=None, help='Custom title')
    parser.add_argument('--clipboard', action='store_true', help='Use clipboard content')
    parser.add_argument('--file', '-f', help='Read from file')
    parser.add_argument('--stdin', '-s', action='store_true', help='Read from stdin')
    
    args = parser.parse_args()
    
    # Get content from various sources
    content = None
    
    if args.clipboard:
        content = get_clipboard()
        if not content:
            print("❌ Clipboard is empty")
            sys.exit(1)
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            sys.exit(1)
    elif args.stdin or not sys.stdin.isatty():
        content = sys.stdin.read()
    elif args.content:
        content = args.content
    else:
        # Interactive mode - ask for content
        print("📝 Enter your note (Ctrl+D to finish):")
        content = sys.stdin.read()
    
    if not content or not content.strip():
        print("❌ Content is empty")
        sys.exit(1)
    
    # Generate title
    if args.title:
        title = args.title
    else:
        # Use first line or first 50 chars
        first_line = content.split('\n')[0].strip()
        if len(first_line) > 50:
            title = first_line[:47] + "..."
        else:
            title = first_line or f"Quick Note {datetime.now().strftime('%H:%M')}"
    
    # Parse tags
    tags = [t.strip() for t in args.tags.split(',') if t.strip()]
    
    # Store
    try:
        from datetime import datetime
        doc = store(
            content=content,
            title=title,
            category=args.category,
            tags=tags,
            source="quick-capture"
        )
        print(f"✅ Stored: {title}")
        print(f"   ID: {doc['id']}")
        print(f"   Category: {args.category}")
        if tags:
            print(f"   Tags: {', '.join(tags)}")
    except Exception as e:
        print(f"❌ Error storing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    from datetime import datetime
    main()
