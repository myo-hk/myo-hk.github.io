import "./Cost4Banquet.css";
interface Props { step: number; }

export function Cost4Banquet({ step }: Props) {
  if (step === 0) {
    return (
      <div className="c4-scene">
        <div className="c4-hook">
          <svg viewBox="0 0 80 80" className="c4-hook-icon" width="80" height="80">
            <rect x="16" y="28" width="48" height="36" rx="8" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)" />
            <path d="M24 18l4-6M40 18l4-6M56 18l4-6" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" />
            <circle cx="32" cy="44" r="3" fill="var(--accent)" />
            <circle cx="48" cy="44" r="3" fill="var(--accent)" />
            <path d="M30 52q10 6 20 0" stroke="var(--accent)" strokeWidth="2" fill="none" strokeLinecap="round" />
          </svg>
          <h1 className="c4-title">婚宴開支</h1>
          <p className="c4-sub">最大筆開支・佔總預算約 50%</p>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="c4-scene">
        <div className="c4-number-block">
          <div className="c4-highlight-bar">
            <span className="c4-rule" />
            <span className="c4-number-appear">$10K-15K</span>
            <span className="c4-rule" />
          </div>
          <span className="c4-number-label">酒店婚宴每圍價錢</span>
          <span className="c4-number-sub">視乎酒店星級同菜單選擇</span>
        </div>
      </div>
    );
  }

  return (
    <div className="c4-scene">
      <div className="c4-card" style={{ animationDelay: "100ms" }}>
        <h2 className="c4-card-title">酒店 vs 酒樓</h2>
        <div className="c4-compare">
          <div className="c4-compare-item">
            <svg viewBox="0 0 40 40" width="36" height="36">
              <rect x="8" y="16" width="24" height="20" rx="4" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
              <path d="M14 8l6-4 6 4" stroke="var(--accent)" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
              <rect x="16" y="10" width="8" height="6" stroke="var(--accent)" strokeWidth="1.5" fill="var(--accent-soft)" />
            </svg>
            <span className="c4-compare-label">酒店婚宴</span>
            <span className="c4-compare-value">HK$10,000 - 15,000</span>
          </div>
          <div className="c4-compare-divider" />
          <div className="c4-compare-item">
            <svg viewBox="0 0 40 40" width="36" height="36">
              <rect x="8" y="16" width="24" height="20" rx="4" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
              <circle cx="20" cy="26" r="4" stroke="var(--accent)" strokeWidth="2" />
              <path d="M14 12l6-4 6 4" stroke="var(--accent)" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <span className="c4-compare-label">酒樓婚宴</span>
            <span className="c4-compare-value">HK$6,000 - 10,000</span>
          </div>
        </div>
      </div>
    </div>
  );
}