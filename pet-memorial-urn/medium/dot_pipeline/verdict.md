# Verdict — Pet Memorial Urn, Medium size (v1) — Independent Verification Pass

## Overall: CONDITIONAL PASS — BLOCKED for production sign-off pending the neck-ID risk

**The CAD/manufacturing build itself is a clean, high-confidence PASS.** Every geometric,
topological, and dimensional check performed against the exported deliverables (STEP, 3MF, STL —
the live Fusion document was not accessible this session, exactly as anticipated in the task brief)
confirms the body, lid, and neck-fit-test article were built correctly and precisely to Medium's
own spec, with no cross-contamination from the concurrent Small-build session and no
mixing of Large's numbers into Medium's files.

**But this build cannot be signed off for a production print run**, because the spec's own
single highest-named risk — the 72mm neck/collar opening ID, tagged `ESTIMATED` and explicitly
flagged by the spec itself as a bigger compromise than Large's equivalent decision (72mm sits
*below* the real 79–89mm competitor cluster the spec's own research found for this capacity tier)
— has not been physically verified or explicitly risk-accepted in writing anywhere in this
project's files. Per the standing QA rule for this pipeline, this blocks default approval; it does
not get waved through just because everything else checks out.

---

## What passed (hard numbers)

| Check | Result |
|---|---|
| Body: manifold/watertight, no contamination | PASS (1 solid, Euler=2, correct topology) |
| Body: cavity volume | PASS — measured 806.1 cm³ vs. 819.4 cm³ target (−1.63%, within ±5% band) |
| Body: wall thickness at 5 control points | PASS — exact match to spec (3.2mm nominal, 8.0mm collar, 4.0mm floor) at every point checked |
| Body: overhang re-measurement, full profile | PASS overall; neck-collar blend confirmed at **44.98° peak**, right at the 45° guideline — real, confirmed watch-item, not a failure |
| Lid: manifold + sealed-void topology | PASS — confirmed independently at both STL mesh level and STEP B-rep level (`BREP_WITH_VOIDS` with a 3-face fully-closed void shell) |
| Lid: all dimensions (brim/dome/plateau/plug/cap) | PASS — every figure matches spec to sub-0.01mm |
| Plug/bore fit | PASS — boolean intersection = 0mm³ (collision-free), 0.5mm nominal diametral clearance confirmed, 4mm collision margin above the neck taper independently confirmed |
| `neck-fit-test-medium` dimensions | PASS — 72mm ID / 78.4mm neck OD / 88mm collar OD all measured exactly matching the body's own numbers |
| Document/file contamination | PASS — no stray components in any STEP/3MF/STL; every measured dimension matches Medium's own spec, clearly distinct from Large's (80mm ID/100mm OD/153.9mm belly) |
| Load test | PASS — static remains weight is trivial for this shell/floor |
| Slicer checks | Not performed — no slicer CLI available in this environment; substituted with direct geometric overhang/bridge measurement (see tests.md §8) |

## What did not pass cleanly / needs a decision

1. **BLOCKING — §4.3 neck ID (72mm), `ESTIMATED`, untested against a real remains bag.** This is
   the spec's own named top risk, made *larger* than Large's equivalent decision by the spec's own
   fresh competitor research (72mm sits below the entire 79–89mm cluster found for this capacity
   tier). **Route back to the Planner/requester — not a Coder or Tester fix.** Required before
   production sign-off: either (a) a physical pass/fail test of a real medium-pet remains bag
   through the printed `neck-fit-test-medium` article, or (b) explicit written risk acceptance from
   whoever requested this build, accepting that this dimension may require a future revision if the
   bag doesn't pass.
2. **Brim-to-collar fit (§7 of tests.md) — confirmed zero-clearance-margin condition (88.000mm =
   88.000mm exactly), not a hypothetical.** Not a hard failure — this is a deliberate v7 design
   identity choice the spec already names as a known risk — but flagged here as a *distinct* fit
   risk from the plug/bore interface (which does have real clearance), worth watching on the first
   physical print specifically for a tight/binding fit rather than assuming "matches on paper"
   means "fits in hand." **[SUPERSEDED by the RE-TEST PASS below — a fix was applied and
   independently confirmed 2026-09-09.]**
3. **Material choice for the body (PLA, 3.2mm wall) — thinner and equally brittle compared to
   Large's already-PLA body (4.0mm).** Not a spec violation (finish requirement explicitly calls
   for a PLA variant), but flagged per QA process as an unexamined-default risk: recommend PETG for
   the body if drop/impact resilience is prioritized over the exact matte "stoneware" finish, with
   the trade-off made explicitly rather than silently inherited from Large.
4. **PETG-lid/PLA-body shrinkage-mismatch risk at the plug/bore clearance** — named in spec, not yet
   mitigated by an actual printed test coupon as the spec itself recommends.
5. **Cost estimate revision (informational only):** real measured material volumes are ~15–26%
   higher than the spec's rough pre-build estimates (see tests.md §10) — not a functional issue,
   just an update for the record.

---

## Recommendation

Do not release this build for a full production print until item 1 above is resolved (physical bag
test or written risk acceptance). Everything else in this report is either a clean pass or a named,
non-blocking risk that can be decided by the Director/requester alongside item 1 — none of the
non-blocking items require re-opening the CAD model itself; the geometry as exported is a faithful,
precise, uncontaminated implementation of the Medium spec.

---
---

# RE-TEST PASS — Scoped Verification of Brim-OD Tolerance Fix (2026-09-09, v1.1)

## Verdict on this specific fix: PASS — correctly and cleanly applied

This is a **scoped re-verification**, not a full re-test (per task instruction). It covers only the
one change described in spec §5.1/§13 v1.1: brim OD reduced from 88.000mm to 87.700mm on the lid,
collar OD left unchanged at 88.000mm on the body. Findings were produced independently — by
re-measuring the actual exported STEP/3MF/STL geometry (text/entity parsing, XML vertex parsing,
mesh cross-section slicing, volume integration) — not by trusting the Coder's report or the spec's
own revision-history narrative.

| Verification item (from task) | Result |
|---|---|
| 1. Brim OD = 87.700mm on actual exported geometry | **CONFIRMED** — 43.850mm radius measured independently in STEP (`CYLINDRICAL_SURFACE`/`CIRCLE` entities), STL (exact-plane cross-section), and 3MF (raw XML vertex parse). All three formats agree; pre-fix archive confirms the prior value was exactly 44.000mm/88.000mm. |
| 2. Plug and dome geometry unchanged, bit-identical | **CONFIRMED** — full STEP-file diff shows the *only* substantive changes are the brim radius itself and one geometrically-dependent fillet (a torus tangent to the brim's outer edge, which correctly shifts by the same 0.15mm); everything referencing the plug (OD 71.5mm/wall 3.2mm/cap split) is completely absent from the diff. Independent STL cross-section re-measurement at the plug and dome control heights confirms the same values pre/post fix to within mesh-tessellation noise. |
| 3. Single valid manifold solid, watertight | **CONFIRMED** — STL: `is_watertight=True`, 2 correctly-structured components (outer shell + sealed void), same as before the fix. STEP: identical `BREP_WITH_VOIDS` structure (10-face outer shell + 3-face void shell), identical face/vertex counts pre/post fix. 3MF: single object/item, no contamination. |
| 4. Body and neck-fit-test files untouched | **CONFIRMED** — file timestamps unchanged (15:07, predating even the prior test pass) on all six body/neck-fit-test deliverables; independently re-measured body material volume (182.465 cm³) matches the prior pass's recorded 182.47 cm³; body collar OD re-measured at ≈88mm (unchanged, not narrowed to match the lid). MD5 hashes recorded in tests.md RT-4 for future audit. |
| 5. Material volume delta small, expected direction | **CONFIRMED** — independently measured STL volume delta = −0.228 cm³ (−0.18%), same direction as and same order of magnitude as the Coder's claimed Fusion mass-properties delta (−0.329 cm³); an independent analytic thin-ring sanity check (removing a ring at Δr=0.15mm over the brim's effective height) predicts ≈0.17–0.33 cm³, bracketing both measurements. |

**One non-blocking observation (not a fix defect):** the applied −0.15mm-per-side allowance sits at
the very bottom of the shop's own stated FDM tolerance range (±0.15–0.25mm/surface, per spec §5.3)
rather than comfortably inside it. The fix is applied correctly and exactly as instructed — this is
a note that the brim/collar interface should still be checked on the first physical print, with
reduced (not zero) risk, not a "resolved and can be ignored" status. See tests.md RT-6.

**This fix does not touch, resolve, or worsen the project's still-open BLOCKING item** (§4.3's
72mm neck ID, `ESTIMATED` and untested against a real remains bag — unchanged from the original
pass above). **Overall project status remains CONDITIONAL PASS — BLOCKED for production sign-off**
on that unrelated item; this fix itself is cleanly verified and closes out finding #2 in the
original verdict's "what did not pass cleanly" list.

---
---

# RE-TEST PASS — v2 Body-Profile Revision ("Thrown-Ceramic" Rounder Silhouette, 2026-09-10), Independent Verification (2026-09-11)

## Verdict on this revision: PASS — clean, accurately-executed rebuild; standing blocker unchanged

**Scope, per task instruction.** Independent, cold-start verification of the Medium body's v2
profile revision (`specs.md` §4.7): a rounder "thrown-ceramic" silhouette applied to the geometry
**below P3 only** (base, belly, shoulder). The lid, alignment plug, and `neck-fit-test-medium`
article were explicitly out of scope — confirmed untouched. Every figure below was independently
re-derived from the exported `urn-body-medium.{step,3mf,stl}`, not read from the Coder's own
reported numbers, using STEP entity-level parsing (the authoritative, tessellation-free source for
the highest-stakes claims), 3MF/STL mesh analysis, and a `git`/timestamp/md5 audit. Full detail in
`tests.md`'s "RE-TEST PASS — v2 Body-Profile Revision" section (RT2-0 through RT2-12).

**This is a clean pass on every one of the 12 items specified in the verification task**, with
several claims (G1 shoulder tangency, R6/R4 fillet tangency, P3-and-above identity) confirmed at a
higher level of rigor than mesh comparison alone — directly from the raw STEP B-rep/Bezier
control-point data, which is immune to mesh-tessellation noise.

| # | Item | Result |
|---|---|---|
| 1 | Single valid manifold solid — watertight, V−E+F=2, 0 non-manifold edges (STEP/3MF/STL) | **PASS** — confirmed exactly (V=56,158, E=168,468, F=112,312, V−E+F=2) in both STL and 3MF; STEP is a single `MANIFOLD_SOLID_BREP`/`CLOSED_SHELL` |
| 2 | Cavity volume — target 819.4 cm³, band 778.4–860.3 cm³; Coder reported 844.703 cm³ | **PASS, genuinely in-band** — independently measured **844.31 cm³** (+3.04%) via cross-section integration, cross-checked at 844.16 cm³ via an envelope-minus-material method; ~16 cm³ / 2% margin remains to the ceiling, not a near-miss. Method validated first against the known-good v1 body (805.91 cm³, bracketed by the original Tester's 806.1 and Reviewer's 805.30). |
| 3 | Base OD = 88mm (unchanged from v1); base OD ≥ collar OD, both 88mm parity | **PASS, exact** — both the base's flat cylindrical band and the collar's rim vertex trace to the *same literal* `44.` value in the STEP file; true bit-for-bit parity, not just numerically close |
| 4 | Belly max OD = 120.4mm, single point, zero overshoot | **PASS** — 0 of ~1,300 full-height samples exceed 60.2mm radius anywhere; STEP control point confirms a true single apex (r=60.2, z=59) with zero-slope tangent handles on both adjoining curves |
| 5 | Shoulder — tangent-continuous (G1), no kink (literal G2 not required, per task) | **PASS, rigorously confirmed** — raw Bezier tangent vectors at P2 are collinear to 5 significant figures on both the external and internal profile; slope at the junction (dr/dz=−0.35, 19.29° from vertical) matches the spec's own stated value almost exactly |
| 6 | Foot fillets — external R6, internal floor-to-wall R4, real torus faces, tangent | **PASS, exact** — confirmed directly from the two `TOROIDAL_SURFACE` STEP entities (minor radii 6.0mm and 4.0mm exactly), with analytic tangency to both the flat plane and the adjoining cylindrical walls confirmed via the major+minor=cylinder-radius identity |
| 7 | Overall height = 131mm exact | **PASS, exact** — mesh z-bounds 0.000000–131.000000mm in both STL and 3MF |
| 8 | Nominal wall 3.2mm radial through reshaped span; perpendicular min (Coder: ~2.71mm @ z~75) not below 0.8mm floor | **PASS** — radial wall confirmed 3.20±0.01mm throughout; independently measured perpendicular minimum **2.7107mm @ z=73.5mm** — matches the Coder's figure closely, confirmed not worse, and 3.4× clear of the 0.8mm floor. Also checked the collar-blend band separately for a hidden worse minimum — found none. |
| 9 | P3 and above byte-identical to v1 (collar bore 72mm ID, collar OD 88mm, neck OD 78.4mm, P3→P4 blend) | **PASS, at the highest available rigor** — the exact *set* of point radii present in the STEP file at z=119 (P3) and z=131 (P4) is identical, literal-for-literal, between v1 and v2; the shoulder-region radii correctly differ (confirming the comparison isn't a trivial false-positive). Mesh comparison corroborates: ≤18-micron residual differences at/above P3 (tessellation-level noise) vs. multi-millimeter real differences below P3. |
| 10 | Print orientation (base down, Z=0); overhangs — faired lower body (Coder: ~27.4°) and R6 foot-fillet underside (Coder: ~1.76mm below 45°) | **PASS** — lower-body peak independently measured at 27.39° (matches almost exactly); foot-fillet 45° crossing solved analytically from the exact torus geometry at z=1.757mm (matches to 3 sig. figs.). **Named, non-blocking finding:** this lower-body overhang is nearly double v1's (~16.4°) — still self-supporting, but a real, quantified cost of the rounder profile, not zero-cost. Also computed (not requested, but relevant): approximate tip-over angle drops from v1's ~40.2° to v2's ~35.8° as a consequence of the R6-fillet's smaller flat contact footprint (88mm→76mm) — still a comfortable margin for normal handling, but a concrete number rather than an unverified "still stable" assertion. |
| 11 | `urn-lid-medium.*` and `neck-fit-test-medium.*` NOT modified | **PASS** — `git diff --stat HEAD` is empty for all six files; timestamps unchanged (predating this revision); STL md5 for `neck-fit-test-medium` matches exactly across git HEAD, working tree, and the prior pass's recorded value |
| 12 | Standing item: 72mm neck ID remains `ESTIMATED`/untested | **Restated, not re-litigated** — unaffected by this revision (confirmed via item 9: everything at/above P3, including the entire neck/collar, is byte-identical to the already-blocked v1 geometry) |

## What this re-test does NOT change

**The project's overall status remains CONDITIONAL PASS — BLOCKED for production sign-off**, per
the original verdict above. The v2 body-profile revision is a purely cosmetic/silhouette rebuild
below P3; it does not touch, resolve, worsen, or otherwise interact with the standing blocking item
(§4.3's 72mm neck/collar ID, `ESTIMATED` and untested against a real medium-pet remains bag — see
item 12 above and the original verdict's item 1). **This routes back to the Planner/requester, not
a modeling fix, and remains gated behind either a physical `neck-fit-test-medium` bag test or
explicit written risk acceptance before any full production print of this body.**

## New findings from this pass worth carrying forward (non-blocking)

1. **Lower-body overhang roughly doubled by the rounder profile (16.4°→27.4° peak, still well under
   the 45° guideline).** Not a support-triggering change, but a real trade-off of the aesthetic
   revision — worth a visual check on the first print for layer-stepping quality on this now more
   sharply curved surface, distinct from the pre-existing neck-collar-blend watch-item.
2. **Approximate tip-over stability margin reduced from ~40.2° to ~35.8°** by the R6 foot fillet's
   smaller flat contact footprint (88mm→76mm diameter). Both figures represent a comfortable margin
   for normal handling and accidental knocks — this is not a functional concern — but it's now a
   quantified number rather than the spec's qualitative "still stable" claim, useful if a future
   revision pushes the base rounding further.
3. **No slicer available in this environment** (same limitation as every prior pass on this
   project) — recommend an actual slicer preview pass before production printing, specifically to
   visually confirm print quality on the new faired lower-body curve (not support necessity, which
   the geometry rules out at 27.4° peak).

## Recommendation

**Approve the v2 body-profile revision itself** — it is a faithful, correctly-executed
implementation of the approved rounder-silhouette mockup, verified independently to a high degree of
rigor with no modeling defects found. **Do not release the Medium build for a full production
print** until the pre-existing, unaffected §4.3 neck-ID blocker is resolved (physical bag test or
written risk acceptance) — this was true before this revision and remains true after it.
