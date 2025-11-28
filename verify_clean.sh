#!/bin/bash
#
# Verification script to ensure no credentials before GitHub upload
#

echo "🔍 Scanning for sensitive data..."
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

FOUND_ISSUES=0

# Check for AWS keys (excluding templates and docs)
echo -n "Checking for AWS Access Keys... "
if grep -r "AKIA[A-Z0-9]" --include="*.py" --include="*.conf" --exclude-dir="venv" --exclude-dir="path" --exclude-dir="target" --exclude-dir="docs" . 2>/dev/null | grep -v "YOUR_AWS" | grep -v "EXAMPLE" | grep -v ".gitignore"; then
    echo -e "${RED}❌ FOUND${NC}"
    FOUND_ISSUES=1
else
    echo -e "${GREEN}✅ Clean${NC}"
fi

# Check for AWS secrets
echo -n "Checking for AWS Secret Keys... "
if grep -r "fs.s3a.secret.key  [A-Za-z0-9/+=]" --include="*.py" --include="*.conf" --exclude-dir="venv" --exclude-dir="path" --exclude-dir="target" --exclude-dir="docs" . 2>/dev/null | grep -v "YOUR" | grep -v "#"; then
    echo -e "${RED}❌ FOUND${NC}"
    FOUND_ISSUES=1
else
    echo -e "${GREEN}✅ Clean${NC}"
fi

# Check for hardcoded IPs in config/code (excluding docs)
echo -n "Checking for hardcoded IP addresses... "
if grep -r "192\.168\." --include="*.py" --include="*.conf" --exclude-dir="venv" --exclude-dir="path" --exclude-dir="target" --exclude-dir="logs" --exclude-dir="docs" . 2>/dev/null; then
    echo -e "${RED}❌ FOUND${NC}"
    FOUND_ISSUES=1
else
    echo -e "${GREEN}✅ Clean${NC}"
fi

# Check for specific bucket names
echo -n "Checking for specific bucket names... "
if grep -r "test-archit-xdp" --include="*.py" --include="*.conf" --exclude-dir="venv" --exclude-dir="path" --exclude-dir="target" --exclude-dir="docs" . 2>/dev/null; then
    echo -e "${RED}❌ FOUND${NC}"
    FOUND_ISSUES=1
else
    echo -e "${GREEN}✅ Clean${NC}"
fi

# Check for hardcoded user paths
echo -n "Checking for hardcoded user paths... "
if grep -r "/Users/gajananmishra" --include="*.py" --exclude-dir="venv" --exclude-dir="path" --exclude-dir="target" . 2>/dev/null | grep -v "CELEBORN_HOME" | grep -v "expanduser" | grep -v "abspath"; then
    echo -e "${RED}❌ FOUND${NC}"
    FOUND_ISSUES=1
else
    echo -e "${GREEN}✅ Clean${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ $FOUND_ISSUES -eq 0 ]; then
    echo -e "${GREEN}✅ Repository is CLEAN and ready for GitHub!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. git init (if not already initialized)"
    echo "  2. git add ."
    echo "  3. git commit -m 'Initial commit: Celeborn with S3 support'"
    echo "  4. git remote add origin <your-repo-url>"
    echo "  5. git push -u origin main"
else
    echo -e "${RED}❌ ISSUES FOUND - Do NOT upload to GitHub yet!${NC}"
    echo ""
    echo "Please review and fix the issues above before uploading."
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

