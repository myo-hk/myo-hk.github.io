import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Clean } from "../chapters/02-clean/Clean.tsx";
import { NARRATIONS as N02 } from "../chapters/02-clean/narrations";
import { Storage } from "../chapters/03-storage/Storage.tsx";
import { NARRATIONS as N03 } from "../chapters/03-storage/narrations";
import { Avoid } from "../chapters/04-avoid/Avoid.tsx";
import { NARRATIONS as N04 } from "../chapters/04-avoid/narrations";
import { Preserve } from "../chapters/05-preserve/Preserve.tsx";
import { NARRATIONS as N05 } from "../chapters/05-preserve/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "婚紗保存方法", narrations: N01, Component: Coldopen },
  { id: "02-clean", title: "清潔方法", narrations: N02, Component: Clean },
  { id: "03-storage", title: "存放方式", narrations: N03, Component: Storage },
  { id: "04-avoid", title: "保護技巧", narrations: N04, Component: Avoid },
  { id: "05-preserve", title: "保存技巧", narrations: N05, Component: Preserve },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];