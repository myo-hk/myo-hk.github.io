#!/bin/bash
# Lighthouse score checker for MyO
# Usage: ./tests/lighthouse-check.sh [mobile|desktop] [url]
set -euo pipefail

MODE="${1:-mobile}"
URL="${2:-https://myo-makeyourown.pages.dev}"
OUTFILE="/tmp/lighthouse-${MODE}-result.json"

echo "=== Lighthouse $MODE: $URL ==="

if command -v lighthouse &> /dev/null; then
    PRESET="--preset=$MODE"
    npx lighthouse "$URL" \
        $PRESET \
        --output=json \
        --output-path="$OUTFILE" \
        --chrome-flags="--headless --no-sandbox" \
        2>/dev/null || true

    if [ -f "$OUTFILE" ]; then
        python3 -c "
import json
with open('$OUTFILE') as f:
    d = json.load(f)
print()
print(f'  {\"Category\":20s} {\"Score\":>6s}  {\"Status\":>8s}')
print(f'  {\"-\"*20} {\"-\":>6s}  {\"-\":>8s}')
for cat, data in d['categories'].items():
    score = int(data['score'] * 100)
    status = '✅ PASS' if score >= 90 else ('⚠️  WARN' if score >= 50 else '❌ FAIL')
    print(f'  {cat:20s} {score:>4d}/100  {status}')
" 2>/dev/null || echo "Could not parse results"
    fi
else
    echo "Lighthouse CLI not found."
    echo "Install: npm install -g lighthouse"
    echo "Or visit: https://pagespeed.web.dev/?url=$URL"
fi