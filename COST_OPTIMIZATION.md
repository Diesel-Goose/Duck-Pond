# Duck Pond Cost Optimization Guide
## LLM API Cost Reduction Strategy

**Current Burn Rate:** $20/day ($600/month)  
**Target:** $0-2/day ($0-60/month)  
**Savings:** 95-100%

---

## The Problem

You're spending $20/day on cloud LLM APIs (OpenAI, Claude, etc.) when you have a **Mac Mini M4 with Ollama running locally**. This is burning cash unnecessarily.

---

## Cost-Cutting Rules (Implement Immediately)

### Rule 1: Local-First Mandate
**NEVER use cloud LLM when Ollama is available**

| Task | Old Way (Cost) | New Way (Cost) | Savings |
|------|----------------|----------------|---------|
| Text generation | GPT-4 ($0.03/1K tokens) | Ollama/llama3 ($0) | 100% |
| Code review | GPT-4 ($0.03/1K tokens) | Ollama/llama3 ($0) | 100% |
| Summarization | GPT-3.5 ($0.002/1K tokens) | Ollama/llama3 ($0) | 100% |
| Document analysis | Claude ($0.008/1K tokens) | Ollama/llama3 ($0) | 100% |
| Chat/QA | GPT-4 ($0.06/1K tokens) | Ollama/llama3 ($0) | 100% |

### Rule 2: API Tiers (Strict Hierarchy)

**Tier 1: Ollama (Local) — FREE**
- All routine text generation
- Code completion and review
- Document summarization
- Question answering
- Journal generation (already implemented)
- Email analysis (already implemented)

**Tier 2: Ollama with larger model (Local) — FREE**
- Complex reasoning tasks
- Multi-step analysis
- Code architecture decisions
- Business plan writing

**Tier 3: Cloud API (Pay) — EMERGENCY ONLY**
- Tasks Ollama cannot handle after 3 attempts
- External API integrations requiring specific formats
- Real-time information (web search + synthesis)
- Tasks explicitly delegated by Chairman with "API-OK" tag

### Rule 3: Cost Monitoring

**Daily Budget:** $2 maximum  
**Weekly Budget:** $10 maximum  
**Monthly Budget:** $50 maximum

**Enforcement:**
- Track every API call in `~/.duckpond/cost_log.json`
- Before ANY cloud API call, check budget
- If budget exceeded, use Ollama only until reset
- Report daily spend to Chairman

---

## Immediate Actions

### 1. Audit Current API Usage

Find where cloud APIs are being called:

```bash
# Search for API keys in use
grep -r "openai" ~/Documents/HonkNode/ 2>/dev/null
grep -r "OPENAI" ~/Documents/HonkNode/ 2>/dev/null
grep -r "claude" ~/Documents/HonkNode/ 2>/dev/null
grep -r "anthropic" ~/Documents/HonkNode/ 2>/dev/null

# Check running processes
ps aux | grep -E "python|node" | grep -v grep
```

### 2. Replace Cloud Calls with Ollama

**Before (Costly):**
```python
import openai
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
```

**After (Free):**
```python
import requests
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }
)
```

### 3. Implement Cost Tracker

**File:** `~/Documents/HonkNode/Duck-Pond/System/cost_tracker.py`

```python
import json
from datetime import datetime
from pathlib import Path

COST_LOG = Path.home() / "Documents" / "HonkNode" / "Duck-Pond" / ".vault" / "cost_log.json"
DAILY_BUDGET = 2.00  # $2/day max

def log_api_call(service, cost, task):
    """Log every API call with cost."""
    data = load_cost_log()
    today = datetime.now().strftime("%Y-%m-%d")
    
    if today not in data:
        data[today] = {"calls": [], "total": 0.0}
    
    data[today]["calls"].append({
        "time": datetime.now().isoformat(),
        "service": service,
        "cost": cost,
        "task": task
    })
    data[today]["total"] += cost
    
    save_cost_log(data)
    return data[today]["total"]

def check_budget():
    """Check if we have budget remaining."""
    data = load_cost_log()
    today = datetime.now().strftime("%Y-%m-%d")
    spent = data.get(today, {}).get("total", 0.0)
    remaining = DAILY_BUDGET - spent
    
    if remaining <= 0:
        print(f"🚨 Daily budget EXCEEDED: ${spent:.2f} / ${DAILY_BUDGET:.2f}")
        print("   Switching to Ollama-only mode")
        return False, 0.0
    
    print(f"💰 Budget: ${spent:.2f} spent / ${DAILY_BUDGET:.2f} daily")
    print(f"   Remaining: ${remaining:.2f}")
    return True, remaining

def load_cost_log():
    if COST_LOG.exists():
        with open(COST_LOG) as f:
            return json.load(f)
    return {}

def save_cost_log(data):
    COST_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(COST_LOG, 'w') as f:
        json.dump(data, f, indent=2)
```

### 4. Create Ollama-Only Wrapper

**File:** `~/Documents/HonkNode/Duck-Pond/System/llm_wrapper.py`

```python
"""
LLM Wrapper - ALWAYS try Ollama first, fallback to cloud only if needed
"""
import requests
import json
from cost_tracker import log_api_call, check_budget

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate(prompt, model="llama3", max_retries=2):
    """
    Generate text using Ollama (free) first.
    Only fall back to cloud API if Ollama fails AND budget allows.
    """
    # Try Ollama first
    for attempt in range(max_retries):
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_ctx": 4096
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "text": result.get("response", ""),
                    "source": "ollama",
                    "cost": 0.00,
                    "model": model
                }
        except Exception as e:
            print(f"⚠️  Ollama attempt {attempt + 1} failed: {e}")
    
    # Ollama failed - check if we can use cloud API
    print("⚠️  Ollama unavailable, checking budget for cloud fallback...")
    can_use_cloud, remaining = check_budget()
    
    if not can_use_cloud:
        print("🚨 Budget exceeded. Cannot use cloud API.")
        print("   Returning error. Please fix Ollama or wait for budget reset.")
        return {
            "text": "Error: Ollama unavailable and budget exceeded",
            "source": "error",
            "cost": 0.00,
            "model": "none"
        }
    
    # FALLBACK: Use cloud API (expensive, logged)
    print(f"💸 Using cloud API fallback (${remaining:.2f} remaining in budget)")
    
    # Try OpenAI (most expensive, use sparingly)
    try:
        import os
        # Only import if key exists
        if os.environ.get("OPENAI_API_KEY"):
            import openai
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Cheaper than GPT-4
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            
            # Estimate cost (GPT-3.5: $0.002/1K tokens)
            tokens_used = response['usage']['total_tokens']
            cost = (tokens_used / 1000) * 0.002
            
            log_api_call("openai_gpt35", cost, prompt[:50])
            
            return {
                "text": response['choices'][0]['message']['content'],
                "source": "openai",
                "cost": cost,
                "model": "gpt-3.5-turbo",
                "tokens": tokens_used
            }
    except Exception as e:
        print(f"❌ Cloud API also failed: {e}")
    
    return {
        "text": "Error: All LLM options exhausted",
        "source": "error",
        "cost": 0.00,
        "model": "none"
    }

# Convenience functions
def quick_generate(prompt):
    """Quick generation with default settings."""
    return generate(prompt)["text"]

def summarize(text, max_length=200):
    """Summarize text using Ollama."""
    prompt = f"Summarize this in {max_length} characters or less:\n\n{text}"
    return generate(prompt)["text"]
```

---

## Cost Monitoring Commands

Add to `duck-pond.sh`:

```bash
# Cost tracking
dp-cost() {
    python3 "$DUCK_SYSTEM/cost_tracker.py" status
}

dp-cost-reset() {
    echo "Resetting daily cost counter..."
    python3 "$DUCK_SYSTEM/cost_tracker.py" reset
}
```

---

## Expected Savings

**Before Optimization:**
- $20/day = $600/month
- Unlimited cloud API usage
- No tracking

**After Optimization:**
- $0-2/day = $0-60/month
- 95-100% local Ollama usage
- Full cost tracking and enforcement

**Monthly Savings:** $540-600
**Annual Savings:** $6,480-7,200

---

## Chairman's Mandate

**Effective immediately:**

1. ✅ ALL text generation uses Ollama (local) first
2. ✅ Cloud APIs require explicit "API-OK" tag from Chairman
3. ✅ Daily budget cap: $2 maximum
4. ✅ Every API call logged with cost
5. ✅ Weekly cost report to Chairman

**Exceptions (rare):**
- Real-time web search + synthesis
- External API requiring specific JSON formats
- Tasks explicitly marked "API-OK" by Chairman
- Ollama fails 3 times on same task

---

## Implementation Checklist

- [ ] Audit all current API usage
- [ ] Replace cloud calls with Ollama
- [ ] Implement cost_tracker.py
- [ ] Implement llm_wrapper.py
- [ ] Add cost monitoring to shell shortcuts
- [ ] Test Ollama-only mode for 24 hours
- [ ] Report savings to Chairman

---

**Duck Pond: Local-first, Billion-scale, Cost-disciplined.**

🦆💰 **Quack protocol: PROFITABLE**
