import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Japan } from "../chapters/02-japan/Japan";
import { NARRATIONS as N02 } from "../chapters/02-japan/narrations";
import { Thailand } from "../chapters/03-thailand/Thailand";
import { NARRATIONS as N03 } from "../chapters/03-thailand/narrations";
import { Europe } from "../chapters/04-europe/Europe";
import { NARRATIONS as N04 } from "../chapters/04-europe/narrations";
import { Taiwan } from "../chapters/05-taiwan/Taiwan";
import { NARRATIONS as N05 } from "../chapters/05-taiwan/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "蜜月目的地推薦", narrations: N01, Component: Coldopen },
  { id: "02-japan", title: "亞洲目的地", narrations: N02, Component: Japan },
  { id: "03-thailand", title: "歐洲目的地", narrations: N03, Component: Thailand },
  { id: "04-europe", title: "海島度假", narrations: N04, Component: Europe },
  { id: "05-taiwan", title: "台灣蜜月", narrations: N05, Component: Taiwan },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];