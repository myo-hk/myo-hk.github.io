import "./Budget.css";

interface Props { step: number; }

const COSTS = [
  { label: "婚宴", amount: "HK$180,000", pct: "50%" },
  { label: "婚戒", amount: "HK$40,000", pct: "11%" },
  { label: "婚紗攝影", amount: "HK$25,000", pct: "7%" },
  { label: "婚紗禮服", amount: "HK$20,000", pct: "6%" },
  { label: "其他", amount: "HK$95,000", pct: "26%" },
];

export function Budget({ step }: Props) {
  if (step === 0) {
    return (
      <div className="bg-scene">
        <div className="bg-hook">
          <svg viewBox="0 0 80 80" className="bg-hook-icon" width="80" height="80">
            <circle cx="40" cy="40" r="36" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)" />
            <text x="40" y="48" textAnchor="middle" fill="var(--accent)" fontSize="32" fontWeight="900" fontFamily="var(--font-display-en)">$</text>
          </svg>
          <h1 className="bg-title">結婚要幾錢？</h1>
          <p className="bg-sub">香港結婚平均開支大拆解</p>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="bg-scene">
        <div className="bg-number-block">
          <div className="bg-highlight-bar">
            <div className="bg-rule" />
            <span className="bg-number-appear">36 萬</span>
            <div className="bg-rule" />
          </div>
          <p className="bg-number-label">2024 香港結婚平均開支</p>
          <p className="bg-number-sub">視乎規模，由 20 萬到 50 萬不等</p>
        </div>
      </div>
    );
  }

  if (step >= 2 && step < 7) {
    const c = COSTS[step - 2];
    return (
      <div className="bg-scene">
        <div className="bg-cost-card" style={{ animationDelay: "100ms" }}>
          <div className="bg-cost-bar-bg">
            <div className="bg-cost-bar-fill" style={{ width: c.pct }} />
          </div>
          <div className="bg-cost-info">
            <span className="bg-cost-label">{c.label}</span>
            <span className="bg-cost-amount">{c.amount}</span>
            <span className="bg-cost-pct">{c.pct}</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-scene">
      <div className="bg-final">
        <svg viewBox="0 0 80 80" className="bg-final-icon" width="80" height="80">
          <circle cx="40" cy="40" r="36" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)" />
          <path d="M22 40l12 12 24-24" stroke="var(--accent)" strokeWidth="4" fill="none" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        <h2>記得預留應急錢</h2>
        <p>約總預算嘅 10%，以備不時之需</p>
      </div>
    </div>
  );
}