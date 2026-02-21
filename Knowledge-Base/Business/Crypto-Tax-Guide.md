# Cryptocurrency Tax Guide
## Compliance & Reporting for Greenhead Labs

**Token-Optimized Quick Reference**

---

## Tax Basics (30-sec read)

**IRS Classification:** Property (not currency)  
**Tax Events:** Any disposal (sell, trade, spend, earn)  
**Record Keeping:** All transactions, cost basis, dates  
**Penalties:** Up to 20% accuracy penalty + interest  
**Greenhead Labs:** Must report all activity, maintain audit trail

---

## Taxable Events

### ALWAYS Taxable
```
✅ Selling crypto for fiat (USD)
✅ Trading crypto for crypto (BTC → ETH)
✅ Spending crypto on goods/services
✅ Receiving crypto as income (payment, mining, staking)
✅ Hard fork proceeds (if you control new coin)
✅ Airdrops (if you have dominion/control)
```

### NOT Taxable (usually)
```
❌ Buying crypto with fiat (USD → BTC)
❌ Transferring between your own wallets
❌ Holding (unrealized gains)
❌ Donating to qualified charity
❌ Gifting (under $17K/year limit)
```

---

## Cost Basis Methods

### FIFO (First In, First Out)
```
Default IRS method
Sell oldest coins first

Example:
Buy 1 BTC @ $20,000 (Jan)
Buy 1 BTC @ $40,000 (Mar)
Sell 1 BTC @ $50,000 (Jun)

FIFO: Sold the Jan BTC
Gain: $50,000 - $20,000 = $30,000
```

### LIFO (Last In, First Out)
```
May reduce taxes in rising markets
Requires specific identification

Same example:
LIFO: Sold the Mar BTC
Gain: $50,000 - $40,000 = $10,000
(Tax savings: $20K less gain)
```

### HIFO (Highest In, First Out)
```
Maximize losses / minimize gains
Best for tax optimization

Same example:
HIFO: Sold the $40K BTC (higher cost)
Gain: $50,000 - $40,000 = $10,000
```

### Specific Identification
```
Choose which specific coins to sell
Must have detailed records
Must identify BEFORE sale

Greenhead Strategy: Use HIFO for optimization
Software: Track lot-level data
```

---

## Income Tax (Ordinary Income)

### Mining Income
```
Fair market value when received
Self-employment tax if business
Deductible expenses:
├── Equipment (depreciated)
├── Electricity
├── Internet
├── Space (if dedicated)
└── Pool fees

Example:
Mine 0.1 BTC when BTC = $50,000
Income: $5,000 (reported as ordinary income)
```

### Staking Rewards
```
Fair market value when received
Ordinary income rate
New IRS guidance (2023): Recognize when in control

Example:
Stake ETH, receive 0.5 ETH reward
ETH price: $3,000
Income: $1,500
```

### Payment for Services
```
FMV of crypto when received
Report on 1099-NEC (if >$600)
Self-employment tax applies

Example:
Invoice: $10,000
Paid: 0.2 BTC when BTC = $50,000
Income: $10,000
```

### Airdrops & Hard Forks
```
Taxable when you have dominion/control
FMV at that moment

Example:
Hold BTC, receive BCH airdrop
BCH price: $300 when received
Income: $300
```

---

## Capital Gains Tax

### Short-Term (< 1 year)
```
Ordinary income tax rates
10% - 37% (federal)

Example:
Buy BTC @ $40,000 (Jan 1)
Sell BTC @ $50,000 (Jun 1)
Gain: $10,000 (short-term)
Tax: Up to $3,700 (37% bracket)
```

### Long-Term (> 1 year)
```
Preferential rates
0% - 20% (federal)
+ 3.8% NIIT (high income)

2024 Rates:
├── 0%: $0 - $47,025 (single)
├── 15%: $47,026 - $518,900
└── 20%: $518,901+

Same example (held > 1 year):
Tax: $1,500 (15% bracket)
Savings: $2,200 vs short-term
```

### Wash Sale Rule
```
⚠️ 2024 UPDATE: Wash sales NOW apply to crypto

Rule: Can't claim loss if you rebuy within 30 days
Before: Crypto exempt (loophole)
After: Same as stocks

Example:
Sell BTC at loss: -$10,000
Rebuy BTC 10 days later
Result: Loss disallowed (added to basis)

Strategy: Harvest losses carefully, wait 31 days
```

---

## DeFi Tax Complexity

### Liquidity Pools
```
Adding liquidity: Not taxable (like deposit)
LP tokens received: Track cost basis

Removing liquidity: Taxable event
Gain/loss = (value received) - (cost basis)

Impermanent Loss: Realized when exiting pool
```

### Yield Farming
```
Rewards: Ordinary income when received
Token appreciation: Capital gain when sold

Example:
Day 1: Farm generates 100 tokens @ $1 = $100 income
Day 30: Tokens worth $2 each
Day 30 sale: $200 proceeds
Capital gain: $200 - $100 = $100

Total income: $100 (ordinary) + $100 (capital gain)
```

### Lending/Borrowing
```
Lending crypto: Not taxable (like deposit)
Interest received: Ordinary income

Borrowing crypto: Not taxable (loan)
Using borrowed funds: Not taxable
Liquidation: Taxable if collateral sold
```

### NFTs
```
Buying NFT: Not taxable (establishes basis)
Selling NFT: Capital gain/loss
Creating NFT: Not taxable
Selling created NFT: Ordinary income (if business)

Wash sale rules apply
```

---

## Record Keeping Requirements

### Minimum Documentation
```
For EACH transaction:
├── Date acquired
├── Date sold/disposed
├── Proceeds (USD value)
├── Cost basis (USD value)
├── Gain/loss amount
└── Transaction ID/hash
```

### Recommended Tools
```
Commercial:
├── CoinTracker (best for DeFi)
├── Koinly (international support)
├── TaxBit (enterprise)
├── TokenTax (CPA review)

DIY:
├── Excel/Sheets with API feeds
├── Python scripts (Duck-Pond)
└── Exchange exports (CSV)
```

### Retention
```
Keep records for:
├── 7 years (IRS statute of limitations)
├── Permanently (cost basis tracking)
└── Blockchain records (immutable backup)
```

---

## Greenhead Labs Compliance Stack

### Quarterly Reviews
```
1. Export all transactions
2. Calculate gains/losses
3. Review cost basis method
4. Identify optimization opportunities
5. Estimated tax payments
```

### Annual Filing
```
Forms:
├── 8949: Sales and dispositions
├── Schedule D: Capital gains summary
├── Schedule C: Mining/business income
├── Schedule 1: Other income
└── 1040: Main return

Deadlines:
├── April 15: Individual filing
├── June/Sept/Jan: Estimated payments
└── Oct 15: Extension deadline
```

### Audit Defense
```
Documentation:
├── Complete transaction history
├── Exchange statements
├── Wallet addresses owned
├── Cost basis calculations
└⃣ Third-party valuations

Red Flags to Avoid:
├── Unreported income
├── Missing cost basis
├── Unreasonable positions
└⃣ Cash transactions >$10K
```

---

## Tax Optimization Strategies

### 1. Long-Term Holding
```
Hold > 1 year for lower rates
0% bracket: Up to $47K taxable income
Plan sales around income levels
```

### 2. Tax-Loss Harvesting
```
Sell losers to offset gains
Buy different (not same) asset
Avoid wash sale (30-day rule)

Example:
$50K gains, $30K losses
Net gain: $20K (tax on $20K vs $50K)
```

### 3. Qualified Opportunity Zones
```
Defer capital gains
Invest in designated zones
Reduce tax on future gains
Complex: Consult tax pro
```

### 4. Charitable Giving
```
Donate appreciated crypto
No capital gains tax
Full FMV deduction
Better than cash gifts

Example:
Donate BTC worth $50K (basis $10K)
Deduction: $50K
Avoid tax on $40K gain
Cash savings: ~$12K (30% bracket)
```

### 5. Self-Directed IRA
```
Invest crypto in IRA
Tax-deferred growth
Roth: Tax-free withdrawals
Restrictions apply
```

---

## State & International

### State Tax Considerations
```
Some states tax crypto differently:
├── No income tax: TX, FL, NV, WA, WY, SD, AK, TN, NH
├── High tax: CA, NY, NJ, HI
└── Greenhead: Wyoming (favorable)
```

### International Reporting
```
FBAR: Report foreign accounts >$10K
FATCA: Report foreign assets >$50K
Penalties: Severe for non-compliance
```

---

## Penalties & Enforcement

### Common Penalties
```
Failure to file: 5% per month (max 25%)
Failure to pay: 0.5% per month
Accuracy: 20% of underpayment
Fraud: 75% of underpayment
Criminal: Jail time (tax evasion)
```

### IRS Enforcement Trends
```
Increased focus on crypto:
├── John Doe summons (exchange data)
├── Blockchain analytics contracts
├── Question on Form 1040
└── Criminal prosecutions increasing

Best Practice: Report everything, be conservative
```

---

## Quick Reference

| Event | Tax Treatment | Form |
|-------|---------------|------|
| Buy crypto | Not taxable | Track basis |
| Sell for fiat | Capital gain | 8949 |
| Trade crypto | Capital gain | 8949 |
| Mining income | Ordinary income | Schedule C |
| Staking rewards | Ordinary income | Schedule 1 |
| Airdrops | Ordinary income | Schedule 1 |
| Hard forks | Ordinary income | Schedule 1 |
| DeFi yields | Ordinary income | Schedule 1 |
| NFT sales | Capital gain | 8949 |

---

**Diesel-Goose Knowledge Priority:** HIGH  
**Usage:** All financial operations, compliance  
**Last Updated:** 2026-02-21  
**Token Count:** ~1,400

⚠️ **Disclaimer: Not tax advice. Consult CPA for specific situations.**

🦆 **Tax knowledge locked. Compliance protocols active.**
