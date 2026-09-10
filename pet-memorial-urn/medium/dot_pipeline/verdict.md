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
