import "./Coldopen.css";

interface Props {
  step: number;
}

const STEPS_DATA = [
  { num: "01", label: "訂日期・預算" },
  { num: "02", label: "法律・文件" },
  { num: "03", label: "試妝・請柬" },
  { num: "04", label: "最終確認" },
  { num: "05", label: "婚禮衝刺" },
];

export default function Coldopen({ step }: Props) {
  if (step === 0) {
    return (
      <div className="co-scene">
        <div className="co-hook">
          <div className="co-question-mark">?</div>
          <h1>結婚籌備<br />其實只需 12 個月</h1>
          <p className="co-sub">由決定到行禮，每個月都有嘢要準備</p>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="co-scene">
        <div className="co-promise">
          <p className="co-promise-text">
            超過 70% 新人喺婚禮前 6-12 個月先開始籌備<br />
            結果成日因為時間唔夠而手忙腳亂
          </p>
          <div className="co-highlight-bar">
            <div className="co-rule" />
            <span className="co-number-appear">12</span>
            <div className="co-rule-right" />
          </div>
          <p className="co-promise-sub">
            其實只要跟住 12 個月時間表<br />
            一步一步嚟，就唔會漏任何細節
          </p>
        </div>
      </div>
    );
  }

  if (step === 2) {
    return (
      <div className="co-scene">
        <div className="co-preview">
          <p className="co-preview-label">五個階段搞定婚禮籌備</p>
          <div className="co-steps-row">
            {STEPS_DATA.map((s, i) => (
              <div
                key={s.num}
                className="co-step-card"
                style={{ animationDelay: `${i * 80}ms` }}
              >
                <span className="co-step-num">{s.num}</span>
                <span className="co-step-label">{s.label}</span>
              </div>
            ))}
          </div>
          <div className="co-price-row">
            <div className="co-rule" />
            <span className="co-price">$1,020</span>
            <span className="co-price-label">起</span>
            <div className="co-rule" />
          </div>
        </div>
      </div>
    );
  }

  return null;
}