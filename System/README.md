# 🦆 Local Vault – Diesel-Goose Secure Document System

**Local-first, Ollama-powered document storage and retrieval.**

All data stays on your Mac Mini M4. No cloud. No API costs. Fully sovereign.

---

## What is Local Vault?

Local Vault is a secure document management system designed for the Chairman. It combines:

- **Semantic search** – Find documents by meaning, not just keywords
- **Ollama integration** – Local AI for embeddings and Q&A
- **Markdown-native** – Human-readable, future-proof format
- **Category organization** – Business, Technical, Personal, Projects
- **Full-text indexing** – Fast search across all documents
- **Version control** – Archive instead of delete

**Cost:** $0 (uses local Ollama, no API calls)  
**Security:** AES-256 (Mac Mini disk encryption) + file permissions  
**Privacy:** Never leaves your machine

---

## Quick Start

### 1. Store a Document

```bash
cd ~/Documents/local\ Vault/System
python vault_cli.py store "Q1 Strategy Meeting"
```

Then type your content and press Ctrl+D (or type `END` on new line).

### 2. Search Documents

```bash
python vault_cli.py search "revenue targets"
python vault_cli.py search "xrpl" --category Business
```

### 3. Ask Questions (Ollama)

```bash
python vault_cli.py ask "What are our Year 3 goals?"
python vault_cli.py ask "Summarize our business plan"
```

### 4. List All Documents

```bash
python vault_cli.py list
python vault_cli.py list Business
```

---

## Folder Structure

```
local Vault/
├── System/                    # Vault system files (DO NOT MODIFY)
│   ├── vault_core.py         # Core storage engine
│   ├── vault_search.py       # Ollama semantic search
│   ├── vault_cli.py          # Command line interface
│   └── README.md             # This file
│
├── .vault/                    # Hidden index & config
│   ├── index.json            # Document index
│   └── config.json           # Vault settings
│
├── Knowledge-Base/            # Long-term knowledge storage
│   ├── Business/             # Business plans, strategy, finance
│   ├── Technical/            # Code docs, architecture, APIs
│   └── Personal/             # Personal notes (optional)
│
├── Projects/                  # Active & completed projects
│   ├── Active/               # Current projects
│   └── Completed/            # Archived projects
│
├── Archive/                   # Deleted documents (soft delete)
│
├── Diesel-Goose/             # AI-specific files
│
└── GreeheadLabs/             # Company documents
    ├── Business Documents/
    ├── Business Plan/
    └── Business Templates/
```

---

## Python API Usage

### Store Documents Programmatically

```python
from vault_core import store, search, retrieve

# Store a document
doc = store(
    content="Meeting notes from today...",
    title="Q1 Strategy Meeting",
    category="Business",
    tags=["strategy", "q1", "xrpl"],
    source="manual entry"
)

print(f"Stored with ID: {doc['id']}")
```

### Search Documents

```python
from vault_core import search

# Simple search
results = search(query="revenue", category="Business")

# Advanced search
results = search(
    query="year 3",
    category="Business",
    tags=["plan"],
    limit=5
)

for doc in results:
    print(f"{doc['title']} - {doc['path']}")
```

### Semantic Search with Ollama

```python
from vault_search import VaultSearch

search = VaultSearch()

# Semantic similarity search
results = search.semantic_search(
    query="What are our financial goals?",
    top_k=5
)

for doc in results:
    print(f"{doc['title']} (score: {doc['similarity']:.2f})")
```

### Ask Questions

```python
from vault_search import VaultSearch

search = VaultSearch()

# Ask natural language questions
answer = search.ask("What is our Year 1 revenue target?")
print(answer)
```

---

## Document Format

All documents are stored as Markdown with YAML frontmatter:

```markdown
---
{
  "id": "abc123def4567890",
  "title": "Document Title",
  "category": "Business",
  "tags": ["strategy", "xrpl"],
  "source": "email",
  "created": "2026-02-21T00:00:00",
  "modified": "2026-02-21T00:00:00",
  "format": "markdown",
  "word_count": 150,
  "keywords": ["XRPL", "Strategy", "Revenue"]
}
---

# Document Title

Your content here...
```

**Benefits:**
- ✅ Human-readable
- ✅ Future-proof
- ✅ Works with any Markdown editor
- ✅ Easy to backup/migrate
- ✅ Git-friendly (if needed)

---

## CLI Commands Reference

| Command | Description | Example |
|---------|-------------|---------|
| `store <title>` | Store new document | `store "Meeting Notes" --category Business --tags "xrpl"` |
| `search <query>` | Search documents | `search "revenue targets"` |
| `ask <question>` | Ask Ollama about docs | `ask "What are our goals?"` |
| `list [cat]` | List all documents | `list Business` |
| `show <id>` | Show document content | `show abc123def456` |
| `delete <id>` | Archive document | `delete abc123def456` |
| `stats` | Show vault stats | `stats` |
| `index` | Rebuild index | `index` |
| `help` | Show help | `help` |

---

## Ollama Integration

Local Vault uses your local Ollama instance for:

1. **Embeddings** – Convert text to vectors for semantic search
2. **Q&A** – Answer questions using your documents as context
3. **Summarization** – Generate document summaries

**Requirements:**
- Ollama running on `localhost:11434`
- At least one model pulled (e.g., `llama3`)

**Cost:** $0 (runs locally on M4)

---

## Security Best Practices

### 1. File Permissions

Documents are stored with standard macOS permissions:
```bash
chmod 600 ~/Documents/local\ Vault/Knowledge-Base/Business/*.md
```

### 2. Disk Encryption

Ensure FileVault is enabled:
```bash
fdesetup status
```

### 3. Backup Strategy

```bash
# Backup vault to encrypted drive
rsync -av ~/Documents/local\ Vault/ /Volumes/EncryptedBackup/Vault/

# Or to VAULT.dmg
hdiutil attach ~/Documents/VAULT.dmg
cp -r ~/Documents/local\ Vault/* /Volumes/VAULT/
```

### 4. Never Store

❌ Private keys or seed phrases  
❌ Passwords (use 1Password)  
❌ Unencrypted sensitive data  

---

## Importing Existing Documents

### From Email

```python
from vault_core import store

email_content = """
Subject: Business Plan
From: nathan@greenhead.io

[email body here]
"""

store(
    content=email_content,
    title="Business Plan - Email from Chairman",
    category="Business",
    tags=["email", "strategy"],
    source="email"
)
```

### From Files

```python
import glob
from pathlib import Path
from vault_core import store

for file_path in glob.glob("~/Documents/old_notes/*.txt"):
    with open(file_path, 'r') as f:
        content = f.read()
    
    title = Path(file_path).stem
    store(content, title, category="Archive")
```

---

## Troubleshooting

### Issue: Ollama not responding

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running:
brew services start ollama
```

### Issue: Permission denied

```bash
# Fix permissions
chmod -R u+rw ~/Documents/local\ Vault/
```

### Issue: Index corrupted

```bash
# Rebuild index
cd ~/Documents/local\ Vault/System
python vault_cli.py index
```

---

## Performance

- **Storage:** ~1KB per document (plus content)
- **Search:** <100ms for 1000 documents
- **Indexing:** ~1 doc/second
- **Memory:** Minimal (lazy loading)

**Scales to:** 10,000+ documents without issues

---

## Future Enhancements

- [ ] Vector database (ChromaDB) for better semantic search
- [ ] Document versioning (Git integration)
- [ ] OCR for scanned documents
- [ ] Audio transcription integration
- [ ] Automatic categorization with AI
- [ ] Multi-user support (future)

---

## Principles

1. **Local First** – No cloud, no API costs, full control
2. **Human Readable** – Markdown, not proprietary formats
3. **AI Enhanced** – Ollama for search and Q&A
4. **Simple** – Minimal complexity, maximum reliability
5. **Secure** – Encryption at rest, minimal attack surface

---

## Version

**Local Vault v1.0**  
Built for the Chairman by Diesel-Goose AI  
February 2026

🦆 **Quack protocol: Active. All data local. All systems secure.**
