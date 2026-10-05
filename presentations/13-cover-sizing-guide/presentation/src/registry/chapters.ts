import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Standard } from "../chapters/02-standard/Standard";
import { NARRATIONS as N02 } from "../chapters/02-standard/narrations";
import { Measure } from "../chapters/03-measure/Measure";
import { NARRATIONS as N03 } from "../chapters/03-measure/narrations";
import { Fitting } from "../chapters/04-fitting/Fitting";
import { NARRATIONS as N04 } from "../chapters/04-fitting/narrations";
import { Tips } from "../chapters/05-tips/Tips";
import { NARRATIONS as N05 } from "../chapters/05-tips/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "證書套尺寸指南", narrations: N01, Component: Coldopen },
  { id: "02-standard", title: "標準尺寸", narrations: N02, Component: Standard },
  { id: "03-measure", title: "量度方法", narrations: N03, Component: Measure },
  { id: "04-fitting", title: "合身調整", narrations: N04, Component: Fitting },
  { id: "05-tips", title: "選購貼士", narrations: N05, Component: Tips },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];