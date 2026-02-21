#!/bin/bash
# OpenClaw Feature Setup Helper
# Run this to diagnose and fix browser/web search issues

echo "🦆 OpenClaw Feature Setup Helper"
echo "================================"
echo ""

# Check OpenClaw installation
echo "🔍 Checking OpenClaw status..."
if command -v openclaw &> /dev/null; then
    echo "✅ OpenClaw CLI found"
    openclaw --version 2>/dev/null || echo "⚠️  Version check failed"
else
    echo "❌ OpenClaw CLI not found in PATH"
    echo "   Install from: https://openclaw.ai/download"
fi
echo ""

# Check browser installation
echo "🔍 Checking browser installation..."
BROWSERS=("google-chrome" "chromium" "brave-browser" "firefox")
FOUND_BROWSER=""
for browser in "${BROWSERS[@]}"; do
    if command -v $browser &> /dev/null; then
        echo "✅ Found: $browser"
        FOUND_BROWSER=$browser
    fi
done

if [ -z "$FOUND_BROWSER" ]; then
    echo "❌ No supported browser found"
    echo "   Install Brave (recommended):"
    echo "   brew install --cask brave-browser"
else
    echo "✅ Browser ready: $FOUND_BROWSER"
fi
echo ""

# Check OpenClaw config
echo "🔍 Checking OpenClaw configuration..."
CONFIG_FILE="$HOME/.openclaw/openclaw.json"
if [ -f "$CONFIG_FILE" ]; then
    echo "✅ Config file exists: $CONFIG_FILE"
    
    # Check for web search config
    if grep -q "brave" "$CONFIG_FILE" 2>/dev/null; then
        echo "✅ Web search (Brave) appears configured"
    else
        echo "❌ Web search not configured"
        echo "   Action needed: Add Brave API key"
    fi
    
    # Check for browser config
    if grep -q "browser" "$CONFIG_FILE" 2>/dev/null; then
        echo "✅ Browser config found"
    else
        echo "❌ Browser not configured"
        echo "   Action needed: Connect Chrome extension"
    fi
else
    echo "❌ Config file not found"
    echo "   Run: openclaw onboard"
fi
echo ""

# Check Chrome extension
echo "🔍 Checking Chrome extension..."
CHROME_EXT_DIR="$HOME/Library/Application Support/Google/Chrome/Default/Extensions"
if [ -d "$CHROME_EXT_DIR" ]; then
    # Look for OpenClaw extension (approximate)
    if find "$CHROME_EXT_DIR" -name "*openclaw*" -o -name "*claw*" 2>/dev/null | grep -q .; then
        echo "✅ OpenClaw extension may be installed"
    else
        echo "❌ OpenClaw extension not detected"
        echo "   Install from Chrome Web Store"
    fi
else
    echo "⚠️  Chrome profile not found"
    echo "   Chrome may not be installed or never launched"
fi
echo ""

# Check gateway status
echo "🔍 Checking Gateway status..."
GATEWAY_PID=$(pgrep -f "openclaw.*gateway" || echo "")
if [ -n "$GATEWAY_PID" ]; then
    echo "✅ Gateway running (PID: $GATEWAY_PID)"
else
    echo "❌ Gateway not running"
    echo "   Start with: openclaw gateway start"
fi
echo ""

# Environment variables
echo "🔍 Checking environment variables..."
if [ -n "$BRAVE_API_KEY" ]; then
    echo "✅ BRAVE_API_KEY is set"
else
    echo "❌ BRAVE_API_KEY not set"
    echo "   Add to ~/.zshrc: export BRAVE_API_KEY='your_key'"
fi
echo ""

# Summary
echo "📋 SUMMARY"
echo "=========="
echo ""
echo "To enable Web Search:"
echo "1. Get Brave API key: https://brave.com/search/api/"
echo "2. Run: openclaw configure --section web"
echo "3. Or add to ~/.zshrc: export BRAVE_API_KEY='your_key'"
echo ""
echo "To enable Browser Automation:"
echo "1. Install Chrome/Brave"
echo "2. Install OpenClaw extension from Chrome Web Store"
echo "3. Navigate to a website and click extension icon to attach"
echo "4. Badge should show 'ON' when connected"
echo ""
echo "Quick test commands:"
echo "  openclaw web-search 'test query'"
echo "  openclaw browser open https://example.com"
echo ""
echo "For detailed guide:"
echo "  open ~/Documents/HonkNode/Duck-Pond/Knowledge-Base/Skills/OpenClaw-Feature-Setup.md"
echo ""
echo "🦆 Setup helper complete."
