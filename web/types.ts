/** Shared scientific display contracts by Jason Stys.
 * Types: Sample, Track, Event, Run, Descriptor. Variables/fields: see docs/CODE_INDEX.md.
 * The service supplies bounded reviewed data, not user-controlled executable content.
 */
export interface Sample {
  t: number;
  position: [number, number, number];
  velocity: [number, number, number];
}
export interface Track {
  name: string;
  kind: "historical" | "synthetic";
  samples: Sample[];
}
export interface Event {
  first: string;
  second: string;
  distance_km: number;
  time_s: number;
  collision_probability: null;
  assessment: string;
  method: string;
}
export interface Run {
  id: string;
  scenario: string;
  horizon_minutes: number;
  earth_radius_km: number;
  sample_interval_s: number;
  provenance: {
    frame: string;
    epoch_utc: string;
    model: string;
    source: string;
    source_description: string;
    source_sha256: string;
    real_time: false;
  };
  limitations: string[];
  tracks: Track[];
  events: Event[];
}
export interface Descriptor {
  id: string;
  title: string;
  kind: string;
  summary: string;
}
