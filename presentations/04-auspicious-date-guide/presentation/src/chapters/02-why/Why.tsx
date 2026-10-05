import "./Why.css";
interface Props { step: number; }

export function Why({ step }: Props) {
  if (step === 0) {
    return (
      <div className="c1-scene">
        <div className="c1-hook">
          <svg viewBox="0 0 80 80" className="c1-hook-icon" width="80" height="80"><rect x="16" y="8" width="48" height="64" rx="4" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><line x1="24" y1="24" x2="56" y2="24" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="34" x2="56" y2="34" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="44" x2="48" y2="44" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/></svg>
          <h1 className="c1-title">為何要揀好日子</h1>
          <p className="c1-sub">了解為何要揀好日子的重點</p>
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
            <span className="c1-number-appear">4. 宜嫁娶的吉日需要配合雙方八字</span>
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
        <h2 className="c1-card-title">為何要揀好日子</h2>
        <div className="c1-list">
          <div className="c1-list-item" style={{ animationDelay: `${0}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>傳統習俗認為吉日結婚可增添福氣</span>
          </div>
          <div className="c1-list-item" style={{ animationDelay: `${100}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>父母長輩通常有特定要求或期望</span>
          </div>
          <div className="c1-list-item" style={{ animationDelay: `${200}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>農曆新年、端午等節日較多人結婚</span>
          </div>
          <div className="c1-list-item" style={{ animationDelay: `${300}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>宜嫁娶的吉日需要配合雙方八字</span>
          </div>
          <div className="c1-list-item" style={{ animationDelay: `${400}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>避開農曆七月等傳統禁忌月份</span>
          </div>
        </div>
      </div>
    </div>
  );
}