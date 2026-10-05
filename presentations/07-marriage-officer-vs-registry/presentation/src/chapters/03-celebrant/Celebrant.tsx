import "./Celebrant.css";
interface Props { step: number; }

export function Celebrant({ step }: Props) {
  if (step === 0) {
    return (
      <div className="c2-scene">
        <div className="c2-hook">
          <svg viewBox="0 0 80 80" className="c2-hook-icon" width="80" height="80"><rect x="16" y="8" width="48" height="64" rx="4" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><line x1="24" y1="24" x2="56" y2="24" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="34" x2="56" y2="34" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="44" x2="48" y2="44" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/></svg>
          <h1 className="c2-title">監禮人結婚</h1>
          <p className="c2-sub">聘請婚姻監禮人到場見證，彈性更大</p>
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
            <span className="c2-number-appear">$2K-5K</span>
            <span className="c2-rule" />
          </div>
          <span className="c2-number-label">監禮人費用</span>
          <span className="c2-number-sub">視乎經驗及名氣</span>
        </div>
      </div>
    );
  }

  return (
    <div className="c2-scene">
      <div className="c2-card">
        <h2 className="c2-card-title">婚姻監禮人特點</h2>
        <div className="c2-list">
          <div className="c2-list-item" style={{ animationDelay: `${0}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>任何18歲以上人士都可擔任監禮人</span>
          </div>
          <div className="c2-list-item" style={{ animationDelay: `${100}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>可以係親友、牧師或專業證婚人</span>
          </div>
          <div className="c2-list-item" style={{ animationDelay: `${200}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>可選擇在任何日子和地點舉行婚禮</span>
          </div>
          <div className="c2-list-item" style={{ animationDelay: `${300}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>需先向婚姻登記處遞交結婚通知書</span>
          </div>
          <div className="c2-list-item" style={{ animationDelay: `${400}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>儀式時間地點更自由靈活</span>
          </div>
        </div>
      </div>
    </div>
  );
}