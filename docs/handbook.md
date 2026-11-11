# Orbital Safety Workbench handbook

By Jason Stys.

The released 1.1.0 portable workbench includes illustrative distance-window review: inspect exact sampled-history interval bounds, boundary censoring and replay positions while retaining archived ISS/SGP4 evidence and downloadable reports.

The released 1.1.0 portable workbench includes illustrative distance-window review: inspect exact sampled-history interval bounds, boundary censoring and replay positions while retaining archived ISS/SGP4 evidence and downloadable reports.

The existing civilian historical replay and fictional multi-object tracks remain the purpose. The actual extracted UI is checked against an analytic relative-distance oracle and exact JSON export, with collision probabilities explicitly absent. POSIX-safe archives and newly complete CPython/PyInstaller notices improve distribution without adding operational prediction or guidance.

## Read the documentation

The [illustrated Windows guide](reports/windows-application-guide.docx) adds actual
installed-app screenshots, a worked scenario, source excerpts and dated acceptance.
Its [review manifest](reports/windows-application-guide.json) identifies the exact
reviewed bytes. Earlier Office editions below retain their historical baselines.

| Edition                                                      | Audience and contents                                                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| [project-guide.docx](reports/project-guide.docx)             | User and developer guide: purpose, current usage, design, boundaries and source references.                        |
| [validation-review.docx](reports/validation-review.docx)     | Reviewer edition: exact tested baseline, observed workflows, dated local results and remaining limits.             |
| [validation-evidence.xlsx](reports/validation-evidence.xlsx) | Two filterable Excel Tables for observed workflows and test-source inventory, with recalculating outcome formulas. |

The editable Markdown remains the maintenance source. The Word files are readable editions. The workbook is an evidence index rather than a test runner. See [publication identities and review](reports/publications.json) and the [documentation refresh record](reports/documentation-refresh-2026-11-09.md).

## Current usage and help

[README quick start](../README.md) is the entry point. Use the project-specific guides below before changing inputs, operating modes or deployment assumptions.

### Usage and operations

- [RELEASE](RELEASE.md)
- [USER GUIDE](USER_GUIDE.md)
- [releases/v1.1.0](releases/v1.1.0.md)

### Design and contracts

- [ARCHITECTURE](ARCHITECTURE.md)

### Security and validation

- [SECURITY](SECURITY.md)
- [TESTING](TESTING.md)

## Historical results and reproduction

The reviewed source is [`89278b3a1997c3b4ab3f4b7acc81672a87a5f22e`](https://github.com/JasonStys/orbital-safety-workbench/tree/89278b3a1997c3b4ab3f4b7acc81672a87a5f22e). The observed functional workflow baseline is `89278b3a1997c3b4ab3f4b7acc81672a87a5f22e`; those observations are recorded at `2026-11-10T05:25:40.628667+00:00`. They do not certify an unrun later revision.

- [Detailed recorded validation](reports/PORTABLE_REFRESH_20261109.md)
- [Current Actions](https://github.com/JasonStys/orbital-safety-workbench/actions) records later integration checks separately.
- Preserve dated measurements and follow the existing testing guide to reproduce them; a test-source inventory alone does not establish execution.

## Practical boundaries

- Historical ISS data and fictional sampled tracks; no live catalog, covariance, collision probability, targeting or maneuver guidance.
- Distances are illustrative display thresholds rather than operational safety radii.
- Unsigned desktop portable folders, not system installers or clean-machine proof. Three-OS extracted-native checks drive an owned URL; default OS browser opening remains manual.

## Maintaining these editions

Update the editable usage/design/test documents first. Rebuild and visually review every Word page and workbook tab before replacing an edition; verify the exact binary digests and evidence source in publications.json. Keep account data, logs with secrets, installed-app state and private test stores out of documentation. Source and release assets retain their existing security and licensing boundaries.
