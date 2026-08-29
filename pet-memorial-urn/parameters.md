# Parameter Sheet — Pet Memorial Urn (Large, current as-built state, v4, 2026-08-29)

**This document describes the actual final as-built geometry**, not the original planning
derivation. `dot_pipeline/specs.md` has gone through four revisions during the build (v1
frustum-stack → v2 tangent-constrained spline → v3 magnet-pocket removal → v4 belly-fullness
edit/wall-rebalance/neck-crease-fix); where anything below differs from an earlier section of
`specs.md`, this document — and the final export files — reflect what was actually built and
shipped. Full narrative (why each change happened, rejected approaches, the independent
Tester/Reviewer verification at each step) is in `dot_pipeline/specs.md`, `tests.md`,
`verdict.md`, and `review.md` — this document intentionally doesn't repeat that story in full,
only the numbers needed to rebuild or edit the design, plus a consolidated incident history
(§6) since this file has had a real, instructive pattern of manual-edit incidents worth keeping
in one place.

**2026-08-28 update (spec v4): the body's belly was manually edited fuller, the inner wall was
reworked to keep tracking it at a constant ~4mm offset, and a separate neck-to-collar crease was
found and fixed.** This grew the internal cavity from ~1511.8 cm³ to **≈1579 cm³** — see §1, §2,
and the new §10 for the full numbers and verification. The lid was **not** touched by this round.

**2026-08-28 update (spec v3): the magnet-assisted closure was removed from the CAD entirely**,
per explicit user decision (handle magnet placement themselves at print time or post-print,
outside this model). §3 below is retired — it now only records what existed historically, for
anyone reading old renders/photos or the incident notes in §6, which still narrate real defects
that happened *while the magnet pockets existed*. The pre-removal STEP/3MF/STL (the exact files
described by the original §3) are preserved, unmodified, at `archive/v2-with-magnet-pockets/` for
anyone who needs to see or re-derive that version. §9 has the full removal writeup.

All dimensions in mm unless stated otherwise. Coordinate convention: Z = height from the part's
own base (Z=0), revolved 360° about the Z axis, both parts centered in X/Y at the world origin
in the exported files — print-ready as exported, no repositioning needed.

---

## 1. Body — overall

| Parameter | Value | Notes |
|---|---|---|
| Overall height (base to top of collar rim) | **160mm** | Unchanged through every revision |
| External base OD | **98mm** | r=49mm — unchanged through every revision |
| External belly max OD | **~153.9mm** (r=76.97mm ext.) | At the belly apex, now a broad plateau spanning Z≈68–70mm (43–44% of the 160mm height), not a sharp point. **v4 value** — grew from the pre-v4 146mm (r=73mm) via a direct, deliberate manual belly edit; see §2 and §10. Internal radius at the apex ≈72.97mm (external minus the verified ~4.00mm wall, below). |
| External shoulder OD | **~92.8mm** (r=46.42mm ext.) at Z=119mm | **Corrected in this documentation pass.** A stale 122mm/r=61mm figure had been carried in this document (and in `specs.md`) since before the v4 belly edit and was never re-derived after that edit shifted the shoulder transition — the Reviewer directly re-measured the as-built geometry and found the actual current value above (`review.md` Addendum 3 §3). Internal radius at the shoulder has **not** been independently re-verified against the current geometry this round; the pre-edit ~57mm figure is carried forward from the v2 derivation as an unverified estimate only — flag for re-check if precision here matters downstream. |
| External neck OD (below collar) | **66mm** | r=33mm — unchanged through every revision |
| Collar OD | **78mm** | r=39mm — delegated-authority revision from an earlier 74mm spec value, carried through every later rebuild, explicitly held unchanged through the v3 magnet-removal and v4 belly edit at the user's own instruction |
| Internal neck/collar ID (constant) | **58mm** | r=29mm, unchanged through every revision |
| Nominal side wall (design target) | **4mm** | The target itself is a design convention (heft/"doesn't feel like plastic"), not a print-minimum; see next row for the as-built verification |
| Side wall thickness (as-built, verified, v4) | **~4.00mm**, confirmed **3.98–4.03mm** across ~60 sampled heights through the belly/shoulder span | The inner wall was reworked during the v4 belly edit specifically to track the new, fuller outer wall at this constant offset. Inner and outer walls now peak at the **same** height — a pre-existing 13.3mm vertical misalignment between the inner/outer peaks (a side effect of the mid-revision inner-wall rework, before it was corrected) is fully resolved. The Reviewer's own independent measurement (a third method, direct NURBS-surface sampling rather than mesh or mass-properties) found **~4.000mm exactly** at every sampled height Z=10–140mm — tighter than the claimed worst-case range at that sampling resolution. |
| Floor thickness | **5mm** | Unchanged through every revision |
| Collar wall thickness | **10mm** | (78−58)/2 — a rim-reinforcement/lid-seating band (originally added to house magnet pockets; those pockets were removed 2026-08-28, see §9 — the collar's own OD/ID/wall/height are unchanged by that removal or by the later v4 belly edit, kept as-is per explicit user instruction both times) |
| Internal cavity volume (current, v4) | **≈1579 cm³** — Coder: 1578.9824 cm³ (Fusion mass-properties), Tester (independent): 1578.11 cm³ (mesh integration), Reviewer (independent, third method): 1578.79 cm³ (direct numerical integral of the sampled parametric surface) | Three genuinely different computational methods converge to within four significant figures — this number is solid. Supersedes the pre-v4 figure of 1511.8 cm³ (itself already +2.3% over the original ~1477.8 cm³ target) — see §2.2 and §10 for the full sequence and why the larger cavity was an accepted, deliberate choice rather than a defect. |
| Body material-shell volume (current, v4) | **≈276.0 cm³** — Coder: 275.9651 cm³, Reviewer (independent): 276.1556 cm³ | Notably **decreased** slightly from the pre-v4 (post-magnet-removal) figure of 293.4042 cm³, despite the cavity growing — the reshaped profile (fuller belly, but a shoulder-to-neck taper that now converges noticeably faster) uses somewhat less total wall material overall. This round is a mild cost improvement, not a tradeoff (`review.md` Addendum 3 §6). |

## 2. Body profile — final spline-based construction, then a v4 manual belly edit layered on top

The body's internal/external profile was originally built as **two tangent-constrained cubic
Bezier-spline curves** (inner cavity boundary + outer wall), not a stack of straight frustum
segments — a full rebuild partway through the project specifically to fix two problems found by
direct visual comparison against `concept/concept-v2.png`: the belly sat too high (56% of height
instead of ~45%), and the straight-line-segment construction produced a visibly faceted body
instead of a smooth curve. **As of v4, the belly/shoulder region has since been directly,
manually edited in Fusion (making the belly fuller) — that is a sculpted change layered on top of
the spline construction below, not a re-run of the spline math.** The P1 (belly) row in the
table below reflects the current, v4, as-built values; P0/P3/P4 are confirmed unchanged; P2
(shoulder) has partial re-verification only (external radius only — see §1's note above).

### 2.1 Control points (internal profile; the external wall is built the same way, offset by wall thickness at each corresponding height)

| Point | Z (from base) | Internal radius | External radius | Tangent condition |
|---|---|---|---|---|
| P0 — floor/base | 5mm | 45mm | 49mm (at Z=0mm, the true base edge) | Vertical (dr/dz=0) — smooth rounded transition off the flat floor. Unchanged through every revision. |
| P1 — belly apex (broad plateau) **†v4** | **~68–70mm (43–44% of height)** | **~72.97mm** (derived: external minus the verified ~4.00mm wall) | **76.97mm** | **Broad, nearly-flat plateau, not a sharp single point** — superseded by a direct manual edit in v4. The original mandatory vertical-tangent/single-clean-peak spline condition (used for the pre-v4 build, where the apex sat at exactly 72mm/45.00%, r=73mm) no longer strictly describes this region. See §10 for the full v4 edit sequence and independent cross-verification. **This is not ~50% up the height, which was an incorrect intermediate figure briefly reported during the v4 documentation-resolution pass, and not the pre-edit 45% (Z=72mm) value** — 43–44% is the corrected, final figure, independently confirmed by three parties (Coder, Tester, Reviewer). |
| P2 — shoulder (inflection) | 119mm | ~57mm (**not independently re-verified against current geometry — carried forward from the v2 pre-edit derivation, may be stale**) | **46.42mm** (~92.8mm OD) — Reviewer-measured directly on the as-built geometry, correcting a stale 61mm/122mm-OD figure that predates the v4 belly edit | Natural/unconstrained (standard central-difference tangent) in the pre-edit construction; not independently re-checked for cusps/reversals against the current as-built geometry this round, though the Reviewer's full-span slope sweep (§10) found no anomalies here. |
| P3 — neck-taper-end / base of collar | 145mm | 29mm | 33mm | Vertical (dr/dz=0) — flattens to match the constant-radius collar-ID cylinder immediately above it. Confirmed unchanged through v4. |
| P4 — rim / top of collar | 160mm | 29mm | 39mm (78mm OD) | Constant radius from P3 (true vertical cylinder). Confirmed unchanged through v4. |

Construction (pre-v4 spline, still the basis everywhere except the belly): each spline is 3
chained cubic Bezier segments (P0→P1→P2→P3), built via exact Hermite-to-Bezier control-point math
(not Fusion's interactive fit-point-spline dragging), then inserted as a `SketchFittedSpline` via
`NurbsCurve3D.createNonRational` + `addByNurbsCurve`. This construction method is retained
outside the belly region; the belly itself is now the product of the v4 manual edit rather than
this parametric recipe (§10).

### 2.2 Volume history — three steps, not a single derivation (why the actual volume isn't a close match to the original target)

A hand-calculable straight-chord (frustum) approximation of the original v2 control-point table
predicted ≈1477.8 cm³ (vs. the 1474.8 cm³ / 90 in³ target — within 0.2%). The **real** v2 spline,
once built, measured **1511.8 cm³ — +2.3% over the target**, because a true tangent-constrained
curve through a true apex bulges outward past the straight-chord approximation near the belly.
This first deviation was within the spec's own pre-authorized ±5% band and was accepted without a
formal spec revision at the time (curve quality — avoiding a re-faceted shoulder — was prioritized
over chasing closer volume precision at that stage; independently reviewed and agreed with, not
just accepted, at both the Tester and Reviewer stage).

**Then, in v4, the user made a direct, intentional manual edit to the outer belly**, making it
visibly fuller, and explicitly chose to **keep** that change. This left the inner wall not
tracking the new outer wall, so the inner wall was reworked to track the outer wall at a constant
~4mm offset (§1). The resulting cavity, **≈1579 cm³, is +6.85% over the original 1474.8 cm³
target** — crossing the spec's own ±5% routine-tolerance band, which is why `specs.md` was
correctly bumped to a formal v4 revision rather than left as an informal understanding. The user
explicitly chose to **accept the larger capacity** rather than thin the wall below ~4mm to force
the volume back down — a deliberate, informed override of the original volume-tolerance-driven
sizing, not a defect silently absorbed. See §10 for the full sequence, verification, and the
Reviewer's business-fit re-confirmation (this is a *more* generous design, not a shortfall).

### 2.3 Neck-to-collar external blend (Z=145–152mm) — two separate fixes, at two different points in the project

The P0–P4 spline above only governs the **internal bore**. The external wall's transition from
the neck OD (66mm) to the full collar OD (78mm) went through two distinct, unrelated repairs:

**Fix #1 (pre-v4):** the transition was initially left as a straight conical chamfer (a leftover
from the pre-spline design) — found to be a literal straight line with two sharp corners (an
instantaneous slope jump at both Z=145mm and Z=152mm), visible as a distinct crease line directly
below the rim. Replaced with a single tangent-constrained cubic Bezier segment, vertical tangent
at both ends (matching the neck taper below and the flat collar cylinder above). Verified via
0.1mm-resolution slope sampling: slope changed gradually and continuously across the full 7mm
span (largest single-step change ~0.23, vs. the old ~0.95 instantaneous jump) — a genuine smooth
S-curve. Peak local angle at that time: ~45.6° from vertical.

**Fix #2 (v4, 2026-08-28):** independent of Fix #1 above and independent of the belly/wall
changes in §2.2, a **separate, pre-existing crease** at the neck-to-collar junction — in the
outer wall, at the top of the neck just below where the collar begins, left over in the outer
wall as the user's belly edit reshaped that region — was found during this revision's
verification pass. Repaired with a **narrowly-scoped fix (only the final 5mm of the outer wall's
tail near the rim)**, rather than touching the wider blend or the belly/collar geometry around
it. Independently confirmed fixed: the junction is smooth at print-relevant resolution. A
sub-print-resolution irregularity was also found at the repair splice seam — ~100× finer than a
typical print layer height, explicitly checked and found immaterial, not a remaining defect.

**Net result after both fixes:** peak local angle at this transition is now **~47.25° at
Z=147.25mm** (up ~1.6° from the ~45.6° figure after Fix #1 alone) — the same disclosed, low-risk
"watch it on the first print" band as before, not a new site or a new category of risk (see §2.4
and §10).

### 2.4 Overhang summary (current, v4)

| Transition | Angle from vertical | Category | Risk |
|---|---|---|---|
| Base → belly apex (Z=0–~69mm) | Gentle flare throughout | Radius *grows* with height, but confirmed **monotonically non-decreasing** across 1,382 sampled steps at 0.5mm resolution (Reviewer, v4 re-check) | None — genuinely self-supporting, no local reversal anywhere |
| Belly apex → shoulder → neck taper end (Z≈69–145mm) | Up to ~54.5° locally at the steepest point (shoulder-to-neck-taper span) | Radius *shrinks* with height (shrinking-cone class) throughout, confirmed still true on the current, fuller/lower belly (Reviewer, v4 re-check: local angle negative at virtually every sampled point; the only positive-angle noise found, 123 of 2,016 steps, tops out at 0.409° — floating-point/sampling noise at the near-flat belly plateau, not a real reversal) | None — self-supporting at any angle; the belly getting bigger and moving slightly lower did **not** introduce a new overhang risk here |
| Neck-to-collar blend (Z=145–152mm) | **~47.25° peak** (Z≈147.25mm) — up from ~45.6° pre-v4, see §2.3 | Radius *grows* with height (real overhang class, but on a short, fully closed 360° revolve) | Low — a few degrees over the 45° guideline; disclosed "watch it" band on the first print (extra cooling / a modest local speed reduction), not expected to need supports. **This is the only zone anywhere on the entire outer wall that exceeds 45°** — confirmed by a full-span continuous sweep, not just a re-check of the previously-known spot (Reviewer, v4). |

## 3. Magnet-assisted closure — REMOVED 2026-08-28, this section is historical only

**As of spec v3 (2026-08-28), this feature no longer exists in the model.** The table below is
kept verbatim as a historical record (it describes exactly what the incident notes in §6 are
narrating, and what the archived `archive/v2-with-magnet-pockets/` files still contain) — it does
**not** describe the current geometry. The current body and lid have no pockets, bosses, or
recesses of any kind at these (or any) locations; the collar top and the lid underside are both
plain, uninterrupted flat surfaces, confirmed unaffected by the later v4 belly/wall edit as well
(§10). See §9 for the removal writeup and re-verification results.

| Parameter | Value (historical — no longer modeled) |
|---|---|
| Magnet type | 6mm diameter × 2mm thick neodymium disc, N42 (commodity size) |
| Count | 6 total — 3 in the body collar top, 3 in the lid underside |
| Bolt circle radius | **34mm** (the true midline of the 10mm-thick collar wall — re-centered here during an earlier fix; not the original spec's 33mm) |
| Spacing | 120° apart (3-fold symmetry — lid seats correctly at any of 3 rotations, no keying feature needed) |
| Pocket size | 6.2mm diameter × 2.2mm deep (0.2mm oversize over the 6×2mm magnet on both dimensions) |
| Embedding method | Post-print: print open-face pockets, insert magnets after printing, secure with CA glue or epoxy, flush with the surrounding surface |
| Polarity | Mark before gluing — all 3 lid magnets same pole down, all 3 body magnets same pole up (opposite the lid's) |
| Verified margin | 1.9mm of solid material on both the inner (cavity-side) and outer (exterior-side) of every pocket — genuinely symmetric, confirmed by direct measurement, not an average |

**Why it was removed:** the user decided to handle any magnet placement themselves, either via a
slicer-level pause-and-embed workflow or a fully manual post-print drill-and-glue step, rather
than have it pre-modeled. This was a deliberate scope reduction, not a defect fix — the "not yet
print-verified" oversize-tolerance risk noted below never actually got resolved one way or the
other; it's moot now since the pockets don't exist to have a tolerance on.

**Historical, no longer applicable:** the 0.2mm oversize was a standard hobbyist convention, not
calibrated against this printer or either material. PETG in particular tends to string/ooze
into small negative features more than PLA — this would have needed a small test-coupon print
before committing to full production, had the feature survived to v3.

## 4. Lid

**Unaffected by the v4 belly/wall/crease-fix round** — the lid was not touched in that revision;
every figure below is unchanged from the previous documentation pass.

| Parameter | Value |
|---|---|
| Overall height (flat underside to top of handle) | 75mm (5mm brim + 30mm dome + 40mm handle) |
| Flat brim disc OD | 100mm |
| Brim thickness | 5mm |
| Dome height above brim top | 30mm |
| Dome base OD (where it meets the brim) | ~80mm |
| Seating interface | Single flat plane — the lid's entire underside rests directly on the body's flat 78mm-OD collar rim. No plug/skirt/alignment lip (deliberately dropped early in the design — a lip would create an unsupported overhang shelf on the one surface most needing to stay flat and print-clean). Centering is by eye/feel (no magnet assist — that feature was removed 2026-08-28, see §9). |
| Handle clear opening | 24mm wide × 22mm tall (independently verified via mesh cross-section, present consistently from y=−4mm to +4mm, cleanly open — a genuine through-channel, not a blind pocket) |
| Handle bail cross-section | 9mm round |
| Handle height above dome apex | 40mm |
| Handle-to-dome foot | Each bail leg terminates in a small rectangular plinth/foot (~32mm × 14mm cross-section) where it meets the dome, rather than the round 9mm bail meeting the curved dome surface directly — gives a wider, more reliable structural bond and print-bed-adhesion footprint than a thin round-to-curved-surface junction would |
| Fillet at handle-to-lid junction | 4mm |
| Handle load case | Rated only for lifting the lid's own weight (~150–190g), not the assembled urn — a 9mm PLA/PETG loop has large margin over this; not sized for heavier loads |
| Lid material-shell volume | 151.16 cm³ (Fusion) / 151.02 cm³ (mesh) — was 150.96/150.82 cm³ before the 2026-08-28 magnet-pocket removal (§9); the small increase is exactly the filled-in pocket volume |

The lid was **not** part of either full-profile rebuild (§2), and was **not** touched by the v4
belly edit — it has been geometrically unchanged since its original build, aside from a
material-only relabel (§5) and a brief in-session incident (§6.2) that was caught and fully
restored before any file was re-exported.

## 5. Material assignments

| Part | Material | Why |
|---|---|---|
| Body | Matte or silk PLA | The body's large smooth, undecorated curved surfaces are what most need the matte/silk "not plastic-feeling" finish the concept calls for — PLA has a wider selection of matte/silk filament options than PETG |
| Lid | **PETG** (changed from PLA) | The handle root fillet is the feature most exposed to a knock or repeated cyclic grip load over years of use — PETG's meaningfully better impact toughness and interlayer adhesion directly address that risk. Confirmed (not just assumed) that this needs no geometry change: the handle fillet and wall thickness were already sized conservatively enough that PETG only *improves* the margin |

**PETG-specific considerations, independently flagged, not yet resolved by geometry:**
- PETG prints at a higher temperature and cools more slowly than PLA, which generally makes fine
  bridging/near-horizontal artifacts (stringing, drooping) more pronounced at a given geometry —
  relevant at the lid's dome apex (already a known, minor, cosmetic-only drooping risk under
  PLA) and worth accounting for in slicer cooling/speed settings, not a geometry concern.
- No orientation change needed for either material — the lid's flat-underside-down orientation
  is already the best-case orientation for PETG's stronger bed adhesion/warping tendencies too.

**Fusion appearance (render-only, not a printed property):** for anyone re-opening the live
document, the body's assigned appearance is **"Matte PLA - Stoneware Tan (urn-body)"** and the
lid's is **"Matte PETG - Stoneware Tan (urn-lid, sanded)"** — both custom appearances derived
from the Fusion Appearance Library's matte plastic base, recolored to a warm tan matching
`concept/concept-v2.png`. Like the material-name metadata note below, this is a visual/render
property layered on the geometry, not a printed or slicer-read setting. **See §6.5/§10 for an
incident where the body's appearance was found silently reverted to Fusion's default "Steel -
Satin" after a timeline rebuild, and had to be reapplied** — worth checking after any future
Revolve/rebuild on this body.

Neither material assignment is embedded in the exported files in a slicer-readable way. The
body's `3mf` does carry the material note as a free-text 3MF `<metadata name="Description">`
field (Fusion exports the component description verbatim) — the lid's `3mf` does not (it was
exported before the PETG description was written onto the component). No slicer auto-reads
material from this field either way — it must be set manually in both cases.

## 6. Incident notes — five real incidents found and fixed during this build (read before editing further)

This live Fusion document has a real, repeating pattern worth keeping in one place for future
editors: **five separate incidents** across the project's lifetime — a mix of scripted-cut
mistakes, direct manual UI edits, and one silent side effect of an otherwise-legitimate timeline
rebuild — every one of them found and fully recovered/verified, none left with residual damage in
the shipped files. Listed chronologically; full technical detail is in the subsection or
cross-referenced section named for each.

**Standing recommendation, reaffirmed after every incident below:** prefer timeline-native,
script-driven parametric edits over direct manual dragging of sketch/BRep geometry in the Fusion
UI for this file. If a manual edit is ever unavoidable, treat it as a higher-scrutiny change
requiring an explicit before/after geometry check (volume, face count, slope continuity, and now
also appearance/material assignment — §6.5), not just a visual glance in the viewport.

### 6.1 Cross-component `participantBodies` leak (original base-pocket defect) — pre-approval

**Root cause:** `ExtrudeFeatureInput.participantBodies` defaults to "all bodies geometrically
intersected by the cut" when left unset. Because `urn-body`, `urn-lid`, and `neck-fit-test` are
all separate components sharing the same local origin in this Fusion document, a cut created in
one component's sketch — if `participantBodies` isn't explicitly restricted — can silently cut
into a completely unrelated body in a different component, if that body happens to occupy the
same local coordinates. This is exactly what happened: the lid's magnet-pocket cut (at the
lid's own local Z=0, its flat underside) leaked into the body's base (also at local Z=0),
producing 3 unintended 6.2mm pockets on the body's underside — dimensionally identical to the
legitimate collar pockets, which is why it initially looked like a plausible intentional feature
rather than a bug.

**This is a standing risk for this file, not a one-off mistake.** Any future cut/extrude added
to any component in this document should explicitly set `participantBodies` to only the
intended target body. This was applied when the collar-pocket and lid-pocket cuts were rebuilt,
but the original body-collar cut (`Extrude1`) predates this practice and has never actually
shown leakage (no other body currently occupies its z-range) — flagged as a latent, unexercised
risk rather than something that was retroactively edited, since editing an existing committed
feature's participant list proved fragile (see below) and this specific feature has never
manifested the problem.

### 6.2 Manual sketch edit corruption + recovery — pre-approval

Partway through the collar-blend fix (§2.3 Fix #1), a direct manual edit to the `BodyProfile`
sketch (made directly in the Fusion UI, not via a script) left the sketch as an open, non-closed
loop — two disconnected points near the revolve axis, one of which implied the 58mm neck ID had
been dragged down to ~0mm (which would have eliminated the opening entirely and broken the lid
seating interface). `Revolve1` was left running on stale cached geometry (a degenerate 2-face,
4.45 cm³ fragment, not a usable body).

**This was not completed or salvaged** — the implied end state was not just imprecise but
functionally broken (no neck opening), so the profile was rebuilt from the last fully-verified,
spec-matching configuration instead of guessing at the incomplete edit's intent. Recovering
required deleting and recreating `Revolve1` (a `RevolveFeature.profile` reassignment on an
already-committed feature with a "lost reference" error could not be done in place), which
cascade-deleted the dependent `Extrude1` (collar-pocket cut); both were rebuilt fresh, with
`Extrude1` recreated with `participantBodies` explicitly restricted this time. Independently
re-verified afterward: cavity volume, belly position, and shoulder-region radii all matched the
pre-incident measurements exactly (to 4–5 significant figures) — a genuine reconstruction of the
same design, not a coincidentally-similar rebuild.

### 6.3 Third manual-edit incident — collar/neck manual drag (post-approval, 2026-08-27)

A user-described edit "near the lid magnet pocket" turned out, on investigation, to have left the
**lid entirely untouched** — the actual damage was a manual drag on the **body's** neck/collar
region, ballooning the collar ID/OD from 58mm/78mm to ~70.7mm/~90.4mm, which indirectly clipped
the magnet pockets (which still existed in the model at this point, pre-v3) down to abnormal
~3×1.9mm cuts as the growing bore ate into the 34mm pocket bolt circle. This was not a delegated
design change — it was treated as an unintended regression and recovered by reproducing the exact
previously-verified control-point/tangent recipe; this time `Revolve1` picked up the corrected
profile cleanly, with no cascade rebuild of `Extrude1` needed (unlike §6.2).

Independently re-verified by both the Tester (`tests.md` Re-test Pass 4, R25–R29) and the
Reviewer (own `trimesh` script, not inherited from the Coder/Tester chain), against the
**pre-v4** design state then in effect: watertight/single-component/Euler=2, bounds unchanged
(±73.0mm XY, 0–160mm Z), shell volume 293.1365 cm³ and face/vertex counts 47,298/23,651 both
bit-for-bit identical to the Tester's own figures, belly apex exactly 73.000mm at Z=72.0mm
(45.00% — the pre-v4 value), collar OD exactly 78.000mm, base cleanliness 77 vertices at r=49.00mm
with zero interior vertices, magnet pockets restored to the correct 6.2mm-diameter/34mm-bolt-circle
spec, and the neck-to-collar blend confirmed still smooth. (All belly/shoulder figures above are
the **pre-v4** state this incident was recovered back to — they have since been superseded by the
deliberate v4 belly edit, §2.2/§10; this incident's own recovery was clean and complete against
the design as it existed at the time.) Standing lesson reaffirmed: this is now the **third**
incident tracing to manual UI dragging rather than scripted/timeline-native edits.

### 6.4 Magnet-assisted closure removed from CAD (2026-08-28, spec v3) — deliberate scope reduction, not a defect

Per explicit user decision, both magnet-pocket cut features were deleted outright from both
parts. This was **not** a defect fix — see §3 for the historical record of what was removed and
§9 for the full removal writeup and re-verification (body-count/face-count/volume-delta checks,
both parts confirmed still single-solid and watertight, cavity volume confirmed unaffected).

### 6.5 v4 belly-fullness edit, inner-wall rebalance, neck-to-collar crease fix, and appearance-reversion catch (2026-08-28, spec v4)

A deliberate, user-directed aesthetic edit (fuller belly) with a genuine volume consequence the
user explicitly chose to accept, plus one incidental side-effect catch (the body's render
appearance had silently reverted to Fusion's default "Steel - Satin" — almost certainly a side
effect of the `Revolve1` recreation associated with this round's work resetting the body's
appearance override; the correct custom appearance was still defined in the document, just not
applied, and was reapplied and saved). This is the **second** time in this project that a
timeline-native rebuild has silently reset something adjacent to the geometry it touched (the
first being the `participantBodies` default itself, §6.1) — worth specifically checking
appearance/material assignment, not just geometry, after any future rebuild in this file. Full
detail, numbers, and independent cross-verification: §10.

## 7. `neck-fit-test` standalone article

A small (~35mm tall, ~122mm max OD) standalone print of just the neck taper + collar section
(shoulder-cut flange at the bottom for bed stability, open bore both ends), built specifically
so the requester can physically test whether a real crematorium remains bag fits through the
58mm neck ID before committing to a full ~160mm body print. Confirmed: 58mm ID and 78mm/66mm OD
(collar/neck) exactly matching the body's own dimensions, watertight, single manifold solid,
self-supporting in its natural flange-down orientation.

**Does not need to be regenerated** if the body profile changes again in a way that doesn't
touch the 58mm ID or 78mm OD collar dimensions specifically (i.e. further changes to the
belly/shoulder region below the neck, per §2, do not affect what this test article represents).
It was **not** rebuilt during either full-body-profile rebuild in this project (v2's spline
rebuild or v4's belly edit), because neither touched the neck ID/collar OD — confirmed by direct
re-measurement each time, not assumed. File timestamps confirm it: `neck-fit-test.*` remain
unchanged from 2026-08-27 13:00, while `urn-body.*` were re-exported 2026-08-28 10:08 for the v4
round.

**This is the requester's own physical test to run, and it has not been run yet** — see the
outstanding-items note in `README.md`. No CAD verification can substitute for actually printing
this and trying a real (or mocked) remains bag through it. **Note on hole shrinkage:** FDM parts
typically print circular IDs slightly undersized versus the model — no compensation has been
baked into the 58mm nominal ID since there's no fixed target to compensate toward (it's an
untested fit against a real bag, not a hardware spec, per `specs.md` §4.4). Check the *actual*
as-printed ID on this test article, don't assume 58mm nominal is what comes off the printer.

## 8. Files

| File | Contents |
|---|---|
| `step/urn-body.step` | Current body, re-editable, reflects the v4 belly edit/wall-rebalance/crease-fix (§2, §10) and the v3 magnet-pocket removal (§9) |
| `3mf/urn-body.3mf` | Current body, slicer-ready. Re-exported 2026-08-28 10:08 for the v4 round. |
| `stl/urn-body.stl` | Current body, universal fallback. Re-exported 2026-08-28 10:08 for the v4 round, independently re-verified watertight. |
| `step/urn-lid.step`, `3mf/urn-lid.3mf`, `stl/urn-lid.stl` | Current lid, magnet pockets removed per §9 (2026-08-28, timestamp 08:16) — **not** touched by the v4 belly-edit round; still the same files as the post-magnet-removal export |
| `archive/v2-with-magnet-pockets/urn-body.{step,3mf,stl}`, `archive/v2-with-magnet-pockets/urn-lid.{step,3mf,stl}` | **Superseded** pre-§9 versions (with the 3+3 magnet pockets described in §3), preserved unmodified for reference — not the current print files |
| `step/neck-fit-test.step`, `3mf/neck-fit-test.3mf`, `stl/neck-fit-test.stl` | Standalone neck/collar fit-test article, §7 — unaffected by §9 or §10, not re-exported since 2026-08-27 |
| `render/pet-memorial-urn-hero.png` | **Current** hero render, refreshed 2026-08-28 from the current (v4) geometry — matte tan "stoneware" appearance on both parts, Photo Booth lighting, lid shown at its true seated height for the render only (the live document itself is not left in an assembled state). A faint viewport grid overlay is visible in the background, a rendering-tool limitation, not a model defect. |
| `archive/pre-v4-belly-render/pet-memorial-urn-hero.png` | **Superseded** hero render from before the v4 belly edit (dated 2026-08-27) — preserved for reference, no longer depicts the current belly proportions |
| `dot_pipeline/specs.md` | Full spec, including the v1→v2→v3→v4 revision history and the delegated-authority deviations (78mm collar OD, etc.) |
| `dot_pipeline/tests.md`, `verdict.md` | Full independent verification history across all build/fix rounds |
| `dot_pipeline/review.md` | Reviewer's independent re-verification and approval, including three post-approval addenda (third manual-edit incident, magnet-pocket removal, v4 capacity/overhang re-check) |

## 9. Magnet-pocket closure removal (2026-08-28, spec v3) — what changed, how it was verified

**What was removed:** the two magnet-pocket cut features only — `Extrude1` in the `urn-body`
component (Cut operation into `urn-body-solid`, using the 3-circle `MagnetPocketsBody` sketch
profile) and `Extrude5` in the `urn-lid` component (Cut operation into `urn-lid-solid`, using the
3-circle `MagnetPocketsLid` sketch profile). Both were deleted outright from the document
timeline (not suppressed) via `Feature.deleteMe()`. Both sat at the tail of their component's
feature chain with nothing downstream depending on them, confirmed by their timeline position
before deletion — so this carried no cascade risk, unlike the `Revolve1`/`Extrude1` cascade in
the §6.2 incident. Timeline count went from 31 to 29 entries — exactly the 2 deleted, no more, no
less. The now-unused `MagnetPocketsBody`/`MagnetPocketsLid` sketches and the `CollarTopPlane`
construction plane were deliberately left in place, unedited — the task was scoped to the cut
features only, and touching sketches in this exact region of the file is what caused the §6.2
incident, so the minimal-risk choice was made here.

**Timeline structure note for future editors:** this document's timeline is one flat,
chronological list shared across all three components (`urn-body`, `urn-lid`, `neck-fit-test`) —
it is *not* grouped by component, and feature names (`Revolve1`, `Extrude1`, etc.) are scoped
per-component, so the same name appears more than once at different timeline positions for
different components. Match on both `entity.name` **and** `entity.parentComponent.name` before
touching anything by name alone. The body's own main profile revolve and its magnet-pocket cut
both ended up appended at the very end of the timeline (indices 29–30 out of 31) because they
were rebuilt fresh during the §6.2 recovery — do not assume timeline position reflects "logical"
feature order for this file. (The v4 belly edit, §10, further modified the body's profile
geometry after this point in the timeline — re-check current indices before assuming this map is
still accurate.)

**Re-verification performed (both parts, at the time of this removal — i.e. against the pre-v4
belly geometry then in effect):**
- Body count stayed at 1 solid per component (3 total in the document) — no split, no orphaned
  fragment, before and after.
- Face/edge counts dropped by exactly 6/6 on each part (3 pocket-wall cylinders + 3 pocket-floor
  planes per part) — matches a clean fill, nothing else touched.
- Volume increased by +0.1992 cm³ (body) and +0.1993 cm³ (lid) — both match the theoretical
  filled-pocket volume (`3 × π × 3.1² × 2.2mm = 0.1993 cm³`) almost exactly, confirming the only
  material change was the pockets themselves.
- The body's top-collar face is now a 2-loop plane (was 5-loop with the pockets) at the exact
  theoretical full-annulus area, `π(39²−29²) = 2136.28mm²` — a genuinely plain flat-topped ring.
  The lid's underside face is now a 1-loop plane (was 4-loop) at the exact theoretical full-circle
  area, `π·50² = 7853.98mm²` — a genuinely plain flat disc.
- The body's inner bore cylinder (r=29.0000mm, z=145–160mm, the collar ID) measured **bit-identical**
  before and after — proving the cavity-defining boundary was never touched by this edit. Every
  other face bounding the internal cavity (floor plane at z=5, main internal-wall NURBS surface
  z=5–145) also measured identical area/extent before and after. Cavity volume (1511.8 cm³, the
  pre-v4 figure) was therefore unaffected by this specific edit — confirmed by this direct
  face-level check, not assumed from the pocket's small size alone.
- Belly apex independently re-sampled by scanning the outer-wall NURBS surface's profile
  parameter: max radius found at r=72.9999mm, z≈72.0–72.1mm (≈45.0% of the 160mm height, the
  pre-v4 value) — matches spec exactly, confirming the main body profile was not disturbed by
  this edit.
- Every other face on both bodies (outer wall, neck-to-collar blend, outer collar cylinder,
  dome, brim, handle bail cylinders, handle-to-dome plinths, base) matched **exactly** in area and
  Z-extent between the before- and after-edit face enumerations — the strongest available proof
  that nothing outside the two pocket cuts was disturbed.
- Found (and explained, not "fixed" — not a defect): both bodies have a small number of edges
  owned by only one face (3 on the body, 2 on the lid). These are seam-curve artifacts of the
  custom NURBS surfaces of revolution (the seam is used twice by the same wrapping face) — their
  geometry runs exactly along the θ=0 meridian matching each surface's own control-point profile,
  and they belong to faces proven bit-identical before/after this edit. The untouched
  `neck-fit-test` body (built from plain analytic cylinders/planes, no custom NURBS) shows zero
  such edges, confirming this is a surface-type characteristic of the body/lid's construction
  method, not a manifold defect and not something introduced by this change.
- Independently re-verified outside Fusion: both exported STL meshes pass a from-scratch
  watertightness check (every edge shared by exactly 2 triangles — 0 non-manifold edges in
  either mesh) with mesh-integrated volumes within ~0.03–0.09% of the exact Fusion BRep values
  (normal tessellation-vs-exact-surface deviation, not a defect). Both bounding boxes confirm
  correct print-ready placement (Z=0 at the base, centered in X/Y) independently of Fusion's own
  reporting.
- Quick corroboration by the Reviewer (Addendum 2): a fresh sweep of the collar band
  (Z=155–159.9mm) showed exactly 2 boundary loops (outer wall + inner bore only) at every
  sampled height, versus 5 loops before removal — confirming the pockets are genuinely gone, not
  capped over. Lid underside sweep (Z=0–2.5mm) showed exactly 1 loop at every height.

**Volumes immediately after this change (pre-v4 baseline — since superseded by the v4 belly
edit for the body, §10; the lid figures below remain current):**
- Body material-shell volume: 293.4042 cm³ (was 293.2050 cm³) — **since superseded**, see §1 for
  the current v4 figure (≈276.0 cm³).
- Lid material-shell volume: **151.1556 cm³** (was 150.9563 cm³) — **still current**, the lid was
  not touched by v4.
- Body internal cavity volume: unchanged by this edit at 1511.8 cm³ — **since superseded**, see
  §1/§2/§10 for the current v4 figure (≈1579 cm³).

**Files re-exported at the time:** `step/urn-body.step`, `3mf/urn-body.3mf`, `stl/urn-body.stl`,
`step/urn-lid.step`, `3mf/urn-lid.3mf`, `stl/urn-lid.stl` — all six, both parts. Pre-removal
versions of all six are preserved at `archive/v2-with-magnet-pockets/` (§8). The body files were
re-exported again for v4 (§10); the lid files from this magnet-removal round remain the current
lid files.

**What was explicitly not touched, confirmed by the checks above:** body profile/spline/belly/
shoulder/neck (as they existed at the time — subsequently changed by v4, §10), collar OD/ID/wall/
height (78/58/10/15mm, unchanged per explicit user instruction — not reverted to a nominal wall,
and still unchanged as of v4), lid dome/brim/handle geometry, material assignments, print
orientations, `neck-fit-test`.

## 10. v4 belly-fullness edit, inner-wall rebalance, and neck-to-collar crease fix (2026-08-28, spec v4)

### Sequence of changes

1. **The user manually edited the body's outer belly in Fusion to make it visibly fuller**, and
   explicitly chose to **keep** that change rather than revert it — a deliberate aesthetic
   decision, not a defect.
2. This left the **inner wall not tracking the new, fuller outer wall** (uneven thickness). The
   user directed a rework of the inner wall to track the outer wall at a **constant ~4mm offset**,
   matching the wall-thickness approach used everywhere else in this profile — rather than (a)
   leaving the mismatched inner wall as-is, or (b) thinning the wall below ~4mm specifically to
   force the volume back down toward the original target.
3. **The resulting cavity volume, ≈1579 cm³, is structurally larger than the original target
   allows.** The user explicitly chose to **accept the larger capacity** as the deliberate,
   informed consequence of steps 1–2, rather than have the wall thinned to compensate. This
   crossed the spec's own ±5% routine-tolerance band (+6.85% over the original 1474.8 cm³
   target), which is why `specs.md` was formally revised to v4 rather than left as an informal
   Coder/Tester understanding.
4. **A separate, unrelated crease** at the neck-to-collar junction (in the outer wall, a leftover
   from how the user's belly edit reshaped that region, not connected to the belly/wall changes
   themselves) was found during this revision's verification pass and repaired with a
   narrowly-scoped fix (§2.3, Fix #2).
5. **Incidental catch:** while preparing the refreshed render, the body's Fusion appearance was
   found silently reverted to the default "Steel - Satin" — a side effect of the `Revolve1`
   recreation associated with this round's work resetting the body's appearance override. The
   correct custom appearance ("Matte PLA - Stoneware Tan (urn-body)") was still defined in the
   document, just not applied; it was reapplied and the document saved. Not a geometry defect,
   no bearing on the printed part — but the **second** time in this project a timeline-native
   rebuild has silently reset something adjacent to the geometry it touched (the first being the
   `participantBodies` default itself, §6.1). Worth specifically checking appearance/material
   assignment, not just geometry, after any future rebuild in this file.

### Independent cross-verification (three parties, three methods)

| Check | Coder (Fusion mass-properties) | Tester (mesh integration) | Reviewer (own NURBS-surface sampling + numerical integral, live doc) |
|---|---|---|---|
| Cavity volume | 1578.9824 cm³ | 1578.11 cm³ | 1578.79 cm³ |
| Material (shell) volume | 275.9651 cm³ | — | 276.1556 cm³ |
| Belly apex, external radius | 76.97mm | 76.97mm | 76.9659mm at Z=69.00mm |
| Belly apex, height (as % of 160mm) | ~43–44% (plateau) | ~43–44% (plateau) | 43.12% (plateau spans Z=66.9–71.4mm, i.e. 41.8%–44.6%) |
| Wall thickness (belly/shoulder span) | ~4.00mm (3.98–4.03mm) | ~4.00mm (3.98–4.03mm) | ~4.000mm exactly at every sampled height Z=10–140mm |

All three genuinely different computational methods (a CAD kernel's own mass-properties query, a
mesh-integration on the exported STL, and a from-scratch numerical integral of the sampled
parametric surface) converge to within four significant figures on cavity volume — this is not
on shaky ground. **The 43–44% belly-height figure is the corrected, final number** — earlier in
this revision's resolution, ~50% was briefly and incorrectly reported as an intermediate figure;
that number is wrong and should not be used. The pre-edit v2 value (45%, Z=72mm) is also
superseded — it describes the belly's position before this edit, not the current geometry.

### Fresh overhang-angle check against the current (post-belly-edit) profile

`specs.md` §9 had explicitly flagged that its overhang analysis was computed against the pre-v4
profile and never recomputed after the belly edit. The Reviewer closed this out directly against
the live geometry (not requiring a dedicated Tester round-trip, though the director may want one
anyway given this body region's incident history):

- **Method:** continuous sampling of the entire outer-wall surface from Z=0 (base) to Z=160mm
  (rim) — stitching together all four outer-wall face patches at sub-millimeter resolution,
  computing local `dr/dz` at every step, searching the whole span (not just the previously-known
  trouble spot) for any zone exceeding the 45° guideline.
- **Result:** the **only** zone anywhere on the entire outer wall that exceeds 45° is the
  already-known, already-disclosed neck-to-collar external blend (Z≈145–152mm). Peak local angle
  there is now **47.25° at Z=147.25mm** — about 1.6° higher than the ~45.6° figure for the pre-v4
  profile, but the same location, same disclosed low-risk category, not a new site or new concern
  (§2.3, §2.4).
- **Belly region re-checked directly, not assumed still fine:** base→apex (Z=0–69mm) shows **zero
  locally-decreasing radius steps** across 1,382 sampled steps — genuinely monotonic, the outward
  flare never reverses. Apex→neck-taper-end (Z=69–145mm) stays negative (radius shrinking) at
  virtually every sampled point; the only positive-angle noise (123 of 2,016 steps, max 0.409°)
  sits at floating-point/sampling-noise level, concentrated at the broad, near-flat belly plateau
  where the profile is *supposed* to be near-zero slope — not a real reversal. **The belly getting
  bigger and moving slightly lower did not introduce a new overhang risk anywhere.**

### Documentation discrepancy found and corrected in this same pass

`specs.md`'s and this document's shoulder-OD row (122mm OD / 61mm radius at Z=119mm) had already
been flagged as "not independently re-verified... may be stale" before this pass — **confirmed
stale by the Reviewer's direct measurement.** The actual current radius at Z=119mm is **46.42mm
(≈92.8mm OD)**, roughly 30mm of diameter off from the previously-documented figure. This doesn't
change any pass/fail conclusion (cavity and material volumes were verified directly via
mass-properties/integration, never derived from this figure) but has been corrected in §1/§2
above so nobody designs against the stale number going forward.

### Business-fit re-confirmation

The original ~1474.8 cm³ figure was always framed as a **minimum**, not a fixed target (90 lb ×
1 in³/lb, deliberately sized to the top of the 50–90 lb range because oversizing capacity
slightly is preferable to undersizing it for cremated remains). Run back through the same rule
the requester chose, ≈1579 cm³ ÷ 16.3871 cm³/in³ ≈ 96.3 in³ ≈ 96.3 lb-equivalent capacity — still
comfortably describing the same "large, 50–90 lb" market segment, not a different bracket.
Nothing about the shape of the business case changed: same single-size large-pet urn, same plain
body and open-loop handle the concept brief calls load-bearing to its identity (both independently
reconfirmed unaffected by this round). **Conclusion: this is a deliberate, accepted +6.85%
increase in generosity, not a shortfall** — re-confirmed independently by the Reviewer, not just
carried forward on the Coder/Tester's informal say-so (`review.md` Addendum 3 §2).

### Concept-fidelity note — a real, incremental drift, named plainly

Comparing the refreshed render directly against the approved `concept/concept-v2.png`: **the
built design's belly-to-neck proportions now read noticeably more pronounced/pinched** than the
concept image's considerably gentler taper — a "ginger jar" silhouette with a distinct shoulder
pinch, rather than the concept's smoother, more gradual vase shape. This is an **incremental**
change layered on top of the already-disclosed "banded collar" drift (the collar's flat,
constant-radius band vs. the concept's fully continuous neck curve) named in the original review.

This is named plainly, not silently waved through, but it is **not** an undisclosed defect:
- The user directed this exact change with full awareness of its visual consequence (§10, step 1
  above — "a deliberate aesthetic decision... the user explicitly chose to keep it rather than
  revert").
- The concept brief's own words — "wider through the belly, tapering inward to a narrower neck" —
  are, if anything, *more* true of the current shape than of the original concept photo; this
  reads as an intensification of the same design language, not a departure into a different one.
- The two features the concept brief explicitly calls load-bearing to the design's identity (the
  plain undecorated body, the open-loop bail handle) are both fully intact and correctly
  proportioned, independently reconfirmed.
- The Reviewer's recommendation: a quick, low-stakes visual check-in with the requester (new
  render vs. `concept-v2.png`) is reasonable before treating this as fully final, purely as a
  courtesy confirmation that the more-bulbous look still reads as "right" now that it's built —
  not because the geometry needs to change.

### Render refresh

The pre-v4 hero render no longer depicted the shipped design (it showed the ~73mm-radius,
pre-edit belly). A fresh render was produced from the live, current geometry: the body's reverted
appearance was fixed (step 5 above), the lid's correct "Matte PETG - Stoneware Tan (urn-lid,
sanded)" appearance was confirmed intact, the lid occurrence was temporarily raised to its true
seated height (160mm) and made visible **for the render only**, then both changes were reverted
afterward (transform back to identity, visibility back to hidden) — the only permanent change
saved to the live document is the appearance fix. Saved to
`render/pet-memorial-urn-hero.png` (replacing the stale image); the pre-v4 render is preserved,
not deleted, at `archive/pre-v4-belly-render/pet-memorial-urn-hero.png`. Same honest caveat as
before: a faint background reference-grid overlay is visible and could not be fully suppressed
via the available API — a rendering-tool limitation, not a model defect.

### Cost impact

Despite the +6.85% larger cavity, the body's material (shell) volume **decreased** slightly, from
~293.4 cm³ (pre-v4, post-magnet-removal) to **~276.0 cm³** — the reshaped profile (fuller belly,
but a shoulder-to-neck taper that now converges noticeably faster) uses somewhat less total wall
material overall despite enclosing more internal volume. This round is a mild cost *improvement*,
not a tradeoff.
