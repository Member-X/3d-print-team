# Verdict — Pet Memorial Urn, Small (0–25 lb), First Test Pass

## Overall: CONDITIONAL PASS — CAD/manufacturing checks pass with high precision; blocked from
## final-material production printing on one unresolved, spec-flagged item.

This is a well-executed build. Independent re-measurement (not trust in the Coder's self-reported
numbers) found every geometric control point in specs.md §7.5 — internal and external radii at
P0–P4, wall thickness at 9+ sections, floor thickness, collar wall, brim/dome/plug dimensions on
the lid, and the fit-test article's neck/collar geometry — matching the spec to within mesh-facet
noise (typically ≤0.02mm, often exact to 4 decimal places). Cavity volume measured independently
via horizontal-plane integration landed at ≈412.2–412.4 cm³ against a 409.6775 cm³ target
(+0.6%, well inside the ±5% band). The neck-to-collar overhang, which the spec explicitly flagged
as a closed-form estimate needing confirmation, was independently re-measured by mesh slicing at
≈44.8°, matching the spec's 44.5° estimate within noise. All three parts are single valid manifold
solids; the lid's plug void is confirmed sealed (not a through-hole) by the absence of any boundary
edges in its mesh. The plug/neck clearance (0.5mm) and the 3.0mm collision margin above the internal
taper were both confirmed by measuring the real mating dimensions independently on each part, not
by trusting the stated numbers — both check out exactly. No sign of Medium/Large dimensional or
component contamination was found in any of the nine exported deliverable files (STEP/3MF/STL ×3
parts) — each contains exactly one correctly-named solid at Small-consistent dimensions.

**This does not mean the design is cleared to print in final material yet.**

## Why this is CONDITIONAL, not a clean PASS

1. **BLOCKING: the neck/collar ID (70mm) is tagged `ESTIMATED` in the spec and mates with a real
   external object (a small-pet crematorium remains bag) the team does not have in hand.** The
   spec's own research is real and reasoned, but it is still a compromise number, not a
   measurement. The spec itself names the `neck-fit-test-small` article as the mechanism to close
   this out physically, and I found no evidence that print-and-fit-check has happened, nor any
   written risk acceptance from the requester overriding it. **Per this team's own stated process,
   this routes back to the Planner/requester — it is not something a modeling fix or a re-measure
   can resolve, because the CAD is already an accurate build of the estimate.** Recommendation:
   print `neck-fit-test-small` now (it is small, cheap, and already dimensionally verified against
   the body — see tests.md §4) and check it against a real or realistically-mocked small-pet
   remains bag before committing the full body to a production print.

2. **Material choice for the body (PLA) is an unexamined default given a drop-risk / high-stakes-
   contents combination that the spec itself doesn't reason through.** The body wall is thinner in
   absolute terms than Large's (2.4mm vs. 4mm), and PLA's low impact toughness combined with an
   emotionally significant payload (cremated remains) makes a drop-induced crack a materially worse
   failure mode here than on a typical print. specs.md §10 already applies "PETG for toughness"
   reasoning to the lid; the same reasoning arguably applies more strongly to the body, which
   actually holds the remains. Recommend PETG (or ABS) for the body, or an explicit, informed
   sign-off from the requester if PLA is kept.

3. **The live Fusion document's internal browser tree (sketches, timeline, any suppressed/hidden
   bodies) was not independently inspectable this session** — the read-only Fusion tool available
   to me had no way to list a non-active document's contents or activate it for a screenshot. The
   exported deliverables (STEP/3MF/STL) show no contamination across all three parts and all three
   formats, which is meaningful evidence, but it is not the same guarantee as visually confirming
   the live document's tree shows exactly three items and nothing else. Someone with Fusion UI or
   write access should still do that specific check before treating the concurrent-access incident
   as fully closed out.

4. **Minor, non-blocking:** the lid's dome apex plateau built at 16.82mm diameter vs. the spec's
   derived ≈17.8mm target (−5.5%). Still comfortably printable (21× the 0.8mm floor vs. the spec's
   assumed >20×), not a functional defect, but worth a Coder-level look if a future revision cares
   about matching the derived ratio exactly.

5. **Slicer-level support/adhesion verification (settings actually applied, not just recommended)
   was not completed.** Bambu Studio is installed but did not yield usable CLI output in this
   session; I substituted direct geometric overhang measurement, which is more precise than a
   slicer's default heuristic for the overhang-angle question, but does not confirm that the
   spec's required "supports: touching build plate only" setting (§9.3, critical for the lid's
   sealed void) has actually been applied in a real slicer project. This is a manual pre-flight
   check that must still happen before the lid is sliced for real.

## What does NOT need further work

The dimensional/topological/fit engineering on all three parts is sound and precisely matches the
spec. If the neck-ID risk is resolved (physically, or by written risk acceptance) and the material
question is decided, there is no CAD rework indicated by this pass — the geometry is correct.

## Routing

- Item 1 (neck ID) routes back to the **Planner/requester** — this is a spec-risk decision, not a
  modeling defect. Explicitly named as such per this team's own honesty convention (specs.md §14).
- Item 2 (material) routes back to the **Planner/requester** for a decision — not a modeling defect.
- Item 3 (live-document inspection) needs a human with Fusion UI access, or a future agent with
  write/activate permission on the Fusion session.
- Item 4 (plateau size) is optional Coder-level polish, not required before printing.
- Item 5 (slicer settings) is a manual step for whoever runs the actual slice — flagged so it isn't
  silently skipped.

---

# RE-TEST PASS — v2 Body-Profile Revision ("thrown-ceramic" rounder body + narrowed base), 2026-09-10/11

## Overall: PASS on this revision's own scope (body-profile geometry). Every standing item from the
## first test pass above is unchanged, still open, and still applies — this re-test does not close
## any of them out, and does not need to: none of them are affected by a body-profile-only revision.

**Scope of this verdict.** specs.md §7.7 (v2) reshaped the body **below P3 only** — a rounder
belly/shoulder profile, new R5 external / R3 internal foot fillets, and a base OD narrowed from
90mm to 85mm. Lid, plug, and `neck-fit-test-small` were explicitly not touched and were independently
confirmed unchanged (see tests.md R11). This verdict covers only the rebuilt `urn-body-small.*`
files, cold-start, against specs.md §7.7 and the archived pre-v2 body as a diff reference.

**Every check requested for this re-test pass came back PASS, independently confirmed rather than
taken from the Coder's report:**

- **Single valid manifold solid** across STEP (1 solid/1 shell), 3MF (1 object, 0 components), and
  STL (0 non-manifold edges, V−E+F=2) — confirmed watertight in all three formats.
- **Cavity volume ≈395.93–395.99 cm³** by two independent, mutually-agreeing methods — **−3.35% vs.
  the 409.6775 cm³ target, genuinely inside the 389.19–430.16 cm³ band**, matching the Coder's
  395.979 cm³ to within 0.02 cm³. One nuance worth carrying forward, not a failure: the real margin
  to the band's lower edge is ≈6.8 cm³ (1.65% of target), tighter than the ≈9 cm³ the spec's own
  hand-calc projected — fine as-is, but leaves less headroom than assumed if a future revision
  narrows the body further.
- **Base OD = 85.00mm, confirmed wider than the 82.00mm collar OD by an exact 3.00mm margin** — the
  base/collar hierarchy the spec exists to protect is intact, not inverted, independently measured
  at the foot's own vertical-tangent plateau (not a wider "max radius in the lower body" scan, which
  would incorrectly include the belly rise — see tests.md R3 for the measurement trap this caught).
- **Belly max OD = 98.00mm with zero overshoot anywhere in a full-mesh scan** — the apex is a broad,
  intentionally flat plateau (per the spec's own design goal), not a sharp single point, but it
  never exceeds 98mm.
- **Shoulder is smoothly tangent-continuous (G1), with a curvature trace so smooth it is
  effectively G2 in practice** — no kink, no spike, one gentle distributed inflection, exactly as
  specs.md §7.7 describes. The spec's own flagged risk (a curvature spike at P1 from the lengthened
  down-handle) was specifically checked for and **not found** — no Coder-level fix was needed.
- **Both foot fillets (R5 external, R3 internal) confirmed as real STEP `TOROIDAL_SURFACE` BREP
  faces** with major/minor radii matching the spec exactly (37.5/5.0 and 37.1/3.0), independently
  cross-checked a second way by blind-fitting circles to the mesh profile — both methods agree to
  ≤0.01mm and both are tangent to their neighboring faces.
- **Overall height = 75.7000mm exactly.**
- **Nominal wall = 2.4mm confirmed through the entire reshaped span** (2.398–2.402mm, effectively
  exact), with the one disclosed, non-blocking, safe exception in the belly-rise zone (P0→P1): a
  localized peak of 2.72mm (Coder reported ~2.69mm — the real peak is slightly higher, i.e. even
  safer), never dropping below nominal anywhere in that span.
- **Minimum perpendicular wall thickness on the steepest section (the shoulder, ≈30.6° from
  vertical): 2.065–2.071mm by two independent methods**, matching the Coder's reported ~2.07mm
  almost exactly and sitting at 2.6× the 0.8mm print floor — confirmed not worse, and not a new
  risk.
- **P3-and-above is confirmed geometrically identical to the archived pre-v2 body** — worst
  deviation found anywhere from z=66.7mm (P3) to z=75.65mm (rim) across six sampled heights was
  0.0097mm, which is mesh-tessellation noise between two differently-tessellated STL exports, not a
  real geometry change. The neck ID (70mm), neck OD (74.8mm), collar OD (82mm), and the P3→P4
  external blend are untouched by this revision, confirmed by direct comparison against an
  independently-verified-unmodified archive copy, not assumed from the spec's claim.
- **Print orientation (base-down, Z=0) is baked into both STL and 3MF with no residual transform.**
  Overhang re-measured directly: the faired lower body peaks at 23.68° from vertical (matches the
  Coder's reported ~24° almost exactly), the R5 foot-fillet underside dips below the 45° guideline
  for only its bottom ≈1.5mm (matches the task's own framing exactly, routine for any rounded
  base), and the pre-existing, unaffected P3→P4 neck-to-collar blend peaks at 44.41° — all under the
  45° support threshold, none of them new or worsened by this revision.
- **`urn-lid-small.*` and `neck-fit-test-small.*` confirmed untouched** by two independent signals:
  `git status` shows no changes to those files, and their filesystem timestamps (2026-09-09 15:00)
  predate the body's rebuild (2026-09-10 16:22) — not merely assumed from the spec's own claim that
  the Coder "rebuilds only the body."

## What this re-test does NOT change or resolve

**This is a geometry-correctness pass on a profile revision that was explicitly scoped to
below-P3 only. It has no bearing on, and does not move the needle on, any of the five standing
items from the first test pass above — all five remain exactly as they were:**

1. **Still BLOCKING: the 70mm neck ID remains `ESTIMATED` and untested against a real small-pet
   remains bag.** This revision provably does not touch that geometry (P3-and-above confirmed
   identical to v1, see above) — so it neither resolves nor worsens this risk, but it also does
   nothing to close it out. **The physical `neck-fit-test-small` print-and-check is still required
   before the full body goes to production, exactly as before.** Restated per the task's explicit
   instruction not to re-litigate it, only to carry it forward.
2. **Body material (PLA) is still an unexamined default given the drop-risk / high-stakes-payload
   combination named in the first pass.** The v2 profile does not change the 2.4mm nominal wall or
   the material recommendation — the PETG-for-the-body recommendation from the first pass stands
   unchanged and applies equally to this geometry.
3. **The live Fusion document's internal browser tree is still not independently inspectable** with
   the tools available this session — unchanged tool limitation, not resolved by this pass.
4. The lid's dome-plateau minor deviation (item 4 above) is unaffected — the lid was not touched.
5. Slicer-level settings verification (item 5 above) is still an outstanding manual step.

## New process note from this pass (not a design defect)

During this re-test, a scratchpad script was overwritten mid-session by what was evidently a
different concurrent agent's analysis targeting the Medium build — a real cross-contamination risk
in how this session's shared scratchpad is being used across simultaneous Small/Medium/Large passes
(corroborated by the session's own git-status snapshot showing all three sizes' body files being
edited at once). This did not affect the correctness of this report — every number here was
re-derived from freshly-written, Small-only scripts against `pet-memorial-urn/small/...` paths,
double-checked against git status and file paths before being recorded — but it is worth the
Director/Coordinator's attention as a session-hygiene issue independent of this build's result.

## Routing

- **The v2 body-profile revision itself: no further Coder action needed.** Every geometric target
  in specs.md §7.7 was independently confirmed built correctly, including one contingency check
  (the P1 curvature-spike risk) that was specifically looked for and not found.
- **Items 1–5 from the first test pass are unchanged and route exactly as they did before** — item 1
  (neck ID) and item 2 (material) to the Planner/requester; item 3 (live-document tree) to a human
  with Fusion UI access; item 4 (plateau) is optional polish; item 5 (slicer settings) is a manual
  pre-flight step.
- **New:** the scratchpad cross-contamination observation routes to the Director/Coordinator as a
  session/process note, not to the Coder or Planner for this build.
