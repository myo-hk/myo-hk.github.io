import "./After.css";

interface Props {
  step: number;
}

const TODO_ITEMS = [
  { label: "身份證更新", detail: "HK$460", sub: "帶結婚證書正本" },
  { label: "核證副本", detail: "HK$425/份", sub: "遺失可補領" },
  { label: "免稅額", detail: "HK$264,000", sub: "2025/26 年度" },
  { label: "證書用途", detail: "貸款·遺產·入學", sub: "妥善保存" },
];

const RECAP_STEPS = [
  "確認資格",
  "準備文件",
  "交通知書",
  "揀場地",
  "婚禮+婚後",
];

export default function After({ step }: Props) {
  if (step === 0) {
    return (
      <div className="af-scene">
        <div className="af-label">婚後待辦事項</div>
        <div className="af-cards-grid">
          {TODO_ITEMS.map((item, i) => (
            <div
              key={item.label}
              className="af-card"
              style={{ animationDelay: `${i * 200}ms` }}
            >
              <div className="af-card-icon">
                {i === 0 && (
                  <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
                    <rect x="8" y="6" width="24" height="28" rx="3" stroke="var(--accent)" strokeWidth="2" fill="none" />
                    <circle cx="20" cy="18" r="4" stroke="var(--accent)" strokeWidth="1.5" fill="none" />
                    <path d="M14 30 Q20 26 26 30" stroke="var(--accent)" strokeWidth="1.5" fill="none" />
                  </svg>
                )}
                {i === 1 && (
                  <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
                    <rect x="6" y="8" width="28" height="24" rx="2" stroke="var(--accent)" strokeWidth="2" fill="none" />
                    <path d="M14 16 L20 22 L26 16" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" fill="none" />
                    <line x1="20" y1="22" x2="20" y2="30" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" />
                  </svg>
                )}
                {i === 2 && (
                  <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
                    <circle cx="20" cy="20" r="14" stroke="var(--accent)" strokeWidth="2" fill="none" />
                    <path d="M20 12 L20 28" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" />
                    <path d="M14 18 Q20 14 26 18" stroke="var(--accent)" strokeWidth="2" fill="none" strokeLinecap="round" />
                  </svg>
                )}
                {i === 3 && (
                  <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
                    <rect x="6" y="10" width="28" height="20" rx="2" stroke="var(--accent)" strokeWidth="2" fill="none" />
                    <line x1="10" y1="16" x2="30" y2="16" stroke="var(--accent)" strokeWidth="1.5" />
                    <line x1="10" y1="22" x2="24" y2="22" stroke="var(--accent)" strokeWidth="1.5" />
                    <line x1="10" y1="26" x2="18" y2="26" stroke="var(--accent)" strokeWidth="1.5" />
                  </svg>
                )}
              </div>
              <div className="af-card-body">
                <span className="af-card-label">{item.label}</span>
                <span className="af-card-detail">{item.detail}</span>
                <span className="af-card-sub">{item.sub}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="af-scene">
        <div className="af-numbers-row">
          <div className="af-number-card">
            <div className="af-num-label">身份證更新</div>
            <div className="af-num-value hero-num">HK$460</div>
            <div className="af-num-sub">帶結婚證書正本</div>
          </div>
          <div className="af-number-card af-number-card-late">
            <div className="af-num-label">已婚免稅額</div>
            <div className="af-num-value hero-num">HK$264,000</div>
            <div className="af-num-sub">2025/26 年度 · 合併報稅更划算</div>
          </div>
        </div>
      </div>
    );
  }

  if (step === 2) {
    return (
      <div className="af-scene">
        <div className="af-label">結婚證書用途</div>
        <div className="af-scenes-row">
          <div className="af-scene-card">
            <svg width="64" height="64" viewBox="0 0 64 64" fill="none" className="af-scene-icon">
              <rect x="12" y="16" width="40" height="32" rx="4" stroke="var(--accent)" strokeWidth="2" fill="none" />
              <rect x="20" y="24" width="24" height="16" rx="2" stroke="var(--accent)" strokeWidth="1.5" fill="none" />
              <path d="M28 32 L32 36 L36 28" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              <line x1="32" y1="40" x2="32" y2="46" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" />
            </svg>
            <span className="af-scene-label">申請貸款</span>
            <span className="af-scene-sub">銀行核實婚姻狀況</span>
          </div>
          <div className="af-scene-card">
            <svg width="64" height="64" viewBox="0 0 64 64" fill="none" className="af-scene-icon">
              <rect x="14" y="12" width="36" height="40" rx="3" stroke="var(--accent)" strokeWidth="2" fill="none" />
              <path d="M22 28 L32 20 L42 28" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              <line x1="32" y1="20" x2="32" y2="42" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" />
              <line x1="22" y1="42" x2="42" y2="42" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" />
            </svg>
            <span className="af-scene-label">辦理遺產</span>
            <span className="af-scene-sub">配偶繼承權證明</span>
          </div>
          <div className="af-scene-card">
            <svg width="64" height="64" viewBox="0 0 64 64" fill="none" className="af-scene-icon">
              <path d="M32 12 L12 28 L20 28 L20 50 L44 50 L44 28 L52 28 Z" stroke="var(--accent)" strokeWidth="2" strokeLinejoin="round" fill="none" />
              <rect x="26" y="34" width="12" height="16" rx="1" stroke="var(--accent)" strokeWidth="1.5" fill="none" />
              <line x1="32" y1="34" x2="32" y2="50" stroke="var(--accent)" strokeWidth="1.5" />
            </svg>
            <span className="af-scene-label">子女入學</span>
            <span className="af-scene-sub">父母婚姻證明</span>
          </div>
        </div>
      </div>
    );
  }

  if (step === 3) {
    return (
      <div className="af-scene">
        <div className="af-finale">
          <div className="af-total-section">
            <div className="af-total-label">總費用（最平方案）</div>
            <div className="af-total-value hero-num">HK$1,020</div>
            <div className="af-total-breakdown">
              <span>通知書 HK$305</span>
              <span className="af-plus">+</span>
              <span><span>登記處結婚 HK$715</span></span>
            </div>
          </div>

          <div className="af-recap">
            <div className="af-recap-label">五步搞掂</div>
            <div className="af-recap-steps">
              {RECAP_STEPS.map((s, i) => (
                <div key={s} className="af-recap-step">
                  <span className="af-recap-num">{String(i + 1).padStart(2, "0")}</span>
                  <span className="af-recap-name">{s}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="af-cta">
            <div className="af-cta-text">超過 400 篇香港婚禮教學文章</div>
            <a
              href="https://myo-makeyourown.pages.dev"
              target="_blank"
              rel="noopener noreferrer"
              className="af-cta-link"
              data-no-advance
            >
              <span>myo-makeyourown.pages.dev</span>
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" className="af-cta-arrow">
                <path d="M5 10 L13 10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                <path d="M10 5 L15 10 L10 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </a>
          </div>
        </div>
      </div>
    );
  }

  return null;
}