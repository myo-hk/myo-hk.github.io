/**
 * Batch presentation generator.
 * Usage: node scripts/generate-presentations/generate.js [slug]
 *   slug — optional, generate only one presentation (e.g. "04-auspicious-date-guide")
 *   no args — generate all 38 presentations (02-40)
 */

const fs = require("fs");
const path = require("path");
const { getHook, getSmall } = require("./svgLibrary");
const PRESENTATIONS = require("./data");

const BASE = path.resolve(__dirname, "../../presentations");

/* ─── Helpers ─── */

function guessComponent(chapterId) {
  // "02-cost1-registration" → "Cost1Registration"
  return chapterId
    .replace(/^\d+-/, "")
    .split("-")
    .map((s, i) => (i === 0 ? s : s[0].toUpperCase() + s.slice(1)))
    .join("");
}

function prefixFromId(chapterId) {
  // Map each chapter to a 2-3 letter CSS prefix
  const map = {
    "01-coldopen": "co",
    "06-cta": "ct",
  };
  if (map[chapterId]) return map[chapterId];
  // info chapters: c1, c2, c3, c4, c5, ...
  const num = parseInt(chapterId, 10);
  return `c${num - 1}`;
}

function jsString(s) {
  return JSON.stringify(s);
}


/* ─── Icon mapping ─── */

function getHookIcon(chapterId, presTitle) {
  const id = chapterId.toLowerCase();
  if (id.includes("calendar") || id.includes("date") || id.includes("time")) return "calendar";
  if (id.includes("document") || id.includes("file") || id.includes("paper")) return "document";
  if (id.includes("ring") || id.includes("diamond")) return "diamond";
  if (id.includes("camera") || id.includes("photo") || id.includes("video")) return "camera";
  if (id.includes("venue") || id.includes("hotel") || id.includes("place")) return "venue";
  if (id.includes("gift") || id.includes("present")) return "gift";
  if (id.includes("globe") || id.includes("travel") || id.includes("overseas")) return "globe";
  if (id.includes("compar") || id.includes("vs") || id.includes("difference")) return "scale";
  if (id.includes("clock") || id.includes("timeline") || id.includes("schedule")) return "clock";
  if (id.includes("budget") || id.includes("cost") || id.includes("fee") || id.includes("price") || id.includes("finance")) return "star";
  if (id.includes("heart") || id.includes("love") || id.includes("romance")) return "heart";
  if (id.includes("guide") || id.includes("step") || id.includes("intro")) return "book";
  if (id.includes("star") || id.includes("rating")) return "star";
  if (id.includes("care") || id.includes("clean") || id.includes("storage") || id.includes("wash")) return "check";
  const t = presTitle;
  if (t.indexOf('戒指') !== -1 || t.indexOf('鑽石') !== -1) return "diamond";
  if (t.indexOf('攝影') !== -1 || t.indexOf('相') !== -1) return "camera";
  if (t.indexOf('場地') !== -1 || t.indexOf('婚宴') !== -1 || t.indexOf('教堂') !== -1) return "venue";
  if (t.indexOf('禮物') !== -1 || t.indexOf('回禮') !== -1) return "gift";
  if (t.indexOf('海外') !== -1) return "globe";
  if (t.indexOf('預算') !== -1 || t.indexOf('費用') !== -1 || t.indexOf('開支') !== -1 || t.indexOf('財務') !== -1) return "star";
  if (t.indexOf('流程') !== -1 || t.indexOf('步驟') !== -1 || t.indexOf('程序') !== -1) return "book";
  if (t.indexOf('習俗') !== -1 || t.indexOf('傳統') !== -1 || t.indexOf('儀式') !== -1) return "book";
  if (t.indexOf('禁忌') !== -1 || t.indexOf('注意') !== -1) return "question";
  return "document";
}

function getCardIcon(chapterId, presTitle) {
  return getHookIcon(chapterId, presTitle);
}

/* ─── Content generators ─── */

function generateArticle(p) {
  const chapters = p.chapters || [];
  return `# ${p.title}

## 引言

結婚係人生大事，尤其喺香港，要考慮嘅嘢多不勝數。${p.desc}無論你係啱啱開始計劃定係已經進行緊，呢篇文章都會幫你梳理清楚所有重點。

## ${chapters[0]?.title || "基本概念"}

${p.heroLabel}係香港結婚其中一個最重要嘅考慮因素。根據最新數據，${p.heroSub}了解呢個基本概念，可以幫你喺規劃嘅時候更有方向。

### 點解咁重要？

喺香港嘅結婚流程入面，呢個環節影響住之後每一個決定。無論係預算分配定係時間安排，都需要先了解清楚。

## ${chapters[1]?.title || "詳細分析"}

呢一章會深入探討相關細節。香港嘅結婚市場發展成熟，有好多選擇俾新人。

### 主要考慮因素

- **成本考慮**：香港生活成本高，結婚開支需要仔細規劃
- **時間安排**：由籌備到婚禮，一般需要 6-12 個月
- **法律要求**：根據香港法例，結婚需要滿足特定條件

### 常見選擇

香港嘅新人通常會根據自己嘅需要同預算，選擇最適合嘅方案。無論你嘅預算係幾多，都有相應嘅選擇。

## ${chapters[2]?.title || "深入探討"}

進一步探討相關細節，幫你了解箇中嘅學問同技巧。

### 專家建議

- 盡早開始規劃，俾自己充足時間準備
- 多做比較，唔好急住決定
- 請教有經驗嘅朋友或專業人士

## ${chapters[3]?.title || "實用貼士"}

以下係幾個實用嘅建議，可以幫你慳錢慳時間：

### 預算分配

結婚開支可以分為幾個主要類別。了解每個類別嘅佔比，可以幫你更有效咁分配預算。

### 時間管理

由求婚到婚禮，成個過程大約需要一年時間。每個階段都有唔同嘅重點。

## ${chapters[4]?.title || "注意事項"}

注意以下幾點，可以避免常見嘅問題：

- **文件準備**：確保所有文件齊全
- **截止日期**：留意各項申請嘅截止日期
- **後備方案**：為突發情況做好準備

## 總結

結婚籌備雖然繁複，但只要按部就班，每一步都做好準備，就可以輕鬆搞掂。${p.title}係其中好重要嘅一環，希望呢篇文章幫到您。

記住，結婚最重要嘅係兩個人嘅感情，所有細節都係為咗創造一個美好嘅回憶。`;
}

function generateOutline(p) {
  const chapters = p.chapters || [];
  return `# ${p.title} — Outline

## 第一章：${chapters[0]?.title || "開場"}
- Step 0: 引入主題
- Step 1: 展示核心數據
- Step 2: 預覽章節

## 第二章：${chapters[1]?.title || "主內容一"}
- Step 0: 引入概念
- Step 1: 展示數據
- Step 2: 詳細對比/列表

## 第三章：${chapters[2]?.title || "主內容二"}
- Step 0: 引入概念
- Step 1: 展示數據
- Step 2: 詳細對比/列表

## 第四章：${chapters[3]?.title || "主內容三"}
- Step 0: 引入概念
- Step 1: 展示數據
- Step 2: 詳細對比/列表

## 第五章：${chapters[4]?.title || "主內容四"}
- Step 0: 引入概念
- Step 1: 展示數據
- Step 2: 詳細對比/列表

## 第六章：總結
- Step 0: 完成提示
- Step 1: 重點回顧
- Step 2: 呼籲行動（myo-makeyourown.pages.dev）`;
}

function generateScript(p) {
  const chapters = p.chapters || [];
  const lines = [];
  // ch01 - 3 narrations
  lines.push(`${p.desc}`);
  lines.push(`${p.heroLabel}：${p.heroSub}`);
  lines.push(`等我帶你睇晒成個流程，等你 planning 嘅時候更有預算。`);
  // ch02-05 - 3 each
  for (let i = 1; i <= 4 && i < chapters.length; i++) {
    const ch = chapters[i];
    if (ch.kind === "compare") {
      lines.push(`${ch.hookTitle}，究竟有咩選擇？`);
      lines.push(`等我哋睇下相關嘅數據同價格。`);
      lines.push(`記住，選擇最適合你嘅方案先係最重要。`);
    } else {
      lines.push(`${ch.hookTitle}，呢度有幾個重點。`);
      lines.push(`等我詳細解釋俾你聽。`);
      lines.push(`搞清楚呢啲細節，就可以安心繼續下一步。`);
    }
  }
  // ch06 - 3 narrations
  lines.push(`搞掂晒！你已經掌握晒所有重點。`);
  lines.push(`等我幫你 recap 一下。`);
  lines.push(`想睇更多香港結婚資訊？上 myo-makeyourown.pages.dev`);
  return lines;
}

/* ─── TSX generators ─── */

function coldopenTSX(p, ch, prefix) {
  const compName = "Coldopen";
  const cats = p.categories || [];
  const catsArray = cats.map((c) => jsString(c)).join(", ");
  return `import "./${compName}.css";
interface Props { step: number; }

const CATEGORIES = [${catsArray}];

export function ${compName}({ step }: Props) {
  if (step === 0) {
    return (
      <div className="${prefix}-scene">
        <div className="${prefix}-hook">
          ${getHook("check", prefix)}
          <h1 className="${prefix}-title">${p.title}</h1>
          <p className="${prefix}-sub">${p.desc}</p>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="${prefix}-scene">
        <div className="${prefix}-number-block">
          <div className="${prefix}-highlight-bar">
            <span className="${prefix}-rule" />
            <span className="${prefix}-number-appear">${p.heroNum}</span>
            <span className="${prefix}-rule" />
          </div>
          <span className="${prefix}-number-label">${p.heroLabel}</span>
          <span className="${prefix}-number-sub">${p.heroSub}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="${prefix}-scene">
      <h2 className="${prefix}-preview-title">主要環節</h2>
      <div className="${prefix}-preview-grid">
        {CATEGORIES.map((cat, i) => (
          <div key={i} className="${prefix}-preview-card" style={{ animationDelay: \`\${i * 80}ms\` }}>
            {cat}
          </div>
        ))}
      </div>
    </div>
  );
}`;
}

function infoTSX(p, ch, prefix, idx) {
  const compName = guessComponent(ch.id);
  const chData = p.chapters[idx] || {};

  if (chData.kind === "compare") {
    const items = chData.items || [];
    const pairs = items.map((item) => {
      const [label, value] = typeof item === "string" ? [item, ""] : [item.label, item.value];
      return `          <div className="${prefix}-compare-item">
            <span className="${prefix}-compare-label">${label}</span>
            <span className="${prefix}-compare-value">${value}</span>
          </div>`;
    }).join(`\n          <div className="${prefix}-compare-divider" />\n`);

    return `import "./${compName}.css";
interface Props { step: number; }

export function ${compName}({ step }: Props) {
  if (step === 0) {
    return (
      <div className="${prefix}-scene">
        <div className="${prefix}-hook">
          ${getHook(getCardIcon(ch.id, p.title), prefix)}
          <h1 className="${prefix}-title">${chData.hookTitle || chData.title}</h1>
          <p className="${prefix}-sub">${chData.hookSub || ""}</p>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="${prefix}-scene">
        <div className="${prefix}-number-block">
          <div className="${prefix}-highlight-bar">
            <span className="${prefix}-rule" />
            <span className="${prefix}-number-appear">${chData.num || p.heroNum}</span>
            <span className="${prefix}-rule" />
          </div>
          <span className="${prefix}-number-label">${chData.numLabel || ""}</span>
          <span className="${prefix}-number-sub">${chData.numSub || ""}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="${prefix}-scene">
      <div className="${prefix}-card">
        <h2 className="${prefix}-card-title">${chData.cardTitle || chData.title}</h2>
        <div className="${prefix}-compare">
${pairs}
        </div>
      </div>
    </div>
  );
}`;
  }

  if (chData.kind === "list") {
    const items = chData.items || [];
    const listItems = items.map((item, i) => {
      const label = typeof item === "string" ? item : item.label;
      return `          <div className="${prefix}-list-item" style={{ animationDelay: \`\${${i * 100}}ms\` }}>
            ${getSmall(getCardIcon(ch.id, p.title))}
            <span>${label}</span>
          </div>`;
    }).join("\n");

    return `import "./${compName}.css";
interface Props { step: number; }

export function ${compName}({ step }: Props) {
  if (step === 0) {
    return (
      <div className="${prefix}-scene">
        <div className="${prefix}-hook">
          ${getHook(chData.hookIcon || "document", prefix)}
          <h1 className="${prefix}-title">${chData.hookTitle || chData.title}</h1>
          <p className="${prefix}-sub">${chData.hookSub || ""}</p>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="${prefix}-scene">
        <div className="${prefix}-number-block">
          <div className="${prefix}-highlight-bar">
            <span className="${prefix}-rule" />
            <span className="${prefix}-number-appear">${chData.num || ""}</span>
            <span className="${prefix}-rule" />
          </div>
          <span className="${prefix}-number-label">${chData.numLabel || ""}</span>
          <span className="${prefix}-number-sub">${chData.numSub || ""}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="${prefix}-scene">
      <div className="${prefix}-card">
        <h2 className="${prefix}-card-title">${chData.cardTitle || chData.title}</h2>
        <div className="${prefix}-list">
${listItems}
        </div>
      </div>
    </div>
  );
}`;
  }

  // Default: info cards
  const cards = chData.items || [];
  const cardEls = cards.map((item, i) => {
    const label = typeof item === "string" ? item : item.label || "";
    const desc = typeof item === "string" ? "" : item.desc || "";
    return `          <div className="${prefix}-card" style={{ animationDelay: \`\${${(i + 1) * 100}}ms\` }}>
            ${getSmall(getCardIcon(ch.id, p.title))}
            <span className="${prefix}-card-label">${label}</span>
            ${desc ? `<span className="${prefix}-card-desc">${desc}</span>` : ""}
          </div>`;
  }).join("\n");

  return `import "./${compName}.css";
interface Props { step: number; }

export function ${compName}({ step }: Props) {
  if (step === 0) {
    return (
      <div className="${prefix}-scene">
        <div className="${prefix}-hook">
          ${getHook(chData.hookIcon || "document", prefix)}
          <h1 className="${prefix}-title">${chData.hookTitle || chData.title}</h1>
          <p className="${prefix}-sub">${chData.hookSub || ""}</p>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="${prefix}-scene">
        <div className="${prefix}-number-block">
          <div className="${prefix}-highlight-bar">
            <span className="${prefix}-rule" />
            <span className="${prefix}-number-appear">${chData.num || p.heroNum}</span>
            <span className="${prefix}-rule" />
          </div>
          <span className="${prefix}-number-label">${chData.numLabel || ""}</span>
          <span className="${prefix}-number-sub">${chData.numSub || ""}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="${prefix}-scene">
      <div className="${prefix}-card-grid">
${cardEls}
      </div>
    </div>
  );
}`;
}

function ctaTSX(p, prefix) {
  const recap = p.ctaRecap || p.categories?.map((c, i) => ({ label: c, pct: `${(i + 1) * 5}%` })) || [];
  const recapItems = recap.map((item, i) => {
    return `          <div key={i} className="${prefix}-recap-card" style={{ animationDelay: \`\${${100 + i * 80}}ms\` }}>
            <span className="${prefix}-recap-label">${item.label}</span>
            <div className="${prefix}-recap-bar-bg">
              <div className="${prefix}-recap-bar-fill" style={{ width: "${item.pct}" }} />
            </div>
            <span className="${prefix}-recap-pct">${item.pct}</span>
          </div>`;
  }).join("\n");

  return `import "./CTA.css";
interface Props { step: number; }

const RECAP_ITEMS = ${JSON.stringify(recap)};

export function CTA({ step }: Props) {
  if (step === 0) {
    return (
      <div className="${prefix}-scene">
        <div className="${prefix}-hook">
          ${getHook("check", prefix)}
          <h1 className="${prefix}-title">搞掂晒！</h1>
          <p className="${prefix}-sub">你已經掌握晒${p.title}嘅所有重點</p>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="${prefix}-scene">
        <h2 className="${prefix}-recap-title">重點重温</h2>
        <div className="${prefix}-recap-grid">
${recapItems}
        </div>
      </div>
    );
  }

  return (
    <div className="${prefix}-scene">
      <div className="${prefix}-final-card">
        ${getHook("heart", prefix)}
        <h2 className="${prefix}-final-title">超過 400 篇香港婚禮教學文章</h2>
        <p className="${prefix}-final-desc">由籌備到婚禮，一站式資訊平台</p>
        <a href="https://myo-makeyourown.pages.dev/" className="${prefix}-cta-link" target="_blank" rel="noopener noreferrer">
          myo-makeyourown.pages.dev
          <svg viewBox="0 0 24 24" width="20" height="20">
            <path d="M7 17L17 7M7 7h10v10" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </a>
      </div>
    </div>
  );
}`;
}

function generateTSX(p, ch, prefix, idx) {
  if (idx === 0) return coldopenTSX(p, ch, prefix);
  if (idx === p.chapters.length) return ctaTSX(p, prefix);
  return infoTSX(p, ch, prefix, idx);
}

/* ─── CSS generators ─── */

function sceneStyles(prefix) {
  return `.${prefix}-scene {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  padding: var(--stage-pad-y) var(--stage-pad-x);
  text-align: center;
  overflow: hidden;
}
.${prefix}-hook {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  animation: ${prefix}-fade-in 600ms cubic-bezier(0.16, 1, 0.3, 1) both;
}
.${prefix}-hook-icon {
  animation: ${prefix}-scale-in 500ms cubic-bezier(0.34, 1.56, 0.64, 1) both;
}
.${prefix}-title {
  font-size: clamp(40px, 4.5vw, 72px);
  font-weight: 700;
  color: var(--text);
  font-family: var(--font-display-cn);
}
.${prefix}-sub {
  font-size: 20px;
  color: var(--text-mute);
  font-family: var(--font-display-cn);
}
.${prefix}-number-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  animation: ${prefix}-fade-in 600ms cubic-bezier(0.16, 1, 0.3, 1) both;
}
.${prefix}-highlight-bar {
  display: flex;
  align-items: center;
  gap: 12px;
}
.${prefix}-highlight-bar .${prefix}-rule {
  width: 40px;
  height: 4px;
  background: var(--accent);
  border-radius: 2px;
}
.${prefix}-number-appear {
  font-size: clamp(40px, 5vw, 72px);
  font-weight: var(--hero-num-weight);
  letter-spacing: var(--hero-num-track);
  color: var(--accent);
  font-family: var(--font-display-en);
  animation: ${prefix}-bump 500ms cubic-bezier(0.34, 1.56, 0.64, 1) both;
}
.${prefix}-number-label {
  font-size: 22px;
  font-weight: 600;
  color: var(--text);
  font-family: var(--font-display-cn);
}
.${prefix}-number-sub {
  font-size: 16px;
  color: var(--text-mute);
  font-family: var(--font-display-cn);
}
.${prefix}-preview-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text);
  font-family: var(--font-display-cn);
  margin-bottom: 24px;
  animation: ${prefix}-fade-in 500ms cubic-bezier(0.16, 1, 0.3, 1) both;
}
.${prefix}-preview-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
  max-width: 460px;
}
.${prefix}-preview-card {
  background: var(--card-glass-bg);
  backdrop-filter: blur(8px);
  border: 1px solid var(--card-glass-border);
  border-radius: var(--r-card, 14px);
  padding: 14px 24px;
  font-size: 18px;
  font-weight: 600;
  color: var(--text);
  font-family: var(--font-display-cn);
  box-shadow: var(--card-shadow);
  animation: ${prefix}-fade-in 600ms cubic-bezier(0.16, 1, 0.3, 1) both;
}
.${prefix}-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  background: var(--card-glass-bg);
  backdrop-filter: blur(8px);
  border: 1px solid var(--card-glass-border);
  border-radius: var(--r-card, 24px);
  padding: 32px 40px;
  max-width: 420px;
  box-shadow: var(--card-shadow);
  animation: ${prefix}-fade-in 600ms cubic-bezier(0.16, 1, 0.3, 1) both;
}
.${prefix}-card-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text);
  font-family: var(--font-display-cn);
}
.${prefix}-card-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  max-width: 420px;
}
.${prefix}-card-label {
  font-size: 18px;
  font-weight: 600;
  color: var(--text);
  font-family: var(--font-display-cn);
}
.${prefix}-card-desc {
  font-size: 14px;
  color: var(--text-mute);
  font-family: var(--font-display-cn);
}
.${prefix}-compare {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 100%;
}
.${prefix}-compare-item {
  display: flex;
  align-items: center;
  gap: 12px;
  justify-content: space-between;
}
.${prefix}-compare-label {
  font-size: 18px;
  color: var(--text-2);
  font-family: var(--font-display-cn);
}
.${prefix}-compare-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--accent);
  font-family: var(--font-display-en);
}
.${prefix}-compare-divider {
  height: 1px;
  background: var(--card-glass-border);
}
.${prefix}-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
}
.${prefix}-list-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 18px;
  color: var(--text-2);
  font-family: var(--font-display-cn);
  animation: ${prefix}-fade-in 500ms cubic-bezier(0.16, 1, 0.3, 1) both;
}`;
}

function ctaStyles(prefix) {
  return `.${prefix}-scene {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 100%;
  padding: var(--stage-pad-y) var(--stage-pad-x);
  text-align: center;
  overflow: hidden;
}
.${prefix}-hook {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 24px;
  animation: ${prefix}-fade-in 600ms cubic-bezier(0.16, 1, 0.3, 1) both;
}
.${prefix}-check-icon {
  animation: ${prefix}-scale-in 500ms cubic-bezier(0.34, 1.56, 0.64, 1) both;
}
.${prefix}-title {
  font-size: clamp(40px, 4.5vw, 72px);
  font-weight: 700;
  color: var(--text);
  font-family: var(--font-display-cn);
}
.${prefix}-sub {
  font-size: 20px;
  color: var(--text-mute);
  font-family: var(--font-display-cn);
}
.${prefix}-recap-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text);
  font-family: var(--font-display-cn);
  margin-bottom: 24px;
  animation: ${prefix}-fade-in 500ms cubic-bezier(0.16, 1, 0.3, 1) both;
}
.${prefix}-recap-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
  width: 100%;
  max-width: 460px;
}
.${prefix}-recap-card {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--card-glass-bg);
  backdrop-filter: blur(8px);
  border: 1px solid var(--card-glass-border);
  border-radius: var(--r-card, 14px);
  padding: 14px 20px;
  box-shadow: var(--card-shadow);
  animation: ${prefix}-fade-in 600ms cubic-bezier(0.16, 1, 0.3, 1) both;
}
.${prefix}-recap-label {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
  font-family: var(--font-display-cn);
  min-width: 80px;
  text-align: left;
}
.${prefix}-recap-bar-bg {
  flex: 1;
  height: 12px;
  background: var(--accent-soft);
  border-radius: 6px;
  overflow: hidden;
}
.${prefix}-recap-bar-fill {
  height: 100%;
  background: var(--accent);
  border-radius: 6px;
  animation: ${prefix}-bar-grow 800ms cubic-bezier(0.16, 1, 0.3, 1) both;
  transform-origin: left;
}
.${prefix}-recap-pct {
  font-size: 16px;
  font-weight: 700;
  color: var(--accent);
  font-family: var(--font-display-en);
  min-width: 40px;
  text-align: right;
}
.${prefix}-final-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  background: var(--card-glass-bg);
  backdrop-filter: blur(8px);
  border: 1px solid var(--card-glass-border);
  border-radius: var(--r-card, 24px);
  padding: 40px 48px;
  max-width: 440px;
  box-shadow: var(--card-shadow);
  animation: ${prefix}-fade-in 600ms cubic-bezier(0.16, 1, 0.3, 1) both;
}
.${prefix}-heart-icon {
  animation: ${prefix}-scale-in 500ms cubic-bezier(0.34, 1.56, 0.64, 1) both;
}
.${prefix}-final-title {
  font-size: 22px;
  font-weight: 700;
  color: var(--text);
  font-family: var(--font-display-cn);
}
.${prefix}-final-desc {
  font-size: 16px;
  color: var(--text-mute);
  font-family: var(--font-display-cn);
}
.${prefix}-cta-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: 700;
  color: var(--accent);
  font-family: var(--font-display-en);
  text-decoration: none;
  padding: 12px 24px;
  border: 2px solid var(--accent);
  border-radius: 12px;
  transition: background 200ms, color 200ms;
}
.${prefix}-cta-link:hover {
  background: var(--accent);
  color: var(--bg);
}

@keyframes ${prefix}-fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes ${prefix}-scale-in {
  from { opacity: 0; transform: scale(0.5); }
  to { opacity: 1; transform: scale(1); }
}
@keyframes ${prefix}-bar-grow {
  from { transform: scaleX(0); }
  to { transform: scaleX(1); }
}
@keyframes ${prefix}-bump {
  from { opacity: 0; transform: scale(0.5); }
  to { opacity: 1; transform: scale(1); }
}`;
}

function infoStyles(prefix) {
  const base = sceneStyles(prefix);
  // For compare/list cards, we also need specific card styles.
  // sceneStyles already includes .pfx-card, .pfx-compare, .pfx-list.
  return base;
}

function generateCSS(ch, prefix, idx) {
  if (idx === 0) return sceneStyles(prefix);
  if (idx === 6) return ctaStyles(prefix);
  return infoStyles(prefix);
}

/* ─── Narrations generator ─── */

function narrationsLines(ch, idx, p) {
  if (idx === 0) {
    // coldopen
    return [
      `"${p.desc}"`,
      `"${p.heroLabel}：${p.heroSub}"`,
      `"等我帶你逐個環節睇清楚。"`,
    ];
  }
  if (idx === 6) {
    // cta
    return [
      `"搞掂晒！你已經掌握晒所有重點。"`,
      `"等我幫你重温一下關鍵資訊。"`,
      `"想睇更多香港結婚資訊？上 myo-makeyourown.pages.dev"`,
    ];
  }
  // info chapter
  const chData = p.chapters[idx - 1] || {};
  return [
    `"${chData.hookTitle || chData.title}，一齊了解下。"`,
    `"呢個環節有唔少細節要留意。"`,
    `"搞清楚之後，就可以安心 proceed。"`,
  ];
}

function generateNarrations(ch, idx, p) {
  const lines = narrationsLines(ch, idx, p);
  return `import type { Narration } from "../../registry/types";

export const NARRATIONS: Narration[] = [
${lines.join(",\n")},
];`;
}

/* ─── Registry generator ─── */

function generateRegistry(p) {
  const chaps = p.chapters || [];
  const imports = chaps.map((ch, i) => {
    const compNames = ["Coldopen", ...chaps.slice(0, 5).map((c) => guessComponent(c.id)), "CTA"];
    const dir = ch.id;
    return `import { ${compNames[i]} } from "../chapters/${dir}/${compNames[i]}";
import { NARRATIONS as N${String(i + 1).padStart(2, "0")} } from "../chapters/${dir}/narrations";`;
  }).join("\n");

  const chDefs = chaps.map((ch, i) => {
    const nIndex = String(i + 1).padStart(2, "0");
    const compNames = ["Coldopen", ...chaps.slice(0, 5).map((c) => guessComponent(c.id)), "CTA"];
    return `  { id: "${ch.id}", title: "${ch.title}", narrations: N${nIndex}, Component: ${compNames[i]} },`;
  }).join("\n");

  return `import type { ChapterDef } from "./types";

${imports}

export const CHAPTERS: ChapterDef[] = [
${chDefs}
];`;
}

/* ─── Main runner ─── */

async function generate(p) {
  const presDir = path.join(BASE, p.dir);
  const srcDir = path.join(presDir, "presentation/src");

  // Check this is a scaffold presentation
  if (!fs.existsSync(srcDir)) {
    console.log(`  SKIP: ${p.dir} — no src dir`);
    return;
  }

  // 1. Content files
  const contentDir = presDir;
  fs.writeFileSync(path.join(contentDir, "article.md"), generateArticle(p), "utf-8");
  console.log(`  ✓ article.md`);
  fs.writeFileSync(path.join(contentDir, "outline.md"), generateOutline(p), "utf-8");
  console.log(`  ✓ outline.md`);
  const scriptLines = generateScript(p);
  fs.writeFileSync(path.join(contentDir, "script.md"), scriptLines.join("\n"), "utf-8");
  console.log(`  ✓ script.md`);

  // 2. Chapter files
  const chaptersDir = path.join(srcDir, "chapters");
  const allChapters = [
    { id: "01-coldopen", title: p.title },
    ...(p.chapters || []),
    { id: "06-cta", title: "總結與下一步" },
  ];

  for (let i = 0; i < allChapters.length; i++) {
    const ch = allChapters[i];
    const chDir = path.join(chaptersDir, ch.id);
    if (!fs.existsSync(chDir)) {
      console.log(`  SKIP chapter: ${ch.id} — dir not found`);
      continue;
    }
    const prefix = prefixFromId(ch.id);

    // TSX
    let tsx;
    if (i === 0) tsx = coldopenTSX(p, ch, prefix);
    else if (i === 6) tsx = ctaTSX(p, prefix);
    else tsx = infoTSX(p, ch, prefix, i - 1);

    const compName = i === 0 ? "Coldopen" : i === 6 ? "CTA" : guessComponent(ch.id);
    fs.writeFileSync(path.join(chDir, `${compName}.tsx`), tsx, "utf-8");
    console.log(`  ✓ ${ch.id}/${compName}.tsx`);

    // CSS
    const css = generateCSS(ch, prefix, i);
    const cssName = i === 0 ? "Coldopen" : i === 6 ? "CTA" : compName;
    fs.writeFileSync(path.join(chDir, `${cssName}.css`), css, "utf-8");
    console.log(`  ✓ ${ch.id}/${cssName}.css`);

    // Narrations
    const narr = generateNarrations(ch, i, p);
    fs.writeFileSync(path.join(chDir, "narrations.ts"), narr, "utf-8");
    console.log(`  ✓ ${ch.id}/narrations.ts`);

    // Clean up orphan scaffold files (U*.css artifacts)
    const orphanFiles = fs.readdirSync(chDir).filter((f) => f.startsWith("U") && f.endsWith(".css"));
    for (const of of orphanFiles) {
      fs.unlinkSync(path.join(chDir, of));
    }
  }

  // 3. Registry
  const registryDir = path.join(srcDir, "registry");
  if (fs.existsSync(registryDir)) {
    const reg = generateRegistry(p);
    // Write the imports for all 6 chapters properly
    const allChNames = ["Coldopen", ...(p.chapters || []).slice(0, 5).map((c) => guessComponent(c.id)), "CTA"];
    const importLines = [];
    const defLines = [];
    const allCh2 = [
      { id: "01-coldopen", title: p.title },
      ...(p.chapters || []).slice(0, 5),
      { id: "06-cta", title: "總結與下一步" },
    ];

    for (let i = 0; i < allCh2.length; i++) {
      const ch2 = allCh2[i];
      const cn = allChNames[i];
      const nIdx = String(i + 1).padStart(2, "0");
      importLines.push(`import { ${cn} } from "../chapters/${ch2.id}/${cn}";`);
      importLines.push(`import { NARRATIONS as N${nIdx} } from "../chapters/${ch2.id}/narrations";`);
    }

    for (let i = 0; i < allCh2.length; i++) {
      const ch2 = allCh2[i];
      const nIdx = String(i + 1).padStart(2, "0");
      const cn = allChNames[i];
      defLines.push(`  { id: "${ch2.id}", title: "${ch2.title}", narrations: N${nIdx}, Component: ${cn} },`);
    }

    const regContent = `import type { ChapterDef } from "./types";

${importLines.join("\n")}

export const CHAPTERS: ChapterDef[] = [
${defLines.join("\n")}];`;

    fs.writeFileSync(path.join(registryDir, "chapters.ts"), regContent, "utf-8");
    console.log(`  ✓ registry/chapters.ts`);
  }

  console.log(`✔ Done: ${p.dir}`);
}

async function main() {
  const singleSlug = process.argv[2];
  const targets = singleSlug
    ? PRESENTATIONS.filter((p) => p.dir === singleSlug || p.slug === singleSlug || p.dir === `presentations/${singleSlug}`)
    : PRESENTATIONS;

  if (targets.length === 0) {
    console.error(`No presentation found${singleSlug ? ` for "${singleSlug}"` : ""}`);
    process.exit(1);
  }

  console.log(`Generating ${targets.length} presentation(s)...\n`);

  for (const p of targets) {
    console.log(`\n--- ${p.dir} ---`);
    try {
      await generate(p);
    } catch (err) {
      console.error(`  ERROR: ${err.message}`);
    }
  }

  console.log("\n✔ All done!");
}

main().catch(console.error);