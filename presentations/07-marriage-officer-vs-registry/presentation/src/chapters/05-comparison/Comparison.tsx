import "./Comparison.css";
interface Props { step: number; }

export function Comparison({ step }: Props) {
  if (step === 0) {
    return (
      <div className="c4-scene">
        <div className="c4-hook">
          <svg viewBox="0 0 80 80" className="c4-hook-icon" width="80" height="80"><rect x="16" y="8" width="48" height="64" rx="4" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><line x1="24" y1="24" x2="56" y2="24" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="34" x2="56" y2="34" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="44" x2="48" y2="44" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/></svg>
          <h1 className="c4-title">比較與選擇</h1>
          <p className="c4-sub">幫你分析邊種結婚方式最適合</p>
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
            <span className="c4-number-appear">$715 起</span>
            <span className="c4-rule" />
          </div>
          <span className="c4-number-label">總費用比較</span>
          <span className="c4-number-sub">視乎選擇方式</span>
        </div>
      </div>
    );
  }

  return (
    <div className="c4-scene">
      <div className="c4-card">
        <h2 className="c4-card-title">三種方式邊個適合你</h2>
        <div className="c4-list">
          <div className="c4-list-item" style={{ animationDelay: `${0}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>預算有限→選婚姻登記處，費用最平</span>
          </div>
          <div className="c4-list-item" style={{ animationDelay: `${100}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>想要彈性→揀監禮人，日時地點自選</span>
          </div>
          <div className="c4-list-item" style={{ animationDelay: `${200}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>想要氣氛→揀教堂，莊嚴浪漫</span>
          </div>
          <div className="c4-list-item" style={{ animationDelay: `${300}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>需提前預訂，熱門日子半年前就要開始</span>
          </div>
          <div className="c4-list-item" style={{ animationDelay: `${400}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>三者都需要向入境事務處遞交通知書</span>
          </div>
        </div>
      </div>
    </div>
  );
}