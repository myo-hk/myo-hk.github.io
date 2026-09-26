import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Engagement } from "../chapters/02-engagement/Engagement.tsx";
import { NARRATIONS as N02 } from "../chapters/02-engagement/narrations";
import { Wedding } from "../chapters/03-wedding/Wedding.tsx";
import { NARRATIONS as N03 } from "../chapters/03-wedding/narrations";
import { Differences } from "../chapters/04-differences/Differences.tsx";
import { NARRATIONS as N04 } from "../chapters/04-differences/narrations";
import { Wear } from "../chapters/05-wear/Wear.tsx";
import { NARRATIONS as N05 } from "../chapters/05-wear/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "訂婚戒 vs 結婚戒", narrations: N01, Component: Coldopen },
  { id: "02-engagement", title: "定義分別", narrations: N02, Component: Engagement },
  { id: "03-wedding", title: "風格比較", narrations: N03, Component: Wedding },
  { id: "04-differences", title: "費用預算", narrations: N04, Component: Differences },
  { id: "05-wear", title: "風格比較", narrations: N05, Component: Wear },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];