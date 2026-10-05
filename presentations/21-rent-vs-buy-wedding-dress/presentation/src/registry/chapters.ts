import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Rent } from "../chapters/02-rent/Rent.tsx";
import { NARRATIONS as N02 } from "../chapters/02-rent/narrations";
import { Buy } from "../chapters/03-buy/Buy.tsx";
import { NARRATIONS as N03 } from "../chapters/03-buy/narrations";
import { Consider } from "../chapters/04-consider/Consider.tsx";
import { NARRATIONS as N04 } from "../chapters/04-consider/narrations";
import { Hybrid } from "../chapters/05-hybrid/Hybrid.tsx";
import { NARRATIONS as N05 } from "../chapters/05-hybrid/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "租 vs 買婚紗", narrations: N01, Component: Coldopen },
  { id: "02-rent", title: "費用比較", narrations: N02, Component: Rent },
  { id: "03-buy", title: "方便程度", narrations: N03, Component: Buy },
  { id: "04-consider", title: "定制選項", narrations: N04, Component: Consider },
  { id: "05-hybrid", title: "租定買？", narrations: N05, Component: Hybrid },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];