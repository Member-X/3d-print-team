# Parameter Sheet — Pet Memorial Urn, Small (0–25 lb pet size)

Sibling build to [Medium](../medium/parameters.md) and [Large](../../parameters.md). Sized to the
top of the 0–25 lb range (25 lb), per the same 1 in³-internal-volume-per-lb rule used for every size
in this line. All dimensions independently verified by both a Tester pass and a Reviewer pass, each
using a different measurement method against the exported STEP/3MF/STL files — see
`dot_pipeline/tests.md` and `dot_pipeline/review.md` for the full cross-check tables.

## 1. Body

| Parameter | Value | Tag |
|---|---|---|
| Overall height (base to collar rim) | **75.7mm** | DERIVED |
| External base OD | **90mm** (r=45mm) | DERIVED — deliberately widened above a naive linear scale to keep the base wider than the collar (see §6) |
| External belly max OD (≈44.3% of height) | **98mm** (r=49mm) | DERIVED |
| External shoulder OD | **88mm** (r=44mm) | DERIVED — deliberately widened, same reason as base |
| External neck OD (below collar) | **74.8mm** (r=37.4mm) | DERIVED — 70mm ID + 2×2.4mm wall |
| Internal neck/collar ID | **70mm** (r=35mm) | **ESTIMATED — the highest-risk figure in this document, mates with a real remains bag, not yet physically verified. See §7.** |
| Collar OD | **82mm** (r=41mm) | DERIVED — 70mm ID + 2×6mm reinforcement wall |
| Collar wall thickness | **6.0mm** | ESTIMATED — holds Large's own 2.5× nominal-wall ratio |
| Nominal side wall | **2.4mm** | ESTIMATED — re-derived via a volume-budget argument, not a linear scale of Large's 4mm (see specs.md §7.1) |
| Floor thickness | **3.0mm** | ESTIMATED — 1.25× nominal wall, same ratio as Large |
| Internal cavity volume | **≈412.3 cm³** (Tester: 412.2–412.4, Reviewer: 412.13, independently corroborating) | VERIFIED — target was 409.6775 cm³, +0.6% |
| Material (shell) volume | **≈72.26 cm³** (Tester and Reviewer agree to <0.01%) | VERIFIED |

## 2. Body profile — control points

Construction: tangent-constrained spline through P0–P4, revolved 360° — same method as Large.

| Point | Z_ext (mm) | Internal r (mm) | External r (mm) | Tangent condition |
|---|---|---|---|---|
| P0 — floor/base | 3.0 | 42.6 | 45.0 | Horizontal (dr/dz=0) |
| P1 — belly max (plateau) | 33.5 | 46.6 | 49.0 | Broad plateau, not a sharp point |
| P2 — shoulder (inflection) | 54.3 | 41.6 | 44.0 | Tangent-continuous, no reversal |
| P3 — neck-taper-end | 66.7 | 35.0 | 37.4 | dr/dz → 0, flattens into collar |
| P4 — rim/top of collar | 75.7 | 35.0 | 41.0 (via a tangent blend from 37.4mm, peak angle ≈44.5–44.8°) | Constant radius internally |

All measured exactly matching this table on the as-built geometry (Tester §1, Reviewer §2) — every
control point confirmed to 3–4 decimal places.

## 3. Lid

| Parameter | Value | Tag |
|---|---|---|
| Brim OD | **81.7mm** | DERIVED — flush with 82mm collar, −0.3mm process allowance |
| Brim thickness | **6.0mm** | ESTIMATED |
| Dome base OD | **65.4mm** (r=32.7mm) | ESTIMATED — 0.80 ratio of this build's own brim |
| Dome height above brim top | **≈23.3mm** | ESTIMATED |
| Dome apex plateau diameter | **16.8mm as-built** (r=8.41mm) — spec derivation targeted ≈17.8mm | ESTIMATED — a minor (~5.5%), non-blocking, cosmetic-only deviation confirmed by both the Tester and Reviewer via independent methods |
| **Brim-to-dome fillet (added by requester, 2026-09-09)** | **5.0mm radius**, at the sharp exterior edge where the flat brim top meets the dome (majorRadius=35.85mm, z=7.0mm) | Manual edit, verified clean — single valid solid maintained, structurally separate from the plug (different height/radius), no functional dimension affected. Distinct from the pre-existing 4mm apex/plateau fillet (majorRadius=8.41mm, z=31.3mm). |
| Total lid height (bounding box) | **≈35.3mm** | DERIVED |
| Lid material volume | **≈90.07 cm³** (post-fillet; was ≈91.41 cm³ pre-fillet) | VERIFIED — Fusion mass-properties, confirmed live |

## 4. Alignment plug (lid underside)

| Parameter | Value | Tag |
|---|---|---|
| Plug OD | **69.5mm** (r=34.75mm) | DERIVED — 70mm ID − 0.5mm clearance |
| Plug wall | **2.4mm** | ESTIMATED — matches this build's own nominal wall |
| Plug interior ID (void) | **64.7mm** | DERIVED |
| Plug total depth | **6.0mm** (3.5mm hollow + 2.5mm solid tip cap) | ESTIMATED — same 33% bore-zone-margin fraction as Large |
| Diametral clearance vs. neck ID | **0.5mm** | ESTIMATED — held at Large's own figure, treated as a fixed FDM process tolerance, not scaled down |
| Collision margin above internal taper (P3) | **3.0mm** | Independently confirmed via measured plug depth + measured taper location (both Tester and Reviewer) |

## 5. Material assignments

| Part | Material | Why |
|---|---|---|
| Body | **PLA** (matte/silk) | Finish goal. **The requester was explicitly asked whether to switch to PETG given the thinner 2.4mm wall and drop-risk with an irreplaceable payload, and confirmed keeping PLA** — a deliberate, informed decision, not an unexamined default. |
| Lid | **PETG** | Toughness on the thin-fillet transitions (brim-to-dome fillet, dome-to-plateau fillet, plug wall) — same reasoning as every other size in this line. |

**Named risk, carried forward from Large:** PLA can soften/warp under sustained heat/UV exposure —
accepted for the same finish-requirement reason. PETG-lid-into-PLA-body shrinkage mismatch at the
plug/bore interface is unverified against a real print; a small clearance-test coupon is recommended
before committing to the full lid print.

## 6. Why the base and shoulder were widened past a naive linear scale

The chosen neck ID (70mm) is well above what a pure volume-based linear scale of Large's design
would give (≈51mm) — a deliberate, research-backed departure (see specs.md §6). This makes the
external neck OD (74.8mm) wider than a naively-scaled shoulder would be, which would otherwise
produce a profile that flares outward instead of tapering inward. The base and shoulder were
therefore deliberately widened (base to 90mm, shoulder to 88mm) so the vessel's visual hierarchy —
belly (98mm) > base (90mm) > shoulder (88mm) > collar (82mm) > neck OD (74.8mm) — is never inverted.
Independently re-confirmed by both the Tester and Reviewer.

## 7. Standing risk — physical verification required before production printing

**The 70mm neck ID mates with a real crematorium remains bag this team does not have in hand.** Real
competitor research was done (see specs.md §6) — two sourced small-tier opening figures (63.5mm,
66.7mm) and explicit industry commentary flagging that range as a documented bag-fit problem at this
weight bracket — and 70mm was chosen specifically to sit above that flagged range. But it remains
`ESTIMATED`, not `VERIFIED`. **Both the Tester and Reviewer independently blocked full production
printing on this item.** Print `neck-fit-test-small.stl` and test a real (or mocked) small-pet
remains bag before committing to the full body print. If it doesn't clear comfortably, the fix is
widening the neck ID in a future revision, not resizing the whole body.

## 8. Proportional drift across the size line (informational, not a defect)

| Size | Collar OD | Belly OD | Collar ÷ Belly |
|---|---|---|---|
| Large | 100mm | 153.9mm | ≈65.0% |
| Medium | 88mm | 120.4mm | ≈73.1% |
| **Small** | **82mm** | **98mm** | **≈83.7%** |

A real, geometrically-forced consequence of not shrinking the neck opening in proportion to volume
at any size — confirmed independently by the Small and Medium Reviewer passes. The belly remains the
widest feature at every size (hierarchy never inverts), but the three sizes will not read as pure
scale copies of one another side by side.

## 9. Files

| File | Contents |
|---|---|
| `step/urn-body-small.step`, `3mf/urn-body-small.3mf`, `stl/urn-body-small.stl` | Body |
| `step/urn-lid-small.step`, `3mf/urn-lid-small.3mf`, `stl/urn-lid-small.stl` | Lid, including the requester's 5mm brim-to-dome fillet |
| `step/neck-fit-test-small.step`, `3mf/neck-fit-test-small.3mf`, `stl/neck-fit-test-small.stl` | Standalone neck/collar fit-test article — the physical go/no-go for §7's standing risk |
| `render/pet-memorial-urn-small-hero.png` | Hero render, current (post-fillet) geometry |
| `dot_pipeline/specs.md` | Full spec: volume derivation, fresh competitor research for the neck opening, wall-thickness/collar re-derivations, full control-point table, revision history |
| `dot_pipeline/tests.md`, `verdict.md` | Independent Tester verification (own STL/STEP/3MF analysis, not a re-read of the Coder's numbers) |
| `dot_pipeline/review.md` | Reviewer's independent second-method verification, business-fit and concept-fidelity assessment |

## 10. Revision history

| Date | What changed | Why |
|---|---|---|
| 2026-09-09 (v1) | Initial build — full spec, CAD, Tester and Reviewer passes, all as described above. | First pass for this size, part of the Director's three-size lineup expansion. |
| 2026-09-09 (manual edit) | Requester added a 5mm-radius fillet to the lid's brim-to-dome edge directly in Fusion; confirmed the lid isn't designed for repeated removal, resolving the line-wide "does no-handle still work" question for this size. | Cosmetic refinement + explicit confirmation of a carried-forward design decision. |
| 2026-09-09 (this pass) | `README.md` and `parameters.md` written for the first time, incorporating the fillet edit and the no-handle confirmation. | Required follow-up flagged by both the Tester and Reviewer; this project's established convention writes these once a size clears review. |
