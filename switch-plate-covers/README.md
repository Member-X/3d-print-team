# Switch Plate Covers

Parametric, 3D-printable wall plate covers modeled in Fusion 360 from standard US electrical
wall-plate dimensions: a **double-gang toggle switch plate** and a **single-gang Decora-style
plate** (the same opening used for rocker switches, GFCI outlets, dimmers, and jacks).

Source Fusion file: `Double Gang Switch Plate.f3d` (in the user's Fusion project — not stored
in this repo). This folder holds the exported, print-ready geometry plus the design record.

## Why this isn't just a flat rectangle with holes cut in it

A wall switch/outlet's mounting yoke, its screws, and the toggle/rocker mechanism all sit
slightly proud of the finished wall surface — electrical boxes are commonly recessed a bit and
the device is leveled forward until the yoke clears the wall. A uniformly flat cover plate
would contact that raised hardware in the middle first and rock or gap around its outer edges
instead of sitting flush. Real wall plates solve this two ways, both replicated here:

1. **Back relief pocket** (double-gang plate only) — a shallow pocket recessed into the back
   around each toggle opening, sized to clear the yoke, its mounting screws, and the toggle
   mechanism, so only the plate's outer rim actually touches the wall.
2. **Front screw counterbore** — a shallow recess around each mounting-screw hole so the screw
   head sits flush with the visible face instead of standing proud.

## Folder contents

```
switch-plate-covers/
├── README.md          this file
├── parameters.md       full dimension table + design rationale for every parameter
├── step/                *.step  — parametric CAD exchange, for re-editing in any CAD tool
├── 3mf/                 *.3mf   — mesh + print metadata, preferred for modern slicers
└── stl/                 *.stl   — mesh, universal slicer fallback
```

Every body is exported individually in all three formats, **centered at the origin with its
bottom face at Z=0** (print-bed-ready orientation — thin dimension vertical, large face down).

> **Exports are currently stale.** The project owner reduced the front-edge fillet from 3.75mm
> to 1.5mm on two of the shelled bodies and added a new 1.5mm fillet to the flat Decora body
> after these files were generated (see below). The files in `step/`, `3mf/`, `stl/` do not yet
> reflect that change — re-export before using them.

## Bodies

| File base name | Description |
|---|---|
| `double-gang-toggle-plate` | Flat double-gang toggle plate, no shell/fillet |
| `double-gang-toggle-plate-shelled` | Same, with a cosmetic 1mm back shell + **1.5mm front fillet** (reduced from 3.75mm) |
| `decora-single-gang-plate` | Flat single-gang Decora/GFCI-style plate, correct screw holes, **1.5mm front fillet** (newly added) |
| `decora-single-gang-plate-shelled` | Same, with 1mm back shell + **1.5mm front fillet** (reduced from 3.75mm) |
| `decora-single-gang-plate-shelled-original-no-holes` | Superseded early draft, kept for reference — still carries the original 3.75mm fillet, untouched — see Known Issues |

Full dimensions for every feature (opening size, screw spacing, corner radii, pocket/shell/fillet
values) are in [`parameters.md`](parameters.md), including the fillet revision history.

## Design sources

- Overall plate dimensions, toggle opening size, gang spacing, and 2.375" toggle screw
  spacing: [Kyle Switch Plates size reference](https://www.kyleswitchplates.com/switch-plate-size-reference-information/),
  [wallplate.store size guide](https://wallplate.store/pages/toggle-switch-wall-plate-size-reference-guide)
- Decora/GFCI opening size (1.3125" × 2.625"): same sources, cross-checked against multiple
  Decora product listings
- Decora/GFCI **screw spacing (3.28")**: corrected from a ruler-photo measurement of an
  installed GFCI outlet plate (screws visibly outboard of the opening), confirmed against the
  NEMA WD1 duplex-receptacle mounting strap standard — see "Known issues" below for why the
  first attempt was wrong
- Relief pocket / counterbore concept: general wall-plate mounting-hardware knowledge (yoke and
  screw heads standing proud of the wall)

## Known issues / caveats

- **Relief pocket size is a generic estimate**, not measured from a specific switch or
  electrical box. If your box depth or device yoke differs meaningfully, check clearance before
  printing a batch.
- **`decora-single-gang-plate-shelled-original-no-holes`** was built before the screw-spacing
  correction and never got screw holes — cutting holes into it afterward split the body into two
  disconnected solids because its shell wall was thinner than the cut depth at that location.
  It's kept only as a reference for what not to do; use `decora-single-gang-plate-shelled`
  instead, which was rebuilt from the corrected flat body.
- The Decora shelled body's screw holes are **plain through-holes**, not counterbored, for the
  same reason (a counterbore cut also split the thin shell wall). Only the flat
  `decora-single-gang-plate` has the counterbore.
- Corner radii (outer plate corners, toggle-opening corners) are typical injection-molding
  conventions, not independently verified against a manufacturer drawing.

## Printing notes

- Print flat (large face down), thin dimension vertical — this is the orientation the exports
  are already in.
- No supports should be needed; the relief pocket and counterbore are shallow enough to bridge,
  but check your slicer's preview if using a coarse layer height.
