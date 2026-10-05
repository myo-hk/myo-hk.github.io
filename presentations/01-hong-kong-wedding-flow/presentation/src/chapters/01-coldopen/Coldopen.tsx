import "./Coldopen.css";

interface Props {
  step: number;
}

const STEPS = [
  { num: "01", label: "確認資格" },
  { num: "02", label: "準備文件" },
  { num: "03", label: "交通知書" },
  { num: "04", label: "揀場地" },
  { num: "05", label: "婚禮+婚後" },
];

export default function Coldopen({ step }: Props) {
  if (step === 0) {
    return (
      <div className="cd-scene">
        <div className="cd-hook">
          <div className="cd-question-mark">?</div>
          <h1>香港結婚註冊<br />其實只係五步</h1>
          <p className="cd-sub">由準備到註冊，拆開嚟睇一啲都唔複雜</p>
        </div>
      </div>
    );
  }

  if (step === 1) {
    return (
      <div className="cd-scene">
        <div className="cd-promise">
          <p className="cd-promise-text">
            大部分人都覺得結婚註冊好複雜<br />
            又怕漏文件，又怕排錯期
          </p>
          <div className="cd-highlight-bar">
            <div className="cd-rule" />
            <span className="cd-number-appear">5</span>
            <div className="cd-rule-right" />
          </div>
          <p className="cd-promise-sub">
            但拆開嚟睇，其實只需要五個環節
          </p>
        </div>
      </div>
    );
  }

  if (step === 2) {
    return (
      <div className="cd-scene">
        <div className="cd-preview">
          <p className="cd-preview-label">五步搞掂香港結婚註冊</p>
          <div className="cd-steps-row">
            {STEPS.map((s, i) => (
              <div
                key={s.num}
                className="cd-step-card"
                style={{ animationDelay: `${i * 80}ms` }}
              >
                <span className="cd-step-num">{s.num}</span>
                <span className="cd-step-label">{s.label}</span>
              </div>
            ))}
          </div>
          <div className="cd-price-row">
            <div className="cd-rule" />
            <span className="cd-price">$1,020</span>
            <span className="cd-price-label">最平方案</span>
            <div className="cd-rule" />
          </div>
        </div>
      </div>
    );
  }

  return null;
}