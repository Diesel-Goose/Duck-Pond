#!/bin/bash
# Brave Browser + Web Search Setup for Greenhead Labs
# This script configures OpenClaw to use Brave Browser and Brave Search API

echo "🦆 Brave Browser Setup for Greenhead Labs"
echo "=========================================="
echo ""

# Check if Brave is installed
echo "🔍 Checking Brave Browser installation..."
if [ -d "/Applications/Brave Browser.app" ]; then
    echo "✅ Brave Browser found in Applications"
    
    # Check version
    BRAVE_VERSION=$(/Applications/Brave\ Browser.app/Contents/MacOS/Brave\ Browser --version 2>/dev/null | head -1 || echo "Unknown")
    echo "   Version: $BRAVE_VERSION"
else
    echo "❌ Brave Browser not found"
    echo "   Install from: https://brave.com/download/"
    exit 1
fi
echo ""

# Check for OpenClaw extension
echo "🔍 Checking OpenClaw Browser Relay extension..."
EXTENSION_PATH="$HOME/Library/Application Support/BraveSoftware/Brave-Browser/Default/Extensions"
if [ -d "$EXTENSION_PATH" ]; then
    # Look for OpenClaw extension
    if find "$EXTENSION_PATH" -name "*openclaw*" -o -name "*claw*" 2>/dev/null | grep -q .; then
        echo "✅ OpenClaw extension may be installed"
    else
        echo "⚠️  OpenClaw extension not detected"
        echo "   Install from Chrome Web Store:"
        echo "   https://chromewebstore.google.com/detail/openclaw-browser-relay"
    fi
else
    echo "⚠️  Brave profile not found - may need to launch Brave first"
fi
echo ""

# Check OpenClaw configuration
echo "🔍 Checking OpenClaw configuration..."
OPENCLAW_CONFIG="$HOME/.openclaw/openclaw.json"

if [ -f "$OPENCLAW_CONFIG" ]; then
    echo "✅ OpenClaw config found"
    
    # Check for web search config
    if grep -q "brave" "$OPENCLAW_CONFIG" 2>/dev/null; then
        echo "✅ Brave Search appears configured"
    else
        echo "❌ Brave Search not configured"
        echo ""
        echo "To configure, you need a Brave Search API key:"
        echo "1. Visit: https://brave.com/search/api/"
        echo "2. Sign up for free tier (2000 queries/month)"
        echo "3. Get your API key"
        echo "4. Add to OpenClaw config"
    fi
else
    echo "❌ OpenClaw config not found"
    echo "   Run: openclaw onboard"
fi
echo ""

# Test web search if configured
echo "🔍 Testing configuration..."
if command -v openclaw &> /dev/null; then
    echo "✅ OpenClaw CLI found"
    
    # Try a test search
    echo ""
    echo "Testing web search (if configured)..."
    openclaw web-search "test query" 2>&1 | head -5 || echo "   Web search not configured or failed"
else
    echo "❌ OpenClaw CLI not found"
fi
echo ""

# Summary
echo "📋 SETUP STATUS"
echo "==============="
echo ""
echo "To complete setup:"
echo ""
echo "1. BRAVE SEARCH API KEY"
echo "   ☐ Get from: https://brave.com/search/api/"
echo "   ☐ Free tier: 2000 queries/month"
echo "   ☐ Add to: ~/.openclaw/openclaw.json"
echo ""
echo "2. OPENCLAW BROWSER EXTENSION"
echo "   ☐ Open Brave Browser"
echo "   ☐ Visit Chrome Web Store"
echo "   ☐ Search: 'OpenClaw Browser Relay'"
echo "   ☐ Install extension"
echo "   ☐ Pin to toolbar"
echo ""
echo "3. CONNECT BROWSER"
echo "   ☐ Navigate to website you want to control"
echo "   ☐ Click OpenClaw extension icon"
echo "   ☐ Toggle 'Attach Tab' to ON"
echo "   ☐ Badge shows green 'ON'"
echo ""
echo "4. TEST CONNECTION"
echo "   ☐ Run: openclaw browser open https://example.com"
echo "   ☐ Run: openclaw browser snapshot"
echo ""
echo "🦆 Ready to help you browse and search!"
