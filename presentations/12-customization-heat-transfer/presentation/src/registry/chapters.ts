import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Technology } from "../chapters/02-technology/Technology";
import { NARRATIONS as N02 } from "../chapters/02-technology/narrations";
import { Durability } from "../chapters/03-durability/Durability";
import { NARRATIONS as N03 } from "../chapters/03-durability/narrations";
import { Colors } from "../chapters/04-colors/Colors";
import { NARRATIONS as N04 } from "../chapters/04-colors/narrations";
import { Custom } from "../chapters/05-custom/Custom";
import { NARRATIONS as N05 } from "../chapters/05-custom/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "證書套熱轉印訂製", narrations: N01, Component: Coldopen },
  { id: "02-technology", title: "設計選擇", narrations: N02, Component: Technology },
  { id: "03-durability", title: "顏色建議", narrations: N03, Component: Durability },
  { id: "04-colors", title: "字體款式", narrations: N04, Component: Colors },
  { id: "05-custom", title: "確認稿樣", narrations: N05, Component: Custom },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA }
];