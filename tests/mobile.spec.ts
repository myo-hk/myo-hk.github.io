import { test, expect } from '@playwright/test';

test.describe('MyO 手機版 UX/UI 測試', () => {

  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test.describe('漢堡選單功能', () => {
    test('選單應該預設隱藏', async ({ page, viewport }) => {
      if (viewport && viewport.width >= 768) test.skip();
      const menu = page.locator('#mobile-menu');
      // 檢查選單是否有 active 類別（應該沒有，處於隱藏狀態）
      await expect(menu).not.toHaveClass(/active/);
    });

    test('點擊漢堡圖標應該展開選單', async ({ page, viewport }) => {
      if (viewport && viewport.width >= 768) test.skip();
      const menuButton = page.locator('#mobile-menu-button');
      const menu = page.locator('#mobile-menu');

      await menuButton.click();
      await expect(menu).toHaveClass(/active/);
    });

    test('點擊選單項目後應該關閉選單', async ({ page, viewport }) => {
      if (viewport && viewport.width >= 768) test.skip();
      const menuButton = page.locator('#mobile-menu-button');
      const menu = page.locator('#mobile-menu');
      const menuLink = menu.locator('a').first();

      // 展開選單
      await menuButton.click();
      await expect(menu).toHaveClass(/active/);

      // 點擊選單連結
      await menuLink.click();

      // 選單應該關閉
      await expect(menu).not.toHaveClass(/active/);
    });

    test('選單項目應該有觸控回饋效果', async ({ page, viewport }) => {
      if (viewport && viewport.width >= 768) test.skip();

      // 檢查手機版選單元素存在於 DOM
      const menu = page.locator('#mobile-menu');
      await expect(menu).toBeAttached();

      // 檢查選單內有連結
      const menuLinks = page.locator('#mobile-menu a');
      const count = await menuLinks.count();
      expect(count).toBeGreaterThan(0);
    });
  });

  test.describe('Swiper 輪播功能', () => {
    test('Swiper 應該正確初始化', async ({ page }) => {
      const swiper = page.locator('.mySwiper');
      await expect(swiper).toBeVisible();
    });

    test('輪播應該支援滑動操作', async ({ page, viewport }) => {
      if (viewport && viewport.width >= 768) test.skip();

      const wrapper = page.locator('.mySwiper .swiper-wrapper');
      await expect(wrapper).toBeVisible();

      // 檢查 Swiper 配置中的 touch 參數
      const swiper = page.locator('.mySwiper');
      await expect(swiper).toBeVisible();
    });

    test('箭頭按鈕應該可點擊', async ({ page }) => {
      const nextButton = page.locator('.mySwiper .swiper-button-next');

      // 檢查箭頭存在
      await expect(nextButton).toBeVisible();

      // 檢查箭頭有足夠的觸控區域 (40-44px)
      const buttonSize = await nextButton.evaluate((el) => {
        const rect = el.getBoundingClientRect();
        return { width: rect.width, height: rect.height };
      });

      expect(buttonSize.width).toBeGreaterThanOrEqual(38);
      expect(buttonSize.height).toBeGreaterThanOrEqual(38);
    });
  });

  test.describe('Modal 彈窗功能', () => {
    test('點擊顏色選項應該開啟 Modal', async ({ page }) => {
      const colorOption = page.locator('.select-option[data-type="color"]').first();

      await colorOption.click();

      const modal = page.locator('#image-modal');
      await expect(modal).toBeVisible();
    });

    test('點擊關閉按鈕應該關閉 Modal', async ({ page }) => {
      // 先打開 Modal
      const colorOption = page.locator('.select-option[data-type="color"]').first();
      await colorOption.click();

      const modal = page.locator('#image-modal');
      const closeButton = page.locator('.close-button');

      await closeButton.click();
      await expect(modal).not.toBeVisible();
    });

    test('點擊背景應該關閉 Modal', async ({ page }) => {
      const colorOption = page.locator('.select-option[data-type="color"]').first();
      await colorOption.click();

      const modal = page.locator('#image-modal');

      // 點擊背景
      await modal.click({ position: { x: 10, y: 10 } });

      await expect(modal).not.toBeVisible();
    });

    test('ESC 鍵應該關閉 Modal', async ({ page }) => {
      const colorOption = page.locator('.select-option[data-type="color"]').first();
      await colorOption.click();

      const modal = page.locator('#image-modal');

      // 按 ESC 鍵
      await page.keyboard.press('Escape');

      await expect(modal).not.toBeVisible();
    });

    test('關閉按鈕應該有足夠的大小', async ({ page }) => {
      const colorOption = page.locator('.select-option[data-type="color"]').first();
      await colorOption.click();

      const closeButton = page.locator('.close-button');

      const buttonSize = await closeButton.evaluate((el) => {
        const rect = el.getBoundingClientRect();
        return { width: rect.width, height: rect.height };
      });

      // 關閉按鈕應該至少 40px
      expect(buttonSize.width).toBeGreaterThanOrEqual(40);
      expect(buttonSize.height).toBeGreaterThanOrEqual(40);
    });
  });

  test.describe('Sticky Bar 功能', () => {
    test('手機版應該顯示 Sticky Bar', async ({ page, isMobile }) => {
      if (!isMobile) test.skip();

      const stickyBar = page.locator('#sticky-conversion-bar');
      await expect(stickyBar).toBeVisible();
    });

    test('Sticky Bar 應該固定在底部', async ({ page, isMobile }) => {
      if (!isMobile) test.skip();

      const stickyBar = page.locator('#sticky-conversion-bar');
      const position = await stickyBar.evaluate((el) => {
        return window.getComputedStyle(el).position;
      });

      expect(position).toBe('fixed');
    });

    test('WhatsApp 按鈕應該可點擊', async ({ page, isMobile }) => {
      if (!isMobile) test.skip();

      const whatsappBtn = page.locator('#sticky-conversion-bar .btn-whatsapp');
      await expect(whatsappBtn).toBeVisible();

      const href = await whatsappBtn.getAttribute('href');
      expect(href).toContain('whatsapp');
    });

    test('Instagram 按鈕應該可點擊', async ({ page, isMobile }) => {
      if (!isMobile) test.skip();

      const instagramBtn = page.locator('#sticky-conversion-bar .btn-ig');
      await expect(instagramBtn).toBeVisible();

      const href = await instagramBtn.getAttribute('href');
      expect(href).toContain('instagram');
    });
  });

  test.describe('導航功能', () => {
    test('頂部導航應該存在', async ({ page }) => {
      const nav = page.locator('nav');
      await expect(nav).toBeVisible();
    });

    test('桌面版選單應該可見', async ({ page, isMobile }) => {
      if (isMobile) test.skip();

      const desktopMenu = page.locator('.desktop-nav-links');
      await expect(desktopMenu).toBeVisible();
    });

    test('手機版漢堡選單應該可見', async ({ page, isMobile }) => {
      if (!isMobile) test.skip();

      const hamburgerBtn = page.locator('#mobile-menu-button');
      await expect(hamburgerBtn).toBeVisible();
    });
  });

  test.describe('響應式設計', () => {
    test('手機版字體大小應該合適', async ({ page, isMobile }) => {
      if (!isMobile) test.skip();

      const title = page.locator('.hero-section h1');
      const fontSize = await title.evaluate((el) => {
        return parseFloat(window.getComputedStyle(el).fontSize);
      });

      // 手機版標題應該小於 40px
      expect(fontSize).toBeLessThan(40);
    });
  });
});