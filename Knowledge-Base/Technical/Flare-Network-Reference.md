# Flare Network Technical Reference
## Decentralized Data & Smart Contracts for Greenhead Labs

**Token-Optimized Quick Reference**

---

## Flare Basics (30-sec read)

**What:** Layer-1 blockchain with native oracles & EVM compatibility  
**Why:** Brings smart contracts to non-smart-contract chains (XRP, BTC, DOGE)  
**Speed:** ~3-5 second block times  
**Token:** FLR (governance + collateral)  
**Consensus:** Avalanche-based, federated byzantine agreement

**Greenhead Labs Use Case:**
- Decentralized price feeds for XRPL DeFi
- Cross-chain interoperability
- AI oracle verification
- State connector for external data

---

## Core Architecture

### State Connector
```
Flare's Secret Weapon:
├── Trustlessly verifies external chain states
├── E.g., "Did Bitcoin tx X confirm?"
├── No oracle intermediaries
└── Brings BTC/DOGE/XRP to smart contracts
```

**Technical Process:**
1. Attestation providers observe external chains
2. Stake FLR to make claims
3. Challenge period (7 days)
4. Majority stake wins
5. Smart contracts use verified data

### Flare Time Series Oracle (FTSO)
```
Decentralized Price Feeds:
├── 100+ data providers
├── Submit price estimates every 3 minutes
├── Median calculation (outliers removed)
├── Rewards for accuracy
└── Penalties for manipulation
```

**Supported Assets:** FLR, SGB, XRP, BTC, ETH, DOGE, ADA, ALGO, LTC, XLM, BNB, MATIC, SOL, USDC, USDT, XDC

### F-Assets
```
Bridging Non-Smart-Contract Assets:
XRP (on XRPL) → FXRP (on Flare) → Use in DeFi
├── Backed by FLR collateral
├── Mint/burn mechanism
├── Redeemable 1:1
└── Enables XRP in smart contracts
```

---

## EVM Compatibility

### Solidity Support
```solidity
// Standard Solidity works on Flare
pragma solidity ^0.8.0;

contract FlareExample {
    // Access FTSO prices
    IFtsoRegistry ftsoRegistry;
    
    function getXRPPrice() external view returns (uint256) {
        (uint256 price, ) = ftsoRegistry.getCurrentPrice("XRP");
        return price;
    }
}
```

### Key Differences from Ethereum
- **Gas token:** FLR
- **Block time:** ~3-5s (vs 12s Ethereum)
- **Finality:** ~1-2s (vs 15min Ethereum)
- **Oracles:** Native (no Chainlink needed)

---

## Greenhead Labs Integration Points

### AI-Powered Price Prediction
```
Diesel-Goose AI → Analyze FTSO data
                    ↓
              Predict price movements
                    ↓
            Flare smart contract execution
```

### Cross-Chain Automation
```
XRPL Payment Detected (State Connector)
           ↓
    Flare Smart Contract Triggered
           ↓
    Execute ETH/AVAX Transaction
```

### Decentralized Data Verification
- Verify XRPL transactions for Greenhead clients
- Cross-reference multiple data sources
- AI-based anomaly detection

---

## Development Setup

### Networks
```
Mainnet:
- Chain ID: 14
- RPC: https://flare-api.flare.network/ext/bc/C/rpc

Testnet (Coston2):
- Chain ID: 114
- RPC: https://coston2-api.flare.network/ext/bc/C/rpc
```

### Key Contracts
```javascript
// FTSO Registry
const ftsoRegistry = "0xaD67FE666cFB81f1227DcC048a236c7199C94cD5";

// State Connector
const stateConnector = "0xbcEecF535e7C3fc272512722A9e5b13D765F92A1";

// F-Asset Manager
const fAssetManager = "0x..."; // Asset-specific
```

---

## Security Model

### Attestation Provider Risks
- **Collusion:** 50%+ stake can attack
- **Latency:** Slow finality for state connector
- **Cost:** 7-day challenge period

### FTSO Risks
- **Price manipulation:** Brief spikes during sampling
- **Provider centralization:** Top 10 control majority

### Mitigation
```
✅ Use median prices (not single oracle)
✅ Implement circuit breakers
✅ Multi-block confirmation
✅ AI anomaly detection layer
```

---

## Cost Structure

| Operation | FLR Cost | USD Estimate |
|-----------|----------|--------------|
| Simple TX | 0.001 | $0.0001 |
| Contract deploy | 0.5-2 | $0.05-0.20 |
| FTSO query | 0.0005 | $0.00005 |
| State connector | Variable | Depends on complexity |

---

## Comparison: Flare vs Chainlink

| Feature | Flare (Native) | Chainlink (External) |
|---------|----------------|---------------------|
| Oracles | Built-in | Separate integration |
| Cost | Lower | Higher |
| Decentralization | 100+ providers | Varies by feed |
| Speed | 3min updates | Varies |
| EVM | Native | Any chain |

---

## Quick Resources

- **Docs:** https://docs.flare.network/
- **Explorer:** https://flare-explorer.flare.network/
- **FTSO Monitoring:** https://flaremetrics.io/
- **GitHub:** https://github.com/flare-foundation/

---

## Greenhead Labs Strategy

**Phase 1:** Monitor FTSO for XRP price signals  
**Phase 2:** Build F-Asset integration for XRPL clients  
**Phase 3:** AI-powered state connector verification  
**Phase 4:** Cross-chain treasury management

**Diesel-Goose Knowledge Priority:** HIGH  
**Usage:** Oracle data, cross-chain automation, price feeds  
**Last Updated:** 2026-02-21  
**Token Count:** ~1,000

🦆 **Flare Knowledge Locked. Cross-chain intelligence active.**
