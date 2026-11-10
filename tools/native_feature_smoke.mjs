/** Jason Stys — actual extracted civilian distance-window review and downloaded evidence.
 * Functions: owned journey; variables: analytic synthetic relative-z oracle and censored windows.
 * Source lines: docs/CODE_INDEX.md. Display thresholds are illustrative, never safety radii or targeting.
 */
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { expect } from "@playwright/test";
import { runNativeJourney } from "./native_browser.mjs";

await runNativeJourney(async ({ page, request, outputDirectory, version }) => {
  await expect(page.getByRole("status")).toContainText("Evidence ready");
  await page.locator("#scenario").selectOption("synthetic-crossing");
  await page.getByRole("combobox", { name: "REPLAY WINDOW", exact: true }).selectOption("30");
  await expect(page.locator("#scene-title")).toContainText("Fictional");
  await expect(page.locator("#time")).toHaveAttribute("max", "1800");
  const run = await (await request.get("api/run?scenario=synthetic-crossing&minutes=30")).json();
  assert.equal(run.software_version, version);
  assert.equal(run.screening_windows.length, 9);
  const pair = (radius) =>
    run.screening_windows.find(
      (row) => row.first === "Demo A" && row.second === "Demo B" && row.threshold_km === radius,
    );
  // Relative z is0.008*(t-907)km, independently giving907±125s at1km.
  const narrow = pair(1).windows[0];
  assert.ok(Math.abs(narrow.start_s - 782) < 1e-8 && Math.abs(narrow.end_s - 1032) < 1e-8);
  assert.equal(narrow.duration_s, 250);
  assert.deepEqual([narrow.start_censored, narrow.end_censored], [false, false]);
  assert.deepEqual(pair(10).windows[0], {
    start_s: 0,
    end_s: 1800,
    duration_s: 1800,
    start_censored: true,
    end_censored: true,
  });
  assert.ok(run.events.every((event) => event.collision_probability === null));
  await page.locator("#screening-windows summary").click();
  await expect(page.locator("#screening-windows")).toContainText("not safety radii");
  await page.locator("#screening-windows button").first().click();
  await expect(page.locator("#time")).not.toHaveValue("0");
  const pending = page.waitForEvent("download");
  await page.getByRole("link", { name: "JSON ↓", exact: true }).click();
  const download = await pending;
  const file = path.join(outputDirectory, "native-distance-windows.json");
  await download.saveAs(file);
  assert.deepEqual(JSON.parse(await readFile(file, "utf8")), run);
  assert.equal((await request.get("api/run?minutes=0")).status(), 400);
  const historical = await (await request.get("api/run?scenario=iss-archive&minutes=30")).json();
  assert.deepEqual(historical.screening_windows, []);
  assert.equal(historical.provenance.frame, "TEME");
});
