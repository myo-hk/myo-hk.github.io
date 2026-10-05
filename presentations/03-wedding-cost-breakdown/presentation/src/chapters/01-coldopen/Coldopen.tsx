import "./Coldopen.css";
interface Props { step: number; }

const CATEGORIES = ["註冊", "婚戒", "攝影", "婚宴", "其他"];

export function Coldopen({ step }: Props) {
  if (step === 0) {
    return (
      <div className="co-scene">
        <div className="co-hook">
          <svg viewBox="0 0 80 80" className="co-hook-icon" width="80" height="80">
            <circle cx="40" cy="40" r="36" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)" />
            <path d="M26 44l6 6 14-18" stroke="var(--accent)" strokeWidth="4" fill="none" strokeLinecap="round" strokeLinejoin="round" />
            <text x="40" y="52" textAnchor="middle" fill="var(--accent)" fontSize="16" fontWeight="700" fontFamily="var(--font-display-en)">$</text>
          </svg>
          <h1 className="co-title">結婚要幾錢？</h1>
          <p className="co-sub">逐項拆解結婚開支・等你 budget 規劃得更清晰</p>
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
            <span className="co-number-appear">36 萬</span>
            <span className="co-rule" />
          </div>
          <span className="co-number-label">香港結婚平均開支</span>
          <span className="co-number-sub">2024 年最新數據・由 20 萬到 50 萬不等</span>
        </div>
      </div>
    );
  }

  return (
    <div className="co-scene">
      <h2 className="co-preview-title">5 大開支類別</h2>
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