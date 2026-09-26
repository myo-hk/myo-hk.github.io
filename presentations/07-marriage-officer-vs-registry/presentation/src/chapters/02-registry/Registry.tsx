import "./Registry.css";
interface Props { step: number; }

export function Registry({ step }: Props) {
  if (step === 0) {
    return (
      <div className="c1-scene">
        <div className="c1-hook">
          <svg viewBox="0 0 80 80" className="c1-hook-icon" width="80" height="80"><rect x="16" y="8" width="48" height="64" rx="4" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><line x1="24" y1="24" x2="56" y2="24" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="34" x2="56" y2="34" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="44" x2="48" y2="44" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/></svg>
          <h1 className="c1-title">登記處結婚</h1>
          <p className="c1-sub">了解登記處結婚的重點</p>
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
            <span className="c1-number-appear">$715</span>
            <span className="c1-rule" />
          </div>
          <span className="c1-number-label">登記處基本費用</span>
          <span className="c1-number-sub">監禮人另加 $2,000-$5,000</span>
        </div>
      </div>
    );
  }

  return (
    <div className="c1-scene">
      <div className="c1-card">
        <h2 className="c1-card-title">登記處結婚</h2>
        <div className="c1-list">
          <div className="c1-list-item" style={{ animationDelay: `${0}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>香港大會堂同紅棉道婚姻登記處最熱門</span>
          </div>
          <div className="c1-list-item" style={{ animationDelay: `${100}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>遞交「結婚通知書」後需等15天冷靜期</span>
          </div>
          <div className="c1-list-item" style={{ animationDelay: `${200}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>婚禮必須在遞交通知書後15天內舉行</span>
          </div>
          <div className="c1-list-item" style={{ animationDelay: `${300}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>需聘請婚姻監禮人在場主持儀式</span>
          </div>
          <div className="c1-list-item" style={{ animationDelay: `${400}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>簡潔正式，適合小型家庭婚禮</span>
          </div>
        </div>
      </div>
    </div>
  );
}