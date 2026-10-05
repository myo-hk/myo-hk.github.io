import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Dates } from "../chapters/02-dates/Dates";
import { NARRATIONS as N02 } from "../chapters/02-dates/narrations";
import { Items } from "../chapters/03-items/Items";
import { NARRATIONS as N03 } from "../chapters/03-items/narrations";
import { Actions } from "../chapters/04-actions/Actions";
import { NARRATIONS as N04 } from "../chapters/04-actions/narrations";
import { Modern } from "../chapters/05-modern/Modern";
import { NARRATIONS as N05 } from "../chapters/05-modern/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "婚禮禁忌大全", narrations: N01, Component: Coldopen },
  { id: "02-dates", title: "日子禁忌", narrations: N02, Component: Dates },
  { id: "03-items", title: "物品禁忌", narrations: N03, Component: Items },
  { id: "04-actions", title: "行為禁忌", narrations: N04, Component: Actions },
  { id: "05-modern", title: "現代觀點", narrations: N05, Component: Modern },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },
];
