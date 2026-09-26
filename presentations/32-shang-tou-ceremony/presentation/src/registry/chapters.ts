import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Meaning } from "../chapters/02-meaning/Meaning.tsx";
import { NARRATIONS as N02 } from "../chapters/02-meaning/narrations";
import { Time } from "../chapters/03-time/Time.tsx";
import { NARRATIONS as N03 } from "../chapters/03-time/narrations";
import { Items } from "../chapters/04-items/Items.tsx";
import { NARRATIONS as N04 } from "../chapters/04-items/narrations";
import { Steps } from "../chapters/05-steps/Steps.tsx";
import { NARRATIONS as N05 } from "../chapters/05-steps/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "上頭儀式指南", narrations: N01, Component: Coldopen },
  { id: "02-meaning", title: "習俗意義", narrations: N02, Component: Meaning },
  { id: "03-time", title: "時間安排", narrations: N03, Component: Time },
  { id: "04-items", title: "禮儀規範", narrations: N04, Component: Items },
  { id: "05-steps", title: "上頭步驟", narrations: N05, Component: Steps },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];