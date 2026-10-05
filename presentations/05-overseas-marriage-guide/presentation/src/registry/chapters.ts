import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Requirements } from "../chapters/02-requirements/Requirements";
import { NARRATIONS as N02 } from "../chapters/02-requirements/narrations";
import { Documents } from "../chapters/03-documents/Documents";
import { NARRATIONS as N03 } from "../chapters/03-documents/narrations";
import { Process } from "../chapters/04-process/Process";
import { NARRATIONS as N04 } from "../chapters/04-process/narrations";
import { Legalization } from "../chapters/05-legalization/Legalization";
import { NARRATIONS as N05 } from "../chapters/05-legalization/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "海外結婚指南", narrations: N01, Component: Coldopen },
  { id: "02-requirements", title: "申請資格", narrations: N02, Component: Requirements },
  { id: "03-documents", title: "所需文件", narrations: N03, Component: Documents },
  { id: "04-process", title: "辦理流程", narrations: N04, Component: Process },
  { id: "05-legalization", title: "文件認證", narrations: N05, Component: Legalization },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];