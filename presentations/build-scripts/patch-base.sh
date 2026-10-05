#!/bin/bash
# Patch all 40 vite.config.ts files with the correct base path
# Usage: bash presentations/build-scripts/patch-base.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PRESENTATIONS_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Patching base path in all vite.config.ts files..."
echo ""

for config_file in "$PRESENTATIONS_DIR"/*/presentation/vite.config.ts; do
  # Extract the slug from the path
  dir_name="$(basename "$(dirname "$(dirname "$config_file")")")"
  base_path="/presentations/$dir_name/presentation/"
  
  echo "[$dir_name] Setting base: \"$base_path\""
  
  # Check if base is already set
  if grep -q "base:" "$config_file" 2>/dev/null; then
    echo "  -> base already set, skipping"
    continue
  fi
  
  # Add base after the plugins line, with proper formatting
  # Using a temp file for sed compatibility across platforms
  awk -v base="  base: \"$base_path\"," '
    /plugins: \[react\(\)\],/ {
      print
      print base
      next
    }
    { print }
  ' "$config_file" > "${config_file}.tmp" && mv "${config_file}.tmp" "$config_file"
  
  echo "  -> patched ✓"
done

echo ""
echo "All patches complete!"