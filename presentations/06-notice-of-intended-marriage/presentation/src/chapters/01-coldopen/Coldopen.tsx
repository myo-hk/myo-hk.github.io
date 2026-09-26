import "./Coldopen.css";
interface Props { step: number; }

const CATEGORIES = ["申請資格", "遞交方式", "費用說明", "展示通知書"];

export function Coldopen({ step }: Props) {
  if (step === 0) {
    return (
      <div className="co-scene">
        <div className="co-hook">
          <svg viewBox="0 0 80 80" className="co-hook-icon" width="80" height="80"><circle cx="40" cy="40" r="36" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><path d="M24 40l12 12 20-20" stroke="var(--accent)" strokeWidth="4" fill="none" strokeLinecap="round" strokeLinejoin="round"/></svg>
          <h1 className="co-title">擬結婚通知書</h1>
          <p className="co-sub">擬結婚通知書係註冊第一步。等我話你知遞交通知書嘅程序同費用。</p>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="co-scene">
        <div className="co-number-block">
          <div className="co-highlight-bar">
            <span className="co-rule" />
            <span className="co-number-appear">HK$305</span>
            <span className="co-rule" />
          </div>
          <span className="co-number-label">擬結婚通知書費用</span>
          <span className="co-number-sub">遞交後 15 天方可舉行婚禮</span>
        </div>
      </div>
    );
  }

  return (
    <div className="co-scene">
      <h2 className="co-preview-title">主要環節</h2>
      <div className="co-preview-grid">
        {CATEGORIES.map((cat, i) => (
          <div key={i} className="co-preview-card" style={{ animationDelay: `${i * 80}ms` }}>
            {cat}
          </div>
        ))}
      </div>
    </div>
  );
}