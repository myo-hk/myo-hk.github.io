import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Legal } from "../chapters/02-legal/Legal";
import { NARRATIONS as N02 } from "../chapters/02-legal/narrations";
import { Property } from "../chapters/03-property/Property";
import { NARRATIONS as N03 } from "../chapters/03-property/narrations";
import { Prenup } from "../chapters/04-prenup/Prenup";
import { NARRATIONS as N04 } from "../chapters/04-prenup/narrations";
import { Tax } from "../chapters/05-tax/Tax";
import { NARRATIONS as N05 } from "../chapters/05-tax/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "結婚法律與財產", narrations: N01, Component: Coldopen },
  { id: "02-legal", title: "法律權益", narrations: N02, Component: Legal },
  { id: "03-property", title: "財產安排", narrations: N03, Component: Property },
  { id: "04-prenup", title: "婚前協議", narrations: N04, Component: Prenup },
  { id: "05-tax", title: "稅務須知", narrations: N05, Component: Tax },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];