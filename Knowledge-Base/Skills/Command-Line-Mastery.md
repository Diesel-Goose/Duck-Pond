# Command Line Mastery
## Duck-Pond CLI Reference

**Quick commands for Greenhead Labs operations**

---

## Duck-Pond CLI (dp)

### Main Commands
```bash
dp                         # Show main menu
dp ask "question"         # Query Ollama (free AI)
dp search "term"          # Search knowledge base
dp cost status            # Check API spending
dp tokens                 # Token optimization guide
dp journal                # Generate Morning Journal
dp sync                   # Sync with GitHub
dp status                 # System health check
dp help                   # Show all commands
```

### Navigation
```bash
cd ~/Documents/HonkNode/Duck-Pond    # Main directory
cd System/                            # Scripts
cd Knowledge-Base/Technical/          # Tech docs
cd Knowledge-Base/Business/           # Business docs
cd Projects/Active/                   # Current work
cd Journal/                           # Daily logs
```

---

## Git Workflow

### Daily Workflow
```bash
# Start of day
git pull origin main                    # Get latest

# Make changes
# ... edit files ...

# Commit
git add -A
git commit -m "Descriptive message"
git push origin main

# If conflict
git pull --rebase origin main
git push origin main
```

### Branching (for L2+)
```bash
# Create feature branch
git checkout -b feature/new-trading-bot

# Work and commit
git add -A
git commit -m "Add arbitrage detection"

# Push branch
git push origin feature/new-trading-bot

# Create PR on GitHub
# After merge
git checkout main
git pull origin main
git branch -d feature/new-trading-bot
```

### Useful Aliases
```bash
# Add to ~/.zshrc
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.lg "log --oneline --graph"

# Usage
git st      # status
git co main # checkout
git lg      # pretty log
```

---

## Ollama Commands

### Model Management
```bash
ollama list                    # Show installed models
ollama pull llama3            # Download model
ollama rm llama3              # Remove model
ollama run llama3             # Interactive mode
ollama run llama3 "prompt"    # One-shot query
```

### Performance
```bash
ollama serve                   # Start API server
ollama ps                      # Show running models
ollama stop llama3            # Stop specific model
```

### Custom Models
```bash
# Create from Modelfile
ollama create mymodel -f Modelfile

# Show model info
ollama show llama3
```

---

## File Operations

### Search
```bash
# Find files
find . -name "*.py"                     # Python files
find . -type f -size +1M                # Large files
find . -mtime -7                        # Modified in last 7 days

# Search content
grep -r "XRPL" .                        # Search in all files
grep -ri "defi" .                       # Case insensitive
grep -n "TODO" *.py                     # Show line numbers
```

### Quick Edits
```bash
# Create file
touch newfile.py

# Edit
code file.py                            # VS Code
nano file.py                            # Terminal editor
echo "content" > file.txt               # Write to file
echo "more" >> file.txt                 # Append

# View
cat file.txt                            # Full file
head -20 file.txt                       # First 20 lines
tail -20 file.txt                       # Last 20 lines
less file.txt                           # Scrollable
```

---

## System Monitoring

### Mac Mini (HonkNode)
```bash
# CPU/Memory
top                                     # Process list
htop                                    # Better top (if installed)

# Disk usage
df -h                                   # Disk space
du -sh *                                # Directory sizes
du -sh ~/Documents/HonkNode/*           # HonkNode sizes

# Memory
vm_stat                                 # Virtual memory

# Power
sudo powermetrics --samplers smc -n 1   # Power usage
```

### Network
```bash
# Check connection
ping google.com

# Ports
lsof -i :11434                          # What's using port 11434
netstat -an | grep LISTEN               # Listening ports

# Speed test
curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python -
```

---

## Python Virtual Environments

### Setup
```bash
# Create
python3 -m venv venv

# Activate
source venv/bin/activate                # macOS/Linux
venv\Scripts\activate                   # Windows

# Install packages
pip install xrpl-py web3 pandas

# Save requirements
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt

# Deactivate
deactivate
```

---

## Security Commands

### Hashing
```bash
# SHA256
shasum -a 256 file.txt

# MD5
md5 file.txt

# Compare
shasum -c checksums.txt                 # Verify against list
```

### Encryption
```bash
# Encrypt file
gpg -c file.txt                         # Symmetric

# Decrypt
gpg file.txt.gpg

# SSH keys
ssh-keygen -t ed25519 -C "email"        # Generate key
cat ~/.ssh/id_ed25519.pub               # Show public key
```

### Permissions
```bash
# View
ls -la

# Change
chmod 600 file                          # Owner only
chmod 755 directory                     # Owner full, others read/execute
chmod +x script.sh                      # Make executable

# Owner
chown user:group file
```

---

## Productivity Shortcuts

### Terminal
```bash
# Navigation
Ctrl + A        # Beginning of line
Ctrl + E        # End of line
Ctrl + U        # Clear line
Ctrl + R        # Search history
Ctrl + C        # Cancel command
Ctrl + D        # Exit

# History
history         # Show command history
!123            # Run command 123 from history
!!              # Run last command
```

### macOS Specific
```bash
# Screenshot
Cmd + Shift + 3   # Full screen
Cmd + Shift + 4   # Selection
Cmd + Shift + 5   # Options

# Spotlight
Cmd + Space       # Open Spotlight

# Terminal
Cmd + T           # New tab
Cmd + W           # Close tab
Cmd + +           # Zoom in
Cmd + -           # Zoom out
```

---

## Quick Fixes

### Kill Process
```bash
# Find PID
ps aux | grep ollama

# Kill
kill <PID>
kill -9 <PID>       # Force kill

# Or
pkill ollama
```

### Clear Space
```bash
# Check disk
df -h

# Find large files
find ~ -type f -size +100M

# Clear caches
rm -rf ~/Library/Caches/*

# Docker cleanup (if using)
docker system prune -a
```

### Restart Services
```bash
# Ollama
pkill ollama
ollama serve

# Python script
pkill -f script.py
python3 script.py
```

---

## Resources

**Learn More:**
- https://explainshell.com/ - Command explanation
- https://tldr.sh/ - Simplified man pages
- https://cheat.sh/ - Command cheatsheets

---

**Diesel-Goose Knowledge Priority:** MEDIUM  
**Usage:** Daily operations, productivity  
**Last Updated:** 2026-02-21  
**Token Count:** ~900

🦆 **Command line mastered. Terminal velocity achieved.**
