import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Cleaning } from "../chapters/02-cleaning/Cleaning.tsx";
import { NARRATIONS as N02 } from "../chapters/02-cleaning/narrations";
import { Storage } from "../chapters/03-storage/Storage.tsx";
import { NARRATIONS as N03 } from "../chapters/03-storage/narrations";
import { Handling } from "../chapters/04-handling/Handling.tsx";
import { NARRATIONS as N04 } from "../chapters/04-handling/narrations";
import { Materials } from "../chapters/05-materials/Materials.tsx";
import { NARRATIONS as N05 } from "../chapters/05-materials/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "證書套保存指南", narrations: N01, Component: Coldopen },
  { id: "02-cleaning", title: "清潔方法", narrations: N02, Component: Cleaning },
  { id: "03-storage", title: "存放方式", narrations: N03, Component: Storage },
  { id: "04-handling", title: "保護技巧", narrations: N04, Component: Handling },
  { id: "05-materials", title: "維修須知", narrations: N05, Component: Materials },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA }
];