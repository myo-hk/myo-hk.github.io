import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { sixMonths } from "../chapters/02-sixMonths/sixMonths";
import { NARRATIONS as N02 } from "../chapters/02-sixMonths/narrations";
import { threeMonths } from "../chapters/03-threeMonths/threeMonths";
import { NARRATIONS as N03 } from "../chapters/03-threeMonths/narrations";
import { oneMonth } from "../chapters/04-oneMonth/oneMonth";
import { NARRATIONS as N04 } from "../chapters/04-oneMonth/narrations";
import { oneWeek } from "../chapters/05-oneWeek/oneWeek";
import { NARRATIONS as N05 } from "../chapters/05-oneWeek/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "新娘護膚時間表", narrations: N01, Component: Coldopen },
  { id: "02-sixMonths", title: "六個月前", narrations: N02, Component: sixMonths },
  { id: "03-threeMonths", title: "三個月前", narrations: N03, Component: threeMonths },
  { id: "04-oneMonth", title: "一個月前", narrations: N04, Component: oneMonth },
  { id: "05-oneWeek", title: "一星期前", narrations: N05, Component: oneWeek },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },
];
