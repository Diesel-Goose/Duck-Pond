#!/usr/bin/env python3
"""
Duck Pond Fuzzy Finder
Interactive document browser using fzf (if available) or fallback to CLI.

Usage:
  dp-fzf              # Interactive fuzzy search
  dp-fzf --recent     # Show recent docs with preview
  dp-fzf --tags       # Browse by tag

Requires: fzf (brew install fzf)
Fallback: CLI menu if fzf not installed

Author: Diesel-Goose AI
"""

import sys
import subprocess
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from vault_core import get_vault, VAULT_ROOT

def has_fzf():
    """Check if fzf is installed."""
    try:
        subprocess.run(['fzf', '--version'], capture_output=True, check=True)
        return True
    except:
        return False

def list_docs_for_fzf():
    """Generate list for fzf."""
    vault = get_vault()
    docs = vault.list_all()
    
    lines = []
    for doc in sorted(docs, key=lambda x: x['modified'], reverse=True):
        line = f"{doc['title'][:50]:50} │ {doc['category']:12} │ {doc['id'][:8]} │ {','.join(doc.get('tags', []))[:20]}"
        lines.append(line)
    
    return '\n'.join(lines)

def interactive_fzf():
    """Run fzf interactive search."""
    if not has_fzf():
        print("⚠️  fzf not installed. Install with: brew install fzf")
        print("Falling back to CLI menu...")
        return interactive_cli()
    
    docs_list = list_docs_for_fzf()
    
    if not docs_list:
        print("📭 No documents found")
        return
    
    try:
        # Run fzf with preview
        result = subprocess.run(
            ['fzf', '--height', '80%', '--layout', 'reverse', '--border',
             '--header', 'Select document (Enter=open, Ctrl-C=quit)',
             '--preview', f'cat {VAULT_ROOT}/$(python3 -c "import sys; sys.path.insert(0, \"{Path(__file__).parent}\"); from vault_core import get_vault; docs = get_vault().list_all(); print([d for d in docs if d[\\'id\\'][:8] == \"{{8}}\"][0][\\'path\\'])") 2>/dev/null || echo "Preview not available"',
             '--preview-window', 'right:50%:wrap'],
            input=docs_list,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout:
            selected = result.stdout.strip()
            doc_id = selected.split('│')[2].strip()
            
            # Get full document
            vault = get_vault()
            for doc in vault.list_all():
                if doc['id'].startswith(doc_id):
                    open_doc(doc['id'])
                    return
    except Exception as e:
        print(f"❌ Error: {e}")
        interactive_cli()

def interactive_cli():
    """Fallback CLI menu."""
    vault = get_vault()
    docs = sorted(vault.list_all(), key=lambda x: x['modified'], reverse=True)[:20]
    
    if not docs:
        print("📭 No documents found")
        return
    
    print("📄 Recent Documents:\n")
    for i, doc in enumerate(docs, 1):
        print(f"{i:2}. {doc['title'][:45]:45} | {doc['category']}")
    
    print("\nSelect number (or 'q' to quit): ", end='')
    choice = input().strip()
    
    if choice.lower() == 'q':
        return
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(docs):
            open_doc(docs[idx]['id'])
        else:
            print("❌ Invalid selection")
    except ValueError:
        print("❌ Invalid input")

def open_doc(doc_id):
    """Open document in default editor."""
    vault = get_vault()
    doc = vault.retrieve(doc_id)
    
    if not doc:
        print("❌ Document not found")
        return
    
    path = VAULT_ROOT / doc['metadata']['path']
    editor = os.environ.get('EDITOR', 'nano')
    
    print(f"✏️  Opening: {doc['metadata']['title']}")
    subprocess.run([editor, str(path)])

def browse_by_tag():
    """Browse documents by tag."""
    vault = get_vault()
    
    # Get all tags
    tags = set()
    for doc in vault.list_all():
        tags.update(doc.get('tags', []))
    
    if not tags:
        print("📭 No tags found")
        return
    
    print("🏷️  Available Tags:\n")
    tag_list = sorted(tags)
    for i, tag in enumerate(tag_list, 1):
        count = sum(1 for d in vault.list_all() if tag in d.get('tags', []))
        print(f"{i:2}. {tag:20} ({count} docs)")
    
    print("\nSelect tag number (or 'q' to quit): ", end='')
    choice = input().strip()
    
    if choice.lower() == 'q':
        return
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(tag_list):
            selected_tag = tag_list[idx]
            docs = vault.search(tags=[selected_tag])
            
            print(f"\n📄 Documents with tag '{selected_tag}':\n")
            for i, doc in enumerate(docs, 1):
                print(f"{i:2}. {doc['title']}")
            
            print("\nSelect to open (or Enter to go back): ", end='')
            doc_choice = input().strip()
            if doc_choice:
                doc_idx = int(doc_choice) - 1
                if 0 <= doc_idx < len(docs):
                    open_doc(docs[doc_idx]['id'])
    except (ValueError, IndexError):
        print("❌ Invalid selection")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Duck Pond Fuzzy Finder')
    parser.add_argument('--tags', '-t', action='store_true', help='Browse by tag')
    parser.add_argument('--recent', '-r', action='store_true', help='Show recent')
    
    args = parser.parse_args()
    
    if args.tags:
        browse_by_tag()
    else:
        interactive_fzf()

if __name__ == "__main__":
    main()
