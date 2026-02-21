# Local LLM Optimization
## Maximizing Ollama Performance on HonkNode

**Token-Optimized Quick Reference**

---

## Ollama Setup (30-sec read)

**What:** Run AI models locally on M4 chip  
**Why:** Free, private, fast, no API limits  
**Where:** HonkNode (Mac Mini M4, 16GB)  
**Cost:** $0 vs $20/day cloud API  
**Speed:** 10-50 tokens/sec depending on model

---

## Model Selection Guide

### Quick Reference
```
Model        Size    RAM     Speed    Quality    Best For
────────────────────────────────────────────────────────────
phi3         3.8B    3GB     ⚡⚡⚡⚡⚡   ⭐⭐⭐      Simple Q&A, summaries
llama3       8B      6GB     ⚡⚡⚡⚡    ⭐⭐⭐⭐     General purpose (DEFAULT)
codegemma    7B      5GB     ⚡⚡⚡⚡    ⭐⭐⭐⭐     Coding tasks
mistral      7B      5GB     ⚡⚡⚡⚡    ⭐⭐⭐⭐     Reasoning
mixtral      47B     26GB    ⚡⚡      ⭐⭐⭐⭐⭐    Complex reasoning
llama3:70b   70B     40GB+   ⚡        ⭐⭐⭐⭐⭐    Maximum quality
```

### Greenhead Labs Standard
```
Default: llama3 (8B)
Why: Best speed/quality balance for 16GB RAM

Fast tasks: phi3 (3.8B)
Complex tasks: mixtral (47B) if memory available
Coding: codegemma or codellama
```

---

## Installation & Setup

### Install Ollama
```bash
# macOS (HonkNode)
curl -fsSL https://ollama.com/install.sh | sh

# Or download from ollama.com
```

### Pull Models
```bash
# Essential models
ollama pull llama3          # Default
ollama pull phi3            # Fast
ollama pull codegemma       # Coding
ollama pull mixtral         # Complex tasks

# Check installed
ollama list
```

### Verify Installation
```bash
# Test query
ollama run llama3 "Explain blockchain in 3 bullet points"

# Expected: ~20-30 tokens/sec on M4
```

---

## Performance Optimization

### 1. Quantization (Reduce Memory)
```bash
# Full precision (slowest, most accurate)
ollama pull llama3

# 4-bit quantized (recommended)
ollama pull llama3:q4_0

# Even smaller (faster, less accurate)
ollama pull llama3:q2_K

# Greenhead Standard: q4_0
```

**Memory Savings:**
- FP16: 16GB for 8B model
- Q4_0: 4GB for 8B model
- Q2_K: 2GB for 8B model

### 2. Context Window Tuning
```python
# Default: 2048 tokens
# Increase for long documents
# Decrease for speed/memory

# Optimal for HonkNode:
CONTEXT_WINDOW = 4096  # Good balance

# llm_wrapper.py settings:
ollama.generate(
    model='llama3',
    prompt=prompt,
    options={
        'num_ctx': 4096,  # Context window
        'temperature': 0.7,
        'top_p': 0.9
    }
)
```

### 3. Batch Processing
```python
# Process multiple queries together
prompts = [
    "Summarize: " + doc1,
    "Summarize: " + doc2,
    "Summarize: " + doc3
]

# Sequential (slower)
for p in prompts:
    result = ollama.generate(p)

# Parallel (faster, more memory)
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=3) as exe:
    results = list(exe.map(generate, prompts))
```

### 4. Caching Strategies
```python
import hashlib
import json

response_cache = {}

def cached_generate(prompt, model='llama3'):
    # Create cache key
    key = hashlib.md5(f"{model}:{prompt}".encode()).hexdigest()
    
    # Check cache
    if key in response_cache:
        return response_cache[key]  # Instant, zero energy
    
    # Generate and cache
    result = ollama.generate(model=model, prompt=prompt)
    response_cache[key] = result
    
    # Persist cache
    with open('cache.json', 'w') as f:
        json.dump(response_cache, f)
    
    return result
```

---

## Advanced Configuration

### Modelfile (Custom Models)
```dockerfile
# Create custom model
# File: GreenheadAssistant

FROM llama3

# System prompt
SYSTEM """
You are Diesel-Goose, the AI executive assistant for Greenhead Labs.
You specialize in blockchain, DeFi, and cryptocurrency operations.
Be concise, technical, and accurate.
"""

# Parameters
PARAMETER temperature 0.5
PARAMETER top_p 0.9
PARAMETER num_ctx 4096

# Create
cat GreenheadAssistant | ollama create diesel-goose -f -

# Use
ollama run diesel-goose
```

### API Server Mode
```bash
# Start API server
ollama serve

# Default: http://localhost:11434

# Test API
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Explain XRPL consensus"
}'
```

### Integration with llm_wrapper.py
```python
import ollama
import subprocess

class LocalLLM:
    def __init__(self, model='llama3'):
        self.model = model
        self.ensure_running()
    
    def ensure_running(self):
        """Ensure Ollama is running."""
        try:
            ollama.list()
        except:
            subprocess.Popen(['ollama', 'serve'])
    
    def generate(self, prompt, **kwargs):
        """Generate with error handling."""
        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options=kwargs
            )
            return response['response']
        except Exception as e:
            return f"Error: {e}"

# Usage
llm = LocalLLM('llama3')
result = llm.generate("Explain DeFi", temperature=0.7)
```

---

## Performance Benchmarks

### M4 Chip Performance
```
Model        Quant    Tokens/sec    RAM Used
─────────────────────────────────────────────
phi3         q4_0     45-55         2.5 GB
llama3       q4_0     25-35         5 GB
llama3       q8_0     15-20         8 GB
mixtral      q4_0     8-12          28 GB
mixtral      q3_K_M   10-15         22 GB

Note: Higher context = slower generation
```

### Optimization Checklist
```
✅ Use quantized models (q4_0)
✅ Set appropriate context window
✅ Enable response caching
✅ Batch similar requests
✅ Monitor memory usage
✅ Restart if memory leaks
```

---

## Troubleshooting

### Slow Generation
```
Causes:
├── Model too large for RAM (swapping)
├── Context window too big
├── Other processes using CPU
└── Thermal throttling

Solutions:
├── Use smaller model (phi3 vs llama3)
├── Reduce num_ctx
├── Close other apps
├── Check temps (sudo powermetrics)
```

### Out of Memory
```
Error: "runtime error: out of memory"

Solutions:
├── Use smaller model
├── Reduce context window
├── Close other applications
├── Restart Ollama service
└── Use quantization (q4_0 or q2_K)
```

### Model Not Found
```
Error: "model 'X' not found"

Fix:
ollama pull X

Verify:
ollama list
```

### Service Not Running
```
Error: Connection refused

Fix:
ollama serve

Or start on boot:
brew services start ollama
```

---

## Greenhead Labs Best Practices

### 1. Model Selection
```
Simple Q&A → phi3 (fastest)
General work → llama3 (balanced)
Complex reasoning → mixtral (quality)
Never use cloud unless Ollama fails 3x
```

### 2. Prompt Engineering
```
✅ Be specific
✅ Provide context
✅ Use examples
✅ Request structured output

❌ Vague requests
❌ Missing context
❌ Expecting mind-reading
```

### 3. Cost Tracking
```python
# Log all LLM usage
def log_usage(model, tokens, source):
    cost = 0 if model in LOCAL_MODELS else calculate_cloud_cost(tokens)
    
    with open('llm_usage.log', 'a') as f:
        f.write(f"{timestamp},{model},{tokens},{cost},{source}\n")
```

### 4. Fallback Strategy
```python
def generate_with_fallback(prompt):
    """Try local first, cloud only if needed."""
    
    # Try Ollama
    try:
        return ollama.generate('llama3', prompt)
    except:
        pass
    
    # Try alternative local model
    try:
        return ollama.generate('phi3', prompt)
    except:
        pass
    
    # Last resort: Cloud (if budget allows)
    if budget_remaining > 0:
        return cloud_api.generate(prompt)
    
    return "Error: No models available"
```

---

## Resources

- **Ollama Docs:** https://github.com/ollama/ollama
- **Model Library:** https://ollama.com/library
- **Discord:** https://discord.gg/ollama
- **GitHub:** https://github.com/ollama/ollama

---

**Diesel-Goose Knowledge Priority:** CRITICAL  
**Usage:** All AI operations, cost reduction  
**Last Updated:** 2026-02-21  
**Token Count:** ~1,200

🦆 **Ollama optimized. Local inference at maximum efficiency.**
