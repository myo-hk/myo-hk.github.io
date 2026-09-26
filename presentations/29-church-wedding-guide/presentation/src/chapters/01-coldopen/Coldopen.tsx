import "./Coldopen.css";
interface Props { step: number; }

const CATEGORIES = ["預訂流程", "婚禮儀式", "接待安排", "05 dress"];

export function Coldopen({ step }: Props) {
  if (step === 0) {
    return (
      <div className="co-scene">
        <div className="co-hook">
          <svg viewBox="0 0 80 80" className="co-hook-icon" width="80" height="80"><circle cx="40" cy="40" r="36" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><path d="M24 40l12 12 20-20" stroke="var(--accent)" strokeWidth="4" fill="none" strokeLinecap="round" strokeLinejoin="round"/></svg>
          <h1 className="co-title">教堂婚禮指南</h1>
          <p className="co-sub">教堂婚禮莊嚴浪漫。等我介紹香港教堂婚禮流程、服飾同注意事項。</p>
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
            <span className="co-number-appear">HKk</span>
            <span className="co-rule" />
          </div>
          <span className="co-number-label">教堂婚禮費用</span>
          <span className="co-number-sub">視乎教堂</span>
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