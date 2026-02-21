#!/bin/zsh
# Duck Pond Quick Access - Add to ~/.zshrc
# Source this file: echo 'source ~/Documents/HonkNode/Duck-Pond/System/duck-pond.sh' >> ~/.zshrc

# Configuration
DUCK_POND_ROOT="$HOME/Documents/HonkNode/Duck-Pond"
DUCK_SYSTEM="$DUCK_POND_ROOT/System"

# Main shortcut function
dp() {
    case "$1" in
        store|s)
            shift
            python3 "$DUCK_SYSTEM/vault_cli.py" store "$@"
            ;;
        search|find|f)
            shift
            python3 "$DUCK_SYSTEM/vault_cli.py" search "$@"
            ;;
        ask|a)
            shift
            python3 "$DUCK_SYSTEM/vault_cli.py" ask "$@"
            ;;
        list|ls|l)
            shift
            python3 "$DUCK_SYSTEM/vault_cli.py" list "$@"
            ;;
        show|cat|c)
            shift
            python3 "$DUCK_SYSTEM/vault_cli.py" show "$@"
            ;;
        stats)
            python3 "$DUCK_SYSTEM/vault_cli.py" stats
            ;;
        quick|q)
            # Quick note - capture immediately
            shift
            _dp_quick "$@"
            ;;
        today|journal|j)
            # Daily journal entry
            _dp_journal
            ;;
        recent|r)
            # Show recent documents
            _dp_recent
            ;;
        edit|e)
            # Edit document by ID or search
            shift
            _dp_edit "$@"
            ;;
        tags)
            # List all tags
            _dp_tags
            ;;
        open|o)
            # Open Duck Pond in Finder
            open "$DUCK_POND_ROOT"
            ;;
        help|h|--help|-h)
            _dp_help
            ;;
        *)
            # Default: search
            if [ -z "$1" ]; then
                _dp_help
            else
                python3 "$DUCK_SYSTEM/vault_cli.py" search "$@"
            fi
            ;;
    esac
}

# Quick note capture
dp-quick() { _dp_quick "$@"; }
_dp_quick() {
    local title="${1:-Quick Note $(date +%H:%M)}"
    local category="${2:-Personal}"
    
    echo "📝 Quick Note: $title"
    echo "   Category: $category"
    echo "   Type your note (Ctrl+D to save):"
    echo "   ─────────────────────────────────"
    
    python3 "$DUCK_SYSTEM/vault_cli.py" store "$title" --category "$category"
}

# Daily journal
dp-journal() { _dp_journal; }
_dp_journal() {
    local date_str=$(date +%Y-%m-%d)
    local title="Journal Entry - $date_str"
    local filepath="$DUCK_POND_ROOT/Knowledge-Base/Personal/journal-$date_str.md"
    
    if [ -f "$filepath" ]; then
        echo "📓 Opening existing journal entry..."
        ${EDITOR:-nano} "$filepath"
    else
        echo "# Journal Entry - $date_str" > "$filepath"
        echo "" >> "$filepath"
        echo "## Morning" >> "$filepath"
        echo "" >> "$filepath"
        echo "## Afternoon" >> "$filepath"
        echo "" >> "$filepath"
        echo "## Evening" >> "$filepath"
        echo "" >> "$filepath"
        echo "## Notes" >> "$filepath"
        echo "" >> "$filepath"
        
        # Add to vault index
        python3 -c "
import sys
sys.path.insert(0, '$DUCK_SYSTEM')
from vault_core import store
with open('$filepath', 'r') as f:
    content = f.read()
store(content, '$title', category='Personal', tags=['journal', 'daily'])
" 2>/dev/null
        
        echo "📓 Created new journal entry"
        ${EDITOR:-nano} "$filepath"
    fi
}

# Recent documents
dp-recent() { _dp_recent; }
_dp_recent() {
    echo "📄 Recent Documents (last 10):"
    echo ""
    
    python3 -c "
import sys
sys.path.insert(0, '$DUCK_SYSTEM')
from vault_core import get_vault
vault = get_vault()
docs = sorted(vault.list_all(), key=lambda x: x['modified'], reverse=True)[:10]
for i, doc in enumerate(docs, 1):
    print(f\"{i:2}. {doc['title'][:40]:40} | {doc['id'][:8]}... | {doc['category']}\")
" 2>/dev/null
}

# Edit document
dp-edit() { _dp_edit "$@"; }
_dp_edit() {
    local query="$1"
    
    if [ -z "$query" ]; then
        echo "Usage: dp edit <search-term>"
        return 1
    fi
    
    # Find document
    local result=$(python3 -c "
import sys
sys.path.insert(0, '$DUCK_SYSTEM')
from vault_core import get_vault
vault = get_vault()
docs = vault.search('$query', limit=1)
if docs:
    print(docs[0]['id'])
" 2>/dev/null)
    
    if [ -n "$result" ]; then
        local doc_path="$DUCK_POND_ROOT/$(python3 -c "
import sys
sys.path.insert(0, '$DUCK_SYSTEM')
from vault_core import get_vault
vault = get_vault()
doc = vault.retrieve('$result')
if doc:
    print(doc['metadata']['path'])
" 2>/dev/null)"
        
        if [ -f "$DUCK_POND_ROOT/$doc_path" ]; then
            echo "✏️  Editing: $result"
            ${EDITOR:-nano} "$DUCK_POND_ROOT/$doc_path"
            
            # Update modification time in index
            python3 -c "
import sys
sys.path.insert(0, '$DUCK_SYSTEM')
from vault_core import get_vault
from datetime import datetime
vault = get_vault()
for doc in vault.index['documents']:
    if doc['id'] == '$result':
        doc['modified'] = datetime.now().isoformat()
vault._save_index()
" 2>/dev/null
        fi
    else
        echo "❌ No document found matching: $query"
    fi
}

# List all tags
dp-tags() { _dp_tags; }
_dp_tags() {
    echo "🏷️  All Tags:"
    python3 -c "
import sys
sys.path.insert(0, '$DUCK_SYSTEM')
from vault_core import get_vault
vault = get_vault()
tags = set()
for doc in vault.list_all():
    tags.update(doc.get('tags', []))
for tag in sorted(tags):
    count = sum(1 for d in vault.list_all() if tag in d.get('tags', []))
    print(f\"  {tag:20} ({count} docs)\")
" 2>/dev/null
}

# Help
dp-help() { _dp_help; }
_dp_help() {
    cat << 'EOF'
🦆 Duck Pond Quick Commands

USAGE: dp <command> [arguments]

COMMANDS:
  store, s <title>          Store new document
  search, f <query>         Search documents  
  ask, a <question>         Ask AI about your docs
  list, l [category]        List documents
  show, c <id>              Show document content
  quick, q [title]          Quick note capture
  today, j                  Daily journal entry
  recent, r                 Show recent documents
  edit, e <search>          Edit document
  tags                      List all tags
  stats                     Show statistics
  open, o                   Open in Finder
  help                      Show this help

SHORTCUTS:
  dp <search-term>          Same as: dp search <term>
  dp-quick "Note text"      Quick save
  dp-journal                Open today's journal
  dp-recent                 Show last 10 docs

EXAMPLES:
  dp s "Meeting Notes" --category Business
  dp f "revenue targets"
  dp a "What are our goals?"
  dp quick "Idea: AI for compliance"
  dp today
  dp edit "business plan"
  dp tags

All data stays local. No cloud. Quack protocol active.
EOF
}

# Auto-complete for zsh
if [ -n "$ZSH_VERSION" ]; then
    _dp_completion() {
        local -a commands=(store search ask list show quick today recent edit tags stats open help)
        _describe 'command' commands
    }
    compdef _dp_completion dp
fi

echo "🦆 Duck Pond shortcuts loaded. Type 'dp' to start."
