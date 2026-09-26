import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Reasons } from "../chapters/02-reasons/Reasons";
import { NARRATIONS as N02 } from "../chapters/02-reasons/narrations";
import { Process } from "../chapters/03-process/Process";
import { NARRATIONS as N03 } from "../chapters/03-process/narrations";
import { Documents } from "../chapters/04-documents/Documents";
import { NARRATIONS as N04 } from "../chapters/04-documents/narrations";
import { Timeline } from "../chapters/05-timeline/Timeline";
import { NARRATIONS as N05 } from "../chapters/05-timeline/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "婚後改名指南", narrations: N01, Component: Coldopen },
  { id: "02-reasons", title: "改名原因", narrations: N02, Component: Reasons },
  { id: "03-process", title: "改名程序", narrations: N03, Component: Process },
  { id: "04-documents", title: "所需文件", narrations: N04, Component: Documents },
  { id: "05-timeline", title: "時間流程", narrations: N05, Component: Timeline },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];