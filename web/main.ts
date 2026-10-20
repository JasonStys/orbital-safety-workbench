/** Read-only browser application by Jason Stys.
 * Functions: el, text, stop, updateCursor, plot, renderRun, load, animate.
 * Variables: run/scene/time/playing/generation are local view state, never operational commands.
 * Every definition and variable has exact lines in docs/CODE_INDEX.md.
 */
import { atTime, clock, fixed, magnitude, readBookmark, svgPath, writeBookmark } from "./display";
import { OrbitScene } from "./scene";
import type { Run } from "./types";

/** Require the static shell contract once, rather than propagate nullable elements. */
function el<T extends HTMLElement = HTMLElement>(id: string): T {
  const node = document.getElementById(id);
  if (!node) throw new Error(`Missing application element: ${id}`);
  return node as T;
}
/** All dynamic text uses textContent; no data is interpreted as executable HTML. */
function text(id: string, value: string): void {
  el(id).textContent = value;
}
const scenario = el<HTMLSelectElement>("scenario"),
  minutes = el<HTMLSelectElement>("minutes");
const object = el<HTMLSelectElement>("object"),
  slider = el<HTMLInputElement>("time");
let run: Run | undefined, scene: OrbitScene | undefined;
let time = 0,
  playing = false,
  generation = 0,
  request: AbortController | undefined,
  lastFrame = 0;
let animationFrame = 0;
const bookmark = readBookmark({ getItem: (key) => localStorage.getItem(key) });
scenario.value = bookmark.scenario;
minutes.value = String(bookmark.minutes);

/** Pause and cancel the sole animation callback, including hidden tabs and failed loads. */
function stop(): void {
  playing = false;
  cancelAnimationFrame(animationFrame);
  text("play", "▶ Play");
  el("play").setAttribute("aria-label", "Play replay");
}
/** Synchronize 3D markers, values and accessible time labels to a single bounded offset. */
function updateCursor(): void {
  if (!run) return;
  const track = run.tracks[Number(object.value)] ?? run.tracks[0]!;
  const sample = atTime(track, time);
  text("elapsed", clock(time));
  slider.value = String(Math.round(time));
  slider.setAttribute("aria-valuetext", `${clock(time)} elapsed`);
  text("speed", magnitude(sample.velocity).toFixed(3));
  text("height", (magnitude(sample.position) - run.earth_radius_km).toFixed(2));
  ["x", "y", "z"].forEach((key, i) => text(key, fixed(sample.position[i]!, 3)));
  scene?.update(time);
}
/** Render inline SVG from numeric coordinates only; no external image/chart dependencies. */
function plot(): void {
  if (!run) return;
  const projection = document.getElementById("projection")!;
  projection.replaceChildren();
  const ns = "http://www.w3.org/2000/svg";
  const circle = document.createElementNS(ns, "circle");
  circle.setAttribute("cx", "300");
  circle.setAttribute("cy", "140");
  circle.setAttribute("r", String(run.earth_radius_km / 60));
  circle.setAttribute("fill", "#d9e6e7");
  circle.setAttribute("stroke", "#6c8b95");
  projection.append(circle);
  run.tracks.forEach((track, i) => {
    const line = document.createElementNS(ns, "path");
    line.setAttribute(
      "d",
      track.samples
        .map(
          (s, n) =>
            `${n ? "L" : "M"}${(300 + s.position[0] / 60).toFixed(2)},${(140 - s.position[1] / 60).toFixed(2)}`,
        )
        .join(" "),
    );
    line.setAttribute("fill", "none");
    line.setAttribute("stroke", ["#087467", "#a34d00", "#6953a6"][i % 3]!);
    line.setAttribute("stroke-width", "2");
    projection.append(line);
  });
  const track = run.tracks[Number(object.value)] ?? run.tracks[0]!;
  const heights = track.samples.map((s) => magnitude(s.position) - run!.earth_radius_km);
  const min = Math.min(...heights),
    max = Math.max(...heights);
  const chart = document.getElementById("chart")!;
  const line = document.createElementNS(ns, "path");
  line.setAttribute("d", svgPath(heights, min, max));
  line.setAttribute("fill", "none");
  line.setAttribute("stroke", "#087467");
  line.setAttribute("stroke-width", "2");
  chart.replaceChildren(line);
  text(
    "chart-summary",
    `${track.name}: ${min.toFixed(2)}–${max.toFixed(2)} km radial height · 0–${run.horizon_minutes} minutes · ${track.samples.length} samples`,
  );
}
/** Install one complete run atomically, then dispose the previous scene's GPU resources. */
function renderRun(value: Run): void {
  stop();
  run = value;
  time = 0;
  object.replaceChildren(...run.tracks.map((track, i) => new Option(track.name, String(i))));
  slider.max = String(run.horizon_minutes * 60);
  text("duration", clock(run.horizon_minutes * 60));
  text(
    "scene-title",
    `${run.scenario === "iss-archive" ? "Archived ISS" : "Fictional histories"} / ${run.provenance.frame}`,
  );
  text(
    "scene-mode",
    run.scenario === "iss-archive"
      ? "HISTORICAL REPLAY / MAY 2024"
      : "SYNTHETIC / NOT REAL OBJECTS",
  );
  text("frame-note", `Frame: ${run.provenance.frame}. Reference sphere only; no ground track.`);
  const events = el("events");
  events.replaceChildren();
  if (!run.events.length)
    events.textContent = "One object: no pairwise screening. Collision probability unavailable.";
  for (const event of run.events) {
    const row = document.createElement("div");
    row.className = "event";
    const names = document.createElement("span"),
      distance = document.createElement("span");
    names.textContent = `${event.first} / ${event.second}`;
    distance.textContent = `${event.distance_km.toFixed(3)} km @ ${clock(event.time_s)}`;
    row.append(names, distance);
    events.append(row);
  }
  if (run.events.length) {
    const note = document.createElement("p");
    note.className = "fine";
    note.textContent =
      "Piecewise-linear minima, not collision probability. No covariance or object sizes.";
    events.append(note);
  }
  const provenance = el("provenance");
  provenance.replaceChildren();
  const entries = {
    "Epoch / UTC": run.provenance.epoch_utc,
    Frame: run.provenance.frame,
    Model: run.provenance.model,
    Source: run.provenance.source_description,
    "Source SHA-256": run.provenance.source_sha256,
    "Run SHA-256": run.id,
    "Units / sampling": `km · km/s · seconds / ${run.sample_interval_s}s samples`,
  };
  for (const [key, value] of Object.entries(entries)) {
    const dt = document.createElement("dt"),
      dd = document.createElement("dd");
    dt.textContent = key;
    dd.textContent = value;
    provenance.append(dt, dd);
  }
  el("limits").replaceChildren(
    ...run.limitations.map((limit) => {
      const li = document.createElement("li");
      li.textContent = limit;
      return li;
    }),
  );
  for (const format of ["json", "csv", "html"]) {
    const link = el<HTMLAnchorElement>(format);
    link.href = `/api/report?${new URLSearchParams({ scenario: run.scenario, minutes: String(run.horizon_minutes), format })}`;
  }
  scene?.dispose();
  scene = undefined;
  el("webgl-note").hidden = true;
  try {
    scene = new OrbitScene(el("scene"), run);
  } catch {
    el("webgl-note").hidden = false;
  }
  [object, slider, el<HTMLButtonElement>("play")].forEach((control) => {
    control.disabled = false;
  });
  plot();
  updateCursor();
}
/** Fetch a bounded scenario; abort superseded requests and never display stale run evidence. */
async function load(): Promise<void> {
  const version = ++generation;
  request?.abort();
  request = new AbortController();
  stop();
  el("error").hidden = true;
  text("status", "Loading reviewed scenario…");
  [object, slider, el<HTMLButtonElement>("play")].forEach((control) => {
    control.disabled = true;
  });
  el("json").setAttribute("aria-disabled", "true");
  try {
    const response = await fetch(
      `/api/run?${new URLSearchParams({ scenario: scenario.value, minutes: minutes.value })}`,
      { signal: request.signal },
    );
    if (!response.ok) throw new Error("Service unavailable");
    const value = (await response.json()) as Run;
    if (version !== generation) return;
    renderRun(value);
    const saved = writeBookmark(
      { setItem: (key, val) => localStorage.setItem(key, val) },
      { scenario: scenario.value, minutes: Number(minutes.value) },
    );
    text(
      "status",
      saved ? "Evidence ready · local only" : "Evidence ready · preferences not saved",
    );
  } catch {
    if (version !== generation) return;
    text("status", "Unable to load scenario");
    text(
      "error",
      "The local service could not load this scenario. Previous evidence may be visible; click Reload evidence to retry.",
    );
    el("error").hidden = false;
  } finally {
    if (version === generation) {
      scenario.disabled = false;
      minutes.disabled = false;
      el("json").removeAttribute("aria-disabled");
    }
  }
}
/** Advance at 60× elapsed time, capped on background jumps; no simulation computation in frames. */
function animate(now: number): void {
  if (!playing || !run) return;
  time = Math.min(run.horizon_minutes * 60, time + Math.min(0.1, (now - lastFrame) / 1000) * 60);
  lastFrame = now;
  updateCursor();
  if (time >= run.horizon_minutes * 60) stop();
  else animationFrame = requestAnimationFrame(animate);
}
scenario.addEventListener("change", () => {
  void load();
});
minutes.addEventListener("change", () => {
  void load();
});
el("reload").addEventListener("click", () => {
  void load();
});
object.addEventListener("change", () => {
  updateCursor();
  plot();
});
slider.addEventListener("input", () => {
  stop();
  time = Number(slider.value);
  updateCursor();
});
el("reset").addEventListener("click", () => scene?.reset());
el("play").addEventListener("click", () => {
  if (playing) stop();
  else if (run) {
    if (time >= run.horizon_minutes * 60) time = 0;
    playing = true;
    lastFrame = performance.now();
    text("play", "Ⅱ Pause");
    el("play").setAttribute("aria-label", "Pause replay");
    animationFrame = requestAnimationFrame(animate);
  }
});
document.addEventListener("visibilitychange", () => {
  if (document.hidden) stop();
});
window.addEventListener("pagehide", () => {
  stop();
  request?.abort();
  scene?.dispose();
});
void load();
