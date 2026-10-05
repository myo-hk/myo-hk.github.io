import "./CTA.css";
interface Props { step: number; }

export function CTA({ step }: Props) {
  if (step === 0) {
    return (
      <div className="ct-scene">
        <div className="ct-hook">
          <svg viewBox="0 0 80 80" className="ct-hook-icon" width="80" height="80"><rect x="16" y="8" width="48" height="64" rx="4" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><line x1="24" y1="24" x2="56" y2="24" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="34" x2="56" y2="34" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="44" x2="48" y2="44" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/></svg>
          <h1 className="ct-title">總結與下一步</h1>
          <p className="ct-sub">準備好就開始你嘅結婚籌備旅程</p>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="ct-scene">
        <div className="ct-number-block">
          <div className="ct-highlight-bar">
            <span className="ct-rule" />
            <span className="ct-number-appear">$3K-8K</span>
            <span className="ct-rule" />
          </div>
          <span className="ct-number-label">擇日費用參考</span>
          <span className="ct-number-sub">視平師傅經驗及名氣</span>
        </div>
      </div>
    );
  }

  return (
    <div className="ct-scene">
      <div className="ct-card-grid">

      </div>
    </div>
  );
}