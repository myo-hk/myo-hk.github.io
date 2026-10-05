import "./CTA.css";
interface Props { step: number; }

const COST_ITEMS = [
  { label: "註冊費用", pct: "1%" },
  { label: "婚戒預算", pct: "11%" },
  { label: "攝影費用", pct: "7%" },
  { label: "婚宴開支", pct: "50%" },
  { label: "其他雜項", pct: "13%" },
];

export function CTA({ step }: Props) {
  if (step === 0) {
    return (
      <div className="ct-scene">
        <div className="ct-hook">
          <svg viewBox="0 0 80 80" className="ct-check-icon" width="80" height="80">
            <circle cx="40" cy="40" r="36" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)" />
            <path d="M24 40l12 12 20-20" stroke="var(--accent)" strokeWidth="4" fill="none" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          <h1 className="ct-title">總結與下一步</h1>
          <p className="ct-sub">準備好就開始你嘅結婚籌備旅程</p>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="ct-scene">
        <h2 className="ct-recap-title">五大開支佔比</h2>
        <div className="ct-recap-grid">
          {COST_ITEMS.map((item, i) => (
            <div key={i} className="ct-recap-card" style={{ animationDelay: `${100 + i * 80}ms` }}>
              <span className="ct-recap-label">{item.label}</span>
              <div className="ct-recap-bar-bg">
                <div className="ct-recap-bar-fill" style={{ width: item.pct }} />
              </div>
              <span className="ct-recap-pct">{item.pct}</span>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="ct-scene">
      <div className="ct-final-card">
        <svg viewBox="0 0 64 64" className="ct-heart-icon" width="64" height="64">
          <circle cx="32" cy="32" r="28" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
          <path d="M32 22c-4-4-10-4-14 0s-4 10 0 14l14 14 14-14c4-4 4-10 0-14s-10-4-14 0z" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
        </svg>
        <h2 className="ct-final-title">超過 400 篇香港婚禮教學文章</h2>
        <p className="ct-final-desc">由預算規劃到婚禮籌備，一站式資訊平台</p>
        <a href="https://myo-makeyourown.pages.dev/" className="ct-cta-link" target="_blank" rel="noopener noreferrer">
          myo-makeyourown.pages.dev
          <svg viewBox="0 0 24 24" width="20" height="20">
            <path d="M7 17L17 7M7 7h10v10" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </a>
      </div>
    </div>
  );
}