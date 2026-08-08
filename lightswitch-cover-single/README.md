# Lightswitch Cover Single (Jumbo)

A jumbo/oversized single-gang toggle switch wall plate, corrected from an existing rough draft
design and validated through a full spec → build → test → review pipeline. Companion project to
[`../switch-plate-covers/`](../switch-plate-covers/) (double-gang and Decora-style plates).

Source Fusion file: `Lightswitch-Cover-Single.f3d` (in the user's Fusion project, not stored in
this repo). This folder holds the exported, print-ready geometry; the full design record —
spec, revision history, independent test report, and final review — lives in
[`../dot_pipeline/`](../dot_pipeline/).

## What this is

The starting point was an existing Fusion model with reasonable design instincts (a real
conical countersink, a shelled/hollow back with reinforcing bosses at the screw holes, rounded
outer edges) but several unverified dimensions — rounded to convenient metric numbers instead of
derived from the real inch-based electrical standard. Two things were wrong badly enough to
matter:

1. **Overall size and screw spacing** were off from the true jumbo single-gang standard and the
   real NEMA toggle-switch strap spacing.
2. **The screw hole channel**, once corrected, was initially rebuilt as a ~4mm bore through a
   solid boss column — found during testing to be too tight/long for real installation. Tracing
   through exactly how the original reference model's screw holes actually work (a short guide
   channel opening into an already-hollow interior, not a full-depth precision bore) fixed it.

Both fixes, and the reasoning behind them, are recorded in [`../dot_pipeline/specs.md`](../dot_pipeline/specs.md).

## Folder contents

```
lightswitch-cover-single/
├── README.md          this file
├── parameters.md        condensed dimension reference — see ../dot_pipeline/ for full detail
├── step/                 *.step  — parametric CAD exchange
├── 3mf/                  *.3mf   — mesh + print metadata, preferred for modern slicers
└── stl/                  *.stl   — mesh, universal slicer fallback
```

Both bodies are exported centered at the origin with the bottom face at Z=0, thin (5mm)
dimension vertical — print-bed-ready, same convention as `switch-plate-covers/`.

## Files

| File base name | Description |
|---|---|
| `lightswitch-cover-single-jumbo` | Functional, corrected jumbo single-gang plate |
| `lightswitch-cover-single-jumbo-tapered-edge` | Same, with a 1.5mm rounded outer edge (cosmetic) |

The original reference design (`Body1` in the Fusion file) is not exported — it's kept in the
Fusion document only as an unmodified comparison reference.

## Pipeline record

This design went through the full spec → build → test → review process:

1. **[Spec](../dot_pipeline/specs.md)** — every dimension tagged VERIFIED with its source
   (retail listings, this project's established NEMA-based standards, or direct measurement of
   the reference geometry), plus a revision history explaining every correction made and why.
2. **Build** — corrected the flat dimensions first, then discovered and fixed the screw-hole
   channel bug through direct geometry comparison against the reference design.
3. **[Test](../dot_pipeline/tests.md)** — independent re-measurement of the live geometry
   (not a re-read of the build report): confirmed the screw path is genuinely open front-to-back,
   wall thickness clears nozzle minimums with large margin, and the design clears a real switch
   yoke by 20+mm on every axis.
4. **[Review](../dot_pipeline/review.md)** — final approval, including an independent spot-check
   of the Tester's numbers and one documentation-only error caught and corrected (a mislabeled
   dimension in the spec — didn't affect the exported geometry).

## Printing notes

- **Material: PETG**, not PLA — thin walls and screw bosses see repeated mechanical stress from
  screw insertion/removal, and PETG holds up better than PLA's brittleness here.
- Print flat, back face down, thin dimension vertical.
- No supports expected. The boss collars are a small (~9mm) unsupported bridge inside the hollow
  cavity — check the first layer of that feature on your first test print.

## Known limitations

- The boss collar diameter (9mm) and the tapered-edge fillet radius (1.5mm) are project design
  choices, not verified real-world specs — store-bought plates don't have a separate reinforcing
  boss at all (they're solid molded plastic), and the reference design's exact edge geometry was
  ambiguous enough that it wasn't worth exactly reverse-engineering.
- This Fusion document's native axis convention differs from `switch-plate-covers/` (thickness
  along Y, not Z) — the exports were rotated to match the project-wide print convention, so raw
  coordinates in the STEP/STL/3MF files won't match the live Fusion model directly.
