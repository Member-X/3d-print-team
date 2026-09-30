# Tests — Pet Memorial Urn (Large, single-size build)

Method note: independent measurement was done directly against the shipped mesh geometry
(`stl/urn-body.stl`, `stl/urn-lid.stl`, and `3mf/urn-body.3mf` for the base-pocket defect,
cross-checked so it's confirmed present in the actual slicer-ready file, not just the STL)
using `trimesh` — horizontal/vertical cross-sectioning, radial deviation analysis, and
volume/watertightness checks — not just re-reading the Coder's report. No slicer was
available in this environment, so supports/adhesion are assessed from geometry/overhang
math rather than an actual sliced preview.

---

## 0. Blocking check — unresolved ESTIMATED dimensions mating with real objects

Two items reviewed under this lens:

1. **Magnet pocket tolerance (6.2×2.2mm for 6×2mm N42 magnets, 0.2mm oversize, `ESTIMATED`).**
   Low risk: the magnet itself is a verified, commodity, tightly-toleranced part; the pocket
   has a glue-based backup retention method regardless of fit; and a bad fit is cheaply
   correctable at assembly time (more glue, or a shim) rather than a functional failure.
   **Not blocking**, but not yet verified either — recommend a small test-coupon print of
   one pocket + a real magnet before committing to a full production print, since FDM hole
   sizing is printer-specific and no slicer/print test was available in this pass.
2. **Neck opening (58mm ID) vs. the crematorium's actual sealed remains bag — spec §4.4,
   edge case 2.** This is the one genuine "mates with a real external object" dimension in
   this spec, and it is explicitly tagged as an `ESTIMATED`, untested assumption in the spec
   itself. **This has not been verified in this pass either** (no physical bag or bag-analog
   was available to test against). Per the tester mandate, this needs either a real test (a
   real or simulated cremation bag pushed through a 58mm ring mockup) or explicit written
   risk acceptance from the requester before this is treated as final — the spec surfacing it
   as a "named risk" is not the same as that sign-off happening. **Flagged, not blocking CAD
   work, but should not be silently carried forward as done.** (See the Re-test Pass below —
   a physical `neck-fit-test` article now exists specifically to let the requester close this
   out themselves; the CAD-side blocker on it is unchanged, this is still a requester action.)

---

## 1. Independent volume verification

Measured directly from `stl/urn-body.stl` via cross-sectional integration (slicing the mesh
at 300 heights from floor to rim and integrating the area enclosed by the inner wall boundary):

- **Measured internal cavity volume: 1472.65 cm³**
- Coder-reported: 1475.00 cm³ (0.16% higher than my measurement — consistent with normal
  slicing-resolution/fillet-sampling variance, not a discrepancy worth chasing)
- Spec target: 1475 cm³ (90 in³)

**Result: PASS.** Independently confirmed within 0.2% of both the Coder's figure and the
spec target. The 90 lb / 1 in³-per-lb sizing target is genuinely met by the real geometry.

Body material-shell volume (for weight estimation): 295.15 cm³. Lid material-shell volume:
150.82 cm³. Both meshes independently confirmed watertight/manifold via `trimesh`.

**Note (see the v2-rebuild Re-test Pass, R10 below): the body's internal profile has since
been re-derived and rebuilt from scratch against a revised spec — the figures above are the
v1 numbers, superseded, kept here for the historical record.**

## 2. Bed-fit check

Measured bounding boxes directly from the STL:
- Body: 145.6 × 145.6 × 160.0mm
- Lid: 100.0 × 100.0 × 75.0mm

Both clear the 256×256×256mm P2S bed by well over 90mm margin on every axis, matching spec.
**PASS**, independently confirmed, printed as two separate jobs so combined height is moot.

## 3. Wall thickness check

Measured outer-minus-inner radius at 14 heights up the body:
- z=90mm (belly max) through z=140mm (neck): **exactly 4.00mm**, matching the spec's nominal
  4mm wall precisely.
- z=10mm through z=80mm (base flare): wall thickness **increases** toward the base, from
  5.62mm down to 4.01mm — thicker than nominal, not thinner. This is a bonus, not a defect:
  it puts extra material exactly where drop-impact loads on a shelf-top object concentrate
  (the base).

**PASS.**

## 4. Overhang / print-orientation assessment (the flagged 54.5°-from-vertical taper)

**This is the headline question from the build report. Verdict: PASS — not a defect, and not
even really a risk once the print-direction physics is worked through, not just a "closed
revolve tolerates more" hand-wave.**

Independently measured the actual local wall slope from the mesh (not recomputed from the
spec's frustum math) across the shoulder→neck region: **peak measured angle 54.5–55.7° from
vertical**, confirming the Coder's number to within measurement noise.

The key point the "under 45° from vertical" framing misses: **the 45° overhang guideline
only applies to surfaces that get wider as printing height increases** (a shelf, a flare, an
inverted cone) — that's the case where a new layer extends into open air with nothing
directly beneath it. The shoulder→neck taper does the opposite: **radius shrinks as height
increases** (57mm → 29mm internal, wide-to-narrow, printed base-up). For a shrinking-radius
taper, every new layer sits entirely within the footprint of the layer below it — it is
mechanically identical to printing a cone or pyramid point-up, which FDM printers handle at
any angle, including angles far steeper than this one, with zero support material. This
isn't a special case that "commonly prints fine" — it's a geometry class that structurally
cannot have this failure mode, independent of the numeric angle.

I also independently checked the *other* taper the Coder introduced (the ~7mm neck-to-collar
blend, deviation #1 from the delegated-authority list) — this one genuinely does widen going
up (34.7mm → 39.3mm radius) and is therefore in the real overhang category. Measured local
slope there: **27–41° from vertical**, safely under the 45° guideline at every sampled point.
**PASS**, confirmed independently, not just taken on the Coder's word.

One minor, non-blocking watch item: the neck/collar region narrows to a small circumference
quickly, meaning each layer up there has a short layer time — on some printers/settings this
can cause minor overheating/blobbing at the very narrowest point. Standard "minimum layer
time" slicer settings handle this; flagging so whoever slices it doesn't need to rediscover
it if the layer surface finish looks slightly rough right at the narrowest neck point.

**Note (see R14 below): this exact question was re-asked and re-verified independently against
the rebuilt v2 spline profile — the reasoning holds, re-confirmed point-by-point on the new
mesh, not just carried forward by analogy.**

## 5. Magnet pocket margin (body collar) — independently verified

Directly measured from both `stl/urn-body.stl` and `3mf/urn-body.3mf`:
- Collar cross-section: outer radius 39.0mm (OD 78mm, matches the revised spec), inner bore
  radius 29.0mm (ID 58mm, matches spec) → wall thickness 10.0mm.
- Magnet pockets measured at **radius 34.0mm** (the true midline of the 10mm-thick wall,
  not the old pre-fix 33mm bolt circle) on all three body pockets (0°, 120°, 240°) and all
  three lid pockets (60°, −60°, 180° — same radius, same 120° spacing, correctly rotationally
  compatible with the body's pattern regardless of assembly rotation).
- Pocket diameter measured 6.18mm (spec: 6.2mm), depth ~2.2mm, matching spec.

**Margin: 1.9mm on both the inner (toward cavity) and outer (toward exterior) sides —
genuinely symmetric, not an averaged number hiding a thin spot.** This is a materially better
result than my own back-of-envelope check suggested before measuring — I'd initially assumed
the bolt circle might have stayed at the pre-fix 33mm radius (which would've left only 0.9mm
on the inner side, same as the original flagged problem), but the Coder actually re-centered
the pockets to the new wall midline. **PASS**, confirmed good margin (2.4× the 0.8mm print
floor), not "barely clearing."

> **Correction from the Re-test Pass below (R2):** the absolute angular positions quoted here
> (0°/120°/240° for the body, 60°/−60°/180° for the lid) turned out to be affected by a
> measurement-tool artifact on my end for the lid figure specifically — see R2 for the
> corrected reading (0°/120°/240° for both) and why it doesn't change this PASS verdict. The
> radius, count, spacing, size, and depth numbers above are all still correct.

## 6. Handle open-hole verification — independently verified, not just Coder self-report

Per the task's specific instruction not to trust the Coder's self-report here, I independently
probed the lid mesh:

- Sliced the lid at y=0 (through the loop's center plane): found a clear opening measuring
  **~22 × 24mm** — matches the spec's 24×22mm target (axes swapped only due to the local
  slice-frame orientation, not a real discrepancy).
- Swept the slice from y=−8mm to y=+8mm in 1–2mm steps: the opening is present and consistent
  in size across **y=−4mm to y=+4mm** (matching the 9mm round bail cross-section), and cleanly
  absent (no material at all, meaning open air, not a cap) at y≤−5mm and y≥+5mm.
- This confirms the opening is a genuine **through-channel**, open to ambient air on both the
  front and back face of the loop, not a blind pocket. Support material generated inside it
  during printing will be reachable and removable from either side.

**PASS.** Hard constraint (open-hole, not enclosed cavity) independently confirmed true in
the actual shipped geometry.

## 7. Plain-body hard constraint (no engraving/plaque) — independently verified

Measured radial deviation from a fitted circle at 7 heights up the belly (z=20 through
z=115): standard deviation of boundary radius ranged **0.23–0.30mm** at every height, fully
consistent with normal STL tessellation faceting and nowhere close to what a several-mm-deep
engraved plaque or recessed panel would produce.

**PASS.** The body is confirmed smooth/plain on all sides in the actual geometry, not just by
spec intent.

## 8. Lid/body seating collision check

Body's own max Z is exactly 160mm (confirmed from STL bounds); the lid's flat underside sits
at the body's z=160 seating plane and the entire lid occupies z≥160 in assembled coordinates.
Since the body has zero material above z=160, there is no shared z-range in which the two
parts' geometry could intersect, regardless of the lid brim's radial overhang past the
collar edge. **PASS**, confirmed geometrically, not just asserted.

## 9. Load test — handle

Lid material-shell volume is 150.82 cm³; at 100% infill and PLA density (~1.24 g/cm³) that's
≈187g, in line with the spec's "well under 200g" estimate (actual printed weight will be
lower at 15–20% infill, since most of that solid-shell volume is the thin brim/dome walls
anyway). A 9mm-diameter round PLA loop has enormous margin over a ~190g static lift load —
**PASS**, no bending/failure expected under the stated design load.

**Usage-education flag (not a design defect):** the handle is explicitly only rated to lift
the lid, not the assembled urn+contents. Nothing on the physical object itself will stop a
user from instinctively trying to lift the whole assembled urn by the small handle. Recommend
this be called out in whatever documentation/care card ships with the piece.

## 10. Drop test (qualitative, no physical article to actually drop)

Highest-risk zones for a knock/drop, in order of concern:
1. **Handle root fillet (4mm)** — protruding, load-bearing, and the feature most likely to
   take a direct hit if the lid is set down carelessly or the assembled piece is bumped while
   being carried by the handle. PLA is brittle under sudden/impact loading even though it's
   plenty strong for the static lift case (see §9 and Material section below).
2. **Magnet pocket edges (collar and lid, 1.9mm wall)** — comfortably above print-minimum
   and not a static-load concern, but a blind-hole edge is a stress riser, and PLA's low
   impact toughness makes a hard direct knock on that specific edge a real (if low-probability)
   crack-initiation risk.
3. **Base** — well protected by design: wall thickness increases toward the base (§3) and
   there's a 10mm internal floor/wall fillet already specified. This is the part's strongest
   zone for impact **except for the defect in §11 below**, which undermines exactly this.

## 11. DEFECT — unintended magnet-style pockets molded into the base (blocking)

**This was not disclosed by the Coder and is not called for anywhere in `specs.md`.**

Independent cross-sectioning of the body mesh found **3 circular pockets on the underside of
the base** (the flat, bed-contacting surface, z=0), at:
- Radius 34.0mm from center, spaced 120° apart (0°, 120°, 240°)
- 6.18mm diameter, ~2.2mm deep

These are **identical in every dimension** to the legitimate collar magnet pockets at the top
of the neck (also radius 34.0mm, 120° apart, 6.18mm diameter, 2.2mm deep) — strongly
indicating this is a duplicated/mis-referenced sketch or pattern feature from the collar
magnet-pocket operation that got applied to the base face as well, not an intentional design
element. Confirmed present in **both** `stl/urn-body.stl` and the actual slicer-ready
`3mf/urn-body.3mf` — this is not an STL-export artifact, it will print as-is if sent to a
slicer unmodified.

**Why this matters, concretely:**
- The base is supposed to be the part's single most reliable, fully-flat, fully-adhered
  first-layer surface (98mm OD, chosen specifically for bed adhesion per spec §9). Three
  unplanned 6.2mm holes in that surface work against that goal — this is the opposite of the
  lid's magnet pockets (which are a deliberate, accounted-for feature on a face that's
  otherwise not load- or adhesion-critical).
- It locally thins the floor (spec: 5mm nominal, chosen partly to carry the settled weight of
  the remains bag "over years on a shelf") in exactly the zone that will absorb impact energy
  if the urn is ever knocked off a shelf or set down hard — the single highest-consequence
  drop scenario for this object, given the contents.
- Nothing in the spec calls for any feature on the base beyond plain floor + internal fillet.
  There's no plausible legitimate design reason (no leveling feet, no drainage, nothing in the
  brief or spec mentions base features) — this reads as a modeling mistake, not a design
  choice, and it wasn't among the 3 disclosed delegated-authority deviations in the build
  report.

**This blocks moving to Reviewer.** It needs to go back to the Coder to find and remove
the erroneous feature/pattern instance and re-export all three deliverable formats
(STEP/3MF/STL) for the body only — the lid was checked with the same method (full-height
scan, every 2mm) and has no equivalent anomaly.

> **See the Re-test Pass below (R1) — this defect has been independently re-verified as
> fixed, and re-confirmed fixed again after a full from-scratch rebuild (R11).**

## 12. Material check

Spec already flags PLA's heat/UV softening risk (§8, edge case 3) — that's adequately
disclosed and accepted for the finish requirement. Separately, and not currently flagged in
the spec: **PLA's brittleness under sudden/impact loading** (as opposed to static strength,
which is fine, see §9) is a real, distinct risk at two features specifically:
- The handle bail root fillet (repeated grip-and-lift use over years, plus a plausible knock
  point).
- The magnet pocket edges (blind-hole stress risers, now made worse in the base area by the
  defect in §11 until that's fixed).

**Recommendation: print the lid in PETG instead of PLA**, or at minimum reinforce the handle
root and magnet pocket edges if PLA is kept. PETG has meaningfully better impact toughness
than PLA at a modest cost to the matte/silk finish goal (PETG does offer some matte/silk-like
filament options today, just a smaller selection than PLA) — worth a direct trade-off
conversation with the requester rather than defaulting silently to PLA everywhere, given this
object holds irreplaceable contents and the failure mode (a crack at the handle or a pocket
edge from a single bad knock) is a real, if not high-probability, outcome for something meant
to sit on a shelf for years and occasionally be handled.

> **See the Re-test Pass below (R4) — the Coder has adopted this PETG recommendation for the
> lid. Assessed independently there, not just accepted.**

## 13. Slicer settings / metadata — process note, not a defect

Confirmed (per build report, not independently re-verifiable without a slicer): layer height
0.16–0.2mm and 15–20% infill are **not** embedded in the 3MF files. Material (matte/silk PLA)
is also not captured in any file metadata. **Both must be set manually in the slicer before
printing** — do not assume the 3MF "just works" with correct settings out of the box.

No slicer was available in this test pass, so supports-needed-for-overhangs and
bed-adhesion-in-practice could not be confirmed by an actual sliced preview — the assessments
above (§4, §10) are geometry-based, not slicer-confirmed.

---
---

# RE-TEST PASS — following Coder fixes (base-pocket defect, PETG lid, neck-fit-test article)

Method note: same independent-verification standard as the original pass — direct mesh
measurement via `trimesh` against the actual shipped files (STL and 3MF), not the Coder's
self-report, with extra scrutiny specifically on the item that blocked last time (§11 above).
No slicer was available in this pass either.

## R1. Base-pocket defect — independent re-verification (the item that blocked last time)

**Re-tested using two independent methods, not just re-running the original cross-section
sweep, specifically because I don't trust my own prior method alone on the exact defect I
caught the Coder on:**

1. **Cross-section sweep, z=0.05mm to z=5mm** (covers the full depth the old bogus pockets
   occupied, plus margin) on the current `stl/urn-body.stl`: every single slice in this range
   returns **exactly one boundary loop with zero interior holes**. The old defect showed up in
   this exact test as 3 extra interior-hole loops at radius 34mm — they are gone.
2. **Direct vertex inspection of the bottom cap** (z=0 vertices only, both STL and 3MF): the
   entire bottom face consists of **77 vertices (STL) / 137 vertices (3MF), all at a single
   uniform radius (49.00mm = the 98mm base OD), with zero interior vertices.** This means the
   bottom cap is a single N-gon/triangle-fan approximating a plain flat disc — there is no
   internal geometry at all on that face, not even non-hole internal geometry. This is a
   stronger confirmation than the cross-section sweep: it's not just "no holes found," it's
   "there is nothing there to have a hole in except the flat disc itself."

Repeated on `3mf/urn-body.3mf` (the actual slicer-ready file, not just the STL) — same result:
137 bottom-face vertices, all at r=49.00mm, zero interior points.

Also re-confirmed overall solid integrity on the current export: `stl/urn-body.stl` is
watertight, winding-consistent, single connected solid, bounds z=[0,160], XY bounding-box
centered exactly on (0,0). `3mf/urn-body.3mf` is watertight, single geometry, consistent
bounds.

**Result: PASS. The base-pocket defect from §11 is confirmed fixed, independently, in both
deliverable formats, using a different (more direct) method than the original detection
method as an extra check against confirmation bias on my own part.** This specific item is
unblocked.

**Process note (per the build report, worth carrying forward, not a new defect):** the Coder
found the 3 bogus pockets had no owning feature in the parametric timeline — they were baked
directly into the saved B-Rep via a scripted direct-edit that bypassed the feature timeline
entirely. I can't independently audit the Fusion timeline itself from mesh files, so I'm
relying on the Coder's account for the *mechanism*, but the *result* (clean base, confirmed
above) is independently verified regardless of mechanism. Flagging this as a standing process
risk: direct-BRep edits that bypass the timeline are exactly the kind of change a normal
"review the feature tree" check would miss, which is presumably how 3 unplanned holes made it
into a prior export undetected by the Coder. Recommend avoiding scripted direct-BRep edits on
this project going forward in favor of timeline-native features, specifically so this class of
defect is visible in the tree next time, not just in the final mesh.

## R2. Legitimate collar magnet pockets — spot-check re-confirmation

Independently re-measured (not just re-read the Coder's report) using a different technique
than either R1 or the original §5 pass (radial ray-casting to find the true outer-wall radius
profile by height, then cross-section sweeps through the collar's top face specifically, once
ray-casting revealed the pockets are bored *axially downward from the flat top rim*, not
radially into the cylindrical wall — worth noting for the record, since assuming the wrong
boring axis initially returned a false "no pockets found" result before I corrected the
approach):

- Collar cross-section confirmed: outer radius 39.0mm (OD 78mm), inner bore radius 29.0mm
  (ID 58mm), 10mm wall — matches spec revision and the original pass's numbers.
- **3 pockets found**, each ~6.2mm diameter (measured interior-hole radius 3.09–3.10mm),
  present from z=157.8mm to z=160mm (top rim) — exactly 2.2mm deep, matching spec.
- Angular positions measured directly from raw mesh vertex world coordinates (not via the
  `trimesh` Path2D projection, which I found introduces an arbitrary rotational offset between
  independent slice calls — see note below): **0°, 120°, 240°**, 120° apart, radius 34.0mm
  bolt circle — matches the "34mm bolt circle, 3 pockets, 78mm OD collar" description in this
  task's brief.

**Result: PASS.** Present, correctly sized, correctly positioned, unaffected by the base fix
— confirmed independently, not just spot-checked against the Coder's claim.

**Methodology correction for the record (not a design defect):** the original pass (§5 above)
reported lid pocket angles as 60°/−60°/180°; my re-measurement of the same, unchanged lid file
in R3 below gets 0°/120°/240°. I traced this to `trimesh`'s `Path3D.to_2D()` picking an
arbitrary in-plane rotation basis independently on each call, which produced a spurious ~60°
offset between slices taken at different heights in my own script. Once I switched to reading
raw mesh vertex world coordinates directly (bypassing that conversion), the measured angles
became stable and self-consistent across every height sampled. This doesn't change any PASS
verdict — the functional claim being tested (3-fold, 120°-spaced pockets on a 34mm bolt circle
that self-align at any of 3 rotations, since there's no keying feature and magnets provide
final centering per spec §5.2) holds under either absolute reading — but it means the specific
absolute-angle numbers quoted in the original §5 pass should not be treated as reliable; the
radius, count, spacing, size, and depth numbers in that section are unaffected and remain
correct.

## R3. Lid magnet pockets — re-confirmed unaffected (file not re-exported, spot-checked anyway)

Per the task, `urn-lid.stl`/`.3mf` were **not** re-exported this round — but re-verified anyway
rather than assuming "unchanged file = still correct":

- 3 pockets confirmed present, ~6.2mm diameter, ~2.2mm deep (from z=0 to ~z=2.2 on the lid's
  underside, which sits face-up in this coordinate frame), radius 34.0mm, 120° apart at
  0°/120°/240° (see methodology note in R2 above for why this differs from the original pass's
  60°/−60°/180° reading — not a real change, a measurement-method correction).
- Lid mesh independently re-confirmed watertight, single solid, bounds unchanged from the
  original pass, XY-centered at (0,0) — no offset leakage from the viewport shift (see R6).

**Result: PASS**, unaffected by the base fix, as claimed.

## R4. PETG-for-lid material change — independent assessment, not a rubber-stamp of the Coder's claim

The Coder's claim is that existing tolerances (magnet pocket oversize, handle root fillet,
wall thickness) are conservative enough that switching the lid from matte/silk PLA to PETG
needs no geometry change. **Partially agree, with one real reservation and one point the
Coder's framing misses entirely:**

- **Handle root fillet, wall thickness: agree, no change needed.** PETG has meaningfully
  *better* interlayer adhesion and impact toughness than PLA — this makes the Coder's already
  "not over-built, matched to actual load case" 4mm fillet (§7) and 4mm nominal wall *more*
  conservative under PETG than it was under PLA, not less. No reservation here; this is a
  straightforward improvement, and it directly addresses part of the brittleness concern
  already raised in §12 above.
- **Magnet pocket oversize (0.2mm): reservation, not a rubber-stamp.** PETG is more prone to
  fine stringing/oozing into small negative features than PLA, and commonly benefits from a
  larger post-print-insert oversize allowance for exactly this reason — 0.2mm is a reasonable
  PLA convention but is on the tight side for PETG specifically, independent of anything else
  in this design. This isn't blocking (the pockets are glue-assist, post-print-insert, not a
  precision press fit — per spec §6.1 — so a slightly tight pocket is correctable with a
  hobby knife or a bit of sanding, not a functional failure), but it means the Coder's
  "existing tolerance is conservative enough" claim doesn't fully hold for this specific
  feature. Recommend the same small test-coupon check already flagged for the PLA body pockets
  (§0) be done in PETG specifically before committing the lid to a full print, rather than
  assuming the PLA-derived number ports over unchanged.
- **Point the Coder's claim doesn't address at all: apex cooling/stringing behavior at the
  dome apex.** Spec §9 already calls out a "known, minor, cosmetic-only" drooping risk right at
  the lid dome's apex under PLA, described as "normal, usually slicer-manageable." PETG prints
  at a meaningfully higher nozzle temperature (~230–250°C vs. PLA's ~200–210°C) and cools more
  slowly, which generally makes fine bridging/near-horizontal overhang artifacts (stringing,
  drooping, blobbing) *more* pronounced at a given geometry than PLA, not less — this is a
  well-known practical difference between the two materials, not a geometry-tolerance question
  at all, which is why a "tolerances are conservative enough" argument doesn't cover it. This
  doesn't require a geometry change (the Coder is right that the *shape* doesn't need to
  change), but it does mean whoever slices the PETG lid should expect to tune cooling
  fan/print-speed settings specifically for that apex, rather than reusing PLA-tuned slicer
  defaults and assuming the same "usually fine" outcome will carry over.
- **Bed adhesion / warping — orientation is still correct, no change needed.** PETG generally
  needs a hotter bed and is more prone to over-adhering (elephant's foot / hard-to-remove
  first layer) than PLA, but the lid's flat-underside-down orientation (chosen in §5.2/§9
  specifically for maximum, continuous flat bed contact) is if anything the *best-case*
  orientation for managing that — no orientation change indicated for the material switch.

**Overall verdict on this item: the Coder's claim is reasonable but incomplete, not a
rationalization to be rejected outright.** Two of three cited tolerances hold up or improve
under PETG; the magnet pocket oversize is genuinely worth a second look via test coupon rather
than assumed fine; and there's a real PETG-specific slicer-settings consideration (apex
cooling) that the "no geometry change needed" framing correctly identifies as not requiring a
geometry change, but which shouldn't be silently treated as "therefore nothing to think about."

## R5. New part — `neck-fit-test` physical test article

Independently verified from `stl/neck-fit-test.stl` and cross-checked against
`3mf/neck-fit-test.3mf`:

- **Manifold/printability:** watertight, winding-consistent, single connected component,
  Euler characteristic 0 (correct for an open-ended tube — the topology is a genus-1 solid:
  outer wall + inner wall + top rim + bottom rim, open bore all the way through, not a
  capped cup). This is the right topology for a "push a bag mockup through it" test — both
  ends are genuinely open, not a blind pocket.
- **ID: confirmed 58mm**, measured as a constant 29.00mm inner radius from z=20mm (where the
  test article's stabilizing base flange blends into the true neck) all the way to z=34mm
  (top of the collar) — this is the full height range that represents the actual body's neck
  opening, and it holds the target dimension exactly, not approximately.
- **OD: confirmed 78mm at the collar** (outer radius exactly 39.00mm from z=27mm to the top),
  and separately confirmed 66mm at the neck proper (outer radius 33.09mm at z=20.1mm, i.e.
  right where the ID reaches its final 58mm) — both figures match the spec's stated external
  OD values for these two zones, not just the headline collar number.
- **Not disclosed but found, and it's a reasonable addition, not a defect:** the test article
  isn't literally just a 35mm-tall extrusion of the neck+collar — it has a wide flared
  stabilizing base flange (up to ~122mm OD at z=0, tapering up to meet the true 66mm neck OD
  by z≈20mm) beneath the represented neck/collar section. This reads as a sensible print-
  stability/bed-adhesion aid for an otherwise small, tall-ish standalone part, not scope creep
  — it doesn't change the ID/OD dimensions being tested, and it doesn't introduce any new
  overhang risk (see below).
- **Printability/orientation:** printed flange-down (matching the main body's own natural
  base-down orientation), the entire profile is self-supporting with zero problematic
  overhangs. Verified by radial ray-casting at 1mm height steps up the full part: the flange-
  to-neck taper (z=0 to z=20) has outer radius *monotonically decreasing* with height at every
  sampled step — the same "shrinking cone" self-supporting geometry class discussed in §4
  above, mechanically incapable of an unsupported-overhang failure. The one genuine widening
  transition (neck-to-collar blend, z=20 to z=27) measures ~40° from vertical, consistent with
  the already-validated 27–41° figure for this same feature on the main body (§4) and safely
  under the 45° guideline.
- **Bed fit:** ~122mm max OD × 35mm tall — trivially clears the 256×256×256mm bed.
- **Position:** bounding box XY-centered at (0,0), Z from 0 to 35mm, in both STL and 3MF —
  correctly positioned for a standalone print job (see R6).

**Result: PASS.** This is a valid, correctly-dimensioned, single-manifold, self-supporting
part, ready for the user to actually print and physically test-fit. (Whether a real remains
bag passes through the resulting 58mm opening is the user's physical test to run — not
something re-verifiable here, and not what this check was scoped to answer.)

## R6. Viewport-shift leakage check — confirmed non-issue

Independently re-measured bounding boxes of all three current STL exports and the two
re-checked/re-confirmed 3MF exports:

| File | XY center | Z range |
|---|---|---|
| `stl/urn-body.stl` | (0.00, 0.00) | 0 → 160mm |
| `stl/urn-lid.stl` | (0.01, 0.00) | 0 → 75mm |
| `stl/neck-fit-test.stl` | (0.00, 0.00) | 0 → 35mm |
| `3mf/urn-body.3mf` | (0.00, 0.00) | 0 → 160mm |
| `3mf/urn-lid.3mf` | (0.00, 0.00) | 0 → 74.99mm |

All five are centered on the print-bed origin and start at Z=0, exactly as a standalone print
job needs, with no measurable offset from the viewport rearrangement. (The 0.01mm lid X-center
figure is well within normal mesh-tessellation noise, not a real offset.)

**Result: PASS.** Confirmed non-issue, not just accepted on the Coder's word.

## R7. Spot-check of previously-passed items (not fully re-run, per task scope)

Re-confirmed still true from the current files, without re-deriving from scratch:
volume/bed-fit/wall-thickness/plain-body constraints are unaffected by anything changed this
round (none of those features were touched); body remains a single watertight solid at the
same bounds as before, aside from the base fix itself.

---
---

# RE-TEST PASS 2 — following full urn-body rebuild against revised specs.md (belly position + spline profile)

Method note: same independent standard as both prior passes — direct measurement against the
actual shipped `stl/urn-body.stl` and `3mf/urn-body.3mf` (freshly re-exported, ~44,400
triangles) via `trimesh`, plus a direct Fusion viewport screenshot for a real visual read of
the "does this actually look smooth" question, not a re-derivation from the spec's own frustum
approximation table. Read the revised `specs.md` sections 4.2/4.3 before starting this pass,
per instruction, so measurements are checked against the current target (belly at 45%/72mm,
spline profile), not the v1 target from the prior two passes.

## R8. Belly position — independently re-measured: PASS, exact match

Measured the true external max-radius height directly from `stl/urn-body.stl` via dense radial
ray-casting (1mm steps first, then 0.1mm steps around the peak to pin it down precisely):

- **Peak external radius: exactly 73.000mm, occurring at exactly z=72.0mm.**
- 72mm / 160mm total height = **45.00%**, matching the Coder's reported figure exactly, not
  approximately — this isn't a "close enough" result, the ray-casting found the peak sample
  landing on precisely 72.0mm with radius climbing monotonically to that point from both sides
  (71.9mm: 72.9934mm; 72.1mm: 72.9984mm — a clean, single, symmetric peak, not a plateau or a
  double-bump artifact).

**Direct visual comparison against `concept/concept-v2.png`**, per the specific instruction not
to skip this step this time: took live screenshots of the actual current Fusion body (not a
rendering of the STL) from the side and from an isometric angle. Since the body is a solid of
revolution (unaffected by viewing azimuth except for the 3 collar magnet-pocket holes and the
flat base), any side-on screenshot is a valid like-for-like comparison to the concept photo's
silhouette. The rendered body's belly reads as clearly sitting in the lower half of the vessel,
proportionally consistent with the concept photo's own low, wide belly — both show the belly
apex meaningfully below the object's vertical center, not at or above it. This qualitative read
is consistent with, and corroborated by, the exact 45.00% figure above.

**Result: PASS**, independently confirmed both numerically (exact) and visually (direct
screenshot comparison against the concept image, not skipped this time).

## R9. Smoothness fix — split result: PASS for the internal-profile spline, but a real residual defect found at the neck-to-collar external blend

This is the item the task asked for real scrutiny on, not just "the math checks out" — so here
is the actual mesh-level analysis, not a repeat of the Coder's mathematical claim.

**Internal-profile-driven regions (base → belly → shoulder → neck-taper-end, z=0 to z=145):
genuinely smooth, confirmed by curvature analysis, not just visual impression.**

Computed `dr/dz` (local slope of the outer radius) at 0.25–0.5mm resolution across this entire
span using mesh cross-sections (not ray-casting, which produced a spurious artifact near the
shoulder from a single grazing ray at one fixed angle — resolved by switching to full
cross-section boundary extraction, which is immune to that single-ray grazing issue):

- **Exactly one sign change in `dr/dz`**, at z=71.5→72.0mm — precisely at the belly apex,
  exactly where the spec's P1 mandatory horizontal-tangent condition requires it, and nowhere
  else in this entire span. This matches the Coder's mathematical claim, confirmed independently
  against the actual mesh rather than the design intent.
- The shoulder region (z=108–130, spanning across the spec's P2 inflection point at z=119) shows
  a **continuously, smoothly decreasing radius with no discontinuity, no reversal, and no cusp**
  — sampled at 0.5mm resolution, every single step is a small, gradually-changing decrement
  (e.g., 65.66→65.48→65.30... mm), never a jump. This is a genuinely smooth curve at the
  shoulder, matching the Coder's claim of "no cusp at the shoulder inflection."
- The neck taper (z=130–145) similarly shows a smooth, continuously decelerating slope as it
  approaches the P3 control point, reaching **exactly r=33.0000mm at exactly z=145.00mm** (the
  spec's exact target for this point) with the slope smoothly approaching zero from below,
  exactly as the spec's P3 tangent condition requires.

**This part of the rebuild is a real, substantiated success** — a visibly faceted body has
genuinely been replaced with a continuously curved one across the entire base-to-neck-taper
span, verified by direct curvature analysis, not just accepted on the Coder's mathematical
self-report.

**Neck-to-collar external blend (z=145–152mm): NOT smooth — a real, measurable, visually
significant residual defect.**

This region sits just above the officially-specified internal-profile spline (which only
governs P0–P4's *internal* bore, per the spec's own framing: "Control points and tangencies
(**internal profile**; spline sketch + revolve)") — the external collar thickening (66mm neck
OD → 78mm collar OD) is a separate feature layered on top, and it was **not** rebuilt with the
same tangent-matched approach:

- Fine-resolution cross-sections (0.1mm steps) directly either side of z=145.0 show the radius
  approaching 33.0000mm smoothly from below (slope decelerating toward zero, as required), then
  **the very next sample above (z=145.10mm) already shows a fully-formed straight-line slope of
  0.857mm/mm** — no easing, no transition, an instantaneous slope change from ~0 to 0.857.
- That slope (**0.857mm/mm, ≈40.6° from vertical**) holds **perfectly constant** for the entire
  7mm span from z=145 to z=152 — every single sample checked (28 points at 0.25mm spacing) sits
  exactly on one straight line, confirming this is a literal conical chamfer, not a curve of any
  kind.
- At z=152.0mm the radius hits exactly 39.0000mm (the collar's full OD) and **instantly flattens
  to a constant 0 slope** for the rest of the way to the rim — again with no easing.
- **This produces two genuine, measurable sharp corners (C0-continuous but C1-discontinuous
  kinks)** — one at z=145mm (where the smoothly-decelerating neck taper meets the straight
  chamfer head-on) and one at z=152mm (where the straight chamfer meets the flat collar
  cylinder). A profile plot of this exact region (radius vs. height, sampled every 0.1mm) shows
  it unambiguously: a smooth curve, then a dead-straight diagonal line, then a dead-straight
  vertical line, with two visible corners between them — not a continuous curve anywhere in
  this 15mm span.
- **Confirmed visually, not just numerically:** a live Fusion screenshot of the actual body
  shows a clearly visible diagonal crease/fold line cutting across the surface at exactly this
  location — this is not a subtle, sub-visual mathematical technicality, it reads as a distinct
  fold in the surface to the eye, in a screenshot taken today of the actual current model.
- **Direct comparison against `concept-v2.png`'s own rim/neck close-up** shows the concept's
  neck-to-rim transition as one continuous, softly rolling curve with no straight sections and
  no corners anywhere — the concept does not show anything resembling a distinct cylindrical
  "collar band" with hard edges. The current model's straight-chamfer collar blend is a visible
  departure from that reference, not a faithful reproduction of it.

**Why this matters:** this is exactly the failure mode the spec's own P3 tangent condition
explicitly warned against — "must flatten to match the constant-radius straight section
immediately above it, **or there will be a visible kink where the taper meets the collar**."
The taper-side flattening was done correctly (confirmed above), but the "constant-radius
section immediately above it" is not actually constant-radius immediately above P3 — it's a
straight ramp up to a *different* constant radius 7mm later, and neither end of that ramp eases
in or out. The predicted kink happened, in a highly visible location (directly below the rim,
in the sightline of essentially every photo of this object, assembled or open) — and a second,
undiscussed kink was introduced at the top of the same ramp. Since the entire stated purpose of
this rebuild round was eliminating exactly this class of defect (facets/kinks) in favor of
continuous curvature, this is a real, unresolved gap against that goal, not a nitpick.

**This is not the same issue as the already-accepted "neck-to-collar blend overhang angle"
finding from the prior pass** — that finding was about the *print-support* implications of a
widening transition (is it under 45°?), which is a separate question from whether that
transition is *shaped* as a smooth curve or a hard-cornered chamfer. Both can be true
simultaneously: the chamfer's overall angle is fine for support purposes (see R14 below), while
its shape is still a cosmetic/smoothness defect.

**Result: PARTIAL — the internal-profile smoothness objective is genuinely met (PASS), but the
neck-to-collar external blend is a real, independently-confirmed (numerically and visually)
smoothness defect that was not disclosed and directly contradicts the stated purpose of this
rebuild round.** Recommend this go back to be fixed using the same tangent-matched approach
already successfully applied to the internal profile (a fillet/blend between the neck OD and
collar OD, rather than a straight conical step) before the smoothness objective can be called
fully resolved.

## R10. Volume — independently re-verified

Measured internal cavity volume directly from `stl/urn-body.stl` via cross-sectional
integration (interior-hole area at 400 heights from the floor top to the rim, integrated via
the trapezoidal rule):

- **Measured: 1511.27 cm³**
- Coder-reported: 1511.8 cm³ (0.03% difference — well within normal mesh-resolution variance)
- Revised spec target: 1477.8 cm³ → **+2.27% deviation**, matching the Coder's reported +2.3%

**Result: PASS.** Independently confirmed, and within the spec's own explicitly stated ~5%
tolerance band for exactly this kind of spline-vs-frustum-approximation deviation (see §4.2's
"Named caveat" paragraph, which pre-authorizes up to ~5% deviation from the frustum estimate
before a spec revision is needed).

**My independent opinion on the volume-vs-smoothness tradeoff, since a real opinion was asked
for and not just agreement:** the Coder's call to accept +2.3% volume overage rather than
over-tightening tangents to chase closer volume accuracy was the right call, and it was
appropriately made at the Coder level rather than needing to go back to the Planner. Two
reasons: first, the spec text itself explicitly pre-authorizes exactly this tradeoff ("flag
back for a spec revision if it falls outside the 1475–1478 cm³ band by more than ~5%" —
2.3% is well inside that band, so no Planner round-trip was actually required by the spec's own
terms, this was anticipated). Second, volume is a `DERIVED — sizing decision` figure with an
explicit tolerance band built in from the start, while curve smoothness at the shoulder was the
literal, stated reason this entire rebuild round exists — prioritizing the harder, less
tolerance-forgiving requirement (visible curve quality) over squeezing a few more tenths of a
percent out of an already-satisfied, explicitly-tolerant requirement (volume) is the correct
engineering priority, not scope overreach. (Separately, and independently of this specific
tradeoff: my R9 finding above shows the shoulder curve quality this tradeoff was made to protect
*did* come out smooth and correct — so the tradeoff bought something real, even though a
different, unrelated part of the same rebuild — the collar blend — still needs a fix.)

## R11. Base-pocket regression check — re-confirmed clean after full rebuild-from-scratch

Independently re-ran the exact same two-method check from R1 above, against the freshly
rebuilt-from-scratch mesh (not assuming the prior fix persists just because it was fixed once):

- Bottom-cap vertex inspection: **77 vertices (STL) / 136 vertices (3MF), all at a single
  uniform radius of 49.00mm, zero interior vertices** — identical signature to the confirmed-fixed
  state from the prior pass.
- Cross-section sweep z=0.05–5mm: single boundary loop, zero interior holes, at every sampled
  height.

**Result: PASS.** The base remains clean after the full from-scratch rebuild, confirmed
independently in both STL and 3MF, not assumed from "it was fixed last time."

**Process risk note, worth recording even though it's not a testable geometry defect this
round:** the Coder's stated root cause — `ExtrudeFeatureInput.participantBodies` silently
defaulting to "all intersected bodies" when left unset, allowing a cut on one component to leak
into a different, unrelated body sharing a local origin — is a systemic risk, not a one-off
mistake specific to the base pockets. Any future feature in this shared multi-body Fusion file
that performs a cut/extrude without explicitly setting `participantBodies` is exposed to the
same class of defect (silent cross-component leakage), and by nature this kind of defect is
easy to miss in a routine review because the leaked geometry looks locally plausible (as
happened here — the original bogus base pockets were dimensionally identical to a legitimate
feature, which is exactly why they were mistaken for intentional at first glance). Recommend
this be treated as a standing modeling-practice rule for this file going forward (always
explicitly set `participantBodies` on any cut/extrude in a multi-body document), not just a
closed incident.

## R12. Collar magnet pockets — re-confirmed unchanged and correct

Independently re-measured against the freshly rebuilt body (not assuming they carried over
correctly just because the Coder reports them untouched):

- Collar cross-section: outer radius 39.0mm (OD 78mm), inner bore radius 29.0mm (ID 58mm) —
  unchanged from the prior pass, matching spec.
- **3 pockets confirmed**, radius 30.9–37.1mm (diameter 6.2mm, centered on a 34.0mm bolt
  circle), at **0°, 120°, 240°**, present from z=157.8mm to z=160mm (2.2mm deep) — measured
  directly from raw mesh vertex coordinates, matching the Coder's reported "3× 6.2mm dia, 34mm
  bolt radius, 120° apart" exactly.

**Result: PASS.** Present, correctly sized and positioned, unaffected by the full rebuild.

## R13. Manifold check — re-confirmed

- `stl/urn-body.stl`: watertight, winding-consistent, **single connected component**, Euler
  characteristic 2 (correct for a closed single-cavity vessel shell with no through-holes —
  topologically a sphere, as expected for a solid-of-revolution vessel with a floor and an open
  rim, no genus).
- `3mf/urn-body.3mf`: watertight, single geometry, consistent bounds with the STL.

**Result: PASS** on everything independently checkable from the exported mesh files. The
Coder's reported B-rep face count (14, down from 26) is a Fusion-timeline-specific metric that
isn't recoverable from a triangulated STL/3MF export — **not independently verified this pass**,
noted honestly rather than silently treated as confirmed. The drop from 26 to 14 faces is
directionally plausible (fewer flat frustum-segment faces, replaced by fewer smooth spline
surfaces) but I have no way to confirm the exact number without direct Fusion timeline access.

## R14. Overhang re-check — is the "shrinking radius is self-supporting regardless of angle" reasoning still valid for the new spline profile?

**Yes, confirmed independently and directly on the actual current mesh — the reasoning holds,
and I checked the specific mechanism rather than just re-asserting the old conclusion by
analogy.**

The concern was whether the new spline's *curve shape* (as opposed to the old frustum's
straight segments) could break the "every layer sits inside the footprint of the layer below"
argument — e.g., if the curve had any small local bulge or reversal hidden inside an
overall-decreasing trend, that specific spot could still overhang even though the endpoints
show a net decrease. This is directly checkable, not just arguable, so it was checked:

- Extracted the actual outer radius at 0.25mm height steps across the entire P2→P3 span
  (z=119mm to z=145mm, the shoulder-to-neck-taper-end region the spec flags at ~47°) — **104
  samples, radius monotonically non-increasing at every single step, zero increasing steps
  found.** There is no hidden local bulge or reversal anywhere in this span on the actual
  built mesh.
- The *local* instantaneous slope actually peaks steeper than the spec's reported ~47° average
  at one point (**54.5° from vertical at z≈137mm**) — steeper locally than the headline figure,
  similar to the pattern already seen and accepted in the prior (v1) build's equivalent
  transition. This doesn't change the conclusion: since the radius never increases anywhere in
  this span, *every* point along it — including the locally steeper 54.5° point — still sits
  within the shrinking-cone category, where the self-supporting argument depends on the sign of
  `dr/dz`, not its magnitude.

**Determination: the reasoning is still valid for the new spline profile, and this is a
stronger confirmation than "the shape class is the same as before" — I directly verified
point-by-point monotonicity on the actual rebuilt mesh rather than assuming a curved profile
preserves the same qualitative behavior as the old straight-segment one.** No supports are
expected on this specific transition regardless of the local angle reaching slightly past 45°
at its steepest point.

(Separately: the neck-to-collar blend, R9 above, is the genuine *widening* transition and was
already assessed on its own overhang merits — ~40.6° from vertical, under the 45° guideline,
still fine from a print-support standpoint even though its *shape* has the smoothness defect
described in R9. The kink itself is not expected to cause a support/overhang failure — sharp
concave-side corners like this typically print fine without support, at most producing a faint
visible ring artifact at the corner — but it is a real cosmetic defect independent of print-
supportability.)

## R15. Lid — spot-check confirms unaffected, no regression from the near-miss

Per the task, the lid was not intentionally changed this round (aside from a caught-and-restored
near-miss during the base-pocket fix). Spot-checked rather than assumed:

- `stl/urn-lid.stl`, `3mf/urn-lid.3mf`, `step/urn-lid.step` all carry a timestamp (12:01) that
  predates the body rebuild (13:44) — consistent with "never touched this round," not just
  claimed.
- Re-measured `stl/urn-lid.stl`: watertight, bounds and face count (17,664 faces) **identical**
  to what was independently verified in the prior re-test pass (R3 above) — no detectable
  regression from the near-miss the Coder described.

**Result: PASS.** Confirmed unaffected, not just accepted on the Coder's account of the
near-miss being fully caught and restored.

## R16. `neck-fit-test` article — confirmed still valid, agree it does not need regeneration

- File timestamps (13:00) predate the body rebuild (13:44) — genuinely untouched this round.
- Spot-re-measured the dimensions it represents: ID constant at 58mm (r=29.00mm) through the
  neck/collar region, OD 78mm (r=39.00mm) at the collar, OD 66mm (r=33.00mm) at the neck below
  the collar — **all unchanged and still accurate**, because the underlying spec values these
  represent (58mm neck ID, 78mm collar OD, 66mm neck OD) were explicitly *not* touched by the
  v2 belly-position/spline revision — only the internal profile's height allocation and control
  points below the neck changed, per specs.md §4.2's own "Everything not called out as changed
  ... is held fixed."

**Result: agree with the Coder — this article does not need to be regenerated.** The physical
opening it represents is genuinely unchanged by this revision, confirmed by direct
re-measurement rather than taken on the Coder's word that "the collar geometry didn't change."


---
---

# RE-TEST PASS 3 -- post-incident recovery verification (BodyProfile corruption + rebuild)

Method note: this pass follows a reported incident (a direct manual sketch edit corrupted
BodyProfile -- open profile, collapsed neck point, drifted belly -- producing a degenerate
4.45 cm3 fragment) and a Coder-performed recovery (BodyProfile, Revolve1, and Extrude1 rebuilt
from the last known-good configuration, with Extrude1 recreated with participantBodies
explicitly restricted to the body). Per instruction, every Coder-reported number below was
independently re-derived from the actual current stl/urn-body.stl and 3mf/urn-body.3mf --
none of it was accepted on the "matches before" claim alone.

## R17. Manifold check post-recovery -- PASS

`stl/urn-body.stl`: watertight, winding-consistent, single connected component, Euler
characteristic 2 (correct closed-vessel topology, unchanged from pre-incident). Bounds
identical to the pre-incident state: X/Y +-73.0mm, Z 0-160mm. `3mf/urn-body.3mf`: watertight,
single geometry, consistent bounds. No sign of a partial or degenerate recovery -- this is a
single valid solid, not a multi-body leftover or an open shell.

## R18. Volume post-recovery -- PASS, matches pre-incident figures independently

- Material shell volume (from the STL mesh): **293.14 cm3** vs. Coder-reported 293.2050 cm3
  (0.02% difference -- normal STL-tessellation-vs-BRep-mass-properties variance, not a
  discrepancy).
- Internal cavity volume (cross-sectional integration, 400 heights): **1511.27 cm3** vs.
  Coder-reported 1511.8067 cm3 (0.03% difference) -- **identical to the 1511.27 cm3 I
  independently measured on this same body in Re-test Pass 2, before the incident.** This is
  the strongest evidence that the recovered geometry is a genuine reconstruction of the same
  design, not a coincidentally-similar rebuild -- the cavity volume matches my own
  independently-derived number from before the incident to 5 significant figures.

## R19. Belly position post-recovery -- PASS, exact, no regression

Re-measured via the same fine ray-casting method used in Re-test Pass 2: peak external radius
**exactly 73.000mm at exactly z=72.0mm -- 45.00% of height**, identical to both the
pre-incident measurement and the Coder's post-recovery claim. No drift.

## R20. Internal profile smoothness (base -> belly -> shoulder -> neck-taper-end) -- PASS, confirmed unchanged, not just re-derived from scratch

Rather than only re-running the smoothness math fresh, I compared the actual sampled radius
values at 0.5mm resolution against the numbers recorded in Re-test Pass 2 for the shoulder
region specifically (the area most likely to show a subtle regression if the rebuild wasn't a
faithful reconstruction): z=108 (65.6580mm), z=110 (64.9400mm), z=112 (64.1967mm), z=114
(63.3834mm), z=116 (62.4982mm), z=118 (61.5211mm), z=120 (60.3980mm) -- **every value matches
the pre-incident measurement exactly, to 4 decimal places.** This is a direct, point-by-point
confirmation that this part of the geometry is not just "similarly shaped" but numerically
identical to what I verified before the incident. The whole-body slope-continuity scan
confirms only one sign change outside the collar-blend region (the mandatory belly-apex
zero-tangent point), with no new cusps introduced anywhere.

## R21. Neck-to-collar blend (z=145-152mm) -- the headline check: genuinely fixed now, confirmed by the same method that caught it broken

This is the item that blocked "ready for Reviewer" in Re-test Pass 2. Re-ran the identical
0.1mm-resolution cross-section sampling method used to originally catch the sharp chamfer:

- **The slope now changes gradually and continuously through the entire span, with no
  instantaneous jumps anywhere.** Below z=145 the slope rises smoothly from -0.61 through zero;
  above z=145 it climbs gradually (0.13 -> 0.33 -> 0.43 -> 0.52 -> 0.61 -> 0.72... mm/mm) up to
  a broad plateau around slope~1.0-1.02 near z=147-150, then eases back down smoothly (0.80 ->
  0.60 -> 0.44 -> 0.32 -> 0.13 -> 0) into the flat collar cylinder by z=152. This is a genuine
  S-curve blend, not a straight chamfer -- every single 0.1mm step's slope change is small and
  gradual (the largest is ~0.23, versus the previous chamfer's ~0.95 instantaneous jump at the
  exact same location).
- **Visually consistent as well**: this new profile shape (smooth ease-in, broad rounded
  shoulder, smooth ease-out) is the same qualitative shape as every other successfully-smoothed
  transition on this body (e.g. the belly apex), not the two-hard-corner shape documented and
  screenshotted as broken in Re-test Pass 2.
- **Minor, non-blocking note**: the smooth curve's local peak angle (~45.6 deg from vertical,
  at z~149.3mm) is marginally steeper than the old chamfer's uniform ~40.6 deg, and slightly
  over the 45 deg guideline the spec already discusses for this same general region. This is
  expected behavior for a tangent-matched blend replacing a straight chord (the smooth curve's
  peak instantaneous slope is normally steeper than the chord average) and is the same
  "continuously curved surface, typically tolerates a few degrees past 45 with adequate
  cooling" case the spec itself already names as a minor, non-blocking watch item for this
  same neighborhood -- not a new concern, and not severe enough to reject the fix.

**Result: PASS.** The neck-to-collar blend defect documented in Re-test Pass 2 is genuinely
fixed, confirmed independently using the exact same method that originally caught it broken --
this is a real fix, not a claim.

## R22. Base cleanliness and collar magnet pockets post-recovery (including the Extrude1 recreation) -- PASS, no regression from the participantBodies fix

Specifically relevant here since Extrude1 (the operation historically responsible for the
original cross-component-leakage defect) was recreated during this recovery:

- **Base**: bottom-cap vertex inspection (both STL and 3MF) shows the identical clean
  signature as every prior pass -- 77 vertices (STL) / 136 vertices (3MF), all at a single
  uniform radius of 49.00mm, zero interior vertices. The `participantBodies` restriction
  applied to the recreated Extrude1 did not introduce any new leakage or omission.
- **Collar magnet pockets**: 3 pockets confirmed present, radius 30.9-37.1mm (6.2mm diameter,
  34mm bolt circle), at 0 deg/120 deg/240 deg, spanning z=157.8-160mm (2.2mm deep) -- measured
  directly from raw mesh vertex coordinates, identical to every prior measurement of this
  feature across all three re-test passes.

**Result: PASS.** Both features that depend on Extrude1/the collar-thickening operation
survived the recreation intact and unchanged.

## R23. "Byte-identical to pre-incident" claim -- cannot independently confirm via hash; geometry checks above are the real verification, stated explicitly

Per the specific instruction to attempt a hash/byte comparison if meaningful, and to say so
explicitly if not: **I do not have a stored hash or byte size from the pre-incident export of
`urn-body`'s STEP/STL/3MF files to compare against.** The pre-incident export the Coder refers
to (with the neck-to-collar blend already fixed) happened in a round between my Re-test Pass 2
and this incident that I was not shown and did not independently capture a hash for -- so a
true byte-for-byte diff against that specific baseline is not something I can perform.

What I can and did do instead: independently re-derive every geometric claim from the current
files using different methods than a hash check (cross-sectional volume integration, dense
ray-casting, vertex-level inspection, slope-continuity analysis), and cross-check those against
my own independently-recorded numbers from Re-test Pass 2 where the underlying geometry should
be unchanged (cavity volume: matches to 5 significant figures; shoulder-region radii: match to
4 decimal places at every sampled point). **This is the real verification for this pass, and
it's a stronger check than a hash match would have been** -- a byte-identical hash only proves
the file wasn't altered in storage, whereas independently re-deriving the same geometric
figures from first principles proves the actual design intent survived the incident, which is
the thing that actually matters here.

## R24. Lid and neck-fit-test files -- confirmed genuinely untouched

No stored hash from prior passes to compare against (same limitation as R23), but strong
corroborating evidence was available and checked:

- `stl/urn-lid.stl`: 883,284 bytes, `3mf/urn-lid.3mf`: 715,749 bytes, `step/urn-lid.step`:
  65,834 bytes -- **exact byte-for-byte size match** to what was recorded in both prior
  re-test passes, at the **exact same filesystem timestamp** (12:01:38-39) recorded in both
  prior passes, predating both the collar-blend-fix round and this incident.
- `stl/neck-fit-test.stl`: 59,484 bytes, `3mf/neck-fit-test.3mf`: 27,804 bytes,
  `step/neck-fit-test.step`: 11,460 bytes -- same exact match, same exact timestamp (13:00),
  also predating both intervening rounds.
- `stl/urn-body.stl` and its siblings, by contrast, carry a fresh timestamp (17:38) and
  different byte sizes than every prior recorded state -- consistent with "only the body was
  touched by the incident and recovery."

**Result: PASS.** Identical file size and identical to-the-second filesystem timestamp across
two independent prior observations is not a cryptographic proof of byte-identity, but it is
strong, consistent, independently-checked evidence that these two files were never touched
during the incident or the recovery, exactly as claimed.


---
---

# RE-TEST PASS 4 -- spot-check after second manual-edit incident (collar/neck dragged outward)

Method note: per the task framing, this is a targeted spot-check against a reproduction of an
exact previously-verified target (not new geometry exploration), but every number below was
independently re-measured from the current `stl/urn-body.stl` and `3mf/urn-body.3mf` -- none
of it was accepted from the Coder's "matches prior verified state" claim alone. File timestamps
confirm the scope of the incident matches what was reported: `urn-body.*` re-exported at 21:35;
`urn-lid.*` and `neck-fit-test.*` unchanged (identical byte sizes AND identical timestamps to
every prior recorded measurement) -- consistent with "lid was checked from scratch and found
undamaged, only the body needed recovery."

## R25. Manifold check -- PASS

`stl/urn-body.stl`: watertight, winding-consistent, single connected component, Euler
characteristic 2, bounds identical to every prior verified pass (+-73.0mm XY, 0-160mm Z).
Shell volume: **293.1365 cm3 -- bit-for-bit identical** (same float value to 10 decimal places)
to the shell volume I measured in Re-test Pass 3, and same exact face/vertex count (47,298
faces / 23,651 vertices) as that pass. `3mf/urn-body.3mf`: watertight, single geometry,
consistent bounds, base-cap vertex count (136) matching prior passes exactly.

## R26. Collar ID/OD -- PASS, this is the specific thing that broke, given specific scrutiny

Sampled the collar cross-section at four heights within the collar band, away from the pocket
cuts and the rim edge (z=153, 155, 157mm): **exterior radius consistently ~38.98-38.99mm (OD
~78mm), interior bore radius consistently ~28.98-28.99mm (ID ~58mm)** at every sampled height.
This is the correct target, not the broken state (which had ballooned to ~35.34mm/~45.18mm
radius, i.e. ~70.7mm/~90.4mm diameter) -- the collar has genuinely been restored to spec, not
just visually "look right."

## R27. Magnet pockets -- PASS, correct size and position, not the abnormal ~3mm x ~1.9mm cuts from the incident

Direct vertex-level measurement in the top 2.2mm of the collar (z=157.5-160mm): **3 pockets,
radius range 30.90-37.10mm (i.e. centered on the 34.0mm bolt circle, 6.20mm diameter exactly),
at 0 deg / 120 deg / 240 deg**, depth confirmed via cross-section interior-count drop-off
(4 interior rings at z=157.8-159.9mm, down to 1 -- just the bore -- at z<=157.8mm, i.e. exactly
2.2mm deep). This is the full-size, correctly-positioned pocket, not the abnormal
~3mm-diameter/~1.9mm-deep cut the collar expansion had produced as a side effect. Base
cleanliness also re-confirmed unaffected: 77 vertices (STL) / 136 vertices (3MF), all at a
uniform 49.00mm radius, zero interior vertices.

## R28. Cavity volume and belly apex -- PASS, both bit-for-bit identical to the last verified state

- **Cavity volume: 1511.2683137624656 cm3** -- this is not just "close to" but **the exact same
  floating-point value**, to every digit, as what I measured independently in both Re-test
  Pass 2 and Re-test Pass 3 on the pre-incident geometry. Matches the Coder's reported 1511.8067
  cm3 to within the same ~0.03% mesh-resolution variance seen throughout this project.
- **Belly apex: exactly 73.000mm at exactly z=72.0mm (45.00% of height)** -- identical to every
  prior pass, no drift.

## R29. Neck-to-collar blend smoothness -- PASS, confirmed intact and unaffected by this recovery

Re-ran the same 0.1mm-resolution slope-continuity check used to originally catch this feature
broken (Re-test Pass 2) and to confirm it fixed (Re-test Pass 3). Spot-sampled radius values at
z=145.0, 145.1, 145.5, 147.0, 149.3, 151.0, 152.0mm all match my Re-test Pass 3 measurements
exactly (e.g. z=145.0: r=33.0000, z=152.0: r=39.0000, both exact). Largest single-step slope
change across the entire 145-152mm span: 0.2275 -- matching the smooth, no-discontinuity result
from Re-test Pass 3 (versus the ~0.95 instantaneous jump that characterized the original
chamfer defect two rounds ago). Peak local angle 45.56 deg from vertical, same as previously
measured. **This fix was not touched or degraded by the targeted collar/neck recovery.**

## Result: PASS on all 5 requested checks, independently re-measured

Given the unusually exact numeric matches (bit-for-bit identical shell volume and cavity
volume floats, identical face/vertex counts, identical radius values at spot-checked heights),
this reads as a genuine, faithful reconstruction from the same control-point/tangent recipe --
not merely "close enough" or "internally consistent." No residual damage from the second
incident was found anywhere checked.


---
---

# RE-TEST PASS 5 -- magnet-assisted closure removed entirely (subtractive change, both parts)

Method note: read the revised `specs.md` v3 (S6 rewritten, magnet hardware table deleted, collar
purpose re-labeled but geometry held fixed) before starting. Per the specific instruction not to
treat this as a trivial subtractive change given the collar/pocket region's history of three
manual-edit incidents, every claim below was independently re-measured from the current
`stl/urn-body.stl`, `stl/urn-lid.stl`, and both `3mf/` exports -- not accepted from the Coder's
internally-consistent math alone.

## R30. Manifold/watertightness -- PASS, independently re-run, not trusted from the Coder's self-report

Ran a direct edge-manifold check on both exported STL files (every edge in a valid printable
mesh must be shared by exactly 2 triangles) rather than relying on a single watertight flag:

- `stl/urn-body.stl`: watertight, winding-consistent, single connected component, Euler
  characteristic 2 (unchanged, correct closed-vessel topology). **Zero edges with a face-count
  other than 2**, checked across all ~46,900 faces.
- `stl/urn-lid.stl`: watertight, winding-consistent, single connected component, Euler
  characteristic 0 (correct -- the handle through-hole makes this a genus-1 solid, same
  topology class as every prior verified lid). **Zero edges with a face-count other than 2**,
  checked across all ~17,200 faces.
- Repeated the same edge-count check on **both slicer-ready 3MF files** (the files that
  actually matter for printing): zero non-2-count edges in either.

**Result: PASS**, confirmed by direct re-derivation, not by trusting the Coder's "from-scratch
watertightness check" claim.

## R31. Body: collar dims, belly apex, neck-to-collar blend, cavity volume -- PASS

- **Collar ID/OD**: sampled cross-sections at z=150/153/155/157/159mm -- exterior radius
  consistently ~38.98-38.99mm (OD ~78mm), interior bore radius consistently ~28.98-28.99mm (ID
  ~58mm) at every height. Matches spec exactly, unchanged from every prior pass.
- **Pocket removal genuinely complete, not just capped over**: swept the entire collar band
  (z=145-160mm, 0.5mm steps) checking for any interior loop beyond the single expected bore --
  **zero anomalies found anywhere in the band.** At z=159mm specifically (where 4 interior
  rings -- 1 bore + 3 pockets -- existed in every pre-removal pass), there is now exactly 1
  interior ring (just the bore). This confirms the pocket cavities are genuinely gone, not
  present-but-hidden or partially remaining.
- **Belly apex**: exactly 73.000mm at exactly z=72.0mm (45.00% of height) -- identical to every
  prior measurement, unaffected by this change (as expected, since the pocket removal shouldn't
  touch this region, but independently re-confirmed rather than assumed).
- **Neck-to-collar blend (z=145-152mm)**: re-ran the same 0.1mm-resolution slope-continuity
  check used in every prior pass to verify this fix. Spot-sampled radius values (z=145.0:
  33.0000, z=145.1: 33.0132, z=147.0: 34.4941, z=152.0: 39.0000) and the max slope-discontinuity
  metric (0.2275) are **identical to every digit** to my measurements from the last two passes.
  This region is completely untouched by the pocket-removal change, exactly as expected given
  the pockets were bored from the top rim face, not into this side-wall transition.
- **Cavity volume**: measured **1511.08 cm3** via cross-sectional integration, vs. the Coder's
  claimed-unchanged 1511.8 cm3 (0.048% difference) and my own pre-change measurement of 1511.27
  cm3 (0.013% difference). This is a slightly larger gap than the bit-for-bit-identical result
  I got in the pure-recovery passes, but still well within the normal mesh-tessellation noise
  band seen throughout this project (0.02-0.2% has been typical whenever the underlying B-rep
  is re-triangulated by Fusion after any feature-tree edit, even in regions that are
  dimensionally unaffected) -- **not concerning, and expected here specifically because,
  unlike the incident-recovery passes, the geometry actually did change this time** (a feature
  was genuinely removed from the tree), which changes the mesh discretization seed for the
  whole body even in untouched regions like the cavity walls.

**Result: PASS on all four sub-items**, independently re-derived.

## R32. Lid: new volume, handle through-hole, flat underside -- PASS

- **Volume**: shell volume measured **151.02 cm3** vs. the Coder's claimed 151.1556 cm3 (0.09%
  difference, same normal-noise band as above). Plausible and consistent with the claimed
  +0.1993 cm3 delta from the pre-removal 150.96 cm3 baseline (removing a blind pocket adds
  material, i.e. increases shell/material volume slightly, which is the correct direction).
- **Handle through-hole**: re-ran the same y-sweep method used in every prior pass. Opening
  present and open (a genuine air gap, not a cap) from y=-4mm to y=+4mm, absent beyond +-4.5mm,
  measuring exactly **22mm x 24mm** at the center slice -- unaffected by the underside pocket
  removal, as expected since these are unrelated features, but independently reconfirmed rather
  than assumed.
- **Flat underside, no pocket remnants**: inspected the underside face directly -- 99 vertices
  at z=0.00mm exactly, all at a uniform radius of ~50.0mm (the brim OD), and swept
  cross-sections from z=0 to z=2.75mm (covering the old pocket's full depth plus margin) finding
  **zero interior loops at every sampled height.** The underside is a genuine plain flat plane,
  not a plane with capped-over or partially-remaining pocket geometry.

**Result: PASS on all three sub-items**, independently re-derived.

## R33. No stray/orphaned geometry from the removal -- PASS, checked directly, not inferred from face-count arithmetic

Rather than just checking that the Coder's reported face-count deltas (14->8 body, 24->18 lid)
add up internally, I directly swept both parts' formerly-pocketed regions for any leftover
geometry:

- Body collar band (z=145-160mm): zero interior loops beyond the single bore, at every 0.5mm
  step across the full 15mm band -- no leftover pocket walls, no partial cuts, nothing
  resembling the original base-pocket-leak defect from the first incident in this project.
- Lid underside (z=0-2.75mm): zero interior loops at every 0.25mm step -- same result.
- Both parts confirmed single-connected-component (no orphaned disconnected fragments) and
  fully edge-manifold (R30) -- a stray or partially-cut pocket wall would very likely show up
  as either a non-manifold edge or a disconnected shell fragment, and neither was found.

**Result: PASS.** No evidence of stray geometry anywhere checked.

## R34. The "single-face-owned edge" claim -- investigated directly, assessed as benign, with an honest limitation noted

I don't have direct access to Fusion's B-rep edge/face adjacency data from outside the
application (this MCP's read tool doesn't expose a geometry/topology query), so I can't inspect
the *Fusion-side* edge ownership the Coder is describing directly. What I *can* and did check
is the thing that actually matters for printability: **does this manifest as a real defect in
the exported, slicer-ready mesh files?**

Ran a direct, from-scratch edge-manifold check (every edge must be shared by exactly 2
triangles) on both STL exports and both 3MF exports -- **zero non-2-count edges found in any of
the four files** (R30 above). I also independently checked the untouched `neck-fit-test.stl`
control body the Coder referenced as a baseline -- it likewise shows zero non-manifold edges,
consistent with the Coder's claim that it's a clean reference point unaffected by whatever
seam-curve artifact exists at the B-rep level.

**Assessment: this reads as genuinely benign, not a defect worth blocking on.** A NURBS
revolve seam (the parametric "wrap-around" line on a surface of revolution, similar to the
international date line on a globe) commonly produces a B-rep edge that is topologically
associated with a surface in an asymmetric way at the CAD-kernel level, without that having any
effect on the tessellated output mesh's manifold-ness -- and that is exactly what the direct
edge-count evidence here shows. I'm stating this as an assessment based on strong indirect
mesh-level evidence, not a first-hand confirmation of the B-rep-level claim itself, since I
don't have tooling to inspect the Fusion document's topology directly -- flagging that
distinction explicitly rather than implying more certainty than the evidence supports.

## Result: PASS on all requested items, independently re-verified

The magnet-pocket removal is a clean, complete, well-executed subtractive change on both parts.
No stray geometry, no manifold regressions, no effect on any unrelated feature (belly position,
neck-to-collar blend, handle through-hole all independently reconfirmed unchanged). The one
claim I could not directly verify (B-rep-level single-face-owned edges) is supported by strong
indirect evidence and assessed as benign, with that limitation stated explicitly rather than
glossed over.


---
---

# RE-TEST PASS 6 -- fuller belly + wall rebalance + neck/collar crease fix (4th manual-edit-related incident on this region)

Method note: full rigor per the director's specific instruction, not a quick pass. Every claim
below was independently re-derived from the current `stl/urn-body.stl` and `3mf/urn-body.3mf`,
using methods deliberately cross-checked against each other where a discrepancy showed up (see
R36 -- I caught and corrected my own methodology error mid-pass, the same `to_planar()`
translation-offset pitfall the original Reviewer's addendum in `review.md` independently
documented hitting earlier in this project).

## R35. Manifold/watertightness -- PASS

`stl/urn-body.stl`: watertight, winding-consistent, single connected component, Euler
characteristic 2 (correct topology, unchanged). Direct edge-manifold check (every edge shared
by exactly 2 triangles, not just the aggregate watertight flag): **zero non-2-count edges**
across all ~50,100 faces. `3mf/urn-body.3mf`: watertight, single geometry, base-cap vertex
signature consistent (134 vertices, uniform r=49.00mm). Shell volume 276.08 cm3 vs. the Coder's
claimed 275.9651 cm3 (0.04% difference, normal mesh-tessellation noise). Bounds
(+-76.95mm XY, 0-160mm Z) consistent with the claimed fuller belly. B-rep face count (9,
Fusion-native) is not independently checkable from exported mesh files -- noted honestly, as in
every prior pass, rather than assumed confirmed.

## R36. Belly apex and wall-offset tracking -- PASS, with one methodology note and one correction to the incoming figure worth flagging

**Wall-offset tracking (the more consequential check -- confirms no repeat of the 13.3mm
misalignment): strongly confirmed, PASS.** Measured outer and inner wall radius independently
at ~60 heights from z=15mm to z=142.5mm (every 2.5mm) using raw section-vertex radius
clustering (not `to_planar()`, see methodology note below). **Wall thickness holds at
3.98-4.03mm at every single sampled height across the entire belly and shoulder span** -- a
remarkably tight band, essentially the nominal 4.00mm everywhere, with no sign of the
outer/inner walls drifting apart or overlapping anywhere. Both walls independently peak at
exactly the same height (z=70.0mm in my sampling grid) -- direct, positive confirmation that
the rebalance genuinely fixed the 13.3mm vertical peak-misalignment described in the incident
report, not just reduced it.

**Belly apex position: radius confirmed almost exactly; the exact z is a broad, nearly-flat
plateau rather than a sharp point, worth stating plainly for anyone using this number
downstream.** Peak external radius measured at **76.956-76.957mm**, matching the Coder's
76.9660mm to within 0.013% -- solid agreement. But the surrounding curve is unusually flat: at
0.02mm sampling resolution, radius stays within 0.01mm of its maximum across a **~2.3mm-wide
band from about z=68.0mm to z=70.3mm** (unlike the sharp, unambiguous apex the pre-edit
tangent-constrained spline produced, where the true maximum was pinpoint-precise to the
sub-0.01mm level). The Coder's reported z=69.11mm falls squarely inside this plateau, so my
measurement does not contradict it -- but presenting "z=69.11mm" as a single precise figure
somewhat overstates the underlying curve's actual sharpness at that point. **Recommend
documenting this as "belly apex radius 76.97mm, occurring across a broad plateau roughly
z=68-70mm (~43-44% of height)" rather than a single decimal-precise z value**, so a future
editor doesn't mistake a flat region for a sharp control point.

**A concrete correction to flag for the record: the incident summary describes the height
position as "~50% of 160mm height."** Neither the Coder's own more precise figure (69.11mm =
43.2%) nor my independent measurement (68-70mm plateau = 42.5-43.9%) supports that -- the real
figure is **~43-44%**, i.e. the belly actually ended up very slightly *lower* than the
pre-edit 45% target, not higher toward 50%. This should be corrected wherever "~50%" gets
written into `specs.md`/`README.md`/`parameters.md`, not carried forward as-is.

**Methodology note for the record:** my first attempt at the wall-offset scan used
`trimesh`'s `Path3D.to_planar()` to separate exterior/interior polygon rings, and got a
wildly wrong "outer radius" (79.3mm vs. the true 76.96mm) at the belly. Root cause: `to_planar()`
returns coordinates in a 2D frame with a nonzero translation component (confirmed by inspecting
the returned transform matrix directly), so computing radius as `sqrt(x^2+y^2)` on those 2D
coordinates does not equal true distance from the part's central axis. This is the same
pitfall independently documented in `review.md`'s original approval pass ("an unconverted
local-frame projection that initially gave a false 75mm belly radius"). I caught it by
cross-checking against a second, independent method (raw 3D section vertices, radius computed
directly in world coordinates) before reporting a number, rather than reporting the first
result -- flagging this explicitly since it's now been independently hit by two different
reviewers on this same body at this same feature, which makes it worth a standing note: this
specific `trimesh` API is not safe to use for radius/distance-from-axis calculations on this
project without correcting for its translation offset first.

## R37. Neck-to-collar junction (z=140-152mm) -- PASS at practical/print-relevant resolution; one sub-visual, sub-print-resolution observation noted for completeness, not as a defect

Re-ran the same slope-continuity method used in every prior pass on this region, at multiple
resolutions:

- **At 0.1mm sampling (the resolution used in every prior pass on this exact feature, and
  finer than any realistic FDM layer height): the crease is genuinely gone.** Slope near
  z=140-145mm sits close to flat (-0.005 to +0.007), matching the Coder's claimed near-zero
  tail-end slope; the transition into the collar blend from z=145 onward ramps up gradually
  (0.13 -> 0.33 -> 0.43 -> 0.52 -> 0.63 -> 0.72 -> 0.78 mm/mm across 0.1mm steps) with the
  largest single-step slope-change measured at **0.1998** -- comparable to, and if anything
  slightly better than, the 0.2275 I measured on the already-fixed version two passes ago.
  Peak local angle (45.56 deg at z~149.3mm) and every spot-checked radius value (r=34.4941mm
  at z=147, r=39.0000mm at z=152) are **identical to the previously-verified fix**, confirming
  the outer wall's z=140-160mm tail is unaffected apart from the intended narrow splice near
  z=140-145mm.
- **At ultra-fine 0.02mm sampling (roughly 10x finer than the finest FDM layer height in
  common use, and about 100x finer than this shop's planned 0.16-0.2mm layers): a small,
  localized irregularity is visible right at z=140.00mm**, the exact tail-splice handoff point
  -- a discrete slope step of ~0.138 at that single point, versus a ~0.055 baseline step
  magnitude measured (same ultra-fine resolution) in a known-clean, already-verified-smooth
  region of the shoulder for comparison. This reads as a real, if very small, local artifact
  right at the splice seam -- but it is roughly two orders of magnitude below what any FDM
  printer could resolve (a full print layer spans 8-15x the z-distance over which this
  irregularity exists) and is not detectable at any sampling resolution coarser than ~0.05mm,
  including the 0.1mm resolution used for every practical assessment in this project so far.
  **Not treating this as a defect** -- it's included here for completeness and honesty about
  what "confirm the crease is genuinely gone" actually found at maximum measurement resolution,
  not because it changes the practical conclusion. The crease that was fixed this round was a
  ~15-20x larger-magnitude, multi-millimeter-wide, coarse-resolution-visible defect (the
  original hard chamfer); what remains at the splice seam is a sub-visual, sub-print-resolution
  residual that reads as smooth at every resolution that actually matters for this object.

**Result: PASS.** The crease is genuinely fixed at every resolution that matters for print
quality or visual appearance; a sub-print-resolution residual at the exact splice point is
noted for completeness, not flagged as a problem.

## R38. Collar dimensions, base cleanliness -- PASS, both unchanged

- **Collar**: outer radius 39.000mm (OD 78mm), inner bore radius 29.000mm (ID 58mm) at
  z=153/155/157/159mm -- exactly matching spec, unaffected by this round's changes (as
  expected, since neither the belly edit nor the tail-splice touched this region).
- **Collar band clean**: swept z=145-160mm at 0.5mm steps, zero anomalous interior loops
  anywhere -- consistent with the magnet-pocket removal from the prior round remaining intact.
- **Base**: 76 vertices, uniform r=49.00mm, zero interior vertices -- clean, matching every
  prior pass.

## R39. Cavity volume -- PASS, independently confirms the new ~1579 cm3 figure

Measured via cross-sectional integration (400 heights, floor-top to rim): **1578.11 cm3**, vs.
the Coder's claimed 1578.9824 cm3 -- a 0.055% difference, within the same normal
mesh-resolution noise band seen consistently throughout this project whenever a real B-rep
edit has occurred (as opposed to a pure re-export of unchanged geometry, which has produced
bit-for-bit-identical figures in past passes). **This independently confirms the ~1579 cm3
figure is solid and can be treated as authoritative** for documentation purposes -- this is
not a number that should be second-guessed further; two independent measurement methods (mine
and the Coder's Fusion-native mass-properties readout) agree to within normal tolerance.

## R40. Lid -- PASS, confirmed genuinely untouched

`stl/urn-lid.stl`: 861,684 bytes, `3mf/urn-lid.3mf`: 828,497 bytes, `step/urn-lid.step`:
60,805 bytes -- **exact byte-for-byte match** to every figure recorded in Re-test Pass 5,
watertight, same bounds (100x100x75mm), same face/vertex counts (17,232/8,616). No lid files
were re-exported this round (confirmed via filesystem timestamp, unchanged since Re-test Pass
5's magnet-pocket removal) -- consistent with the claim that this round's changes were entirely
scoped to the body.

## Summary of hard numbers, independently confirmed, for use in documentation

| Figure | Coder-reported | Independently measured | Status |
|---|---|---|---|
| Belly apex radius | 76.9660mm | 76.956-76.957mm | Confirmed (0.013% diff) |
| Belly apex height | z=69.11mm (43.2%) | broad plateau z~68-70mm (42.5-43.9%) | Consistent, but report as a plateau, not a sharp point; **correct any "~50%" language to ~43-44%** |
| Wall thickness through belly | ~4mm, min 3.90mm at claimed pinch point | 3.98-4.03mm at all 60 sampled heights z=15-142.5mm | Confirmed, tighter than the Coder's own worst-case figure |
| Neck-to-collar crease | Fixed | Fixed at every practically-relevant resolution; negligible sub-print-resolution residual at the exact splice point, noted not flagged | Confirmed |
| Collar OD/ID | 78mm/58mm | 78.000mm/58.000mm (measured 39.000/29.000mm radius) | Confirmed, unchanged |
| Base pockets | 0 | 0 | Confirmed, unchanged |
| Material volume | 275.9651 cm3 | 276.08 cm3 | Confirmed (0.04% diff) |
| Cavity volume | 1578.9824 cm3 | 1578.11 cm3 | Confirmed (0.055% diff) -- **this is the number to carry into documentation as the new accepted target/capacity** |
| Lid | Untouched | Byte-identical to last pass | Confirmed |


---
---

# RE-TEST PASS 7 -- v5 major revision: neck/collar widened 58mm->80mm ID, height trimmed, lid resized (5th manual-edit-related incident on this file)

Method note: full rigor per the director's explicit instruction -- this is the largest single
change to this file since the original build. Read the full revised `specs.md` (new/updated
S4.2.2, S4.3, S4.4, S5.1, S5.2, S6.2, S9, S13) before starting. Every number below was
independently re-derived from the current `stl/urn-body.stl`, `stl/urn-lid.stl`,
`stl/neck-fit-test.stl`, and their 3MF siblings -- none accepted from internal-consistency
checks alone.

## R41. Manifold/watertightness, all three parts -- PASS

Direct edge-manifold check (every edge shared by exactly 2 triangles) plus the standard
watertight/single-component/correct-Euler checks, on all three STL exports and all three 3MF
exports:

| Part | Watertight | Single component | Euler | Non-2-count edges | Bounds |
|---|---|---|---|---|---|
| `urn-body.stl` | Yes | Yes | 2 (correct, closed vessel) | 0 | +-76.96mm XY, 0-153.5mm Z |
| `urn-lid.stl` | Yes | Yes | 0 (correct, genus-1 handle) | 0 | +-61.0mm XY, 0-75mm Z |
| `neck-fit-test.stl` | Yes | Yes | 0 (correct, open tube) | 0 | +-72.0mm XY, 0-35mm Z |

All three 3MF exports (the actual slicer-ready files) independently re-checked with the same
method: zero non-manifold edges, consistent bounds with their STL siblings. **Result: PASS on
all three parts, both file formats, not trusted from self-report.**

## R42. Body -- belly apex unchanged, confirmed not disturbed by the height trim -- PASS

Fine cross-section scan (0.25mm steps, z=60-80mm): peak external radius **76.964mm at z=69.0mm**
-- matches the spec's claimed 76.97mm/unchanged-absolute-Z almost exactly, and the belly's flat
plateau (values within 0.02mm of the peak span z=68.25-70.0mm in my sampling) sits inside the
spec's documented 66.9-71.4mm plateau range. **Confirmed: the belly genuinely was not moved or
reshaped by the 6.5mm height trim** -- it sits at the same absolute height it did before this
revision, exactly as claimed.

## R43. Body -- shoulder, neck, collar dimensions -- PASS, exact matches at every checked point

Measured outer/inner radius directly (raw section-vertex radius clustering, not `to_planar()` --
see the standing methodology note from the previous pass about that API's translation-offset
pitfall) at the key control-point heights:

| Location | Z | Outer r (measured) | Inner r (measured) | Wall | Spec target |
|---|---|---|---|---|---|
| Shoulder (P2) | 112.5mm | **46.420mm** | **42.420mm** | **4.000mm** | 46.42mm ext (Reviewer-verified) / ~42.42mm int (spec's own flagged `ESTIMATED`, needing Coder re-verification) |
| Neck taper end (P3) | 138.5mm | **44.000mm** | **40.000mm** | **4.000mm** | 44mm ext (88mm OD) / 40mm int (80mm ID) |
| Collar (P4 band) | 150-153.4mm | **50.000mm** (constant) | **40.000mm** (constant) | **10.000mm** | 50mm ext (100mm OD) / 40mm int (80mm ID) / 10mm wall |

**Every single value matches its spec target to the third decimal place or better.** Notably,
the shoulder's internal radius -- flagged in `specs.md` S4.2.2 as an `ESTIMATED` figure
("flagged explicitly for the Coder to re-verify the true internal shoulder radius against the
actual rebuilt geometry") -- is independently confirmed here at **exactly 42.420mm**, matching
the spec's estimate to the third decimal. **This closes out that flagged estimation risk: the
42.42mm figure can be upgraded from `ESTIMATED` to `VERIFIED` in the next spec pass.** The
Coder's claim that "wall measured exactly 4.000mm there, validating this figure" is
independently confirmed true, not just internally self-consistent.

## R44. Body -- base cleanliness and collar-band cleanliness -- PASS

- Base: 76 vertices at z=0, all at a uniform radius of 49.00mm (98mm OD, unchanged as claimed),
  zero interior vertices -- the magnet-pocket removal from two revisions ago remains intact and
  undisturbed by this round's changes.
- Collar band (z=138.5-153.5mm): swept at 0.5mm steps, zero anomalous interior loops anywhere --
  no residual pocket geometry, no leftover features from the resize.

## R45. Body -- cavity volume, the number most worth scrutinizing -- PASS

Measured via cross-sectional integration (400 heights, floor-top to rim): **1579.31 cm3**, vs.
the Coder's claimed 1580.25 cm3 (0.06% difference, well within the normal mesh-resolution
tolerance band this project has consistently shown between independent mesh-based measurement
and Fusion-native mass-properties queries). **This independently confirms the cavity volume is
solid** -- both the spec's own hand-calculated estimate (~1578.6 cm3, via the frustum-delta
method) and two independent CAD-based measurements (Coder's and mine) now agree to within
~0.1% of each other and to within 0.08% of the ~1579 cm3 target. This is a genuinely
well-executed piece of geometry work given it required tuning spline tangent scaling after a
first-pass construction reportedly came in 6.25% off -- the final result lands the volume
essentially dead-on target, independently confirmed.

## R46. Body -- neck-to-collar blend overhang angle -- PASS, independently re-measured with a striking cross-check against the prior revision

Re-ran the same slope-continuity method used in every prior pass on this feature, now relocated
to z~138.5-146mm per the v5 profile:

- **Peak local slope-angle: 45.56 deg from vertical, at z=143.04mm** (fine 0.02mm-resolution
  scan). This is close to, though not identical to, the Coder's independently-measured 45.81 deg
  -- both comfortably inside the spec's own estimated ~47.25 deg and the "same low-risk band"
  framing, and both gentler than the spec's own reasoned-from-invariance estimate.
- **Notable independent cross-check, not something I went looking for but worth reporting
  plainly:** the peak slope value I measured here (1.0198915009043685, angle 45.56421951834084
  deg) is -- to 10 significant figures -- **the same number I independently measured on the v4
  (pre-widening) collar blend two revisions ago** (1.0198915009041667, 45.56421951833517 deg).
  This is a striking, unprompted confirmation of `specs.md` S9's own reasoned argument: "the
  radius delta driving this blend is unchanged at 6mm... holding the blend's height span
  unchanged too... the same construction method applied to the same (Delta r, Delta z) inputs
  produces the same curve shape... the peak overhang angle is therefore expected to stay ~47.25
  deg, just relocated." The blend's peak angle didn't just end up "close to" its predicted value
  by coincidence -- it is mathematically identical (to floating-point precision) to the
  pre-widening blend, exactly as the geometric-invariance argument predicted. This is about as
  strong a confirmation of that specific piece of spec reasoning as independent measurement can
  provide.
- No kinks found: max single-step slope-change across the whole z=137-154mm span is 0.1998,
  consistent with a genuinely smooth curve (versus ~0.95 for the original, since-fixed hard
  chamfer defect from several revisions ago).
- Self-supporting monotonicity confirmed on both flanking segments: belly-to-shoulder
  (z=69-112.5mm) and shoulder-to-neck-taper (z=112.5-138.5mm) both show **zero locally-increasing
  radius steps** at 0.5mm sampling resolution -- both remain in the shrinking-cone,
  self-supporting-regardless-of-angle class, confirmed directly rather than assumed from the
  spec's own reasoning.

**Result: PASS**, independently confirmed, not just accepted on the Coder's own "independent"
measurement.

## R47. Lid -- brim OD, dome base OD -- PASS

- Brim OD: measured **122.00mm** exactly (r=61.0mm at z=0, flat through z=0.1-3.0mm before the
  edge fillet begins) -- matches spec exactly.
- Dome base OD: the dome is a continuous curve with no sharp "base" transition point (expected,
  it's a dome), but sampling right around where the brim's edge fillet hands off into the dome
  proper (z~7.5mm) gives **r=48.64mm (97.3mm OD)** -- matches the Coder's claimed ~97.2mm to
  within 0.1mm, and is close enough to the ~98mm target that I agree with the director's framing
  that this is "close enough," not worth another pass. The ~0.7mm gap is well inside any
  reasonable tolerance for an `ESTIMATED` aesthetic ratio-preservation figure.

## R48. Lid -- handle through-hole integrity post-scale -- PASS, verified directly, not assumed from "unchanged"

This was specifically flagged as needing direct verification since the lid was built via a
non-uniform Scale feature (X=Y=1.22, Z=1.0) applied before the handle/plinth features -- a
scale-adjacent operation is exactly the kind of change that could silently squash or cap an
opening if the scale boundary or feature order were off by even one step. Swept the mesh across
the loop's full depth (y=-8mm to +8mm): opening present (a genuine 2-boundary-loop cross-section,
meaning open air) from **y=-4mm to y=+4mm**, cleanly absent (solid, 0 interior loops) beyond
+-4.5mm -- and measured the opening itself at the center slice as **exactly 22mm x 24mm**,
identical to every prior verified figure for this feature across the entire project. **The
non-uniform scale (applied before the handle features, per the Coder's report) did not touch
the handle at all** -- confirmed directly, not inferred from feature-order description alone.

## R49. Lid -- total height, manifold -- PASS

Bounds confirm z=0 to 75.0mm exactly -- unchanged, as claimed. Manifold/watertight status
covered in R41.

## R50. `neck-fit-test` article -- PASS, correctly rebuilt at the new dimensions, self-supporting

This is the file the requester will actually print for a physical go/no-go decision, so it got
the same scrutiny as the body:

- **ID confirmed 80mm** (r=40.000mm, constant from z=20.5mm to the top).
- **Neck OD confirmed 88mm** (r=44.0-44.4mm around z=20.5mm, matching the P3 handoff).
- **Collar OD confirmed 100mm** (r=50.000mm, constant z=28-35mm).
- **Wall thickness confirmed ~4.00mm** through the flange-to-neck taper (z=0.5-18mm, matches the
  main body's own wall convention).
- **Self-supporting confirmed**: the flange-to-neck taper (z=0.5-20mm) shows zero
  locally-increasing radius steps (shrinking-cone class, self-supporting regardless of angle).
  The collar-widening blend (z=20-28mm) peaks at ~40.6 deg from vertical -- under the 45 deg
  guideline, and consistent with this same test article's own blend construction measured in
  earlier revisions (this article appears to use a simpler blend than the main body's
  tangent-matched one, but it's comfortably within the safe range either way).
- **Single valid manifold solid**, confirmed in R41.

**Result: PASS.** This is a valid, correctly-dimensioned, self-supporting article, ready for the
requester to actually print and use for the physical neck-opening test -- and critically, it now
represents the *correct* (80mm ID) geometry, closing out the gap the spec explicitly flagged
("if this file is left at its old dimensions, the requester's physical fit test will validate
the wrong opening size").

## R51. File-location / path-bug check -- PASS, no stray or misplaced files found

Per the Coder's report of catching and fixing a path bug that initially dumped files in the
wrong folder, searched the entire repository for any stray copies of `urn-body`, `urn-lid`, or
`neck-fit-test` files outside the canonical `step/`, `3mf/`, `stl/` locations: **none found**,
aside from the already-accounted-for `archive/v2-with-magnet-pockets/` folder from an earlier,
unrelated revision. All 9 files in the canonical locations share the same export timestamp
(08:27, this round), confirming they are the current, final versions -- not stale leftovers from
before the path-bug fix.

## R52. Base-vs-collar visual proportion -- PASS, confirmed via a live Fusion screenshot, not just the dimensional check

Took a live screenshot of the actual current body from a side-on view. The belly is clearly and
unambiguously the widest, most visually dominant feature of the silhouette; the base and collar
read as comparably narrow at each end, consistent with the dimensional check (98mm base vs.
100mm collar OD, effectively at parity) rather than either end looking flared or top-heavy
relative to the other. The neck-to-collar region also reads as smoothly rounded in this render,
visually consistent with the numeric slope-continuity findings in R46 (no visible crease).

## Summary table -- hard numbers for documentation

| Figure | Coder-reported | Independently measured | Status |
|---|---|---|---|
| Body height | 153.5mm | 153.5mm (exact bounds) | Confirmed |
| Belly apex radius / height | 76.966mm / z~69.11mm | 76.964mm / z=69.0mm (plateau) | Confirmed |
| Shoulder ext/int radius | 46.42mm / 42.42mm | 46.420mm / 42.420mm | Confirmed exactly, closes the `ESTIMATED` flag on the internal figure |
| Neck OD/ID | 88mm/80mm | 44.000mm/40.000mm radius (exact) | Confirmed |
| Collar OD/ID | 100mm/80mm | 50.000mm/40.000mm radius (exact) | Confirmed |
| Cavity volume | 1580.25 cm3 | 1579.31 cm3 | Confirmed (0.06% diff) |
| Neck-to-collar peak angle | 45.81 deg | 45.56 deg (bit-identical to the pre-widening v4 blend) | Confirmed, same low-risk band |
| Lid brim OD | 122mm | 122.00mm (exact) | Confirmed |
| Lid dome base OD | ~97.2mm | ~97.3mm | Confirmed, close enough |
| Lid handle opening | 24x22mm, unchanged | 24x22mm, present y=-4 to +4mm | Confirmed, unaffected by the scale |
| neck-fit-test ID/OD | 80/88/100mm | 80.000/88.0-88.8/100.000mm | Confirmed |
| Base pockets | 0 | 0 | Confirmed |
| Single manifold solid (all 3 parts) | Yes | Yes, zero non-manifold edges | Confirmed |


---
---

# RE-TEST PASS 8 -- v6 candidate: lid-underside alignment plug (Option A, straight-walled, hollow)

Method note: read `specs.md` S5.2.1 in full (the two-option analysis) before starting. Every
number below was independently re-derived from the current `stl/urn-lid.stl` and
`3mf/urn-lid.3mf`, cross-referenced against a fresh re-measurement of the untouched
`stl/urn-body.stl` for the collision/clearance checks (not taken from memory of prior passes).

## R53. Manifold/watertightness -- PASS

`stl/urn-lid.stl`: watertight, winding-consistent, single connected component, Euler
characteristic 0 (correct -- still genus-1 from the handle through-hole; the plug, being a
blind-ended hollow tube open only at its tip, doesn't add a second through-hole/change the
genus). Direct edge-manifold check: **zero non-2-count edges** across all ~18,100 faces.
`3mf/urn-lid.3mf`: watertight, single geometry, zero non-manifold edges, consistent bounds.
Overall part bounds now z=0 to 85mm (confirmed exactly = 75mm original lid + 10mm plug), with
the coordinate origin evidently redefined so z=0 is the plug tip -- consistent with the
"plug-tip-down" print orientation.

## R54. Wall thickness / plug geometry -- PASS, exact match

Measured outer/inner radius directly at 10 heights through the plug (z=0 to z=9.9mm): **constant
39.750mm outer / 35.750mm inner at every sampled height, wall = 4.000mm exactly, unchanged
across the full depth** -- true concentric cylinders, no taper, matching Option A's spec exactly.
The plug's bottom edge (z=0, the tip) has vertices *only* at r=35.75mm and r=39.75mm -- confirming
the tip is a genuine open ring (hollow, open to the outside), not capped.

## R55. Single valid manifold solid -- confirmed, see R53 (both STL and 3MF)

## R56. Collision check against the body's internal taper -- PASS, independently confirmed using real geometry of both parts

- Re-measured the (untouched) body directly rather than trusting it was unaffected: P3
  (neck-taper-end) at **z=138.5mm measures outer=44.000mm / inner=40.000mm**, and the collar band
  (z=145.5-153.4mm) measures a constant **outer=50.000mm / inner=40.000mm** -- both identical to
  every prior independent measurement in this project, confirming the body file is genuinely
  untouched.
- Body's own bounds confirm total height still exactly 153.5mm (rim/P4 at z=153.5mm).
- Plug depth independently measured at exactly 10.0mm (R54). Since the lid's flat underside/
  seating plane sits at body-Z=153.5mm when assembled (resting on the rim), and the plug hangs
  10.0mm below that seating plane, **the plug tip lands at body-Z = 153.5 - 10.0 = 143.5mm** --
  matching the claimed figure exactly, combining two independently-verified real measurements
  (not two nominal design figures).
- **Margin: 143.5mm - 138.5mm (P3) = 5.0mm**, confirmed. No collision with the internal
  taper/shoulder transition.

**Result: PASS**, confirmed against actual as-built geometry of both parts, not nominal-vs-nominal
arithmetic.

## R57. Clearance -- PASS, confirmed against real geometry of both parts, not nominal-vs-nominal

- Plug OD, measured: **79.500mm** (2 x 39.750mm, R54).
- Body bore ID at the engagement depth (z=138.5-153.5mm, the full constant-ID zone), measured:
  **80.000mm** (2 x 40.000mm, R56) -- constant throughout, confirmed at multiple heights.
- **Diametral clearance: 80.000 - 79.500 = 0.500mm exactly**, confirmed against the real,
  independently-measured geometry of both parts, matching the claimed figure precisely.

## R58. Handle -- PASS, verified directly (the hard constraint), not trusted from "unaffected" framing

Per the specific instruction not to trust "unaffected" on the project's hard constraint, swept
the loop's full depth exactly as in every prior pass: opening present (2-boundary-loop
cross-section, genuine open air) from **y=-4mm to y=+4mm**, cleanly absent beyond +-4.5mm, and
measuring **exactly 22mm x 24mm** at the center slice -- bit-for-bit identical to every handle
measurement recorded across this entire project. **The plug addition (a lid-underside-only,
purely additive feature per the spec's own framing) genuinely did not touch the handle in any
way.**

## R59. Independent assessment of the enclosed internal bridge -- this is the important one, and I don't think "cosmetic non-issue, watch cooling" is the complete picture

**First, confirming the geometry itself, independently, not taken on the Coder's description:**
cross-sectioned the plug region at fine z-resolution and found the transition precisely: at
z=9.99mm, the cross-section still shows 1 interior loop (hollow, r_min=35.750mm -- material
only in the ring from 35.75-39.75mm). At **z=10.00mm exactly, the interior loop disappears
entirely (0 interiors, fully solid from r=0 to r=61mm)**. This confirms the hollow plug cavity
is capped by the flat underside of the solid 5mm-thick brim disc itself -- a genuinely
fully-enclosed void, 71.5mm in diameter (2 x 35.75mm), 10mm tall, anchored around its entire
perimeter by the 4mm-thick plug wall, open only at the tip 10mm below. The geometry claim is
accurate.

**My independent technical assessment, since a real opinion was specifically requested:**

I don't think "cosmetic non-issue, watch cooling/bridging speed" is the complete picture, though
I agree with the underlying conclusion that this shouldn't block the design. Two things need to
be said separately: **how likely is this to print imperfectly**, and **does that actually
matter**.

- **Likelihood of an imperfect bridge: real, not negligible, even with full-perimeter
  anchoring.** A 71.5mm-diameter unsupported horizontal span is well beyond what FDM printing is
  commonly considered reliably capable of bridging cleanly -- community and slicer-vendor
  guidance for confident, clean bridging on a well-tuned consumer printer typically tops out
  somewhere in the 40-50mm range even for PLA, which bridges noticeably better than most other
  common filaments. **This lid is PETG**, which is generally regarded as a *weaker* bridging
  material than PLA (higher melt viscosity, more elastic/slower-to-set behavior when hot, more
  prone to gradual sag across a span rather than staying taut) -- this compounds the size risk
  rather than offsetting it. Full-perimeter anchoring is a genuine, real mitigating factor (it's
  meaningfully better than a two-sided bridge), but it does not change the fact that the
  *center* of a 71.5mm circular span is roughly twice the distance from any anchor point that
  this project's own established ~45-50mm comfort zone would suggest is safe. I would expect a
  visible dip/sag and likely some stringing on the first bridging layer(s) under default or
  naive slicer settings, not a clean flat ceiling.
- **Does it matter: no, for exactly the reason the Coder gives -- but only because it's both
  hidden AND non-functional, not because the print risk itself is small.** This surface is
  fully enclosed, invisible once assembled, and structurally disconnected from anything the
  plug's fit/function or the object's outer finish depends on. A sagged, stringy, or even
  partially-incomplete ceiling here has no cosmetic or functional consequence I can identify --
  it doesn't touch the plug's OD (the fit-critical surface), doesn't touch any visible face, and
  doesn't sit anywhere near the object's structural load path. **My assessment: treat this as a
  real, likely-to-be-imperfect bridge, not a low-probability edge case -- but one whose
  consequence is genuinely contained to zero visible or functional impact, which is what
  actually justifies not blocking on it.** The Coder's practical bottom line (don't block, note
  it) is right; the framing ("cosmetic non-issue... watch cooling") understates the print-quality
  probability while landing on the correct real-world consequence.

**One concrete risk I don't see raised anywhere yet, worth flagging explicitly:** if the
operator's slicer is set to generate supports **"everywhere"** rather than **"support on build
plate only"** (a real, commonly-toggled setting, and not always the default), the slicer may
dutifully attempt to generate support material *inside* this fully sealed 71.5mm void to hold up
the bridge -- support that can **never be removed or accessed** once printed, since the cavity is
completely closed off after the first layer(s) of the ceiling print over it. This wouldn't be a
functional failure (the trapped material is inert, hidden, and disconnected from the urn's usable
cavity, so at worst it's a bit of rattling debris sealed inside a lid nobody will ever open into),
but it's a genuinely non-obvious gotcha specific to this new feature that's worth a one-line
callout in whatever slicer guidance ships with this design: **confirm supports are set to
"touching build plate only" before slicing the lid**, both to avoid wasted/trapped material and
because support generated in a spot this deep inside a mostly-enclosed geometry is also more
likely to be poorly formed in the first place.

**On the director's specific question -- would a tilt angle help both overhang zones at once?
No, I don't think so, and here's the reasoning:** tilting the whole part would help the
*internal bridge* specifically (a flat horizontal disc tilted past ~45 deg behaves like a
self-supporting sloped surface instead of a flat span, using the same self-supporting-angle
logic this project has relied on throughout) -- but the **outer support annulus is a
discontinuous vertical step** (Δr=21.25mm within a single layer transition, not a sloped
surface), and tilting a part doesn't convert a literal step/cliff into a self-supporting slope
the way it does for an already-sloped or curved surface -- the shelf still needs support directly
beneath it at essentially any orientation. Worse, any tilt large enough to meaningfully help the
internal bridge would **reintroduce overhang risk on the dome and handle**, both of which were
specifically oriented flat-underside-down to get zero overhang on those *visible, functional*
surfaces. Trading a hidden, consequence-free bridge risk for a new overhang risk on visible
geometry is the wrong trade. **My recommendation: keep the flat, plug-tip-down orientation as
planned, and handle the internal bridge with slicer-level settings specific to that one z-band**
(maximum cooling fan, reduced print speed for that layer range, and possibly a slightly increased
bridge flow/multiple-thin-perimeter setting if the slicer supports it) rather than a whole-part
tilt -- this is the standard, lower-risk way to manage a single problematic bridge region without
disturbing an otherwise well-optimized orientation.

## R60. Oversize compensation / test-coupon recommendation -- agree, and independently corroborated by this project's own history

The Coder's claim that no unauthorized oversize compensation was added (built to spec'd nominal
79.5mm/80.0mm exactly) is corroborated by R57's direct measurement -- the clearance came out at
exactly the nominal 0.500mm, not a pre-padded or silently-adjusted value.

**I agree with the recommendation to print a clearance-test coupon before the full lid print,
and would put it slightly more strongly than a general good-practice suggestion:** FDM parts
systematically tend to print internal bores slightly undersized and external bosses/plugs
slightly oversized relative to nominal CAD dimensions (a mix of inward corner rounding, extrusion
overlap compensation, and general dimensional shrinkage/tolerance stack-up) -- meaning the
*realized* clearance on a real print is more likely to end up **tighter than 0.5mm than looser**,
not a coin-flip in either direction. Combined with the named PETG-plug/PLA-body
material-shrinkage-mismatch risk already flagged in the spec, this is a real, directionally
biased risk (toward "too tight," specifically), not a generic disclaimer -- a test coupon is the
right call before committing an ~85mm-tall, multi-hour PETG print to an untested fit.


---
---

# RE-TEST PASS 9 — v7 major lid revision (plug capped, handle removed, brim thickened+shrunk, dome apex flattened)

Method note, this pass: independent measurement was done against `stl/urn-lid.stl` and
`3mf/urn-lid.3mf` (both re-exported this round) using `trimesh` (cross-sectioning at fine Z
resolution, face-adjacency-angle crease detection, connected-component/watertightness analysis)
**and, new this round, direct text-level parsing of `step/urn-lid.step`'s native B-rep entities**
(`ADVANCED_FACE`, `CLOSED_SHELL`, `BREP_WITH_VOIDS`, `SPHERICAL_SURFACE`, `TOROIDAL_SURFACE` and
their `CARTESIAN_POINT` placements) to get exact analytic parameters rather than mesh-approximated
ones — this was necessary for the dome-math check below, which needs exact sphere/torus
parameters, not tessellated estimates. `stl/urn-body.stl` and `stl/neck-fit-test.stl` were also
re-checked (not just trusted as "unaffected") since a body-fit claim (the plug/bore clearance) is
being re-verified this round. No slicer was available in this environment (Bambu Studio is
installed but GUI-only, no headless CLI path found in this sandbox) — overhang/support assessment
is geometric (radius-monotonicity sweep + mesh crease detection), not a real sliced preview.

## 0. Blocking-check status carried forward — still open, unaffected by v7

The neck-opening-vs-real-remains-bag `ESTIMATED` dimension (§4.4, edge case 2) remains
**unresolved and unaffected by this round** — v7 is lid-only, the body/neck were not touched, and
the `neck-fit-test` article was not re-exported (confirmed by timestamp: still 2026-08-31, and its
own bounding box, 143.97×143.98×35mm, matches the v5 figures exactly, re-measured this pass on
`stl/neck-fit-test.stl`). **This is still the single most load-bearing open item in the whole
project and this pass does not close it.** Nothing new to add here; restated per the instruction
to check for unresolved `ESTIMATED` hardware-mating dimensions before anything else, not to let it
quietly age out of the record because five lid changes are landing in the same round.

## R61. Plug geometry (capped tip) — PASS, all claimed numbers independently confirmed exactly

Cross-sectioned `stl/urn-lid.stl` at 0.01–1mm resolution from Z=0 (bed) to Z=10 (seating plane):

- **Z=0 to Z≈3.99mm: fully solid**, single circular boundary at r=39.750mm (outer OD only, no
  interior loop) — confirms a genuine solid tip cap, not a thin-walled dome or shell standing in
  for "solid."
- **Z=4.01mm to Z=9.99mm: hollow**, two concentric boundaries at r=39.750mm (outer) and
  r=35.750mm (inner) at every sampled height — constant **4.000mm wall**, exact match to spec.
- **Solid/hollow transition sits at Z=4.0mm exactly** (6mm hollow + 4mm solid tip = 10mm total)
  — matches the claimed split exactly, not approximately.
- **Plug OD is a true, constant-diameter vertical cylinder for its full 10mm depth** (39.75000mm
  at every one of 100 sampled heights, zero deviation beyond mesh-tessellation noise at the 5th
  decimal) — genuinely zero-overhang on its own wall, as claimed.
- Bottom face (Z=0.000mm exactly, confirmed against the mesh's own bounding box) is the tip cap
  — this is the literal bed-contact layer in the specified print orientation, confirmed by
  construction (solid material starts at Z=0, no void beneath it), not just asserted.

## R62. Brim/plug/dome key dimensions — PASS, all headline figures confirmed

| Dimension | Claimed | Independently measured | Method | Verdict |
|---|---|---|---|---|
| Plug OD | 79.500mm | 79.500mm (39.750×2) | mesh cross-section, Z=0–10 | PASS, exact |
| Plug ID (hollow) | 35.750mm | 35.750mm | mesh cross-section, Z=4–10 | PASS, exact |
| Plug wall | 4.000mm | 4.000mm | derived from above | PASS, exact |
| Plug/hollow split | 6mm hollow + 4mm solid | 6.0mm / 4.0mm (transition at Z=4.0mm) | mesh cross-section | PASS, exact |
| Brim OD | 99.700mm | 99.700mm (49.850×2) | mesh cross-section, Z=10–17 (flat wall region) | PASS, exact |
| Total lid height (seating plane to plateau top) | 39.000mm | 39.000mm (Z=10 to Z=49) | bounding box + seating-plane Z | PASS, exact |
| Total lid bounding-box height | 49.000mm | 49.000mm (Z=0 to Z=49) | `mesh.bounds` | PASS, exact |
| Plateau diameter | 17.70mm | **17.7012mm** (r=8.85061mm) | mesh vertices at Z=49 (43 verts, single exact radius) **and** STEP torus #17 major-radius parameter (8.85061203mm) — two independent methods, bit-identical | PASS, exact |
| Combined assembled height | 192.500mm | 192.500mm (body 153.500mm, re-measured on the untouched body STL, + lid 39.000mm) | mesh bounding boxes, both parts | PASS, exact |
| Lid material volume | 192.5274 cm³ | 192.2807 cm³ (3MF) / 192.2838 cm³ (STL) | `trimesh.volume` (signed-tetrahedra, divergence theorem) | PASS within 0.13% — expected, see note below |

**Note on the 0.13% volume delta:** mesh (STL/3MF) volumes are computed from a tessellated
(faceted) approximation of curved surfaces, which for convex outward curves always sits slightly
*inside* the true analytic surface (chords vs. arcs) — a small systematic under-measurement versus
a CAD kernel's exact analytic volume is expected and is not a discrepancy worth chasing further.
The direction (mesh < analytic) is exactly what this systematic effect predicts.

**Cross-check against the archived pre-v7 lid, using the same method both times (not
cross-method bias):** `archive/pre-v7-handle-removal/urn-lid.stl` measures **228.4522 cm³** via
the identical `trimesh.volume` method. `(228.4522 − 192.2838) / 228.4522 = 15.84%` reduction —
matches the claimed "-15.8%" almost exactly, using a same-method comparison rather than mixing a
mesh figure against a CAD-reported one.

## R63. The 2-connected-components finding — independently re-derived from first principles, not just checked against the Coder's explanation. **This is confirmed correct, not a rationalization of a defect.**

This was flagged as the most important thing to get right this round, so it was checked two
independent ways, at two different levels of the data (tessellated mesh **and** native B-rep),
plus a differential check against the pre-cap archive.

**Method 1 — mesh-level (`trimesh.split`)**, on `stl/urn-lid.stl`:
- `mesh.is_watertight` = **True** (the *whole* mesh is watertight — components being separate
  does not mean broken/non-manifold).
- `mesh.split(only_watertight=False)` → **exactly 2 components**, both individually watertight:
  - Component A: bounds `z=[4,10]`, `r≈35.75mm` — **volume = −24.070 cm³** (negative — see below).
  - Component B: bounds `z=[0,49]`, full outer envelope — **volume = +216.354 cm³**.
  - Sum: 216.354 − 24.070 = **192.284 cm³**, matching the whole-mesh volume exactly.
- The magnitude of Component A (24.07 cm³) matches the analytically-expected volume of the sealed
  hollow void almost exactly: a cylinder r=35.75mm, h=6mm → π×35.75²×6 = **24.085 cm³** (0.06%
  off, pure tessellation noise). **Component A is the void's own boundary shell, not stray
  geometry** — its location (z=4–10, r=35.75) is exactly the hollow interior of the capped plug,
  bounded below by the new solid tip cap and above by the brim's underside.
- The negative sign on Component A's standalone volume is exactly what you'd expect for a
  correctly-oriented internal-void shell: its face normals point *outward from the void* (i.e.
  *into* the material), which is the opposite convention from a standalone exterior shell's
  normals (pointing away from the material) — when trimesh's divergence-theorem volume formula is
  applied to this shell *in isolation* as if it were its own solid, that reversed-relative-to-a-
  standalone-body orientation is exactly what produces a negative number. Summed with the outer
  shell (correct convention: outer volume minus void volume = net material volume), it gives the
  right net material volume. **This is not a symptom of bad topology — it's the textbook signature
  of a manifold hollow object represented as two disjoint closed shells.**

**Method 2 — B-rep-level, `step/urn-lid.step` (the authoritative CAD data, not a tessellation)**:
- `ADVANCED_BREP_SHAPE_REPRESENTATION`: **1** — one solid shape representation in this file, not two.
- `BREP_WITH_VOIDS(`: **1** — this is the STEP entity name *specifically* used to represent a
  solid B-rep with one or more internal void shells, as opposed to `MANIFOLD_SOLID_BREP` (used for
  a solid with no internal voids, and correspondingly absent from this file — 0 occurrences).
  **The CAD kernel itself classified this part as "one solid with an internal void" at export
  time — this isn't an interpretation I'm applying after the fact, it's what the file says it is.**
- `CLOSED_SHELL(` count: 2, referenced as `#157` (3 faces: `#144,#145,#146` — matches a void shell
  made of {floor plane, inner cylindrical wall, ceiling plane}) and `#158` (10 faces — the outer
  shell: everything visible from outside, tip bottom, plug OD wall, brim, dome sphere, plateau,
  and the three fillet toruses). `#157` is wrapped in an `ORIENTED_CLOSED_SHELL(...,.F.)` at line
  34 — exactly the construct used to attach a void shell (with orientation) inside a
  `BREP_WITH_VOIDS`. 3+10 = 13 faces total, matching `ADVANCED_FACE(` count = 13 exactly.
- **Conclusion: one topological solid, by the CAD kernel's own native classification, with one
  outer shell and one internal void shell. This is definitionally what "2 mesh components" should
  look like for a correctly capped hollow feature — it is not possible for a genuinely correct
  sealed-cavity capping to produce anything other than 2 disjoint shells at the mesh level**, since
  a sealed interior surface has no shared edges with the exterior surface once there's no opening
  connecting them.

**Method 3 — differential check against the pre-cap archive, confirming the signature actually
changed the way the theory predicts (not just checking the new file in isolation):**
`archive/pre-v7-handle-removal/urn-lid.stl` (the v6 lid, open-tip plug, handle still present) —
`mesh.split()` → **1 component only**, `is_watertight=True`, `euler_number=0` (the 0, not 2,
reflects the handle's through-hole loop, genus 1 — expected and unrelated to this check).
**Before capping, the void was open to the outside air through the tip, so the "void's boundary"
and the "outer boundary" were never separate — they're the same continuous connected surface,
reached by walking through the open hole.** After capping, they become topologically disjoint.
**This is exactly the predicted before/after signature change, independently confirmed on the
actual archived file, not just reasoned about abstractly.**

**Verdict: the Coder's and Reviewer's explanation is correct. 2 components is the correct,
expected, unavoidable signature of a sealed internal cavity in this specific case, verified three
independent ways (tessellated-mesh split, native B-rep entity classification, and a differential
before/after check against the real archived pre-cap file). This is not a fragmentation defect,
and treating it as one would be a false alarm.**

## R64. Handle removal — PASS, confirmed via full face-inventory audit, not trusted from "unaffected"

Per the instruction not to accept "unaffected" claims on a project hard-constraint feature without
direct re-verification: swept the entire mesh and the entire STEP face list, not just the region
where the handle used to be.

- `stl/urn-lid.stl`: **exactly 2 connected components** (accounted for fully in R63 above — one
  outer shell, one void shell). **There is no third, orphaned island anywhere in the mesh** — if
  15 timeline entries had left any stray geometry (a disconnected fragment, a leftover face, a
  degenerate sliver), it would show up as a 3rd (or more) component in this same split, since
  orphaned geometry from a deleted feature chain has no reason to share edges with either the
  main outer shell or the sealed void. It doesn't. 2 components, fully and exactly explained by
  R63, no unexplained remainder.
- `step/urn-lid.step`: **13 `ADVANCED_FACE` entities total — 6 planes, 3 cylinders, 1 sphere, 3
  toruses** (counted directly via text search on the entity keywords, not summarized from a
  report). 6+3+1+3 = 13, exactly matching the claimed face inventory and the `ADVANCED_FACE` count
  with nothing left over and nothing missing. A leftover handle/plinth fragment (which would need
  its own loop-shaped geometry — at minimum an additional torus or a pair of cylinders for a bail
  shape) is not present in this inventory.
- Old handle bounding region (per every prior revision: roughly `y=−4` to `+4mm`, above the old
  dome apex) checked directly on the current mesh: fully solid/absent-of-void at every sampled
  height in that region above the plateau — no residual bail, no residual plinth boss, no
  residual mounting nub.

**Verdict: handle removal is clean. No orphaned geometry, confirmed by an independent face-count
reconciliation (13=13) and a component-count reconciliation (2=2, fully explained), not just a
visual "looks fine" pass.**

## R65. Dome apex plateau math — this is a **real finding, not a confirmation**. The Coder's framing ("not simultaneously achievable on a spherical cap") is factually incorrect; a spherical cap *could* have hit both the ~22mm plateau and the ~29mm height targets, with only a 0.44% change in sphere radius.

This was flagged as needing a genuine independent check, not a rubber stamp, so the actual sphere
and torus parameters were pulled directly from the STEP file (not re-derived from the spec's own
worked hand-calc, to avoid just checking the Coder's arithmetic against itself):

**Confirmed via STEP (`SPHERICAL_SURFACE` #16 + its `AXIS2_PLACEMENT_3D` #183 → `CARTESIAN_POINT`
#278):**
- Sphere radius: **R = 41.6666666666667mm** — this is *exactly* the value the spec's own §5.1.4
  hand-calc computes from `R=(a²+h²)/(2h)` with **a=40mm, h=30mm** — i.e., **the base-radius/
  full-point-apex-height pair from *before* the flattening request**, not a value freshly
  re-derived for the new (base, height-to-plateau, plateau-radius) three-way target.
- Sphere center: global Z = 8.33333mm. This places the sphere's natural `r=40mm` circle at global
  Z=20.0mm exactly (independently solved: `sqrt(R²−40²)=11.667`, `8.333+11.667=20.0`) — which
  lines up with the brim-top boundary (10mm plug + 10mm brim = Z=20), confirming the sphere really
  is anchored to an 80mm base at the intended location. The sphere's own un-flattened apex
  (r=0) would land at global Z = 8.333+41.667 = **50.0mm**, one full mm above the actual built
  49.0mm top — consistent with "~1mm lost to blending," as claimed.
- **At global Z=49 (the actual built height, i.e. 29mm above the Z=20 base), this sphere's own
  raw, unblended radius is 9.074mm** (computed directly: `sqrt(41.6667² − (49−8.3333)²)`) — **not**
  11mm. The as-built, blended plateau (8.8506mm radius, confirmed independently via mesh vertices
  at Z=49 *and* via `TOROIDAL_SURFACE` #17's major radius, 8.85061203mm — two independent methods,
  agreeing to 6 significant figures) is slightly smaller than even that raw 9.074mm figure, which
  is exactly what a tangent-matched blend should do (a smooth fillet transitioning into a flat cap
  always lands at a marginally smaller/lower point than the raw curve-plane intersection, since the
  blend itself consumes a bit more of the curve to go tangent). **This part of the Coder's math is
  internally consistent and correctly executed** — 17.70mm genuinely is the correct consequence of
  combining *this specific* sphere with a full 29mm height target.

**But that's a narrower and different claim than "not simultaneously achievable on a spherical
cap," and the difference matters.** Solving the actual geometry problem properly — three targets
(base radius a=40mm, height-to-plateau h=29mm, plateau radius r_p=11mm/22mm diameter), one free
parameter (sphere radius R, since a cap's height, base, and plateau radius over-determine R once
all three are specified) — gives a closed-form, exact answer:

```
z_c = (r_p² + h² − a²) / (2h) = (121 + 841 − 1600) / 58 = −638/58 = −11.0mm  (sphere center,
                                                                               relative to base)
R² = a² + z_c² = 1600 + 121 = 1721  →  R = 41.4849mm

Verification: at h=29 (relative to base), radius = sqrt(R² − (h−z_c)²) = sqrt(1721 − 40²)
            = sqrt(1721 − 1600) = sqrt(121) = 11.0mm  ✓ exact
Verification: at base (h=0), radius = sqrt(1721 − 121) = sqrt(1600) = 40.0mm  ✓ exact
```

**A sphere of radius 41.4849mm — just 0.1818mm (0.44%) smaller than the 41.6667mm sphere actually
used — hits *both* the 80mm base OD, the ~29mm height, and the ~22mm (r=11mm) plateau diameter
simultaneously, exactly, with no blending shortfall to account for.** No non-spherical geometry is
needed; the claim that these two targets are "not simultaneously achievable on one spherical cap"
is incorrect as a general statement about the geometry. What's actually true is narrower: **they
are not simultaneously achievable while also re-using the exact sphere radius left over from the
pre-flattening (30mm point-apex) dome design.** That's a legitimate reason to have kept 41.667mm
(preserving already-verified, previously-shipped dome curvature rather than re-deriving and
re-verifying a new one) — but it's a *choice*, not a mathematical wall, and the spec/parameters
documentation should say so rather than presenting the 17.70mm outcome as unavoidable.

**Why this matters enough to flag rather than let it pass as "close enough":** the gap between the
built 17.70mm and the originally-intended ~22mm plateau is not small (−20% on a visually-checked
proportion — the ~22mm figure was itself sized against a concept-comparison reference image,
`v7-dome-apex-flattened.png`, specifically so the flat spot would "read as roughly a quarter of the
dome's base width"). At 17.70mm the plateau reads as ~22% of the 80mm dome base instead of the
intended ~27% — a real, visible proportion shift versus the approved reference image, and one that
turns out to have been avoidable with a trivial (<0.2mm) radius change, not a hard trade-off forced
by the height requirement. **This should route back to whoever owns the dome-apex sizing decision
(Planner/Concept fidelity), not be silently absorbed as "the geometry made me do it,"** since the
actual constraint was a choice to preserve existing curvature, not a mathematical impossibility.
This does **not** block printing — the built geometry is valid, smooth, and self-supporting either
way (confirmed in R66 below) — but the documentation's causal claim is wrong and should be
corrected, and the Planner/requester should get an actual choice between "keep 41.667mm sphere,
accept 17.70mm plateau" and "use 41.485mm sphere, get the originally-intended ~22mm plateau,
with a fresh (cheap) re-verification of the dome curve" rather than being told only one was ever
possible.

## R66. Dome/brim/plug surface quality — self-supporting sweep and crease detection, PASS

- **Radius-monotonicity sweep, Z=10mm (top of plug) to Z=49mm (plateau top), 390 points at
  0.1mm resolution:** **zero locally-increasing-radius steps.** Confirms the entire brim+dome
  envelope is in the "shrinking cone" self-supporting class this project relies on throughout —
  independently reproduces the Coder's claimed 200-point sweep at nearly double the sampling
  density, same result (zero violations).
- **Plug OD, Z=0–10mm:** constant 39.750mm at every sampled height — genuinely zero overhang, not
  just "low overhang."
- **Crease/kink detection (`face_adjacency_angles`, all faces above Z=15mm, i.e. brim-top and
  dome):** **maximum adjacent-facet angle = 12.64°**, at Z≈21.1mm (the brim-to-dome fillet region,
  where curvature is locally tightest) — well below the 20–30°+ range that would indicate a
  genuine sharp corner rather than ordinary mesh tessellation of a continuously curved surface.
  **No sharp kink anywhere in the dome, the brim-to-dome transition, or the dome-to-plateau
  transition.** This independently confirms the "genuine tangent fillet, not a faceted corner"
  claim for both blends (brim-to-dome and dome-to-plateau), via a method (facet-normal angle
  analysis) that doesn't depend on trusting the Coder's own sweep script.

## R67. A real documentation-vs-as-built discrepancy found, low severity — the "10mm flat brim ring" does not exist as a literal flat surface in the built part

Spec §5.1.3 derives the 80mm dome base OD and corroborates it with "flat brim ring width: 50mm
(brim r) − 40mm (dome-base r) = 10mm per side — a clearly visible, proportionate flat rim" and
compares this explicitly to the collar's own 10mm wall band. **Checked directly against the actual
geometry, not assumed from the spec's narrative:**

- Fine-resolution radius sweep (Z=9.5 to Z=22, 0.25mm steps) shows the brim's vertical wall
  holding a genuinely constant 49.85mm radius only from **Z=10 to Z=17** (7mm), after which the
  radius **continuously decreases** from 49.85mm down through the dome's sphere, with **no
  intervening flat/constant-radius plateau** at any height in between.
- STEP-level confirmation: two additional fillet `TOROIDAL_SURFACE`s exist in this exact region —
  #19 (major r=46.85mm, minor r=3mm, centered Z=17) and #18 (major r=41.4729mm, minor r=2mm,
  centered Z=22) — a **compound two-stage fillet** blending the vertical brim wall directly into
  the dome sphere, with no flat annular face modeled between them.
- **This means the "10mm flat ring, matching the collar's own wall band" corroborating check in
  the spec describes a design intent that was not literally built** — the actual transition is a
  smooth continuous curve, not a flat shelf. **This is not a print-quality problem** (a filleted
  transition is if anything *better* for print quality and edge durability than a flat shelf with
  two sharp corners would have been, and R66 confirms it's smooth and self-supporting) — but it is
  a real gap between what the spec's corroborating math describes and what got built, and the
  "visually echoes the collar's 10mm band" reasoning in §5.1.3 doesn't actually hold for the
  as-built part the way the spec claims. **Low severity, documentation-accuracy issue, not a
  functional or print-quality defect** — flagged so it doesn't get cited later as a verified visual
  proportion when it isn't literally present.

## R68. Lid is a solid mass (aside from the plug's hollow), confirmed — not a defect, but worth naming for print-time/material-estimate accuracy

`3mf/urn-lid.3mf`'s mesh object is itself named **`urn-lid-solid`** in the file, and direct
cross-sectioning at multiple dome/brim heights (Z=15, 25, 35, 40, 45) finds **only one boundary
circle at every height** (not two, the way the plug's hollow section reads) — confirming the
brim+dome is genuinely solid, not a thin shell over an internal cavity, throughout its extent
outside the plug. A rough analytic sanity check (solid disc + spherical-cap volume formulas)
lands within ~1.6% of the measured total, consistent with this being intentional, not a modeling
error. **This is consistent with every prior revision of this lid (v1–v6 also read as solid by
the same cross-section test on the archived file) and is not new to v7** — noted here because it
has a real, if minor, downstream consequence: **the reported "material volume" (192.5 cm³) and
any $-cost/weight figures derived from it represent a 100%-dense CAD volume, not what a typical
FDM slicer will actually deposit at the spec's own recommended 15–20% infill setting (§11).** The
*actual* printed mass/cost will likely be meaningfully lower than the documented figures suggest
(a safe direction to be wrong in) — worth a one-line clarification in `parameters.md` so a future
reader doesn't take the material-volume figures as printed-mass estimates.

## R69. Fit/clearance re-verification against the actual (untouched) body file — PASS, not assumed from "body unaffected"

Per the instruction to check fit against real mating hardware/geometry, not just the part it's
visibly touching: re-measured the body's internal bore directly on `stl/urn-body.stl` (not
re-used from a prior pass's numbers), since the plug/bore fit is the one place this lid revision's
correctness depends on a body dimension.

- Body bore radius at Z=138.5, 140, 143.5, 145, 148, 150, 153.0, 153.4mm: **39.96–40.00mm at every
  sampled height** (mesh-tessellation noise only, true value 40.000mm) — confirms the 80mm ID bore
  is genuinely constant through the full engagement zone, still true after the lid-only v7 changes
  (as expected, since the body file's timestamp — Aug 31 — confirms it was not touched this round).
- Plug tip (lid Z=0, i.e. body Z=153.5−10=143.5mm once seated): bore radius at that exact body
  height measured at 39.963mm (≈40mm) — **taper has not yet begun**, confirming the claimed 5.0mm
  collision margin above P3 (body Z=138.5mm, where the bore starts narrowing) independently, using
  two freshly-measured real numbers, not nominal arithmetic.
- Diametral clearance, recomputed from these two independently-remeasured real parts: 80.000 −
  79.500 = **0.500mm exactly** — matches nominal, no unauthorized oversize/undersize compensation
  baked in on either side.
- **Body's own overall dimensions unaffected by v7**, re-confirmed directly (not just by
  timestamp): height 153.500mm, belly OD 153.89–153.91mm — both match the documented v5 figures.
  `neck-fit-test.stl` also re-measured: 143.97×143.98×35mm, matches its documented v5 figures
  exactly. Neither file shows any sign of accidental modification during this lid-focused round.

## R70. Structural/usability tests, per the standard test suite

1. **Drop test (accidental knock).** The plug wall (4.0mm, PETG) and the brim (10.0mm, PETG,
   thicker than the pre-v7 5mm) are both well clear of the 0.8mm print-floor and are on the
   tougher of the project's two materials (PETG, not PLA) — no thin-wall cracking concern at
   either. **The one drop-risk consideration that changed this round is not structural but
   behavioral: with the handle gone, there is no dedicated grip feature, and a smooth domed
   lid gripped by hand (rather than a purpose-built handle loop) is more likely to be dropped in
   the first place** — especially relevant for a lid that may be handled with less-than-ideal grip
   (e.g. slightly damp/gloved hands during a somber, emotionally distracting task). This is a
   real, if modest, *likelihood-of-drop* consideration distinct from *survives-a-drop* — the lid
   itself (solid PETG dome/brim, no thin unsupported features outside the sealed internal bridge)
   should survive an ordinary drop onto a hard floor without cracking, but the odds of a drop
   happening at all plausibly go up without a handle. Not a blocker (this was an explicit,
   confirmed user override of the concept's own "hard constraint" framing, not something this
   Tester pass can re-litigate), but worth naming as a real usability trade-off for the Reviewer's
   business-fit judgment, not just a structural non-issue.
2. **Load test.** No dedicated load-bearing lift feature exists any more (§11 of the spec makes
   this explicit) — the lid only ever carries its own weight when lifted by hand, and the body
   only carries the modest static weight of a bagged-remains payload resting on its 5mm floor.
   Neither load case is close to a real structural concern at these wall thicknesses/materials.
   No load-bearing failure mode identified.
3. **Fit test.** See R69 above — plug/bore clearance (0.500mm), collision margin (5.0mm), and
   brim/collar flush-fit (99.700mm lid brim vs. 100.000mm body collar, a deliberate 0.3mm
   negative allowance reasoned from this project's own documented "external features print
   oversized" tendency) all independently re-confirmed. **The brim/collar edge has zero
   print-tolerance margin by design (spec's own named risk, §5.1.1/§10 edge case 4)** — this is a
   disclosed, reasoned, cosmetic-only risk (a slightly proud or slightly recessed edge, not a
   functional fit failure) and doesn't change this test's pass status, but is restated here since
   it's exactly the kind of "fits the collar's OD but check the rest of the mating condition"
   class of check this role is asked to prioritize. No hardware component (magnets, fasteners)
   exists anywhere in this design any more, so there's no secondary "clears its own mounting
   hardware" check applicable here — the plug/bore pair *is* the only mating interface.
4. **Use-case-specific: internal bridge / trapped-support risk.** Unchanged from v6, re-confirmed
   still applies identically post-capping (per spec's own §5.2.2 analysis, and independently
   re-verified in R61 above that the void's floor is now solid, not open, at Z=4mm) — same
   71.5mm-diameter enclosed-bridge risk, same "confirm supports are set to build-plate-only before
   slicing" recommendation as RE-TEST PASS 8 already established. No new use-case risk introduced
   by the capping itself, consistent with the spec's own "does not eliminate, does not worsen"
   framing (§5.2.2), independently confirmed rather than taken on faith.

## R71. Material check

**Lid: PETG, unchanged this round, still the right call.** The plug wall (4mm) and brim (10mm,
thickened this round) are the two features most exposed to mechanical stress (friction-fit
insertion/removal cycles on the plug; repeated hand-gripping on the brim edge now that it's the
*only* grip surface, per R70.1) — PETG's higher impact toughness versus PLA is the correct
material choice for both, and nothing about v7's changes weakens that reasoning. **No material
change is recommended.** The one thing worth flagging plainly: **if anyone ever reverts this lid
to PLA for cost or finish-matching reasons (§8 notes PETG's glossier finish as a named
mismatch risk against the PLA body), the plug and the now-sole-grip brim edge should be treated as
the two features that would most need re-assessment — PLA's brittleness under a snap/impact load
is a real risk specifically at a thin friction-fit wall like this plug, not a generic caution.**
Body material (PLA) is unaffected by and unrelated to this round's changes; no new body-side
material concern.

## Overall assessment of this pass

**14 checks run (R61–R71 plus the carried-forward blocking-check restatement), covering every
headline number in the v7 revision.** Every dimensional and volumetric claim checked out exactly
or within expected tessellation tolerance. The two things flagged as needing real scrutiny by name
— the 2-components signature and the dome plateau/height math — got that scrutiny:

- **2 components: confirmed correct, three independent ways (R63).** Not a defect. Safe to carry
  forward without further concern.
- **Dome plateau math: a real, quantified error in the *reasoning*, not in the *geometry*
  (R65).** The built part is valid and self-supporting either way, but the spec's claim that
  22mm/29mm were mutually unachievable on a spherical cap is wrong — a 0.44%-smaller sphere would
  have hit both. This should go back to whoever owns the apex-sizing call, framed as a choice
  (keep current geometry vs. cheaply re-derive for the originally-intended proportion), not
  absorbed silently.
- **One new documentation-accuracy gap found and not previously flagged: the "10mm flat brim
  ring" doesn't exist as a literal flat surface in the built part (R67).** Cosmetic/documentation
  only, no print-quality consequence.
- **Handle removal: clean, independently confirmed via face-inventory and component-count
  reconciliation (R64).** No orphaned geometry.

**Recommendation: ready for the Reviewer, with two items carried forward explicitly rather than
silently cleared** — (1) the dome plateau/height math correction (R65) should be seen and decided
on by whoever owns dome-apex sizing, not just noted in a test log, and (2) the pre-existing,
still-open neck-opening-vs-real-bag `ESTIMATED` risk (§0 above) remains exactly as open as it was
before this round and should not be treated as addressed just because this round shipped
successfully. Neither of these blocks this specific lid revision's own internal correctness, which
is otherwise solid.


---
---

# RE-TEST PASS 10 — scoped re-check: dome sphere radius corrected (17.70mm → 21.73mm plateau)

Scoped follow-up, not a full re-run — re-checks only the dome-apex geometry and the invariants
that a sphere-radius change could plausibly disturb (manifold/void signature, overall heights,
volume), per the request. Files re-exported (confirmed by timestamp: 2026-09-02 17:32, all three
of `step/urn-lid.step`, `3mf/urn-lid.3mf`, `stl/urn-lid.stl`).

## R72. Sphere radius fix — confirmed exactly, using the same STEP-level method as R65

`SPHERICAL_SURFACE` #16 now reads **R = 41.4849370253831mm** — this is the exact value
independently derived in R65 last pass (`R=41.4849mm`, solved from the 3-target system: 80mm
base, 29mm height, 22mm/r=11mm plateau). The Coder used the exact figure this Tester calculated,
not an approximation of it.

Sphere center (via `AXIS2_PLACEMENT_3D` #183 → `CARTESIAN_POINT` #278): global **Z=9.0mm** (moved
from 8.333mm last round). Re-deriving from this: base radius at global Z=20 (unchanged brim-top
boundary) = `sqrt(41.4849370254² − (20−9)²) = sqrt(1721.000 − 121) = sqrt(1600) = 40.000mm`
**exact** — dome base OD is still exactly 80mm, confirmed independently, not just carried over
from the claim (claim #3, PASS).

**Raw (unblended) sphere radius at Z=49 (the target plateau height):**
`sqrt(41.4849370254² − (49−9)²) = sqrt(1721.000 − 1600) = sqrt(121) = 11.000mm exact.` This
confirms the corrected sphere genuinely passes through r=11.0mm at exactly z=49 — i.e., the
sphere itself hits the *original* ~22mm-diameter target precisely, with no compromise needed at
the raw-curve level. Any shortfall from 22mm in the final built part is therefore attributable
entirely to the blend/fillet, not to the sphere being wrong — consistent with the Coder's
disclosed reasoning.

## R73. Plateau diameter — PASS, confirmed two independent ways, matches claim exactly

- **Mesh vertices at Z=49.0 (48 verts, single flat cap):** radius = 10.864167mm at every vertex
  (range 10.8641668–10.8641675mm, i.e. agreement to 6 significant figures) → **diameter =
  21.7283mm.**
- **STEP `TOROIDAL_SURFACE` #17** (the dome-to-plateau fillet): major radius =
  **10.8641670619166mm**, minor radius = **0.999999999999845mm** (a 1mm fillet, down from the
  prior round's 2mm — matches the Coder's disclosed "smaller fillet radius" choice). Major radius
  × 2 = 21.7283mm, bit-identical to the mesh measurement.
- **Both methods agree to 6+ significant figures with the claimed 21.7283mm.** PASS, exact.

**Sanity-check on the tradeoff, not just the number:** the raw sphere hits r=11.0mm exactly at
z=49 (R72 above); the built, blended result is 10.864mm — the 1mm-fillet blend "eats" 0.136mm of
radius to achieve tangency. This is a small, plausible blend consumption (smaller than the
prior round's ~0.22mm consumption from a 2mm fillet against a less-well-aligned raw intersection),
consistent with genuinely improving the geometry rather than just re-arranging the same problem.

## R74. Tangency at the dome-to-plateau blend — independently verified genuine, not just claimed

- **Radius-monotonicity sweep, Z=10–49mm, 390 points at 0.1mm resolution: zero
  locally-increasing-radius steps** — reproduces the Coder's 200-point sweep claim at higher
  density, same result.
- **Facet-crease detection** (`face_adjacency_angles`, all faces Z>15mm): **max angle = 12.72°**,
  located at Z≈21.1mm — the brim-to-dome fillet region, unrelated to and unaffected by this
  round's change, and statistically identical to last round's 12.64° at the same location (normal
  mesh-tessellation faceting on a region of high curvature, not a real crease). **No new crease
  appears anywhere near the dome-to-plateau blend (Z≈47–49mm) or anywhere else** — if the 1mm
  fillet had failed to achieve genuine tangency (e.g. a naive intersection with no blend, or a
  fillet radius too small to smooth the actual slope mismatch), this would show up as a sharp,
  isolated spike in this same sweep, and it doesn't.
- **Geometric cross-check specific to tangency, not just "no visible kink":** the torus's top
  point (directly above its Z=48 center circle, at Z=48+1=49) sits exactly at the measured
  plateau height and radius — this is the flat-plane side of the tangency, and it's automatic by
  construction (a torus's topmost point always has a horizontal tangent plane, matching a flat
  cap with zero slope-mismatch by definition). Combined with the monotonic-radius and low-crease-
  angle findings above (which specifically check the *sphere* side of the blend, where a slope
  mismatch would actually be capable of showing up), **this is a genuine tangent blend on both
  ends, independently confirmed, not just claimed.**

## R75. Everything else the radius change could have disturbed — confirmed undisturbed

| Item | Claimed | Measured | Method | Verdict |
|---|---|---|---|---|
| Dome height (base to plateau) | 29.000mm (unchanged) | 29.000mm (Z=20 to Z=49) | bounds + base Z | PASS, exact |
| Dome base OD | 80mm (unchanged) | 80.000mm exact (R72) | STEP sphere+placement math | PASS, exact |
| Total lid height (seating to plateau) | 39.000mm (unchanged) | 39.000mm | bounds | PASS, exact |
| Total bbox height | 49.000mm (unchanged) | 49.000mm | `mesh.bounds` | PASS, exact |
| Manifold/void signature | Undisturbed, same 2-component/`BREP_WITH_VOIDS` signature | Confirmed: `is_watertight=True`, 2 components (outer +218.11 cm³, void −24.07 cm³ — **numerically identical to last round's void figure**, as expected since the plug wasn't touched), `BREP_WITH_VOIDS(`=1, `ADVANCED_FACE(`=13 (6 planes+3 cyl+1 sphere+3 tori, same inventory as before) | mesh split + STEP entity count | PASS, exact — the plug/void geometry is confirmed byte-for-byte-equivalent in volume, not just "should be unaffected" |
| Material volume | 194.2929 cm³ | 194.041 cm³ (STL) / 194.038 cm³ (3MF) | `trimesh.volume` | PASS within 0.13% (same systematic mesh-vs-analytic gap as last round, same direction, consistent ratio — 1.0013× both times) |
| Volume delta vs. prior round | +0.92% | +0.915% (194.041 vs 192.284, both mesh-measured, same method both times) | same-method comparison | PASS, matches essentially exactly |

**No other lid feature was touched by this change** — plug (OD/ID/wall/depth/solid-tip-cap),
brim (OD/thickness), and the brim-to-dome fillet (torus #19, major=46.85mm/minor=3mm — unchanged
digit-for-digit from last round) all re-confirmed identical. This was a genuinely scoped,
single-parameter fix (one sphere radius + one fillet radius), not a broader rebuild in disguise —
confirmed by everything *outside* the dome apex being bit-identical to RE-TEST PASS 9's numbers.

## Independent verdict on the 21.73mm-vs-22mm tradeoff: the right call, and it costs less than it looks like it does

Asked to give a real read, not just pass/fail: **tangency was correctly prioritized over hitting
an exact 22.00mm, and the two are not actually in as much tension as the framing might suggest.**

- The spec's own language around the 22mm figure was never a tight tolerance — §5.1.4 calls it
  **"an aesthetic judgment call... roughly a quarter of the dome's base width"** and tags it
  `ESTIMATED`. There was never a stated precision requirement (e.g. "22.00mm ±0.1mm") to weigh
  against tangency.
- The spec's tangency requirement, by contrast, **is** explicit and reasoned from real
  print-quality consequences: §5.1.4 names the alternative outcome plainly — *"a visible ~15° kink
  where the curve meets a flat plateau"* — and this project has a documented history (§13 v2) of
  treating exactly this class of faceted/kinked transition as a real defect worth a full rebuild
  to fix, not a cosmetic nitpick. Reintroducing a ~15° kink to hit an exact but always-approximate
  aesthetic number would have been a worse trade than the one actually made.
- **The proportion the 22mm figure was actually standing in for is preserved almost exactly:**
  22mm ÷ 80mm base = 27.5% ("roughly a quarter"); the built 21.73mm ÷ 80mm = **27.16%** — a
  0.34-percentage-point difference, not visually distinguishable from the reference image the
  22mm figure was itself eyeballed against. **This isn't "a compromise that got most of the way
  there" — it's a resolution that hits the actual design intent (the proportion) while correctly
  treating the specific decimal (22.00mm) as the softer, less load-bearing of the two numbers.**

**Verdict: yes, this is the right call, for a stronger reason than "tangency matters more than
aesthetics in general" — in this specific case, satisfying tangency barely cost anything against
the actual (proportional) design intent, while failing tangency would have reintroduced a
previously-identified, print-quality-relevant defect class. This is a clean resolution, not a
lesser compromise.**

## Is this ready for the Reviewer?

**Yes.** All 7 requested re-verification items pass exactly or within the same expected
mesh-tessellation tolerance seen throughout this project. The dome-apex fix is correctly scoped
(only the sphere radius and one fillet radius changed; everything else confirmed bit-identical),
genuinely resolves the R65 finding from the prior pass (the causal claim in the spec can now be
corrected to reflect that the retained-sphere choice, not a mathematical wall, was what produced
17.70mm — and the corrected sphere shows this directly), and the tangency claim is independently
verified true, not just asserted. **No open items remain from this specific dome-apex issue.**
The two items already carried forward from RE-TEST PASS 9 remain exactly as before and are
restated once more so they don't quietly drop out of the handoff: (1) the "10mm flat brim ring"
documentation-vs-as-built gap (R67, cosmetic/documentation only, unaffected by this fix) and (2)
the pre-existing, still-open neck-opening-vs-real-remains-bag `ESTIMATED` risk (§4.4), which this
lid-only fix does not and cannot touch.

---
---

# RE-TEST PASS 11 — v8 body revision (rounder "thrown-ceramic" profile, reshaped below P3) — cold-start independent verification

Method note: this pass started cold (no memory of the build session) and verified strictly from
the exported deliverable files — `step/urn-body.step` (raw STEP entity parsing, no CAD kernel),
`3mf/urn-body.3mf` (zip/XML parsing + `trimesh` mesh load), and `stl/urn-body.stl` (`trimesh`,
dense cross-sectional profiling at 0.02-0.1mm resolution, nearest-point wall-thickness search via
`scipy.spatial.cKDTree`, facet-adjacency-angle crease detection) — diffed against the archived
pre-v8 baseline at `archive/pre-v8-rounder-body/{step,3mf,stl}/urn-body.step` using the identical
methods on both, not the Coders report. Per the task framing, three build decisions are treated as
pre-accepted and are not re-litigated as defects below: the belly keeping its v7 hand-sculpted
shape (not rebuilt as a broad-swell Bezier), the shoulder witness landing at internal r 47.0mm
(not the specs originally-written 45.0mm), and the foot fillets being tangent to v7s real
gently-flaring foot wall (not an idealized vertical wall). All are independently confirmed present
and correctly built below — the point of re-checking them was to verify the accepted decision was
actually what got built, not to second-guess the decision itself.

## R76. Single valid manifold solid — confirmed across STEP, 3MF, and STL, with one honest gap disclosed

- STL: watertight, winding-consistent, Euler number = 2, 0 edges with an incident-face count
  other than 2 (checked directly, not inferred) — 146,894 triangles, 73,449 vertices, single
  connected component (trimesh.split returns exactly 1 body).
- 3MF: independently loaded and re-checked with the same method (not assumed to inherit the STL
  result) — a different tessellation (44,022 triangles, a coarser re-mesh than the STLs), also
  watertight, Euler = 2, 0 non-2-count edges, 1 connected component. The fact that a completely
  independent retesselation of the same B-rep passes the identical checks is stronger evidence of a
  genuinely valid solid than checking one format alone.
- STEP: raw entity parsing (not a CAD-kernel read) finds exactly 1 CLOSED_SHELL and
  exactly 1 MANIFOLD_SOLID_BREP — both singular, as required for one valid solid. 10
  ADVANCED_FACE entities — matches the Coders reported face count exactly. Composed of 3
  B_SPLINE_SURFACE (compound B_SPLINE_SURFACE_WITH_KNOTS/RATIONAL_B_SPLINE_SURFACE entities,
  down from 5 in pre-v8), 2 CYLINDRICAL_SURFACE, 2 new TOROIDAL_SURFACE (0 in pre-v8 — see
  R81), and 3 PLANE — 3+2+2+3 = 10, reconciles exactly.
- Honest gap: the Coders reported "12 edges" could not be independently reproduced by text
  parsing alone. Raw EDGE_CURVE entity count is 20 (up from pre-v8s 18); resolving each to its
  two VERTEX_POINT 3D coordinates and de-duplicating by coordinate pair gives 16 distinct
  vertex-pairs — same count (16) in both v8 and pre-v8, so at least self-consistent, but not the
  Coders "12." B-rep topological edge/vertex/face (V-E+F=2) accounting depends on kernel-internal
  loop/seam conventions that arent reliably recoverable from flat STEP text without a real CAD
  kernel — flagged honestly rather than forcing a match. This does not weaken the manifold
  finding: the mesh-level Euler=2 / watertight / 0-non-manifold-edge checks above are the
  authoritative, directly-checkable proof of a valid printable solid in both exported mesh formats,
  and the STEP-level shell/solid/face counts that are independently reproducible all match.

Result: PASS on the decisive checks (watertight, manifold, single solid, single shell, correct
face count, matching across all three formats); one sub-item (raw STEP edge count) noted as not
independently reproducible rather than silently assumed correct.

## R77. Cavity volume — independently measured, matches the Coders figure closely, with a real (non-blocking) surprise in the "why"

Measured via solid-of-revolution integration: dense radial cross-sections of the inner-wall
boundary from floor-top to rim (trimesh.section_multiplane at 0.1mm steps, ~1,530 planes),
pi*r_inner(z)^2 integrated by the trapezoidal rule. Run twice with slightly different
endpoint-interpolation handling as a self-consistency check:

- v8 measured cavity: 1569.82 cm3 and 1570.19 cm3 (two independent integration runs, 0.02%
  apart) — essentially exact agreement with the Coders reported 1570.3 cm3 (within 0.03-0.05%).
- -0.55% to -0.58% vs. the ~1579 cm3 binding target (confirmed from specs.md section 4.1 as the
  current authoritative target, not the historical 1474.8/1477.8 cm3 figures) — comfortably inside
  the +/-5% band (~1500-1658 cm3), ~70 cm3 above the floor and ~88 cm3 below the ceiling.
- Cross-validation of method: the identical method applied to the archived pre-v8 (v7) body
  returns 1579.10 cm3 and 1579.85 cm3 — matching the long-established, many-times-independently-
  verified ~1579 cm3 v7 figure almost exactly. Since my method reproduces a number this project
  has confirmed at least four separate times before, I trust it applied to v8.

Result: PASS, independently confirmed, inside the pre-authorized band.

A real, non-blocking surprise worth documenting, not just passing over: the specs own
delta-from-baseline hand-calc (section 4.2.3) predicted the v8 reshape would add ~27.8 cm3
(P1->P3 chord-sum delta) for a total estimate of ~1608 cm3. The actual built cavity instead
decreased slightly from the v7 baseline (1579->1570, delta ~-9 cm3) — a ~37 cm3 gap from the
hand-calcs predicted direction, though still safely inside the band either way. Root-caused by
directly diffing the v8 vs. pre-v8 internal-radius profile (see R83s table): the new, longer
belly tangent-handles that create the "broad swell" (move 1) pull the curve inward through the
mid-flank (z~80-108mm) by as much as 4.2mm at z~100mm relative to v7s equivalent curve — this
is a larger narrowing than the +/-1-2 cm3 "upper flank" correction term the specs own fairing
estimate anticipated. This more than offsets the volume gained at the shoulder witness itself
(+4.58mm external radius at Z=112.5) and the shoulder-to-P3 segment. This is exactly the kind of
gap the specs own section 4.2.3 explicitly flagged as expected and pre-authorized ("Hand-calc -> CAD
confidence is lower for Large than for Small/Medium... the real CAD cavity could still land
somewhat off ~1608 cm3; the flag-back triggers above cover both directions") — no flag-back is
triggered because 1570 cm3 is well inside the band, but the reason the hand-calc missed by this
much is a real, verifiable geometric effect (the frustum/chord method structurally cannot see a
curve dipping inward between its sampled endpoints), not a measurement inconsistency, and is worth
recording for whoever tunes this profile next.

## R78. Belly max OD — PASS, single point, zero overshoot, confirmed in both mesh formats

Dense radial scan (0.1-0.2mm steps) of the full outer profile, in both deliverable mesh formats:

- STL: peak outer radius 76.9657mm (OD 153.9314mm) at z~68.8-69.25mm. Zero samples anywhere
  in the full 0-153.5mm height range exceed 76.966mm; zero exceed 77.066mm (target+0.1mm).
- 3MF: peak outer radius 76.9660mm (OD 153.9319mm) at z~68.78mm — matches the STL to
  0.0003mm.
- Broad swell, not a sharp point: radius stays within 0.05mm of the peak across z~66.2-71.2mm
  (53 samples) and within 0.10mm across z~65.1-72.1mm — a genuine broad swell, consistent with the
  specs move-1 intent (lengthened tangent handles), not a plateau (v7s shape) and not a cusp.
- Cross-checked against the archived pre-v8 body: peak radius 76.9651-76.9657mm at z~69.09-69.12mm
  — confirms the belly apex radius and absolute height are unchanged, exactly as the spec
  requires ("position and radius unchanged").

Result: PASS. 153.9mm OD +/-0.1mm target met almost exactly (153.93 vs. 153.9), single
maximum-radius point, no overshoot above or below the belly, matches the pre-accepted "belly keeps
its v7 shape" framing (radius/height untouched; only the apex curvature was faired into a swell).

## R79. Overall height, base plane, and XY centering — PASS, exact

- Overall height: STL and 3MF bounds both run Z = [~0, 153.5]mm exactly (STL min Z =
  2.2e-15, i.e. exact 0 to floating-point precision).
- Base face at Z=0: confirmed — the entire bottom-cap vertex ring sits at Z=0 in both formats.
- Centered X/Y: mesh centroid at (-0.0004, -0.0009) — within normal mesh-tessellation noise of
  the origin. Bounds are symmetric to within ~0.01mm (X: [-76.696, 76.965]; Y: [-76.956, 76.960]).

Result: PASS, all three sub-items exact or effectively exact.

## R80. Base OD "98mm at the top of the foot-fillet arc" — a precision/documentation note, not a defect (consistent with the pre-accepted foot-fillet decision)

specs.md section 4.2.3 states the base OD "stays 98mm, now first reached at the top of the fillet arc
(Z_ext ~7mm)" — this describes what would happen if the fillet were tangent to an idealized
vertical r=49mm wall. Per the tasks pre-accepted framing, the fillet is actually tangent to
v7s real, continuously-flaring foot wall instead. Measuring the real profile directly: the
outer radius crosses r=49.0mm (98mm OD) momentarily at approximately z~2.7-2.8mm (between the
z=2.5 sample at 48.97mm and the z=3.0 sample at 49.36mm), then keeps flaring outward continuously
all the way to the belly — there is no sustained constant-98mm-OD section at all, at z~7mm or
anywhere else.

This is not a new defect introduced by v8 — the archived pre-v8 (v7) body shows the identical
character: its own outer radius is already 49.005mm at z=0.02mm and climbs continuously to
50.39mm by z=5mm, with no flat vertical section either. The "idealized vertical wall" the specs
98mm/Z~7mm language assumes never existed even in v7. Recommend specs.md/parameters.md note
this precisely (crossing height ~2.7mm, no sustained plateau) rather than carry forward the
Z~7mm figure as if it were confirmed on the real geometry — a documentation-accuracy item, not a
geometry defect, and not blocking.

True flat bottom contact-disc OD, measured two independent ways in exact agreement:
- STL: all 127 bottom-cap (Z=0) vertices sit at exactly r=43.6297mm (zero variance).
- STEP: the external foot-fillet torus (TOROIDAL_SURFACE #16, R81 below) has major radius
  43.6296748269217mm — matching the mesh figure to 4 decimal places, an exact
  cross-format agreement between the raw B-rep parameter and the independently-tessellated mesh.
- Contact-disc OD = 87.26mm. Contact-OD:height = 87.26/153.5 = 0.568, close to the tasks stated
  "~89mm / 0.58" figure (small, immaterial rounding difference between "~89mm" and the precisely-
  measured 87.26mm — both describe the same real, intentional, disclosed footprint reduction from
  v7s ~98mm contact ring). Confirmed more stable than the specs original 0.55 target, as
  claimed — PASS, not a defect.

## R81. Foot fillets — confirmed as real analytic torus faces, both radii essentially exact, tangent on both sides

Extracted directly from step/urn-body.step (0 TOROIDAL_SURFACE entities exist in the archived
pre-v8 STEP — these are a genuine, verifiable new addition in v8, not merely claimed):

| Fillet | STEP entity | Minor radius (measured) | Nominal | Deviation |
|---|---|---|---|---|
| Internal floor-to-wall | #15 TOROIDAL_SURFACE | 4.99753384748094mm | R5.0 | -2.466 micron |
| External foot | #16 TOROIDAL_SURFACE | 6.99999749183678mm | R7.0 | -2.5 nm |

The internal fillets -2.466-micron deviation matches the Coders own reported 4.99753 figure to 5
decimal places — independently confirmed, and, as the Coder characterized it, immaterial (a
3-point-arc-fit rounding artifact roughly 3 orders of magnitude finer than a print layer).

Tangency, checked directly on the mesh (facet-adjacency-angle scan), not assumed from the STEP
parameters alone:
- Base-plane to external-fillet transition (z~0-0.5mm): max facet angle 6.6deg, mean 2.3deg — consistent
  with ordinary tessellation faceting of a continuously curved region, not a real corner.
- External-fillet to flaring-wall transition (z~6.5-8mm): max 5.2deg, mean 1.6deg.
- Floor-plane to internal-fillet transition (z~4.5-5.5mm): max 7.4deg, mean 2.4deg.

All three are in the same low range as ordinary curved-surface tessellation noise found elsewhere
on this body, and an order of magnitude below the genuine 90deg corner correctly found at the flat
top rim (R76/legitimate design edge) and well below the one real, small, pre-existing discontinuity
found at P3 (R83, ~18.6deg, inherited from v7 unchanged). Result: PASS — both fillets are real,
essentially-exact-radius, tangent torus faces, not polygon approximations or untangent stubs.

## R82. Wall thickness — radial and true-perpendicular, both confirmed matching the Coders figures closely

Radial (same-Z outer-minus-inner) across the reshaped z=10-135mm span: measured 3.94-4.08mm
— matches the Coders reported 3.93-4.08mm range almost exactly (sampled at z=10, 20, 26.5, 30, 40,
50, 60, 69, 80, 90, 95, 100, 107.5, 112.5, 120, 130, 135mm).

True perpendicular (nearest-point) minimum, computed properly rather than approximated: built
the full inner and outer meridian-profile point clouds (from the 0.1mm-resolution cross-section
scan) and ran a scipy.spatial.cKDTree nearest-neighbor search from every outer-profile point to
the inner-profile polyline — this measures the true minimum wall thickness along whatever direction
is actually shortest, not a same-Z radial approximation (which overstates true thickness on a
sloped wall).

- Minimum: 2.7704mm at z=96.52mm (outer r=63.41mm) — matches the Coders reported ~2.78mm @
  z~95 almost exactly, both in magnitude and location.
- This is 3.46x the 0.8mm print-floor (tasks "3.5x" — matches).
- The minimum occurs where the local outer-wall slope is steepest: independently measured
  -46.2deg from vertical at this exact point (via np.gradient on the same profile) — this is
  local steepness within the belly-to-shoulder span, which is a monotonically-shrinking-radius
  region throughout (radius decreases from the belly apex all the way to P3, confirmed by the same
  scan finding zero meaningfully-increasing steps in that span) — the same "shrinking cone,
  self-supporting regardless of local angle" class this project has relied on since its earliest
  passes, so the steep local angle here is a wall-thickness consideration, not an overhang risk.

Result: PASS, both figures independently confirmed and comfortably above the print-minimum.

## R83. P3-and-above byte-identical to v7 — the critical check for lid/plug fit, confirmed by four independent methods

This is the single most consequential check this pass, since the lid, plug, and neck-fit-test
all depend entirely on this region and were not rebuilt (R86).

1. STEP-level cylindrical-surface parameters — exact match, not approximate:

| Surface | v8 | pre-v8 (v7) | Match |
|---|---|---|---|
| Collar OD cylinder | r = 50.0mm (#25) | r = 50.0mm (#20) | exact |
| Bore ID cylinder | r = 40.0mm (#26) | r = 40.0mm (#21) | exact |

2. Mesh cross-section radius diff, z=138.5-153.3mm (v8 STL vs. pre-v8 STL, both independently
re-sliced with the same method):

| z (mm) | v8 outer | v7 outer | delta | v8 inner | v7 inner | delta |
|---|---|---|---|---|---|---|
| 138.5 | 44.004 | 44.002 | +0.002 | 40.000 | 40.000 | +0.000 |
| 140.0 | 45.028 | 45.038 | -0.010 | 40.000 | 40.000 | +0.000 |
| 142.0 | 47.008 | 47.025 | -0.017 | 40.000 | 40.000 | +0.000 |
| 145.0 | 49.793 | 49.811 | -0.018 | 40.000 | 40.000 | +0.000 |
| 145.5-153.3 | 50.000 | 50.000 | +0.000 | 39.987-40.000 | 39.959-40.000 | <=0.013 |

All differences are <=0.02mm — consistent with v8s mesh having ~2.75x more triangles than the
pre-v8 mesh (finer tessellation resolves the true analytic surface slightly more precisely), not a
real geometric change. Bore ID is constant 40.000mm (80mm ID) throughout in both.

3. P3->P4 external-blend peak overhang angle — matches the Coders reported figures almost
exactly: fine-resolution (0.05mm) slope scan across z=138.5-145.6mm:
- v8: peak 45.488deg from vertical at z=142.70mm.
- pre-v8: peak 45.472deg from vertical at z=142.90mm.
- Coder reported 45.48deg vs. v7s 45.46deg — my independent figures (45.488/45.472) match to within
  0.01-0.02deg. Confirms this feature is unchanged, still marginally over the 45deg guideline on a
  continuously curved surface (same previously-accepted "fine with adequate cooling" category this
  project settled on across RE-TEST PASS 2/3/7).

4. A small, pre-existing slope discontinuity found exactly at P3 (z=138.5mm) — present
identically in both v8 and pre-v8, i.e. confirmed inherited/unchanged, not a new defect:
fine-resolution (0.02mm) slope scan either side of z=138.5mm found a real, sudden dr/dz jump at
the exact P3 boundary in both files:
- v8: dr/dz goes from -0.0206 (just below P3, consistent with the required "flatten to dr/dz->0"
  taper-end condition) to +0.2161 immediately above.
- pre-v8: -0.0044 to +0.1092 at the identical location.
- A facet-adjacency-angle scan independently flags this same location (z=138.5mm) as the largest
  non-trivial angle anywhere on the body outside the legitimate flat-plane edges (~18.6deg in v8).

This is not new — its the same small residual imperfection this project already found, fixed
to a much smaller magnitude, and explicitly accepted in RE-TEST PASS 3 ("the largest single-step
slope change anywhere in this span is about a quarter of the size of the instantaneous jump I
measured last time at the exact same location" — my v8 measurement of a jump to dr/dz~0.22 is
indeed roughly a quarter of that original fully-broken chamfers 0.857mm/mm figure). Finding it
present at statistically the same magnitude and the exact same location in both v7 and v8 is
itself further, independent confirmation of byte-identity in this region, not a new problem —
noted for completeness since I found it while specifically scrutinizing this exact boundary, not
because it changes the pass/fail call.

Result: PASS — the critical check. P3-and-above is confirmed geometrically unchanged (to
within mesh-tessellation noise) across STEP parameters and mesh cross-sections, by four independent
methods. The lid/plug fit-critical region is intact.

## R84. Shoulder witness (P2) — radius and tangent confirmed matching the pre-accepted decision; one documentation-class discrepancy flagged (non-blocking)

Fine-resolution (0.01-0.02mm) scan pinpointing the exact witness point:

- Internal radius at Z_ext=112.5mm: 47.00015mm — matches the tasks pre-accepted "shallowed to
  internal r 47.0mm" framing exactly, not specs.md section 4.2.3s originally-written 45.0mm target.
  (For reference: v7s original pinch was r=42.42mm; the specs own "shallow" fallback direction
  was toward r~47.5mm if the built cavity came back low — the as-built 47.0mm sits almost exactly
  on that fallback trajectory, consistent with iterative volume tuning, though not itself
  documented as such anywhere I could find in specs.md.)
- Tangent slope: dr/dz = -0.4765 at z=112.5mm — matches the specs required -0.474 (~25.4deg from
  vertical, matched to the P1-P3 chord direction) closely.
- No sharp kink (G0/G1 break) found: dr/dz transitions smoothly through the witness point on
  both sides (-0.559 -> -0.521 -> -0.499 -> -0.479 -> -0.476 -> -0.477 -> -0.476 -> -0.459, sampled at
  0.5-2mm steps from z=110 to z=118) — no discontinuous jump anywhere near this point, unlike the
  genuine jump found at P3 (R83).

One discrepancy flagged, not blocking: the body 3MFs own metadata Description field (see R86)
explicitly self-describes this feature as a "G1 witness" — but specs.md section 4.2.3 explicitly
requires "G2 (curvature-continuous)" at this point ("matched on both sides, G2 (curvature-
continuous)... no kink"). I could not independently confirm or refute true G1-vs-G2
continuity from the mesh alone — second-derivative (d2r/dz2) estimates from a triangulated STL
are too noise-dominated at this resolution to reliably distinguish "tangent-matched only" from
"curvature-matched," and Im not asserting a defect I cant actually measure. What I can say:
no visible/measurable slope discontinuity exists here (the smoothness that would fail under either
G1 or G2 is absent), so this is, at most, a documentation-accuracy gap between what specs.md
requires and what the models own metadata says was built — not a demonstrated visible defect.
Unlike the radius value (45mm->47mm), this specific downgrade (G2->G1) was not named in this
tasks pre-accepted-decisions list. Recommend: specs.md/parameters.md be corrected to record
both the as-built radius (47.0mm, already covered) and the as-built continuity class (G1, per
the models own record) rather than leaving the G2 requirement standing as if fully met.
Flagged per this projects standing practice of not letting a spec-vs-built mismatch pass silently
— not a re-build trigger.

Result: PASS on the functionally load-bearing parts (radius matches the accepted decision,
tangent matches spec, no kink found); documentation note on the continuity-class claim.

## R85. Print orientation / overhang re-check — PASS, matches the Coders figures closely

- Base-to-belly flare (z~7-69mm, the classic "growing cone" overhang-relevant direction): peak
  angle from vertical 34.54deg at z=22.52mm — matches the Coders reported "max 34.58deg @ z26.5"
  closely (small difference attributable to sampling grid/method, not a real discrepancy).
  Comfortably under the 45deg guideline; confirmed self-supporting.
- Belly-to-shoulder-witness-to-P3 (z~69-138.5mm): confirmed monotonically non-increasing in radius
  across the full span (isolated <=0.01mm non-monotonic samples right at the belly-apex turning
  point itself are a sampling artifact at the exact peak, not a real reversal) — the
  "shrinking-radius, self-supporting regardless of local angle" class, unaffected by the locally
  steep -46deg angle found at z~95-96mm (R82).
- R7 external foot-fillet underside: the near-horizontal (>45deg-from-vertical) span runs from
  z=0 to where the local angle crosses 45deg-from-horizontal, interpolated at z~2.16mm (between
  the z=2.02mm sample at 43.1deg and the z=2.52mm sample at 49.8deg from horizontal). This is in the
  same small-and-routine ballpark as, though somewhat larger than, both the Coders reported
  ~1.90mm and the specs own theoretical R*(1-cos45deg)=2.05mm estimate for an idealized tangent
  case — all three describe the same "a few bridged layers at the very base edge, minor cosmetic
  sag at worst" outcome, not a functional concern regardless of which sub-2.2mm figure is used.
- Neck-to-collar blend peak overhang: 45.48-45.49deg (R83) — unchanged from v7, still in the
  previously-accepted "marginal, continuously curved, fine with adequate cooling" category.

Result: PASS on every sub-item, all closely matching the Coders independently-reported figures.

## R86. Lid and neck-fit-test confirmed genuinely untouched; body 3MF metadata refresh confirmed as claimed

Stronger than a timestamp check: git status --porcelain against the last commit
(1aeba56, "Update Large through v7...") shows zero diff for step/urn-lid.step,
3mf/urn-lid.3mf, stl/urn-lid.stl, step/neck-fit-test.step, 3mf/neck-fit-test.3mf, and
stl/neck-fit-test.stl — only urn-body.{step,3mf,stl} show as modified. Git compares actual
content hashes against the committed tree, which is a more decisive check than filesystem
timestamps alone (a file could be touched without its content changing, or vice versa on some
filesystems) — this confirms the lid and fit-test files are byte-identical to the last commit,
not merely "old-looking."

Timestamps corroborate independently: urn-lid.* dated Sep 2 17:32; neck-fit-test.* dated Aug
31 08:27 — both predate the body rebuild (Sep 10 18:03-18:07) by more than a week, consistent with
"never touched this round."

Body 3MF metadata refresh — confirmed present and accurate, not just claimed. Read the actual
metadata Description field from 3mf/urn-body.3mf; it now reads (excerpt): "...pet-
memorial-urn LARGE body, spec v8 (rounder thrown-ceramic profile, 2026-09-10). Belly max OD
153.93mm at Z~69; overall height 153.5mm; base contact OD ~89mm (R7 rounded foot); nominal wall
4.0mm radial (min perpendicular ~2.78mm on the steepest shoulder section)...shoulder tangent-break
removed to a G1 witness (internal r 47.0mm at Z 112.5), foot eased with an R7 external / R5
internal fillet...Neck ID 80mm / collar OD 100mm / 10mm collar band / bore / P3->P4 blend are
byte-identical to v7..." — this is a genuine, substantive content refresh (not a stale v2-era
log), matches the actual measured geometry (R76-R85 above independently corroborate essentially
every figure quoted in it, including the "G1 witness" language flagged in R84), and is exactly the
kind of metadata-only change the task said to expect and not treat as a geometry change.

Result: PASS on both sub-items — lid/fit-test confirmed untouched by the most decisive method
available (content-hash diff via git, not just timestamps), and the metadata refresh independently
verified accurate to the real geometry.

## R87. Standing item restated, not re-litigated

The 80mm neck ID remains ESTIMATED/untested against a real crematorium remains bag, gated behind
the physical neck-fit-test print (specs.md section 4.4/section 10 edge case 2). Unaffected by this v8
rebuild — confirmed directly in R83/R86 that the neck/bore/collar region is geometrically
unchanged and that neck-fit-test.* was not touched. This is not a new gate on the v8 revision
specifically; it is the same pre-existing open item this project has carried and restated since
the v5 neck-widening, and it still requires the requesters own physical test (or explicit written
risk acceptance) before being called closed.
