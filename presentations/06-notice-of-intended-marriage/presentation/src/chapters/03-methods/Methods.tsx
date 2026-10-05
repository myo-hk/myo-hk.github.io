import "./Methods.css";
interface Props { step: number; }

export function Methods({ step }: Props) {
  if (step === 0) {
    return (
      <div className="c2-scene">
        <div className="c2-hook">
          <svg viewBox="0 0 80 80" className="c2-hook-icon" width="80" height="80"><rect x="16" y="8" width="48" height="64" rx="4" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><line x1="24" y1="24" x2="56" y2="24" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="34" x2="56" y2="34" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="44" x2="48" y2="44" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/></svg>
          <h1 className="c2-title">遞交方式</h1>
          <p className="c2-sub">了解遞交通知書嘅線上同線下方法</p>
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
            <span className="c2-number-appear">4. 填寫指定表格</span>
            <span className="c2-rule" />
          </div>
          <span className="c2-number-label">星評價</span>
          <span className="c2-number-sub">新人推薦</span>
        </div>
      </div>
    );
  }

  return (
    <div className="c2-scene">
      <div className="c2-card">
        <h2 className="c2-card-title">遞交方式</h2>
        <div className="c2-list">
          <div className="c2-list-item" style={{ animationDelay: `${0}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>親身前往婚姻登記處遞交</span>
          </div>
          <div className="c2-list-item" style={{ animationDelay: `${100}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>經網上預約系統提交申請</span>
          </div>
          <div className="c2-list-item" style={{ animationDelay: `${200}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>授權香港以外嘅婚姻監禮人辦理</span>
          </div>
          <div className="c2-list-item" style={{ animationDelay: `${300}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>遞交後可選擇婚禮日期同地點</span>
          </div>
          <div className="c2-list-item" style={{ animationDelay: `${400}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>遞交後最少15日方可舉行婚禮</span>
          </div>
        </div>
      </div>
    </div>
  );
}