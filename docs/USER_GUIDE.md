# Using the workbench

## Start

For a published portable ZIP, verify its SHA-256 against the matching `.sha256` release file, extract the **entire folder**, and launch `OrbitalSafetyWorkbench` (Windows: `.exe`). It opens your default browser at an available `http://127.0.0.1:<port>/` address. Keep the console open; Ctrl+C closes the server. No elevated permissions are needed. A ZIP checksum detects corruption relative to its published manifest; it is not a code-signing signature. Bundles are unsigned/unnotarized: do not bypass OS warnings. Source setup in the README is the alternative.

Platform builds run on the platform/architecture listed in the ZIP name. Do not assume a Windows executable works on Linux, or that a macOS ARM build works on Intel. Mobile layouts are tested at 390 CSS pixels, but there is no mobile-native package or LAN server. A local application is not a hosted Internet service.

## Explore

1. Select historical ISS or a clearly labeled synthetic case, then a 30/60/120-minute window.
2. Drag/scroll the reference-sphere view with a pointer; **Reset camera** restores the view. If WebGL is unavailable, use the XY projection, numeric readout and chart. These do not depend on WebGL.
3. Select an object. Use the time slider (keyboard arrows work) or Play/Pause. Playback is 60 replay seconds per real second; it pauses in hidden tabs and stops at the final timestamp. Reduced-motion users can use the slider without starting playback.
4. Inspect positions (km), speed magnitude (km/s), radial height and pairwise minimum distances. All time offsets are elapsed seconds/minutes from the displayed historical/synthetic epoch, not today's time.
5. Review evidence and limitations, then download JSON/CSV/HTML. JSON and HTML contain the complete scientific record; CSV contains all object samples with unit labels and the run ID. CSV does not contain every prose limitation: keep JSON/HTML alongside it.

One object yields no pairwise event. A very small fictional separation does not mean real collision probability. Without covariance and physical sizes the probability is unavailable, not zero.

## Privacy and storage

Only your scenario/window preference is saved in localStorage. No identities, passwords, browser history, analytics or remote data requests are collected. Report downloads go to your browser's chosen download folder. Optional CLI SQLite histories stay at the path you choose, outside Git by default (`*.sqlite3*` is ignored). Protect exported data through your OS account and disk encryption as appropriate. Built-in data is public historical or fictional.

## Troubleshooting

- **Missing website build:** run `npm ci` and `npm run build`, or use a complete release bundle. Do not remove a bundle's `_internal` folder.
- **Unable to load:** keep the server console running, confirm the printed URL uses `127.0.0.1` (not localhost), then Reload evidence. Previous evidence is explicitly labeled when loading fails.
- **3D unavailable:** try a supported current browser with WebGL enabled; the projection and numeric readout remain available. No OS protection must be disabled.
- **Preferences not saved:** private/blocked storage is fine; the app uses defaults and continues without persistence.
- **Export exists:** use a new filename; the CLI refuses silent overwrites.
- **History full:** choose a new history database; no automatic deletion happens.

Help/contact: [Jason Stys on GitHub](https://github.com/JasonStys) and [project issues](https://github.com/JasonStys/orbital-safety-workbench/issues). Include software version, OS/browser and a synthetic reproducible scenario, not private files or credentials.
