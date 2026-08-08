# Spec — Lightswitch-Cover-Single (Jumbo Single-Gang Toggle Plate)

Revision spec for the existing Fusion 360 design **"Lightswitch-Cover-Single"**. This document
formalizes corrections to an existing single-gang toggle wall-plate model, carrying forward the
parts of its geometry that are already good practice and correcting the parts that were rounded
metric guesses rather than derived from the real electrical standard. This is a **spec only** —
no modeling or Fusion changes are performed as part of producing this document.

Companion reference: [`switch-plate-covers/parameters.md`](../switch-plate-covers/parameters.md)
(same NEMA-based reasoning, screw strap spacing, and back-relief rationale applied here).

## Source key

Every dimension below is tagged with where it comes from:

| Tag | Meaning |
|---|---|
| **VERIFIED — geometry** | Measured directly from the existing "Lightswitch-Cover-Single" Fusion model (project recon) |
| **VERIFIED — parameters.md** | Taken from `switch-plate-covers/parameters.md`, itself sourced from Kyle Switch Plates / wallplate.store size references and the NEMA toggle-switch strap standard |
| **VERIFIED — retail** | Confirmed via multiple independent retail listings (Amazon, switchplates.com) agreeing on the jumbo single-gang plate standard |
| **VERIFIED — computed** | Arithmetic derived from two or more of the above VERIFIED values (shown with the calculation) |

No dimension in this spec is ESTIMATED — every value is either a direct measurement of the
existing model, an independently corroborated real-world standard, or a computation from those.

---

## 1. Revision history — what changed and why

The existing model was a rough, jumbo-sized single-gang attempt built to clean rounded metric
numbers rather than derived from the real inch-based electrical wall-plate standard. Two
dimensions are corrected; everything else about the design intent (jumbo/oversized format,
shelled back with boss islands, conical countersink, filleted edges) is retained.

| Parameter | Original (unverified draft) | Corrected | Reason |
|---|---|---|---|
| Overall size | 80mm × 125mm (rounded metric guess) | **88.9mm × 139.7mm** (3.5" × 5.5") | True jumbo single-gang standard, confirmed by multiple independent retail listings (Amazon, switchplates.com). The original was a metric rounding, not a derived standard — it happened to be close (80/125 ≈ same 0.64 aspect ratio as 3.5/5.5) but off by ~9mm / ~15mm. |
| Mounting screw spacing | 62mm (2.441") | **60.325mm (2.375")** | Real NEMA toggle-switch strap spacing, already verified and in use on the double-gang plate in `parameters.md`. The original was 1.7mm off from the standard — enough to make the plate incompatible with a real toggle switch's screw strap. |
| Toggle opening size | 11mm × 25mm | **10.32mm × 23.81mm** (0.40625" × 0.9375") | Corrected to the standard opening size documented in `parameters.md`, cross-checked against the same retail size references used for the double-gang plate. |
| Toggle opening corner radius | 4mm | **1.59mm (0.0625" / 1/16")** | The original radius was unusually large for a toggle cutout. 1.59mm matches the toggle-opening corner radius already verified and used in `parameters.md` for the double-gang plate — same feature, same standard. |

Everything else (overall thickness, shell/boss-island construction, screw shank + countersink,
outer fillet) is unchanged from the existing model — see Sections 2–4.

---

## 2. Overall plate

| Parameter | Value | Tag / Source |
|---|---|---|
| Overall width (X) | **88.9mm (3.5")** | VERIFIED — retail (Amazon, switchplates.com; jumbo single-gang standard) |
| Overall height (Y) | **139.7mm (5.5")** | VERIFIED — retail (Amazon, switchplates.com; jumbo single-gang standard) |
| Overall thickness (Z) | **5mm** | VERIFIED — geometry (unchanged, no correction needed) |
| Outer corner fillet radius | **~2.35mm** | VERIFIED — geometry (unchanged; not flagged as incorrect) |
| Edge profile | Rounded bullnose | VERIFIED — geometry (unchanged) |

This remains an intentionally jumbo/oversized single-gang plate (larger than the standard
2.75" × 4.5" single-gang / Decora plate in `parameters.md`) — that design intent was correct in
the original model; only the specific numbers it rounded to were wrong.

## 3. Toggle opening

| Parameter | Value | Tag / Source |
|---|---|---|
| Opening width (X) | **10.32mm (0.40625")** | VERIFIED — parameters.md (toggle opening standard) |
| Opening height (Y) | **23.81mm (0.9375")** | VERIFIED — parameters.md (toggle opening standard) |
| Opening corner radius | **1.59mm (0.0625" / 1/16")** | VERIFIED — parameters.md (same toggle-opening corner radius used on the double-gang plate) |
| Opening center | (0, 0) — plate center | VERIFIED — geometry (unchanged placement convention) |

## 4. Mounting screws

**Revised after initial build** — testing found the first build's screw channel (~4mm long,
full-depth through a solid boss column) was too tight/long for real installation. Rebuilt as a
short guide channel opening into open cavity, matching how the `Body1` reference is actually
constructed, and corrected to real retail hardware dimensions in the process.

| Parameter | Value | Tag / Source |
|---|---|---|
| Screw hole spacing (vertical, center-to-center) | **60.325mm (2.375")** | VERIFIED — parameters.md (NEMA toggle-switch strap standard) |
| Screw hole positions | **(0, +30.1625mm) and (0, −30.1625mm)** | VERIFIED — computed (half of 60.325mm spacing, centered on plate) |
| Screw shank diameter | **4.7625mm (3/16")** | VERIFIED — Kyle Switch Plates retail spec (was 5mm placeholder, corrected) |
| Countersink top diameter | **7.9375mm (5/16")** | VERIFIED — Kyle Switch Plates retail spec (was 7mm placeholder, corrected) |
| Screw head treatment | **90° conical countersink** (45° half-angle) | VERIFIED — geometry, confirmed genuine cone surface, not a counterbore |
| Total guide-channel depth (countersink + shank) | **1.9mm** | VERIFIED — geometry, measured and independently re-confirmed during testing. Opens into fully open cavity below — confirmed no material blocks the path from boss floor to back face. |

## 5. Back construction — open cavity with boss collars

**Revised after initial build.** The first build made the boss a full-height solid column
(0–5mm), which forced the ~4mm screw channel above. Testing traced through `Body1`'s actual
construction and found its interior is not a solid-floored pocket at all — it's a fully open
cavity behind a thin front skin, with short boss "collars" hanging from the skin at each screw
location, opening directly into the cavity below. Rebuilt to match.

| Parameter | Value | Tag / Source |
|---|---|---|
| Front skin thickness (across most of the back, i.e. cavity ceiling) | **1.65mm** | VERIFIED — geometry, matches `Body1`'s measured rim/skin width exactly (superseded the ~4mm rim-inset assumption in the original draft, which was wrong) |
| Relief depth (cavity depth from back to ceiling) | **3.35mm** (5mm thickness − 1.65mm skin) | VERIFIED — geometry |
| Rim inset (solid margin from outer edge, i.e. cavity footprint inset) | **1.65mm** | VERIFIED — geometry, corrected from the original draft's unverified ~4mm assumption |
| Relief pocket / cavity footprint | **85.6mm × 136.4mm** | VERIFIED — geometry, measured directly (supersedes the original draft's computed 80.9×131.7mm, which used the wrong 4mm inset) |
| Boss collar outer diameter | **9mm** | Project design choice (not a retail spec — store-bought plates are solid molded plastic, no boss). Sized with ~0.5mm margin around the 7.9375mm countersink. |
| Boss collar depth (how far the collar hangs below the cavity ceiling, Y=3.35mm floor to Y=3.10mm boss floor) | **0.25mm** | VERIFIED — geometry. (Corrected: an earlier draft of this spec mistakenly copied the 1.9mm guide-channel depth into this field — that's a different dimension, see Section 4.) |
| Boss collar centers | **(0, +30.1625mm) and (0, −30.1625mm)** | VERIFIED — computed (co-located with the screw hole positions, Section 4) |

Clearance against real hardware (switch yoke 44.45mm × 74.625mm, per `parameters.md`): margin of
20.6mm and 30.9mm per side on the two axes — large margin, confirmed during testing.

## 6. Cosmetic variant — tapered edge

A second body, `Lightswitch Cover Single V2 (tapered edge)`, duplicates the corrected-jumbo body
above with one addition: a **1.5mm-radius edge fillet** on the front and back outer perimeter
edges (approximating `Body1`'s rounded/tapered edge look, which is geometrically ambiguous/
possibly compound and wasn't worth exactly reverse-engineering). Confirmed via feature diff
during testing to differ from the corrected-jumbo body *only* by this fillet — no other geometry
changed. 1.5mm radius is a project design choice, not a verified match to `Body1`'s exact edge
construction.

---

## 7. Material recommendation

**PETG over PLA.** The shelled 1.65mm back wall and the two screw boss islands see repeated
mechanical stress from screw insertion/removal over the plate's service life (mounting,
re-mounting, wall-plate swaps). This project has already established, on the double-gang and
Decora plates, that thin walls and screw bosses under this kind of cyclic stress hold up better
in PETG than PLA (which is more brittle and prone to cracking at thin, stressed features). PETG
also tolerates the mild flex needed to seat a plate over a slightly proud switch yoke without
the wall thickness. No change to nozzle assumptions is implied — standard 0.4mm nozzle, and the
1.65mm wall clears the ≥2×nozzle minimum line width comfortably regardless of material.

## 8. Print orientation

**Print flat, bottom (back) face down, thin dimension (5mm, Z) vertical** — same convention used
for the rest of this project's switch-plate deliverables (see `switch-plate-covers/README.md`).
The shell relief and countersinks are shallow enough that no supports should be required; check
slicer preview at coarse layer heights. Testing flagged the boss/collar floor as a small
unsupported bridge (~9mm diameter) inside the hollow cavity — should print fine at that size, but
worth a first-layer check on the initial test print.

---

## 9. Full corrected parameter table (for modeling reference)

Reflects the as-tested, as-built geometry (post-screw-hole revision, Sections 4–5) — see
`dot_pipeline/tests.md` and `dot_pipeline/verdict.md` for the independent QA pass that confirmed
these values against the live model.

| Parameter | Value | Tag |
|---|---|---|
| Overall width (X) | 88.9mm (3.5") | VERIFIED — retail |
| Overall height (Y) | 139.7mm (5.5") | VERIFIED — retail |
| Overall thickness (Z) | 5mm | VERIFIED — geometry |
| Outer corner fillet radius | ~2.35mm | VERIFIED — geometry |
| Toggle opening width | 10.32mm (0.40625") | VERIFIED — parameters.md |
| Toggle opening height | 23.81mm (0.9375") | VERIFIED — parameters.md |
| Toggle opening corner radius | 1.59mm (0.0625") | VERIFIED — parameters.md |
| Mounting screw spacing | 60.325mm (2.375") | VERIFIED — parameters.md |
| Screw hole positions | (0, ±30.1625mm) | VERIFIED — computed |
| Screw shank diameter | 4.7625mm (3/16") | VERIFIED — retail (Kyle Switch Plates) |
| Countersink top diameter | 7.9375mm (5/16") | VERIFIED — retail (Kyle Switch Plates) |
| Screw head treatment | 90° conical countersink | VERIFIED — geometry |
| Total guide-channel depth | 1.9mm | VERIFIED — geometry, tested |
| Front skin / cavity ceiling thickness | 1.65mm | VERIFIED — geometry |
| Relief depth | 3.35mm | VERIFIED — geometry |
| Rim inset from outer edge | 1.65mm | VERIFIED — geometry |
| Relief pocket / cavity footprint | 85.6mm × 136.4mm | VERIFIED — geometry, tested |
| Boss collar diameter | 9mm | Project design choice |
| Boss collar depth (below cavity ceiling) | 0.25mm | VERIFIED — geometry |
| Boss collar centers | (0, ±30.1625mm) | VERIFIED — computed |
| Tapered-edge fillet radius (cosmetic variant only) | 1.5mm | Project design choice |
| Material | PETG | Project decision (rationale in Section 7) |
| Print orientation | Flat, back face down, 5mm dimension vertical | Project convention |
