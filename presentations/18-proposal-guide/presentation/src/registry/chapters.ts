import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Where } from "../chapters/02-where/Where.tsx";
import { NARRATIONS as N02 } from "../chapters/02-where/narrations";
import { Ring } from "../chapters/03-ring/Ring.tsx";
import { NARRATIONS as N03 } from "../chapters/03-ring/narrations";
import { Words } from "../chapters/04-words/Words.tsx";
import { NARRATIONS as N04 } from "../chapters/04-words/narrations";
import { Photography } from "../chapters/05-photography/Photography.tsx";
import { NARRATIONS as N05 } from "../chapters/05-photography/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "求婚大作戰攻略", narrations: N01, Component: Coldopen },
  { id: "02-where", title: "時機選擇", narrations: N02, Component: Where },
  { id: "03-ring", title: "地點建議", narrations: N03, Component: Ring },
  { id: "04-words", title: "戒指揀選", narrations: N04, Component: Words },
  { id: "05-photography", title: "求婚台詞", narrations: N05, Component: Photography },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];