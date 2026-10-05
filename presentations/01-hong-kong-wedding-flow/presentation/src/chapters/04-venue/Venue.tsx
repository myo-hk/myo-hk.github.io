import "./Venue.css";

interface Props {
  step: number;
}

const LOCATIONS = [
  "大會堂婚姻登記處",
  "紅棉路婚姻登記處",
  "沙田婚姻登記處",
  "屯門婚姻登記處",
  "尖沙咀婚姻登記處",
];

const COMPARISON_ROWS = [
  { label: "費用", registry: "HK$715", church: "按教堂規定", celebrant: "HK$2,000–5,000" },
  { label: "自由度", registry: "固定時間地點", church: "宗教場所限定", celebrant: "任何時間地點" },
  { label: "主持", registry: "登記官", church: "神職人員", celebrant: "執業律師/公證人" },
  { label: "適合", registry: "預算有限", church: "有宗教信仰", celebrant: "追求彈性" },
];

export default function Venue({ step }: Props) {
  if (step === 0) {
    return (
      <div className="ve-scene">
        <div className="ve-kicker">第三個環節</div>
        <h2 className="ve-title">揀場地 · 三種選擇</h2>
        <div className="ve-cards-row">
          <div className="ve-card" style={{ animationDelay: "0ms" }}>
            <div className="ve-card-num">01</div>
            <div className="ve-card-icon ve-icon-registry" />
            <h3 className="ve-card-title">婚姻登記處</h3>
            <p className="ve-card-desc">簡約莊重<br />HK$715 起</p>
          </div>
          <div className="ve-card" style={{ animationDelay: "120ms" }}>
            <div className="ve-card-num">02</div>
            <div className="ve-card-icon ve-icon-church" />
            <h3 className="ve-card-title">特許禮拜場所</h3>
            <p className="ve-card-desc">宗教儀式<br />神職人員主持</p>
          </div>
          <div className="ve-card" style={{ animationDelay: "240ms" }}>
            <div className="ve-card-num">03</div>
            <div className="ve-card-icon ve-icon-celebrant" />
            <h3 className="ve-card-title">婚姻監禮人</h3>
            <p className="ve-card-desc">自由場地時間<br />HK$2,000–5,000</p>
          </div>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="ve-scene">
        <div className="ve-detail-left">
          <div className="ve-detail-badge">01</div>
          <h2 className="ve-detail-title">婚姻登記處</h2>
          <p className="ve-detail-sub">香港五間婚姻登記處</p>
          <div className="ve-locations-list">
            {LOCATIONS.map((loc, i) => (
              <div
                key={loc}
                className="ve-location-item"
                style={{ animationDelay: `${i * 120}ms` }}
              >
                <span className="ve-location-dot" />
                <span className="ve-location-name">{loc}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="ve-detail-right">
          <div className="ve-price-card">
            <span className="ve-price-label">辦公時間</span>
            <span className="ve-price-amount">HK$715</span>
            <div className="ve-rule-short" />
            <span className="ve-price-label">非辦公時間</span>
            <span className="ve-price-amount ve-price-alt">HK$1,935</span>
          </div>
          <p className="ve-price-note">星期六下午 · 星期日</p>
        </div>
      </div>
    );
  }

  if (step === 2) {
    return (
      <div className="ve-scene">
        <div className="ve-detail-badge">02</div>
        <h2 className="ve-detail-title">特許禮拜場所</h2>
        <div className="ve-church-layout">
          <div className="ve-church-visual">
            <div className="ve-church-arch">
              <div className="ve-church-window" />
              <div className="ve-church-cross" />
            </div>
          </div>
          <div className="ve-church-details">
            <div className="ve-church-item" style={{ animationDelay: "0ms" }}>
              <span className="ve-church-check" />
              <span>特許禮拜場所舉行婚禮</span>
            </div>
            <div className="ve-church-item" style={{ animationDelay: "120ms" }}>
              <span className="ve-church-check" />
              <span>由合資格神職人員主持</span>
            </div>
            <div className="ve-church-item" style={{ animationDelay: "240ms" }}>
              <span className="ve-church-check" />
              <span>按教會儀式進行</span>
            </div>
            <div className="ve-church-item" style={{ animationDelay: "360ms" }}>
              <span className="ve-church-check" />
              <span>天主教 · 基督教 · 清真寺</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (step === 3) {
    return (
      <div className="ve-scene">
        <div className="ve-detail-badge">03</div>
        <h2 className="ve-detail-title">婚姻監禮人</h2>
        <p className="ve-detail-sub">自由度最高 · 任何時間任何地點</p>
        <div className="ve-celebrant-grid">
          <div className="ve-celebrant-card" style={{ animationDelay: "0ms" }}>
            <div className="ve-celebrant-icon ve-celebrant-icon-hotel" />
            <span className="ve-celebrant-label">酒店</span>
          </div>
          <div className="ve-celebrant-card" style={{ animationDelay: "100ms" }}>
            <div className="ve-celebrant-icon ve-celebrant-icon-garden" />
            <span className="ve-celebrant-label">花園</span>
          </div>
          <div className="ve-celebrant-card" style={{ animationDelay: "200ms" }}>
            <div className="ve-celebrant-icon ve-celebrant-icon-beach" />
            <span className="ve-celebrant-label">海灘</span>
          </div>
          <div className="ve-celebrant-card" style={{ animationDelay: "300ms" }}>
            <div className="ve-celebrant-icon ve-celebrant-icon-restaurant" />
            <span className="ve-celebrant-label">空中餐廳</span>
          </div>
        </div>
        <div className="ve-celebrant-price">
          <div className="ve-rule-short" />
          <span className="ve-celebrant-price-range">HK$2,000 – HK$5,000</span>
          <span className="ve-celebrant-price-note">自行與監禮人議價</span>
          <div className="ve-rule-short" />
        </div>
      </div>
    );
  }

  if (step === 4) {
    return (
      <div className="ve-scene">
        <h2 className="ve-title ve-title-compare">三種選擇 · 一覽比較</h2>
        <div className="ve-table-wrap">
          <table className="ve-table">
            <thead>
              <tr>
                <th />
                <th className="ve-th-accent">婚姻登記處</th>
                <th>特許禮拜場所</th>
                <th className="ve-th-accent">婚姻監禮人</th>
              </tr>
            </thead>
            <tbody>
              {COMPARISON_ROWS.map((row, i) => (
                <tr key={row.label} style={{ animationDelay: `${i * 150}ms` }}>
                  <td className="ve-td-label">{row.label}</td>
                  <td className="ve-td-accent">{row.registry}</td>
                  <td>{row.church}</td>
                  <td className="ve-td-accent">{row.celebrant}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="ve-compare-footer">
          <span className="ve-compare-tag">最平 HK$715 登記處結婚</span>
          <span className="ve-compare-tag">最自由：監禮人</span>
          <span className="ve-compare-tag">最莊重：登記處</span>
        </div>
      </div>
    );
  }

  return null;
}