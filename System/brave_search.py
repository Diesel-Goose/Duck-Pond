#!/usr/bin/env python3
"""
Brave Search Integration for Greenhead Labs
Web search via Brave API - privacy-focused, fast

Usage: python3 brave_search.py "your search query" [--count 5]
"""

import sys
import json
import argparse
from pathlib import Path
import requests

class BraveSearchClient:
    """Brave Search API client"""
    
    BASE_URL = "https://api.search.brave.com/res/v1"
    
    def __init__(self):
        self.api_key = self._load_api_key()
    
    def _load_api_key(self) -> str:
        """Load API key from credentials"""
        try:
            creds_file = Path.home() / "Documents" / "HonkNode" / "Duck-Pond" / ".credentials" / "credentials.json"
            with open(creds_file, 'r') as f:
                data = json.load(f)
                return data.get("credentials", {}).get("brave_search", {}).get("api_key", "")
        except:
            return ""
    
    def search(self, query: str, count: int = 5, offset: int = 0) -> dict:
        """
        Perform web search
        
        Args:
            query: Search query
            count: Number of results (1-20)
            offset: Pagination offset
        """
        if not self.api_key:
            return {"error": "API key not found. Check credentials."}
        
        headers = {
            "X-Subscription-Token": self.api_key,
            "Accept": "application/json"
        }
        
        params = {
            "q": query,
            "count": min(count, 20),  # Max 20
            "offset": offset
        }
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/web/search",
                headers=headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                return {"error": "Invalid API key"}
            return {"error": f"HTTP {response.status_code}: {str(e)}"}
        except Exception as e:
            return {"error": str(e)}
    
    def search_news(self, query: str, count: int = 5) -> dict:
        """Search news articles"""
        if not self.api_key:
            return {"error": "API key not found"}
        
        headers = {
            "X-Subscription-Token": self.api_key,
            "Accept": "application/json"
        }
        
        params = {
            "q": query,
            "count": min(count, 20)
        }
        
        try:
            response = requests.get(
                f"{self.BASE_URL}/news/search",
                headers=headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

def format_results(data: dict, verbose: bool = False) -> str:
    """Format search results for display"""
    if "error" in data:
        return f"❌ Error: {data['error']}"
    
    results = data.get('web', {}).get('results', [])
    if not results:
        return "No results found."
    
    output = []
    output.append(f"\n🦁 Found {len(results)} results:\n")
    
    for i, result in enumerate(results, 1):
        title = result.get('title', 'No title')
        url = result.get('url', 'No URL')
        description = result.get('description', '')
        
        output.append(f"{i}. {title}")
        output.append(f"   🌐 {url}")
        
        if verbose and description:
            # Truncate description
            desc = description[:150] + "..." if len(description) > 150 else description
            output.append(f"   📝 {desc}")
        
        output.append("")
    
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Brave Search for Greenhead Labs")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--count", "-n", type=int, default=5, help="Number of results (1-20)")
    parser.add_argument("--news", action="store_true", help="Search news instead of web")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show descriptions")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    
    args = parser.parse_args()
    
    client = BraveSearchClient()
    
    if args.news:
        results = client.search_news(args.query, args.count)
    else:
        results = client.search(args.query, args.count)
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_results(results, args.verbose))

if __name__ == "__main__":
    main()
