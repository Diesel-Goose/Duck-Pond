#!/usr/bin/env python3
"""
Mercury Bank API Integration for Greenhead Labs LLC
Banking automation for business accounts

API Docs: https://docs.mercury.com/
Base URL: https://api.mercury.com/api/v1
"""

import json
import requests
from pathlib import Path
from typing import Dict, Optional, Any, List
from datetime import datetime, timedelta

class MercuryClient:
    """
    Mercury Bank API Client
    
    Features:
    - Account information
    - Transaction history
    - Transfers between accounts
    - Counterparty management
    - Webhook handling
    """
    
    BASE_URL = "https://api.mercury.com/api/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Mercury client
        
        Args:
            api_key: Mercury API key (or loads from credentials)
        """
        self.api_key = api_key or self._load_api_key()
        if not self.api_key:
            raise ValueError("Mercury API key required. Get from: https://app.mercury.com/settings/api")
    
    def _load_api_key(self) -> Optional[str]:
        """Load API key from secure storage"""
        creds_file = Path.home() / "Documents" / "HonkNode" / "Duck-Pond" / ".credentials" / "credentials.json"
        
        if creds_file.exists():
            try:
                with open(creds_file, 'r') as f:
                    data = json.load(f)
                    mercury = data.get("credentials", {}).get("mercury", {})
                    return mercury.get("api_key")
            except:
                pass
        
        return None
    
    def _headers(self) -> Dict[str, str]:
        """Generate API headers"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make API request"""
        url = f"{self.BASE_URL}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self._headers(),
                timeout=30,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                return {"error": "Invalid API key"}
            elif response.status_code == 404:
                return {"error": "Account or resource not found"}
            else:
                return {"error": f"HTTP {response.status_code}: {str(e)}"}
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== ACCOUNTS ====================
    
    def list_accounts(self) -> Dict[str, Any]:
        """Get all accounts for the organization"""
        return self._request("GET", "/accounts")
    
    def get_account(self, account_id: str) -> Dict[str, Any]:
        """Get specific account details"""
        return self._request("GET", f"/account/{account_id}")
    
    def get_account_balance(self, account_id: str) -> Dict[str, Any]:
        """Get account balance"""
        result = self.get_account(account_id)
        if "error" not in result:
            return {
                "account_id": account_id,
                "balance": result.get("currentBalance"),
                "available": result.get("availableBalance"),
                "currency": result.get("currency", "USD"),
                "name": result.get("name")
            }
        return result
    
    # ==================== TRANSACTIONS ====================
    
    def list_transactions(
        self, 
        account_id: str, 
        limit: int = 100,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get transactions for an account
        
        Args:
            account_id: Mercury account ID
            limit: Max transactions to return (default 100)
            start_date: ISO 8601 date (e.g., "2026-01-01")
            end_date: ISO 8601 date
        """
        params = {"limit": limit}
        if start_date:
            params["start"] = start_date
        if end_date:
            params["end"] = end_date
        
        return self._request("GET", f"/account/{account_id}/transactions", params=params)
    
    def get_transaction(self, account_id: str, transaction_id: str) -> Dict[str, Any]:
        """Get specific transaction details"""
        return self._request("GET", f"/account/{account_id}/transaction/{transaction_id}")
    
    # ==================== TRANSFERS ====================
    
    def list_transfers(self, limit: int = 100) -> Dict[str, Any]:
        """Get all transfers"""
        return self._request("GET", "/transfers", params={"limit": limit})
    
    def get_transfer(self, transfer_id: str) -> Dict[str, Any]:
        """Get specific transfer details"""
        return self._request("GET", f"/transfer/{transfer_id}")
    
    # ==================== COUNTERPARTIES ====================
    
    def list_counterparties(self) -> Dict[str, Any]:
        """Get all saved counterparties (recipients)"""
        return self._request("GET", "/counterparties")
    
    def get_counterparty(self, counterparty_id: str) -> Dict[str, Any]:
        """Get specific counterparty"""
        return self._request("GET", f"/counterparty/{counterparty_id}")
    
    # ==================== WEBHOOKS ====================
    
    def list_webhooks(self) -> Dict[str, Any]:
        """Get all configured webhooks"""
        return self._request("GET", "/webhooks")
    
    def create_webhook(self, url: str, secret: str, events: List[str]) -> Dict[str, Any]:
        """
        Create webhook for real-time notifications
        
        Events:
        - transaction.created
        - transaction.updated
        - transfer.created
        - transfer.completed
        - transfer.failed
        """
        data = {
            "url": url,
            "secret": secret,
            "events": events
        }
        return self._request("POST", "/webhooks", json=data)
    
    # ==================== PING ====================
    
    def ping(self) -> Dict[str, Any]:
        """Test API connectivity"""
        # Try to list accounts as health check
        result = self.list_accounts()
        if "error" not in result:
            return {
                "connected": True,
                "accounts_found": len(result.get("accounts", [])),
                "timestamp": datetime.now().isoformat()
            }
        return {
            "connected": False,
            "error": result.get("error")
        }


# ==================== BUSINESS LOGIC ====================

def categorize_transaction(tx: Dict) -> str:
    """Categorize a transaction for accounting"""
    description = tx.get("description", "").lower()
    
    categories = {
        "software": ["github", "aws", "vercel", "stripe", "twilio", "openai"],
        "infrastructure": ["cloudflare", "digitalocean", "linode", "vultr"],
        "marketing": ["google ads", "facebook", "twitter", "linkedin"],
        "legal": ["legal", "lawyer", "attorney", "clerk"],
        "payroll": ["gusto", "deel", "remote", "payroll"],
        "crypto": ["coinbase", "kraken", "binance", "crypto", "blockchain"]
    }
    
    for category, keywords in categories.items():
        if any(kw in description for kw in keywords):
            return category
    
    return "uncategorized"


def generate_report(client: MercuryClient, account_id: str, days: int = 30) -> Dict:
    """Generate financial report"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    transactions = client.list_transactions(
        account_id=account_id,
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
        limit=1000
    )
    
    if "error" in transactions:
        return transactions
    
    tx_list = transactions.get("transactions", [])
    
    # Calculate totals
    income = sum(tx.get("amount", 0) for tx in tx_list if tx.get("amount", 0) > 0)
    expenses = sum(tx.get("amount", 0) for tx in tx_list if tx.get("amount", 0) < 0)
    
    # Categorize
    categories = {}
    for tx in tx_list:
        cat = categorize_transaction(tx)
        categories[cat] = categories.get(cat, 0) + abs(tx.get("amount", 0))
    
    return {
        "period_days": days,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "total_transactions": len(tx_list),
        "income": income,
        "expenses": abs(expenses),
        "net": income + expenses,
        "by_category": categories
    }


# ==================== CLI ====================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Mercury Bank API Client for Greenhead Labs")
        print("\nUsage:")
        print("  python3 mercury_client.py ping                    # Test connection")
        print("  python3 mercury_client.py accounts                # List accounts")
        print("  python3 mercury_client.py balance <account_id>    # Get balance")
        print("  python3 mercury_client.py transactions <account_id> [limit]")
        print("  python3 mercury_client.py report <account_id> [days]")
        sys.exit(0)
    
    command = sys.argv[1]
    
    try:
        client = MercuryClient()
    except ValueError as e:
        print(f"❌ {e}")
        print("   Add your API key to ~/.credentials/credentials.json")
        sys.exit(1)
    
    if command == "ping":
        result = client.ping()
        print(json.dumps(result, indent=2))
    
    elif command == "accounts":
        result = client.list_accounts()
        print(json.dumps(result, indent=2))
    
    elif command == "balance" and len(sys.argv) > 2:
        account_id = sys.argv[2]
        result = client.get_account_balance(account_id)
        print(json.dumps(result, indent=2))
    
    elif command == "transactions" and len(sys.argv) > 2:
        account_id = sys.argv[2]
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 100
        result = client.list_transactions(account_id, limit=limit)
        print(json.dumps(result, indent=2))
    
    elif command == "report" and len(sys.argv) > 2:
        account_id = sys.argv[2]
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        result = generate_report(client, account_id, days)
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {command}")
        print("Run without arguments for help")
        sys.exit(1)
