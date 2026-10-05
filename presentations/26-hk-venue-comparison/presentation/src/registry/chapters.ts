import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Hotel } from "../chapters/02-hotel/Hotel.tsx";
import { NARRATIONS as N02 } from "../chapters/02-hotel/narrations";
import { Restaurant } from "../chapters/03-restaurant/Restaurant.tsx";
import { NARRATIONS as N03 } from "../chapters/03-restaurant/narrations";
import { Church } from "../chapters/04-church/Church.tsx";
import { NARRATIONS as N04 } from "../chapters/04-church/narrations";
import { Outdoor } from "../chapters/05-outdoor/Outdoor.tsx";
import { NARRATIONS as N05 } from "../chapters/05-outdoor/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "香港婚禮場地比較", narrations: N01, Component: Coldopen },
  { id: "02-hotel", title: "酒店選擇", narrations: N02, Component: Hotel },
  { id: "03-restaurant", title: "餐廳選擇", narrations: N03, Component: Restaurant },
  { id: "04-church", title: "教堂場地", narrations: N04, Component: Church },
  { id: "05-outdoor", title: "戶外場地", narrations: N05, Component: Outdoor },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];