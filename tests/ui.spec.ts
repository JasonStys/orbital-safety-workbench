/** End-user production-server tests by Jason Stys.
 * Functions: test callbacks exercise scenarios, scrub/play, exports, errors, accessibility and mobile.
 * Variables: browser/page, expected evidence, downloaded files. Exact lines: docs/CODE_INDEX.md.
 */
import { expect, test } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { readFile } from "node:fs/promises";

test("no-WebGL fallback preserves scientific evidence without external requests", async ({
  page,
}) => {
  const foreign: string[] = [];
  page.on("request", (request) => {
    if (!request.url().startsWith("http://127.0.0.1:") && !request.url().startsWith("data:"))
      foreign.push(request.url());
  });
  await page.addInitScript(() => {
    const original = HTMLCanvasElement.prototype.getContext;
    Object.defineProperty(HTMLCanvasElement.prototype, "getContext", {
      value: function (this: HTMLCanvasElement, id: string, ...args: unknown[]) {
        return id.includes("webgl") ? null : Reflect.apply(original, this, [id, ...args]);
      },
    });
  });
  await page.goto("/");
  await expect(page.getByRole("status")).toContainText("Evidence ready");
  await expect(page.locator("#webgl-note")).toBeVisible();
  await expect(page.locator("#projection path")).toHaveCount(1);
  await expect(page.locator("#speed")).toHaveText(/7\.\d{3}/);
  expect(foreign).toEqual([]);
});

test("replay controls, multi-object screening and real export", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("status")).toContainText("Evidence ready");
  await expect(page.locator("#speed")).toHaveText(/7\.\d{3}/);
  await page
    .getByRole("combobox", { name: "SCENARIO", exact: true })
    .selectOption("synthetic-crossing");
  await expect(page.locator("#scene-title")).toContainText("Fictional");
  await expect(page.locator("#events")).toContainText("0.000 km @ 15:07");
  await page.getByRole("combobox", { name: "REPLAY WINDOW", exact: true }).selectOption("120");
  await expect(page.getByRole("status")).toContainText("Evidence ready");
  await expect(page.locator("#time")).toHaveAttribute("max", "7200");
  await page.getByLabel("Selected object", { exact: true }).selectOption("1");
  await page.getByLabel("Elapsed replay seconds").fill("907");
  await expect(page.locator("#elapsed")).toHaveText("15:07");
  await expect(page.locator("#z")).toHaveText("0.000");
  await page.getByRole("button", { name: "Play replay", exact: true }).click();
  await expect(page.getByRole("button", { name: "Pause replay", exact: true })).toBeVisible();
  await expect(page.locator("#elapsed")).not.toHaveText("15:07");
  await page.getByRole("button", { name: "Pause replay", exact: true }).click();
  await page.getByRole("button", { name: "Reset camera" }).click();
  const downloadPromise = page.waitForEvent("download");
  await page.getByRole("link", { name: "JSON ↓", exact: true }).click();
  const download = await downloadPromise;
  const report = JSON.parse(await readFile((await download.path())!, "utf8"));
  expect(report.scenario).toBe("synthetic-crossing");
  expect(report.horizon_minutes).toBe(120);
  expect(report.events[0].collision_probability).toBeNull();
  expect(report.tracks[0].samples).toHaveLength(721);
  expect(report.id).toMatch(/^[a-f0-9]{64}$/);
  await page.reload();
  await expect(page.locator("#scenario")).toHaveValue("synthetic-crossing");
  await expect(page.locator("#minutes")).toHaveValue("120");
});

test("service errors are visible and retry recovers", async ({ page }) => {
  await page.route("**/api/run?**", (route) => route.fulfill({ status: 500, body: "unavailable" }));
  await page.goto("/");
  await expect(page.getByRole("alert")).toContainText("could not load");
  await expect(page.getByRole("button", { name: "Play replay", exact: true })).toBeDisabled();
  await page.unroute("**/api/run?**");
  await page.getByRole("button", { name: "Reload evidence" }).click();
  await expect(page.getByRole("status")).toContainText("Evidence ready");
  await expect(page.getByRole("alert")).toBeHidden();
});

test("superseded results cannot replace the current selection", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("status")).toContainText("Evidence ready");
  await page.route("**/api/run?scenario=synthetic-crossing&**", async (route) => {
    await new Promise((resolve) => setTimeout(resolve, 300));
    try {
      await route.continue();
    } catch {
      /* Aborted superseded request is expected. */
    }
  });
  await page.locator("#scenario").selectOption("synthetic-crossing");
  await page.locator("#scenario").selectOption("synthetic-separated");
  await expect(page.getByRole("status")).toContainText("Evidence ready");
  await expect(page.locator("#events")).toContainText("242.744 km");
  await expect(page.locator("#json")).toHaveAttribute("href", /synthetic-separated/);
});

test("accessible desktop and narrow mobile have no serious issues or overflow", async ({
  page,
}) => {
  await page.goto("/");
  await expect(page.getByRole("status")).toContainText("Evidence ready");
  const desktop = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
    .analyze();
  expect(desktop.violations).toEqual([]);
  await page.setViewportSize({ width: 390, height: 844 });
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  await page
    .getByRole("combobox", { name: "SCENARIO", exact: true })
    .selectOption("synthetic-separated");
  await expect(page.getByRole("status")).toContainText("Evidence ready");
  const mobile = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
    .analyze();
  expect(mobile.violations).toEqual([]);
  await page.getByRole("link", { name: "How it works" }).click();
  await expect(page.locator("#help")).toBeInViewport();
});

test("blocked preferences do not prevent scientific use", async ({ page }) => {
  await page.addInitScript(() => {
    Object.defineProperty(window, "localStorage", {
      get() {
        throw new Error("denied");
      },
    });
  });
  await page.goto("/");
  await expect(page.getByRole("status")).toContainText("preferences not saved");
  await expect(page.locator("#speed")).toHaveText(/7\.\d{3}/);
});
