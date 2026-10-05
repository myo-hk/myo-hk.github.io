import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Why } from "../chapters/02-why/Why";
import { NARRATIONS as N02 } from "../chapters/02-why/narrations";
import { Methods } from "../chapters/03-methods/Methods";
import { NARRATIONS as N03 } from "../chapters/03-methods/narrations";
import { Calendar } from "../chapters/04-calendar/Calendar";
import { NARRATIONS as N04 } from "../chapters/04-calendar/narrations";
import { Tips } from "../chapters/05-tips/Tips";
import { NARRATIONS as N05 } from "../chapters/05-tips/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "吉日選擇指南", narrations: N01, Component: Coldopen },
  { id: "02-why", title: "為何要揀好日子", narrations: N02, Component: Why },
  { id: "03-methods", title: "揀日方法", narrations: N03, Component: Methods },
  { id: "04-calendar", title: "如何睇日曆", narrations: N04, Component: Calendar },
  { id: "05-tips", title: "揀日技巧", narrations: N05, Component: Tips },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];