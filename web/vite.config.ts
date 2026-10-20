/** Website build by Jason Stys. Variables: root/outDir are isolated web paths.
 * Functions: defineConfig declares a local-only, bundled, CDN-free build. Index: docs/CODE_INDEX.md.
 */
import { defineConfig } from "vite";
export default defineConfig({
  root: "web",
  base: "/",
  build: { outDir: "dist", emptyOutDir: true },
});
