#!/usr/bin/env python3
"""
Flare Network Integration for Greenhead Labs
EVM-compatible smart contract interactions

Born: February 21, 2026
Purpose: Flare blockchain operations, FTSO oracle data, F-Assets
"""

import json
import requests
from pathlib import Path
from typing import Dict, Optional, Any, List
from decimal import Decimal

class FlareClient:
    """Flare Network API client"""
    
    # Network endpoints
    NETWORKS = {
        "mainnet": {
            "rpc": "https://flare-api.flare.network/ext/bc/C/rpc",
            "chain_id": 14,
            "explorer": "https://flare-explorer.flare.network/"
        },
        "coston2": {  # Testnet
            "rpc": "https://coston2-api.flare.network/ext/bc/C/rpc",
            "chain_id": 114,
            "explorer": "https://coston2-explorer.flare.network/"
        }
    }
    
    # FTSO Registry (mainnet)
    FTSO_REGISTRY = "0xaD67FE666cFB81f1227DcC048a236c7199C94cD5"
    
    def __init__(self, network: str = "mainnet"):
        self.network = network
        self.rpc_url = self.NETWORKS[network]["rpc"]
        self.chain_id = self.NETWORKS[network]["chain_id"]
    
    def _rpc_call(self, method: str, params: List = None) -> Dict[str, Any]:
        """Make JSON-RPC call to Flare node"""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": 1
        }
        
        try:
            response = requests.post(
                self.rpc_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            
            if "error" in result:
                return {"error": result["error"]}
            
            return {"result": result.get("result")}
        
        except Exception as e:
            return {"error": str(e)}
    
    def get_block_number(self) -> Dict[str, Any]:
        """Get latest block number"""
        return self._rpc_call("eth_blockNumber")
    
    def get_balance(self, address: str) -> Dict[str, Any]:
        """Get FLR balance for address"""
        result = self._rpc_call("eth_getBalance", [address, "latest"])
        
        if "result" in result:
            # Convert from wei to FLR
            wei = int(result["result"], 16)
            flr = wei / 1e18
            return {
                "address": address,
                "balance_wei": wei,
                "balance_flr": flr
            }
        
        return result
    
    def get_gas_price(self) -> Dict[str, Any]:
        """Get current gas price"""
        result = self._rpc_call("eth_gasPrice")
        
        if "result" in result:
            wei = int(result["result"], 16)
            gwei = wei / 1e9
            return {
                "gas_price_wei": wei,
                "gas_price_gwei": gwei
            }
        
        return result
    
    def get_chain_id(self) -> Dict[str, Any]:
        """Get network chain ID"""
        return {"chain_id": self.chain_id, "network": self.network}
    
    def ping(self) -> Dict[str, Any]:
        """Test connection to Flare network"""
        block_result = self.get_block_number()
        chain_result = self.get_chain_id()
        
        if "result" in block_result:
            block_num = int(block_result["result"], 16)
            return {
                "connected": True,
                "network": self.network,
                "chain_id": self.chain_id,
                "latest_block": block_num,
                "rpc_url": self.rpc_url
            }
        
        return {
            "connected": False,
            "error": block_result.get("error", "Unknown error")
        }


class FTSOClient:
    """Flare Time Series Oracle (FTSO) client"""
    
    # Supported price feeds
    ASSETS = [
        "FLR", "SGB", "XRP", "BTC", "ETH", "DOGE", "ADA", 
        "ALGO", "LTC", "XLM", "BNB", "MATIC", "SOL", 
        "USDC", "USDT", "XDC"
    ]
    
    def __init__(self):
        self.flare = FlareClient("mainnet")
    
    def get_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get current price from FTSO
        Note: This is a simplified version. Full implementation
        requires calling the FTSORegistry contract.
        """
        symbol = symbol.upper()
        
        if symbol not in self.ASSETS:
            return {
                "error": f"Symbol {symbol} not supported",
                "supported": self.ASSETS
            }
        
        # For now, return placeholder with instructions
        # Full implementation would call:
        # FTSORegistry.getCurrentPrice(symbol)
        return {
            "symbol": symbol,
            "note": "Full FTSO integration requires web3 contract calls",
            "supported_assets": self.ASSETS,
            "registry_address": self.flare.FTSO_REGISTRY,
            "documentation": "https://docs.flare.network/"
        }


class FAssetClient:
    """F-Assets (bridged tokens) client"""
    
    # F-Asset contracts (mainnet)
    FASSETS = {
        "FXRP": {
            "address": "0x...",  # Placeholder - would need real address
            "underlying": "XRP",
            "decimals": 18
        }
    }
    
    def get_info(self, fasset: str) -> Dict[str, Any]:
        """Get F-Asset information"""
        fasset = fasset.upper()
        
        if fasset not in self.FASSETS:
            return {
                "error": f"F-Asset {fasset} not found",
                "available": list(self.FASSETS.keys())
            }
        
        return self.FASSETS[fasset]


# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Flare Network Client for Greenhead Labs")
        print("\nUsage:")
        print("  python3 flare_client.py ping [mainnet|coston2]  # Test connection")
        print("  python3 flare_client.py block                   # Get block number")
        print("  python3 flare_client.py balance <address>       # Get FLR balance")
        print("  python3 flare_client.py gas                     # Get gas price")
        print("  python3 flare_client.py fts price <symbol>      # Get FTSO price")
        print("  python3 flare_client.py chain                   # Get chain ID")
        sys.exit(0)
    
    command = sys.argv[1]
    network = "mainnet"
    
    # Check for network argument
    if len(sys.argv) > 2 and sys.argv[-1] in ["mainnet", "coston2"]:
        network = sys.argv[-1]
    
    flare = FlareClient(network)
    ftso = FTSOClient()
    
    if command == "ping":
        result = flare.ping()
        print(json.dumps(result, indent=2))
    
    elif command == "block":
        result = flare.get_block_number()
        if "result" in result:
            block = int(result["result"], 16)
            print(json.dumps({"block_number": block, "hex": result["result"]}, indent=2))
        else:
            print(json.dumps(result, indent=2))
    
    elif command == "balance" and len(sys.argv) > 2:
        address = sys.argv[2]
        result = flare.get_balance(address)
        print(json.dumps(result, indent=2))
    
    elif command == "gas":
        result = flare.get_gas_price()
        print(json.dumps(result, indent=2))
    
    elif command == "chain":
        result = flare.get_chain_id()
        print(json.dumps(result, indent=2))
    
    elif command == "fts":
        if len(sys.argv) > 3 and sys.argv[2] == "price":
            symbol = sys.argv[3]
            result = ftso.get_price(symbol)
            print(json.dumps(result, indent=2))
        else:
            print("Usage: python3 flare_client.py fts price <SYMBOL>")
            print("Supported:", ", ".join(ftso.ASSETS))
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
