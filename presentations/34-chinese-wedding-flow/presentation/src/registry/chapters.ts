import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Proposal } from "../chapters/02-proposal/Proposal";
import { NARRATIONS as N02 } from "../chapters/02-proposal/narrations";
import { Guoda } from "../chapters/03-guoda/Guoda";
import { NARRATIONS as N03 } from "../chapters/03-guoda/narrations";
import { Wedding } from "../chapters/04-wedding/Wedding";
import { NARRATIONS as N04 } from "../chapters/04-wedding/narrations";
import { Honeymoon } from "../chapters/05-honeymoon/Honeymoon";
import { NARRATIONS as N05 } from "../chapters/05-honeymoon/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "中式結婚流程", narrations: N01, Component: Coldopen },
  { id: "02-proposal", title: "提親", narrations: N02, Component: Proposal },
  { id: "03-guoda", title: "過大禮", narrations: N03, Component: Guoda },
  { id: "04-wedding", title: "婚禮當日", narrations: N04, Component: Wedding },
  { id: "05-honeymoon", title: "回門", narrations: N05, Component: Honeymoon },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },
];
