import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Year1 } from "../chapters/02-year1/Year1";
import { NARRATIONS as N02 } from "../chapters/02-year1/narrations";
import { Year5 } from "../chapters/03-year5/Year5";
import { NARRATIONS as N03 } from "../chapters/03-year5/narrations";
import { Year10 } from "../chapters/04-year10/Year10";
import { NARRATIONS as N04 } from "../chapters/04-year10/narrations";
import { Year15 } from "../chapters/05-year15/Year15";
import { NARRATIONS as N05 } from "../chapters/05-year15/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "週年禮物指南", narrations: N01, Component: Coldopen },
  { id: "02-year1", title: "紙婚禮物", narrations: N02, Component: Year1 },
  { id: "03-year5", title: "木婚禮物", narrations: N03, Component: Year5 },
  { id: "04-year10", title: "錫婚禮物", narrations: N04, Component: Year10 },
  { id: "05-year15", title: "水晶婚禮物", narrations: N05, Component: Year15 },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },
];
