import "./Notice.css";

interface Props {
  step: number;
}

export default function Notice({ step }: Props) {
  if (step === 0) {
    return (
      <div className="no-scene">
        <div className="no-title-group">
          <span className="no-chapter-badge">第二環節</span>
          <h1 className="no-title">擬結婚通知書</h1>
          <p className="no-subtitle">
            啟動整個註冊程序嘅關鍵一步
          </p>
          <div className="no-rule-accent" />
          <p className="no-hint">
            婚禮前最少 <strong>15 日</strong>、最多 <strong><span>3 個月通知期</span></strong>遞交
          </p>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="no-scene">
        <div className="no-timeline-group">
          <h2 className="no-timeline-heading">通知期係點样计嘅？</h2>
          <div className="no-timeline">
            {/* Jan 1 — submit day */}
            <div className="no-tl-node no-tl-submit">
              <span className="no-tl-date">1 月 1 日</span>
              <span className="no-tl-label">遞交</span>
              <div className="no-tl-dot" />
            </div>

            {/* gap zone — 15 days */}
            <div className="no-tl-track">
              <div className="no-tl-bar" />
              <div className="no-tl-days">
                {Array.from({ length: 15 }, (_, i) => (
                  <span key={i} className="no-tl-day" style={{ animationDelay: `${i * 60}ms` }}>
                    {i + 1}
                  </span>
                ))}
              </div>
              <span className="no-tl-track-label">15 天 · 遞交當日唔計</span>
            </div>

            {/* Jan 17 — ceremony day */}
            <div className="no-tl-node no-tl-ceremony">
              <span className="no-tl-date">1 月 17 日</span>
              <span className="no-tl-label">可行禮</span>
              <div className="no-tl-dot no-tl-dot-accent" />
            </div>
          </div>

          <div className="no-tl-rule">
            <span className="no-tl-rule-text">最長 3 個月內要完成婚禮</span>
          </div>
        </div>
      </div>
    );
  }

  if (step === 2) {
    return (
      <div className="no-scene">
        <div className="no-methods-group">
          <h2 className="no-methods-heading">兩種遞交方式</h2>
          <div className="no-methods-row">
            <div className="no-method-card">
              <div className="no-method-icon">
                <svg viewBox="0 0 64 64" fill="none" className="no-method-svg">
                  <circle cx="32" cy="20" r="10" stroke="currentColor" strokeWidth="2.5" fill="none" />
                  <path d="M16 52c0-8.8 7.2-16 16-16s16 7.2 16 16" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" fill="none" />
                  <path d="M32 38v8m-4-4h8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                </svg>
              </div>
              <h3 className="no-method-title">親身遞交</h3>
              <ul className="no-method-list">
                <li>婚姻登記處排隊</li>
                <li>可網上預約</li>
                <li>亦可直接 walk-in</li>
              </ul>
            </div>

            <div className="no-method-card no-method-card-alt">
              <div className="no-method-icon">
                <svg viewBox="0 0 64 64" fill="none" className="no-method-svg">
                  <rect x="12" y="10" width="40" height="44" rx="4" stroke="currentColor" strokeWidth="2.5" fill="none" />
                  <path d="M22 10V6h20v4" stroke="currentColor" strokeWidth="2.5" fill="none" />
                  <path d="M22 28h20M22 36h14M22 44h8" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                  <circle cx="46" cy="46" r="10" fill="var(--accent)" opacity="0.15" />
                  <path d="M43 46l2 2 4-4" stroke="var(--accent)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </div>
              <h3 className="no-method-title">監禮人代辦</h3>
              <ul className="no-method-list">
                <li>婚姻監禮人代辦手續</li>
                <li>律師或公證人</li>
                <li>可同時預約場地</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (step === 3) {
    return (
      <div className="no-scene">
        <div className="no-fee-group">
          <span className="no-fee-label">費用</span>
          <div className="no-fee-number">
            <span className="no-fee-currency">HK$</span>
            <span className="no-fee-amount">305</span>
          </div>
          <div className="no-fee-payments">
            <span className="no-pay-label">支付方式</span>
            <div className="no-pay-icons">
              <div className="no-pay-item">
                <svg viewBox="0 0 48 48" className="no-pay-svg"><rect x="8" y="14" width="32" height="20" rx="3" stroke="currentColor" strokeWidth="2" fill="none" /><circle cx="24" cy="24" r="5" stroke="currentColor" strokeWidth="2" fill="none" /></svg>
                <span>現金</span>
              </div>
              <div className="no-pay-item">
                <svg viewBox="0 0 48 48" className="no-pay-svg"><rect x="8" y="12" width="32" height="24" rx="4" stroke="currentColor" strokeWidth="2" fill="none" /><circle cx="24" cy="24" r="4" stroke="currentColor" strokeWidth="2" fill="none" /><path d="M16 20h16M16 28h16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" /></svg>
                <span>八達通</span>
              </div>
              <div className="no-pay-item">
                <svg viewBox="0 0 48 48" className="no-pay-svg"><path d="M24 8L8 24l16 16 16-16L24 8z" stroke="currentColor" strokeWidth="2" fill="none" /><path d="M24 16l-6 6 6 6 6-6-6-6z" stroke="currentColor" strokeWidth="1.5" fill="none" /></svg>
                <span>轉數快</span>
              </div>
              <div className="no-pay-item">
                <svg viewBox="0 0 48 48" className="no-pay-svg"><rect x="10" y="14" width="28" height="20" rx="4" stroke="currentColor" strokeWidth="2" fill="none" /><path d="M18 24h12M22 20l-4 4 4 4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" /></svg>
                <span>支付寶</span>
              </div>
              <div className="no-pay-item">
                <svg viewBox="0 0 48 48" className="no-pay-svg"><rect x="10" y="14" width="28" height="20" rx="4" stroke="currentColor" strokeWidth="2" fill="none" /><path d="M18 24h12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" /><circle cx="24" cy="24" r="3" stroke="currentColor" strokeWidth="1.5" fill="none" /></svg>
                <span>微信支付</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (step === 4) {
    return (
      <div className="no-scene">
        <div className="no-display-group">
          <h2 className="no-display-heading">公開展示 15 天</h2>
          <div className="no-wall">
            <div className="no-notice-board">
              {/* pin */}
              <div className="no-pin" />
              <div className="no-pin-shadow" />

              {/* notice paper */}
              <div className="no-notice-paper">
                <div className="no-notice-header">
                  <span className="no-notice-badge">婚姻登記處</span>
                  <span className="no-notice-id">個案編號 #2026-0042</span>
                </div>
                <div className="no-notice-body">
                  <div className="no-notice-row">
                    <span className="no-notice-field">擬結婚通知書</span>
                  </div>
                  <div className="no-notice-row">
                    <span className="no-notice-val">陳大明</span>
                    <span className="no-notice-amp">&</span>
                    <span className="no-notice-val">李小美</span>
                  </div>
                  <div className="no-notice-row no-notice-date">
                    <span>遞交日期：2026 年 1 月 1 日</span>
                  </div>
                  <div className="no-notice-row no-notice-date">
                    <span>展示期限：2026 年 1 月 16 日</span>
                  </div>
                </div>
              </div>

              {/* checkmark stamp */}
              <div className="no-stamp">
                <svg viewBox="0 0 80 80" className="no-stamp-svg">
                  <circle cx="40" cy="40" r="36" stroke="var(--accent)" strokeWidth="3" fill="none" opacity="0.3" />
                  <path d="M24 42l10 10 22-24" stroke="var(--accent)" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" fill="none" />
                </svg>
              </div>
            </div>
          </div>
          <p className="no-display-sub">冇人反對？咁就過關喇</p>
        </div>
      </div>
    );
  }

  return null;
}