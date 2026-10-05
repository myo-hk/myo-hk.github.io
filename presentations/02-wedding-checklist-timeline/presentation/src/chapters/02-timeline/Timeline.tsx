import "./Timeline.css";

interface Props { step: number; }

const PHASES = [
  {
    range: "12-9 個月",
    label: "決定期",
    icon: (
      <svg viewBox="0 0 64 64" fill="none" className="tl-svg">
        <rect x="8" y="12" width="48" height="40" rx="4" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
        <circle cx="32" cy="32" r="8" stroke="var(--accent)" strokeWidth="2" fill="var(--accent)" opacity="0.3" />
        <path d="M28 32l3 3 5-5" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
    items: ["確定婚期", "訂預算", "賓客名單", "預訂場地"],
  },
  {
    range: "8-6 個月",
    label: "執行期",
    icon: (
      <svg viewBox="0 0 64 64" fill="none" className="tl-svg">
        <rect x="10" y="14" width="44" height="36" rx="4" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
        <path d="M22 32l7 7 13-13" stroke="var(--accent)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
        <circle cx="20" cy="20" r="3" fill="var(--accent)" opacity="0.4" />
      </svg>
    ),
    items: ["交通知書", "買婚戒", "揀婚紗", "預訂攝影"],
  },
  {
    range: "5-3 個月",
    label: "落實期",
    icon: (
      <svg viewBox="0 0 64 64" fill="none" className="tl-svg">
        <rect x="12" y="16" width="40" height="32" rx="4" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
        <path d="M24 30l6 6 10-10" stroke="var(--accent)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M18 44l4-6" stroke="var(--accent)" strokeWidth="1.5" strokeLinecap="round" />
      </svg>
    ),
    items: ["發請柬", "試妝", "確認菜單", "買證書套"],
  },
  {
    range: "2-1 個月",
    label: "確認期",
    icon: (
      <svg viewBox="0 0 64 64" fill="none" className="tl-svg">
        <circle cx="32" cy="32" r="20" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
        <path d="M22 32l7 7 13-13" stroke="var(--accent)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
        <circle cx="44" cy="20" r="4" fill="var(--accent)" opacity="0.5" />
      </svg>
    ),
    items: ["確認人數", "婚紗修改", "買配件", "準備利是"],
  },
  {
    range: "最後 1 個月",
    label: "衝刺期",
    icon: (
      <svg viewBox="0 0 64 64" fill="none" className="tl-svg">
        <path d="M32 12v10M32 42v10" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" />
        <circle cx="32" cy="32" r="14" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
        <path d="M28 32l4 4 6-8" stroke="var(--accent)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
    items: ["確認細節", "打包蜜月", "美容", "休息"],
  },
];

export function Timeline({ step }: Props) {
  if (step < PHASES.length) {
    const p = PHASES[step];
    return (
      <div className="tl-scene">
        <div className="tl-phase" style={{ animationDelay: "100ms" }}>
          <div className="tl-icon-wrap">{p.icon}</div>
          <div className="tl-badge">
            <span className="tl-range">{p.range}</span>
            <span className="tl-label">{p.label}</span>
          </div>
          <div className="tl-items">
            {p.items.map((item, i) => (
              <div key={i} className="tl-item" style={{ animationDelay: `${300 + i * 100}ms` }}>
                <svg viewBox="0 0 20 20" className="tl-check" width="16" height="16">
                  <path d="M4 10l4 4 8-8" stroke="var(--accent)" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                <span>{item}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="tl-scene">
      <div className="tl-final">
        <svg viewBox="0 0 80 80" className="tl-final-icon" width="80" height="80">
          <circle cx="40" cy="40" r="36" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)" />
          <path d="M24 40l12 12 20-20" stroke="var(--accent)" strokeWidth="4" fill="none" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        <h2>12 個月時間表</h2>
        <p>跟住呢個時間表，籌備婚禮就唔會手忙腳亂</p>
      </div>
    </div>
  );
}