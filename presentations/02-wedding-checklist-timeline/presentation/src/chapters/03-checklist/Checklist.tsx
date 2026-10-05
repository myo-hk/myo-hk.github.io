import "./Checklist.css";

interface Props { step: number; }

const CATEGORIES = [
  {
    title: "文件法律",
    icon: (
      <svg viewBox="0 0 64 64" fill="none" className="cl-svg">
        <rect x="12" y="8" width="40" height="48" rx="4" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
        <path d="M24 24h16M24 34h16M24 44h8" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" />
      </svg>
    ),
    items: ["擬結婚通知書", "身份證", "見證人 2 位"],
  },
  {
    title: "婚禮必需品",
    icon: (
      <svg viewBox="0 0 64 64" fill="none" className="cl-svg">
        <circle cx="32" cy="32" r="22" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
        <path d="M26 32l4 4 8-8" stroke="var(--accent)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
        <path d="M32 10v8M32 46v8" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" opacity="0.5" />
      </svg>
    ),
    items: ["婚紗禮服", "結婚戒指", "婚鞋", "證書套"],
  },
  {
    title: "場地飲食",
    icon: (
      <svg viewBox="0 0 64 64" fill="none" className="cl-svg">
        <path d="M12 20h40L48 48H16L12 20z" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
        <circle cx="32" cy="34" r="6" stroke="var(--accent)" strokeWidth="2" />
        <path d="M32 16v8" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" />
      </svg>
    ),
    items: ["婚宴場地", "菜單試菜", "酒水", "結婚蛋糕"],
  },
  {
    title: "婚禮當日",
    icon: (
      <svg viewBox="0 0 64 64" fill="none" className="cl-svg">
        <rect x="14" y="18" width="36" height="28" rx="4" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" />
        <path d="M24 28l4 4 8-8M24 40l4 4 8-8" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    ),
    items: ["利是封", "回禮禮物", "後備衣物", "急救包"],
  },
];

export function Checklist({ step }: Props) {
  if (step < CATEGORIES.length) {
    const c = CATEGORIES[step];
    return (
      <div className="cl-scene">
        <div className="cl-category" style={{ animationDelay: "100ms" }}>
          <div className="cl-icon-wrap">{c.icon}</div>
          <h2 className="cl-title">{c.title}</h2>
          <div className="cl-items">
            {c.items.map((item, i) => (
              <div key={i} className="cl-item" style={{ animationDelay: `${300 + i * 100}ms` }}>
                <svg viewBox="0 0 24 24" className="cl-check" width="20" height="20">
                  <rect x="3" y="3" width="18" height="18" rx="3" stroke="var(--accent)" strokeWidth="2" fill="none" />
                  <path d="M8 12l3 3 5-5" stroke="var(--accent)" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
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
    <div className="cl-scene">
      <div className="cl-final">
        <svg viewBox="0 0 80 80" className="cl-final-icon" width="80" height="80">
          <circle cx="40" cy="40" r="36" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)" />
          <path d="M22 40l12 12 24-24" stroke="var(--accent)" strokeWidth="4" fill="none" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        <h2>全部搞掂晒！</h2>
        <p>每項逐個打勾，婚禮準備無遺漏</p>
      </div>
    </div>
  );
}