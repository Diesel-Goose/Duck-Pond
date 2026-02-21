# Web3 & DeFi Fundamentals
## Core Concepts for Greenhead Labs Operations

**Token-Optimized Quick Reference**

---

## Web3 Basics (30-sec read)

**What:** Decentralized internet built on blockchain  
**Web1:** Read-only (static pages)  
**Web2:** Read-write (social media, platforms own data)  
**Web3:** Read-write-own (users own assets/data)

**Key Principles:**
1. **Ownership:** Users own wallets, assets, data
2. **Permissionless:** No gatekeepers
3. **Trustless:** Code = law (smart contracts)
4. **Composability:** Money legos (DeFi)

**Why Greenhead Labs Cares:**
- Financial infrastructure without intermediaries
- Automated, trustless systems
- Global, 24/7 markets
- AI + blockchain = autonomous finance

---

## DeFi (Decentralized Finance)

### Core Primitives

| Primitive | Traditional | DeFi Equivalent | Protocols |
|-----------|-------------|-----------------|-----------|
| Exchange | NYSE, Nasdaq | DEX | Uniswap, dYdX, XRPL DEX |
| Lending | Banks | Lending pools | Aave, Compound |
| Stablecoins | Bank deposits | Crypto-pegged | USDC, USDT, DAI |
| Derivatives | CME, CBOE | Perp swaps | dYdX, GMX |
| Insurance | Insurance cos | Coverage pools | Nexus Mutual |
| Asset mgmt | ETFs | Index funds | Index Coop |

### Key Mechanisms

**AMM (Automated Market Maker):**
```
No order books. Liquidity pools instead.
X * Y = K (constant product formula)

Pool: 100 ETH + 200,000 USDC (K = 20,000,000)
Trade: Buy 1 ETH
New: 99 ETH + 202,020 USDC (K still = 20,000,000)
Price impact: Slippage based on trade size
```

**Liquidity Mining:**
- Provide liquidity → Earn fees + tokens
- Risk: Impermanent loss

**Yield Farming:**
- Move assets between protocols
- Maximize APY (Annual Percentage Yield)
- Risk: Smart contract bugs, rug pulls

---

## Greenhead Labs DeFi Applications

### AI-Powered Market Making
```
Traditional: Human traders, high latency
Greenhead: AI agents, real-time on-chain
├── Monitor order flow
├── Predict price movements
├── Auto-adjust positions
└── Risk management 24/7
```

### Cross-Chain Arbitrage
```
XRPL: XRP @ $0.60
Ethereum: FXRP @ $0.605
Flare: FXRP @ $0.598

AI detects → Executes → Profits
```

### Treasury Management
- Automated yield optimization
- Multi-sig security
- Real-time risk monitoring
- Compliance reporting

---

## Wallet & Key Management

### Wallet Types

| Type | Examples | Use Case |
|------|----------|----------|
| Hot (software) | MetaMask, XUMM | Daily transactions |
| Cold (hardware) | Ledger, Trezor | Long-term storage |
| Multisig | Gnosis Safe | Corporate treasury |
| Smart contract | Argent, Loopring | Social recovery |

### Key Security (CRITICAL)
```
✅ NEVER: Store keys in code
✅ NEVER: Share private keys
✅ NEVER: Store seed phrases digitally
✅ ALWAYS: Use environment variables
✅ ALWAYS: Hardware wallets for large amounts
✅ ALWAYS: Multi-sig for operations

Diesel-Goose Rule: No key touches cloud storage
```

---

## Smart Contract Security

### Common Vulnerabilities

| Attack | Description | Prevention |
|--------|-------------|------------|
| Reentrancy | Recursive calls drain funds | Checks-effects-interactions |
| Flash loans | Borrow → Attack → Repay in 1 block | Price oracles, time delays |
| Oracle manipulation | Fake price feeds | Multiple oracles, TWAP |
| Front-running | MEV extraction | Commit-reveal schemes |
| Integer overflow | Math errors | SafeMath, Solidity 0.8+ |

### Greenhead Labs Security Stack
```
1. Static analysis (Slither, Mythril)
2. Formal verification (Certora)
3. Bug bounties (Immunefi)
4. Audits (Trail of Bits, OpenZeppelin)
5. Insurance (Nexus Mutual)
6. Monitoring (Tenderly, Forta)
```

---

## Tokenomics

### Token Types

**Utility Tokens:**
- Access to service
- Governance rights
- Example: UNI (Uniswap), FLR (Flare)

**Security Tokens:**
- Represent real-world assets
- Subject to securities laws
- Example: Tokenized real estate

**Governance Tokens:**
- Voting rights in DAOs
- Protocol parameter changes
- Example: MKR (MakerDAO)

**Stablecoins:**
| Type | Mechanism | Examples | Risk |
|------|-----------|----------|------|
| Fiat-backed | 1:1 USD reserves | USDC, USDT | Custodial |
| Crypto-backed | Overcollateralized | DAI | Liquidation |
| Algorithmic | Seigniorage shares | (Failed projects) | Death spiral |

---

## Gas & Transaction Economics

### Gas Concepts
```
Gas = Computational cost
Gas Price = Cost per unit (in gwei)
Total Fee = Gas Used × Gas Price

Ethereum Example:
- Simple transfer: 21,000 gas
- Gas price: 20 gwei
- Fee: 21,000 × 20 = 420,000 gwei = 0.00042 ETH
```

### Layer 2 Solutions
| L2 | Type | Speed | Cost | Security |
|----|------|-------|------|----------|
| Arbitrum | Optimistic Rollup | Fast | Low | Ethereum |
| Optimism | Optimistic Rollup | Fast | Low | Ethereum |
| zkSync | ZK-Rollup | Fastest | Lowest | Ethereum |
| Polygon | Sidechain | Fast | Very Low | Separate |

---

## AI + Web3 Integration

### Decentralized AI
```
Problem: Centralized AI (OpenAI) has control
Solution: Decentralized AI networks
├── Bittensor: Incentivized ML
├── Fetch.ai: Autonomous agents
├── Ocean Protocol: Data marketplaces
└── Greenhead Labs: AI on local hardware
```

### Greenhead Labs Architecture
```
Local AI (Mac Mini M4)
├── Ollama (free inference)
├── Duck Pond (local storage)
├── XRPL/Flare/Hedera integration
└── No cloud dependency
```

---

## Regulatory Landscape

### Key Regulations
| Region | Regulation | Impact |
|--------|------------|--------|
| USA | SEC securities laws | Token classification |
| EU | MiCA (2024) | Licensing requirements |
| UK | FCA guidance | Consumer protection |
| Singapore | MAS framework | Institutional clarity |

### Greenhead Labs Compliance
```
✅ KYC/AML for fiat on-ramps
✅ Securities law review for tokens
✅ Tax reporting automation
✅ Audit trails (Hedera HCS)
✅ Wyoming DAO-friendly structure
```

---

## Quick Resources

- **DeFi Llama:** https://defillama.com/ (TVL tracking)
- **Dune Analytics:** https://dune.com/ (On-chain data)
- **CoinGecko:** https://coingecko.com/ (Prices)
- **Rekt News:** https://rekt.news/ (Hack postmortems)

---

**Diesel-Goose Knowledge Priority:** CRITICAL  
**Usage:** All operations, DeFi strategies, security  
**Last Updated:** 2026-02-21  
**Token Count:** ~1,400

🦆 **Web3 Knowledge Locked. DeFi-native intelligence active.**
