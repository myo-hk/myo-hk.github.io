import "./Ceremony.css";

interface Props {
  step: number;
}

const FLOW_NODES = [
  { label: "聲明書", sub: "Declaration" },
  { label: "交換誓言", sub: "Vows" },
  { label: "簽證書", sub: "Signing" },
];

export default function Ceremony({ step }: Props) {
  // step 0 — ceremony flow node diagram
  if (step === 0) {
    return (
      <div className="ce-scene">
        <div className="ce-flow">
          {FLOW_NODES.map((node, i) => {
            const lit = i === 0 || i === 1;
            return (
              <div key={node.label} className="ce-flow-row">
                <div className={`ce-node ${lit ? "ce-node--lit" : ""}`}>
                  <span className="ce-node-num">0{i + 1}</span>
                  <span className="ce-node-label">{node.label}</span>
                  <span className="ce-node-sub">{node.sub}</span>
                </div>
                {i < FLOW_NODES.length - 1 && (
                  <div className={`ce-arrow ${lit ? "ce-arrow--lit" : ""}`} />
                )}
              </div>
            );
          })}
        </div>
        <p className="ce-hint">逐項完成，不可跳過</p>
      </div>
    );
  }

  // step 1 — witness requirements card
  if (step === 1) {
    return (
      <div className="ce-scene">
        <div className="ce-card ce-card--witness">
          <div className="ce-card-icon">
            <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="24" cy="16" r="8" stroke="currentColor" strokeWidth="2.5" />
              <path d="M8 40c0-8.837 7.163-16 16-16s16 7.163 16 16" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" />
              <circle cx="38" cy="16" r="6" stroke="currentColor" strokeWidth="2" strokeDasharray="3 2" />
              <path d="M42 36c0-6.627-4.477-12-10-12" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeDasharray="3 2" />
            </svg>
          </div>
          <div className="ce-witness-numbers">
            <span className="ce-big-num">2</span>
            <span className="ce-big-num-label">名見證人</span>
          </div>
          <div className="ce-witness-rule" />
          <div className="ce-witness-age">
            <span className="ce-age-badge">18+</span>
            <span className="ce-age-text">年滿十八歲</span>
          </div>
          <p className="ce-witness-note">見證人負責確認雙方自願結婚</p>
        </div>
      </div>
    );
  }

  // step 2 — certificate reveal with dimensions
  if (step === 2) {
    return (
      <div className="ce-scene">
        <div className="ce-cert-wrap">
          <div className="ce-cert">
            <div className="ce-cert-inner">
              <div className="ce-cert-header">結婚證書</div>
              <div className="ce-cert-body">
                <div className="ce-cert-line" />
                <div className="ce-cert-line ce-cert-line--short" />
                <div className="ce-cert-line" />
                <div className="ce-cert-line ce-cert-line--short" />
                <div className="ce-cert-line" />
              </div>
              <div className="ce-cert-seal"><span>香港特別行政區 (HKSAR)</span></div>
            </div>
          </div>
          <div className="ce-dim-badge">
            <span className="ce-dim-w">209</span>
            <span className="ce-dim-x">mm</span>
            <span className="ce-dim-sep">×</span>
            <span className="ce-dim-h">298</span>
            <span className="ce-dim-x">mm</span>
          </div>
        </div>
        <p className="ce-cert-note">一式兩份，正本即場領取</p>
      </div>
    );
  }

  // step 3 — certificate sliding into cover
  if (step === 3) {
    return (
      <div className="ce-scene">
        <div className="ce-cover-wrap">
          <div className="ce-cover">
            <div className="ce-cover-spine" />
            <div className="ce-cover-pocket">
              <div className="ce-cert-slide">
                <div className="ce-cert-slide-inner">
                  <div className="ce-cert-slide-header">結婚證書</div>
                  <div className="ce-cert-slide-lines">
                    <div className="ce-cert-slide-line" />
                    <div className="ce-cert-slide-line ce-cert-slide-line--short" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <p className="ce-cover-hint">好好保護你的證書</p>
      </div>
    );
  }

  return null;
}