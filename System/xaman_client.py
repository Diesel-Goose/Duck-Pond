#!/usr/bin/env python3
"""
Xaman (XUMM) API Integration for Greenhead Labs
XRPL Wallet Operations via Xaman API

Born: February 21, 2026
Purpose: Secure XRPL transactions, sign requests, wallet management
"""

import json
import requests
from pathlib import Path
from typing import Dict, Optional, Any

class XamanClient:
    """Xaman API client for XRPL operations"""
    
    BASE_URL = "https://xumm.app/api/v1/platform"
    
    def __init__(self):
        self.api_key = None
        self.api_secret = None
        self._load_credentials()
    
    def _load_credentials(self):
        """Load API credentials from secure storage"""
        creds_file = Path.home() / "Documents" / "HonkNode" / "Duck-Pond" / ".credentials" / "credentials.json"
        
        if creds_file.exists():
            with open(creds_file, 'r') as f:
                data = json.load(f)
                xaman = data.get("credentials", {}).get("xaman", {})
                self.api_key = xaman.get("api_key")
                self.api_secret = xaman.get("api_secret")
        
        if not self.api_key or not self.api_secret:
            raise ValueError("Xaman credentials not found. Run setup first.")
    
    def _headers(self) -> Dict[str, str]:
        """Generate API headers"""
        return {
            'authorization': 'Bearer ',
            'content-type': 'application/json',
            'x-api-key': self.api_key,
            'x-api-secret': self.api_secret
        }
    
    def ping(self) -> Dict[str, Any]:
        """Test API connectivity"""
        try:
            response = requests.post(
                f"{self.BASE_URL}/ping",
                headers=self._headers(),
                json={}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e), "pong": False}
    
    def get_curated_assets(self) -> Dict[str, Any]:
        """Get list of curated assets"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/curated-assets",
                headers=self._headers()
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_rates(self, currency: str = "XRP") -> Dict[str, Any]:
        """Get exchange rates"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/rates/{currency}",
                headers=self._headers()
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def create_sign_request(self, tx_json: Dict[str, Any], 
                           options: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create a sign request for user to approve
        
        Args:
            tx_json: XRPL transaction JSON
            options: Optional settings (submit, expire, etc.)
        
        Returns:
            Sign request with QR code URL
        """
        payload = {
            "txjson": tx_json
        }
        
        if options:
            payload["options"] = options
        
        try:
            response = requests.post(
                f"{self.BASE_URL}/payload",
                headers=self._headers(),
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_payload_status(self, payload_uuid: str) -> Dict[str, Any]:
        """Check status of a sign request"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/payload/{payload_uuid}",
                headers=self._headers()
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def delete_payload(self, payload_uuid: str) -> Dict[str, Any]:
        """Cancel/delete a sign request"""
        try:
            response = requests.delete(
                f"{self.BASE_URL}/payload/{payload_uuid}",
                headers=self._headers()
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_user_tokens(self) -> Dict[str, Any]:
        """Get stored user tokens (paired wallets)"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/userdata",
                headers=self._headers()
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}


# Common transaction templates
def payment_template(destination: str, amount: str, currency: str = "XRP") -> Dict[str, Any]:
    """Create a payment transaction"""
    if currency == "XRP":
        # Amount in drops (1 XRP = 1,000,000 drops)
        drops = int(float(amount) * 1_000_000)
        return {
            "TransactionType": "Payment",
            "Destination": destination,
            "Amount": str(drops)
        }
    else:
        # IOU payment
        return {
            "TransactionType": "Payment",
            "Destination": destination,
            "Amount": {
                "currency": currency,
                "value": amount,
                "issuer": destination  # Usually the issuer address
            }
        }


def trust_set_template(issuer: str, currency: str, limit: str) -> Dict[str, Any]:
    """Create a trust line transaction"""
    return {
        "TransactionType": "TrustSet",
        "LimitAmount": {
            "currency": currency,
            "issuer": issuer,
            "value": limit
        }
    }


def offer_create_template(taker_gets: Dict, taker_pays: Dict) -> Dict[str, Any]:
    """Create a DEX offer"""
    return {
        "TransactionType": "OfferCreate",
        "TakerGets": taker_gets,
        "TakerPays": taker_pays
    }


# CLI interface
if __name__ == "__main__":
    import sys
    
    client = XamanClient()
    
    if len(sys.argv) < 2:
        print("Xaman API Client for Greenhead Labs")
        print("\nUsage:")
        print("  python3 xaman_client.py ping              # Test connection")
        print("  python3 xaman_client.py rates [XRP]       # Get exchange rates")
        print("  python3 xaman_client.py assets            # List curated assets")
        print("  python3 xaman_client.py status <uuid>     # Check payload status")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "ping":
        result = client.ping()
        print(json.dumps(result, indent=2))
    
    elif command == "rates":
        currency = sys.argv[2] if len(sys.argv) > 2 else "XRP"
        result = client.get_rates(currency)
        print(json.dumps(result, indent=2))
    
    elif command == "assets":
        result = client.get_curated_assets()
        print(json.dumps(result, indent=2))
    
    elif command == "status" and len(sys.argv) > 2:
        uuid = sys.argv[2]
        result = client.get_payload_status(uuid)
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
