import { test, expect } from "@playwright/test";

// A4 at 96dpi, and the scale the print stylesheet hard-codes
// (docs/lessons/poster-print.md — do not change without re-verifying page count).
const A4_HEIGHT_PX = 1123;
const PRINT_SCALE = 1.8898;

test.describe("poster-en.html — English flyer", () => {
  test("is declared as English with reciprocal hreflang", async ({ request }) => {
    const html = await request.get("/poster-en.html").then((r) => r.text());

    expect(html).toContain('<html lang="en">');
    expect(html).toContain(
      '<link rel="canonical" href="https://myo-makeyourown.pages.dev/poster-en.html">'
    );
    expect(html).toContain(
      '<link rel="alternate" hreflang="en" href="https://myo-makeyourown.pages.dev/poster-en.html">'
    );
    expect(html).toContain(
      '<link rel="alternate" hreflang="zh-HK" href="https://myo-makeyourown.pages.dev/poster.html">'
    );

    const zhHtml = await request.get("/poster.html").then((r) => r.text());
    expect(zhHtml).toContain(
      '<link rel="alternate" hreflang="en" href="https://myo-makeyourown.pages.dev/poster-en.html">'
    );
  });

  test("body copy is English, leaving only the language switch in Chinese", async ({
    page,
  }) => {
    await page.goto("/poster-en.html");

    const bodyText = await page.locator("body").innerText();
    const cjk = bodyText.match(/[一-鿿]/g) ?? [];
    expect(cjk).toEqual(["中", "文"]);

    await expect(page).toHaveTitle(
      "My O! Wedding Certificate Holder — Printable A5 Flyer"
    );
    await expect(page.locator(".brand-sub")).toHaveText(
      "Wedding Certificate Holder"
    );
  });

  test("English page ships no CJK webfonts", async ({ request }) => {
    const html = await request.get("/poster-en.html").then((r) => r.text());
    for (const family of ["Noto+Sans+TC", "Noto+Serif+TC", "Noto+Serif+HK", "LXGW+WenKai+TC"]) {
      expect(html).not.toContain(family);
    }
  });

  test("design artwork matches the Chinese flyer, including style 3", async ({
    request,
  }) => {
    const en = await request.get("/poster-en.html").then((r) => r.text());
    const zh = await request.get("/poster.html").then((r) => r.text());

    const artwork = (html: string) =>
      [...html.matchAll(/src="(image\/cert_[^"]+)"/g)].map((m) => m[1]);

    expect(artwork(en)).toEqual(artwork(zh));
  });

  test("language switcher cross-links both posters", async ({ page }) => {
    await page.goto("/poster-en.html");
    const zhLink = page.locator('.lang-switch a[hreflang="zh-HK"]');
    await expect(zhLink).toHaveAttribute("href", "poster.html");
    await expect(page.locator(".lang-switch .is-active")).toHaveText("EN");

    await page.goto("/poster.html");
    const enLink = page.locator('.lang-switch a[hreflang="en"]');
    await expect(enLink).toHaveAttribute("href", "poster-en.html");
    await expect(page.locator(".lang-switch .is-active")).toHaveText("中文");
  });

  test("QR codes stay on one row, not nested inside each other", async ({ page }) => {
    await page.goto("/poster-en.html");

    const items = page.locator(".qr-section > a.qr-link > .qr-item");
    await expect(items).toHaveCount(3);
    await expect(page.locator(".qr-item a.qr-link")).toHaveCount(0);

    const tops = await items.evaluateAll((els) =>
      els.map((el) => Math.round(el.getBoundingClientRect().top))
    );
    expect(new Set(tops).size).toBe(1);
  });

  test("highlight boxes do not wrap their titles", async ({ page }) => {
    await page.goto("/poster-en.html");

    const heights = await page
      .locator(".highlight-title")
      .evaluateAll((els) => els.map((el) => el.getBoundingClientRect().height));
    expect(heights.length).toBe(4);
    // The poster is transform-scaled on narrow viewports, so heights are
    // fractional; what matters is that no title spills to a second line.
    for (const h of heights) expect(Math.abs(h - heights[0])).toBeLessThan(1);
  });

  // The regression this page was built to avoid: English copy runs ~1.5-2x
  // longer than Chinese, which pushed the flyer past one A4 page and produced
  // a blank second sheet in the downloaded PDF.
  test("flyer still fits on a single A4 page when printed", async ({ page }) => {
    await page.goto("/poster-en.html");

    const height = await page
      .locator(".a5-flyer")
      .evaluate((el) => (el as HTMLElement).offsetHeight);

    expect(height * PRINT_SCALE).toBeLessThanOrEqual(A4_HEIGHT_PX);
  });

  test("print stylesheet pins the flyer to the page corner and hides chrome", async ({
    page,
  }) => {
    await page.goto("/poster-en.html");
    await page.emulateMedia({ media: "print" });

    const flyer = await page.locator(".a5-flyer").evaluate((el) => {
      const cs = getComputedStyle(el);
      return { position: cs.position, left: cs.left, transform: cs.transform };
    });
    expect(flyer.position).toBe("absolute");
    expect(flyer.left).toBe("0px");
    // Computed transform resolves scale() to matrix() notation.
    expect(flyer.transform).toMatch(
      new RegExp(`matrix\\(${PRINT_SCALE},\\s*0,\\s*0,\\s*${PRINT_SCALE},`)
    );

    await expect(page.locator("#downloadPdfBtn")).toBeHidden();
    await expect(page.locator(".lang-switch")).toBeHidden();
  });
});
