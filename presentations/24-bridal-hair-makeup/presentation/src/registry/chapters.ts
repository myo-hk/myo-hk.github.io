import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Trial } from "../chapters/02-trial/Trial.tsx";
import { NARRATIONS as N02 } from "../chapters/02-trial/narrations";
import { Style } from "../chapters/03-style/Style.tsx";
import { NARRATIONS as N03 } from "../chapters/03-style/narrations";
import { Hair } from "../chapters/04-hair/Hair.tsx";
import { NARRATIONS as N04 } from "../chapters/04-hair/narrations";
import { Day } from "../chapters/05-day/Day.tsx";
import { NARRATIONS as N05 } from "../chapters/05-day/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "新娘化妝髮型指南", narrations: N01, Component: Coldopen },
  { id: "02-trial", title: "試妝安排", narrations: N02, Component: Trial },
  { id: "03-style", title: "造型建議", narrations: N03, Component: Style },
  { id: "04-hair", title: "時間安排", narrations: N04, Component: Hair },
  { id: "05-day", title: "大日子造型", narrations: N05, Component: Day },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];