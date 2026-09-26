import "./Eligibility.css";

interface Props {
  step: number;
}

const CONDITIONS = [
  { label: "年滿 16 歲", desc: "最低法定結婚年齡" },
  { label: "一夫一妻", desc: "婚姻條例第 181 章" },
  { label: "非近親", desc: "法律定義的禁婚親屬關係" },
  { label: "不限國籍", desc: "任何國籍及居住地均可" },
];

const DOCUMENTS = [
  {
    label: "香港身份證",
    desc: "香港居民只需帶身份證",
    icon: "id-card",
  },
  {
    label: "旅行證件",
    desc: "海外人士需有效護照或簽證身份書",
    icon: "passport",
  },
];

const SPECIAL_CASES = [
  {
    label: "未滿 21 歲",
    detail: "需父母或監護人書面同意",
    form: "表格 MR4",
    icon: "underage",
  },
  {
    label: "離婚人士",
    detail: "需提交法庭發出嘅離婚判令",
    form: "絕對判令 / 暫准判令",
    icon: "divorce",
  },
  {
    label: "鰥夫或寡婦",
    detail: "需提交前配偶嘅死亡證明書",
    form: "死亡證明書正本",
    icon: "widowed",
  },
];

/* ─── SVG icon components ─── */

function CheckCircle({ animated }: { animated: boolean }) {
  return (
    <svg
      className={`el-check-circle${animated ? " el-check-animated" : ""}`}
      viewBox="0 0 32 32"
      width="32"
      height="32"
    >
      <circle
        cx="16"
        cy="16"
        r="14"
        fill="none"
        stroke="var(--accent)"
        strokeWidth="2.5"
        opacity="0.3"
      />
      <path
        className="el-check-path"
        d="M9 16l5 5 9-9"
        fill="none"
        stroke="var(--accent)"
        strokeWidth="3"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeDasharray="30"
        strokeDashoffset={animated ? "0" : "30"}
      />
    </svg>
  );
}

function IdCardSvg() {
  return (
    <svg viewBox="0 0 48 34" width="48" height="34" className="el-doc-svg">
      <rect
        x="2"
        y="2"
        width="44"
        height="30"
        rx="4"
        fill="none"
        stroke="var(--accent)"
        strokeWidth="1.5"
      />
      <rect
        x="8"
        y="6"
        width="14"
        height="16"
        rx="2"
        fill="var(--accent-soft)"
        stroke="var(--accent)"
        strokeWidth="1"
      />
      <line
        x1="26"
        y1="9"
        x2="42"
        y2="9"
        stroke="var(--text-2)"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <line
        x1="26"
        y1="14"
        x2="42"
        y2="14"
        stroke="var(--text-mute)"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <line
        x1="26"
        y1="19"
        x2="36"
        y2="19"
        stroke="var(--text-faint)"
        strokeWidth="2"
        strokeLinecap="round"
      />
    </svg>
  );
}

function PassportSvg() {
  return (
    <svg viewBox="0 0 38 48" width="38" height="48" className="el-doc-svg">
      <rect
        x="2"
        y="2"
        width="34"
        height="44"
        rx="4"
        fill="none"
        stroke="var(--accent)"
        strokeWidth="1.5"
      />
      <circle
        cx="19"
        cy="16"
        r="7"
        fill="var(--accent-soft)"
        stroke="var(--accent)"
        strokeWidth="1"
      />
      <line
        x1="8"
        y1="28"
        x2="30"
        y2="28"
        stroke="var(--text-2)"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <line
        x1="8"
        y1="33"
        x2="26"
        y2="33"
        stroke="var(--text-mute)"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <line
        x1="8"
        y1="38"
        x2="22"
        y2="38"
        stroke="var(--text-faint)"
        strokeWidth="2"
        strokeLinecap="round"
      />
    </svg>
  );
}

function UnderageSvg() {
  return (
    <svg viewBox="0 0 40 40" width="40" height="40" className="el-special-svg">
      <circle
        cx="20"
        cy="20"
        r="18"
        fill="var(--accent-soft)"
        stroke="var(--accent)"
        strokeWidth="1.5"
      />
      <text
        x="20"
        y="25"
        textAnchor="middle"
        fontSize="18"
        fontWeight="700"
        fill="var(--accent)"
        fontFamily="var(--font-display-en)"
      >
        21
      </text>
    </svg>
  );
}

function DivorceSvg() {
  return (
    <svg viewBox="0 0 36 44" width="36" height="44" className="el-special-svg">
      <rect
        x="2"
        y="2"
        width="32"
        height="40"
        rx="3"
        fill="none"
        stroke="var(--accent)"
        strokeWidth="1.5"
      />
      <line
        x1="6"
        y1="10"
        x2="30"
        y2="10"
        stroke="var(--text-2)"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <line
        x1="6"
        y1="15"
        x2="30"
        y2="15"
        stroke="var(--text-mute)"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <line
        x1="6"
        y1="20"
        x2="24"
        y2="20"
        stroke="var(--text-faint)"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <text
        x="18"
        y="34"
        textAnchor="middle"
        fontSize="12"
        fontWeight="700"
        fill="var(--accent)"
        fontFamily="var(--font-display-cn)"
      >
        判
      </text>
    </svg>
  );
}

function WidowedSvg() {
  return (
    <svg viewBox="0 0 36 44" width="36" height="44" className="el-special-svg">
      <rect
        x="2"
        y="2"
        width="32"
        height="40"
        rx="3"
        fill="none"
        stroke="var(--accent)"
        strokeWidth="1.5"
      />
      <line
        x1="6"
        y1="10"
        x2="30"
        y2="10"
        stroke="var(--text-2)"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <line
        x1="6"
        y1="15"
        x2="30"
        y2="15"
        stroke="var(--text-mute)"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <line
        x1="6"
        y1="20"
        x2="24"
        y2="20"
        stroke="var(--text-faint)"
        strokeWidth="2"
        strokeLinecap="round"
      />
      <text
        x="18"
        y="34"
        textAnchor="middle"
        fontSize="12"
        fontWeight="700"
        fill="var(--accent)"
        fontFamily="var(--font-display-cn)"
      >
        亡
      </text>
    </svg>
  );
}

/* ─── Main component ─── */

export default function Eligibility({ step }: Props) {
  /* ─── Step 0: 4 conditions with staggered checkmark reveal ─── */
  if (step === 0) {
    return (
      <div className="el-scene">
        <div className="el-scene-inner">
          <p className="el-legal-ref">香港法例第 181 章《婚姻條例》</p>
          <h2 className="el-step-title">結婚資格條件</h2>
          <div className="el-conditions-list">
            {CONDITIONS.map((c, i) => (
              <div
                key={c.label}
                className="el-condition-card"
                style={{ animationDelay: `${i * 500}ms` }}
              >
                <CheckCircle animated />
                <div className="el-condition-text">
                  <span className="el-condition-label">{c.label}</span>
                  <span className="el-condition-desc">{c.desc}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  /* ─── Step 1: Documents needed ─── */
  if (step === 1) {
    return (
      <div className="el-scene">
        <div className="el-scene-inner">
          <h2 className="el-step-title">所需文件</h2>
          <p className="el-step-subtitle">大部分人只需要身份證</p>
          <div className="el-docs-row">
            {DOCUMENTS.map((d, i) => (
              <div
                key={d.label}
                className="el-doc-card"
                style={{ animationDelay: `${i * 700}ms` }}
              >
                <div className="el-doc-icon-wrap">
                  {d.icon === "id-card" ? <IdCardSvg /> : <PassportSvg />}
                </div>
                <span className="el-doc-label">{d.label}</span>
                <span className="el-doc-desc">{d.desc}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  /* ─── Step 2: Special cases ─── */
  if (step === 2) {
    return (
      <div className="el-scene">
        <div className="el-scene-inner">
          <h2 className="el-step-title">特殊情況</h2>
          <p className="el-step-subtitle">以下情況需要額外文件</p>
          <div className="el-specials-row">
            {SPECIAL_CASES.map((s, i) => {
              const dirs = ["el-from-left", "el-from-right", "el-from-bottom"];
              return (
                <div
                  key={s.label}
                  className={`el-special-card ${dirs[i]}`}
                  style={{ animationDelay: `${i * 500}ms` }}
                >
                  <div className="el-special-icon-wrap">
                    {s.icon === "underage" ? (
                      <UnderageSvg />
                    ) : s.icon === "divorce" ? (
                      <DivorceSvg />
                    ) : (
                      <WidowedSvg />
                    )}
                  </div>
                  <span className="el-special-label">{s.label}</span>
                  <span className="el-special-detail">{s.detail}</span>
                  <span className="el-special-form">{s.form}</span>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    );
  }

  /* ─── Step 3: Transition — eligibility confirmed ─── */
  if (step === 3) {
    return (
      <div className="el-scene">
        <div className="el-scene-inner el-transition-center">
          <div className="el-big-check-wrap">
            <svg
              className="el-big-check-svg"
              viewBox="0 0 120 120"
              width="120"
              height="120"
            >
              <circle
                cx="60"
                cy="60"
                r="54"
                fill="none"
                stroke="var(--accent)"
                strokeWidth="4"
                opacity="0.15"
              />
              <path
                className="el-big-check-path"
                d="M30 60l20 20 40-40"
                fill="none"
                stroke="var(--accent)"
                strokeWidth="8"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeDasharray="200"
                strokeDashoffset="200"
              />
            </svg>
          </div>
          <h2 className="el-transition-title">資格確認 ✓</h2>
          <p className="el-transition-sub">文件準備好，下一步：遞交擬結婚通知書</p>
        </div>
      </div>
    );
  }

  return null;
}