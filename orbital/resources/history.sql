-- Immutable local run evidence by Jason Stys. No identities, credentials or telemetry.
-- Variables: id SHA-256 primary key; scenario reviewed scenario ID; report_json full evidence.
-- Objects: runs table, immutable_report trigger. Exact line index: docs/CODE_INDEX.md.
CREATE TABLE IF NOT EXISTS runs (
    id TEXT PRIMARY KEY CHECK(length(id) = 64),
    scenario TEXT NOT NULL,
    report_json TEXT NOT NULL CHECK(json_valid(report_json)),
    saved_at_utc TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);
CREATE TRIGGER IF NOT EXISTS immutable_report
BEFORE UPDATE ON runs BEGIN
    SELECT RAISE(ABORT, 'Saved evidence is immutable');
END;
