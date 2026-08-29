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
