import type { ChapterDef } from "./types";
import Coldopen from "../chapters/01-coldopen/Coldopen";
import { Timeline } from "../chapters/02-timeline/Timeline";
import { Checklist } from "../chapters/03-checklist/Checklist";
import { Budget } from "../chapters/04-budget/Budget";
import { Vendors } from "../chapters/05-vendors/Vendors";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { NARRATIONS as N02 } from "../chapters/02-timeline/narrations";
import { NARRATIONS as N03 } from "../chapters/03-checklist/narrations";
import { NARRATIONS as N04 } from "../chapters/04-budget/narrations";
import { NARRATIONS as N05 } from "../chapters/05-vendors/narrations";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "你準備好結婚了嗎？", narrations: N01, Component: Coldopen },
  { id: "02-timeline", title: "12 個月部署時間表", narrations: N02, Component: Timeline },
  { id: "03-checklist", title: "婚禮必做清單", narrations: N03, Component: Checklist },
  { id: "04-budget", title: "結婚費用預算", narrations: N04, Component: Budget },
  { id: "05-vendors", title: "供應商選擇貼士", narrations: N05, Component: Vendors },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },
];
