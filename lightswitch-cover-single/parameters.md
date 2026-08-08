# Parameter Sheet — Lightswitch Cover Single (Jumbo)

Full pipeline record for this revision lives in [`../dot_pipeline/`](../dot_pipeline/):
[`specs.md`](../dot_pipeline/specs.md) (spec + revision history), [`tests.md`](../dot_pipeline/tests.md)
(independent QA pass), [`verdict.md`](../dot_pipeline/verdict.md) (Tester sign-off), [`review.md`](../dot_pipeline/review.md)
(final Reviewer approval). This file is the condensed reference; the pipeline docs have the full
reasoning and measurement methodology.

All dimensions in mm unless noted (this document's Fusion file uses mm as its native unit,
unlike the inch-based `switch-plate-covers/` project). Companion reference:
[`../switch-plate-covers/parameters.md`](../switch-plate-covers/parameters.md) — same NEMA-based
reasoning applied here.

## Overall plate

| Parameter | Value | Source |
|---|---|---|
| Overall width | 88.9mm (3.5") | VERIFIED — retail (jumbo single-gang standard, multiple independent listings) |
| Overall height | 139.7mm (5.5") | VERIFIED — retail |
| Overall thickness | 5mm | VERIFIED — geometry (from original reference design) |
| Outer corner fillet radius | ~2.35mm | VERIFIED — geometry |

This is an intentionally oversized/jumbo single-gang plate — bigger than the standard 69.85×114.3mm
single-gang plate documented in `switch-plate-covers/parameters.md`.

## Toggle opening

| Parameter | Value | Source |
|---|---|---|
| Opening size | 10.32mm × 23.81mm (0.40625" × 0.9375") | VERIFIED — matches the standard toggle opening used project-wide |
| Opening corner radius | 1.59mm (1/16") | VERIFIED — same standard used on the double-gang plate |

## Mounting screws

| Parameter | Value | Source |
|---|---|---|
| Screw spacing (vertical) | 60.325mm (2.375") | VERIFIED — NEMA toggle-switch strap standard |
| Screw shank diameter | 4.7625mm (3/16") | VERIFIED — Kyle Switch Plates retail spec |
| Countersink top diameter | 7.9375mm (5/16") | VERIFIED — Kyle Switch Plates retail spec |
| Countersink angle | 90° included (45° half-angle) | VERIFIED — geometry, genuine cone |
| Total guide-channel depth | 1.9mm | VERIFIED — geometry, independently tested |

**Why the channel is short, not full-depth:** the screw only needs a precise-diameter guide
channel near the front; the interior is fully hollow behind it, so the screw's remaining travel
to reach the switch is through open space, not a long tight bore. A first build mistakenly made
this a full ~4mm bore through a solid boss column — flagged during testing as too tight for real
installation and rebuilt. See revision history in `../dot_pipeline/specs.md` §4 for the full story.

## Back construction — open cavity with boss collars

| Parameter | Value | Source |
|---|---|---|
| Front skin / cavity ceiling thickness | 1.65mm | VERIFIED — geometry, matches the original reference design exactly |
| Relief depth | 3.35mm | VERIFIED — geometry |
| Rim inset from outer edge | 1.65mm | VERIFIED — geometry |
| Relief cavity footprint | 85.6mm × 136.4mm | VERIFIED — geometry, tested |
| Boss collar diameter | 9mm | Project design choice — not a retail spec, store-bought plates have no boss |
| Boss collar depth below ceiling | 0.25mm | VERIFIED — geometry |

Unlike a simple solid-floored pocket, this is a genuinely open cavity — nearly the entire
interior (minus a thin 1.65mm rim and skin) is hollow front-to-back, with short boss "collars"
hanging from the front skin at each screw location for reinforcement.

## Cosmetic variant

`lightswitch-cover-single-jumbo-tapered-edge` is identical to the base jumbo body except for a
**1.5mm-radius edge fillet** on the front and back outer perimeter edges, approximating the
rounded/tapered look of the original reference design. Confirmed via feature diff during testing
to differ *only* by this fillet.

## Material and print orientation

- **Material: PETG** (not PLA) — the 1.65mm skin and screw collars see repeated mechanical stress
  from screw insertion/removal; PETG's ductility holds up better than PLA's brittleness here,
  consistent with the rest of this project's recommendations.
- **Orientation:** print flat, back face down, 5mm thickness vertical — matches every export in
  this project. No supports expected; the boss collars are a small (~9mm) unsupported bridge
  inside the hollow cavity — worth checking the first layer of that feature on the first print.

## Fit verification

Tested against a real single-pole toggle switch yoke (44.45mm × 74.625mm, per
`switch-plate-covers/parameters.md`): margin of 20.6mm and 30.9mm per side on the two axes —
large clearance, no interference risk.

## Files

| File base name | Body |
|---|---|
| `lightswitch-cover-single-jumbo` | Functional, corrected jumbo plate |
| `lightswitch-cover-single-jumbo-tapered-edge` | Same, with rounded outer edges |

Exported centered at the origin with the bottom face at Z=0, thin (5mm) dimension vertical —
print-bed-ready, same convention as `switch-plate-covers/`. Note: this Fusion document's native
axis convention has thickness along Y (not Z); the exports were rotated during export to match
the project-wide Z-up convention, so the STEP/3MF/STL files do not share raw coordinates with the
live Fusion model — check `../dot_pipeline/specs.md` if working from the Fusion file directly.
