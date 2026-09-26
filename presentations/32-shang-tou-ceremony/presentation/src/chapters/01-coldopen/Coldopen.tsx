import "./Coldopen.css";
interface Props { step: number; }

const CATEGORIES = ["習俗意義", "時間安排", "禮儀規範", "05 steps"];

export function Coldopen({ step }: Props) {
  if (step === 0) {
    return (
      <div className="co-scene">
        <div className="co-hook">
          <svg viewBox="0 0 80 80" className="co-hook-icon" width="80" height="80"><circle cx="40" cy="40" r="36" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><path d="M24 40l12 12 20-20" stroke="var(--accent)" strokeWidth="4" fill="none" strokeLinecap="round" strokeLinejoin="round"/></svg>
          <h1 className="co-title">上頭儀式指南</h1>
          <p className="co-sub">上頭儀式係傳統婚禮習俗。等我介紹上頭嘅意義、時間同步驟。</p>
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
            <span className="co-number-appear">10+</span>
            <span className="co-rule" />
          </div>
          <span className="co-number-label">步驟</span>
          <span className="co-number-sub">傳統儀式</span>
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