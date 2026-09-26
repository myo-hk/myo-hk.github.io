import { test, expect } from "@playwright/test";

const GA4_ID = "G-GQLW7LNP6H";

const PAGES = [
  { path: "/index.html", name: "home" },
  { path: "/faq.html", name: "faq" },
  { path: "/blog/index.html", name: "blog index" },
  { path: "/blog/婚禮攝影對焦技巧.html", name: "blog article (CJK filename)" },
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
        if (/Content Security Policy|Refused to/i.test(text)) {
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
});
