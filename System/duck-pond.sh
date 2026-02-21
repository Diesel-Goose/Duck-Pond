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
        creds|c)
            # Credential management
            shift
            python3 "$DUCK_SYSTEM/dp-creds.py" "$@"
            ;;
        cost)
            # Cost tracking
            shift
            python3 "$DUCK_SYSTEM/cost_tracker.py" "$@"
            ;;
        xaman|x)
            # Xaman (XUMM) XRPL wallet operations
            shift
            _dp_xaman "$@"
            ;;
        flare|f)
            # Flare Network operations
            shift
            _dp_flare "$@"
            ;;
        mercury|m)
            # Mercury Bank operations
            shift
            _dp_mercury "$@"
            ;;
        brave|search|bs)
            # Brave Search - web search
            shift
            _dp_brave "$@"
            ;;
        tokens|t)
            # Token optimization info
            _dp_tokens_info
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

# Token optimization info
dp-tokens() { _dp_tokens_info; }
_dp_tokens_info() {
    cat << 'EOF'
💾 Token Optimization Guide

CONTEXT LIMIT: 123K tokens

QUICK TIPS:
  1. Use Ollama (local) for routine tasks - FREE, no token limit
  2. Store large docs in Duck Pond, reference by path
  3. /new or /reset when context gets full
  4. Summarize before sending to API

COMMANDS:
  dp cost status            Check API spending
  dp tokens                 Show this guide
  /new or /reset            Clear context (start fresh)

COST SAVINGS:
  • Ollama (local): $0.00 per call
  • Cloud API: $0.002-0.06 per 1K tokens
  • Target: $0-2/day (down from $20/day)

For full guide: open ~/Documents/HonkNode/Duck-Pond/TOKEN_OPTIMIZATION.md
EOF
}

# Xaman (XUMM) wallet operations
dp-xaman() { _dp_xaman "$@"; }
_dp_xaman() {
    case "$1" in
        ping|p)
            echo "🔗 Testing Xaman API connection..."
            python3 "$DUCK_SYSTEM/xaman_client.py" ping
            ;;
        rates|r)
            local currency="${2:-XRP}"
            echo "💰 Getting $currency rates..."
            python3 "$DUCK_SYSTEM/xaman_client.py" rates "$currency"
            ;;
        assets|a)
            echo "📊 Listing curated assets..."
            python3 "$DUCK_SYSTEM/xaman_client.py" assets
            ;;
        status|s)
            if [ -z "$2" ]; then
                echo "❌ Usage: dp xaman status <payload_uuid>"
                return 1
            fi
            echo "📋 Checking payload status..."
            python3 "$DUCK_SYSTEM/xaman_client.py" status "$2"
            ;;
        pay|payment)
            echo "💸 Creating payment request..."
            _dp_xaman_payment "$2" "$3" "$4"
            ;;
        help|h|--help|-h|*)
            cat << 'EOF'
🔗 Xaman (XUMM) Wallet Commands

USAGE: dp xaman <command> [args]

COMMANDS:
  ping, p                   Test API connection
  rates, r [XRP]            Get exchange rates
  assets, a                 List curated assets
  status, s <uuid>          Check payload status
  pay <dest> <amt> [cur]    Create payment request
  help                      Show this help

EXAMPLES:
  dp xaman ping
  dp xaman rates USD
  dp xaman assets
  dp xaman status abc-123-uuid
  dp xaman pay rN7n... 100 XRP

NOTES:
  - Requires Xaman mobile app for signing
  - API credentials stored in .credentials/
  - All transactions require manual approval
  - Test on XRPL Testnet first

For detailed docs: open ~/Documents/HonkNode/Duck-Pond/Knowledge-Base/Technical/XRPL-XRP-Reference.md
EOF
            ;;
    esac
}

# Create payment request helper
_dp_xaman_payment() {
    local destination="$1"
    local amount="$2"
    local currency="${3:-XRP}"
    
    if [ -z "$destination" ] || [ -z "$amount" ]; then
        echo "❌ Usage: dp xaman pay <destination> <amount> [currency]"
        echo "   Example: dp xaman pay rN7n7ot... 100 XRP"
        return 1
    fi
    
    echo "🦆 Creating payment request..."
    echo "   To: $destination"
    echo "   Amount: $amount $currency"
    echo ""
    
    python3 << PYEOF
import sys
sys.path.insert(0, '$DUCK_SYSTEM')
from xaman_client import XamanClient, payment_template
import json

client = XamanClient()
tx = payment_template("$destination", "$amount", "$currency")
result = client.create_sign_request(tx)

if 'error' in result:
    print(f"❌ Error: {result['error']}")
else:
    print("✅ Payment request created!")
    print(f"   UUID: {result.get('uuid', 'N/A')}")
    print(f"   QR URL: {result.get('refs', {}).get('qr_png', 'N/A')}")
    print(f"   Status: {result.get('pushed', False) and 'Pushed to app' or 'Check app manually'}")
    print("")
    print("Next steps:")
    print("1. Scan QR code with Xaman app")
    print("2. Approve transaction on mobile")
    print(f"3. Check status: dp xaman status {result.get('uuid', 'uuid-here')}")
PYEOF
}

# Flare Network operations
dp-flare() { _dp_flare "$@"; }
_dp_flare() {
    case "$1" in
        ping|p)
            echo "🔗 Testing Flare Network connection..."
            python3 "$DUCK_SYSTEM/flare_client.py" ping
            ;;
        block|b)
            echo "⛓️  Getting latest block..."
            python3 "$DUCK_SYSTEM/flare_client.py" block
            ;;
        balance|bal)
            if [ -z "$2" ]; then
                echo "❌ Usage: dp flare balance <address>"
                return 1
            fi
            echo "💰 Checking FLR balance..."
            python3 "$DUCK_SYSTEM/flare_client.py" balance "$2"
            ;;
        gas|g)
            echo "⛽ Getting gas price..."
            python3 "$DUCK_SYSTEM/flare_client.py" gas
            ;;
        chain|c)
            echo "🔗 Getting chain info..."
            python3 "$DUCK_SYSTEM/flare_client.py" chain
            ;;
        fts|price)
            if [ -z "$2" ]; then
                echo "❌ Usage: dp flare fts <SYMBOL>"
                echo "   Example: dp flare fts XRP"
                return 1
            fi
            echo "📊 Getting FTSO price for $2..."
            python3 "$DUCK_SYSTEM/flare_client.py" fts price "$2"
            ;;
        help|h|--help|-h|*)
            cat << 'EOF'
🔥 Flare Network Commands

USAGE: dp flare <command> [args]

COMMANDS:
  ping, p                   Test connection to Flare
  block, b                  Get latest block number
  balance, bal <address>    Get FLR balance
  gas, g                    Get current gas price
  chain, c                  Get chain ID info
  fts, price <SYMBOL>       Get FTSO oracle price
  help                      Show this help

EXAMPLES:
  dp flare ping
  dp flare block
  dp flare balance 0x1234...
  dp flare gas
  dp flare fts XRP
  dp flare fts BTC

NETWORKS:
  - Mainnet (chain_id: 14) - Default
  - Coston2 (chain_id: 114) - Testnet

FEATURES:
  - EVM compatible (MetaMask works)
  - FTSO price feeds (XRP, BTC, ETH, etc.)
  - F-Assets (FXRP, etc.) - coming soon
  - State Connector - cross-chain verification

For detailed docs: open ~/Documents/HonkNode/Duck-Pond/Knowledge-Base/Technical/Flare-Network-Reference.md
EOF
            ;;
    esac
}

# Mercury Bank operations
dp-mercury() { _dp_mercury "$@"; }
_dp_mercury() {
    case "$1" in
        ping|p)
            echo "🏦 Testing Mercury Bank connection..."
            python3 "$DUCK_SYSTEM/mercury_client.py" ping
            ;;
        accounts|a)
            echo "💳 Listing Mercury accounts..."
            python3 "$DUCK_SYSTEM/mercury_client.py" accounts
            ;;
        balance|bal)
            if [ -z "$2" ]; then
                echo "❌ Usage: dp mercury balance <account_id>"
                return 1
            fi
            echo "💰 Getting account balance..."
            python3 "$DUCK_SYSTEM/mercury_client.py" balance "$2"
            ;;
        transactions|tx)
            if [ -z "$2" ]; then
                echo "❌ Usage: dp mercury transactions <account_id> [limit]"
                return 1
            fi
            local limit="${3:-100}"
            echo "📊 Getting transactions (limit: $limit)..."
            python3 "$DUCK_SYSTEM/mercury_client.py" transactions "$2" "$limit"
            ;;
        report|r)
            if [ -z "$2" ]; then
                echo "❌ Usage: dp mercury report <account_id> [days]"
                return 1
            fi
            local days="${3:-30}"
            echo "📈 Generating $days day report..."
            python3 "$DUCK_SYSTEM/mercury_client.py" report "$2" "$days"
            ;;
        help|h|--help|-h|*)
            cat << 'EOF'
🏦 Mercury Bank Commands

USAGE: dp mercury <command> [args]

COMMANDS:
  ping, p                   Test API connection
  accounts, a               List all accounts
  balance, bal <account>    Get account balance
  transactions, tx <acc>    Get transactions
  report, r <account>       Generate financial report
  help                      Show this help

EXAMPLES:
  dp mercury ping
  dp mercury accounts
  dp mercury balance acc_123abc
  dp mercury transactions acc_123abc 50
  dp mercury report acc_123abc 30

SETUP:
1. Get API key: https://app.mercury.com/settings/api
2. Store: dp creds add mercury api_key YOUR_KEY
3. Test: dp mercury ping

FEATURES:
- Real-time balance checking
- Transaction history export
- Automated categorization
- Financial reporting
- Webhook support (coming soon)

SECURITY:
- API key stored in encrypted credentials
- Read-only by default
- No sensitive data logged
- Access restricted to L4+ (C-Suite)

For detailed docs: open ~/Documents/HonkNode/Duck-Pond/Knowledge-Base/Business/Mercury-Bank-Integration.md
EOF
            ;;
    esac
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
  creds <cmd>               Credential manager
  cost <cmd>                Cost tracker (status/check/log)
  xaman <cmd>               Xaman XRPL wallet (ping/rates/pay)
  flare <cmd>               Flare Network (ping/balance/fts)
  mercury <cmd>             Mercury Bank (accounts/transactions)
  tokens                    Token optimization guide
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
  dp creds add gmail app_password <secret>
  dp creds show gmail
  dp creds list

SECURITY:
  Credentials stored in: ~/Documents/HonkNode/Duck-Pond/.credentials/
  Permissions: 700 (owner only), never synced to cloud/GitHub

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
