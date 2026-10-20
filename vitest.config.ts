/** Unit-test routing by Jason Stys. Function: defineConfig. Variable: include isolates pure display tests.
 * Exact symbol line map: docs/CODE_INDEX.md. Browser integration tests run separately.
 */
import { defineConfig } from "vitest/config";
export default defineConfig({ test: { include: ["tests/display.test.ts"] } });
