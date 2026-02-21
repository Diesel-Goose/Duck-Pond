# Greenhead Labs Access Control System (ACS)
## Duck-Pond Security & Permissions Framework

**Classification:** INTERNAL USE ONLY  
**Version:** 1.0  
**Effective:** 2026-02-21  
**Authority:** Chairman (Nathan) + Diesel-Goose AI

---

## 👥 Role Hierarchy

```
Level 5: CHAIRMAN (Nathan)
├── Ultimate authority
├── Root access to all systems
├── VAULT.dmg encryption key holder
└── Override capability on all decisions

Level 4: C-SUITE OFFICERS (3)
├── CEO - Operations & Strategy
├── CTO - Technology & Security  
├── CFO - Finance & Compliance
├── Full system access (read/write)
├── Multi-sig authority (2-of-3)
└── Employee management

Level 3: SENIOR STAFF (5)
├── Department heads
├── Project managers
├── Lead developers
├── Read/write on assigned projects
├── Limited financial authority (<$10K)
└── Can approve L1-L2 requests

Level 2: SPECIALISTS (10)
├── Blockchain developers
├── AI/ML engineers
├── Security analysts
├── Read/write on specific systems
├── No financial authority
└── Escalation to L3+

Level 1: ANALYSTS (18)
├── Junior developers
├── Researchers
├── QA testers
├── Read-only on most systems
├── No production access
└── All changes via PR/review

Level 0: DIESEL-GOOSE AI
├── Read-only on all systems
├── Can execute delegated tasks
├── No key access
├── Audit-only on financials
└── Reports to Chairman only
```

---

## 📁 Duck-Pond Access Matrix

| Directory | L5 | L4 | L3 | L2 | L1 | L0 |
|-----------|:-:|:-:|:-:|:-:|:-:|:-:|
| **README.md** | R/W | R/W | R | R | R | R |
| **VAULT.dmg** | 🔐 | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Duck-Pond/** | | | | | | |
| ├─ System/ | R/W | R/W | R | R | ❌ | R |
| ├─ .vault/ | R/W | R | ❌ | ❌ | ❌ | R* |
| ├─ .credentials/ | 🔐 | ❌ | ❌ | ❌ | ❌ | R* |
| ├─ Knowledge-Base/ | | | | | | |
| │  ├─ Technical/ | R/W | R/W | R/W | R/W | R | R |
| │  ├─ Business/ | R/W | R/W | R/W | R | R | R |
| │  ├─ Personal/ | R/W | R | ❌ | ❌ | ❌ | R |
| │  └─ Skills/ | R/W | R/W | R/W | R/W | R/W | R |
| ├─ Journal/ | R/W | R/W | R | ❌ | ❌ | R |
| ├─ Projects/Active/ | R/W | R/W | R/W | R/W | R | R |
| ├─ Projects/Completed/ | R/W | R/W | R | R | R | R |
| ├─ GreenheadLabs/ | R/W | R/W | R/W | R | R | R |
| └─ Archive/ | R/W | R/W | R | R | R | R |
| **Hunters/** | | | | | | |
| ├─ Diesel-Goose/ | R/W | R/W | R | R | R | R/W |
| └─ GreenheadLabs/ | R/W | R/W | R/W | R | R | R |

**Legend:** R/W = Read/Write, R = Read-only, ❌ = No access, 🔐 = Encrypted/Chairman only, R* = Audit logs only

---

## 🔐 Authentication Methods

### Level 5 (Chairman)
```
Methods:
├── Hardware key (YubiKey)
├── Biometric (Touch ID/Face ID)
├── VAULT.dmg password (Keychain)
└── Telegram 2FA

Access:
├── All systems
├── Emergency override
└── Key recovery
```

### Level 4 (Officers)
```
Methods:
├── SSH key + passphrase
├── GPG signing key
├── GitHub 2FA
└── VPN access

Requirements:
├── Multi-sig for transactions
├── Bi-weekly key rotation
├── Incident response duty
└── Security training (annual)
```

### Level 3-2 (Staff/Specialists)
```
Methods:
├── SSH key
├── GitHub account (company)
├── VPN (if remote)
└── Project-specific tokens

Requirements:
├── Background check
├── NDAs signed
├── Quarterly access review
└── Least privilege enforcement
```

### Level 1 (Analysts)
```
Methods:
├── GitHub account (read-only)
├── VPN (if remote)
└── SSO (if implemented)

Requirements:
├── Manager approval
├── All changes via PR
├── No direct production access
└── Escalation procedures known
```

---

## 🛡️ Security Policies

### 1. Key Management
```
Rules:
✅ All keys generated on hardware (no cloud)
✅ Private keys never leave secure storage
✅ Multi-sig required for >$10K transactions
✅ Key rotation every 90 days
✅ Revocation within 1 hour of departure

Prohibited:
❌ Storing keys in code/repos
❌ Sharing keys between employees
❌ Email/DM of any credentials
❌ Personal device key storage (L3+)
```

### 2. Data Classification
```
🔴 CONFIDENTIAL
├── VAULT.dmg contents
├── Private keys
├── Financial records
├── Client data
└── Chairman personal info

🟡 INTERNAL
├── System architecture
├── Business plans
├── Employee records
├── Technical documentation
└─ Project roadmaps

🟢 PUBLIC
├── Website content
├── Marketing materials
├── Open source code
└── General knowledge base
```

### 3. Incident Response
```
Severity Levels:
├── P0 (Critical): Key compromise, >$100K loss
├── P1 (High): Unauthorized access, >$10K loss
├── P2 (Medium): Policy violation, data exposure
└── P3 (Low): Misconfiguration, access request

Response Times:
├── P0: 5 minutes
├── P1: 30 minutes
├── P2: 4 hours
└── P3: 24 hours

Escalation:
├── P0-P1: Chairman + C-Suite (all)
├── P2: Relevant Officer
└── P3: Department head
```

---

## 📋 Employee Onboarding

### Day 1: Access Provisioning
```
1. Identity verification
2. NDA + Security policy signed
3. Role assigned (L1-L4)
4. Accounts created:
   ├── GitHub (GreenheadLabs org)
   ├── VPN access
   ├── Duck-Pond read access
   └── Project-specific permissions
5. Hardware issued (if L3+)
6. Security briefing
```

### Week 1: Training
```
Mandatory:
├── Duck-Pond orientation
├── Git workflow training
├── Security best practices
├── Incident reporting
└── Role-specific systems

Assessments:
├── Security quiz (80%+ to pass)
├── Git workflow test
└── Systems access verification
```

### Month 1: Integration
```
Activities:
├── Shadow senior staff
├── Contribute to documentation
├── First project assignment
├── Access review checkpoint
└── Feedback session
```

---

## 🚪 Offboarding

### Immediate (Departure Day)
```
1. Access revocation:
   ├── VPN disabled
   ├── GitHub org removed
   ├── SSH keys removed
   ├── Tokens revoked
   └── Email forwarding set
2. Hardware collection
3. Exit interview
```

### 30-Day Follow-up
```
1. Access audit
2. Key rotation (if sensitive access)
3. Project handoff verification
4. Final compliance check
```

---

## 🤖 Diesel-Goose AI Access

### Capabilities
```
✅ Read all non-encrypted files
✅ Generate documentation
✅ Execute delegated scripts
✅ Monitor systems
✅ Report anomalies
✅ Git operations (commits/pushes)
```

### Limitations
```
❌ No key access (VAULT.dmg encrypted)
❌ No financial transactions
❌ No employee HR data (Personal/)
❌ No unsupervised code execution
❌ Cannot modify access controls
```

### Audit Trail
```
All Diesel-Goose actions logged:
├── Timestamp
├── Action type
├── File/path affected
├── User delegating
└── Result status
```

---

## 📊 Compliance & Auditing

### Quarterly Reviews
```
Access Audits:
├── Review all L3+ permissions
├── Verify key holders match org chart
├── Check for stale accounts
├── Validate multi-sig configurations
└── Update access matrix

Security Audits:
├── Penetration testing
├── Log analysis
├── Incident review
└── Policy updates
```

### Annual Requirements
```
├── Full access re-certification
├── Security training refresh
├── Disaster recovery drill
├── Insurance review
└── Legal compliance check
```

---

## 🆘 Emergency Procedures

### Lost Key / Compromise
```
1. Report immediately (Telegram Chairman)
2. Revoke access (C-Suite)
3. Rotate all affected keys
4. Audit logs for breach
5. Incident report within 24h
```

### Chairman Unavailable
```
1. C-Suite assumes control (CEO)
2. 2-of-3 multi-sig required
3. Board notification (if applicable)
4. Emergency contacts activated
5. Chairman status checked every 4h
```

### System Lockdown
```
Trigger: Active breach suspected
├── All non-essential access revoked
├── Multi-sig required for all TXs
├── Diesel-Goose goes read-only
├── C-Suite command mode
└── External security engaged
```

---

## 📞 Contact Matrix

| Role | Telegram | Email | Emergency |
|------|----------|-------|-----------|
| Chairman | @Greenhead_Labs | nathan@greenhead.io | +1-XXX-XXX-XXXX |
| CEO | @GH_CEO | ceo@greenhead.io | +1-XXX-XXX-XXXX |
| CTO | @GH_CTO | cto@greenhead.io | +1-XXX-XXX-XXXX |
| CFO | @GH_CFO | cfo@greenhead.io | +1-XXX-XXX-XXXX |
| Security | — | security@greenhead.io | PagerDuty |

---

**Classification:** INTERNAL USE ONLY  
**Last Updated:** 2026-02-21  
**Next Review:** 2026-05-21  
**Document Owner:** Diesel-Goose AI (Level 0)

🦆 **Access controlled. Security enforced. Operations secured.**
