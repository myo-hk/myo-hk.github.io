import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Cut } from "../chapters/02-cut/Cut.tsx";
import { NARRATIONS as N02 } from "../chapters/02-cut/narrations";
import { Color } from "../chapters/03-color/Color.tsx";
import { NARRATIONS as N03 } from "../chapters/03-color/narrations";
import { Clarity } from "../chapters/04-clarity/Clarity.tsx";
import { NARRATIONS as N04 } from "../chapters/04-clarity/narrations";
import { Carat } from "../chapters/05-carat/Carat.tsx";
import { NARRATIONS as N05 } from "../chapters/05-carat/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "鑽石4C指南", narrations: N01, Component: Coldopen },
  { id: "02-cut", title: "切割grading", narrations: N02, Component: Cut },
  { id: "03-color", title: "成色grading", narrations: N03, Component: Color },
  { id: "04-clarity", title: "淨度grading", narrations: N04, Component: Clarity },
  { id: "05-carat", title: "克拉重量", narrations: N05, Component: Carat },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA }
];
