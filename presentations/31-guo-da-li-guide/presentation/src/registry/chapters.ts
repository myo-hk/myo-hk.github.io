import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Gifts } from "../chapters/02-gifts/Gifts.tsx";
import { NARRATIONS as N02 } from "../chapters/02-gifts/narrations";
import { Process } from "../chapters/03-process/Process.tsx";
import { NARRATIONS as N03 } from "../chapters/03-process/narrations";
import { Modern } from "../chapters/04-modern/Modern.tsx";
import { NARRATIONS as N04 } from "../chapters/04-modern/narrations";
import { Advice } from "../chapters/05-advice/Advice.tsx";
import { NARRATIONS as N05 } from "../chapters/05-advice/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "過大禮完整指南", narrations: N01, Component: Coldopen },
  { id: "02-gifts", title: "準備工作", narrations: N02, Component: Gifts },
  { id: "03-process", title: "禮儀細節", narrations: N03, Component: Process },
  { id: "04-modern", title: "禁忌習俗", narrations: N04, Component: Modern },
  { id: "05-advice", title: "過大禮貼士", narrations: N05, Component: Advice },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];