import "./Church.css";
interface Props { step: number; }

export function Church({ step }: Props) {
  if (step === 0) {
    return (
      <div className="c3-scene">
        <div className="c3-hook">
          <svg viewBox="0 0 80 80" className="c3-hook-icon" width="80" height="80"><rect x="16" y="8" width="48" height="64" rx="4" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><line x1="24" y1="24" x2="56" y2="24" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="34" x2="56" y2="34" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="44" x2="48" y2="44" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/></svg>
          <h1 className="c3-title">教堂結婚</h1>
          <p className="c3-sub">教堂婚禮有氣氛兼有宗教意義，但需提早預約</p>
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
            <span className="c3-number-appear">$5K-20K</span>
            <span className="c3-rule" />
          </div>
          <span className="c3-number-label">教堂場地費</span>
          <span className="c3-number-sub">視乎教堂及牧師安排</span>
        </div>
      </div>
    );
  }

  return (
    <div className="c3-scene">
      <div className="c3-card">
        <h2 className="c3-card-title">教堂結婚特點</h2>
        <div className="c3-list">
          <div className="c3-list-item" style={{ animationDelay: `${0}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>聖約翰座堂、循道衛理等熱門教堂需排期</span>
          </div>
          <div className="c3-list-item" style={{ animationDelay: `${100}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>需先成為教會會友或符合教堂要求</span>
          </div>
          <div className="c3-list-item" style={{ animationDelay: `${200}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>儀式莊嚴，有詩歌和牧師證婚</span>
          </div>
          <div className="c3-list-item" style={{ animationDelay: `${300}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>通常需在政府登記處先完成法律程序</span>
          </div>
          <div className="c3-list-item" style={{ animationDelay: `${400}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>可容納較多親友，適合大型婚禮</span>
          </div>
        </div>
      </div>
    </div>
  );
}