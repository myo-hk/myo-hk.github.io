import type { ChapterDef } from "./types";
import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { Cost1Registration } from "../chapters/02-cost1-registration/Cost1Registration";
import { Cost2Ring } from "../chapters/03-cost2-ring/Cost2Ring";
import { Cost3Photo } from "../chapters/04-cost3-photo/Cost3Photo";
import { Cost4Banquet } from "../chapters/05-cost4-banquet/Cost4Banquet";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { NARRATIONS as N02 } from "../chapters/02-cost1-registration/narrations";
import { NARRATIONS as N03 } from "../chapters/03-cost2-ring/narrations";
import { NARRATIONS as N04 } from "../chapters/04-cost3-photo/narrations";
import { NARRATIONS as N05 } from "../chapters/05-cost4-banquet/narrations";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "結婚要幾錢？", narrations: N01, Component: Coldopen },
  { id: "02-cost1-registration", title: "註冊費用", narrations: N02, Component: Cost1Registration },
  { id: "03-cost2-ring", title: "婚戒預算", narrations: N03, Component: Cost2Ring },
  { id: "04-cost3-photo", title: "攝影費用", narrations: N04, Component: Cost3Photo },
  { id: "05-cost4-banquet", title: "婚宴開支", narrations: N05, Component: Cost4Banquet },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },
];
