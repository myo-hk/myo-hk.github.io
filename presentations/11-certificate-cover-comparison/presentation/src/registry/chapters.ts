import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Leather } from "../chapters/02-leather/Leather";
import { NARRATIONS as N02 } from "../chapters/02-leather/narrations";
import { Linen } from "../chapters/03-linen/Linen";
import { NARRATIONS as N03 } from "../chapters/03-linen/narrations";
import { Velvet } from "../chapters/04-velvet/Velvet";
import { NARRATIONS as N04 } from "../chapters/04-velvet/narrations";
import { Custom } from "../chapters/05-custom/Custom";
import { NARRATIONS as N05 } from "../chapters/05-custom/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "結婚證書套比較", narrations: N01, Component: Coldopen },
  { id: "02-leather", title: "材質比較", narrations: N02, Component: Leather },
  { id: "03-linen", title: "手感質地", narrations: N03, Component: Linen },
  { id: "04-velvet", title: "耐用程度", narrations: N04, Component: Velvet },
  { id: "05-custom", title: "價格分析", narrations: N05, Component: Custom },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];