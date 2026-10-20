/** Pure bounded display utilities by Jason Stys.
 * Functions: atTime, magnitude, clock, svgPath, readBookmark, writeBookmark.
 * Variables: Bookmark is a reviewed scenario/horizon pair; exact line map: docs/CODE_INDEX.md.
 */
import type { Sample, Track } from "./types";
export interface Bookmark {
  scenario: string;
  minutes: number;
}

/** Interpolate a reviewed history for display only; inputs outside coverage are errors. */
export function atTime(track: Track, time: number): Sample {
  const first = track.samples[0],
    last = track.samples.at(-1);
  if (!first || !last || !Number.isFinite(time) || time < first.t || time > last.t)
    throw new Error("Time outside track");
  const rightIndex = Math.min(
    track.samples.length - 1,
    Math.max(
      1,
      track.samples.findIndex((s) => s.t >= time),
    ),
  );
  const left = track.samples[rightIndex - 1]!,
    right = track.samples[rightIndex]!;
  const f = (time - left.t) / (right.t - left.t);
  const mix = (a: number[], b: number[]): [number, number, number] =>
    [0, 1, 2].map((i) => a[i]! + f * (b[i]! - a[i]!)) as [number, number, number];
  return {
    t: time,
    position: mix(left.position, right.position),
    velocity: mix(left.velocity, right.velocity),
  };
}
/** Euclidean norm; source quantities retain km or km/s, never guessed units. */
export function magnitude(vector: number[]): number {
  return Math.hypot(...vector);
}
/** Normalize display-only negative zero after rounding; evidence retains original precision. */
export function fixed(value: number, digits: number): string {
  const rounded = value.toFixed(digits);
  return /^-0(?:\.0+)?$/.test(rounded) ? rounded.slice(1) : rounded;
}
/** Format an elapsed offset, not UTC or local civil time. */
export function clock(seconds: number): string {
  return `${Math.floor(seconds / 60)
    .toString()
    .padStart(2, "0")}:${Math.floor(seconds % 60)
    .toString()
    .padStart(2, "0")}`;
}
/** SVG line points in a fixed viewport; a constant series still has a finite scale. */
export function svgPath(values: number[], min: number, max: number): string {
  return values
    .map(
      (v, i) =>
        `${i ? "L" : "M"}${((i * 600) / Math.max(1, values.length - 1)).toFixed(2)},${(110 - ((v - min) / Math.max(0.001, max - min)) * 100).toFixed(2)}`,
    )
    .join(" ");
}
/** Load only finite reviewed settings; private data and histories never enter browser storage. */
export function readBookmark(storage: Pick<Storage, "getItem">): Bookmark {
  try {
    const value: unknown = JSON.parse(storage.getItem("orbital-view-v1") ?? "null");
    if (
      typeof value === "object" &&
      value !== null &&
      "scenario" in value &&
      "minutes" in value &&
      ["iss-archive", "synthetic-crossing", "synthetic-separated"].includes(
        String(value.scenario),
      ) &&
      [30, 60, 120].includes(Number(value.minutes))
    )
      return { scenario: String(value.scenario), minutes: Number(value.minutes) };
  } catch {
    /* Storage denied or corrupt: use reviewed defaults, no app failure. */
  }
  return { scenario: "iss-archive", minutes: 60 };
}
/** A blocked or full localStorage is non-fatal; return a status the UI can explain. */
export function writeBookmark(storage: Pick<Storage, "setItem">, bookmark: Bookmark): boolean {
  try {
    storage.setItem("orbital-view-v1", JSON.stringify(bookmark));
    return true;
  } catch {
    return false;
  }
}
