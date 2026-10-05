#!/bin/bash
# scaffolds.sh — Create a new video presentation from the template
# Usage: bash _scaffold.sh <NN> <topic-slug> "<Chinese Title>" <theme-name>
#
# Example:
#   bash _scaffold.sh 02 wedding-checklist-timeline "婚前準備清單：倒數 6 個月時間表" warm-keynote
#
# Theme names (with theme CSS variable files):
#   warm-keynote   — cream paper + teal accent
#   paper-press    — off-white + deep navy
#   kraft-paper    — kraft brown + forest green
#   midnight-press — dark indigo + gold accents
#   vintage-editorial — sepia + burgundy
#   indigo-porcelain — porcelain white + indigo blue
#   forest-ink     — forest green + warm brown
#   sunset-zine    — warm peach + deep purple
#
# Color values per theme:
# warm-keynote:    --bg: #faf8f5; --text: #2d1f1a; --accent: #c17f5e; --accent2: #5a8f8a
# paper-press:     --bg: #f7f5f0; --text: #1a1a2e; --accent: #1e3a5f; --accent2: #8b7355
# kraft-paper:     --bg: #f5f0e8; --text: #3a2a1a; --accent: #6b8e5a; --accent2: #a0805a
# midnight-press:  --bg: #1a1a2e; --text: #e8dcc8; --accent: #c9a84c; --accent2: #6c5b7b
# vintage-editorial: --bg: #f8f0e3; --text: #3d2b1f; --accent: #8b3a3a; --accent2: #6b5b4a
# indigo-porcelain: --bg: #f4f1eb; --text: #1b2a3a; --accent: #2b4f7b; --accent2: #5a7a9a
# forest-ink:     --bg: #f0ede6; --text: #2a3a2a; --accent: #4a6b3a; --accent2: #7a5a3a
# sunset-zine:    --bg: #faf0e6; --text: #3a1a2a; --accent: #b85a4a; --accent2: #6a3a5a

set -euo pipefail

NUM="$1"
SLUG="$2"
TITLE="$3"
THEME="$4"

DIR="presentations/${NUM}-${SLUG}"
TEMPLATE="presentations/01-hong-kong-wedding-flow/presentation"

if [ -z "$NUM" ] || [ -z "$SLUG" ] || [ -z "$TITLE" ] || [ -z "$THEME" ]; then
  echo "Usage: bash _scaffold.sh <NN> <topic-slug> \"<Chinese Title>\" <theme-name>"
  exit 1
fi

echo "==> Creating $DIR"

# Create directories
mkdir -p "$DIR/presentation/src"
mkdir -p "$DIR/presentation/public"
mkdir -p "$DIR/presentation/scripts/tts-providers"
mkdir -p "$DIR/presentation/src/chapters"
mkdir -p "$DIR/presentation/src/components"
mkdir -p "$DIR/presentation/src/hooks"
mkdir -p "$DIR/presentation/src/registry"
mkdir -p "$DIR/presentation/src/styles"
mkdir -p "$DIR/presentation/src/assets"

# Copy template files (excluding node_modules, chapters, and theme-specific)
cp "$TEMPLATE/.gitignore" "$DIR/presentation/"
cp "$TEMPLATE/eslint.config.js" "$DIR/presentation/"
# index.src.html is the Vite entry point (never a build artifact).
# Do NOT copy index.html — it is the build output and will be overwritten by `npm run build`.
cp "$TEMPLATE/index.src.html" "$DIR/presentation/"
cp "$TEMPLATE/package.json" "$DIR/presentation/"
cp "$TEMPLATE/tsconfig.app.json" "$DIR/presentation/"
cp "$TEMPLATE/tsconfig.json" "$DIR/presentation/"
cp "$TEMPLATE/tsconfig.node.json" "$DIR/presentation/"
cp "$TEMPLATE/vite.config.ts" "$DIR/presentation/"
cp "$TEMPLATE/public/favicon.svg" "$DIR/presentation/public/"
cp "$TEMPLATE/public/icons.svg" "$DIR/presentation/public/"
cp "$TEMPLATE/src/assets/hero.png" "$DIR/presentation/src/assets/"
cp "$TEMPLATE/src/assets/vite.svg" "$DIR/presentation/src/assets/"
cp "$TEMPLATE/scripts/extract-narrations.ts" "$DIR/presentation/scripts/"
cp "$TEMPLATE/scripts/synthesize-audio.sh" "$DIR/presentation/scripts/"
cp "$TEMPLATE/scripts/tts-providers/README.md" "$DIR/presentation/scripts/tts-providers/"

# Copy components, hooks, and styles (shared infrastructure)
cp "$TEMPLATE/src/components/AutoStartGate.tsx" "$DIR/presentation/src/components/"
cp "$TEMPLATE/src/components/AutoStartGate.css" "$DIR/presentation/src/components/"
cp "$TEMPLATE/src/components/AutoToggle.tsx" "$DIR/presentation/src/components/"
cp "$TEMPLATE/src/components/AutoToggle.css" "$DIR/presentation/src/components/"
cp "$TEMPLATE/src/components/MaskReveal.tsx" "$DIR/presentation/src/components/"
cp "$TEMPLATE/src/components/ProgressBar.tsx" "$DIR/presentation/src/components/"
cp "$TEMPLATE/src/components/ProgressBar.css" "$DIR/presentation/src/components/"
cp "$TEMPLATE/src/components/Stage.tsx" "$DIR/presentation/src/components/"
cp "$TEMPLATE/src/hooks/useAudioPlayer.ts" "$DIR/presentation/src/hooks/"
cp "$TEMPLATE/src/hooks/useAutoMode.ts" "$DIR/presentation/src/hooks/"
cp "$TEMPLATE/src/hooks/useStageScale.ts" "$DIR/presentation/src/hooks/"
cp "$TEMPLATE/src/hooks/useStepper.ts" "$DIR/presentation/src/hooks/"
cp "$TEMPLATE/src/main.tsx" "$DIR/presentation/src/"
cp "$TEMPLATE/src/analytics.ts" "$DIR/presentation/src/"
cp "$TEMPLATE/src/registry/types.ts" "$DIR/presentation/src/registry/"
cp "$TEMPLATE/src/styles/base.css" "$DIR/presentation/src/styles/"
cp "$TEMPLATE/src/styles/fonts.css" "$DIR/presentation/src/styles/"
cp "$TEMPLATE/src/styles/animations.css" "$DIR/presentation/src/styles/"

# Write theme-specific tokens.css
case "$THEME" in
  warm-keynote)
    cat > "$DIR/presentation/src/styles/tokens.css" << 'TOKENS'
:root {
  --bg: #faf8f5;
  --bg-card: #ffffff;
  --text: #2d1f1a;
  --text-muted: #8a7a72;
  --accent: #c17f5e;
  --accent-light: #e8d5c8;
  --accent2: #5a8f8a;
  --accent2-light: #c8ddd8;
  --border: #e5ddd6;
  --shadow: 0 2px 12px rgba(0,0,0,0.06);
  --radius: 12px;
  --radius-sm: 8px;
  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
TOKENS
    ;;
  paper-press)
    cat > "$DIR/presentation/src/styles/tokens.css" << 'TOKENS'
:root {
  --bg: #f7f5f0;
  --bg-card: #ffffff;
  --text: #1a1a2e;
  --text-muted: #6b6b7a;
  --accent: #1e3a5f;
  --accent-light: #d0dbe8;
  --accent2: #8b7355;
  --accent2-light: #ddd4c8;
  --border: #d8d4cc;
  --shadow: 0 2px 12px rgba(0,0,0,0.06);
  --radius: 8px;
  --radius-sm: 6px;
  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
TOKENS
    ;;
  kraft-paper)
    cat > "$DIR/presentation/src/styles/tokens.css" << 'TOKENS'
:root {
  --bg: #f5f0e8;
  --bg-card: #faf7f0;
  --text: #3a2a1a;
  --text-muted: #7a6a5a;
  --accent: #6b8e5a;
  --accent-light: #d4e0ca;
  --accent2: #a0805a;
  --accent2-light: #e0d4c4;
  --border: #d8cebe;
  --shadow: 0 2px 12px rgba(0,0,0,0.06);
  --radius: 8px;
  --radius-sm: 6px;
  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
TOKENS
    ;;
  midnight-press)
    cat > "$DIR/presentation/src/styles/tokens.css" << 'TOKENS'
:root {
  --bg: #1a1a2e;
  --bg-card: #252542;
  --text: #e8dcc8;
  --text-muted: #9a8e7e;
  --accent: #c9a84c;
  --accent-light: #3a3520;
  --accent2: #6c5b7b;
  --accent2-light: #2e2a3a;
  --border: #3a3a5a;
  --shadow: 0 2px 12px rgba(0,0,0,0.2);
  --radius: 12px;
  --radius-sm: 8px;
  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
TOKENS
    ;;
  vintage-editorial)
    cat > "$DIR/presentation/src/styles/tokens.css" << 'TOKENS'
:root {
  --bg: #f8f0e3;
  --bg-card: #fefaf5;
  --text: #3d2b1f;
  --text-muted: #8a7a6a;
  --accent: #8b3a3a;
  --accent-light: #e0c8c8;
  --accent2: #6b5b4a;
  --accent2-light: #d8d0c4;
  --border: #d8cec0;
  --shadow: 0 2px 12px rgba(0,0,0,0.06);
  --radius: 8px;
  --radius-sm: 6px;
  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
TOKENS
    ;;
  indigo-porcelain)
    cat > "$DIR/presentation/src/styles/tokens.css" << 'TOKENS'
:root {
  --bg: #f4f1eb;
  --bg-card: #ffffff;
  --text: #1b2a3a;
  --text-muted: #6a7a8a;
  --accent: #2b4f7b;
  --accent-light: #c8d8e8;
  --accent2: #5a7a9a;
  --accent2-light: #d0dce8;
  --border: #d4d0c8;
  --shadow: 0 2px 12px rgba(0,0,0,0.06);
  --radius: 10px;
  --radius-sm: 6px;
  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
TOKENS
    ;;
  forest-ink)
    cat > "$DIR/presentation/src/styles/tokens.css" << 'TOKENS'
:root {
  --bg: #f0ede6;
  --bg-card: #faf8f2;
  --text: #2a3a2a;
  --text-muted: #6a7a6a;
  --accent: #4a6b3a;
  --accent-light: #d0dcc8;
  --accent2: #7a5a3a;
  --accent2-light: #d8d0c4;
  --border: #d4cec2;
  --shadow: 0 2px 12px rgba(0,0,0,0.06);
  --radius: 8px;
  --radius-sm: 6px;
  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
TOKENS
    ;;
  sunset-zine)
    cat > "$DIR/presentation/src/styles/tokens.css" << 'TOKENS'
:root {
  --bg: #faf0e6;
  --bg-card: #fff8f2;
  --text: #3a1a2a;
  --text-muted: #8a6a7a;
  --accent: #b85a4a;
  --accent-light: #e8c8c0;
  --accent2: #6a3a5a;
  --accent2-light: #d8c0d0;
  --border: #e0d4c8;
  --shadow: 0 2px 12px rgba(0,0,0,0.06);
  --radius: 12px;
  --radius-sm: 8px;
  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
TOKENS
    ;;
  *)
    echo "Unknown theme: $THEME"
    exit 1
    ;;
esac

# Write the App.tsx (same as template but chapter import name)
cat > "$DIR/presentation/src/App.tsx" << 'APP'
import "./styles/fonts.css";
import "./styles/tokens.css";
import "./styles/base.css";
import "./styles/animations.css";

import { useCallback } from "react";
import { AutoStartGate } from "./components/AutoStartGate";
import { AutoToggle } from "./components/AutoToggle";
import { ProgressBar } from "./components/ProgressBar";
import { Stage } from "./components/Stage";
import { useAudioPlayer } from "./hooks/useAudioPlayer";
import { useAutoMode } from "./hooks/useAutoMode";
import { useStepper } from "./hooks/useStepper";
import { CHAPTERS } from "./registry/chapters";

function estimateMs(text: string): number {
  if (!text) return 1500;
  return Math.max(1500, text.length * 250);
}

export default function App() {
  const stepper = useStepper(CHAPTERS);
  const ch = CHAPTERS[stepper.cursor.chapter]!;
  const Cmp = ch.Component;
  const stepText = ch.narrations[stepper.cursor.step] ?? "";

  const { mode, cycleMode, autoStarted, setAutoStarted } = useAutoMode();

  const audioSrc =
    mode === "manual" || stepText === ""
      ? null
      : `${import.meta.env.BASE_URL}audio/${ch.id}/${stepper.cursor.step + 1}.mp3`;

  const onAutoAdvance = useCallback(() => stepper.next(), [stepper]);

  useAudioPlayer({
    src: audioSrc, mode, trailMs: 200, estimateFallbackMs: estimateMs(stepText),
    onAutoAdvance, autoStarted,
  });

  return (
    <>
      <Stage onAdvance={stepper.next}>
        <div key={ch.id} className="scene">
          <Cmp step={stepper.cursor.step} />
        </div>
      </Stage>
      <ProgressBar chapters={CHAPTERS} cursor={stepper.cursor} onJumpChapter={stepper.jumpToChapter} />
      <AutoToggle mode={mode} onCycle={cycleMode} />
      <AutoStartGate visible={mode === "auto" && !autoStarted} onStart={() => setAutoStarted(true)} />
    </>
  );
}
APP

# Create empty chapters placeholder
cat > "$DIR/presentation/src/registry/chapters.ts" << 'CHAP'
import type { Chapter } from "./types";

export const CHAPTERS: Chapter[] = [];
CHAP

# Create blank topic files
touch "$DIR/article.md"
touch "$DIR/script.md"
touch "$DIR/outline.md"

echo "==> Done! Scaffold created at $DIR"
echo "==> Next: Write article.md, script.md, outline.md, then build chapters/"
echo "==> Then: npm install && npm run build"