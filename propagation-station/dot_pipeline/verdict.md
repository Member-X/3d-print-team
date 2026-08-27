# Verdict — 2-Tube Hydroponic Propagation Stand (v4 spec)

## Overall: CONDITIONAL FAIL — blocked on an unresolved mating dimension, not on a modeling defect

**Geometry/modeling quality: PASS, cleanly, across every check performed.** Manifold/watertight
(both STL orientations, confirmed no trapped internal void independently of the Coder's own
earlier fix), all named wall thicknesses (base foot 8.00mm, side wall 8.5mm, land 6.03mm, ceiling
envelope 8.13mm), bore diameter (exactly 28.500mm, both bores, cross-checked at both the mesh and
STEP/BREP level), slant angle (exactly 30.000° from vertical in use orientation, exactly vertical
in print orientation, both bores matching to floating-point precision), overhang profile (exactly
one region, matching the pre-accepted tilted-base-foot underside, nothing else), and bounding box
(80×114.8×93.1mm, comfortable P2S-volume margin) all check out exactly as the spec claims, with no
drift introduced during modeling or export. Full detail in `tests.md`.

**But this is not enough to clear the part for production, because the model's core mating
dimension is built on a spec value that is still explicitly marked OPEN, not resolved:**

> Tube OD (27mm, → 28.5mm bore) is an ESTIMATE. §8 item 1 in the spec itself says: "No physical
> tube has been measured yet — still open." This is distinct from §8 items 3–5, which the product
> owner *did* explicitly resolve with a documented decision trail. Item 1 has no such resolution.

Per this pipeline's standing rule — block on an unresolved ESTIMATED dimension that mates with
real hardware rather than let it pass by default because nothing else looks wrong — **this is
called out as a blocker, not a footnote.** I quantified why the risk is sharper than the spec's own
text suggests: typical FDM hole shrink (~0.1–0.3mm undersized) would plausibly bring the effective
bore down to ~28.2–28.4mm, eating most of the already-thin 0.75mm/side design clearance before even
accounting for the ±1–2mm real-world tube OD variance the spec itself names in §7 edge case 1. A
tube at the higher end of that variance band would not fit the as-printed bore at all.

**This routes back to the product owner / Planner, not to the Coder.** There is no bore-geometry
bug to fix — the model is a faithful, dimensionally-exact realization of the spec's own (still
unverified) number. The fix is verifying the real tube (manufacturer spec sheet, caliper
measurement, or ruler-photo — per the spec's own §8 item 1 requirement) or the product owner
signing off in writing to accept the risk as-is, the same way they explicitly did for items 3–5.

## Secondary open item, same category, lower severity

The 30° slant angle is also still open per §8 item 2 (no physical fill test performed). The model
correctly implements exactly 30° in both bores and both orientations — that part is not in
question — but the angle *choice itself* (does it actually prevent spilling) is unvalidated. Lower
severity than the tube-fit issue because a wrong angle produces a usability disappointment
(spilling), not an assembly failure (tube physically won't fit); recommend combining this test with
the tube-fit verification in a single first physical print rather than treating them as two
separate follow-ups.

## Everything else: pass, with a few non-blocking recommendations

- `.3mf` export is geometry-only (no baked-in print profile), despite being described as a
  "slicer-ready project export...at the settings from §6.1/§9" — recommend regenerating from an
  actual slicer with settings saved, or correcting the file's description.
- Print-orientation file touches the bed along a knife-edge line (zero native contact area) before
  supports are generated — expected given the accepted tilt trade-off, but concrete enough that a
  brim + supports-enabled note should accompany the print file explicitly, not be assumed implicit.
- Recommend PETG over PLA specifically for this part's one mechanically-concentrated feature (the
  6mm land between the two bore openings, sitting between two sharp-cornered rim intersections) —
  a reasoned recommendation given PLA's brittleness under impact, not a re-litigation of the spec's
  otherwise-sound low-load/no-cyclic-flex reasoning.
- One-tube-filled X-axis tipping case (spec's own flagged edge case for the Tester to spot-check):
  confirmed safe by calculation, ~35mm margin against a 40mm half-footprint.

Full test-by-test detail, all measured numbers, and reasoning: see
`propagation-station/dot_pipeline/tests.md`.

---

## PROJECT HALTED — 2026-08-26

**Status: stopped by product owner, not resumed.** After the Tester's CONDITIONAL FAIL (unresolved
tube-OD mating dimension — see above), the product owner reviewed the three proposed paths forward
(verify a real tube, accept the risk in writing and proceed to review, or widen clearance as a
hedge) and declined all three, judging the design "not functional" as it stands. This is a decision
to stop, not a request for another design iteration.

**Where this leaves the project:**
- Geometry/modeling quality passed every check performed (manifold, wall thicknesses, bore
  diameter, slant angle, overhang profile, bounding box — see main verdict above and `tests.md`).
- The blocking issue was never a modeling bug — it was that this design was built end-to-end
  (spec through Coder through Tester) on an unverified tube OD (27mmm, ESTIMATED from a
  reference listing, never measured against a real physical tube), and the Tester's shrink/
  tolerance analysis concluded the resulting 28.5mm bore has too little real margin to trust
  without that verification.
- No further work (Planner, Coder, Tester, Reviewer) should be dispatched on this project unless
  the product owner explicitly asks to resume or revise it.

**If revisited in future:** the fastest unblock is still what §8 item 1 always asked for — a real
tube in hand (or a manufacturer spec sheet) to measure OD/length against, before any bore geometry
is re-cut. The 30° slant angle (§8 item 2) is unvalidated in the same way and should be tested
alongside tube fit on a first physical print, not separately.

All output files (STL x2, STEP, 3MF) remain at
`propagation-station/src/propagation_station/` in their last-built (91mm height) state, left as-is,
not deleted, in case they're useful as a starting point for a future revision.
