#!/usr/bin/env python3
"""Batch-fix ProgressBar.css for presentations 02-40 + update package.json build scripts."""

import glob
import os
import re

BASE = '/Users/bubu/Documents/Github/myo-hk/presentations'

def fix_css(path):
    """Apply 3 changes to ProgressBar.css"""
    with open(path) as f:
        lines = f.readlines()
    
    out = []
    in_pb_block = False
    in_hover_block = False
    hover_block_end = -1
    pb_opacity_fixed = False
    pb_transform_fixed = False
    
    for i, line in enumerate(lines):
        stripped = line.rstrip()
        
        # Track blocks
        if re.match(r'^\.pb\s*\{', stripped):
            in_pb_block = True
        elif in_pb_block and stripped == '}':
            in_pb_block = False
        
        if re.match(r'^\.pb-hover:hover\s*\.pb\s*\{', stripped):
            in_hover_block = True
        elif in_hover_block and stripped == '}':
            in_hover_block = False
            hover_block_end = i  # The } closing .pb-hover:hover .pb
        
        # Apply changes to .pb block
        if in_pb_block and not pb_opacity_fixed and 'opacity: 0;' in stripped:
            line = line.replace('opacity: 0;', 'opacity: 1;')
            pb_opacity_fixed = True
        if in_pb_block and not pb_transform_fixed and 'transform: translateY(100%);' in stripped:
            line = line.replace('transform: translateY(100%);', 'transform: translateY(calc(100% - 30px));')
            pb_transform_fixed = True
        
        out.append(line)
    
    # Insert ::before block after hover_block_end
    if hover_block_end > 0:
        before_block = """\n.pb-hover::before {
  content: '';
  position: absolute;
  left: 50%;
  bottom: calc(100% - 6px);
  transform: translateX(-50%);
  width: 40px;
  height: 3px;
  border-radius: 2px;
  background: var(--accent);
  opacity: 0.4;
  pointer-events: none;
  transition: opacity var(--dur-quick);
}
.pb-hover:hover::before {
  opacity: 0;
}
"""
        out.insert(hover_block_end + 1, before_block)
    
    result = ''.join(out)
    if result != ''.join(lines):
        with open(path, 'w') as f:
            f.write(result)
        return True
    return False

def fix_package_json(path):
    """Add post-build copy to build script."""
    with open(path) as f:
        content = f.read()
    
    old = '"build": "tsc -b && vite build"'
    new = '"build": "tsc -b && vite build && cp dist/index.html index.html"'
    
    if old in content:
        content = content.replace(old, new)
        with open(path, 'w') as f:
            f.write(content)
        return True
    return False

# Main
fixed_css = 0
fixed_pkg = 0

for i in range(2, 41):
    prefix = f'{i:02d}'
    matches = glob.glob(os.path.join(BASE, f'{prefix}-*'))
    for m in matches:
        css_path = os.path.join(m, 'presentation/src/components/ProgressBar.css')
        pkg_path = os.path.join(m, 'presentation/package.json')
        
        if os.path.exists(css_path):
            if fix_css(css_path):
                print(f'CSS  fixed: {os.path.basename(m)}/presentation/src/components/ProgressBar.css')
                fixed_css += 1
            else:
                print(f'CSS  skip:  {os.path.basename(m)} (no changes needed or already fixed)')
        
        if os.path.exists(pkg_path):
            if fix_package_json(pkg_path):
                print(f'PKG  fixed: {os.path.basename(m)}/presentation/package.json')
                fixed_pkg += 1
            else:
                print(f'PKG  skip:  {os.path.basename(m)} (already has post-build copy)')

print(f'\nDone: {fixed_css} CSS files fixed, {fixed_pkg} package.json files updated')
