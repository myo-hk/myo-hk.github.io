import type { ChapterDef } from "./types";
import Coldopen from "../chapters/01-coldopen/Coldopen";
import { NARRATIONS as coldopenNarrations } from "../chapters/01-coldopen/narrations";
import Eligibility from "../chapters/02-eligibility/Eligibility";
import { NARRATIONS as eligibilityNarrations } from "../chapters/02-eligibility/narrations";
import Notice from "../chapters/03-notice/Notice";
import { NARRATIONS as noticeNarrations } from "../chapters/03-notice/narrations";
import Venue from "../chapters/04-venue/Venue";
import { NARRATIONS as venueNarrations } from "../chapters/04-venue/narrations";
import Ceremony from "../chapters/05-ceremony/Ceremony";
import { NARRATIONS as ceremonyNarrations } from "../chapters/05-ceremony/narrations";
import After from "../chapters/06-after/After";
import { NARRATIONS as afterNarrations } from "../chapters/06-after/narrations";

export const CHAPTERS: ChapterDef[] = [
  {
    id: "coldopen",
    title: "你準備好結婚了嗎？",
    narrations: coldopenNarrations,
    Component: Coldopen,
  },
  {
    id: "eligibility",
    title: "結婚資格與文件",
    narrations: eligibilityNarrations,
    Component: Eligibility,
  },
  {
    id: "notice",
    title: "遞交擬結婚通知書",
    narrations: noticeNarrations,
    Component: Notice,
  },
  {
    id: "venue",
    title: "婚禮場地三種選擇",
    narrations: venueNarrations,
    Component: Venue,
  },
  {
    id: "ceremony",
    title: "婚禮當天流程",
    narrations: ceremonyNarrations,
    Component: Ceremony,
  },
  {
    id: "after",
    title: "婚後事項",
    narrations: afterNarrations,
    Component: After,
  },
];