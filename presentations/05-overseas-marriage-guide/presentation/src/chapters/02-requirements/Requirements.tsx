import "./Requirements.css";
interface Props { step: number; }

export function Requirements({ step }: Props) {
  if (step === 0) {
    return (
      <div className="c1-scene">
        <div className="c1-hook">
          <svg viewBox="0 0 80 80" className="c1-hook-icon" width="80" height="80"><rect x="16" y="8" width="48" height="64" rx="4" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><line x1="24" y1="24" x2="56" y2="24" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="34" x2="56" y2="34" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="44" x2="48" y2="44" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/></svg>
          <h1 className="c1-title">申請資格</h1>
          <p className="c1-sub">了解申請資格的重點</p>
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
            <span className="c1-number-appear">4. 無現存婚姻</span>
            <span className="c1-rule" />
          </div>
          <span className="c1-number-label">星評價</span>
          <span className="c1-number-sub">新人推薦</span>
        </div>
      </div>
    );
  }

  return (
    <div className="c1-scene">
      <div className="c1-card">
        <h2 className="c1-card-title">申請資格</h2>
        <div className="c1-list">
          <div className="c1-list-item" style={{ animationDelay: `${0}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>雙方年滿16歲</span>
          </div>
          <div className="c1-list-item" style={{ animationDelay: `${100}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>無血緣關係限制</span>
          </div>
          <div className="c1-list-item" style={{ animationDelay: `${200}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>符合目的地結婚要求</span>
          </div>
          <div className="c1-list-item" style={{ animationDelay: `${300}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>單身證明文件齊全</span>
          </div>
          <div className="c1-list-item" style={{ animationDelay: `${400}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>無未解除嘅婚姻關係</span>
          </div>
        </div>
      </div>
    </div>
  );
}