# Blockchain Security Best Practices
## Defense-in-Depth for Greenhead Labs

**Token-Optimized Quick Reference**

---

## Security Mindset (30-sec read)

**Assume:** Everything will be attacked  
**Rule:** Defense in depth (multiple layers)  
**Reality:** $3.8B stolen from DeFi in 2022  
**Greenhead Labs Mission:** Zero breaches, ever

**Core Principles:**
1. **Never trust, always verify** (code, people, systems)
2. **Least privilege** (minimum access needed)
3. **Fail secure** (if broken, lock down)
4. **Assume compromise** (plan for when, not if)

---

## Key Management (CRITICAL)

### Private Key Security Hierarchy
```
Tier 1: Cold Storage (HSM/air-gapped)
├── Institutional custody
├── Multi-sig required
└── Never touches internet

Tier 2: Hardware Wallets
├── Ledger, Trezor
├── Physical possession
├── PIN + passphrase
└── For large holdings

Tier 3: Hot Wallets
├── Daily operations
├── Limited funds
├── 2FA enabled
└── Separate from savings

Tier 4: Smart Contract Wallets
├── Multi-sig (Gnosis Safe)
├── Recovery mechanisms
├── Access controls
└── Corporate standard
```

### Key Generation Rules
```
✅ DO:
├── Use hardware RNG (Ledger, etc.)
├── Generate offline
├── Write seed phrase on metal/paper
├── Store in geographically separate locations
└── Test recovery process

❌ NEVER:
├── Generate keys in cloud VMs
├── Store keys in GitHub/code
├── Screenshot seed phrases
├── Email/DM keys to anyone
└── Use brain wallets
```

### Multi-Signature Setup
```
Greenhead Labs Standard:
├── 3-of-5 multisig
├── Keys held by:
│   ├── Chairman (Nathan)
│   ├── CTO (agent)
│   ├── CFO (agent)
│   ├── Legal counsel
│   └── Cold storage backup
├── Transaction limits:
│   ├── < $10K: 1-of-5
│   ├── $10K-100K: 2-of-5
│   └── > $100K: 3-of-5
└── Time delays for large TXs
```

---

## Smart Contract Security

### Development Lifecycle
```
1. Design
   ├── Threat modeling
   ├── Economic audit
   └── Invariant identification

2. Implementation
   ├── Established patterns (OpenZeppelin)
   ├── No experimental features
   └── 100% test coverage

3. Testing
   ├── Unit tests
   ├── Integration tests
   ├── Fuzzing (Echidna)
   └── Formal verification (Certora)

4. Review
   ├── Internal audit
   ├── External audit (2+ firms)
   ├── Bug bounty (Immunefi)
   └── Community review

5. Deployment
   ├── Testnet (2+ weeks)
   ├── Staging (1+ week)
   ├── Mainnet (timelock + monitoring)
   └── Incident response plan
```

### Common Vulnerabilities (OWASP for Web3)

| Vulnerability | Risk | Prevention |
|---------------|------|------------|
| Reentrancy | Critical | Checks-effects-interactions, ReentrancyGuard |
| Integer overflow | High | SafeMath, Solidity 0.8+ |
| Access control | Critical | Ownable, Role-based access |
| Oracle manipulation | High | Multiple oracles, TWAP |
| Front-running | Medium | Commit-reveal, flashbots |
| Unchecked calls | High | Always check return values |
| DoS | Medium | Gas limits, pull over push |
| Timestamp dependence | Low | Use block numbers |

### Code Example: Secure Contract
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract GreenheadVault is ReentrancyGuard, Ownable {
    // State variables first
    mapping(address => uint256) private balances;
    bool private paused;
    
    // Events
    event Deposit(address indexed user, uint256 amount);
    event Withdrawal(address indexed user, uint256 amount);
    
    // Modifiers
    modifier whenNotPaused() {
        require(!paused, "Contract paused");
        _;
    }
    
    // Functions: Checks → Effects → Interactions
    function withdraw(uint256 amount) external nonReentrant whenNotPaused {
        // CHECKS
        require(amount > 0, "Invalid amount");
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        // EFFECTS (state change before external call)
        balances[msg.sender] -= amount;
        
        // INTERACTIONS (external call last)
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        emit Withdrawal(msg.sender, amount);
    }
}
```

---

## Operational Security (OpSec)

### Infrastructure Security
```
✅ DO:
├── Separate dev/staging/prod environments
├── VPN for all access
├── 2FA everywhere (hardware keys preferred)
├── Encrypted backups (3-2-1 rule)
├── Regular penetration testing
└── Log everything (immutable storage)

❌ NEVER:
├── Use personal devices for keys
├── Share admin accounts
├── Store keys in environment variables
├── Connect to public WiFi with keys
└── Skip security updates
```

### Social Engineering Defense
```
Common Attacks:
├── Phishing emails (fake airdrops, support)
├── Fake customer support (Twitter, Discord)
├── Impersonation (fake team members)
├── Baiting (USB drops, fake software)
└── Quid pro quo ("help me, I'll help you")

Defenses:
├── Verify all requests via secondary channel
├── No private key entry in response to emails
├── Zero trust for "urgent" requests
├── Document all key access
└── Regular security training
```

### Incident Response Plan
```
1. DETECT (within 1 minute)
   ├── Monitoring alerts
   ├── Anomaly detection
   └── Community reports

2. CONTAIN (within 5 minutes)
   ├── Pause contracts
   ├── Revoke access
   └── Isolate affected systems

3. ERADICATE (within 1 hour)
   ├── Identify root cause
   ├── Patch vulnerability
   └── Verify fix

4. RECOVER (within 24 hours)
   ├── Gradual restart
   ├── Monitoring enhanced
   └── Insurance claims

5. POST-INCIDENT
   ├── Public disclosure
   ├── Root cause analysis
   ├── Process improvements
   └── Legal review
```

---

## Monitoring & Alerting

### Critical Alerts
```
Must Alert On:
├── Large withdrawals (> threshold)
├── Failed authentication attempts
├── Smart contract function calls
├── Unusual gas consumption
├── New admin roles granted
├── Price oracle deviations
└── Reentrancy attempts

Alert Channels:
├── PagerDuty (critical)
├── Telegram (high)
├── Email (medium)
└── Dashboard (all)
```

### Monitoring Tools
```
On-Chain:
├── Tenderly (real-time monitoring)
├── Forta (threat detection)
├── OpenZeppelin Defender
└── Custom scripts

Off-Chain:
├── Datadog (infrastructure)
├── Splunk (log analysis)
├── PagerDuty (incident mgmt)
└── Statuspage (communication)
```

---

## Compliance & Legal

### Regulatory Requirements
```
USA:
├── FinCEN (BSA compliance)
├── OFAC (sanctions screening)
├── SEC (securities laws)
└── State licenses (MTL, etc.)

EU:
├── MiCA (Markets in Crypto-Assets)
├── GDPR (data privacy)
└── AMLD5 (anti-money laundering)

Singapore:
├── MAS PSA (Payment Services Act)
├── AML/CFT guidelines
└── Consumer protection
```

### Documentation Requirements
```
Maintain:
├── Incident response logs
├── Access control audit trails
├── Transaction monitoring records
├── Security policy versions
├── Audit reports (external)
├── Bug bounty submissions
└── Insurance policies
```

---

## Greenhead Labs Security Stack

### Layer 1: Prevention
```
├── Multi-sig wallets (Gnosis Safe)
├── Hardware security modules (HSM)
├── Formal verification (Certora)
├── Bug bounties (Immunefi)
└── Security audits (Trail of Bits)
```

### Layer 2: Detection
```
├── Real-time monitoring (Tenderly)
├── AI anomaly detection (custom)
├── On-chain analytics (Nansen)
├── Community reporting (Discord)
└── Automated alerts (PagerDuty)
```

### Layer 3: Response
```
├── Incident response team
├── Emergency contacts (24/7)
├── Insurance coverage
├── Legal counsel (retainer)
└── Public communication plan
```

---

## Quick Security Checklist

### Daily
- [ ] Review security alerts
- [ ] Check key access logs
- [ ] Monitor social channels for scams

### Weekly
- [ ] Review access permissions
- [ ] Update threat intelligence
- [ ] Test backup recovery

### Monthly
- [ ] Security audit review
- [ ] Policy updates
- [ ] Team training

### Quarterly
- [ ] Penetration testing
- [ ] Disaster recovery drill
- [ ] Insurance review

---

## Emergency Contacts

```
Chairman (Nathan): Telegram @Greenhead_Labs
Security Team: security@greenhead.io
Legal Counsel: legal@greenhead.io
Insurance: policy@greenhead.io
Law Enforcement: FBI IC3 (if needed)
```

---

**Diesel-Goose Knowledge Priority:** CRITICAL  
**Usage:** All operations, architecture decisions  
**Last Updated:** 2026-02-21  
**Token Count:** ~1,500

🦆 **Security Knowledge Locked. Defense-in-depth active.**
