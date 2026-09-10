# Pet Memorial Urn — Small (0–25 lb pet size)

Part of the pet-memorial-urn size lineup, alongside [Medium](../medium/README.md) (25–50 lb) and
[Large](../../README.md) (50–90 lb, the original build this whole product line's design language
came from). This is the **smallest** size, sized to the top of its stated range (25 lb).

## Status: CAD-complete and reviewed, blocked from full-scale production printing

**The neck/collar opening (70mm ID) has not been physically verified against a real remains bag.**
This is the single most important thing left before this design is truly "done" — print
`stl/neck-fit-test-small.stl` and test-fit a real or mocked small-pet remains bag through it before
committing to a full production print of `urn-body-small`. Everything else below has been checked
and approved; this one item is a planning-level open risk, not a modeling defect.

## What it is

A rounded, vase-like memorial urn body with a domed lid, carrying forward the same design identity
established on the Large build's v7 revision:

- **No handle or grip feature of any kind on the lid.** The lid is lifted by hand, gripping the
  brim/dome edge directly. **The requester has confirmed this lid is not designed for repeated
  removal, so the lack of a handle is intentionally fine** — not an oversight or an unresolved
  question.
- **No magnet-assisted or mechanical closure.** The lid simply rests on the body's collar rim.
- **Plain, undecorated body** — no engraving, no plaque, no text.
- **Flush-fit lid brim** (81.7mm OD against the body's 82mm collar OD — a deliberate −0.3mm
  allowance to avoid a proud edge from normal FDM print variance, same convention Large uses).
- **Flattened dome apex** (a small flat plateau at the top, not a rounded point) — reads more
  intentional with no handle up there, and avoids an apex-drooping print artifact.
- **A softened brim-to-dome edge**: the requester added a 5mm-radius fillet directly in Fusion
  where the flat brim top meets the rising dome, rounding a sharp exterior transition. Purely
  cosmetic — verified not to affect the body, the plug, or any mating dimension.
- **A hollow, capped alignment plug** on the lid's underside (69.5mm OD, 6mm deep) that seats into
  the body's neck bore for a secure, friction-fit alignment — a straight-walled design (not a
  tapered stopper), matching the Large build's own rejected-tapered-stopper reasoning.

## Current dimensions (as built and independently verified)

| Parameter | Value |
|---|---|
| Internal cavity volume | ≈412.3 cm³ (target 409.68 cm³, +0.6%) |
| Body overall height | 75.7mm |
| Body max OD (belly) | 98mm |
| Body base OD | 90mm |
| Neck/collar ID | **70mm** — see the blocking note above |
| Neck OD / Collar OD | 74.8mm / 82mm |
| Body nominal wall | 2.4mm |
| Lid brim OD / thickness | 81.7mm / 6.0mm |
| Lid total height (bounding box) | ≈35.3mm |
| Dome apex plateau diameter | 16.8mm (as-built; the spec's own derivation targeted ≈17.8mm — a
  minor, non-blocking, cosmetic-only deviation) |
| Plug OD / clearance | 69.5mm / 0.5mm diametral |
| Combined material cost (filament) | ≈$4.1–5.1 |

Full dimension table with VERIFIED/DERIVED/ESTIMATED provenance tags: [parameters.md](parameters.md).

## Material

- **Body: PLA** (matte/silk finish, matching the "doesn't feel like plastic" goal). The body's wall
  is thinner in absolute terms than Large's (2.4mm vs. 4mm), and the Tester/Reviewer both flagged
  that PLA's brittleness is a real drop/impact risk at this thinner wall, holding an irreplaceable
  payload — PETG was recommended as an alternative. **The requester was asked directly and
  explicitly chose to keep PLA** — this is a confirmed, informed decision, not an unexamined
  default.
- **Lid: PETG** — better toughness for the thin-fillet transitions (brim-to-dome fillet,
  dome-to-plateau fillet, plug wall), same reasoning as every other size in this line.

## Print orientation

- **Body:** base down, opening/neck facing up. Fully self-supporting except the neck-to-collar
  external blend (peak ≈44.5–44.8°, right at the 45° guideline) — worth watching on the first print,
  same low-risk category as every other size in this line.
- **Lid:** flat underside down (plug-tip-down), dome facing up. The plug's tip cap is bed-supported;
  the plug's hollow interior has a sealed internal ceiling bridge (~12mm diameter) that will likely
  show minor sag/stringing under default settings — this is expected, cosmetic-only, and completely
  hidden once assembled. **Confirm slicer supports are set to "touching build plate only" before
  slicing the lid** — a permissive setting could generate unremovable support material inside the
  sealed void.

## Known limitations

- **The 70mm neck ID is a research-informed compromise, not a verified fit.** Real competitor data
  for small-pet urns found two sourced opening figures (63.5mm, 66.7mm) that industry commentary
  explicitly flags as often too narrow for a real bag — 70mm was chosen to sit comfortably above
  that flagged range, but it has not been tested against a real bag. See the Status section above.
- **Proportions read differently than Large.** Because the neck opening wasn't shrunk in proportion
  to volume (a deliberate, reasoned choice — see specs.md §6), Small's collar reads noticeably wider
  relative to its belly than Large's does (≈84% collar-to-belly ratio vs. Large's ≈65%). This isn't
  a defect, but the three sizes won't look like pure scale copies of each other side by side.
  Worth a look at the hero renders (this size's and Large's) before treating this as final.
- **Dome plateau came out slightly smaller than derived** (16.8mm built vs. ≈17.8mm target) — still
  comfortably printable (>20× the print floor), cosmetic-only.

## Files

| File | Contents |
|---|---|
| `step/urn-body-small.step`, `3mf/urn-body-small.3mf`, `stl/urn-body-small.stl` | Body |
| `step/urn-lid-small.step`, `3mf/urn-lid-small.3mf`, `stl/urn-lid-small.stl` | Lid (includes the 5mm cosmetic brim-to-dome fillet, added directly in Fusion by the requester) |
| `step/neck-fit-test-small.step`, `3mf/neck-fit-test-small.3mf`, `stl/neck-fit-test-small.stl` | **Print this and test-fit a real remains bag before committing to the full body print.** |
| `render/pet-memorial-urn-small-hero.png` | Hero render, current geometry, matte tan appearance |
| `dot_pipeline/specs.md` | Full spec, including the neck-opening research, wall-thickness re-derivation reasoning, and the fillet/no-handle-confirmed revision notes |
| `dot_pipeline/tests.md`, `verdict.md`, `review.md` | Independent verification and review history |

## Recreating this design

This is a from-scratch parametric build (tangent-constrained spline profile revolved 360°, same
technique as Large), not derived from a mesh import — the full control-point table, tangent
conditions, and construction method are in `dot_pipeline/specs.md` §6–§9, sufficient to rebuild the
geometry exactly without needing the live Fusion document.
