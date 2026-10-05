import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Prepare } from "../chapters/02-prepare/Prepare";
import { NARRATIONS as N02 } from "../chapters/02-prepare/narrations";
import { Order } from "../chapters/03-order/Order";
import { NARRATIONS as N03 } from "../chapters/03-order/narrations";
import { Kneeling } from "../chapters/04-kneeling/Kneeling";
import { NARRATIONS as N04 } from "../chapters/04-kneeling/narrations";
import { Gifts } from "../chapters/05-gifts/Gifts";
import { NARRATIONS as N05 } from "../chapters/05-gifts/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "敬茶儀式指南", narrations: N01, Component: Coldopen },
  { id: "02-prepare", title: "準備工作", narrations: N02, Component: Prepare },
  { id: "03-order", title: "禮儀規範", narrations: N03, Component: Order },
  { id: "04-kneeling", title: "誓詞環節", narrations: N04, Component: Kneeling },
  { id: "05-gifts", title: "敬茶禮物", narrations: N05, Component: Gifts },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];