# Token Optimization & Local LLM Strategy
## Keeping Context Under 123K, Maximizing Ollama Usage

**Born:** Feb 21, 2026 at 4:20 PM, Cheyenne WY  
**Purpose:** Minimize cloud API usage, maximize local Ollama performance

---

## The Problem

**Current State:**
- Context limit: 123K tokens
- Daily API burn: $20/day (unsustainable)
- Too many calls to Kimi K2.5 (cloud)
- Not leveraging local Ollama enough

**Target State:**
- Stay under 123K context
- Daily API burn: $0-2/day
- 95%+ local Ollama usage
- Fast, local responses

---

## Token Budgeting (123K Limit)

### Context Budget Allocation

```
Total Context: 123,000 tokens
├── System/Persona: ~2,000 tokens (2%)
├── HEARTBEAT.md reference: ~1,000 tokens (1%)
├── Recent conversation: ~10,000 tokens (8%)
├── Duck Pond search results: ~5,000 tokens (4%)
├── Code/files to edit: ~20,000 tokens (16%)
└── Working buffer: ~85,000 tokens (69%)
```

### When Context Gets Full

**Symptoms:**
- Slow responses
- High API costs
- Truncated outputs
- Lost conversation history

**Solutions:**
1. **Summarize conversation** → Store in Duck Pond
2. **Offload to local files** → Reference by path
3. **Use Ollama for routine tasks** → No token limit
4. **Clear old context** → Start fresh session

---

## Ollama-First Strategy

### Rule: Always Try Ollama First

**Flow:**
```
User Request
    ↓
Can Ollama handle this?
    ↓ YES → Use Ollama (free, fast, local)
    ↓ NO → Check budget
              ↓
        Budget available?
              ↓ YES → Use cloud API (expensive)
              ↓ NO → Defer to Chairman
```

### What Ollama Excels At (Use These)

| Task | Ollama | Cloud API |
|------|--------|-----------|
| Text generation | ✅ Free | ❌ $0.03/1K tokens |
| Code completion | ✅ Free | ❌ $0.03/1K tokens |
| Summarization | ✅ Free | ❌ $0.002/1K tokens |
| Q&A over docs | ✅ Free | ❌ $0.03/1K tokens |
| Brainstorming | ✅ Free | ❌ $0.03/1K tokens |
| Format conversion | ✅ Free | ❌ $0.002/1K tokens |
| Simple analysis | ✅ Free | ❌ $0.03/1K tokens |

### What Needs Cloud API (Rare)

- Real-time web search + synthesis
- Complex multi-step reasoning (after Ollama fails)
- External API integrations
- Tasks explicitly marked "API-OK" by Chairman

---

## Token-Saving Techniques

### 1. Summarize Before Sending

**Before (expensive):**
```
Send entire 50K token document to API
Cost: $1.50 per call
```

**After (cheap):**
```
Ollama summarizes to 500 tokens
Send summary to API if needed
Cost: $0.00 (Ollama) + $0.015 (API) = $0.015
Savings: 99%
```

### 2. Chunk Large Documents

```python
# Split large files into chunks
def chunk_text(text, max_tokens=2000):
    words = text.split()
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    for word in words:
        # Rough estimate: 1 word ≈ 1.3 tokens
        word_tokens = len(word) / 4 + 1
        
        if current_tokens + word_tokens > max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_tokens = word_tokens
        else:
            current_chunk.append(word)
            current_tokens += word_tokens
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks
```

### 3. Use Local Storage (Duck Pond)

**Instead of keeping in context:**
```
❌ Bad: "Remember this 10K token business plan"
```

**Store locally, reference by path:**
```
✅ Good: "Reference ~/Documents/HonkNode/Duck-Pond/Knowledge-Base/Business/plan.md"
```

### 4. Clear Context Regularly

```bash
# When context gets full
/new or /reset  # Start fresh session

# Then load only what's needed from Duck Pond
dp show <doc_id>  # Load specific document
```

### 5. Compress System Prompts

**Before (verbose):**
```
You are Diesel-Goose AI, the executive assistant to the Chairman of Greenhead Labs...
[500 tokens of persona description]
```

**After (compressed):**
```
Diesel-Goose AI | Chairman's exec assistant | Local-first | Faith-aligned | Billions trajectory
[50 tokens]
```

---

## Fast Local Operations (Ollama)

### Use These Commands (No API Cost)

```bash
# Generate text locally
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Write a summary of: $TEXT",
  "stream": false
}'

# Quick local Q&A
dp ask "What are our goals?"  # Uses Ollama

# Generate journal (already implemented)
python3 generate-morning-journal.py  # Uses Ollama

# Cost check (local)
dp-cost status  # Shows spending, no API call
```

### Python: Local-First Code Pattern

```python
from llm_wrapper import generate

# This tries Ollama first (free), only falls back to cloud if needed
result = generate("Your prompt here")

print(f"Cost: ${result['cost']:.4f}")  # Usually $0.00
print(f"Source: {result['source']}")   # Usually "ollama"
```

---

## Context Management Commands

### Add to duck-pond.sh

```bash
# Check token usage
dp-tokens() {
    echo "💾 Context Management"
    echo "====================="
    echo "To reduce token usage:"
    echo "  1. /new or /reset - Start fresh session"
    echo "  2. Store docs in Duck Pond, reference by path"
    echo "  3. Use Ollama for routine tasks"
    echo "  4. Summarize long conversations"
    echo ""
    echo "Current session: Check /status"
}

# Summarize and store
dp-summarize() {
    local file="$1"
    if [ -f "$file" ]; then
        echo "📝 Summarizing $file with Ollama..."
        local summary=$(curl -s http://localhost:11434/api/generate \
            -d "{\"model\":\"llama3\",\"prompt\":\"Summarize this in 200 words:\n$(cat "$file")\",\"stream\":false}" \
            | jq -r '.response')
        
        echo "$summary" | dp-quick "Summary: $(basename $file)"
        echo "✅ Summary stored in Duck Pond"
    else
        echo "❌ File not found: $file"
    fi
}
```

---

## Monitoring Token Usage

### Track Daily Metrics

```python
# Add to cost_tracker.py
def log_token_usage(source, tokens_in, tokens_out, task):
    """Log token usage for monitoring."""
    data = load_log()
    today = get_today()
    
    if "tokens" not in data[today]:
        data[today]["tokens"] = {"in": 0, "out": 0, "calls": 0}
    
    data[today]["tokens"]["in"] += tokens_in
    data[today]["tokens"]["out"] += tokens_out
    data[today]["tokens"]["calls"] += 1
    
    save_log(data)
    
    # Alert if approaching limit
    total = data[today]["tokens"]["in"] + data[today]["tokens"]["out"]
    if total > 100000:  # 100K warning
        print(f"⚠️  Token usage high: {total:,} / 123,000")
```

---

## Emergency Procedures

### Context Overflow (123K+ tokens)

**Symptoms:**
- "Context limit exceeded" errors
- Truncated responses
- Slow performance

**Fix:**
```bash
1. /new or /reset           # Clear context immediately
2. dp recent                # See recent documents
3. Load only what you need:
   dp show <doc_id>         # Load specific doc
   dp search <query>        # Find relevant docs
4. Use Ollama for new tasks  # No token limit
```

### API Budget Exceeded

**Symptoms:**
- "Budget exceeded" warnings
- Can't use cloud APIs

**Fix:**
```bash
1. Use Ollama exclusively    # Free, unlimited
2. Check costs:
   dp-cost status            # See spending
3. Defer to Chairman:
   "Chairman: Budget exceeded, need API access for X"
```

---

## Success Metrics

**Daily Targets:**
- Token usage: < 50K average
- API calls: < 10 per day
- Ollama usage: > 95% of tasks
- API cost: $0-2 per day

**Weekly Review:**
```bash
# Check weekly stats
dp-cost status

# Review token-heavy operations
# Optimize or move to Ollama
```

---

## Chairman's Mandate

**Effective immediately:**

1. ✅ **Ollama-first** for ALL routine tasks
2. ✅ **Local storage** for large documents (Duck Pond)
3. ✅ **Context discipline** - Stay under 100K tokens
4. ✅ **Token monitoring** - Track usage daily
5. ✅ **Budget enforcement** - $2/day max, no exceptions

**Exceptions (rare, approved by Chairman only):**
- Critical business decisions requiring GPT-4
- Real-time market analysis
- External API integrations
- Emergency situations

---

**Fast. Local. Cost-disciplined. Token-optimized.**

🦆⚡ **Quack protocol: EFFICIENT**
