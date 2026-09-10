# Parameter Sheet — Pet Memorial Urn, Medium (25–50 lb pet size)

Sibling build to [Small](../small/parameters.md) and [Large](../../parameters.md). Sized to the top
of the 25–50 lb range (50 lb), per the same 1 in³-internal-volume-per-lb rule used for every size in
this line. All dimensions independently verified by both a Tester pass (twice — original build and
the scoped brim-fix re-test) and a Reviewer pass, each using a different measurement method against
the exported STEP/3MF/STL files — see `dot_pipeline/tests.md` and `dot_pipeline/review.md`.

## 1. Body

| Parameter | Value | Tag |
|---|---|---|
| Overall height | **131mm** | DERIVED |
| External base OD | **88mm** (r=44mm) | ESTIMATED — foot deliberately thickened from a naive 80.4mm to reach exact parity with the collar (see §6) |
| External belly max OD (45.0% of height) | **120.4mm** (r=60.2mm) | DERIVED |
| External shoulder OD | **100.4mm** (r=50.2mm) | DERIVED |
| External neck OD (below collar) | **78.4mm** (r=39.2mm) | DERIVED — 72mm ID + 2×3.2mm wall |
| Internal neck/collar ID | **72mm** (r=36mm) | **ESTIMATED — the highest-risk figure in this entire size lineup, mates with a real remains bag, sits below the entire 79–89mm real-competitor cluster found for this capacity tier. Not yet physically verified. See §7.** |
| Collar OD | **88mm** (r=44mm) | DERIVED — 72mm ID + 2×8mm reinforcement wall |
| Collar wall thickness | **8.0mm** | ESTIMATED — holds Large's own 2.5× nominal-wall ratio |
| Nominal side wall | **3.2mm** | ESTIMATED — re-derived via a material/cavity-ratio proportionality argument, not a linear scale of Large's 4mm |
| Floor thickness | **4.0mm** | ESTIMATED — 1.25× nominal wall, same ratio as Large |
| Internal cavity volume | **≈805.3–806.5 cm³** (Coder 818.3 hand-calc, Tester 806.1, Reviewer 805.3 — CAD/mesh figures, not the hand-calc) | VERIFIED — target 819.4 cm³, −1.6% to −1.7% |
| Material (shell) volume | **≈182.47 cm³** (Tester and Reviewer agree to <0.01%) | VERIFIED |

## 2. Body profile — control points

Construction: tangent-constrained spline through P0–P4, revolved 360° — same method as Large/Small.

| Point | Z_ext (mm) | Internal r (mm) | External r (mm) | Tangent condition |
|---|---|---|---|---|
| P0 — floor/base | 4 | 37 | 44 | Horizontal (dr/dz=0) |
| P1 — belly max (45.0% of height) | 59 | 57 | 60.2 | Broad plateau |
| P2 — shoulder (inflection) | 77 | 47 | 50.2 | Tangent-continuous |
| P3 — neck-taper-end | 119 | 36 | 39.2 | dr/dz → 0 |
| P4 — rim/top of collar | 131 | 36 | 44.0 (via a tangent blend, independently measured peak angle 44.98°) | Constant radius internally |

Every control point independently confirmed matching this table to the third decimal place (Tester
§1, Reviewer §2).

## 3. Lid

| Parameter | Value | Tag |
|---|---|---|
| Brim OD | **87.700mm** (was 88.000mm — see §8 revision history) | DERIVED — flush with 88mm collar, −0.3mm process allowance applied after the original zero-clearance fit was flagged |
| Brim thickness | **8.0mm** | ESTIMATED |
| Dome base OD | **70.4mm** (r=35.2mm) | ESTIMATED — 0.80 ratio of this build's own brim |
| Dome height above brim top | **≈25mm** | ESTIMATED |
| Dome apex plateau diameter | **≈19mm** (r≈9.5mm, measured 9.23–9.77mm range) | ESTIMATED |
| Total lid height (bounding box) | **41mm** | DERIVED, confirmed exact |
| Lid material volume | **≈123.86 cm³** (post-fix; was ≈124.19 cm³ pre-fix) | VERIFIED |

## 4. Alignment plug (lid underside)

| Parameter | Value | Tag |
|---|---|---|
| Plug OD | **71.5mm** (r=35.75mm) | DERIVED — 72mm ID − 0.5mm clearance |
| Plug wall | **3.2mm** | ESTIMATED — matches this build's own nominal wall |
| Plug interior ID (void) | **65.1mm** (r=32.55mm) | DERIVED |
| Plug total depth | **8.0mm** (5mm hollow + 3mm solid tip cap) | DERIVED — matches Large's 33% bore-zone-margin fraction |
| Diametral clearance vs. neck ID | **0.5mm** | ESTIMATED — held at Large's own figure, a fixed FDM process tolerance |
| Collision margin above internal taper (P3) | **4.0mm** | Independently confirmed via a boolean collision check (0.0mm³ intersection) and direct measurement, both the Tester and Reviewer |

## 5. Material assignments

| Part | Material | Why |
|---|---|---|
| Body | **PLA** (matte/silk) | Finish goal. **The requester was explicitly asked whether to switch to PETG given the thinner 3.2mm wall and drop-risk with an irreplaceable payload, and confirmed keeping PLA** — a deliberate, informed decision, consistent with the same choice made for Small. |
| Lid | **PETG** | Toughness on thin-fillet transitions and the plug wall. |

**Named risk, carried forward from Large:** PLA heat/UV softening, accepted for finish reasons.
PETG-lid-into-PLA-body shrinkage mismatch at the plug/bore interface unverified against a real
print; a clearance-test coupon is recommended before the full lid print.

## 6. Why the base was widened to match the collar exactly

A naive linear scale of Large's base geometry would give ≈80.4mm base OD, but the chosen collar OD
(88mm, driven by the neck-ID decision in §7) would overshoot that by 9.4% — a bigger relative gap
than Large ever accepted. Rather than compromise the neck ID further, the base's external foot was
deliberately thickened (from a naive 3.2mm to 7mm) to bring base OD to exactly 88mm — true parity
with the collar, not just "close." The belly (120.4mm) remains unambiguously the widest feature
(36% wider than base/collar), preserving the vessel's visual hierarchy.

## 7. Standing risk — physical verification required before production printing

**The 72mm neck ID mates with a real crematorium remains bag this team does not have in hand, and
this is the largest research-to-built gap of any size in this product line.** Real manufacturer
spec-sheet data for this exact capacity tier (Reminded, Best Friend Services Odyssey Series) shows
opening diameters clustering tightly at 79–89mm regardless of exact capacity — this build's 50 in³
target sits inside that capacity range, meaning a "conservative" opening arguably shouldn't have
gone much below ~79mm at all. 72mm was chosen anyway, specifically to avoid the collar overshooting
this smaller body's base width (§6). **Both the Tester and Reviewer independently named this the
single highest-priority item to resolve across the entire size lineup, ahead of even Small's or
Large's equivalent risk.** Print `neck-fit-test-medium.stl` and test a real (or mocked) medium-pet
remains bag before committing to the full body print. If it doesn't clear comfortably, the fix is
widening the neck ID in a future revision — which may also require revisiting the base-widening
decision in §6, since the two were resolved together.

## 8. Revision history

| Date | What changed | Why |
|---|---|---|
| 2026-09-09 (v1) | Initial build — full spec, CAD, first Tester pass, all as described above (except §3's brim figure). | First pass for this size. |
| 2026-09-09 (v1.1) | **Brim OD reduced from 88.000mm to 87.700mm on the lid only** (collar OD unchanged at 88.000mm on the body). The first Tester pass measured the brim-to-collar fit as an exact 88.000mm = 88.000mm zero-clearance match — a real, not hypothetical, fit risk. Applied the same −0.3mm allowance Large uses for its own identical flush-fit case. Re-verified clean by a second, scoped Tester pass across all three file formats (STEP/3MF/STL): plug and dome bit-identical pre/post fix, body and neck-fit-test files confirmed untouched, volume delta small and in the expected direction (−0.23 to −0.33 cm³ depending on measurement method). Pre-fix files archived to `archive/pre-brim-tolerance-fix/`. | Avoid a proud/binding lid edge from normal FDM dimensional variance on what was an as-designed zero-margin mating diameter. |
| 2026-09-09 (this pass) | `README.md` and `parameters.md` written for the first time, following the Reviewer pass. | Required follow-up flagged by both the Tester and Reviewer; this project's established convention writes these once a size clears review. |

## 9. Files

| File | Contents |
|---|---|
| `step/urn-body-medium.step`, `3mf/urn-body-medium.3mf`, `stl/urn-body-medium.stl` | Body |
| `step/urn-lid-medium.step`, `3mf/urn-lid-medium.3mf`, `stl/urn-lid-medium.stl` | Lid, current (post-fix) version |
| `archive/pre-brim-tolerance-fix/` | Pre-fix lid files (88.0mm brim), kept for reference only |
| `step/neck-fit-test-medium.step`, `3mf/neck-fit-test-medium.3mf`, `stl/neck-fit-test-medium.stl` | Standalone neck/collar fit-test article — the physical go/no-go for §7's standing risk |
| `render/pet-memorial-urn-medium-hero.png` | Hero render, current (post-fix) geometry |
| `dot_pipeline/specs.md` | Full spec: volume derivation, fresh competitor research, wall/collar re-derivations, full control-point table, v1→v1.1 revision history |
| `dot_pipeline/tests.md`, `verdict.md` | Independent Tester verification, including the scoped brim-fix re-test |
| `dot_pipeline/review.md` | Reviewer's independent second-method verification, business-fit and concept-fidelity assessment |
