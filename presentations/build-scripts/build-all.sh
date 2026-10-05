#!/bin/bash
# Build all 40 presentation projects with parallel workers
# Usage: bash presentations/build-scripts/build-all.sh [--skip-existing]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PRESENTATIONS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SKIP_EXISTING=false
[[ "${1:-}" == "--skip-existing" ]] && SKIP_EXISTING=true

# Collect all project dirs (sorted by number)
PROJECT_DIRS=()
for dir in "$PRESENTATIONS_DIR"/*/presentation/; do
  if [ -f "$dir/package.json" ] && [ -f "$dir/vite.config.ts" ]; then
    PROJECT_DIRS+=("$dir")
  fi
done

echo "Found ${#PROJECT_DIRS[@]} projects to build"
echo "Skip existing dist: $SKIP_EXISTING"
echo ""

# Build function
build_one() {
  local dir="$1"
  local slug="$(basename "$(dirname "$dir")")"
  
  if $SKIP_EXISTING && [ -f "$dir/dist/index.html" ]; then
    echo "[$slug] SKIP (dist already exists)"
    return 0
  fi
  
  echo "[$slug] Starting..."
  
  # npm install if needed
  if [ ! -d "$dir/node_modules" ]; then
    echo "[$slug] Installing dependencies..."
    cd "$dir" && npm install --silent 2>&1 | tail -1
  fi
  
  cd "$dir" && npm run build 2>&1 | tail -3
  echo "[$slug] Done ✓"
}

# Build sequentially (parallelizing via agents instead)
for dir in "${PROJECT_DIRS[@]}"; do
  build_one "$dir"
done

echo ""
echo "=== All builds complete ==="