import "./Cost2Ring.css";
interface Props { step: number; }

export function Cost2Ring({ step }: Props) {
  if (step === 0) {
    return (
      <div className="c2-scene">
        <div className="c2-hook">
          <svg viewBox="0 0 80 80" className="c2-hook-icon" width="80" height="80">
            <circle cx="40" cy="40" r="24" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)" />
            <circle cx="40" cy="40" r="10" stroke="var(--accent)" strokeWidth="2" fill="var(--accent)" />
            <path d="M40 16l8 8M40 16l-8 8" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" />
            <path d="M28 52l-8 8M52 52l8 8" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" />
          </svg>
          <h1 className="c2-title">婚戒預算</h1>
          <p className="c2-sub">第二大成開支・約佔總預算 11%</p>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="c2-scene">
        <div className="c2-number-block">
          <div className="c2-highlight-bar">
            <span className="c2-rule" />
            <span className="c2-number-appear">$10K-50K</span>
            <span className="c2-rule" />
          </div>
          <span className="c2-number-label">一對結婚戒指價格</span>
          <span className="c2-number-sub">視乎品牌、款式同材質</span>
        </div>
      </div>
    );
  }

  return (
    <div className="c2-scene">
      <div className="c2-card" style={{ animationDelay: "100ms" }}>
        <h2 className="c2-card-title">鑽石 vs 素色戒指</h2>
        <div className="c2-compare">
          <div className="c2-compare-item">
            <svg viewBox="0 0 32 32" width="28" height="28">
              <polygon points="16,4 20,12 16,24 12,12" fill="var(--accent)" opacity="0.4" />
              <polygon points="16,4 20,12 28,12 16,28" fill="var(--accent)" opacity="0.6" />
              <polygon points="16,4 12,12 4,12 16,28" fill="var(--accent)" opacity="0.8" />
            </svg>
            <span className="c2-compare-label">鑽石戒指</span>
            <span className="c2-compare-value">視乎 4C 級別</span>
          </div>
          <div className="c2-compare-divider" />
          <div className="c2-compare-item">
            <svg viewBox="0 0 32 32" width="28" height="28">
              <circle cx="16" cy="16" r="10" stroke="var(--accent)" strokeWidth="2" fill="none" />
            </svg>
            <span className="c2-compare-label">素色戒指</span>
            <span className="c2-compare-value">約 HK$3,000 起（素圈）</span>
          </div>
        </div>
      </div>
    </div>
  );
}