# Hedera (HBAR) Technical Reference
## Enterprise-Grade Blockchain for Greenhead Labs

**Token-Optimized Quick Reference**

---

## Hedera Basics (30-sec read)

**What:** Enterprise-grade public network with hashgraph consensus  
**Speed:** 10,000+ TPS, 3-5 second finality  
**Cost:** $0.0001 fixed per transaction  
**Consensus:** Hashgraph (aBFT - asynchronous Byzantine Fault Tolerance)  
**Token:** HBAR (50B supply, no mining)

**Why Greenhead Labs Cares:**
- Governing Council = enterprise legitimacy (Boeing, IBM, Google)
- Predictable fees (critical for enterprise budgeting)
- EVM-compatible smart contracts
- Carbon-negative (environmental compliance)
- Best for: supply chain, credentials, compliance

---

## Hashgraph vs Blockchain

```
Blockchain (Bitcoin, Ethereum):
├── Blocks in linear chain
├── Miners/validators compete
├── Forks possible
└── PoW/PoS energy intensive

Hashgraph (Hedera):
├── DAG (Directed Acyclic Graph)
├── Gossip protocol (efficient)
├── No forks (100% finality)
└── aBFT mathematically proven
```

**Key Advantage:** Fair ordering + no wasted energy

---

## Core Services

### 1. Consensus Service (HCS)
```
Immutable event logs:
├── Order-Guaranteed messaging
├── Audit trails
├── Supply chain tracking
└── $0.0001 per message

Use Case: Track compliance events, AI decision logs
```

### 2. Token Service (HTS)
```
Native tokenization (no smart contracts):
├── Fungible tokens (ERC-20 like)
├── NFTs (ERC-721/1155 like)
├── KYC verification hooks
├── Fractional ownership
└── $0.001 to create, $0.0001 to transfer

Use Case: Client tokens, asset tokenization, loyalty points
```

### 3. Smart Contract Service
```
EVM-compatible (Solidity):
├── 300ms execution time
├── 1M gas per TX limit
├── HBARSYS (native oracle)
└── $0.05-0.20 per execution

Use Case: DeFi protocols, automated compliance
```

### 4. File Service
```
Immutable storage:
├── Append-only files
├── 1MB max per file
├── 48hr expiration default
└── $0.05 to create

Use Case: Credential storage, legal documents
```

---

## Governing Council (Enterprise Legitimacy)

**Current Members:**
- Google
- IBM
- Boeing
- LG
- Standard Bank
- UCL (University College London)
- Shinhan Bank
- And more...

**Why This Matters:**
- No single entity controls network
- Rotating terms prevent capture
- Enterprise credibility for clients
- Compliance-friendly structure

---

## Greenhead Labs Integration Points

### AI Audit Logging
```python
# Log AI decisions to Hedera (immutable)
from hedera import TopicMessageSubmitTransaction

tx = TopicMessageSubmitTransaction(
    topic_id="0.0.123456",
    message=json.dumps({
        "ai_decision": "approve_transaction",
        "confidence": 0.94,
        "timestamp": "2026-02-21T12:00:00Z"
    })
)
```

### Enterprise Tokenization
```
Client wants to tokenize real estate:
├── Create HTS token (compliance-enabled)
├── Set KYC requirements
├── Fractional ownership (0.000001 precision)
├── Automated dividend distribution
└── Hedera = enterprise clients trust it
```

### Compliance Automation
- Immutable audit trails (HCS)
- Regulatory reporting (predictable costs)
- Carbon footprint tracking (Hedera is carbon-negative)

---

## Development Setup

### Networks
```
Mainnet:
- Explorer: https://hashscan.io/mainnet
- Mirror Node: https://mainnet-public.mirrornode.hedera.com

Testnet:
- Explorer: https://hashscan.io/testnet
- Faucet: https://portal.hedera.com/faucet
```

### SDKs
```javascript
// JavaScript
const { Client, TransferTransaction } = require("@hashgraph/sdk");

// Python
from hedera import Client, TransferTransaction

// Go, Java, Rust also available
```

---

## Cost Structure (Predictable)

| Operation | HBAR Cost | USD (@ $0.20) |
|-----------|-----------|---------------|
| Cryptotransfer | 0.0001 | $0.00002 |
| Token create | 1.0 | $0.20 |
| Token mint | 0.001 | $0.0002 |
| Smart contract call | 0.05-0.20 | $0.01-0.04 |
| Consensus message | 0.0001 | $0.00002 |
| File create | 0.05 | $0.01 |

**Greenhead Labs Advantage:** Predictable budgeting vs Ethereum's variable gas

---

## Security Features

### aBFT Consensus
- Mathematically proven security
- 1/3 malicious nodes tolerated
- No 51% attacks possible

### Key Management
- Native multi-sig support
- Threshold keys
- Scheduled transactions

### Compliance
- Optional KYC hooks on tokens
- Freeze/unfreeze accounts
- Wipe tokens (for security tokens)

---

## Hedera vs Ethereum vs XRPL

| Feature | Hedera | Ethereum | XRPL |
|---------|--------|----------|------|
| Speed | 10K TPS | 15 TPS | 1.5K TPS |
| Finality | 3-5s | 15min | 3-5s |
| Cost | Fixed $0.0001 | Variable | $0.0002 |
| Consensus | Hashgraph | PoS | RPCA |
| Smart Contracts | EVM | EVM native | Hooks |
| Enterprise Ready | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |

---

## Greenhead Labs Strategy

**Phase 1:** Use Hedera for compliance logging (HCS)  
**Phase 2:** Tokenize client assets (HTS)  
**Phase 3:** EVM smart contracts for DeFi protocols  
**Phase 4:** Governing Council relationships for enterprise sales

---

## Resources

- **Docs:** https://docs.hedera.com/
- **Explorer:** https://hashscan.io/
- **Portal:** https://portal.hedera.com/
- **GitHub:** https://github.com/hashgraph/

---

**Diesel-Goose Knowledge Priority:** MEDIUM-HIGH  
**Usage:** Enterprise compliance, asset tokenization, audit trails  
**Last Updated:** 2026-02-21  
**Token Count:** ~1,100

🦆 **Hedera Knowledge Locked. Enterprise-grade compliance ready.**
