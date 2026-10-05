import "./CTA.css";

interface Props { step: number; }

const RECAP = [
  { num: "01", period: "12-9 個月", desc: "訂日期・預算・場地" },
  { num: "02", period: "8-6 個月", desc: "文件・婚戒・供應商" },
  { num: "03", period: "5-3 個月", desc: "請柬・試妝・菜單" },
  { num: "04", period: "2-1 個月", desc: "確認・修改・利是" },
  { num: "05", period: "最後 1 月", desc: "衝刺・休息・準備" },
];

export function CTA({ step }: Props) {
  if (step === 0) {
    return (
      <div className="cta-scene">
        <div className="cta-hook">
          <svg viewBox="0 0 80 80" className="cta-check-icon" width="80" height="80">
            <circle cx="40" cy="40" r="36" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)" />
            <path d="M24 40l12 12 20-20" stroke="var(--accent)" strokeWidth="4" fill="none" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          <h1 className="cta-title">搞掂晒！</h1>
          <p className="cta-sub">你已經掌握咗結婚籌備嘅完整流程</p>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="cta-scene">
        <h2 className="cta-recap-title">五個階段 recap</h2>
        <div className="cta-recap-grid">
          {RECAP.map((r, i) => (
            <div
              key={i}
              className="cta-recap-card"
              style={{ animationDelay: `${100 + i * 80}ms` }}
            >
              <span className="cta-recap-num">{r.num}</span>
              <span className="cta-recap-period">{r.period}</span>
              <span className="cta-recap-desc">{r.desc}</span>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="cta-scene">
      <div className="cta-final-card">
        <svg viewBox="0 0 64 64" className="cta-heart-icon" width="64" height="64">
          <circle cx="32" cy="32" r="28" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
          <path d="M32 22c-4-4-10-4-14 0s-4 10 0 14l14 14 14-14c4-4 4-10 0-14s-10-4-14 0z" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
        </svg>
        <h2 className="cta-final-title">超過 400 篇香港婚禮教學文章</h2>
        <p className="cta-final-desc">由籌備到婚後，一站式婚禮資訊平台</p>
        <a
          href="https://myo-makeyourown.pages.dev/"
          className="cta-link"
          target="_blank"
          rel="noopener noreferrer"
        >
          myo-makeyourown.pages.dev
          <svg viewBox="0 0 24 24" className="cta-external-icon" width="20" height="20">
            <path d="M7 17L17 7M7 7h10v10" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </a>
      </div>
    </div>
  );
}