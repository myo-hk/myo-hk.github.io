import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Venues } from "../chapters/02-venues/Venues.tsx";
import { NARRATIONS as N02 } from "../chapters/02-venues/narrations";
import { Booking } from "../chapters/03-booking/Booking.tsx";
import { NARRATIONS as N03 } from "../chapters/03-booking/narrations";
import { Ceremony } from "../chapters/04-ceremony/Ceremony.tsx";
import { NARRATIONS as N04 } from "../chapters/04-ceremony/narrations";
import { Dress } from "../chapters/05-dress/Dress.tsx";
import { NARRATIONS as N05 } from "../chapters/05-dress/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "教堂婚禮指南", narrations: N01, Component: Coldopen },
  { id: "02-venues", title: "預訂流程", narrations: N02, Component: Venues },
  { id: "03-booking", title: "婚禮儀式", narrations: N03, Component: Booking },
  { id: "04-ceremony", title: "接待安排", narrations: N04, Component: Ceremony },
  { id: "05-dress", title: "教堂婚紗", narrations: N05, Component: Dress },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];