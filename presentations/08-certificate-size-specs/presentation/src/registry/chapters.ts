import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Size } from "../chapters/02-size/Size";
import { NARRATIONS as N02 } from "../chapters/02-size/narrations";
import { Content } from "../chapters/03-content/Content";
import { NARRATIONS as N03 } from "../chapters/03-content/narrations";
import { Care } from "../chapters/04-care/Care";
import { NARRATIONS as N04 } from "../chapters/04-care/narrations";
import { Myo } from "../chapters/05-myo/Myo";
import { NARRATIONS as N05 } from "../chapters/05-myo/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "結婚證書尺寸規格", narrations: N01, Component: Coldopen },
  { id: "02-size", title: "標準尺寸", narrations: N02, Component: Size },
  { id: "03-content", title: "內容話你知", narrations: N03, Component: Content },
  { id: "04-care", title: "保養心得", narrations: N04, Component: Care },
  { id: "05-myo", title: "MyO 證書套", narrations: N05, Component: Myo },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];