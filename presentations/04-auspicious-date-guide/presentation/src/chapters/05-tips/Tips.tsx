import "./Tips.css";
interface Props { step: number; }

export function Tips({ step }: Props) {
  if (step === 0) {
    return (
      <div className="c4-scene">
        <div className="c4-hook">
          <svg viewBox="0 0 80 80" className="c4-hook-icon" width="80" height="80"><rect x="16" y="8" width="48" height="64" rx="4" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><line x1="24" y1="24" x2="56" y2="24" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="34" x2="56" y2="34" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="44" x2="48" y2="44" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/></svg>
          <h1 className="c4-title">揀日技巧</h1>
          <p className="c4-sub">實用建議幫你揀到又合八字又稱心嘅結婚吉日</p>
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
            <span className="c4-number-appear">4. 親友日程先確認</span>
            <span className="c4-rule" />
          </div>
          <span className="c4-number-label">星評價</span>
          <span className="c4-number-sub">新人推薦</span>
        </div>
      </div>
    );
  }

  return (
    <div className="c4-scene">
      <div className="c4-card">
        <h2 className="c4-card-title">揀日技巧同注意事項</h2>
        <div className="c4-list">
          <div className="c4-list-item" style={{ animationDelay: `${0}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>提前同雙方家長溝通，避免日子衝突</span>
          </div>
          <div className="c4-list-item" style={{ animationDelay: `${100}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>預算有限可考慮平日或淡季日子</span>
          </div>
          <div className="c4-list-item" style={{ animationDelay: `${200}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>場地預訂要配合吉日，提前一年較穩陣</span>
          </div>
          <div className="c4-list-item" style={{ animationDelay: `${300}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>如果師傅揀的日子唔合意，可再傾</span>
          </div>
          <div className="c4-list-item" style={{ animationDelay: `${400}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>最重要雙方同意，風水只是參考</span>
          </div>
        </div>
      </div>
    </div>
  );
}