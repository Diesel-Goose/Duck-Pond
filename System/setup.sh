#!/bin/zsh
# Duck Pond Setup Script
# Run this to configure Duck Pond for optimal use

echo "🦆 Setting up Duck Pond..."

DUCK_POND="$HOME/Documents/HonkNode/Duck-Pond"
SYSTEM="$DUCK_POND/System"

# Check if Duck Pond exists
if [ ! -d "$DUCK_POND" ]; then
    echo "❌ Duck Pond not found at $DUCK_POND"
    exit 1
fi

# Make scripts executable
chmod +x "$SYSTEM/"*.py
chmod +x "$SYSTEM/duck-pond.sh"

echo "✅ Scripts made executable"

# Add to .zshrc if not already present
if ! grep -q "duck-pond.sh" "$HOME/.zshrc" 2>/dev/null; then
    echo "" >> "$HOME/.zshrc"
    echo "# Duck Pond Quick Access" >> "$HOME/.zshrc"
    echo "source $SYSTEM/duck-pond.sh" >> "$HOME/.zshrc"
    echo "✅ Added Duck Pond to .zshrc"
else
    echo "✅ Duck Pond already in .zshrc"
fi

# Create symlinks for global access
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

# Create wrapper scripts
cat > "$BIN_DIR/dp" << EOF
#!/bin/zsh
source "$SYSTEM/duck-pond.sh"
dp "\$@"
EOF

cat > "$BIN_DIR/dp-quick" << EOF
#!/bin/zsh
cd "$SYSTEM" && python3 dp-quick.py "\$@"
EOF

cat > "$BIN_DIR/dp-fzf" << EOF
#!/bin/zsh
cd "$SYSTEM" && python3 dp-fzf.py "\$@"
EOF

cat > "$BIN_DIR/dp-template" << EOF
#!/bin/zsh
cd "$SYSTEM" && python3 dp-template.py "\$@"
EOF

chmod +x "$BIN_DIR/"dp*

echo "✅ Created global commands: dp, dp-quick, dp-fzf, dp-template"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "" >> "$HOME/.zshrc"
    echo "# Local bin for Duck Pond" >> "$HOME/.zshrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc"
    echo "✅ Added ~/.local/bin to PATH"
fi

# Check for dependencies
echo ""
echo "🔍 Checking dependencies..."

# Check Python
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 installed"
else
    echo "❌ Python 3 not found. Install with: brew install python"
fi

# Check Ollama
if command -v ollama &> /dev/null; then
    echo "✅ Ollama installed"
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✅ Ollama running"
    else
        echo "⚠️  Ollama installed but not running. Start with: ollama serve"
    fi
else
    echo "⚠️  Ollama not installed. Install with: brew install ollama"
fi

# Check fzf (optional)
if command -v fzf &> /dev/null; then
    echo "✅ fzf installed (for fuzzy search)"
else
    echo "⚠️  fzf not installed. For fuzzy search: brew install fzf"
fi

# Check editor
if [ -n "$EDITOR" ]; then
    echo "✅ EDITOR set to: $EDITOR"
else
    echo "⚠️  EDITOR not set. Add to .zshrc: export EDITOR='nano' (or vim, code, etc.)"
fi

echo ""
echo "🦆 Setup complete!"
echo ""
echo "Quick start:"
echo "  1. Restart your terminal (or: source ~/.zshrc)"
echo "  2. Type 'dp' to see commands"
echo "  3. Type 'dp-quick \"Your note\"' to store something"
echo "  4. Type 'dp-fzf' for interactive search"
echo ""
echo "Or use the full path:"
echo "  cd $SYSTEM"
echo "  python3 vault_cli.py help"
