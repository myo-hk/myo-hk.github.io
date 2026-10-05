import "./Vendors.css";

interface Props { step: number; }

const VENDORS = [
  {
    name: "攝影師",
    tip: "睇作品風格，傾清楚合約細節同交相時間",
    icon: (
      <svg viewBox="0 0 64 64" fill="none" className="vn-svg">
        <rect x="12" y="18" width="40" height="30" rx="4" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
        <circle cx="32" cy="33" r="8" stroke="var(--accent)" strokeWidth="2" />
        <circle cx="32" cy="33" r="3" fill="var(--accent)" />
        <rect x="10" y="16" width="8" height="6" rx="2" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
      </svg>
    ),
  },
  {
    name: "化妝師",
    tip: "一定要預約試妝，確認髮型同妝容風格",
    icon: (
      <svg viewBox="0 0 64 64" fill="none" className="vn-svg">
        <ellipse cx="32" cy="28" rx="14" ry="16" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
        <circle cx="26" cy="24" r="2" fill="var(--accent)" />
        <circle cx="38" cy="24" r="2" fill="var(--accent)" />
        <path d="M28 34q4 3 8 0" stroke="var(--accent)" strokeWidth="2" fill="none" strokeLinecap="round" />
        <path d="M12 48l12-6M52 48l-12-6" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" />
      </svg>
    ),
  },
  {
    name: "司儀",
    tip: "揀有經驗嘅司儀，確認流程同默契",
    icon: (
      <svg viewBox="0 0 64 64" fill="none" className="vn-svg">
        <rect x="16" y="12" width="32" height="24" rx="4" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
        <path d="M32 36v8M24 44h16" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" />
        <path d="M20 20l8 4-8 4" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M44 20l-8 4 8 4" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
  },
  {
    name: "場地佈置",
    tip: "睇實物相確認主題風格，傾清楚細節",
    icon: (
      <svg viewBox="0 0 64 64" fill="none" className="vn-svg">
        <rect x="14" y="24" width="36" height="28" rx="4" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
        <path d="M32 12l4 8h-8l4-8z" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
        <circle cx="32" cy="38" r="4" stroke="var(--accent)" strokeWidth="2" />
        <path d="M22 46l4-4M42 46l-4-4" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" />
      </svg>
    ),
  },
];

export function Vendors({ step }: Props) {
  if (step === 0) {
    return (
      <div className="vn-scene">
        <div className="vn-hook">
          <svg viewBox="0 0 80 80" className="vn-hook-icon" width="80" height="80">
            <circle cx="40" cy="40" r="36" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)" />
            <path d="M30 30l8 8M50 30l-8 8M30 50l8-8M50 50l-8-8" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" />
          </svg>
          <h1 className="vn-title">供應商點揀好？</h1>
          <p className="vn-sub">四個最緊要嘅婚禮供應商揀選貼士</p>
        </div>
      </div>
    );
  }

  if (step >= 1 && step <= 4) {
    const v = VENDORS[step - 1];
    return (
      <div className="vn-scene">
        <div className="vn-card" style={{ animationDelay: "100ms" }}>
          <div className="vn-icon-wrap">{v.icon}</div>
          <h2 className="vn-name">{v.name}</h2>
          <p className="vn-tip">{v.tip}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="vn-scene">
      <div className="vn-final">
        <svg viewBox="0 0 80 80" className="vn-final-icon" width="80" height="80">
          <circle cx="40" cy="40" r="36" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)" />
          <path d="M22 40l12 12 24-24" stroke="var(--accent)" strokeWidth="4" fill="none" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        <h2>揀供應商三大貼士</h2>
        <div className="vn-tips-list">
          <div className="vn-tip-item">✓ 睇作品風格</div>
          <div className="vn-tip-item">✓ 睇網上評價</div>
          <div className="vn-tip-item">✓ 傾清楚合約條款</div>
        </div>
      </div>
    </div>
  );
}