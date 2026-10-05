/**
 * SVG icon strings for presentation chapters.
 * All use var(--accent) / var(--accent-soft) for theme compatibility.
 * Hook icons: 80×80. Card icons: 32×32.
 * __pfx__ is replaced at runtime with the chapter's CSS prefix.
 */

const ICONS = {

  check80: `<svg viewBox="0 0 80 80" class="__pfx__-hook-icon" width="80" height="80"><circle cx="40" cy="40" r="36" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><path d="M24 40l12 12 20-20" stroke="var(--accent)" strokeWidth="4" fill="none" strokeLinecap="round" strokeLinejoin="round"/></svg>`,

  question80: `<svg viewBox="0 0 80 80" class="__pfx__-hook-icon" width="80" height="80"><circle cx="40" cy="40" r="36" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><text x="40" y="52" textAnchor="middle" fill="var(--accent)" fontSize="36" fontWeight="700" fontFamily="var(--font-display-en)">?</text></svg>`,

  heart80: `<svg viewBox="0 0 80 80" class="__pfx__-hook-icon" width="80" height="80"><circle cx="40" cy="40" r="36" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><path d="M40 28c-4-5-10-5-14-1s-3 10 1 14l13 13 13-13c4-4 4-10 1-14s-10-4-14 1z" stroke="var(--accent)" strokeWidth="3" fill="none" strokeLinecap="round"/></svg>`,

  star80: `<svg viewBox="0 0 80 80" class="__pfx__-hook-icon" width="80" height="80"><circle cx="40" cy="40" r="36" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><path d="M40 16l8 18 20 2-15 14 4 20-17-10-17 10 4-20L12 36l20-2z" stroke="var(--accent)" strokeWidth="3" fill="none" strokeLinejoin="round"/></svg>`,

  calendar80: `<svg viewBox="0 0 80 80" class="__pfx__-hook-icon" width="80" height="80"><rect x="12" y="16" width="56" height="52" rx="6" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><line x1="12" y1="32" x2="68" y2="32" stroke="var(--accent)" strokeWidth="2"/><path d="M24 12v8M56 12v8" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round"/><text x="40" y="56" textAnchor="middle" fill="var(--accent)" fontSize="16" fontWeight="700" fontFamily="var(--font-display-cn)">日期</text></svg>`,

  document80: `<svg viewBox="0 0 80 80" class="__pfx__-hook-icon" width="80" height="80"><rect x="16" y="8" width="48" height="64" rx="4" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><line x1="24" y1="24" x2="56" y2="24" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="34" x2="56" y2="34" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="24" y1="44" x2="48" y2="44" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/></svg>`,

  ring80: `<svg viewBox="0 0 80 80" class="__pfx__-hook-icon" width="80" height="80"><circle cx="40" cy="40" r="20" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><circle cx="40" cy="40" r="12" stroke="var(--accent)" strokeWidth="2" fill="none" strokeDasharray="4 2"/><text x="40" y="44" textAnchor="middle" fill="var(--accent)" fontSize="10" fontWeight="700">&#9670;</text></svg>`,

  camera80: `<svg viewBox="0 0 80 80" class="__pfx__-hook-icon" width="80" height="80"><rect x="10" y="28" width="60" height="42" rx="6" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><circle cx="40" cy="48" r="12" stroke="var(--accent)" strokeWidth="2.5" fill="none"/><circle cx="40" cy="48" r="5" fill="var(--accent)"/><path d="M30 16l10-8 10 8" stroke="var(--accent)" strokeWidth="3" fill="none" strokeLinecap="round" strokeLinejoin="round"/></svg>`,

  venue80: `<svg viewBox="0 0 80 80" class="__pfx__-hook-icon" width="80" height="80"><path d="M12 68V36l28-20 28 20v32" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)" strokeLinejoin="round"/><line x1="30" y1="68" x2="30" y2="46" stroke="var(--accent)" strokeWidth="2.5"/><line x1="50" y1="68" x2="50" y2="46" stroke="var(--accent)" strokeWidth="2.5"/></svg>`,

  gift80: `<svg viewBox="0 0 80 80" class="__pfx__-hook-icon" width="80" height="80"><rect x="14" y="34" width="52" height="36" rx="4" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><path d="M20 34V20a8 8 0 0116 0v14M60 34V20a8 8 0 00-16 0v14" stroke="var(--accent)" strokeWidth="2.5" fill="none"/><line x1="40" y1="34" x2="40" y2="70" stroke="var(--accent)" strokeWidth="2.5"/></svg>`,

  globe80: `<svg viewBox="0 0 80 80" class="__pfx__-hook-icon" width="80" height="80"><circle cx="40" cy="40" r="34" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><ellipse cx="40" cy="40" rx="18" ry="34" stroke="var(--accent)" strokeWidth="1.5" fill="none"/><line x1="8" y1="40" x2="72" y2="40" stroke="var(--accent)" strokeWidth="1.5"/></svg>`,

  scale80: `<svg viewBox="0 0 80 80" class="__pfx__-hook-icon" width="80" height="80"><rect x="14" y="14" width="20" height="52" rx="3" stroke="var(--accent)" strokeWidth="2.5" fill="var(--accent-soft)"/><rect x="46" y="14" width="20" height="52" rx="3" stroke="var(--accent)" strokeWidth="2.5" fill="var(--accent-soft)"/><line x1="24" y1="66" x2="56" y2="66" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round"/></svg>`,

  clock80: `<svg viewBox="0 0 80 80" class="__pfx__-hook-icon" width="80" height="80"><circle cx="40" cy="40" r="34" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><line x1="40" y1="14" x2="40" y2="40" stroke="var(--accent)" strokeWidth="2.5" strokeLinecap="round"/><line x1="40" y1="40" x2="56" y2="52" stroke="var(--accent)" strokeWidth="2.5" strokeLinecap="round"/></svg>`,

  diamond80: `<svg viewBox="0 0 80 80" class="__pfx__-hook-icon" width="80" height="80"><polygon points="40,12 14,36 40,68 66,36" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)" strokeLinejoin="round"/><line x1="14" y1="36" x2="66" y2="36" stroke="var(--accent)" strokeWidth="1.5"/><line x1="40" y1="12" x2="40" y2="68" stroke="var(--accent)" strokeWidth="1.5"/></svg>`,

  book80: `<svg viewBox="0 0 80 80" class="__pfx__-hook-icon" width="80" height="80"><rect x="14" y="12" width="52" height="56" rx="4" stroke="var(--accent)" strokeWidth="3" fill="var(--accent-soft)"/><line x1="14" y1="36" x2="66" y2="36" stroke="var(--accent)" strokeWidth="2"/><line x1="14" y1="50" x2="66" y2="50" stroke="var(--accent)" strokeWidth="2"/></svg>`,

  /* ─── Card/check icons ─── */
  check32: `<svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="14" fill="none" stroke="var(--accent)" strokeWidth="2.5" opacity="0.3"/><path d="M9 16l5 5 9-9" fill="none" stroke="var(--accent)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>`,

  diamond32: `<svg viewBox="0 0 32 32" width="32" height="32"><polygon points="16,6 6,16 16,26 26,16" fill="var(--accent-soft)" stroke="var(--accent)" strokeWidth="2" strokeLinejoin="round"/></svg>`,
};

/**
 * Get hook SVG by key, replacing __pfx__ with the chapter prefix.
 */
function getHook(key, prefix) {
  const name = key + "80";
  const svg = ICONS[name] || ICONS.question80;
  return svg.replace(/__pfx__/g, prefix);
}

/**
 * Get small card icon.
 */
function getSmall(key) {
  const name = key + "32";
  return ICONS[name] || ICONS.check32;
}

module.exports = { getHook, getSmall },
  document32: `<svg viewBox="0 0 32 32" width="32" height="32"><rect x="6" y="4" width="20" height="24" rx="2" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)"/><line x1="10" y1="10" x2="22" y2="10" stroke="var(--accent)" strokeWidth="1.5" strokeLinecap="round"/><line x1="10" y1="15" x2="22" y2="15" stroke="var(--accent)" strokeWidth="1.5" strokeLinecap="round"/><line x1="10" y1="20" x2="18" y2="20" stroke="var(--accent)" strokeWidth="1.5" strokeLinecap="round"/></svg>`,

  calendar32: `<svg viewBox="0 0 32 32" width="32" height="32"><rect x="5" y="7" width="22" height="20" rx="2" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)"/><line x1="5" y1="13" x2="27" y2="13" stroke="var(--accent)" strokeWidth="2"/><path d="M10 3v4M22 3v4" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><text x="16" y="22" textAnchor="middle" fill="var(--accent)" fontSize="7" fontWeight="700">日期</text></svg>`,

  ring32: `<svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="8" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)"/><circle cx="16" cy="16" r="4" stroke="var(--accent)" strokeWidth="1.5" fill="none" strokeDasharray="2 1"/></svg>`,

  camera32: `<svg viewBox="0 0 32 32" width="32" height="32"><rect x="5" y="12" width="22" height="15" rx="3" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)"/><circle cx="16" cy="19" r="4" stroke="var(--accent)" strokeWidth="1.5" fill="none"/><circle cx="16" cy="19" r="2" fill="var(--accent)"/><path d="M13 8l3-2 3 2" stroke="var(--accent)" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round"/></svg>`,

  venue32: `<svg viewBox="0 0 32 32" width="32" height="32"><path d="M6 26V14l10-8 10 8v12" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" strokeLinejoin="round"/><line x1="12" y1="26" x2="12" y2="18" stroke="var(--accent)" strokeWidth="2"/><line x1="20" y1="26" x2="20" y2="18" stroke="var(--accent)" strokeWidth="2"/></svg>`,

  gift32: `<svg viewBox="0 0 32 32" width="32" height="32"><rect x="6" y="14" width="20" height="13" rx="2" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)"/><path d="M9 14V9a4 4 0 016 0v5M23 14V9a4 4 0 00-6 0v5" stroke="var(--accent)" strokeWidth="1.5" fill="none"/><line x1="16" y1="14" x2="16" y2="27" stroke="var(--accent)" strokeWidth="2"/></svg>`,

  globe32: `<svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="13" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)"/><ellipse cx="16" cy="16" rx="7" ry="13" stroke="var(--accent)" strokeWidth="1.5" fill="none"/><line x1="4" y1="16" x2="28" y2="16" stroke="var(--accent)" strokeWidth="1.5"/></svg>`,

  scale32: `<svg viewBox="0 0 32 32" width="32" height="32"><rect x="6" y="7" width="8" height="18" rx="2" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)"/><rect x="18" y="7" width="8" height="18" rx="2" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)"/><line x1="10" y1="25" x2="22" y2="25" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/></svg>`,

  clock32: `<svg viewBox="0 0 32 32" width="32" height="32"><circle cx="16" cy="16" r="13" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)"/><line x1="16" y1="6" x2="16" y2="16" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/><line x1="16" y1="16" x2="24" y2="20" stroke="var(--accent)" strokeWidth="2" strokeLinecap="round"/></svg>`,

  star32: `<svg viewBox="0 0 32 32" width="32" height="32"><path d="M16 4l4 10 11 1-8 7 3 11-10-6-10 6 3-11-8-7 11-1z" fill="var(--accent-soft)" stroke="var(--accent)" strokeWidth="1.5" strokeLinejoin="round"/></svg>`,

  heart32: `<svg viewBox="0 0 32 32" width="32" height="32"><path d="M16 10c-2-3-5-3-7-1s-2 5 1 7l6 6 6-6c3-2 3-5 1-7s-5-2-7 1z" fill="var(--accent-soft)" stroke="var(--accent)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/></svg>`,

  money32: `<svg viewBox="0 0 32 32" width="32" height="32"><rect x="4" y="8" width="24" height="16" rx="2" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)"/><circle cx="16" cy="16" r="4" stroke="var(--accent)" strokeWidth="1.5" fill="none"/><line x1="4" y1="13" x2="8" y2="13" stroke="var(--accent)" strokeWidth="1.5"/><line x1="4" y1="19" x2="8" y2="19" stroke="var(--accent)" strokeWidth="1.5"/><line x1="24" y1="13" x2="28" y2="13" stroke="var(--accent)" strokeWidth="1.5"/><line x1="24" y1="19" x2="28" y2="19" stroke="var(--accent)" strokeWidth="1.5"/></svg>`,

  chat32: `<svg viewBox="0 0 32 32" width="32" height="32"><path d="M4 5h24a2 2 0 012 2v14a2 2 0 01-2 2H10l-6 4V7a2 2 0 012-2z" stroke="var(--accent)" strokeWidth="2" fill="var(--accent-soft)" strokeLinejoin="round"/></svg>`,

;