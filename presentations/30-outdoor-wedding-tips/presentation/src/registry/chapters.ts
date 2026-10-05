import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Weather } from "../chapters/02-weather/Weather.tsx";
import { NARRATIONS as N02 } from "../chapters/02-weather/narrations";
import { Deco } from "../chapters/03-deco/Deco.tsx";
import { NARRATIONS as N03 } from "../chapters/03-deco/narrations";
import { Logistics } from "../chapters/04-logistics/Logistics.tsx";
import { NARRATIONS as N04 } from "../chapters/04-logistics/narrations";
import { Photo } from "../chapters/05-photo/Photo.tsx";
import { NARRATIONS as N05 } from "../chapters/05-photo/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "戶外婚禮貼士", narrations: N01, Component: Coldopen },
  { id: "02-weather", title: "場地選擇", narrations: N02, Component: Weather },
  { id: "03-deco", title: "天氣應對", narrations: N03, Component: Deco },
  { id: "04-logistics", title: "場地佈置", narrations: N04, Component: Logistics },
  { id: "05-photo", title: "戶外拍攝", narrations: N05, Component: Photo },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];