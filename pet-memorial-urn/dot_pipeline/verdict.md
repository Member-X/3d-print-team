# Verdict — Pet Memorial Urn (Large, single-size build)

## Overall (original pass): FAIL — blocked from Reviewer, one concrete defect + one unresolved risk to close out

Not a rejection of the design or the Coder's overall work — most of what was tested holds up
extremely well under independent verification, including the one item flagged as highest-risk
(the 54.5° taper). But there is one real, previously-undisclosed geometric defect in the body
that must be fixed and re-exported before this proceeds, plus one named risk that needs a
decision rather than silent carry-forward.

## Blocking (original pass)

1. **Unintended base pockets (`tests.md` §11).** Three 6.2mm-diameter, 2.2mm-deep circular
   pockets were found molded into the underside of the body's base, at the exact same
   radius/spacing/size as the legitimate collar magnet pockets — almost certainly a
   duplicated/mis-applied pattern feature, not an intentional design element. Confirmed
   present in both the STL and the actual slicer-ready 3MF, not an export artifact. This
   undermines first-layer bed contact on the one surface most responsible for print stability,
   and thins the floor exactly where drop-impact loads concentrate. Not called for anywhere in
   the spec, and not among the Coder's disclosed delegated-authority deviations — reads as a
   genuine modeling mistake. **Send back to the Coder**: find/remove the errant feature,
   re-export all three body formats (STEP/3MF/STL). The lid was checked with the same method
   and has no equivalent issue.

   **→ RESOLVED in the re-test pass below (R1). Independently re-verified fixed, not just
   accepted on the Coder's report. Re-confirmed fixed again after a full from-scratch rebuild
   in Re-test Pass 2.**

## Needs a decision (not a CAD defect, but shouldn't be silently treated as resolved)

2. **58mm neck opening vs. a real cremation bag (spec §4.4).** The spec itself already flags
   this as `ESTIMATED` and untested. I had no physical bag or bag-analog available to test
   against in this pass either, so it remains genuinely unverified. Given the object's purpose,
   this should get either a real test or your explicit written acceptance of the risk before
   this is called final — "the spec named the risk" isn't the same as that sign-off happening.

   **→ STILL OPEN, by design — this is exactly what the new `neck-fit-test` article
   (re-test pass, R5) exists to let you close out yourself. The CAD-side status of this risk
   is unchanged from the original pass: the physical test itself hasn't happened, and can't
   be run by a tester. What has changed is that a sound, correctly-dimensioned, printable
   test article now exists specifically to make that real-world test cheap and fast to do.**

## The item you specifically asked me to assess: the 54.5°-from-vertical taper

**Clear PASS — and I'd go further than "watch item."** I independently re-measured the actual
slope from the mesh (54.5–55.7° from vertical, confirming the Coder's number) and worked
through the print-orientation physics directly rather than just trusting the "closed revolve
tapers tolerate more" framing: this taper's radius *shrinks* as print height increases
(shoulder wide → neck narrow), which puts it in the same geometric category as a cone or
pyramid printed point-up. That category is self-supporting at *any* angle, not just angles
under some threshold, because every new layer sits entirely inside the footprint of the layer
below it — there's no unsupported span to bridge, ever. The 45°-from-vertical guideline
specifically describes the opposite case (radius growing with height, like a shelf). So this
isn't "probably fine in practice" — it structurally cannot produce the drooping/sagging
failure mode being worried about. I separately checked the *other* transition the Coder added
(the neck-to-collar blend, which does widen with height and is therefore in the real overhang
category) and confirmed it stays at 27–41° from vertical, safely under 45°. Both are solid.
No orientation change needed, no supports expected on the body's outer surface.

## Other specific call-outs you asked about (original pass)

- **1.9mm magnet pocket margin: solid, not a "barely clears the floor" situation.** I
  initially suspected the number might be an average masking an asymmetric thin spot (if the
  bolt circle had stayed at the pre-fix 33mm radius), but direct measurement confirms the
  pockets were re-centered to the true 34mm midline of the new 10mm-thick wall — margin is
  genuinely 1.9mm on both the inner and outer sides, for both the body collar and the lid.
  This is solid; no further pass needed on the margin itself. (Separate, minor, non-blocking
  point: verify actual magnet fit with a small test coupon before committing to a full print,
  since 0.2mm oversize is a printer-calibration-dependent convention, not something a CAD
  review alone can fully guarantee.)
- **Handle open-hole status: solid, independently confirmed, not just Coder self-report.** I
  swept the mesh across the loop's full depth (y = −8mm to +8mm) and confirmed a genuine
  through-channel open on both faces, sized ~22×24mm as claimed, with no material capping
  either end. No further pass needed here either.

## Material (original pass)

Recommend PETG for the lid specifically (handle root fillet + magnet pocket edges are
repeatedly-stressed/stress-riser features on a piece meant to last years) — this is a new
flag from me, distinct from the heat/UV risk the spec already discloses. Worth a quick
finish-vs-toughness conversation with the requester rather than defaulting to PLA everywhere
by default.

**→ The Coder has adopted this for the re-test pass. See below for my independent assessment
of that specific change — not a simple rubber-stamp of "recommendation accepted, therefore
fine."**

## Process notes (original pass)

Slicer settings (0.16–0.2mm layer height, 15–20% infill) and material (matte/silk PLA) are
confirmed **not** embedded in the 3MF files — must be set manually before printing. No
slicer was available in this environment, so overhang/adhesion conclusions above are
geometry-based, not confirmed by an actual sliced preview.

## What's genuinely solid here (original pass)

Internal cavity volume, bed fit, wall thickness, the plain-body constraint, the lid/body
seating-collision math, and the handle load case all independently checked out exactly as
claimed or better. This is a well-executed build with one concrete, fixable modeling defect
and one open real-world-verification question — not a design that needs rethinking.

---
---

# RE-TEST PASS — VERDICT

## Overall: PASS on everything re-tested. Blocking defect is fixed and independently confirmed.

## 1. Base-pocket fix (the item that blocked last time): PASS, independently confirmed

Re-verified using two methods, deliberately different from (and one of them more direct than)
the method that originally caught the defect, specifically because this is the one item where
I don't want to just trust that a Coder self-report of "fixed" on their own previously-caught
mistake is automatically accurate:

- A full cross-section sweep from z=0.05mm to z=5mm (covering the old defect's full depth plus
  margin) on the current `stl/urn-body.stl` returns a single boundary loop with **zero interior
  holes** at every sampled height.
- Direct inspection of the bottom-face vertices themselves (both STL and 3MF) shows the entire
  base cap is built from vertices at a single uniform radius (49.00mm, the base OD) with **zero
  interior vertices at all** — there's no leftover internal geometry of any kind on that face,
  not just "no holes found by one test."

Both the STL and the actual slicer-ready 3MF confirm the same clean result. **The base is a
genuine single flat plane with zero holes, exactly as claimed.** This item is resolved and
this specific block is lifted.

Noted for the record, not a new defect: the root cause (a scripted direct-BRep edit with no
owning timeline feature) is a process risk worth avoiding going forward, since it's exactly
the kind of change a normal timeline review would miss — that's how it got into a prior export
undetected in the first place.

## 2. Legitimate collar magnet pockets: PASS, spot-checked independently

Still present, correctly sized (6.2mm dia × 2.2mm deep), correctly positioned (34mm bolt
circle, 3-fold, 120° spacing), unaffected by the base fix — confirmed via direct measurement,
not assumed from the "untouched" claim. One methodology note for the record: my own
re-measurement of the *absolute* angular reference for these pockets differs slightly from the
original pass's numbers, traced to an artifact in how a mesh-slicing library I used computes
in-plane rotation for 2D cross-sections — doesn't affect any pass/fail conclusion, since the
functional claim (3-fold symmetric, self-aligning, no keying feature needed) holds regardless
of the absolute angle.

## 3. PETG-for-lid material change: my independent opinion — reasonable, but incomplete, not a rationalization

The Coder's claim that existing tolerances are "conservative enough" holds up for two of the
three things it cites (handle root fillet and wall thickness both get *better*, not just
"still fine," under PETG's superior toughness/layer adhesion), but I don't think it fully
holds for the magnet pocket oversize, and it doesn't address a real PETG-specific
printability consideration at all:

- **Magnet pockets:** 0.2mm oversize is a reasonable PLA convention, but PETG's greater
  tendency to string/ooze into small negative features means this allowance is tighter in
  practice for PETG than the same number is for PLA. Not blocking — it's a glue-assist
  post-print insert, not a precision press fit, so a tight pocket is fixable with a hobby
  knife — but I'd want a PETG-specific test coupon before committing the lid to a full print,
  the same recommendation already standing for the PLA body pockets.
- **Dome apex cooling/stringing:** the spec already flags a known, minor, cosmetic drooping
  risk at the lid's dome apex for PLA. PETG's higher extrusion temperature and slower cooling
  generally make this kind of artifact *more* pronounced, not less, at the same geometry — this
  is a genuine PETG-specific risk that a "tolerances are conservative enough" argument doesn't
  cover, because it's not a tolerance question at all, it's a thermal/cooling-behavior
  difference between the two materials. No geometry change is needed (the Coder isn't wrong
  that the *shape* is fine) — but whoever slices the PETG lid should expect to tune
  cooling/speed settings there rather than assume PLA-tuned defaults transfer unchanged.
- **Bed adhesion/orientation:** no reservation here — the lid's flat-underside-down
  orientation is if anything the best-case orientation for managing PETG's stronger bed
  adhesion/warping tendencies, so nothing needs to change for that reason.

**Bottom line: this isn't a rationalization to reject outright, but it's not fully complete
either.** Recommend a PETG test-coupon check on the magnet pocket specifically, and a heads-up
to whoever slices the lid about apex cooling settings, before treating "no changes needed" as
the final word.

## 4. `neck-fit-test` physical test article: PASS, sound and ready to print

Independently verified: single watertight manifold solid, correct topology for an open-through
tube (both ends genuinely open, not a blind cup), ID confirmed exactly 58mm and OD confirmed
exactly 78mm (collar) / 66mm (neck) — matching the claims precisely, not approximately. Fully
self-supporting in its natural flange-down orientation (the added stabilizing base flange is a
sensible, non-scope-creep addition for print stability, and it doesn't disturb the represented
ID/OD or introduce any new overhang beyond the already-validated ~40° neck-to-collar blend).
Correctly bed-centered, trivially fits the build volume. **This is a sound, printable article,
ready for you to actually print and use for the physical go/no-go decision on the neck
opening.** (Whether a real bag actually passes through it is your test to run, not something a
tester can verify — my scope here was confirming the test article itself is geometrically
correct and printable, and it is.)

## 5. Viewport tidy: confirmed non-issue

Independently re-measured bounding boxes of `urn-body.stl`, `urn-lid.stl`, and
`neck-fit-test.stl` (plus the two re-checked 3MFs): all are correctly centered at (0,0) in XY
and start at Z=0, with no offset leakage from the Fusion viewport rearrangement. Confirmed,
not just accepted on the Coder's word.

## What's still outstanding (not new, carried forward)

1. **The neck-opening-vs-real-bag physical test itself** (named risk #2 above) — unchanged
   status, still requires you to actually run it (or explicitly accept the risk in writing)
   before the full body print is treated as final. The new test article makes this cheap to
   do; it doesn't substitute for doing it.
2. **Magnet fit test coupons** — recommended for both the PLA body pockets (original pass) and
   now specifically for PETG lid pockets (this pass) before committing to full production
   prints, since FDM hole sizing is printer/material-dependent and wasn't slicer-verified in
   either pass.
3. **Slicer settings/material metadata** — still not embedded in any 3MF; must be set manually
   (0.16–0.2mm layer height, 15–20% infill, plus now PETG-specific temp/cooling settings for
   the lid) before printing. No slicer was available in either pass to confirm this by an
   actual sliced preview.

## Is this build ready to move to the Reviewer?

**Yes, with the above three items carried forward as open follow-ups rather than blockers.**
The one item that blocked this build last time (the base-pocket defect) is fixed and
independently confirmed fixed by a method distinct from how it was originally caught. Nothing
newly introduced this round (PETG lid, neck-fit-test article, viewport tidy) failed
verification or introduced a new geometric defect. The remaining open items are real-world
verification steps (the bag fit test, magnet fit coupons) and slicer-setup reminders — none of
them are CAD defects, and none of them are things a tester can close out without a physical
printer and physical hardware in hand. **This is ready to proceed to Reviewer** on that basis;
the neck-fit-test result and magnet coupon results should still be run by you before the full
body is committed to its long final print, but that's a print-house/requester action, not a
gate on the Reviewer step itself.

**Note: this "ready for Reviewer" verdict applied to the v1-derivation body geometry current
at that time. specs.md §4.2 was subsequently revised (belly position, spline profile) and the
body was rebuilt from scratch — see Re-test Pass 2 below for the current verdict on the body
that actually ships.**

---
---

# RE-TEST PASS 2 — VERDICT (urn-body rebuild: belly position + spline profile)

## Overall: PARTIAL PASS — belly position and volume are solid; the internal-profile smoothness fix genuinely worked; but a real, undisclosed smoothness defect was found at the neck-to-collar blend that should go back to the Coder before this is called fully resolved.

This is not a rejection of the rebuild — the two hardest parts of this round's mandate (moving
the belly to the correct height, and replacing the old frustum-stack with a genuinely smooth
internal profile) were both done correctly and I can independently prove it, not just repeat
the Coder's math. But the specific instruction to give real scrutiny to the smoothness claim,
rather than accept "the math checks out," turned up something real: a hard-edged, two-corner
straight chamfer sitting directly below the rim, in the one part of the body that wasn't
covered by the officially-respecified internal-profile spline.

## 1. Belly position: clear PASS

Independently re-measured via dense ray-casting on the actual mesh: peak external radius is
**exactly 73.000mm at exactly z=72.0mm — 45.00% of the 160mm total height**, matching the
Coder's figure exactly. Also did the direct visual comparison against `concept-v2.png` that a
prior round of this same project skipped (that omission is literally why this whole rebuild
exists) — took live screenshots of the actual current Fusion body and compared the silhouette
by eye: the belly reads as clearly low and wide in both, consistent with the concept's
proportions, corroborating the exact numeric result. **No reservations on this item at all.**

## 2. Smoothness fix: split verdict — real success on the profile, real defect at the collar blend

**The part that was hardest to get right — replacing the straight frustum-stack with a
continuously curved internal profile — genuinely worked.** I ran a curvature analysis (not a
visual impression) across the entire base→belly→shoulder→neck-taper span: exactly one sign
change in the radius slope, precisely at the belly apex where the spec's mandatory
zero-tangent condition requires it, and a smooth, continuously decelerating curve everywhere
else, including through the shoulder inflection the Coder specifically flagged as a
cusp-risk. This is a genuinely smooth, faceting-free profile, confirmed independently.

**But the neck-to-collar external blend (the last 15mm below the rim) is not smooth, and this
was not disclosed.** I found a literal straight conical chamfer between the end of the neck
taper (66mm OD) and the full collar OD (78mm), with two sharp, measurable corners — one where
the smoothly-decelerating neck taper meets the chamfer, and one where the chamfer meets the
flat collar cylinder. This isn't a borderline or subjective call: the slope is dead-constant
for the entire 7mm chamfer (confirmed at 0.1mm sampling resolution) and jumps discontinuously
at both ends, and it's visibly obvious as a diagonal crease line in a live screenshot of the
actual model — not something you'd need a caliper or a curvature plot to notice once you know
to look for it. The concept image's own neck-to-rim region, by contrast, is one continuous
soft curve with no comparable hard edge anywhere.

This region falls just outside the specific P0–P4 internal-profile spline the spec
respecified (that table is explicitly scoped to the internal bore) — the external collar
thickening is a separate feature, and it wasn't rebuilt with the same tangent-matched approach
that fixed everything else. Functionally this doesn't hurt printability (the chamfer's overall
angle, ~40.6° from vertical, is still under the 45° support guideline — see item 4 below), but
it directly undermines the stated purpose of this entire rebuild round in a highly visible
spot, right below the rim.

**Recommendation: send back to the Coder to apply the same tangent-matched blend/fillet
treatment to the neck-to-collar transition that was successfully used for the rest of the
profile, rather than the current straight chamfer.** This is a small, contained fix (one
transition, already-proven technique) — not a reason to question the rest of the rebuild,
which held up well everywhere else I checked.

## 3. Volume-vs-smoothness tradeoff: the right call, and correctly made at the Coder level — my real opinion, not just agreement

Independently confirmed the volume figure (1511.27 cm³ vs. the Coder's 1511.8 cm³ — matches to
0.03%), and confirmed the +2.3% deviation from target is real. My opinion: **this did not need
to go back to the Planner, and choosing curve quality over volume precision was correct.** The
spec text itself pre-authorizes exactly this tradeoff, explicitly, in writing, before the
rebuild even started ("flag back for a spec revision if it falls outside the band by more than
~5%") — 2.3% is well inside that pre-agreed tolerance, so this was an anticipated, bounded
decision, not the Coder unilaterally overriding a hard requirement. And volume already carries
an explicit tolerance band by design (it's a `DERIVED — sizing decision`, not a hardware-mating
dimension), while curve smoothness was the literal, named reason this rebuild round exists —
prioritizing the thing with no tolerance margin (visible curve quality) over the thing with an
explicit, pre-approved tolerance margin (volume) is the correct engineering judgment call, and
it's squarely within normal Coder-level implementation latitude. Worth noting: the smoothness
payoff this tradeoff bought turned out to be real (item 2 above confirms the shoulder itself is
genuinely smooth now) — it's a different, unrelated part of the geometry (the collar blend)
that still needs work, not this tradeoff.

## 4. Overhang re-check: the self-supporting reasoning still holds, independently re-verified on the new curve

Directly checked whether the new spline's curved shape (as opposed to the old straight
frustum) could hide a local bulge or reversal inside the P2→P3 shoulder-to-neck span that would
break the "shrinking radius = self-supporting regardless of angle" argument. It doesn't: I
sampled the actual radius at 0.25mm steps across the entire span and found **zero increasing
steps** — the radius decreases at every single measured point, including the one spot where
the local angle briefly exceeds the reported 47° average (54.5° at one point, matching the
same pattern already seen and accepted in this project's earlier build). Since the argument
depends on the *sign* of the radius change, not its magnitude, this holds at every point in the
span, confirmed directly rather than assumed by analogy to the old geometry. **No supports
expected on this transition, full stop — not "probably fine," structurally can't fail this
way.**

## 5. Base-pocket regression, collar magnets, manifold, lid, neck-fit-test: all re-confirmed clean

- **Base-pocket defect: still fixed after the full from-scratch rebuild** — re-ran the same
  independent checks (bottom-cap vertex inspection + cross-section sweep) and got the identical
  clean signature (uniform 49mm-radius perimeter, zero interior vertices) in both STL and 3MF.
  Worth recording for your files: the Coder's stated root cause this time — an unset
  `participantBodies` property on an extrude/cut operation defaulting to "all intersected
  bodies" and leaking a cut across unrelated components sharing a local origin — is a systemic
  risk for this shared multi-body file, not a one-off, and deserves a standing modeling-practice
  rule going forward, not just a closed incident.
- **Collar magnet pockets: unchanged and correct** — 3× 6.2mm dia, 34mm bolt circle, 120° apart,
  2.2mm deep, independently re-measured on the rebuilt body.
- **Manifold: confirmed** watertight, single connected component, correct topology. (The
  Coder's reported 14-face B-rep count isn't independently checkable from exported mesh files —
  noted honestly as unverified rather than assumed correct.)
- **Lid: confirmed untouched** — identical bounds/face count to the previously-verified state,
  file timestamps predate the body rebuild, no regression from the disclosed near-miss.
- **`neck-fit-test` article: confirmed still valid, agree it doesn't need regenerating** — its
  represented dimensions (58mm ID, 78mm/66mm OD) are unaffected by the profile revision, and I
  independently re-measured them rather than taking that on the Coder's word.

## Is `urn-body` ready for the Reviewer?

**Not quite — one more small round-trip to the Coder first, specifically for the neck-to-collar
blend (item 2 above).** Everything else in this pass is solid: the belly-position fix is exact,
the internal-profile smoothness fix is real and independently proven (not just mathematically
claimed), the volume is within an explicitly pre-authorized tolerance and the tradeoff that got
it there was the right call, the overhang reasoning holds up under direct re-verification, and
nothing regressed elsewhere (base fix, collar magnets, lid, neck-fit-test all check out clean).
But sending a body to the Reviewer with a known, visible, easily-fixable kink directly below
the rim — in the exact defect class this entire round of work exists to eliminate — isn't a
good use of the Reviewer's time. Once the collar blend gets the same tangent-matched treatment
already proven to work on the rest of the profile, and a quick re-check confirms that specific
7mm span reads as continuous, this should be ready to go. Everything else stands as-is; this
is a small, targeted fix, not a reason to revisit the rebuild as a whole.


---
---

# RE-TEST PASS 3 -- VERDICT (post-incident recovery: BodyProfile corruption + rebuild)

## Overall: PASS. The recovery is genuine and complete. `urn-body` is now ready for the Reviewer.

This closes out the one open item from Re-test Pass 2 (the neck-to-collar blend defect) and
confirms the incident/recovery didn't introduce any new problems or silently fail to restore
anything. Nothing here was accepted on the "matches before" claim without independent
re-derivation.

## 1. The headline question: is the neck-to-collar blend actually smooth now? Yes -- confirmed with the same method that caught it broken.

I re-ran the identical 0.1mm-resolution cross-section sampling that found the sharp two-corner
chamfer in Re-test Pass 2. This time the slope changes gradually and continuously across the
entire z=145-152mm span -- a real S-curve blend (easing in from the neck taper, through a
broad rounded middle, easing out into the flat collar), not a straight line between two hard
corners. The largest single-step slope change anywhere in this span is about a quarter of the
size of the instantaneous jump I measured last time at the exact same location. This is a
genuine geometric fix, not a re-assertion of the same claim -- I have no reservations about
this specific item anymore.

One minor, non-blocking observation: the new smooth curve's local peak angle (~45.6 degrees
from vertical) is marginally steeper than the old chamfer's average angle, which is normal and
expected when a tangent-matched curve replaces a straight chord. This is the same class of
"a few degrees past 45, on a continuously curved surface, typically fine with adequate
cooling" situation the spec already names elsewhere in this exact neighborhood -- not a new
concern.

## 2. Did anything else regress during the incident or recovery? No.

- **Belly position**: still exactly 73.000mm at exactly z=72.0mm (45.00%) -- no drift.
- **Internal profile (base/belly/shoulder/neck-taper)**: I compared actual sampled radius
  values against my own pre-incident measurements from Re-test Pass 2 point-by-point in the
  shoulder region and found exact matches to 4 decimal places -- this is stronger than "looks
  the same," it's numerically identical.
- **Cavity volume**: 1511.27 cm3, matching my own pre-incident measurement of the same figure
  to 5 significant figures, and matching the Coder's reported 1511.8067 cm3 to 0.03%.
- **Base cleanliness**: still zero pockets, same exact vertex signature as every prior pass.
- **Collar magnet pockets**: still 3x 6.2mm dia, 34mm bolt circle, 120 degrees apart, unaffected
  by the Extrude1 recreation -- specifically relevant since Extrude1 is the operation
  historically responsible for the *original* base-pocket defect earlier in this project, and
  it was recreated from scratch during this recovery with the participantBodies fix applied.
  No new leakage, no regression.
- **Manifold integrity**: single watertight solid, correct topology, unchanged bounds.

## 3. The "byte-identical to pre-incident" claim -- I could not verify this one specific claim, and I'm saying so rather than letting it pass by default

I do not have a stored hash or file size from the pre-incident export to diff against -- that
export (with the collar-blend fix already applied) happened in a round between my last pass and
this incident that I never independently captured. So the literal "byte-identical" claim is
outside what I can confirm.

What I can say with confidence: every geometric property I can independently derive from the
current files (cavity volume, shoulder-region radii, belly position, pocket geometry, base
cleanliness) matches my own pre-incident measurements exactly or within normal mesh-resolution
noise. I'd treat this as a stronger verification than a hash match would have been anyway -- a
hash only proves the file wasn't altered in storage, whereas independently re-deriving the same
numbers from the geometry itself proves the actual design survived, which is what actually
matters for a "did the recovery work" question. Flagging this distinction explicitly rather
than silently treating "I couldn't check the hash" as equivalent to "the geometry checks out,"
per the specific instruction to be honest about which of these two things was actually done.

## 4. Lid and neck-fit-test: confirmed genuinely untouched

No stored hash to compare against here either, but the evidence is about as strong as it gets
short of a hash: identical file size, at the identical to-the-second filesystem timestamp,
recorded independently in two separate prior passes, for both files -- and both timestamps
predate not just this incident but the entire collar-blend-fix round before it. The urn-body
files, by contrast, show a fresh timestamp and different sizes, consistent with "only the body
was touched." I'm confident these two files were not touched during the incident or recovery.

## Process note, worth carrying forward

This is the second time in this project that a direct/manual edit (as opposed to a
timeline-native parametric feature) has caused a real problem -- first the scripted
direct-BRep edit that caused the original base-pocket leakage, now a direct manual sketch drag
that broke BodyProfile entirely. Both times the Coder's recovery approach (rebuild from a
known-good state via the timeline, rather than trying to patch the broken state) was the right
call, and both times it fully worked when checked independently. But the pattern itself --
direct/manual edits bypassing or fighting the timeline being the recurring source of real
defects on this project -- is worth a standing note for whoever works on this file next:
prefer timeline-native parametric edits, and if a direct edit is unavoidable, treat it as a
higher-scrutiny change requiring an explicit before/after geometry check, not just a visual
glance in the viewport.

## Is `urn-body` -- and the project as a whole -- ready for the Reviewer now?

**Yes.** Every item that was open after Re-test Pass 2 is now closed: the neck-to-collar blend
is genuinely smooth (confirmed independently, not just re-claimed), and the incident that
happened since then did not leave any detectable damage anywhere I can check -- belly position,
internal profile, volume, base cleanliness, and collar pockets all independently re-verified
as unchanged from the pre-incident state, and the lid and neck-fit-test article were
confirmed untouched throughout. The only genuinely open items left on this project are the ones
that were always going to require the requester's own physical action, not further CAD
verification:

1. **The neck-fit-test physical print-and-check** (does a real/mocked remains bag pass through
   the 58mm opening) -- the test article for this was verified sound and ready to print back
   in Re-test Pass 1, and nothing since then has changed the collar/neck dimensions it
   represents.
2. **Magnet fit test coupons** (PLA body pockets and PETG lid pockets) -- recommended before
   committing to full production prints, since FDM hole sizing is printer/material-dependent
   and was never slicer-verified in any pass.
3. **Slicer settings** (layer height, infill, PETG-specific temps/cooling for the lid) --
   still not embedded in any file, must be set manually.

None of these three are CAD defects and none of them block the Reviewer step itself -- they're
real-world verification steps for the requester/print-house to run alongside or after review.
**`urn-body` and `urn-lid` are ready to proceed to the Reviewer.**


---
---

# RE-TEST PASS 4 -- VERDICT (second manual-edit incident: collar/neck dragged outward)

## Overall: PASS. Independently confirmed on all 5 requested checks. `urn-body` remains ready for the Reviewer.

This was scoped as a quick spot-check against a reproduction of an exact previously-verified
target, and it came back clean -- with an unusual degree of confidence, because several of the
re-measured values (shell volume, cavity volume, face/vertex counts, and spot-sampled blend
radii) came back **bit-for-bit identical** to my own independent measurements from before this
incident, not just "within normal tolerance." That's a stronger result than I typically get
even on an undamaged, unedited file, and it's good evidence this is a faithful reconstruction
from the same recipe rather than a coincidentally-similar rebuild.

1. **Collar ID/OD (the thing that actually broke): PASS.** Measured ~78mm OD / ~58mm ID at
   three separate heights within the collar band -- correctly restored from the reported
   ~90.4mm/~70.7mm ballooned state back to spec, not just "looks about right."
2. **Magnet pockets: PASS.** Full 6.2mm diameter, 34mm bolt circle, 120 degrees apart, 2.2mm
   deep -- not the abnormal ~3mm x ~1.9mm cuts the collar expansion had produced as a side
   effect. Base cleanliness (0 pockets) also unaffected.
3. **Cavity volume and belly apex: PASS.** Cavity volume matched my own pre-incident
   measurement to every floating-point digit; belly apex still exactly 45.00% of height.
4. **Neck-to-collar blend: PASS, confirmed intact.** The fix from two rounds ago was not
   disturbed by this targeted recovery -- same smooth, discontinuity-free slope profile,
   spot-checked at the same z-values I used in the last pass with matching results.
5. **Manifold: PASS.** Single watertight solid, correct topology, unchanged bounds.

Lid and neck-fit-test files independently confirmed untouched (identical byte sizes and
identical filesystem timestamps to every prior recorded measurement) -- consistent with the
Coder's claim that the lid was checked from scratch and found genuinely undamaged despite the
user's description of where the edit landed.

## Process note (third instance of the same pattern)

This is now the third manual/direct-edit incident on this project (scripted direct-BRep leak;
manual sketch corruption requiring a full profile rebuild; now a manual drag on the
collar/neck). Each time, independent re-verification confirmed the Coder's recovery was
genuine and complete, so the recovery process itself is working -- but the recurring root
cause (live manual edits in the shared Fusion document, outside the tracked timeline/spec
process) is worth surfacing as a standing risk to whoever owns this file, independent of CAD
concerns: every one of these incidents has been caught and fixed, but that's a testament to
verification discipline, not a reason to keep tolerating the underlying exposure.

## Is `urn-body` still ready for the Reviewer?

**Yes, unchanged from the prior pass's conclusion.** Nothing from this second incident left
any detectable damage anywhere checked. The same three items remain open as requester/print-house
actions rather than CAD blockers: the physical neck-fit-test print, magnet fit test coupons
(PLA body + PETG lid), and manual slicer settings. `urn-body` and `urn-lid` remain ready to
proceed to the Reviewer.


---
---

# RE-TEST PASS 5 -- VERDICT (magnet-assisted closure removed entirely, both parts)

## Overall: PASS. Clean, complete, well-executed subtractive change on both parts. No CAD round-trip needed -- but see the Reviewer-routing recommendation below, which is a real, specific finding, not a hedge.

1. **Manifold/watertightness -- PASS, independently re-run.** Direct edge-manifold check (every
   edge shared by exactly 2 triangles) on both STL exports and both 3MF exports: zero
   non-2-count edges anywhere, on top of the standard watertight/single-component/correct-Euler
   checks. Not accepted from the Coder's self-reported check.
2. **Body -- PASS on every sub-item, including the one most worth scrutinizing.** Collar OD/ID
   (~78mm/~58mm) confirmed unchanged at five sampled heights. The pocket removal is genuinely
   complete -- swept the entire 15mm collar band and found zero anomalous interior loops
   anywhere, and the top-of-collar cross-section that used to show 4 interior rings (bore + 3
   pockets) now shows exactly 1 (just the bore). Belly apex still exactly 45.00% of height.
   Neck-to-collar blend slope-continuity numbers are identical to the last two passes' figures
   to 4 decimal places -- completely untouched by this change, as expected. Cavity volume
   (1511.08 cm3) is within normal mesh-tessellation noise of both my own pre-change measurement
   and the Coder's claimed-unchanged figure -- the small (~0.05%) gap is explained by Fusion
   re-triangulating the whole B-rep after any feature-tree edit, not a real cavity-boundary
   change (I directly swept for cavity-boundary anomalies and found none).
3. **Lid -- PASS on every sub-item.** New volume plausible and in the correct direction (removing
   a blind pocket adds material). Handle through-hole re-confirmed genuinely open (22x24mm,
   present y=-4 to +4mm) via the same method used in every prior pass. Underside re-confirmed as
   a genuine plain flat plane with zero pocket remnants at any depth up to 2.75mm.
4. **No stray/orphaned geometry -- PASS, checked directly rather than inferred.** Zero interior
   loops anywhere in either part's formerly-pocketed region, both parts remain single connected
   components, both are fully edge-manifold. Nothing resembling the original base-pocket-leak
   defect.
5. **"Single-face-owned edge" claim -- investigated, assessed as benign, with an honest limit
   stated.** I can't inspect Fusion's B-rep topology directly from outside the application, so I
   can't confirm the CAD-kernel-level claim first-hand. What I can and did confirm: zero
   non-manifold edges in all four exported mesh files (STL + 3MF, both parts), and the
   `neck-fit-test` control body the Coder cited also shows zero -- strong, direct evidence this
   is a benign NURBS-seam artifact that does not translate into any real printability defect,
   stated as an assessment based on that evidence rather than a first-hand confirmation of the
   B-rep claim itself.

## Recommendation on Reviewer routing -- a specific finding, not a generic "check with Reviewer" hedge

**My own geometric/CAD verification above is complete and sufficient on its own terms -- this
does not need to go back through another Coder/Tester round-trip.** But I checked whether this
change is fully covered by the existing `dot_pipeline/review.md` approval before answering the
"does this need a fresh Reviewer look" question, rather than assuming either way, and found a
concrete gap:

**`review.md`'s own "Business fit -- PASS" section explicitly names the magnet-assisted closure
as one of its reasons for approval** ("a genuinely liftable, open-loop lid handle and a
**magnet-assisted (not airtight-dependent) closure** appropriate for remains that are already
bagged"). That feature no longer exists in the CAD. The review document's most recent addendum
(covering the third manual-edit incident, the collar-ballooning one) predates this magnet
removal entirely and doesn't mention it -- I confirmed this by reading the full addendum, which
still discusses "the magnet pockets" as a present, functioning feature throughout. So the
Reviewer has not yet seen this change in any form, and their existing approval record contains
a factually stale statement as a direct result.

This is different in kind from the incident-recovery passes I've done up to now (which were all
reproducing an exact, already-reviewed target after unintended damage). This is a genuine,
intentional, user-directed **scope change to the approved deliverable** -- removing a
customer-facing feature the original business-fit review specifically cited as a positive. Note
for the record: `README.md` and `parameters.md` are both already excellently updated to reflect
this change (I checked both directly) -- this is not a case of the Coder leaving documentation
stale. It's specifically `review.md`, the Reviewer's own record, that has not yet been updated,
and updating it is squarely the Reviewer's call to make (business-fit/concept-parity judgment is
explicitly their charter per their own document's structure, not a Tester's).

**Recommendation: route this to the Reviewer for a lightweight, targeted addendum -- not a full
re-review.** The geometry doesn't need re-verification (I've just done that thoroughly above);
what's needed is a business-fit sign-off that removing the closure mechanism is still consistent
with the approved concept brief, and an update to `review.md`'s stale business-fit sentence so
the project's own approval record doesn't silently misdescribe the shipped design. This is a
five-minute addendum for the Reviewer, not a reason to hold up printing -- but skipping it would
leave this project's own paper trail internally inconsistent in exactly the way this project has
otherwise been careful to avoid at every other step.


---
---

# RE-TEST PASS 6 -- VERDICT (fuller belly + wall rebalance + neck/collar crease fix)

## Overall: PASS. The geometry is sound and independently confirmed. But this needs a Reviewer touch before being called fully closed -- more clearly so than the last (magnet-removal) round did.

1. **Manifold -- PASS.** Watertight, single component, correct topology, zero non-manifold
   edges checked directly.
2. **Wall-offset tracking -- PASS, strongly confirmed.** Measured wall thickness at ~60 heights
   across the entire belly/shoulder span: 3.98-4.03mm everywhere, both walls peaking at the
   same height. This is a direct, positive confirmation the 13.3mm misalignment is genuinely
   fixed, not just reduced.
3. **Belly apex -- PASS on the number that matters (radius), with one correction worth
   making before this goes into documentation.** Radius confirmed to 0.013%. But the position
   is a broad, nearly-flat plateau (z~68-70mm, ~42.5-43.9% of height) rather than a sharp point
   -- the Coder's z=69.11mm falls inside that plateau, so it's not wrong, but I'd document this
   as a range/plateau rather than a single decimal figure. **More importantly: the incident
   summary's "~50% of height" does not match either the Coder's own figure or mine -- the real
   number is ~43-44%, meaning the belly actually ended up slightly lower than the pre-edit 45%
   target, not higher toward 50%. Please correct this specific figure wherever it lands in
   `specs.md`/`README.md`/`parameters.md`.**
4. **Neck-to-collar crease -- PASS.** Genuinely fixed at every resolution that matters for
   print quality or visual appearance (confirmed via the same method used in every prior pass,
   matching the previously-verified fix almost exactly). I also checked at a resolution about
   100x finer than this shop's planned print layer height, purely for completeness given how
   many times this exact region has needed rework -- found a small, sub-print-resolution
   irregularity right at the splice seam, noted honestly in `tests.md` but explicitly not
   treated as a defect, since it's roughly two orders of magnitude below anything an FDM
   printer or the naked eye could ever resolve.
5. **Collar dims, base cleanliness -- PASS, both unchanged**, as expected since neither was
   touched this round.
6. **Cavity volume -- PASS, independently confirms ~1579 cm3 as solid.** My measurement
   (1578.11 cm3) agrees with the Coder's (1578.9824 cm3) to within normal tolerance -- this
   number is not on shaky ground and can be treated as authoritative going into documentation.
7. **Lid -- PASS, confirmed genuinely untouched** via exact byte-for-byte file-size match to
   the last pass.

## Hard numbers to treat as authoritative for updating specs.md/README.md/parameters.md

| Figure | Value to use |
|---|---|
| Belly apex radius | **76.97mm** (both figures agree to 0.01%) |
| Belly apex height | **~43-44% of height** (z~68-70mm plateau) -- **not "~50%"**, correct this specific figure |
| Wall thickness through belly | **~4.00mm, holds 3.98-4.03mm throughout** -- tighter than the incident report's own worst-case 3.90mm figure suggested |
| Collar OD/ID | 78mm/58mm, unchanged |
| Cavity volume (new accepted capacity) | **~1579 cm3** (in³: ~96.3 in³, for reference against the original 90 lb/1in³-per-lb rule if that context is kept in the docs) |
| Material volume | ~276.0 cm3 |

## Recommendation on Reviewer routing -- yes, and more clearly so than the magnet-removal round

**This needs a Reviewer touch, and I'd put this recommendation on firmer ground than my
equivalent recommendation two rounds ago.** Two distinct reasons:

1. **The capacity/target number itself changed by an amount that crosses the spec's own
   pre-written tolerance threshold.** `specs.md` §4.2 explicitly says the Coder should "flag
   back for a spec revision if it falls outside the 1475-1478 cm3 band by more than ~5%." The
   prior accepted figure (~1512-1579, depending on which round) was already using up most of
   that headroom at +2.3%; the new figure is **+6.85% over the original target** -- a real,
   explicit crossing of a threshold this project itself wrote down as the trigger for exactly
   this kind of decision needing more than Coder-level sign-off. I recognize the user has
   already directly approved accepting the larger capacity rather than thinning the wall
   further -- this isn't an undisclosed defect, and I'm not second-guessing the user's decision
   -- but a written spec threshold being explicitly crossed, by design, is exactly the kind of
   event that should be reflected in a formal spec revision and a fresh look from whoever
   signs off on business fit, not just carried forward as an informal Coder/Tester
   understanding.
2. **`review.md`'s existing "Business fit -- PASS" section assessed the design specifically
   against the 90 lb / 1 in3-per-lb capacity target** -- the single most business-relevant
   number in this entire spec, tied directly to the requester's own sizing rule. That approval
   is now evaluating a capacity figure that's materially different from what's actually being
   shipped (roughly +7% larger than the target that approval was written against). This is a
   more substantive gap than the magnet-removal round's stale sentence -- that one was a
   single descriptive phrase about a removed feature; this one is the review's core
   business-fit math no longer matching the product.

**What I don't think this needs: another CAD/geometry round-trip.** The geometry itself is
sound, independently confirmed above, and doesn't need re-verification. What's needed is a
business-fit sign-off on the new capacity figure and a `review.md` update reflecting it --
plus, per the note above, this is also a good moment for whoever owns `specs.md` to log this
as a formal spec revision (a new row in §13) rather than letting the target quietly drift
across three different numbers (1477.8 -> ~1512 -> ~1579 cm3) purely through incident-recovery
narrative without a clean, single "this is the current target and here's why" statement.

## Process note (repeated, now a 4th instance)

This is the fourth time this exact body region (belly/neck/collar) has needed rework via a
manual edit -- three were unintended incidents, this one was a deliberate, user-directed
refinement, which is a healthier reason for a change but doesn't reduce the verification burden
each time. The recovery/verification discipline continues to hold up (every check above passed
independently), but the recurring need to touch this exact region is worth the director's own
attention as a pattern, separate from any single pass's CAD verdict.


---
---

# RE-TEST PASS 7 -- VERDICT (v5 major revision: neck/collar widened, height trimmed, lid resized)

## Overall: PASS. Every independently-checked dimension matches spec, at a level of precision (often to the third decimal place) that reflects genuinely careful execution, not a rushed rework. This needs a full fresh Reviewer pass, not a lightweight addendum -- more clearly so than either of the last two rounds.

## The four things you specifically asked about

1. **Cavity volume: PASS.** Independently measured **1579.31 cm3** vs. the Coder's claimed
   1580.25 cm3 (0.06% difference, well within this project's normal mesh-resolution tolerance
   band). This confirms the tangent-scaling tuning judgment call worked -- the spec's own
   hand-calculated estimate (~1578.6 cm3), the Coder's CAD measurement, and my independent
   measurement now all agree to within about 0.1% of each other and to within 0.08% of the
   ~1579 cm3 target. Given the first-pass construction reportedly came in 6.25% off before this
   tuning, landing this close on the second pass is a genuinely good outcome, not a lucky
   near-miss.

2. **Neck-to-collar overhang angle: PASS, with a striking independent cross-check worth
   highlighting.** I measured the peak angle at **45.56 deg from vertical**, close to the
   Coder's own independently-measured 45.81 deg -- both comfortably under the spec's ~47.25 deg
   estimate. More notably: my measured value is **numerically identical to 10 significant
   figures** to what I independently measured on the pre-widening (v4) collar blend two rounds
   ago. This isn't a coincidence -- it's a direct, unprompted confirmation of the spec's own
   geometric-invariance argument (same radius delta, same blend span, same construction method
   -> same curve shape, just relocated). When a spec's reasoning about *why* a number should
   come out a certain way is confirmed to floating-point precision by independent measurement,
   that's about as strong a validation as this kind of check can produce.

3. **Lid handle-hole integrity post-scale: PASS, verified directly.** This got specific scrutiny
   given the non-uniform scale operation. Swept the full depth of the loop and confirmed a
   genuine, unobstructed through-hole from y=-4mm to +4mm, measuring exactly 22mm x 24mm at
   center -- identical to every prior verified figure for this feature across the entire
   project. The scale operation (applied before the handle features, per the Coder's report)
   left this hard constraint completely intact.

4. **Overall: ready for the Reviewer.** See routing recommendation below for why I think this
   specifically needs a full pass rather than a targeted addendum.

## Everything else checked, in brief (full detail in tests.md R41-R52)

- **Manifold/watertight, all three parts, both STL and 3MF**: PASS, zero non-manifold edges
  found anywhere.
- **Belly apex unchanged by the height trim**: PASS, confirmed at the same absolute height
  (z~69mm, r=76.964mm) it held before this revision -- the trim genuinely came entirely from the
  belly-to-shoulder segment as claimed, not from the belly itself.
- **Shoulder, neck, collar dimensions**: PASS, matched to the third decimal place at every
  checked height. Notably, the shoulder's internal radius (42.42mm) -- flagged in the spec as an
  `ESTIMATED` figure needing Coder re-verification -- came back independently confirmed at
  exactly 42.420mm. **This should be upgraded from `ESTIMATED` to `VERIFIED` in the next spec
  pass**, closing out a flagged risk rather than leaving it open unnecessarily.
- **Base and collar-band cleanliness**: PASS, no pockets, no residual features from the resize.
- **Lid brim/dome dimensions**: PASS (122mm brim exact; dome base ~97.3mm vs. ~97.2mm target,
  close enough).
- **`neck-fit-test` article**: PASS -- correctly rebuilt at 80/88/100mm, single valid manifold
  solid, self-supporting in its print orientation. This is the file the requester will actually
  print, and it now represents the *right* geometry, closing the gap the spec explicitly warned
  about (an unrebuilt test article would have validated the wrong opening size).
- **File-location/path-bug check**: PASS -- searched the whole repo for stray copies, found
  none outside the canonical locations (aside from the already-accounted-for magnet-pocket
  archive from an earlier revision).
- **Base-vs-collar visual proportion**: PASS -- confirmed via a live Fusion screenshot, not just
  the dimensional check. The belly is unambiguously the widest, most visually dominant feature;
  base and collar read as comparably narrow at each end. Not top-heavy.

## Recommendation on Reviewer routing -- yes, and a full pass, not an addendum, more clearly than either of the last two rounds

Both of the last two rounds got a recommendation of "route to Reviewer, but a lightweight/
targeted addendum is enough" -- I don't think that's the right call this time. Three reasons,
in order of weight:

1. **This revision directly rewrites the spec's single most-discussed named risk.** The 58mm
   neck ID has been flagged as an untested `ESTIMATED` assumption since v1 of this spec, and
   this revision changes it based on real, new market/competitor research (not just an internal
   geometry tweak) -- the requester's own risk tolerance and business reasoning for choosing
   80mm over 100mm (to avoid exceeding the 98mm base OD) is exactly the kind of judgment call
   the Reviewer's business-fit charter exists to sign off on, not something that should close
   out purely on a Tester's dimensional-accuracy verification.
2. **The lid was substantially reworked, not just rescaled by a trivial amount.** Brim OD grew
   22%, dome base OD grew 21% -- this is described in the spec itself as "a real geometry rework
   of the lid, shown with the same rigor as the original lid derivation, not a cosmetic pass."
   A change the spec's own authors treat as equivalent in rigor to the original derivation
   deserves the same level of review the original derivation got, not a follow-up note.
3. **Scale of change, plainly:** this touches height, neck ID/OD, collar ID/OD, and both of the
   lid's two headline dimensions (brim and dome) in the same pass. That's a materially larger
   footprint than either of the last two rounds (a subtractive feature removal, and a capacity
   number update on an otherwise-unchanged silhouette). The director's own framing -- "the
   biggest single change to this file since the original build" -- already reaches the same
   conclusion I would independently: this is closer in scope to a second original build than to
   an incremental fix, and should get reviewed with the same rigor as one.

**What I don't think this needs: another CAD/geometry round-trip.** The geometry itself is
sound and precisely executed, independently confirmed above at every checked point. What's
needed is the Reviewer's business-fit judgment on the new opening size, the resized lid's
concept-fidelity (does a 122mm brim / 97mm dome still read as proportioned to the concept
image the way the 100mm/80mm version did?), and a fresh full pass through `review.md` reflecting
this revision -- not just a stale-sentence correction like the last two rounds needed.

## Process note (5th instance, now including a deliberate change alongside the incidents)

This is the fifth manual/direct-edit-related event on this file (a stray, cleanly-removed
fillet-feature pair this time, caught before the real work started -- not itself a defect that
made it into a shipped export). The pattern of this file needing frequent, careful
re-verification continues to hold up well under scrutiny each time, but the frequency itself
remains worth the director's attention as a standing risk independent of any single pass's
verdict.


---
---

# RE-TEST PASS 8 -- VERDICT (v6 candidate: lid-underside alignment plug)

## Overall: PASS on all 5 requested checks. The new internal-bridge finding is real and deserves a more honest risk framing than "cosmetic non-issue," but I agree it shouldn't block. Ready for the Reviewer.

## The 5 requested checks

1. **Collision-free against body's neck taper: PASS.** Plug tip lands at body-Z=143.5mm
   (10.0mm plug depth measured independently, subtracted from the body's independently
   re-confirmed 153.5mm rim height), body's internal taper begins at P3=138.5mm (also
   independently re-confirmed on the untouched body file) -- **5.0mm margin, confirmed using
   real measured geometry of both parts, not nominal-vs-nominal arithmetic.**
2. **Wall thickness: PASS.** Measured 39.750mm outer / 35.750mm inner at 10 sampled heights
   through the full 10mm depth -- constant 4.000mm wall, true cylinders, no taper. Exact match.
3. **Single valid manifold solid: PASS.** Watertight, 1 component, Euler=0, zero non-manifold
   edges -- confirmed independently on both the STL and the actual slicer-ready 3MF.
4. **Handle unaffected: PASS, verified directly.** Swept the loop's full depth and confirmed a
   genuine open through-hole from y=-4 to +4mm, exactly 22mm x 24mm -- bit-for-bit identical to
   every handle measurement across this entire project. Not trusted from "unaffected," directly
   re-measured.
5. **Clearance: PASS.** 80.000mm body bore ID minus 79.500mm plug OD = 0.500mm diametral,
   computed from real independently-measured geometry of both parts, matching the claimed
   figure exactly.

## The bridging risk -- my independent assessment, since this is the most important new thing to get right

**I don't think "cosmetic non-issue needing only a watch-item note" is the complete picture,
though I agree with the underlying conclusion not to block on it.** Two things need separating:
how likely is this bridge to print imperfectly, and does that actually matter.

**Likelihood: real, not negligible.** A 71.5mm-diameter unsupported horizontal span, even with
genuinely favorable full-perimeter anchoring, is well past the range FDM printing is commonly
considered reliably capable of bridging cleanly (community/vendor guidance for confident
bridging tops out around 40-50mm even for PLA). This lid is PETG, which bridges worse than PLA,
not better. I'd expect a visible sag and likely some stringing on the first bridging layer(s)
under default settings -- this is a real print-quality risk, not a low-probability edge case
being overcautiously flagged.

**Consequence: genuinely low, but for a more precise reason than "it's inside the neck."** The
surface is fully enclosed, permanently invisible once assembled, and structurally disconnected
from the plug's fit-critical OD and from any visible finish surface. A bad bridge here has no
functional or cosmetic consequence I can identify. **This is what actually justifies not
blocking -- not that the print will likely turn out fine, but that it doesn't matter if it
doesn't.** I'd recommend the design record reflect that more precisely than "cosmetic
non-issue," since the current framing risks someone reading it later as "this will print clean"
rather than "this may not print clean, and that's fine."

**One concrete, previously-unflagged risk worth adding to whatever slicer guidance ships with
this design:** if the operator's slicer has supports set to "everywhere" rather than "touching
build plate only," it may generate support material *inside* this sealed 71.5mm void that can
never be removed once the ceiling prints over it. Not a functional failure (inert, hidden,
disconnected from the urn's usable cavity), but a genuinely non-obvious gotcha specific to this
new feature -- worth a one-line callout: confirm "support on build plate only" before slicing
the lid.

**On whether a tilt angle would help both overhang zones at once: no.** The internal bridge
would benefit from tilting (a flat disc tilted past ~45 deg behaves like a self-supporting slope
instead of a flat span), but the outer support annulus is a discontinuous vertical step, not a
sloped surface -- tilting doesn't convert a literal step into a self-supporting slope. Worse,
any tilt large enough to meaningfully help the internal bridge would reintroduce overhang risk
on the dome and handle, both deliberately oriented flat-down specifically to avoid that. Trading
a hidden, consequence-free risk for a new risk on visible geometry is the wrong trade.
**Recommendation: keep the flat, plug-tip-down orientation, and handle the internal bridge with
slicer settings scoped to that one layer band** (max cooling, reduced speed there) rather than a
whole-part tilt.

## Test-coupon recommendation -- agree, and would state the direction of risk more specifically

I agree a clearance-test coupon should be printed before committing to the full lid. I'd add:
FDM bores systematically tend to print slightly undersized and bosses/plugs slightly oversized
relative to nominal CAD dimensions -- meaning the realized clearance is more likely to end up
**tighter than the nominal 0.5mm, not looser**. Combined with the already-named PETG/PLA
shrinkage-mismatch risk, this is a directionally-biased risk worth stating plainly, not a
generic "always test your fits" disclaimer.

## Is this ready for the Reviewer?

**Yes.** All 5 geometric checks pass with exact or near-exact matches to spec, the plug is a
clean, well-executed, purely-additive change that doesn't touch anything else in the design
(body, neck-fit-test, and every other lid feature independently confirmed unaffected), and the
one new risk worth real scrutiny (the internal bridge) has a low-consequence profile once
properly assessed, with concrete, actionable mitigations available (slicer settings, a
test coupon) rather than requiring a geometry change. This is a smaller-scope, single-feature
addition compared to the last two rounds (the v5 major revision and the magnet removal both got
"needs a fuller Reviewer look" recommendations from me) -- a targeted Reviewer look at this one
addition, informed by the bridging-risk framing above, should be sufficient here; I don't think
this needs the same full-pass treatment the v5 revision did, since it's additive-only and
doesn't touch any previously-reviewed dimension, proportion, or business-fit judgment.


---
---

# RE-TEST PASS 9 — VERDICT (v7 candidate: plug tip capped, handle removed, brim thickened+shrunk, dome apex flattened)

## Overall: PASS, ready for the Reviewer — with one real finding that should go back to the Planner/dome-owner as a decision, not be silently absorbed, and one pre-existing open item restated so it doesn't get lost in a five-change round.

This was treated as a full independent build, per the instruction that a five-change, 23-feature
rebuild deserves the same rigor as an original pass, not a spot-check. Full detail for every check
below is in `tests.md`, RE-TEST PASS 9 (R61–R71). This verdict summarizes the two items that
actually needed judgment calls, not just measurement.

## 1. Is the 2-connected-components finding a defect? No — confirmed correct three independent ways, including at the native CAD B-rep level, which is stronger evidence than a mesh-only check could ever provide.

This was named as the single most important thing to get right this round, so it got the most
scrutiny. Three independent checks, at two different levels of the data:

1. **Mesh-level** (`trimesh.split` on the actual shipped STL): 2 watertight components — an outer
   shell (+216.35 cm³) and the sealed plug void's own boundary (−24.07 cm³, magnitude matching a
   35.75mm-radius, 6mm-tall cylinder almost exactly). The negative sign is the expected signature
   of a correctly-oriented internal-void shell, not a topology error.
2. **B-rep level** (direct parsing of `step/urn-lid.step`'s actual entities, not the exported
   mesh): the file uses `BREP_WITH_VOIDS` — a STEP entity that exists *specifically* to represent
   one solid with internal void shells — with exactly one outer `CLOSED_SHELL` (10 faces) and one
   inner void `CLOSED_SHELL` (3 faces), totaling the claimed 13 faces exactly. `MANIFOLD_SOLID_BREP`
   (the entity used for a solid with no voids) does not appear at all. **The CAD kernel's own
   native classification of this part is "one solid with a sealed internal void" — this is not an
   interpretation being applied after the fact, it is what the authoritative CAD data says.**
3. **Differential check**: the archived pre-cap lid (`archive/pre-v7-handle-removal/urn-lid.stl`)
   shows exactly **1** component, because its void was open to the exterior through the
   then-unsealed tip. Capping the tip is precisely the change that should flip a design from
   1 component to 2 — and that is exactly what happened, confirmed on the real before/after files
   rather than reasoned about in the abstract.

**Judgment: this is settled. 2 components is correct, expected, and unavoidable for a correctly
sealed cavity in this geometry. I would not accept a re-litigation of this point without new
evidence — the STEP-level check in particular (finding `BREP_WITH_VOIDS` directly, rather than
inferring solid count from a mesh) is about as strong a confirmation as this kind of question
ever gets.**

## 2. Is the dome plateau-vs-height tradeoff math reasoned correctly? Partially — the arithmetic for the built geometry is right, but the framing of the tradeoff as unavoidable is wrong, and that's worth taking seriously.

Pulled the actual sphere and torus parameters directly from the STEP file (not from the spec's own
worked hand-calc, specifically to avoid checking the Coder's arithmetic against itself). Two
separate questions, two separate answers:

**(a) Given the sphere that was actually used (R=41.6667mm — confirmed via STEP, and confirmed to
be exactly the base-radius/point-apex-height sphere from *before* the flattening request, not a
value freshly derived for the new target set), does hitting a full 29mm height force the plateau
down to ~17.7mm? Yes.** Verified directly: this sphere's own raw (pre-blend) radius at the
29mm-height point is 9.07mm, and the built, blended plateau (8.85mm, confirmed two independent
ways) is a small, expected step down from that raw figure — this is a legitimate, correctly-
executed consequence of that specific sphere.

**(b) Is it true, as the spec states, that ~22mm plateau and ~29mm height are "not simultaneously
achievable on one spherical cap" at the 80mm base? No.** Solved the actual 3-target system (base
radius, height, plateau radius) for the sphere radius that satisfies all three exactly: **R =
41.4849mm — 0.44% smaller than the sphere that was used** — hits 80mm base, 29mm height, AND
22mm plateau simultaneously and exactly (verified by direct substitution, not just algebra). No
non-spherical geometry is needed. **The real constraint that was actually operating here was
"keep the existing, previously-verified sphere rather than re-derive and re-verify a new one" —
which is a legitimate, defensible engineering choice (lower risk, less re-verification work) —
but it is not the same claim as "the targets are mathematically incompatible," and the spec
currently states the latter.**

**My judgment on why this matters enough to raise rather than let ride:** the resulting shift is
not trivial — 17.7mm vs. the intended ~22mm is a real, visible ~20% shrink on a proportion that
was itself sized against an approved concept-comparison image specifically to "read as roughly a
quarter of the dome's base width." The actual built part now reads closer to a fifth. The fix, if
one is wanted, is cheap (a <0.2mm sphere-radius change, not a redesign) — which is exactly why I
don't think this should be silently absorbed as "the math made us do it." **Recommendation: this
goes back to whoever owns the dome-apex sizing decision as a named choice — keep the current
17.7mm plateau (fine, if made knowingly, since the built geometry is valid and self-supporting
either way) or take the cheap re-derivation to land closer to the originally-approved ~22mm
proportion. Either is acceptable; presenting it as if there were no choice is not.**

**This does not block this pass.** The built geometry is dimensionally accurate to what it claims
to be, smooth (max 12.6° facet angle, no real creases), and fully self-supporting (zero
locally-increasing-radius steps across a 390-point sweep). This is a documentation/reasoning
correction, not a geometry defect — but it's the kind of correction that changes what the next
person up the chain should be allowed to decide, so it's being surfaced explicitly rather than
filed away as a passed check.

## 3. Handle removal — clean, confirmed two independent ways

Component-count reconciliation (2 = 2, fully explained by the sealed-void finding above, no
unexplained third island) and face-inventory reconciliation (13 `ADVANCED_FACE` entities in the
STEP file = 6 planes + 3 cylinders + 1 sphere + 3 toruses, exactly matching the claim with nothing
left over). Both are structural, not visual, checks — a leftover handle/plinth fragment would show
up as an extra component or extra faces in either method, and neither shows one. **No orphaned
geometry. This reversal of a documented "hard constraint" is exactly what the requester directly
and explicitly confirmed (per `parameters.md` §6, `specs.md` §7), and is not being treated as a
defect** — only its clean execution was in scope for this check, and that's confirmed.

## 4. Fit and clearance — checked against the real mating part, not just re-stated

Re-measured the body's bore directly on the actual (untouched) body STL rather than reusing prior
numbers, since a fit claim always needs re-verification against the real current state of *both*
mating parts, not just the one that changed. Bore ID: 80.000mm constant through the full 15mm
engagement zone, still true post-v7 (as expected, body file unmodified — confirmed by timestamp
*and* by re-measuring its own independent dimensions, not timestamp alone). Clearance: 0.500mm
exact, collision margin: 5.0mm exact, both recomputed from two freshly-measured real numbers.
**No hardware/mounting-clearance class of issue applies here** — this design has no fasteners or
embedded hardware of any kind (magnets were removed project-wide back in v3); the plug/bore pair
is the design's only mating interface, and it passes.

## 5. Named risks correctly carried forward, one new low-severity documentation gap found

- The 71.5mm internal ceiling bridge and its trapped-support slicer gotcha: unchanged by capping,
  as the spec itself claims — independently re-confirmed (the void's floor is now solid, not open,
  exactly as of Z=4mm).
- The zero-tolerance-margin brim/collar flush edge (§5.1.1/§10 edge case 4): re-confirmed present
  and correctly disclosed; the 0.3mm negative allowance is a reasonable, transparently-reasoned
  mitigation, not an issue in itself.
- **New this pass: the spec's "10mm flat brim ring" corroborating check does not describe the
  actual built geometry** — the real transition from brim wall to dome is a smooth compound
  fillet with no flat annular shelf, confirmed both by a fine-resolution mesh sweep and by finding
  two additional fillet toruses in the STEP file exactly where a flat ring was claimed to be. This
  is cosmetic/documentation-only (the smooth transition is arguably *better* for print quality
  than a flat shelf with two sharp corners would have been) but should be corrected in the record
  so it isn't cited later as a verified visual proportion that isn't actually there.

## 6. Material — no change needed, one forward-looking caution recorded

PETG remains correct for the lid; nothing about v7 weakens that reasoning (if anything, the plug
and the now-sole-grip brim edge are both slightly more mechanically relevant than before, and both
favor PETG's toughness over PLA's brittleness). No action needed now — recorded for future editors
in case PLA is ever considered for cost/finish-matching reasons.

## 7. One usability observation, not a structural failure: removing the handle plausibly increases *how often* a drop happens, even though it doesn't change *how well the lid survives* one

The lid itself (solid PETG dome/brim, no thin unsupported features outside the already-disclosed
hidden internal bridge) should survive an ordinary drop without cracking. But gripping a smooth
dome by hand is less secure than a purpose-built handle loop, especially for an object handled
during an emotionally difficult task. This is a legitimate business-fit consideration for the
Reviewer, not something this pass is positioned to resolve (the handle removal was an explicit,
confirmed, user-directed override of the concept's own hard-constraint framing) — flagging it so
it's visible at the review stage rather than only living in a structural test log where it might
be read as "no concern at all."

## 8. Blocking-dimension check — restated, not newly resolved

The neck-opening-vs-real-remains-bag `ESTIMATED` risk (specs.md §4.4) is **unaffected by this
lid-only round and remains open** — no physical bag test has occurred. This is not new information,
but it is restated here deliberately: a five-change lid revision is exactly the kind of round where
a long-standing, unrelated open item could quietly stop being mentioned. It is not stopping this
lid pass, but it should not be treated as resolved by this pass's success either.

## Is this ready for the Reviewer?

**Yes**, with two items to carry forward explicitly in the handoff rather than leave implicit:
(1) the dome plateau/height framing correction (§2 above) needs a decision from whoever owns
apex-sizing — this is a "which of two valid options do we want" question, not a defect to fix
silently, and (2) the pre-existing neck-opening/real-bag risk remains open regardless of how well
this round went. Every other headline number in the v7 revision — plug geometry, brim dimensions,
total/combined heights, material volume, the 2-components question, and handle removal — checks
out cleanly against independent, from-first-principles verification, including direct native
B-rep inspection where mesh-only checking would have left more room for doubt.


---
---

# RE-TEST PASS 10 — VERDICT (scoped re-check: dome sphere radius fix, 17.70mm → 21.73mm plateau)

## Overall: PASS. The R65 finding from the prior pass is resolved correctly, not just patched. Ready for the Reviewer.

Scoped re-check, not a full re-run, per the request — this verdict covers only the dome-apex fix
and the invariants a sphere-radius change could plausibly disturb. Full detail in `tests.md`,
RE-TEST PASS 10 (R72–R75).

## 1. Did the Coder actually fix the thing I flagged, correctly?

Yes. The new sphere radius (**R=41.4849370254mm**, confirmed directly from `SPHERICAL_SURFACE` #16
in the re-exported STEP file) is bit-identical to the value I derived independently last pass by
solving the 3-target system (80mm base / 29mm height / 22mm plateau) — not an approximation of it,
the exact figure. Re-deriving from the new sphere placement independently: base radius at the
brim-top boundary (global Z=20) comes out to exactly 40.000mm, and the sphere's own raw,
unblended radius at the target height (global Z=49) comes out to exactly 11.000mm — meaning the
corrected sphere genuinely threads through the original target with no shortfall at the raw-curve
level. Any remaining gap from a literal 22.00mm is attributable entirely to the (now much smaller,
1mm vs. the prior 2mm) fillet, not to the sphere.

## 2. Is the tangency claim genuine, or just asserted?

**Independently verified genuine**, using a method that doesn't depend on trusting the Coder's own
sweep: a 390-point radius-monotonicity sweep (zero locally-increasing steps) and a facet-crease
detection pass (`face_adjacency_angles`) across the entire dome, which found a maximum facet angle
of 12.72° — statistically identical to the 12.64° found at the same unrelated location (the
brim-to-dome fillet) last pass, and nowhere close to the ~20-30°+ range that would indicate a real
kink. **No sharp transition appears anywhere near the new dome-to-plateau blend.** This is the
same crease-detection method I used last pass to independently confirm the *other* blend was
genuine, applied now to this one — consistent standard, consistent result.

## 3. Is 21.73mm (not exactly 22mm) the right tradeoff, given the spec's explicit tangency requirement? Yes — and it costs less than the framing suggests.

My independent read, since this was specifically asked for rather than a pass/fail:

- **The 22mm figure was never a tight target.** The spec itself calls it "an aesthetic judgment
  call... roughly a quarter of the dome's base width" and tags it `ESTIMATED` — there was no
  stated tolerance to weigh against tangency.
- **The tangency requirement is the one with real, named, print-quality teeth.** The spec spells
  out the alternative explicitly: a visible ~15° kink, and this project has direct history
  (§13 v2) of treating exactly this class of faceted transition as worth a full rebuild to fix,
  not a shrug. Preserving tangency here is consistent with that established standard, not a new
  or arbitrary bar.
- **The proportion the 22mm number was actually protecting is preserved almost exactly**:
  22/80=27.5% intended, 21.73/80=27.16% built — a gap smaller than what anyone could reliably see
  against the reference image the original figure was itself eyeballed from. **This is not "the
  Coder got close but had to compromise" — it's a resolution that hits the real design intent
  (the visual proportion) while correctly deprioritizing the specific decimal, which was always
  the softer of the two constraints.**

**My verdict: right call, cleanly executed, and the tradeoff was disclosed rather than hidden —
exactly the standard this project has held every prior revision to.**

## 4. Did anything else move that shouldn't have?

No. Checked everything a sphere-radius change could plausibly disturb: dome height (29.000mm,
unchanged, confirmed), dome base OD (80.000mm exact, independently re-derived from the new sphere
placement, not just carried over), total lid height and bounding box (39.000mm / 49.000mm,
unchanged), and the manifold/void signature (still 2 components, still `BREP_WITH_VOIDS`, still 13
faces in the same 6+3+1+3 breakdown, and the void's own volume is numerically identical to last
round — confirming the plug region genuinely wasn't touched, not just assumed unaffected because
it's a different feature). Material volume increased +0.92% as claimed, matching a same-method
mesh-to-mesh comparison against the prior round almost exactly (+0.915% measured). **This was a
genuinely scoped, single-parameter-family fix, not a broader change presented as a small one.**

## Is this ready for the Reviewer?

**Yes, with no new open items from this specific fix.** The R65 finding is now closed correctly —
not just patched to hit a number, but re-derived properly, with the underlying tradeoff (tangency
vs. exact diameter) reasoned through and disclosed rather than glossed over. The two items already
on record from RE-TEST PASS 9 remain open and are restated once more, unaffected by this fix: (1)
the "10mm flat brim ring" documentation-vs-as-built gap (cosmetic/documentation only), and (2) the
pre-existing, still-unresolved neck-opening-vs-real-remains-bag `ESTIMATED` risk, which no lid-only
change can touch. Neither blocks this pass.
