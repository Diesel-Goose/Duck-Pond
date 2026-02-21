#!/usr/bin/env python3
"""
Local Vault CLI – Command Line Interface

Simple commands to interact with the Local Vault.

Commands:
  store <title>           Store a new document (interactive)
  search <query>          Search documents
  ask <question>          Ask a question about your documents
  list [category]         List all documents
  show <doc_id>           Show document content
  delete <doc_id>         Archive a document
  stats                   Show vault statistics
  index                   Rebuild search index

Examples:
  python vault_cli.py store "Q1 Financial Report"
  python vault_cli.py search "business plan"
  python vault_cli.py ask "What is our revenue target for Year 3?"
  python vault_cli.py list Business

Author: Diesel-Goose AI
"""

import sys
import json
from pathlib import Path

# Add system path
sys.path.insert(0, str(Path(__file__).parent))

from vault_core import get_vault, store, search, retrieve
from vault_search import VaultSearch

def print_help():
    print("""
🦆 Local Vault CLI – Diesel-Goose Secure Document System

USAGE:
  python vault_cli.py <command> [arguments]

COMMANDS:
  store <title> [--category <cat>] [--tags <tag1,tag2>]
    Store a new document (interactive prompt for content)
    
  search <query> [--category <cat>] [--limit <n>]
    Search for documents
    
  ask <question>
    Ask a question about your documents (uses Ollama)
    
  list [category]
    List all documents, optionally filtered by category
    
  show <doc_id>
    Display full document content
    
  delete <doc_id>
    Archive a document (moves to Archive folder)
    
  stats
    Show vault statistics
    
  index
    Rebuild document index

EXAMPLES:
  python vault_cli.py store "Meeting Notes" --category Business --tags "xrpl,strategy"
  python vault_cli.py search "revenue targets"
  python vault_cli.py ask "What are our goals for Year 1?"
  python vault_cli.py list
  python vault_cli.py show abc123def456

All data stays local on Mac Mini M4. No cloud. Fully secure.
""")

def cmd_store(args):
    """Store a new document."""
    if not args:
        print("❌ Error: Title required")
        print("Usage: python vault_cli.py store 'Document Title'")
        return
    
    title = args[0]
    category = "General"
    tags = []
    
    # Parse optional args
    i = 1
    while i < len(args):
        if args[i] == "--category" and i + 1 < len(args):
            category = args[i + 1]
            i += 2
        elif args[i] == "--tags" and i + 1 < len(args):
            tags = args[i + 1].split(",")
            i += 2
        else:
            i += 1
    
    print(f"📝 Storing document: {title}")
    print(f"   Category: {category}")
    print(f"   Tags: {tags}")
    print()
    print("Enter content (Ctrl+D or type 'END' on new line to finish):")
    print("-" * 50)
    
    lines = []
    try:
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
    except EOFError:
        pass
    
    content = "\n".join(lines)
    
    if not content.strip():
        print("❌ Error: No content provided")
        return
    
    vault = get_vault()
    doc = vault.store(content, title, category=category, tags=tags)
    
    print(f"\n✅ Document stored!")
    print(f"   ID: {doc['id']}")
    print(f"   Path: {doc['path']}")

def cmd_search(args):
    """Search documents."""
    if not args:
        print("❌ Error: Search query required")
        return
    
    query = args[0]
    category = ""
    limit = 10
    
    # Parse optional args
    i = 1
    while i < len(args):
        if args[i] == "--category" and i + 1 < len(args):
            category = args[i + 1]
            i += 2
        elif args[i] == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 2
        else:
            i += 1
    
    vault = get_vault()
    results = vault.search(query, category=category, limit=limit)
    
    print(f"🔍 Search: '{query}'")
    if category:
        print(f"   Category: {category}")
    print()
    
    if not results:
        print("📭 No documents found")
        return
    
    print(f"Found {len(results)} document(s):\n")
    
    for i, doc in enumerate(results, 1):
        print(f"{i}. {doc['title']}")
        print(f"   ID: {doc['id']}")
        print(f"   Category: {doc['category']}")
        print(f"   Tags: {', '.join(doc.get('tags', []))}")
        print(f"   Created: {doc['created'][:10]}")
        print()

def cmd_ask(args):
    """Ask a question."""
    if not args:
        print("❌ Error: Question required")
        return
    
    question = " ".join(args)
    
    print(f"❓ Question: {question}")
    print("🤖 Querying Ollama...\n")
    
    search = VaultSearch()
    answer = search.ask(question)
    
    print(f"💡 Answer:\n{answer}")

def cmd_list(args):
    """List documents."""
    category = args[0] if args else ""
    
    vault = get_vault()
    docs = vault.list_all(category=category)
    
    if category:
        print(f"📁 Documents in category: {category}\n")
    else:
        print(f"📁 All Documents:\n")
    
    if not docs:
        print("📭 No documents found")
        return
    
    # Group by category
    by_category = {}
    for doc in docs:
        cat = doc['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(doc)
    
    for cat, cat_docs in sorted(by_category.items()):
        print(f"\n[{cat}] ({len(cat_docs)} documents)")
        for doc in cat_docs:
            print(f"  • {doc['title']}")
            print(f"    ID: {doc['id']} | Tags: {', '.join(doc.get('tags', []))}")

def cmd_show(args):
    """Show document content."""
    if not args:
        print("❌ Error: Document ID required")
        return
    
    doc_id = args[0]
    vault = get_vault()
    doc = vault.retrieve(doc_id)
    
    if not doc:
        print(f"❌ Document not found: {doc_id}")
        return
    
    print(f"📄 {doc['metadata']['title']}")
    print(f"   Category: {doc['metadata']['category']}")
    print(f"   Created: {doc['metadata']['created']}")
    print("=" * 60)
    print(doc['content'])

def cmd_delete(args):
    """Archive a document."""
    if not args:
        print("❌ Error: Document ID required")
        return
    
    doc_id = args[0]
    vault = get_vault()
    
    # Confirm
    doc = vault.retrieve(doc_id)
    if not doc:
        print(f"❌ Document not found: {doc_id}")
        return
    
    print(f"⚠️  Archive document: {doc['metadata']['title']}?")
    confirm = input("Type 'yes' to confirm: ")
    
    if confirm.lower() == "yes":
        vault.delete(doc_id)
    else:
        print("Cancelled")

def cmd_stats():
    """Show statistics."""
    vault = get_vault()
    stats = vault.stats()
    
    print("🦆 Local Vault Statistics")
    print("=" * 40)
    print(f"Total Documents: {stats['total_documents']}")
    print(f"Last Updated: {stats['last_updated']}")
    print(f"Vault Root: {stats['vault_root']}")
    print()
    print("Categories:")
    for cat, count in sorted(stats['categories'].items()):
        print(f"  {cat}: {count}")

def cmd_index():
    """Rebuild index."""
    print("🔄 Rebuilding document index...")
    vault = get_vault()
    vault._save_index()
    print("✅ Index rebuilt")

def main():
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    args = sys.argv[2:]
    
    commands = {
        "store": cmd_store,
        "search": cmd_search,
        "ask": cmd_ask,
        "list": cmd_list,
        "show": cmd_show,
        "delete": cmd_delete,
        "stats": cmd_stats,
        "index": cmd_index,
        "help": print_help,
    }
    
    if command in commands:
        if command in ["stats", "index", "help"]:
            commands[command]()
        else:
            commands[command](args)
    else:
        print(f"❌ Unknown command: {command}")
        print("Type 'python vault_cli.py help' for usage")

if __name__ == "__main__":
    main()
