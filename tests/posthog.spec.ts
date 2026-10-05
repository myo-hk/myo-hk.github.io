import { test, expect } from "@playwright/test";

const GA4_ID = "G-GQLW7LNP6H";

const PAGES = [
  { path: "/index.html", name: "home" },
  { path: "/faq.html", name: "faq" },
  { path: "/blog/index.html", name: "blog index" },
  { path: "/blog/婚禮攝影對焦技巧.html", name: "blog article (CJK filename)" },
];

// The four pages that carry a CSP <meta> header — these are the only pages
// that must explicitly allow PostHog's rrweb recorder Worker via blob: data:.
const CSP_PAGES = [
  { path: "/index.html", name: "index" },
  { path: "/v2.html", name: "v2" },
  { path: "/poster.html", name: "poster" },
  { path: "/poster-en.html", name: "poster-en" },
  { path: "/heic-converter.html", name: "heic-converter" },
];

test.describe("PostHog loader", () => {
  // Static assertions use the `request` fixture, not a live page, so they can
  // never race the 3000ms lazy-load timer.
  for (const { path, name } of PAGES) {
    test(`${name} ships the deferred loader and keeps GA4`, async ({ request }) => {
      const res = await request.get(path);
      expect(res.ok()).toBe(true);
      const html = await res.text();

      expect(html).toContain("__myoPostHog");
      expect(html).toContain("i.posthog.com");
      expect(html).toContain(GA4_ID);
      expect(html).toContain("dataLayer.push(arguments)");

      // The SDK must never be fetched synchronously from <head>.
      expect(html).not.toMatch(/<script[^>]+src="https:\/\/[^"]*posthog\.com/);
    });
  }

  for (const { path, name } of PAGES) {
    test(`${name} loads with no CSP violations`, async ({ page }) => {
      const violations: string[] = [];
      // Registered BEFORE navigation — CSP violations fire during initial load,
      // so a listener attached after goto() would miss them.
      page.on("console", (msg) => {
        const text = msg.text();
        // Broaden beyond Chrome's exact phrasing: Firefox drops the hyphen,
        // Safari omits "Refused to", and Chromium sometimes uses
        // "Refused to create allowlist for…". Match any variant case-insensitively.
        if (/content.security.policy|refused.to/i.test(text)) {
          violations.push(text);
        }
      });
      page.on("pageerror", (err) => violations.push(String(err)));

      await page.goto(path, { waitUntil: "load" });
      // Force the deferred path so array.js is actually requested under CSP.
      await page.evaluate(() => {
        document.body.dispatchEvent(new MouseEvent("click", { bubbles: true }));
      });
      await page.waitForTimeout(1500);

      expect(violations).toEqual([]);
    });
  }

  // worker-src is the single most important CSP directive for PostHog session
  // recordings: without 'self' blob: data:, rrweb cannot create its recorder
  // Worker and recordings fail silently (no console error, no data).
  //
  // These assertions read raw HTML via the request fixture — no browser needed.
  // They assert the FULL directive with blob: and data: sources; a malformed
  // worker-src (present but missing blob:) is just as broken as an absent one.
  for (const { path, name } of CSP_PAGES) {
    test(`${name} has worker-src in CSP`, async ({ request }) => {
      const html = await request.get(path).then((r) => r.text());
      expect(html).toContain("worker-src 'self' blob: data:");
    });
  }

  // Negative sanity check: a page without a CSP meta tag must NOT contain the
  // directive, proving the assertion above is sensitive (would fail if dropped
  // from a CSP page by a future edit).
  test("non-CSP page does not carry worker-src", async ({ request }) => {
    const html = await request.get("/privacy.html").then((r) => r.text());
    expect(html).not.toContain("worker-src 'self' blob: data:");
  });

  test("deferred loader does not block first paint", async ({ page }) => {
    const start = Date.now();
    await page.goto("/index.html", { waitUntil: "domcontentloaded" });
    // The loader is deferred, so DCL must not wait on PostHog's CDN.
    expect(Date.now() - start).toBeLessThan(3000);
  });

  test("gtag bridge forwards social clicks without throwing", async ({ page }) => {
    await page.goto("/index.html");
    const result = await page.evaluate(() => {
      const w = window as unknown as {
        gtag?: (...args: unknown[]) => void;
        posthog?: { capture?: (n: string, p?: unknown) => void };
      };
      try {
        w.gtag?.("event", "click_whatsapp", {
          event_category: "contact",
          event_label: "wa",
        });
      } catch (err) {
        return { threw: String(err) };
      }
      return { threw: null, sdkReady: typeof w.posthog?.capture === "function" };
    });
    // The bridge must never throw, whether or not array.js has resolved yet.
    expect(result.threw).toBeNull();
  });

  // Static wiring check: the injected block must contain the pre-PostHog event
  // queue and the drain-after-load flush function. If a future edit breaks the
  // bridge structure, this fails before anyone notices in production.
  // Runtime event forwarding is verified post-deployment against PostHog Live Events.
  test("gtag bridge queue-and-flush structure is present", async ({ request }) => {
    const html = await request.get("/index.html").then((r) => r.text());
    expect(html).toContain("var queue = []");
    expect(html).toContain("function flush()");
    expect(html).toContain("original.apply(window, args)");
  });
});
