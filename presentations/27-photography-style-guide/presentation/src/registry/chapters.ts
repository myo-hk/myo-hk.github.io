import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Traditional } from "../chapters/02-traditional/Traditional.tsx";
import { NARRATIONS as N02 } from "../chapters/02-traditional/narrations";
import { Reportage } from "../chapters/03-reportage/Reportage.tsx";
import { NARRATIONS as N03 } from "../chapters/03-reportage/narrations";
import { Fashion } from "../chapters/04-fashion/Fashion.tsx";
import { NARRATIONS as N04 } from "../chapters/04-fashion/narrations";
import { Mix } from "../chapters/05-mix/Mix.tsx";
import { NARRATIONS as N05 } from "../chapters/05-mix/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "婚禮攝影風格指南", narrations: N01, Component: Coldopen },
  { id: "02-traditional", title: "紀實風格", narrations: N02, Component: Traditional },
  { id: "03-reportage", title: "傳統風格", narrations: N03, Component: Reportage },
  { id: "04-fashion", title: "藝術風格", narrations: N04, Component: Fashion },
  { id: "05-mix", title: "混合風格", narrations: N05, Component: Mix },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];