#!/usr/bin/env python3
"""
LLM Wrapper - Cost-Optimized Generation

ALWAYS tries Ollama (local/free) first.
Only falls back to cloud APIs if Ollama fails AND budget allows.

This saves ~$20/day by using local inference instead of cloud LLMs.

Usage:
  from llm_wrapper import generate, quick_generate
  
  result = generate("Your prompt here")
  print(result["text"])  # Generated text
  print(result["cost"])  # $0.00 for Ollama, $0.002+ for cloud

Author: Diesel-Goose AI
Born: Feb 21, 2026 at 4:20 PM, Cheyenne WY
"""

import requests
import json
import os
import sys
from pathlib import Path

# Add cost tracker to path
sys.path.insert(0, str(Path(__file__).parent))
from cost_tracker import log_api_call, check_budget

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3"
MAX_OLLAMA_RETRIES = 2

def generate(prompt, model=DEFAULT_MODEL, max_retries=MAX_OLLAMA_RETRIES, temperature=0.7):
    """
    Generate text using Ollama (FREE) first.
    Only fall back to cloud API if Ollama fails AND budget allows.
    
    Returns dict with:
    - text: generated content
    - source: "ollama" or "openai" or "error"
    - cost: $0.00 for Ollama, actual cost for cloud
    - model: which model was used
    """
    
    # Validate prompt
    if not prompt or not prompt.strip():
        return {
            "text": "Error: Empty prompt",
            "source": "error",
            "cost": 0.0,
            "model": "none"
        }
    
    # Truncate very long prompts (save tokens)
    if len(prompt) > 8000:
        prompt = prompt[:8000] + "\n\n[Content truncated for efficiency]"
    
    # Try Ollama first (FREE)
    print(f"🦆 Trying Ollama/{model} (free)...")
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": temperature,
                        "num_ctx": 4096,
                        "num_predict": 2048  # Limit response length
                    }
                },
                timeout=120  # 2 minute timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                text = result.get("response", "").strip()
                
                if text:
                    print(f"✅ Ollama success (free)")
                    return {
                        "text": text,
                        "source": "ollama",
                        "cost": 0.0,
                        "model": model
                    }
                else:
                    print(f"⚠️  Ollama returned empty response")
            else:
                print(f"⚠️  Ollama error: HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"⚠️  Ollama timeout (attempt {attempt + 1}/{max_retries})")
        except requests.exceptions.ConnectionError:
            print(f"⚠️  Ollama not running (attempt {attempt + 1}/{max_retries})")
            print(f"   Start with: ollama serve")
            break  # Don't retry if Ollama isn't running
        except Exception as e:
            print(f"⚠️  Ollama error: {e}")
    
    # Ollama failed - check if we can use cloud API
    print("\n⚠️  Ollama unavailable, checking budget for cloud fallback...")
    can_use_cloud, remaining = check_budget()
    
    if not can_use_cloud:
        print("🚨 Budget exceeded. Cannot use cloud API.")
        print("   Suggestions:")
        print("   1. Start Ollama: ollama serve")
        print("   2. Wait for tomorrow (budget resets daily)")
        print("   3. Ask Chairman to approve emergency budget")
        return {
            "text": "Error: Ollama unavailable and budget exceeded. Please start Ollama or wait for budget reset.",
            "source": "error",
            "cost": 0.0,
            "model": "none"
        }
    
    # FALLBACK: Use cloud API (expensive, logged)
    print(f"💸 Using cloud API (budget remaining: ${remaining:.2f})")
    
    # Try cheaper models first
    cloud_result = try_openai(prompt, "gpt-3.5-turbo")  # Cheapest
    
    if cloud_result:
        return cloud_result
    
    # If GPT-3.5 fails, try GPT-4 (more expensive)
    print("⚠️  GPT-3.5 failed, trying GPT-4...")
    cloud_result = try_openai(prompt, "gpt-4")
    
    if cloud_result:
        return cloud_result
    
    # All options exhausted
    return {
        "text": "Error: All LLM options exhausted (Ollama + cloud APIs failed)",
        "source": "error",
        "cost": 0.0,
        "model": "none"
    }

def try_openai(prompt, model="gpt-3.5-turbo"):
    """Try OpenAI API with cost tracking."""
    try:
        # Check for API key
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("❌ OPENAI_API_KEY not set")
            return None
        
        # Only import if needed (saves memory)
        import openai
        openai.api_key = api_key
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Be concise."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,  # Limit to save cost
            temperature=0.7
        )
        
        text = response['choices'][0]['message']['content'].strip()
        usage = response['usage']
        
        # Calculate cost
        if model == "gpt-3.5-turbo":
            # $0.002 per 1K tokens
            cost = (usage['total_tokens'] / 1000) * 0.002
        elif model == "gpt-4":
            # $0.03 per 1K tokens (input) + $0.06 per 1K tokens (output)
            input_cost = (usage['prompt_tokens'] / 1000) * 0.03
            output_cost = (usage['completion_tokens'] / 1000) * 0.06
            cost = input_cost + output_cost
        else:
            cost = 0.01  # Default estimate
        
        cost = round(cost, 4)
        
        # Log the cost
        log_api_call(f"openai_{model}", cost, prompt[:50])
        
        print(f"✅ OpenAI/{model} success (${cost:.4f})")
        
        return {
            "text": text,
            "source": "openai",
            "cost": cost,
            "model": model,
            "tokens": usage['total_tokens']
        }
        
    except Exception as e:
        print(f"❌ OpenAI error: {e}")
        return None

# Convenience functions
def quick_generate(prompt, **kwargs):
    """Quick generation - returns text only."""
    result = generate(prompt, **kwargs)
    return result.get("text", "")

def summarize(text, max_words=100, **kwargs):
    """Summarize text using Ollama."""
    prompt = f"Summarize this text in {max_words} words or less:\n\n{text}"
    return quick_generate(prompt, **kwargs)

def analyze(text, question, **kwargs):
    """Analyze text and answer a question."""
    prompt = f"Text: {text}\n\nQuestion: {question}\n\nAnswer:"
    return quick_generate(prompt, **kwargs)

def code_review(code, language="python", **kwargs):
    """Review code for issues."""
    prompt = f"Review this {language} code for bugs, security issues, and improvements:\n\n```{language}\n{code}\n```"
    return quick_generate(prompt, **kwargs)

def generate_bullet_points(topic, count=5, **kwargs):
    """Generate bullet points on a topic."""
    prompt = f"Generate {count} bullet points about: {topic}"
    return quick_generate(prompt, **kwargs)

# Self-test
if __name__ == "__main__":
    print("🦆 LLM Wrapper - Cost-Optimized Generation")
    print("=" * 50)
    print("\nTesting Ollama (free)...")
    
    result = generate("What is 2+2? Answer in one word.")
    
    print(f"\nResult:")
    print(f"  Text: {result['text']}")
    print(f"  Source: {result['source']}")
    print(f"  Cost: ${result['cost']:.4f}")
    print(f"  Model: {result['model']}")
    
    if result['cost'] == 0.0:
        print("\n✅ Success! Using free Ollama.")
    else:
        print(f"\n💸 Used cloud API (${result['cost']:.4f})")
