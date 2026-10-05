import "./Cost3Photo.css";
interface Props { step: number; }

export function Cost3Photo({ step }: Props) {
  if (step === 0) {
    return (
      <div className="c3-scene">
        <div className="c3-hook">
          <svg viewBox="0 0 80 80" className="c3-hook-icon" width="80" height="80">
            <rect x="14" y="22" width="52" height="38" rx="6" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)" />
            <circle cx="40" cy="38" r="8" stroke="var(--accent)" strokeWidth="2" />
            <circle cx="40" cy="38" r="3" fill="var(--accent)" />
            <path d="M14 30l12-8h6l4-4h8l4 4h6l12 8" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
            <circle cx="56" cy="28" r="3" fill="var(--accent)" />
          </svg>
          <h1 className="c3-title">攝影費用</h1>
          <p className="c3-sub">記錄大日子嘅重要投資・約佔總預算 7%</p>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="c3-scene">
        <div className="c3-number-block">
          <div className="c3-highlight-bar">
            <span className="c3-rule" />
            <span className="c3-number-appear">$15K-35K</span>
            <span className="c3-rule" />
          </div>
          <span className="c3-number-label">婚禮攝影套餐</span>
          <span className="c3-number-sub">包括攝影師 + 錄影師全日服務</span>
        </div>
      </div>
    );
  }

  return (
    <div className="c3-scene">
      <div className="c3-card" style={{ animationDelay: "100ms" }}>
        <h2 className="c3-card-title">套餐包括</h2>
        <div className="c3-list">
          <div className="c3-list-item" style={{ animationDelay: "180ms" }}>
            <svg viewBox="0 0 24 24" width="20" height="20"><circle cx="12" cy="12" r="10" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" /><path d="M8 12l3 3 5-5" stroke="var(--accent)" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg>
            <span>全日婚禮拍攝（8-10 小時）</span>
          </div>
          <div className="c3-list-item" style={{ animationDelay: "260ms" }}>
            <svg viewBox="0 0 24 24" width="20" height="20"><circle cx="12" cy="12" r="10" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" /><path d="M8 12l3 3 5-5" stroke="var(--accent)" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg>
            <span>專業錄影同後期剪接</span>
          </div>
          <div className="c3-list-item" style={{ animationDelay: "340ms" }}>
            <svg viewBox="0 0 24 24" width="20" height="20"><circle cx="12" cy="12" r="10" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" /><path d="M8 12l3 3 5-5" stroke="var(--accent)" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" /></svg>
            <span>實體相簿（30-50 頁）</span>
          </div>
        </div>
      </div>
    </div>
  );
}