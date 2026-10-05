import "./Cost1Registration.css";
interface Props { step: number; }

export function Cost1Registration({ step }: Props) {
  if (step === 0) {
    return (
      <div className="c1-scene">
        <div className="c1-hook">
          <svg viewBox="0 0 80 80" className="c1-hook-icon" width="80" height="80">
            <rect x="20" y="12" width="40" height="56" rx="4" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)" />
            <path d="M28 28h24M28 40h24M28 52h16" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" />
            <circle cx="58" cy="56" r="14" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
            <path d="M52 56l4 4 8-8" stroke="var(--accent)" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          <h1 className="c1-title">註冊費用</h1>
          <p className="c1-sub">了解註冊費用的重點</p>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="c1-scene">
        <div className="c1-number-block">
          <div className="c1-highlight-bar">
            <span className="c1-rule" />
            <span className="c1-number-appear">HK$305</span>
            <span className="c1-rule" />
          </div>
          <span className="c1-number-label">擬結婚通知書費用</span>
          <span className="c1-number-sub">結婚嘅第一步・法定必備文件</span>
        </div>
      </div>
    );
  }

  return (
    <div className="c1-scene">
      <div className="c1-card" style={{ animationDelay: "100ms" }}>
        <h2 className="c1-card-title">註冊費用</h2>
        <div className="c1-compare">
          <div className="c1-compare-item">
            <span className="c1-compare-label">婚姻登記處</span>
            <span className="c1-compare-value">HK$715</span>
          </div>
          <div className="c1-compare-divider" />
          <div className="c1-compare-item">
            <span className="c1-compare-label">特許監禮人到場</span>
            <span className="c1-compare-value">HK$2,000 - 5,000</span>
          </div>
        </div>
      </div>
    </div>
  );
}