# 🦆 Local Vault – Quick Reference Card

## Store Something
```bash
cd ~/Documents/local\ Vault/System
python vault_cli.py store "My Document Title"
# Type content, then Ctrl+D (or type END)
```

## Find Something
```bash
# Search by keyword
python vault_cli.py search "revenue"

# Search with category
python vault_cli.py search "xrpl" --category Business

# Ask AI about your documents
python vault_cli.py ask "What are our Year 3 goals?"
```

## See Everything
```bash
# List all documents
python vault_cli.py list

# List by category
python vault_cli.py list Business

# Show vault stats
python vault_cli.py stats
```

## Read a Document
```bash
# Show full content
python vault_cli.py show <doc_id>

# Example
python vault_cli.py show abc123def4567890
```

## Python Quick Use
```python
from vault_core import store, search

# Store
store("My notes", "Notes Title", category="Business")

# Search
results = search("xrpl strategy")
for doc in results:
    print(doc['title'])
```

## Folder Locations
- **Documents:** `~/Documents/Duck-Pond/Knowledge-Base/`
- **Index:** `~/Documents/Duck-Pond/.vault/index.json`
- **System:** `~/Documents/Duck-Pond/System/`

## Remember
✅ All data stays on Mac Mini  
✅ Uses local Ollama (no API costs)  
✅ Markdown format (human readable)  
✅ Encrypted at rest (FileVault)  

🦆 **Local. Secure. Sovereign.**
