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
