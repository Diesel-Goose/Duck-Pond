# XRPL/XRP Technical Reference
## Essential Knowledge for Greenhead Labs Operations

**Token-Optimized Quick Reference** — For Local LLM Fast Retrieval

---

## XRPL Basics (30-sec read)

**What:** XRP Ledger — decentralized blockchain for payments  
**Speed:** 3-5 second finality, 1,500 TPS  
**Cost:** $0.0002 average transaction fee  
**Consensus:** Unique Node List (UNL), not PoW/PoS  
**Token:** XRP (pre-mined, 100B supply, deflationary via burn)

**Why Greenhead Labs Cares:**
- Institutional-grade payments infrastructure
- Built-in DEX (decentralized exchange)
- Tokenization native (IOUs, NFTs)
- Regulatory clarity progressing
- Ripple relationships = enterprise access

---

## Core Technical Concepts

### Consensus Protocol
```
Ripple Protocol Consensus Algorithm (RPCA)
├── Validators propose transactions
├── UNL (Unique Node List) — trusted validators
├── 80% agreement = consensus
└── No mining = energy efficient
```

**Key Point:** 3-5 seconds to finality vs Bitcoin's 10 minutes

### Account Model
```
XRPL Account = Public Key + Sequence Number + Balance
├── Address: rN7n7otQDd6FczFgLdlqtyMVrn3HMfHgFj
├── Requires 10 XRP reserve (base)
├── +2 XRP per trust line
└── +5 XRP per offer
```

### Transaction Types (Greenhead Labs Use Cases)

| Type | Purpose | Use Case |
|------|---------|----------|
| Payment | Send XRP/IOUs | Cross-border settlement |
| OfferCreate | DEX order | Automated market making |
| OfferCancel | Cancel order | Risk management |
| TrustSet | Establish trust line | Token custody |
| EscrowCreate | Time-locked funds | Treasury management |
| PaymentChannel | Off-chain payments | High-frequency micro-payments |

---

## DEX & Liquidity

### Built-in Decentralized Exchange
- **Order books:** XRP/IOU pairs
- **Auto-bridging:** XRP automatically bridges IOU trades
- **Tick size:** Minimum price movement
- **Transfer fees:** Issuer can charge up to 100%

**Greenhead Labs Applications:**
- AI-powered market making
- Arbitrage detection
- Liquidity optimization
- Token issuance for clients

### Pathfinding
```
XRP Ledger automatically finds best payment path:
Sender → [Path A: XRP→USD→EUR] → Receiver
       [Path B: XRP→BTC→EUR]     (compared)
       [Path C: Direct XRP→EUR]   (selected)
```

---

## Tokenization on XRPL

### Issued Currencies (IOUs)
```
Issuer creates: USD.Gatehub
├── Trust line required (2 XRP reserve)
├── Transfer fees configurable
├── Freeze capability
└── Clawback (new feature)
```

### NFTs (XLS-20)
- Native NFT support (no smart contracts needed)
- Mint cost: ~12 XRP
- Transferrable, burnable, taxable
- Ideal for: tickets, collectibles, credentials

---

## APIs & Integration

### rippled (Node Software)
- JSON-RPC / WebSocket APIs
- Full history vs. pruned nodes
- Validator vs. stock node

### xrpl.js / xrpl-py
```python
from xrpl.clients import JsonRpcClient
client = JsonRpcClient("https://s1.ripple.com:51234")
```

### Key Libraries
- **xrpl.js:** JavaScript/TypeScript
- **xrpl-py:** Python
- **ripple-lib:** Legacy (deprecated)

---

## Security Considerations

### Account Security
- **Never:** Store secret keys in code
- **Always:** Use environment variables or HSM
- **Reserves:** Maintain 10+ XRP minimum
- **Multi-sign:** Use for high-value accounts

### Common Vulnerabilities
1. **Reusable nonces** — Always increment sequence
2. **Insufficient reserves** — Account becomes unusable
3. **Trust line spam** — Costs 2 XRP each
4. **DEX manipulation** — Oracle manipulation risks

### Best Practices
```
✅ Use Payment Channels for micro-transactions
✅ Set TrustSet flags (NoRipple, Freeze)
✅ Monitor Offers (auto-cancel expired)
✅ Implement transaction queuing
✅ Use testnet for development
```

---

## Greenhead Labs AI Applications

### Automated Trading
```python
# AI signal → XRPL execution
if ai_model.predict() == "buy":
    tx = OfferCreate(
        taker_gets=xrp_to_drops(100),
        taker_pays=issued_currency(50, "USD", issuer)
    )
```

### Treasury Management
- Escrow for vesting schedules
- Payment channels for payroll
- Multi-sign for board approval

### Compliance Automation
- Monitor transaction patterns
- AML risk scoring
- Automated reporting

---

## Quick Commands

```bash
# Check account balance
xrpl-account-info rN7n7otQDd6FczFgLdlqtyMVrn3HMfHgFj

# Monitor ledger
ws://s1.ripple.com:51233 (WebSocket)

# Testnet faucet
https://test.bithomp.com/

# Explorer
https://bithomp.com/ | https://xrpscan.com/
```

---

## Cost-Efficiency Metrics

| Operation | Cost (XRP) | Cost (USD @ $0.60) |
|-----------|------------|-------------------|
| Payment | 0.00001 | $0.000006 |
| Offer | 0.00001 | $0.000006 |
| TrustSet | 0.00001 | $0.000006 |
| Account create | 10 (reserve) | $6.00 |
| NFT mint | ~12 | $7.20 |

---

## Resources

- **Docs:** https://xrpl.org/
- **Testnet:** https://testnet.xrpl.org/
- **GitHub:** https://github.com/XRPLF/
- **Dev Discord:** xrpldevs.org

---

**Diesel-Goose Knowledge Priority:** HIGH  
**Usage:** AI automation, institutional integrations, payment infrastructure  
**Last Updated:** 2026-02-21  
**Token Count:** ~1,200 (optimized for Ollama fast retrieval)

🦆 **XRPL Knowledge Locked. Ready for billion-scale operations.**
