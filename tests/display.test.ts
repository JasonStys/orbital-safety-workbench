/** Pure display contract tests by Jason Stys.
 * Functions: test callbacks exercise interpolation, finite charts and denied/corrupt preferences.
 * Variables: track, storage doubles. Exact lines: docs/CODE_INDEX.md.
 */
import { describe, expect, test } from "vitest";
import {
  atTime,
  clock,
  fixed,
  magnitude,
  readBookmark,
  svgPath,
  writeBookmark,
} from "../web/display";
import type { Track } from "../web/types";
const track: Track = {
  name: "A",
  kind: "synthetic",
  samples: [
    { t: 0, position: [0, 0, 0], velocity: [0, 0, 0] },
    { t: 10, position: [10, 20, 30], velocity: [2, 4, 6] },
  ],
};
describe("bounded display", () => {
  test.each([0, 5, 10])("interpolates at %s", (time) => {
    expect(atTime(track, time).position).toEqual([time, time * 2, time * 3]);
    expect(atTime(track, time).velocity[0]).toBe(time / 5);
  });
  test.each([-1, 11, NaN, Infinity])("rejects outside time %s", (time) => {
    expect(() => atTime(track, time)).toThrow();
  });
  test("rejects missing history", () =>
    expect(() => atTime({ ...track, samples: [] }, 0)).toThrow());
  test("formats quantities without changing units", () => {
    expect(fixed(-1e-16, 3)).toBe("0.000");
    expect(fixed(-1.234, 3)).toBe("-1.234");
    expect(magnitude([3, 4, 0])).toBe(5);
    expect(clock(7200)).toBe("120:00");
    expect(clock(907)).toBe("15:07");
    expect(svgPath([4, 4], 4, 4)).not.toMatch(/NaN|Infinity/);
    expect(svgPath([], 0, 0)).toBe("");
  });
});
describe("public preferences only", () => {
  test.each([
    null,
    "not-json",
    "{}",
    '{"scenario":"evil","minutes":60}',
    '{"scenario":"iss-archive","minutes":999}',
  ])("defaults on %s", (value) => {
    expect(readBookmark({ getItem: () => value })).toEqual({
      scenario: "iss-archive",
      minutes: 60,
    });
  });
  test("handles blocked storage", () => {
    expect(
      readBookmark({
        getItem: () => {
          throw new Error("denied");
        },
      }).scenario,
    ).toBe("iss-archive");
    expect(
      writeBookmark(
        {
          setItem: () => {
            throw new Error("full");
          },
        },
        { scenario: "iss-archive", minutes: 60 },
      ),
    ).toBe(false);
  });
  test("round trips reviewed settings", () => {
    let data = "";
    expect(
      writeBookmark(
        {
          setItem: (_, value) => {
            data = value;
          },
        },
        { scenario: "synthetic-crossing", minutes: 120 },
      ),
    ).toBe(true);
    expect(readBookmark({ getItem: () => data })).toEqual({
      scenario: "synthetic-crossing",
      minutes: 120,
    });
  });
});
