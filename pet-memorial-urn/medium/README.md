# Pet Memorial Urn — Medium (25–50 lb pet size)

Part of the pet-memorial-urn size lineup, alongside [Small](../small/README.md) (0–25 lb) and
[Large](../../README.md) (50–90 lb, the original build this whole product line's design language
came from). This is the **middle** size, sized to the top of its stated range (50 lb).

## Status: CAD-complete and reviewed, blocked from full-scale production printing

**The neck/collar opening (72mm ID) has not been physically verified against a real remains bag —
and this is a more significant open risk than the equivalent item on Large or Small.** Real
competitor research for this exact capacity tier found opening diameters clustering tightly at
79–89mm; 72mm was chosen below that entire cluster specifically to keep the collar from
overshooting this body's own base width. Both the independent Tester and Reviewer passes named this
explicitly as the single highest-priority item to resolve before committing to a full production
print — print `stl/neck-fit-test-medium.stl` and test-fit a real or mocked medium-pet remains bag
first.

## What it is

A rounded, vase-like memorial urn body with a domed lid, carrying forward the same design identity
established on the Large build's v7 revision:

- **No handle or grip feature of any kind on the lid.** The lid is lifted by hand, gripping the
  brim/dome edge directly. **The requester has confirmed this lid is not designed for repeated
  removal, so the lack of a handle is intentionally fine** — not an oversight or an unresolved
  question.
- **No magnet-assisted or mechanical closure.** The lid simply rests on the body's collar rim.
- **Plain, undecorated body** — no engraving, no plaque, no text.
- **Flush-fit lid brim** (87.7mm OD against the body's 88mm collar OD — a deliberate −0.3mm
  allowance, applied after the first test print found the original 88.0mm-to-88.0mm fit had zero
  print-tolerance margin; same convention Large uses for its own flush brim).
- **Flattened dome apex** (a small flat plateau at the top, not a rounded point).
- **A hollow, capped alignment plug** on the lid's underside (71.5mm OD, 8mm deep) that seats into
  the body's neck bore for a secure, friction-fit alignment.

## Current dimensions (as built and independently verified)

| Parameter | Value |
|---|---|
| Internal cavity volume | ≈805.3–806.5 cm³ (target 819.4 cm³, −1.6%) |
| Body overall height | 131mm |
| Body max OD (belly) | 120.4mm |
| Body base OD | 88mm |
| Neck/collar ID | **72mm** — see the blocking note above, the largest research-to-built gap of any size in this line |
| Neck OD / Collar OD | 78.4mm / 88mm |
| Body nominal wall | 3.2mm |
| Lid brim OD / thickness | **87.7mm** (post-fix, was 88.0mm) / 8.0mm |
| Lid total height (bounding box) | 41mm |
| Dome apex plateau diameter | ≈19mm |
| Plug OD / clearance | 71.5mm / 0.5mm diametral |
| Combined material cost (filament) | ≈$7.7–9.6 |

Full dimension table with VERIFIED/DERIVED/ESTIMATED provenance tags: [parameters.md](parameters.md).

## Material

- **Body: PLA** (matte/silk finish). The body's wall is thinner in absolute terms than Large's
  (3.2mm vs. 4mm), and the Tester/Reviewer both flagged that PLA's brittleness is a real drop/impact
  risk at this thinner wall, holding an irreplaceable payload — PETG was recommended as an
  alternative. **The requester was asked directly and explicitly chose to keep PLA** — this is a
  confirmed, informed decision, not an unexamined default.
- **Lid: PETG** — better toughness for the thin-fillet transitions and the plug wall.

## Print orientation

- **Body:** base down, opening/neck facing up. Fully self-supporting except the neck-to-collar
  external blend (independently measured peak ≈44.98°, right at the 45° guideline — a confirmed,
  not hypothetical, first-print watch-item).
- **Lid:** flat underside down (plug-tip-down), dome facing up. The plug's tip cap is bed-supported;
  the sealed internal ceiling bridge (~65mm diameter — a wide bridge for default settings) will
  likely show some sag/stringing, expected and cosmetic-only since it's fully hidden once assembled.
  **Confirm slicer supports are set to "touching build plate only" before slicing the lid.**

## Known limitations

- **The 72mm neck ID is a bigger compromise, relative to its own supporting research, than any
  other size in this line.** See the Status section above. This is the single item most worth a
  second look before committing to a full print.
- **The brim/collar flush fit started as an exact zero-clearance match** (88.000mm = 88.000mm),
  confirmed by the first Tester pass as a real, not hypothetical, fit risk — since fixed with a
  −0.3mm allowance (brim now 87.7mm), re-verified clean. The applied allowance sits at the low end
  of this printer's own stated tolerance range, so the first physical print's fit is still worth a
  check rather than assuming fully resolved.
- **Proportions read differently than Large.** Medium's collar-to-belly ratio (≈73.1%) sits between
  Large's (≈65%) and Small's (≈83.7%) — a real, geometrically-forced trend across the whole size
  line, not a defect. The three sizes won't look like pure scale copies of each other side by side.
- **The line-wide "does the no-handle design still read as differentiated?" check-in, recommended
  back when Large's handle was removed, has still never happened** — and this is now the third size
  built on top of that unconfirmed identity call. Worth resolving at the product-line level rather
  than letting it age further.

## Files

| File | Contents |
|---|---|
| `step/urn-body-medium.step`, `3mf/urn-body-medium.3mf`, `stl/urn-body-medium.stl` | Body |
| `step/urn-lid-medium.step`, `3mf/urn-lid-medium.3mf`, `stl/urn-lid-medium.stl` | Lid, current (post brim-fix) version |
| `step/neck-fit-test-medium.step`, `3mf/neck-fit-test-medium.3mf`, `stl/neck-fit-test-medium.stl` | **Print this and test-fit a real remains bag before committing to the full body print.** |
| `archive/pre-brim-tolerance-fix/` | Pre-fix lid files (88.0mm brim), kept for reference only |
| `render/pet-memorial-urn-medium-hero.png` | Hero render, current geometry, matte tan appearance |
| `dot_pipeline/specs.md` | Full spec, including the neck-opening research, wall-thickness re-derivation, and the v1.1 brim-fix revision |
| `dot_pipeline/tests.md`, `verdict.md` | Independent verification, including the scoped brim-fix re-test |
| `dot_pipeline/review.md` | Reviewer's independent verification and business-fit assessment |

## Recreating this design

This is a from-scratch parametric build (tangent-constrained spline profile revolved 360°, same
technique as Large and Small), not derived from a mesh import — the full control-point table,
tangent conditions, and construction method are in `dot_pipeline/specs.md` §4–§6, sufficient to
rebuild the geometry exactly without needing the live Fusion document.
