import "./Fitting.css";
interface Props { step: number; }

export function Fitting({ step }: Props) {
  if (step === 0) {
    return (
      <div className="c3-scene">
        <div className="c3-hook">
          <svg viewBox="0 0 80 80" className="c3-hook-icon" width="80" height="80"><rect x="16" y="8" width="48" height="64" rx="4" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><line x1="24" y1="24" x2="56" y2="24" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="34" x2="56" y2="34" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="44" x2="48" y2="44" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/></svg>
          <h1 className="c3-title">合身調整</h1>
          <p className="c3-sub">了解證書套嘅合身調整方法</p>
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
            <span className="c3-number-appear">4. 磁石扣更穩陣</span>
            <span className="c3-rule" />
          </div>
          <span className="c3-number-label">星評價</span>
          <span className="c3-number-sub">新人推薦</span>
        </div>
      </div>
    );
  }

  return (
    <div className="c3-scene">
      <div className="c3-card">
        <h2 className="c3-card-title">合身調整</h2>
        <div className="c3-list">
          <div className="c3-list-item" style={{ animationDelay: `${0}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>證書套太鬆嘅解決方法</span>
          </div>
          <div className="c3-list-item" style={{ animationDelay: `${100}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>證書套太緊嘅處理技巧</span>
          </div>
          <div className="c3-list-item" style={{ animationDelay: `${200}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>加厚內頁嘅調整方式</span>
          </div>
          <div className="c3-list-item" style={{ animationDelay: `${300}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>多張證書嘅擺放方法</span>
          </div>
          <div className="c3-list-item" style={{ animationDelay: `${400}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>完美合身嘅檢查清單</span>
          </div>
        </div>
      </div>
    </div>
  );
}