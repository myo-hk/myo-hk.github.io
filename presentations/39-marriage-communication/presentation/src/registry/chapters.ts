import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Listen } from "../chapters/02-listen/Listen";
import { NARRATIONS as N02 } from "../chapters/02-listen/narrations";
import { Express } from "../chapters/03-express/Express";
import { NARRATIONS as N03 } from "../chapters/03-express/narrations";
import { Weekly } from "../chapters/04-weekly/Weekly";
import { NARRATIONS as N04 } from "../chapters/04-weekly/narrations";
import { Conflict } from "../chapters/05-conflict/Conflict";
import { NARRATIONS as N05 } from "../chapters/05-conflict/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "婚姻溝通技巧", narrations: N01, Component: Coldopen },
  { id: "02-listen", title: "衝突處理", narrations: N02, Component: Listen },
  { id: "03-express", title: "親密關係", narrations: N03, Component: Express },
  { id: "04-weekly", title: "每週傾談", narrations: N04, Component: Weekly },
  { id: "05-conflict", title: "處理衝突", narrations: N05, Component: Conflict },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];