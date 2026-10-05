import "./Legalization.css";
interface Props { step: number; }

export function Legalization({ step }: Props) {
  if (step === 0) {
    return (
      <div className="c4-scene">
        <div className="c4-hook">
          <svg viewBox="0 0 80 80" className="c4-hook-icon" width="80" height="80"><rect x="16" y="8" width="48" height="64" rx="4" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><line x1="24" y1="24" x2="56" y2="24" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="34" x2="56" y2="34" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="44" x2="48" y2="44" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/></svg>
          <h1 className="c4-title">文件認證</h1>
          <p className="c4-sub">了解海外文件認證同公證程序</p>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="c4-scene">
        <div className="c4-number-block">
          <div className="c4-highlight-bar">
            <span className="c4-rule" />
            <span className="c4-number-appear">4. 結婚證書要翻譯</span>
            <span className="c4-rule" />
          </div>
          <span className="c4-number-label">星評價</span>
          <span className="c4-number-sub">新人推薦</span>
        </div>
      </div>
    );
  }

  return (
    <div className="c4-scene">
      <div className="c4-card">
        <h2 className="c4-card-title">文件認證</h2>
        <div className="c4-list">
          <div className="c4-list-item" style={{ animationDelay: `${0}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>國際公證人見證簽名</span>
          </div>
          <div className="c4-list-item" style={{ animationDelay: `${100}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>海牙認證 Apostille</span>
          </div>
          <div className="c4-list-item" style={{ animationDelay: `${200}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>領事館認證程序</span>
          </div>
          <div className="c4-list-item" style={{ animationDelay: `${300}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>翻譯公證文件</span>
          </div>
          <div className="c4-list-item" style={{ animationDelay: `${400}ms` }}>
            <svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
            <span>確認文件有效期</span>
          </div>
        </div>
      </div>
    </div>
  );
}