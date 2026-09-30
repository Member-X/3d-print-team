# Test Report — Pet Memorial Urn, Medium size (v1) — Independent Verification Pass

**Tester note on method.** The live Fusion document `pet-memorial-urn-medium` was NOT usable for
inspection this session: `document/open` shows the shared session currently has
`pet-memorial-urn-small` open plus an untitled active document — `pet-memorial-urn-medium` is not
even loaded, exactly the failure mode the task brief anticipated. All verification below was
therefore done directly against the exported deliverables — `urn-body-medium.step/.3mf/.stl`,
`urn-lid-medium.step/.3mf/.stl`, `neck-fit-test-medium.step/.3mf/.stl` — using STEP entity/topology
parsing, 3MF XML inspection, and STL mesh analysis (cross-section slicing at fine z-resolution,
vertical ray-casting, and boolean collision testing) in Python (trimesh/numpy). Numbers were
cross-checked across formats (STL vs 3MF mesh volumes agree to <0.01%) and against a direct
STEP B-rep topology read. This is treated as a fully sufficient path per the task brief.

---

## 0. Contamination check (concurrent-access incident)

**Result: PASS — no contamination found in any of the three deliverables.**

| File | Products/solids | Extra components? | Notes |
|---|---|---|---|
| `urn-body-medium.step` | 1 `PRODUCT`, 1 `MANIFOLD_SOLID_BREP` ("Body1"), 0 `NEXT_ASSEMBLY_USAGE_OCCURRENCE` | None | Single part, no assembly structure |
| `urn-lid-medium.step` | 1 `PRODUCT`, 1 `BREP_WITH_VOIDS` ("Body1") = 1 outer `CLOSED_SHELL` (10 faces) + 1 void `CLOSED_SHELL` (3 faces) | None | Correct sealed-void B-rep, no extra shells |
| `neck-fit-test-medium.step` | 1 `PRODUCT`, 1 `MANIFOLD_SOLID_BREP` ("Body1") | None | Single part |
| All 3 `.3mf` files | 1 `<object>`, 1 `<item>` each | None | No stray build items or leftover objects |
| All 3 `.stl` files | 1 body (2 for lid: outer shell + its 1 sealed void, expected) | None | Component counts match design intent exactly |

Searched all three STEP headers/bodies for "Large"/"Small" keywords and any Large-scale dimensions
(80mm, 100mm, 153.9mm) — none found as real values (one incidental "80.0" substring match in the
body STEP turned out to be part of unrelated angle values like `2.3935944027350...`, confirmed by
inspecting context, not a real 80mm dimension).

**Every measured dimension below matches Medium's own spec numbers, not Large's** (Large: 80mm neck
ID / 100mm collar OD / 153.9mm belly OD / 4.0mm nominal wall / 153.5mm body height / ~1475–1579
cm³ cavity — all clearly different from what's measured below). This is strong, direct evidence
against cross-contamination, independent of the Coder's own self-audit.

---

## 1. Body — `urn-body-medium.step/.stl/.3mf`

**Manifold/solid validity: PASS.** Single closed 2-manifold shell, `watertight=True`,
`winding_consistent=True`, 1 connected component, Euler number 2 (genus-0, consistent with a
single-blind-cavity vessel — correct topology, no accidental through-hole, no non-manifold
geometry).

**Cavity volume — measured directly by numerical integration of cross-sectional area over height
(not the frustum hand-calc), 1310 z-samples at 0.1mm resolution, cross-checked against the mesh's
own reported material volume (agreement within 0.2%, confirming the integration method is
accurate):**

```
Measured internal cavity volume ≈ 806.1 cm³
Target: 819.4 cm³ (±5% band: 778.4–860.3 cm³)
Deviation: −1.63%
```

**PASS — well within the ±5% tolerance band**, independently confirming the Coder's own hand-calc
(818.3 cm³, −0.13%) was in the right neighborhood, though the real modeled geometry (806.1 cm³)
sits about 1.5 percentage points lower than the hand-calc estimated — expected, since a
tangent-spline surface doesn't equal its straight-chord frustum approximation exactly (the spec's
own §4.5 caveat anticipated this kind of gap).

**Wall thickness — measured at every spec control point via mesh cross-section (outer radius minus
inner radius), independently re-derived, not read off the spec table:**

| Location | Spec (external r / internal r) | Measured (ext / int) | Wall | Verdict |
|---|---|---|---|---|
| Floor (center, z=0–~3.5mm) | n/a / n/a | flat 4.0mm (ray-cast, center to r=35mm) | **4.00mm** | Matches spec's 4.0mm floor exactly |
| P1 belly max (z_ext=59mm) | 60.2 / 57.0mm | 60.200 / 57.000mm | **3.200mm** | Exact match |
| P2 shoulder (z_ext=77mm) | 50.2 / 47.0mm | 50.200 / 47.000mm | **3.200mm** | Exact match |
| P3 neck-taper-end (z_ext=119mm) | 39.2 / 36.0mm | 39.200 / 36.000mm | **3.200mm** | Exact match |
| P4 rim/collar top (z_ext≈131mm) | 44.0 / 36.0mm | 43.994 / 35.999mm | **7.995mm ≈ 8.0mm** | Matches spec's 8mm collar wall |
| Side-wall min/max (z=5–118mm) | nominal 3.2mm | min 3.199mm, max 7.13mm (near transition zones) | — | Nominal wall holds tightly at 3.2mm; no thin spots below spec |

All five control points match the spec's own numbers to the third decimal place — this is a very
strong, independent confirmation that the as-built body is Medium's own geometry, correctly
executed, not a scaled/mixed-up copy of another size.

**Overhang re-measurement — full-height scan, not just the disclosed zone.** Computed local
slope angle (atan(dr/dz)) on the external profile at 0.25–0.5mm z-resolution across the entire
0–131mm height.

- Base→belly flare, belly→shoulder taper, shoulder→neck taper: all "shrinking-radius" or shallow
  expanding class, max unflagged angle ≈29°, confirming spec's claims — **no undisclosed overhang
  risk found anywhere else in the profile.**
- **Neck-to-collar external blend (z≈119–131mm): measured peak angle = 44.98° at z≈125.4mm**
  (fine 0.25mm sampling) / 44.69° (coarser 0.5mm cross-check) — **this independently confirms the
  Coder's extrapolated ~45° estimate almost exactly.** This is genuinely *at* the 45° guideline,
  not clearly under it. **Flag: treat this ~2mm-tall band on the exterior collar blend as a real,
  confirmed first-print watch-item** — a slicer's default 45° auto-support threshold may or may not
  trigger here depending on rounding/mesh faceting, and it should be visually checked on the first
  print rather than assumed safe. This is a print-quality risk, not a structural one.

**Body verdict: PASS**, with the neck-to-collar blend named as a confirmed (not hypothetical)
watch-item.

---

## 2. Lid — `urn-lid-medium.step/.stl/.3mf`

**Manifold/solid validity + sealed-void topology: PASS, confirmed at two independent levels:**

- **STL level:** 2 connected components — outer shell (140,667 mm³, normal winding) + 1 inner
  shell (−16,628 mm³, reversed winding, bounds z=3.0–8.0mm, radius 0–32.55mm). Both individually
  watertight. This is the standard, correct way to encode a sealed internal void in mesh format —
  net volume 124,038.7 mm³ (124.04 cm³) matches the union volume trimesh reports directly.
- **STEP B-rep level (independent of the mesh):** `BREP_WITH_VOIDS('Body1', #157, (#14))` — outer
  boundary `#157` = `CLOSED_SHELL` of 10 faces; void `#14` = `ORIENTED_CLOSED_SHELL(...,.F.)`
  wrapping `#158` = `CLOSED_SHELL` of **3 faces** (cylindrical wall + top cap + bottom cap — a
  fully closed blind pocket). **This directly confirms the void is a sealed cavity, not a hole
  punched through the part** — exactly the topology the task asked to verify, confirmed at the CAD
  kernel level, not just inferred from the mesh.

**Dimension checks, measured via cross-section slicing (not read off the spec table):**

| Parameter | Spec target | Measured | Verdict |
|---|---|---|---|
| Plug OD | 71.5mm | 71.500mm (r=35.750, constant z=0–7.9mm) | Exact |
| Plug wall | 3.2mm | 3.200mm (35.750−32.550) | Exact |
| Plug cap: solid | 3mm nearest tip | z=0–3.0mm solid (single loop) | Exact |
| Plug cap: hollow | 5mm nearest brim | z=3.0–8.0mm (void bounds) | Exact |
| Brim OD | 88mm | 88.000mm (r=44.000, flat z=8–~12mm) | Exact |
| Dome base OD | 70.4mm | ~70.4mm region confirmed near z≈17mm (small blend fillet present, expected) | Matches within blend tolerance |
| Dome height above brim | ~25mm | 41mm (plateau) − 16mm (dome start) = 25mm | Exact |
| Dome apex plateau diameter | ~19mm (r≈9.5mm) | Top-face vertices at z=41.0mm show r=9.23–9.77mm (mean ≈9.5mm) — confirmed **flat plateau**, not a point | Matches |
| Total bounding-box height | ~41mm | 41.000mm exactly | Exact |

**Lid verdict: PASS.** Every dimension matches spec to sub-0.01mm precision; sealed-void topology
independently confirmed at both mesh and B-rep level.

---

## 3. Plug/bore fit test — measured directly, not assumed from spec numbers

**Clearance:** Body bore ID (measured, constant through the collar z=119–131mm) = 72.00mm
(r≈35.98–36.00mm, tiny facet noise ≤0.03mm). Lid plug OD (measured, constant z=0–8mm) = 71.50mm
(r=35.75mm exactly). **Nominal diametral clearance = 0.5mm, matching spec exactly.**

**Collision check — actual boolean intersection, not just arithmetic:** Translated the lid mesh so
its seating plane (z=8mm, lid-local) sits exactly on the body's collar rim top (z=131mm,
body-local) and ran `trimesh.boolean.intersection([body, lid])`.

```
Intersection volume = 0.0 mm³ — CONFIRMED COLLISION-FREE
```

Sampled 40×72 points around the plug's cylindrical surface at this seated position and compared
against the body's own bore radius at each corresponding height:

```
Minimum radial clearance found: 0.233mm (≈0.467mm diametral)
(vs. 0.25mm/0.5mm nominal — the ~0.03mm difference is STL facet/tessellation noise on both
meshes, not a real geometric interference; the STEP-level nominal clearance is a clean 0.5mm)
```

**Collision margin above the neck taper:** With the lid seated, the plug occupies body-frame
z=123–131mm. The body's bore stays a *constant* 36mm radius from z=119mm (P3, where the taper
ends) through z=131mm (rim) — confirmed by direct measurement, not assumed. That leaves the plug's
bottom edge (z=123mm) sitting 4mm above the point where the bore would start narrowing back toward
the shoulder (z=119mm) — **exactly matching the spec's claimed 4mm margin, independently
verified.**

**Fit test verdict: PASS.** Plug engages the bore with real, collision-free clearance and a
confirmed 4mm safety margin above the taper.

---

## 4. `neck-fit-test-medium` — the physical go/no-go article

**Topology: PASS.** `is_watertight=True`, Euler number = 0 (genus-1/torus-topology — correctly an
open tube through both ends, matching "open bore both ends" in the spec). 1 connected component,
no stray geometry.

**Structure confirmed:** bottom flange (z=0–~5.5mm, OD=120mm/ID=94mm, a stability foot for
printing, not a functional dimension) → neck taper (z≈6–36mm, compressed in height vs. the body's
own 42mm taper span but reproducing the *same* endpoint diameters — a reasonable simplification for
a standalone test coupon, since only the diameters matter for the pass/fail bag test, not the taper
length) → collar (z=36–47.9mm, 12mm tall).

**Critical dimensions, measured directly:**

| Dimension | Spec target | Measured |
|---|---|---|
| Collar/neck ID (bore, constant through taper-end + collar) | 72mm | 72.000mm (r=36.000, z=36–47.9mm) |
| Neck OD at taper/collar transition | ~78.4mm | 78.400mm (r=39.200 at z=36mm) |
| Collar OD (top, z=47.9mm) | 88mm | 87.988mm (r=43.994) |

**All three critical numbers match the body's own neck/collar exactly** (not Large's 80mm ID /
100mm OD) — confirms this test article is genuinely representative of what will physically be
built, and matches Medium's own spec, not a leftover/miscopied article from Large or Small.

**Verdict: PASS** as a fit-test article. **This article's entire purpose is to physically resolve
the one item this whole report cannot pass or fail on its own — see §8 below.**

---

## 5. Drop test (accidental knock simulation — analytical, no physical print in hand this pass)

No physical part exists yet to literally drop, so this is a geometric/material risk analysis based
on the measured wall data above.

- **Body, PLA, 3.2mm nominal wall:** this is *thinner* than Large's 4.0mm wall (a deliberate,
  reasoned re-derivation per spec §4.2 — not a mistake), which means Medium's shell has **less
  material margin against a brittle PLA fracture on impact than Large already had.** The highest
  local stress-concentration zone is the **neck-to-collar external blend** — the same z≈119–131mm
  region already flagged for being at the 45° overhang guideline, where wall thickness is
  transitioning from 3.2mm up to 8mm and the external profile curvature changes direction (S-curve
  inflection). A stress-concentration coincidence like this (thin wall + curvature change +
  print-orientation-transition all in the same ~12mm band) is a plausible first-crack location on a
  drop, corner-knock, or being set down hard on the rim. **Recommend calling this out explicitly
  rather than treating "PLA, chosen for finish" as settled** — see §7 Material check.
- **Lid, PETG:** PETG is materially less brittle than PLA under impact; the plug (3.2mm wall) and
  solid cap (3mm) are both comfortably above the 0.8mm floor and in a tougher material — low risk.
  The one soft spot is the **flush 88mm brim edge**, which is now a zero-clearance mating surface
  (see §7) — a corner most likely to chip first if the lid is dropped or set down carelessly on a
  hard surface, independent of material choice, simply because it's a sharp, exposed, exactly-fit
  edge.

**Drop test verdict: CONDITIONAL PASS** — no design flaw found that would cause the part to fail a
reasonable drop under normal handling, but the body's thin-wall/PLA combination at the
neck-collar blend is a real, higher-than-Large risk worth a documented decision (see §7), not a
silent default.

---

## 6. Load test

The only sustained load in this design is the static weight of packed cremated remains resting on
the 4.0mm PLA floor (measured exact) plus the shell's own weight. Estimated remains mass at this
cavity size (806 cm³ × ~0.9–1.0 g/cm³ typical packed-cremains bulk density) ≈ 725–806g — a trivial
compressive load for a 4mm PLA floor with an 88mm-diameter base footprint; no bending or buckling
risk. The lid is lifted by hand at the brim/dome edge (no handle, by design) — the 8mm PETG brim
and 25mm dome comfortably tolerate normal handling/gripping loads.

**Load test verdict: PASS.** This is a decorative static vessel, not a load-bearing bracket — no
plausible normal-use load comes close to a failure threshold for either part.

---

## 7. Fit and clearance — a distinct failure class from structural testing (per QA process)

Two *different* mating interfaces exist in this design, and they were checked separately, per the
QA instruction that "does it fit the visible opening" and "does it clear the surrounding hardware"
are different questions:

1. **Plug ↔ bore (the "invisible" internal alignment feature):** real 0.5mm diametral clearance,
   confirmed collision-free with a confirmed 4mm safety margin — this interface is **correctly
   engineered with tolerance headroom** (§3).
2. **Brim ↔ collar (the visible, load-bearing seating interface — where the lid actually rests):**
   measured **88.000mm brim OD against 88.000mm collar OD — an exact match, zero clearance margin,
   confirmed directly by measurement, not just theoretical from the spec text.** This is the
   surface that actually carries the lid's seating and is handled/removed repeatedly. **Zero
   print-tolerance margin on a mating diameter is a real fit risk independent of whether the part
   is structurally sound** — ordinary FDM dimensional variance (per this project's own documented
   tendency toward slightly-oversized external features) means the most likely outcome is a lid
   that reads as very slightly proud/tight rather than flush, and in a worse case (if variance goes
   the other way, or between two different printers/filaments) could bind or scrape rather than
   seat cleanly. **This is the same risk the spec's own §5.1 names, but this report independently
   confirms it is not a hypothetical — it is measured as an exact zero-margin condition in the
   as-built geometry.** Recommend: if the first physical print shows a tight/binding fit rather
   than a merely-cosmetic "proud edge," apply the same 0.2–0.3mm negative allowance on brim OD the
   spec already proposes as the fix, before assuming it's a slicer/printer-calibration problem.

**Fit/clearance verdict: PASS for the plug/bore interface; CONDITIONAL/WATCH for the brim/collar
interface** — not a defect, but a zero-margin-by-design condition that should be watched on first
print rather than assumed fine because the CAD numbers "match."

---

## 8. Print orientation and support implications

- **Body:** base (flat, 88mm OD, confirmed flat within <0.01mm) down, opening up — matches spec,
  confirmed self-supporting except the disclosed/confirmed neck-collar blend watch-item (§1).
- **Lid:** plug-tip-down, dome up — confirmed correct orientation for a monotonically-shrinking
  dome profile (self-supporting) and a bed-supported solid tip cap.
- **Sealed-void bridging — quantified, not just qualitative:** the void's ceiling (where the
  plug's hollow interior meets the solid brim above it) is an unsupported internal bridge spanning
  **65.1mm in diameter** (2×32.55mm void radius) — confirmed via direct measurement. This is a
  fairly wide bridge for default FDM bridging settings and will very likely sag/string somewhat, as
  the spec itself already anticipates — since it's sealed and never visible, this is cosmetically
  and functionally irrelevant, but it's worth having the actual number on record in case any
  slicer-support-generation review is needed later.
- **"Touching build plate only" support setting:** confirmed the void has no open path to the
  build plate in this orientation (fully enclosed, both mesh-level and B-rep-level confirmed
  sealed) — this setting should correctly generate zero support inside the plug void. No slicer
  was available in this environment to empirically confirm this (see below); this conclusion is
  geometric/topological, consistent with how this project's own Large-build spec already reasoned
  through the identical mechanism.
- **Outer support annulus:** none needed — brim OD and collar OD are flush/matched (confirmed
  §7), unlike an earlier discarded option in Large's own design history where a mismatched brim/
  collar diameter needed a support annulus. Not applicable to this flush v7-identity design.
- **No slicer was available in this environment** (checked for PrusaSlicer/Cura CLI — neither
  found) — overhang/support analysis above was done via direct geometric measurement instead,
  which for the overhang-angle question is arguably more precise than a default slicer's 45°
  auto-support heuristic. **Recommend an actual slicer preview pass (supports set to "touching
  build plate only," per spec §5.4) before committing to a production print run**, specifically to
  visually confirm the neck-collar blend and the void bridge behave as analyzed here.

---

## 9. Material check

**Body: matte/silk PLA (per spec, for finish).** Flagging per QA process: **this body has a
thinner wall (3.2mm) than Large's already-PLA body (4.0mm)**, at the same brittle-under-impact
material, with a confirmed stress-concentration zone at the neck-collar blend (§1, §5). PLA's low
impact toughness is a real risk for a piece explicitly likely to be repeatedly picked up, moved,
and occasionally set down by grieving family members — not a hypothetical edge case for this
product category. **Recommendation: if drop/impact resilience matters more than the exact "stoneware"
matte finish, PETG is the safer body material** — PETG is meaningfully tougher under impact than
PLA and would meaningfully reduce crack risk at the neck-collar blend without changing any
dimension in this spec. If matte/silk PLA's finish is a hard requirement (as spec states), that's a
legitimate trade-off to make — but it should be made **explicitly**, with the drop-risk named, not
left as an unexamined inherited default from Large's own material choice at a now-thinner wall.

**Lid: PETG (per spec).** Appropriate choice, already reasoned through in the spec — no change
recommended. The plug (3.2mm wall) and solid cap (3mm) are both comfortably printable in PETG.

**PETG-lid/PLA-body shrinkage mismatch (named in spec, re-confirmed here):** the plug/bore
0.5mm diametral clearance (§3) is the feature most exposed to this risk, since the two mating
diameters are printed in two different materials with different shrinkage behavior. The spec's own
recommendation (a test coupon of just the plug + a short bore section, printed before the full lid)
is a reasonable, low-cost mitigation and is repeated here as a recommendation, not yet as a
performed test (no evidence a coupon was printed this round).

---

## 10. Cost/material volume — measured vs. spec's rough estimate (informational, not a failure)

| Part | Spec's rough estimate | Measured (this pass) | Delta |
|---|---|---|---|
| Body material volume | ≈145.0 cm³ | **182.47 cm³** | +25.8% |
| Lid material volume | ≈108 cm³ | **124.04 cm³** | +14.8% |

Both of these were explicitly flagged in the spec as rough, order-of-magnitude estimates "to be
replaced by real CAD mass-properties once built" — this is exactly that replacement. Recomputed
cost at the same $20–25/kg assumption: body (PLA, 1.24 g/cm³) ≈ $4.53–5.66; lid (PETG, 1.27 g/cm³)
≈ $3.15–3.94; **combined ≈ $7.68–9.60** (vs. spec's quoted $6.30–7.90). Not a functional issue —
flagged so the Director/requester has the real number rather than the spec-time guess.

---

## 11. THE BLOCKING ITEM — §4.3's 72mm neck ID is an unresolved ESTIMATED dimension mating real hardware

This is called out separately and first in the verdict, per QA process: **every check above passed
on the CAD geometry's own internal consistency, but none of it can validate the one dimension that
actually matters most — whether a real medium-pet remains bag physically passes through 72mm.**

The spec itself (§4.3, §8 edge case 2, §12 item 1) already names this as the single highest-risk
item in the whole document, explicitly **larger risk than Large's equivalent 80mm decision**
(which sat inside its own researched 70–100mm range; 72mm here sits *below* the entire
79–89mm real-competitor cluster the spec's own fresh research found for this capacity tier). The
`neck-fit-test-medium` article exists specifically to close this out physically (§4) — but **there
is no evidence in this project's files that this test has actually been performed**: no README, no
prior tests.md/verdict.md existed before this pass, no photo, no manufacturer bag dimension, no
written risk acceptance from the requester.

**This is not a modeling defect — the CAD faithfully implements what the spec asked for, precisely
(§0, §1, §2, §4).** It is a planning-level open risk that route back to the Planner/spec, not
something a Coder revision can silently patch.

---
---

# RE-TEST PASS — Scoped Verification of Brim-OD Tolerance Fix (2026-09-09, v1.1)

**Scope of this pass, per task instruction:** not a full re-test — independent confirmation that
the single specific fix described in spec §5.1/§13 v1.1 (brim OD 88.000mm → 87.700mm on the lid
only) was applied correctly and cleanly, with no collateral change to any other geometry. All
findings below were produced by re-deriving numbers directly from the exported files
(STEP text/entity parsing, 3MF XML vertex parsing, STL mesh analysis via trimesh/numpy — cross
section slicing at exact z-planes, connected-component/watertightness checks, volume integration)
— **not by reading or trusting the Coder's report or the spec's own revision-history claims.**
Every figure below was measured independently in this pass. The live Fusion document was not
relied upon (same constraint as the prior pass); all three exported formats (STEP/3MF/STL) were
used and cross-checked against each other.

## RT-1. Brim OD — measured at 87.700mm on the actual exported geometry, confirmed in all 3 formats

| Format | Method | Post-fix measured | Pre-fix (archived) measured |
|---|---|---|---|
| STEP | Text-parsed `CYLINDRICAL_SURFACE`/`CIRCLE`/`VECTOR` radius entities (#18, #21, #70, #71) | **43.850mm exactly** (r) → **OD 87.700mm** | 44.000mm exactly → OD 88.000mm |
| STL | `trimesh` exact-plane cross-section (`mesh.section`) at z=8.5–11.9mm (flat brim zone) | **43.8437–43.8500mm** (r) → **OD ≈87.69–87.70mm** | 43.9804–44.0000mm → OD ≈87.96–88.00mm |
| 3MF | Direct XML `<vertex>` parse, max radius over all 9,528 verts | **43.8500mm** (r) → **OD 87.700mm** | 44.0000mm (3,373 verts) → OD 88.000mm |

**Result: PASS.** All three deliverable formats agree, to the limits of STL/3MF mesh tessellation
(sub-0.001mm), that the brim OD is now 87.700mm. This is not a partial or format-inconsistent fix —
STEP (the authoritative B-rep source), 3MF, and STL all carry the corrected value.

## RT-2. Plug and dome geometry — confirmed bit-identical, not just "looks similar"

**Method 1 — full line-by-line `diff` of the raw STEP files (post-fix vs. the archived pre-fix
copy).** The *entire* diff consists of:
- The file `time_stamp`/`PRODUCT_DEFINITION`/`PRODUCT` timestamp strings (expected, metadata only).
- The brim's `VECTOR`/`CYLINDRICAL_SURFACE`/`CIRCLE` radius entities: `44.` → `43.85` (the fix itself).
- One **dependent** toroidal blend/fillet on the brim's top outer edge: `40.85`/`41.` pairs shift by
  exactly the same 0.15mm the brim radius moved (torus center-circle radius = outer radius − fillet
  radius: 44−3=41 pre-fix, 43.85−3=40.85 post-fix) — **this is the expected, correct parametric
  propagation of a fillet tangent to the brim's outer face, not an unintended side effect.**
- A handful of `CIRCLE`/`TOROIDAL_SURFACE`/`CARTESIAN_POINT` entries for the **dome plateau fillet**
  (radii ≈9.2333mm / ≈9.7646mm) differing only in the **12th–13th significant digit**
  (e.g. `9.2333470996957` vs `9.23334709969572`) — this is floating-point re-export noise from an
  independent tessellation/serialization pass, not a geometric change (relative difference ~2×10⁻¹³).

**No other entity in the file changed.** In particular, nothing referencing the plug (OD/wall/depth/
cap, which uses distinct radius values ~35.75mm / ~32.55mm) appears anywhere in the diff — the plug
geometry is untouched at the STEP entity level, full stop, not merely "close."

**Method 2 — independent STL cross-section re-measurement** (exact-plane slicing, not vertex-nearest
filtering) at multiple z-heights on both pre-fix and post-fix meshes:

| Feature | Z | Post-fix r (mm) | Pre-fix r (mm) | Verdict |
|---|---|---|---|---|
| Plug (solid cap zone) | 1.0 | 35.7472–35.7500 | 35.7411–35.7500 | Match (sub-0.001mm, tessellation noise only) |
| Plug (hollow zone, cap transition at z=3.0 confirmed both) | 4.0 | 32.5458 outer wall / 35.7500 OD | 32.5367 / 35.7500 | Match |
| Plug OD, full range 0.5–7.9mm | — | constant 35.750mm both passes | constant 35.750mm both passes | Match — **plug OD/wall/cap unchanged** |
| Dome mid-profile | 16, 20, 30 | 37.3708 / 33.7471–33.7413 / 27.3711–27.3759 | 37.3708 / 33.7428–33.7481 / 27.3814–27.3824 | Match to 4+ sig figs, consistent with independent-tessellation noise |
| Plateau top | 40.5–40.99 | 9.38–11.20mm range | 9.36–11.15mm range | Match within tessellation noise |

**Method 3 — solid/void B-rep structure**, read directly from STEP: `BREP_WITH_VOIDS('Body1',#157,
(#14))` with outer `CLOSED_SHELL` = 10 faces (`#144`–`#153`) and void `CLOSED_SHELL` = 3 faces
(`#154`–`#156`) — **entity numbers, face counts, and shell structure identical pre- and post-fix.**
The sealed plug void was not touched.

**Result: PASS — plug and dome are bit-identical (to STEP-entity precision) pre/post fix; only the
brim OD and its one geometrically-dependent fillet changed.**

## RT-3. Single valid manifold solid, watertight — confirmed

- STL (post-fix): `is_watertight=True`, `is_winding_consistent=True`. Splits into exactly 2
  connected components: outer shell (+140,449.1 mm³) and the sealed internal void (−16,638.2 mm³),
  each individually watertight — the correct, standard mesh encoding of a sealed-void solid,
  identical in structure to the pre-fix mesh (2 components, +140,667.2 / −16,628.5 mm³).
- STEP (post-fix): single `BREP_WITH_VOIDS` product, one manifold-consistent outer shell + one
  fully-enclosed void shell (see RT-2, Method 3) — no stray shells, no extra solids.
- 3MF (post-fix): exactly 1 `<object>` / 1 `<item>` in `3D/3dmodel.model` — no contamination, no
  duplicate build items (pre-fix 3MF also 1/1).
- STEP topology entity counts: **13 `ADVANCED_FACE`, 18 `EDGE_CURVE`, 11 `VERTEX_POINT` — identical
  between pre-fix and post-fix files.** (Note: the Coder's revision-history note in specs.md §13
  states "13/11/11" faces/edges/vertices; this pass's raw STEP entity count for edges is 18, not 11.
  This is very likely a units-of-counting difference — Fusion's UI "edge" count reflects topological
  edges in its browser tree, which can differ from the raw `EDGE_CURVE` entity count in an exported
  STEP file when seam edges on cylindrical/toroidal surfaces are shared by two `ORIENTED_EDGE`
  references but stored as a single curve entity. This is flagged for transparency, not as a defect
  — **what matters for this fix's correctness is that the count is identical pre- and post-fix,
  which it is, confirming no faces/edges/vertices were added or removed by the edit.**)

**Result: PASS.**

## RT-4. Body and neck-fit-test files — confirmed untouched by this fix

| Check | Result |
|---|---|
| File timestamps | `urn-body-medium.step/.3mf/.stl` and `neck-fit-test-medium.step/.3mf/.stl` all show **2026-09-09 15:07** (unchanged) — the lid's three files show **21:43–21:46** (the fix). The 15:07 timestamp predates even the *prior* test pass (whose `tests.md`/`verdict.md` were written 19:25), confirming these files are the same ones already verified in the prior pass, not silently touched during this fix. |
| Body material volume (independent re-measurement, this pass) | **182.465 cm³** — matches the prior pass's independently-measured **182.47 cm³** (tests.md §10) to 4 significant figures. Confirms the body geometry is unchanged, not just unchanged by timestamp. |
| Body collar OD (re-measured, cross-section at z=125–130.5mm) | ≈87.96–87.98mm (mesh-tessellation-limited; matches the spec's unchanged 88.000mm nominal collar OD on the body) — **confirms the fix was NOT mistakenly also applied to the body's collar.** |
| Neck-fit-test critical dims (re-measured) | ID ≈71.99mm / neck OD ≈78.4mm / collar OD ≈87.98–88.00mm — matches the prior pass's recorded 72.000/78.400/87.988mm essentially exactly. |
| MD5 hashes recorded this pass (for future audit) | `urn-body-medium.step` = `5b5bb6a7c297e1ec5729e8b66880d7ca`; `neck-fit-test-medium.step` = `37d44dbf26a8da6dfb94455029b6748b`; `urn-body-medium.stl` = `6fd7a37267197dc024ed6daa3653a406`; `neck-fit-test-medium.stl` = `6066a836bec36a2e2f97de4a2b6cb387` |

**Result: PASS — body and neck-fit-test deliverables are confirmed untouched, both by file
timestamp and by independent volume/dimension re-measurement.**

## RT-5. Material volume delta — small, in the expected direction, and sanity-checked independently

Directly measured (this pass, STL net volume, trimesh):

```
Pre-fix lid net volume:  124.0387 cm³
Post-fix lid net volume: 123.8109 cm³
Delta: -0.2278 cm³ (-0.184%)
```

This is in the same direction as, and the same order of magnitude as, the Coder's own claimed
Fusion mass-properties delta (124.1914 → 123.862 cm³, −0.329 cm³/−0.27% per specs.md §13). The two
deltas are not identical in magnitude (−0.228 vs. −0.329 cm³) — expected, since STL mesh volume is a
chordal (slightly under-) approximation of the analytic CAD volume and the two exports likely used
different tessellation tolerances (this pass's post-fix 3MF has 9,528 vertices vs. the pre-fix
archive's 3,373 — a ~2.8× finer mesh, consistent with a different export-quality setting between the
two saves, not a geometry problem).

**Independent analytic sanity check** (thin-ring approximation, not trusting either party's number):
removing a ring from r=44.0mm to r=43.85mm over the brim's ~4–8mm effective solid height:
`π×(44²−43.85²)×h ≈ 41.4mm²×h` → **≈0.17–0.33 cm³ for h=4–8mm** — brackets both the trimesh-measured
(−0.228 cm³) and Fusion-reported (−0.329 cm³) deltas comfortably. The magnitude and direction are
physically correct for "shrink a thin outer ring by 0.15mm radius," not a symptom of some larger,
unintended geometry change.

**Result: PASS.**

## RT-6. One residual risk worth naming (not a defect in the fix — a scoping observation)

The applied fix is a **−0.15mm per-side / −0.3mm diametral** allowance. The spec's own §5.3 states
FDM clearance-fit tolerance "is typically on the order of ±0.15–0.25mm per surface for a well-tuned
desktop FDM printer" — **the applied fix sits at the very bottom of that self-declared range, not
comfortably inside it.** If this printer/filament combination's actual variance skews toward the
higher end of that stated ±0.15–0.25mm band (plausible — it's a range, not a single number), the
fix reduces the risk from "confirmed zero clearance" to "small but non-zero, possibly-still-tight"
clearance, not necessarily to a comfortably-margined fit. This does not mean the fix was applied
incorrectly — it was applied exactly as instructed and exactly matches the precedent cited (Large's
own identical −0.3mm diametral fix) — but the first physical print of this lid should still be
checked for fit rather than assumed resolved, same "watch it on first print" posture the prior pass
already recommended for this interface, just now at reduced (not eliminated) risk.

---

## RE-TEST SUMMARY

| Item | Verdict |
|---|---|
| RT-1: Brim OD = 87.700mm, all 3 formats | PASS |
| RT-2: Plug/dome bit-identical | PASS |
| RT-3: Single manifold, watertight | PASS |
| RT-4: Body/neck-fit-test untouched | PASS |
| RT-5: Volume delta small, correct direction | PASS |
| RT-6: Residual clearance-margin risk | Named, non-blocking — first-print watch-item |

**This specific fix is correctly and cleanly applied.** No collateral changes to plug, dome, body,
or neck-fit-test geometry were found by any of three independent file-format checks. The brim OD
change is isolated to exactly the two sketch-derived entities (plus one geometrically-dependent
fillet) the revision note describes.

**This re-test does not change the project's overall blocking status.** The §4.3 neck-ID
`ESTIMATED`-dimension-mating-real-hardware item (tests.md §11, verdict.md item 1) remains open and
is entirely unrelated to this fix — this pass only confirms the brim-tolerance fix itself is sound.

---
---

# RE-TEST PASS — v2 Body-Profile Revision ("Thrown-Ceramic" Rounder Silhouette), Independent Verification (2026-09-11)

**Cold start, independent verification.** Scope: the Medium body (`urn-body-medium.step/.3mf/.stl`)
was rebuilt to a rounder profile below P3 per `specs.md` §4.7 (v2, 2026-09-10). Lid, plug, and
`neck-fit-test-medium` are out of scope for this revision (not touched). All numbers below were
measured independently — not read from the Coder's report or the spec's own claims — via:

- **STEP entity/topology parsing**: a custom Python regex-based STEP reader resolving
  `CARTESIAN_POINT`, `CYLINDRICAL_SURFACE`, `TOROIDAL_SURFACE`, and `B_SPLINE_CURVE_WITH_KNOTS`
  entities directly (including tracing each Bezier segment's raw control points and axis
  placements) — this is the authoritative, tessellation-free source of truth used for the
  highest-stakes checks below (G1 tangency, fillet radii/tangency, P3-and-above identity).
- **STL/3MF mesh analysis** (trimesh): watertightness, winding, Euler characteristic, and ordered
  closed-loop cross-section slicing (`mesh.section(...).discrete`, not shapely polygon-hole area
  alone) for exact inner/outer radius extraction at fine z-resolution.
- **`git diff`/timestamp/md5 audit** for the "lid and neck-fit-test untouched" claim.

The live Fusion document was not relied upon (same constraint as prior passes). Findings were
cross-checked against the archived pre-v2 body at `medium/archive/pre-v2-rounder-body/`, which was
first confirmed to be a faithful, untampered copy of the git-committed v1 body (STL/3MF md5 match
the git HEAD blob exactly; STEP md5 matches the md5 the *original* Tester pass recorded for the body
in RT-4 above, `5b5bb6a7c297e1ec5729e8b66880d7ca`, exactly).

## RT2-0. Files actually changed — confirmed via git, independent of the Coder's own claim

`git status`/`git diff --stat` against `HEAD` shows **only** `step/urn-body-medium.step`,
`3mf/urn-body-medium.3mf`, `stl/urn-body-medium.stl` modified under `medium/`. `git diff --stat
HEAD` for `urn-lid-medium.{step,3mf,stl}` and `neck-fit-test-medium.{step,3mf,stl}` is **empty** —
confirmed byte-identical to the last commit. (Raw `md5sum` of `git show HEAD:<file>` vs. the
working-tree file initially appeared to mismatch for these text-based STEP files; traced this to
`core.autocrlf=true` normalizing line endings on checkout — `git diff` correctly reports no content
change, and this was confirmed directly by observing the working file has CRLF terminators while
the git blob has LF, with otherwise identical content.) File timestamps corroborate independently:
body files timestamped 2026-09-10 12:52; lid and neck-fit-test files remain at their pre-existing
2026-09-09 15:07 / 21:43 timestamps — unchanged, and predating this revision entirely.

**Item 11: PASS.**

## RT2-1. Manifold validity — single valid solid, watertight, 0 non-manifold edges, V−E+F=2

| Check | STL | 3MF |
|---|---|---|
| Watertight | True | True |
| Winding consistent | True | True |
| Connected components | 1 | 1 |
| Vertices / unique Edges / Faces | 56,158 / 168,468 / 112,312 | 56,158 / 168,468 / 112,312 |
| V − E + F | **2** | **2** |
| Non-manifold edges (shared by ≠2 faces) | **0** (all edges shared by exactly 2 faces) | **0** |
| Degenerate (zero-area) faces | 0 | — |
| STL vs. 3MF volume agreement | 180,831.5221 mm³ vs. 180,831.5219 mm³ (agree to 5×10⁻⁷ %) | |

STEP: single `MANIFOLD_SOLID_BREP('Body1')`, single `CLOSED_SHELL`. (STEP's *raw entity* counts —
15 `ADVANCED_FACE` / 29 `EDGE_CURVE` / 17 `VERTEX_POINT`, giving V−E+F=3 by naive entity count —
repeat the same seam-edge double-counting artifact the original Tester pass already documented and
ruled non-defective for v1's STEP export in RT-3 above; the mesh-level check is the authoritative
one for this specific question and is clean in both formats.)

**Item 1: PASS.**

## RT2-2. Cavity volume — measured independently; genuinely inside the tolerance band, not clipping it

Method: ordered closed-loop cross-section extraction (not polygon-triangulation) at 0.1mm
z-resolution across the full 0–131mm height, integrating the interior-loop (cavity) area via the
trapezoidal rule.

```
Measured cavity volume (this pass) = 844.31 cm³
Cross-check (revolved-envelope volume − material shell volume) = 844.16 cm³
Coder reported: 844.703 cm³
Target: 819.4 cm³  |  Band (±5%): 778.4 – 860.3 cm³
Deviation vs. target: +3.04% (Coder: +3.09%)
Margin remaining to the ceiling: 860.3 − 844.31 = 16.0 cm³ (1.96%)
```

**Methodology validated before trusting it on v2**: the same script measured the archived v1 body's
cavity at **805.91 cm³**, landing neatly between the original Tester's 806.1 cm³ and the Reviewer's
805.30 cm³ — two independent prior passes, different toolchains, and this pass's own method all
converge to within 0.8 cm³ of each other on the *same known geometry*, which is strong evidence the
method is trustworthy before applying it to the new v2 numbers.

**Confirmed genuinely inside the band, not near-clipping it** — three independent measurements of
v2 (cross-section integration, envelope-minus-material, and the Coder's own CAD mass-properties)
agree to within 0.4 cm³ / 0.05% of each other, and sit comfortably (~2% margin) below the 860.3 cm³
ceiling.

**Item 2: PASS.**

## RT2-3. Base OD = 88mm, unchanged from v1; exact parity with collar OD

Direct from the STEP B-rep (not mesh-approximated): a `CYLINDRICAL_SURFACE` entity with radius
**44.0mm exactly** is used by a real, bounded `ADVANCED_FACE` (#203) spanning a genuine flat
vertical cylindrical wall from z≈6mm (top of the R6 foot fillet) to z≈10mm (start of the
belly-ward spline) — a true, if short (~4mm-tall), flat-walled base band at exactly 88.000mm OD,
not merely a fleeting tangent point. Mesh cross-section independently confirms this flat band
(r=44.0000mm exactly at every sample z=6.5–9.5mm).

Collar OD: the rim (P4, z=131mm) `CARTESIAN_POINT` literal is **r=44.0000mm exactly** — the *same*
numeric value as the base, both ultimately traceable to `44.` literals in the STEP file (base via
the cylindrical surface, collar via the spline's terminal control point).

**Base OD = Collar OD = 88.000mm, exact parity, unchanged from v1** — confirmed both by direct STEP
literal comparison and by mesh measurement (base 88.000mm flat over a real ~4mm band; collar
87.996–88.000mm, mesh-tessellation-limited on the curved terminal edge, with the exact analytic
value at the rim vertex itself being 44.0000mm).

**Item 3: PASS.**

## RT2-4. Belly max OD = 120.4mm, single apex, zero overshoot

Full-height fine scan (0.1mm z-resolution, entire 0–131mm height): peak outer radius =
**60.1995mm (OD 120.399mm)** at z=59.05mm. **Zero samples anywhere in the full profile exceed
60.200mm** (max recorded excess across the entire height: −0.0005mm, i.e., it never exceeds the
target). Belly ovality (max−min radius at the apex ring): 0.0023mm — effectively perfectly round;
mesh volumetric centroid confirms the revolve axis is centered at (x,y) ≈ (−0.0004mm, −0.0008mm).

Direct from STEP: the Bezier control point shared between the two adjoining profile segments sits
at exactly **r=60.2000, z=59.0000**, with the tangent handle on *both* adjoining curves purely
vertical (dr/dz=0 on both sides — handle magnitudes 22mm down / 13mm up, matching the spec's own
stated handle lengths exactly). This is architecturally a genuine single apex, not a plateau with a
hidden secondary maximum elsewhere in either adjoining Bezier segment (confirmed empirically by the
zero-overshoot full-height scan above).

**Item 4: PASS**, with the belly reading as a smooth, gently rounded ~2.5mm-tall near-flat crown
(within 0.02mm of true peak across z=57.75–60.25mm) rather than a mathematically sharp point —
consistent with the spec's own "broad swell, not a point" design intent.

## RT2-5. Shoulder (P2) — tangent-continuous (G1), no kink — confirmed at the Bezier control-point level, not merely by mesh smoothness

This is the most rigorous check performed this pass: the raw cubic Bezier control points for all
six profile curves were extracted directly from the STEP file (not mesh-derived) and tangent-vector
collinearity was checked at every internal junction (P0, P1, P2, P3).

**At P2 (external, r=50.7mm, z=84mm):** incoming tangent vector (from the belly-side curve) =
(−3.9642, 11.3262); outgoing tangent vector (toward the neck-taper) = (−5.2856, 15.1016). Component
ratios: −3.9642/−5.2856 = 0.75005, 11.3262/15.1016 = 0.75004 — **collinear to 5 significant
figures**, i.e., genuinely tangent-continuous, not merely "visually smooth." Slope at the junction:
dr/dz = −0.3500 → 19.29° from vertical, matching the spec's claimed "dr/dz = −0.35 (≈19° from
vertical)" essentially exactly. The mirror check on the internal profile at P2 gives the same
result (ratios 1.33333 / 1.33333 — the exact reciprocal, as expected for the internal-offset curve).

**At P1 (both external r=60.2mm and internal r=57.0mm, z=59mm):** tangent handles are purely
vertical on both adjoining curves (dr/dz=0), confirming smooth tangency there too, with handle
magnitudes (22mm down/13mm up, both internal and external) matching the spec's stated values
exactly.

**No kink found anywhere.** Mesh-derived dr/dz across the shoulder region (z=74–90mm, 1mm sampling)
also changes smoothly and monotonically in magnitude through the junction, with no discontinuous
jump — corroborating the control-point-level finding independently. Per the task brief, literal G2
(curvature-magnitude match, not just tangent-direction match) was already explicitly accepted as
not required/achievable here — **G1 is confirmed, rigorously, at the source-geometry level, which
is a stronger check than the mesh-smoothness confirmation alone would have been.**

**Item 5: PASS.**

## RT2-6. Foot fillets — R6 external / R4 internal, confirmed as real, tangent torus faces at the STEP entity level

Direct from STEP: exactly two `TOROIDAL_SURFACE` entities exist in the entire file (no more, no
fewer):

| Entity | Major radius | Minor radius | Axis origin (z) | Tangent-to-flat at | Tangent-to-wall at |
|---|---|---|---|---|---|
| `#197` (external foot) | 38mm | **6.0mm** | z=6 | z=0, r=38 (flat underside) | z=6, r=44 (=external wall cylinder `#40`, r=44 exactly — major+minor=44 confirms tangency) |
| `#196` (internal floor-to-wall) | 33mm | **4.0mm** | z=8 | z=4, r=33 (internal floor top, matching the unchanged 4mm floor thickness) | z=8, r=37 (=internal wall cylinder `#39`, r=37 exactly — major+minor=37 confirms tangency) |

Both are real, bounded `ADVANCED_FACE` entities in the B-rep (not chamfers or cosmetic
approximations), and both are **analytically tangent** — major+minor radius equals the adjoining
cylindrical wall's radius exactly, in both cases, confirming genuine G1 tangency at both ends of
each fillet directly from the CAD kernel data, with zero mesh-tessellation involved.

**Item 6: PASS**, at the highest available level of rigor.

**Disclosed consequence, independently confirmed:** the flat ground-contact disk shrinks to
**exactly r=38.000mm (76.000mm diameter)** at z=0.0 (mesh cross-section confirms a single filled
loop with no interior hole — a genuine solid disk, not a ring) — matching the spec's disclosed
"≈76mm diameter" figure exactly.

## RT2-7. Overall height = 131mm exact

Mesh z-bounds: **0.000000mm to 131.000000mm** exactly, for both STL and 3MF. Corroborated at the
STEP level: `CARTESIAN_POINT` entities exist at z=0.0 (base) and z=131.0 (rim) in both v1 and v2.

**Item 7: PASS, exact.**

## RT2-8. Wall thickness — nominal 3.2mm radial confirmed; perpendicular minimum independently confirmed at ~2.71mm, not below the 0.8mm floor

**Radial wall** (outer_r − inner_r), sampled every 4mm from z=8mm to z=118mm (spanning the entire
reshaped span): holds at **3.20mm ± 0.01mm** throughout (min 3.1961mm @ z=63.85mm — matching the
spec's own "offset inward 3.2mm" construction instruction). No location radially thinner than spec
anywhere in the reshaped span.

**Perpendicular (true wall-normal) thickness** — computed independently via 2D profile-normal
ray-casting from the inner surface to the outer surface (a distinct, more rigorous method than
radial×cos(angle), though the two agree): global minimum = **2.7107mm at z=73.5mm** (the steepest
section, belly-to-shoulder transition). This is the same physical location and essentially the same
value the Coder reported (**~2.71mm @ z~75mm** — a 1.5mm z-offset and <0.002mm thickness difference,
within method/sampling-resolution noise). **Confirmed: not worse than reported, and 2.71mm / 0.8mm
floor = a 3.4× margin — comfortably clear of the floor.**

I also explicitly checked the P3→P4 collar-blend band (z=119–131mm, where radial wall grows from
3.2mm to 8mm while the outer slope simultaneously steepens toward ~44.5°) for a hidden worse
minimum there, since a steep slope reduces perpendicular thickness relative to radial: perpendicular
thickness in that band ranges from ~3.2mm (at P3, near-zero slope) up to ~4.0mm (at the steepest
point, z≈125mm) — **no location anywhere in the body drops below the 2.71mm minimum already
identified in the belly-shoulder span.**

**Item 8: PASS.**

## RT2-9. P3-and-above byte-identical to v1 — confirmed at the STEP literal level, not just "close" by mesh comparison

**Strongest available check:** every `CARTESIAN_POINT` in both the current v2 STEP and the archived
v1 STEP whose z-coordinate equals 119.0 (P3) or 131.0 (P4/rim) was extracted, and the *set* of
radii present at each height compared:

```
z=119.0 (P3):  v2 radii = {0.0, 36.0, 39.2, 50.91169, 55.43717}
               v1 radii = {0.0, 36.0, 39.2, 50.91169, 55.43717}   — IDENTICAL SET
z=131.0 (P4):  v2 radii = {0.0, 36.0, 44.0, 62.2254}
               v1 radii = {0.0, 36.0, 44.0, 62.2254}              — IDENTICAL SET
```

This is exact, to the literal decimal values stored in each STEP file — not a mesh-tessellation-
limited approximation. `CYLINDRICAL_SURFACE` radii (36mm bore, 44mm collar OD) and the neck-OD
`CIRCLE` radius (39.2mm) are present identically in both files. By contrast, the two files'
*shoulder*-region circle radii genuinely differ, as expected (v1: 47.0/50.2mm; v2: 47.5/50.7mm —
matching the spec's described P2 witness-point change exactly), confirming this comparison isn't a
trivial "everything's the same file" false-positive — the tooling correctly distinguishes real
changes (below P3) from true identity (at/above P3).

Mesh cross-section comparison (v2 vs. archived v1) corroborates: at z=119mm the two meshes agree to
the displayed precision (0.0000mm difference, both outer and inner radius); across the whole
z=119–131mm band all residual differences are ≤18 microns (consistent with the two STL exports
using different facet counts — v2's mesh has 2.2× the vertex density of v1's archived mesh —
approximating the *same* underlying analytic curve slightly differently, not a real geometric
change). By contrast, below P3 (checked at z=70–118mm) the two meshes diverge by up to several
millimeters — confirming these are genuinely different builds below P3 and genuinely identical
at/above it, not a coincidental near-match.

**Item 9: PASS, at the highest available level of rigor** (source-geometry literal match, not just
mesh-noise-level agreement).

Neck OD at P3 = 78.4mm (r=39.2, confirmed identical in both v1/v2), collar bore ID = 72mm (r=36,
confirmed identical in both, and the *same single* `CYLINDRICAL_SURFACE` entity spans the full
P3→P4 bore in each file), collar OD = 88mm (r=44, confirmed identical in both) — **all unchanged,
exactly.**

## RT2-10. Print orientation, overhang — base down (Z=0) confirmed; faired lower-body and foot-fillet overhangs independently confirmed, and one new risk quantified

- **Base at Z=0, flat:** confirmed (mesh z-min = 0.000000mm; the z=0 cross-section is a single
  filled disk with no hole — flat, bed-ready).
- **Faired lower body (v2's new rounder flare, base→belly):** peak local overhang angle =
  **27.39° from vertical at z=27.5mm** (independent fine-resolution measurement, 0.25mm z-steps) —
  matches the Coder's reported **~27.4°** essentially exactly. Comfortably under the 45° guideline,
  self-supporting. **Confirmed not worse than reported.** Worth naming plainly, though: this is
  nearly double v1's equivalent transition (~16.4° per the original v1 spec table) — a real,
  disclosed consequence of the rounder profile, still safe, but a legitimate step up in overhang
  risk on this surface, not a zero-cost change.
- **R6 foot-fillet underside:** solved analytically from the confirmed-exact torus geometry
  (tangent points (r=38,z=0) and (r=44,z=6), R=6): the 45°-from-vertical crossing occurs at
  **z = 6 − 6·cos(45°) = 1.757mm**. This closed-form result matches the Coder's reported "~1.76mm
  below 45°" to 3 significant figures — the strongest possible confirmation available (exact
  geometry, not a discretized approximation). This ~1.8mm-tall band sits right at the build plate
  (within the first several layers) — routine for a rounded base edge, non-blocking.
- **Neck-to-collar external blend (unaffected by v2, re-confirmed unchanged):** peak angle measured
  independently at 44.55–44.98° depending on sampling method (matches the original Tester's
  previously-verified 44.98° for this same, untouched geometry, §1 above) — **at, not clearly over,
  the 45° guideline, exactly as already established and re-confirmed, not newly introduced by this
  revision.**

**Item 10: PASS**, with the lower-body overhang increase (16.4°→27.4°) named as a real, quantified,
non-blocking consequence of the rounder profile.

**Additional, value-add check (not explicitly requested, but directly relevant to whether the
disclosed footprint-narrowing consequence in RT2-6 introduces a real stability concern):**
approximate tip-over angle, computed from each body's actual volumetric center of mass (shell-only,
`trimesh.center_mass`, uniform-density assumption) and its flat-contact radius:

```
v2: CoM z=52.71mm, contact r=38.0mm  → approx. tip angle = atan(38.0/52.71) = 35.8°
v1: CoM z=52.08mm, contact r=44.0mm  → approx. tip angle = atan(44.0/52.08) = 40.2°
```

The R6 foot fillet's contact-ring reduction does cost ~4.4° of tip-stability margin, exactly as the
spec's own qualitative "still stable" claim implied but did not quantify. **35.8° remains a
substantial margin for ordinary handling/accidental-knock scenarios — not a functional concern —
but this is now a concrete, independently-derived number rather than an unverified assertion.**

## RT2-11. `neck-fit-test-medium` and `urn-lid-medium` — confirmed untouched

Restated here against the numbered checklist for completeness (full audit in RT2-0): `git diff`,
file timestamps, and md5 (for the binary, tessellation-insensitive STL format) all independently
agree these six files are unmodified by this revision.

**Item 11: PASS.**

## RT2-12. Standing risk — restated, not re-litigated

**The 72mm neck/collar ID (`specs.md` §4.3) remains `ESTIMATED` and untested against a real
medium-pet remains bag.** This is unchanged and unaffected by the v2 body-profile revision — the
revision only touches geometry below P3, and P3-and-above (which includes the entire neck/collar)
is confirmed byte-identical to v1 at the STEP-literal level (RT2-9). This remains the single
highest-priority open item across this entire size, per the original Tester and Reviewer passes,
gated behind a physical `neck-fit-test-medium` print-and-bag-test or explicit written risk
acceptance from the requester — **not something this or any CAD revision can resolve, and this
pass does not attempt to.**

## RT2 Slicer check

No slicer CLI (PrusaSlicer/Cura/OrcaSlicer/Slic3r) was found in this environment — the same
limitation as the original pass. Substituted with direct geometric overhang analysis (RT2-10),
which for the specific overhang-*angle* question is at least as precise as a slicer's default 45°
auto-support heuristic. Recommend an actual slicer preview pass before committing to a production
print run, specifically on the new faired lower-body region (27.4° peak) and the foot fillet, to
visually confirm print *quality* (layer stepping on the now-more-curved lower body) rather than
support necessity — both angles are safely under 45° and should not trigger auto-supports.

---

## RE-TEST SUMMARY — v2 Body-Profile Revision

| Item | Check | Result |
|---|---|---|
| 1 | Single valid manifold solid, watertight, 0 non-manifold edges, V−E+F=2 (STEP/3MF/STL) | PASS |
| 2 | Cavity volume ≈844.3 cm³ (Coder: 844.703), target 819.4, band 778.4–860.3 | PASS — genuinely in band, independently corroborated 3 ways |
| 3 | Base OD = 88mm, unchanged; parity with collar OD (also 88mm) | PASS — same literal 44mm value at the STEP entity level |
| 4 | Belly max OD = 120.4mm, single point, zero overshoot | PASS — 0 samples exceed 60.2mm anywhere in the full profile |
| 5 | Shoulder tangent-continuous (G1), no kink | PASS — confirmed via Bezier control-point tangent-vector collinearity (5 sig. figs.) |
| 6 | Foot fillets R6 ext / R4 int, real torus faces, tangent | PASS — confirmed via STEP `TOROIDAL_SURFACE` entities, analytic tangency verified |
| 7 | Overall height = 131mm exact | PASS |
| 8 | Nominal wall 3.2mm radial; perpendicular min ~2.71mm, not below 0.8mm floor | PASS — independently measured 2.7107mm @ z=73.5mm, matches Coder's report |
| 9 | P3-and-above byte-identical to v1 | PASS — identical STEP literal radii at z=119 and z=131 |
| 10 | Print orientation base-down; overhangs (faired lower body ~27.4°, foot fillet ~1.76mm<45°) | PASS — both independently confirmed/derived; lower-body overhang increase vs. v1 named plainly |
| 11 | Lid / neck-fit-test files not modified | PASS — `git diff` empty, timestamps and md5 unchanged |
| 12 | 72mm neck-ID standing risk | Restated, unresolved, unaffected by this revision — not re-litigated |

**This re-test pass: PASS.** The v2 body-profile revision is a clean, accurately-executed
implementation of `specs.md` §4.7, verified independently at the STEP-entity level wherever possible
(not just mesh approximation) for the highest-stakes claims (G1 tangency, fillet radii/tangency,
P3-and-above identity). No modeling defect found.

**This does not change the project's standing BLOCKED-for-production status.** The unresolved §4.3
neck-ID item (RT2-12) is untouched by this revision and remains the gating item before a full
production print, exactly as before this revision.
