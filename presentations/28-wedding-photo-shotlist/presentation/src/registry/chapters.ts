import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Prep } from "../chapters/02-prep/Prep.tsx";
import { NARRATIONS as N02 } from "../chapters/02-prep/narrations";
import { Ceremony } from "../chapters/03-ceremony/Ceremony.tsx";
import { NARRATIONS as N03 } from "../chapters/03-ceremony/narrations";
import { Group } from "../chapters/04-group/Group.tsx";
import { NARRATIONS as N04 } from "../chapters/04-group/narrations";
import { Couple } from "../chapters/05-couple/Couple.tsx";
import { NARRATIONS as N05 } from "../chapters/05-couple/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "婚紗相必影清單", narrations: N01, Component: Coldopen },
  { id: "02-prep", title: "準備環節", narrations: N02, Component: Prep },
  { id: "03-ceremony", title: "婚禮儀式", narrations: N03, Component: Ceremony },
  { id: "04-group", title: "婚宴拍攝", narrations: N04, Component: Group },
  { id: "05-couple", title: "新人pose", narrations: N05, Component: Couple },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];