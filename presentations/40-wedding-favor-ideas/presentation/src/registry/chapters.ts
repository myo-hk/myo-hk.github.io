import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Food } from "../chapters/02-food/Food";
import { NARRATIONS as N02 } from "../chapters/02-food/narrations";
import { Candles } from "../chapters/03-candles/Candles";
import { NARRATIONS as N03 } from "../chapters/03-candles/narrations";
import { Personal } from "../chapters/04-personal/Personal";
import { NARRATIONS as N04 } from "../chapters/04-personal/narrations";
import { Practical } from "../chapters/05-practical/Practical";
import { NARRATIONS as N05 } from "../chapters/05-practical/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "婚禮回禮Ideas", narrations: N01, Component: Coldopen },
  { id: "02-food", title: "創意主意", narrations: N02, Component: Food },
  { id: "03-candles", title: "預算考慮", narrations: N03, Component: Candles },
  { id: "04-personal", title: "個人化禮物", narrations: N04, Component: Personal },
  { id: "05-practical", title: "實用回禮", narrations: N05, Component: Practical },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];