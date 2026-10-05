import type { ChapterDef } from "./types";

import { Coldopen } from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as N01 } from "../chapters/01-coldopen/narrations";
import { Classic } from "../chapters/02-classic/Classic.tsx";
import { NARRATIONS as N02 } from "../chapters/02-classic/narrations";
import { Modern } from "../chapters/03-modern/Modern.tsx";
import { NARRATIONS as N03 } from "../chapters/03-modern/narrations";
import { Fit } from "../chapters/04-fit/Fit.tsx";
import { NARRATIONS as N04 } from "../chapters/04-fit/narrations";
import { Accessories } from "../chapters/05-accessories/Accessories.tsx";
import { NARRATIONS as N05 } from "../chapters/05-accessories/narrations";
import { CTA } from "../chapters/06-cta/CTA";
import { NARRATIONS as N06 } from "../chapters/06-cta/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "01-coldopen", title: "新郎西裝指南", narrations: N01, Component: Coldopen },
  { id: "02-classic", title: "租借方案", narrations: N02, Component: Classic },
  { id: "03-modern", title: "購買方案", narrations: N03, Component: Modern },
  { id: "04-fit", title: "配飾搭配", narrations: N04, Component: Fit },
  { id: "05-accessories", title: "配飾搭配", narrations: N05, Component: Accessories },
  { id: "06-cta", title: "總結與下一步", narrations: N06, Component: CTA },];