# Test Report — 2-Tube Hydroponic Propagation Stand (v4 spec)

Tested against `propagation-station/dot_pipeline/specs.md` (v4). Files tested (all under
`propagation-station/src/propagation_station/`):
- `propagation_station.stl` (use orientation)
- `propagation_station_print.stl` (print orientation, pre-rotated 30°)
- `propagation_station.step` (parametric source, both orientations)
- `propagation_station.3mf` (slicer-ready export, print orientation)

Tooling: no slicer application was found installed in this environment (checked for
PrusaSlicer/OrcaSlicer/Cura CLIs — none present), so overhang/support analysis below was done by
direct geometric face-normal analysis of the mesh (equivalent result to a slicer's
"supports needed" flag, just computed by hand rather than rendered). All dimensional
measurements below were taken directly from the actual mesh/BREP data (trimesh on the STL/3MF,
text-level BREP inspection of the STEP entities), not read off the spec's tables — i.e. these are
independent re-measurements, not a re-statement of what the spec claims.

---

## 0. BLOCKING — unresolved ESTIMATED dimension that mates with real hardware

**Tube OD (27mm) → bore diameter (28.5mm) is still an open item, per the spec's own §8, item 1
("OPEN... No physical tube has been measured yet — still open").** This is not resolved and not
explicitly waived by the product owner (contrast with §8 items 3/4/5, which *are* marked RESOLVED
with a clear decision trail). Per this pipeline's standing instruction to block on unverified
mating dimensions rather than let them pass by default, **this is flagged as a blocking issue,
not a pass-with-note.** See §1 below for what I *could* check (the model itself is dimensionally
correct against the spec's own — unverified — number) and §1a for a quantified reason the risk is
larger than the spec's text alone suggests.

**Recommendation:** do not proceed to a physical print run intended for actual use until one of:
(a) a manufacturer spec sheet for the tube to be purchased, (b) a caliper measurement of a real
sample, or (c) a ruler-photo of a real tube, confirms the OD — **or** the product owner
signs off in writing accepting the risk as-is (as they did for §8 items 3–5). A single low-cost
test print of one channel (mentioned in the spec's own §8 item 2 as a way to validate the slant
angle) would also serve to validate the bore/tube fit at the same time — recommend combining
those two open items into one physical test print rather than treating them separately.

---

## 1. Dimensional fidelity: model vs. spec's own numbers

Purpose: confirm nothing drifted during modeling — i.e., the model matches what the spec *claims*,
independent of whether that claim is itself correct (that's §0/§1a's concern).

| Parameter | Spec claim | Measured (mesh + STEP) | Result |
|---|---|---|---|
| Bore diameter | 28.5mm | **28.500mm** (both bores, use-orientation mesh: mean radius 14.24999991mm; STEP: `CYLINDRICAL_SURFACE(...,14.25)` for all 4 cylindrical surfaces across both orientations) | PASS — exact, no drift |
| Bore depth | 70mm | **70.000mm** (axial extent from blind floor to opening rim, both bores) | PASS |
| Channel center positions | X = ±17.25mm | **X = ±17.25000mm** exactly (floor centroids, both mesh and STEP origins) | PASS |
| Inter-channel land | 6mm | **6.03mm** (mesh min-distance between the two bore wall surfaces; algebraic check: 34.5mm spacing − 28.5mm bore = 6.0mm exactly) | PASS |
| Side-wall clearance | 8.5mm | **8.52–8.53mm** (mesh min-distance, bore wall to X=±40 side face, both sides) | PASS |
| Base foot thickness | 8mm | **8.003mm** (min Z of both blind-floor disks above the Z=0 bottom face) | PASS |
| Ceiling clearance above bore rim | ~8.1mm | **8.131mm** (91mm body height − 82.869mm, the highest Z point of the tilted rim-opening disk) — this is the spec's own envelope-math figure (overall height minus rim high-point), not a claim about a specific solid wall's perpendicular thickness at that spot; confirmed as computed, not a defect | PASS |
| Slant angle from vertical | 30° | **Exactly 30.0000°**, both bores (mesh: floor-cap normal = (0, 0.5, 0.866025) to 8 significant figures; STEP: `DIRECTION('center_axis',(...,-0.5,-0.866025403784439))` for both use-orientation cylinders, matching to ~1e-16) | PASS |
| Both bores parallel, same angle | required by design (§2.2) | **Confirmed** — both bores' axis directions match to floating-point noise (~1e-16) in both mesh and STEP; not fanned/mismatched | PASS |
| Print-orientation bore axes vertical | required by §6.2 | **Confirmed** — print-orientation mesh floor-cap normal = exactly (0, 0, 1) for both bores; STEP print-orientation cylinders' `center_axis` = exactly (0, 0, −1) for both | PASS |
| Overall envelope, use orientation | 80 × 80 × 91mm | **80.000 × 80.000 × 91.000mm** (mesh bounds) | PASS |
| Overall envelope, print orientation | ~80 × 114.8 × 93.1mm | **80.000 × 114.782 × 93.099mm** (mesh bounds; 3MF bounds match to the same figures) | PASS |
| Build volume fit (P2S, 256³mm) | comfortable margin | Largest axis (114.78mm) uses ~45% of 256mm travel — comfortable margin confirmed | PASS |

**Bottom line on §1: the Coder did not silently drift any of these numbers away from what the spec
specifies.** Every mating/structural dimension checked reproduces the spec's stated value to
within mesh-tessellation floating-point noise (≤0.03mm), and the two highest-risk geometric facts
(bore diameter, slant angle, and both bores' mutual parallelism/consistency) were independently
re-derived from the STEP BREP data as well as the STL mesh, not just trusted from one source. This
closes out the specific concern in the task brief about a possible "modeling error (wrong
rotation, one bore not matching the other)" — no such error was found.

### 1a. Why the still-open tube-OD risk (§0) is larger than the spec's text alone suggests

The spec's bore diameter (28.5mm) already assumes the printed hole comes out exactly nominal. In
practice, FDM-printed holes commonly print **~0.1–0.3mm undersized** versus the CAD nominal
(elephant's-foot / horizontal-expansion-compensation-adjacent effects, more pronounced on
larger-diameter holes cut against the grain of perimeter toolpaths). Applying that here:

- Nominal per-side clearance: (28.5 − 27) / 2 = **0.75mm** — already a fairly tight fit for a
  hand-inserted glass tube.
- With typical FDM hole shrink, the *as-printed* bore is more realistically **~28.2–28.4mm**, not
  28.5mm — per-side clearance drops to **~0.6–0.7mm**.
- The spec's own edge case §7.1 already flags that real glass tube stock varies **±1–2mm OD**
  across suppliers. If the real tube comes in anywhere above ~28.2mm OD (well within that
  supplier-variance band, and not even an extreme outlier), it will not physically fit the
  as-printed bore at all — not "fit loosely," not "fit at the wrong angle," but **fail to seat**.
- Conversely, if the real tube is narrower (e.g. 25–26mm, also within the stated variance), the
  now-larger effective per-side gap (potentially >1.5mm loose) defeats the retention/no-rattle
  intent named in §4.2 as one of the two reasons a blind bore was chosen over a shallow groove.

**This is not a new engineering flaw in the design — it's the same open risk the spec already
names in §4.1/§7.1/§8, quantified with the FDM-shrink factor added in.** It sharpens the case for
treating §0 as a hard blocker rather than a soft note: the margin was already thin (0.75mm/side)
before accounting for print shrink, and print shrink alone (with zero supplier deviation) plausibly
erodes it to the point of unreliable fit. **Routes back to the product owner/Planner, not to the
Coder** — there is no bore-geometry fix to apply until a real tube is measured.

---

## 2. Manifold / watertight geometry check

| File | Watertight | Euler number | Connected bodies | Winding consistent | Degenerate faces |
|---|---|---|---|---|---|
| `propagation_station.stl` (use) | **True** | 2 | **1** | True | 0 |
| `propagation_station_print.stl` (print) | **True** | 2 | **1** | True | 0 |
| `propagation_station.3mf` (print) | **True** | — (Scene wrapper) | 1 object | — | — |

**Independently checked for the "bore silently sealed into a trapped internal void" bug the Coder
mentioned fixing:** used `trimesh.split()` on both STL files to enumerate all connected mesh
components. **Result: exactly 1 connected component in each file**, matching the reported single
solid volume. A trapped/sealed internal cavity from a failed boolean would show up as a *second*,
separate closed manifold surface disconnected from the outer shell — none was found. Combined with
each bore's floor-cap facet being a flat disk that is provably open into a cylindrical wall leading
to the top surface (confirmed by the facet/axis analysis in §1), this independently confirms the
bore is a genuine open blind pocket, not a sealed void. **PASS — independently re-verified, not
just trusted from the Coder's note.**

Volume cross-check across exports (use STL vs. print STL vs. 3MF): 423,522.97mm³ / 423,522.97mm³ /
423,383.31mm³ — the ~140mm³ (0.03%) 3MF discrepancy is consistent with re-tessellation differences
(3MF has 932 verts/1860 tris vs. STL's 330 verts/656 faces — different mesh export, same
underlying BREP) and is not a geometric defect.

---

## 3. Wall thickness check (everywhere, not just the tables)

All of the spec's named thicknesses were independently re-measured directly off the mesh geometry
(not read from the spec's tables) — see the table in §1. All read correctly in the real model, all
comfortably above the stated 0.8mm (2×nozzle) structural minimum, most by an order of magnitude:

- Base foot: 8.00mm (10× minimum)
- Side wall: 8.5mm (10.6× minimum)
- Inter-channel land: 6.0mm (7.5× minimum)
- **One thickness not explicitly tabulated in the spec, found and worth recording:** the blind
  floor disk's closest approach to the **back face** (Y=−40 in model space) is **7.66mm** —
  comfortably solid, but this is the actual number behind the v3 correction narrative ("moving the
  channel opening position... to keep the blind floor's disk from breaking out the back face") and
  it was not itself stated as a figure anywhere in the spec. No action needed (well above minimum),
  just flagging that it exists and passes, since the spec's own text implies it was a near-miss at
  the previous height/position.

**No other thin-wall zones were found elsewhere in the body** — the two bores and the base are the
only cavities in an otherwise solid wedge, so there is no thin-shelled region to audit beyond
what's already covered above.

**PASS.**

---

## 4. Full overhang audit — print-orientation file

Method: face-normal angle from straight-down, standard 45°-from-vertical threshold (a face
oriented within 45° of horizontal-facing-down is flagged as needing support).

**Result: exactly one overhang region, area 6400mm² (a flat 80×80mm plane), angle 30° from
straight-down.** This face-and-area combination (80×80mm, the full original base-foot footprint)
is unambiguously **the known, accepted tilted-base-foot underside** named in §6.2 — confirmed by
cross-referencing against the same face in the use-orientation file (facet with normal (0,0,−1),
area 6400mm² = 80×80mm exactly, i.e. literally the full base foot before rotation). **No other
face in the entire print-orientation mesh (656 triangles checked individually, not just by
facet-group) crosses the 45° threshold.** In particular:
- No overhang inside either bore (confirms the whole point of the tilt strategy is actually
  working — both bore walls print as vertical cylinders with 0° overhang).
- No overhang at the rim edges, the land between channels, or any side/top face.

**PASS — only the one pre-accepted overhang exists; no other unexpected overhang, per the task's
explicit instruction not to re-flag the known one.**

### 4a. Bed adhesion — concrete finding, worth a slicer-setting note even though not a defect

Checked what portion of the print-orientation geometry actually touches the bed plane (Z=0) before
any supports are generated. **Result: only two vertices, both at Z=0, forming a single straight
edge spanning the full 80mm width (X=−40 to X=+40) at a single Y/Z coordinate** — i.e. the part's
own geometry contacts the bed along a **knife-edge line, not a face**, with zero native contact
area. This is the direct, expected consequence of the accepted tilt (§6.2) and is not a new
defect, but it does mean:
- **A brim (and enabled supports) are not optional niceties here — they are required for this
  print to have any real first-layer adhesion at all**, since without slicer-generated support
  filling the overhang, the model's own footprint provides no contact patch to adhere to, only a
  line.
- Recommend explicitly noting this in the print profile/instructions handed to whoever slices this
  (support enabled + brim), since "accept slicer-generated support" (as decided in §6.2) could be
  read as "some overhang needs support" rather than "the part has *zero* native bed contact area
  without it" — the second framing is the more accurate one and matters for how the print is set up.

---

## 5. Bounding box vs. build volume

`propagation_station_print.stl`: **80.000 × 114.782 × 93.099mm** vs. spec's claimed
"~80 × 114.8 × 93.1mm" — confirmed matching to 3 decimal places. Against the P2S 256×256×256mm
volume: largest axis (114.78mm) uses ~45% of travel. **PASS, comfortable margin**, consistent with
spec §4.5/§10.

---

## 6. STEP vs. STL/3MF consistency

- STEP file contains **both** orientations as separate named solids
  (`MANIFOLD_SOLID_BREP('PropagationStation_PrintOrientation', ...)` and
  `MANIFOLD_SOLID_BREP('PropagationStation_UseOrientation', ...)`), matching the spec's §10
  requirement that the parametric source carry both orientations. **PASS.**
- All 4 `CYLINDRICAL_SURFACE` entities (2 bores × 2 orientations) carry radius **14.25** exactly —
  matches the STL/3MF mesh measurements exactly, no drift between the parametric source and the
  exported mesh files. **PASS.**
- Axis directions cross-checked at the BREP level (not just mesh level): use-orientation bores'
  `center_axis` = (0, −0.5, −0.866025403784439) for **both** bores (agreeing to ~1e-16); print
  orientation bores' `center_axis` = (0, 0, −1) for **both** bores. Confirms the 30°
  angle/verticality claims independently of mesh tessellation. **PASS.**
- No self-intersection detected: zero degenerate triangles in either STL; convex-hull-to-mesh
  volume ratio (0.826) is consistent with a wedge shape with two cylindrical cavities removed, not
  indicative of a self-intersecting or overlapping boolean result.

**One process gap, not a geometry defect:** the `.3mf` file is a bare mesh container (single
`<object>` element, one "Title" metadata field reading literally `"(Unsaved)"`, no print-profile
metadata of any kind — no layer height, no infill, no support settings embedded). This does not
match the spirit of the spec's own file-path description of it as "Slicer-ready project export...
at the settings from §6.1/§9 once confirmed" (§10) — as delivered, it is geometry-only, not a
project file carrying the confirmed 0.2mm/15%-gyroid settings. Whoever prints from this 3MF will
need to manually re-apply those settings; they are not baked in despite the file being named/
described as if they were. **Recommend**: either regenerate the 3MF from an actual slicer with the
project settings saved into it, or update the spec's §10 description to say plainly that the 3MF
is geometry-only and settings must be applied manually.

---

## 7. Structural / usability tests

### 7.1 Drop test (accidental knock)
The printed body itself has no thin walls, bosses, or snap-fits to crack — every measured
thickness is 6mm+ (§3), and the shape is a solid wedge, not a shelled/ribbed structure. The
realistic drop/knock failure mode for this design is **not** the printed PLA body cracking under a
typical knock, but two distinct risks worth naming explicitly:
1. **The land between the two bore openings (6mm, the thinnest cross-section in the part) sits
   directly between two sharp-cornered circular openings** — a direct impact on that ridge (e.g.
   the stand tipping and landing edge-first) concentrates stress right where the two bore rims
   meet the top surface, a geometry that in brittle PLA is more prone to a clean crack than a
   thicker, unbroken cross-section would be. No fillet/radius was checked on that inner edge in the
   provided geometry. **Recommend a small fillet on the two circular rim intersections nearest the
   ridge, and/or PETG for this print** (see §8, material check) rather than assuming a knock only
   ever lands flat.
2. **The glass tube, not the printed part, is the more likely thing to break in a real "knock"
   event.** 80 of the tube's 150mm length protrudes unsupported past the bore opening (only 70mm
   is embedded/braced). A lateral knock to that overhanging length creates a real lever/moment
   against the rim edge where the tube exits the rigid bore — this is a glass-breakage risk
   inherent to the product concept itself (deep-embedment slant-holder for a fragile glass tube),
   not something a bore-geometry tweak fixes. Flagging as a genuine product-concept-level
   consideration (worth a user-facing care note, similar to §7.3's moisture note) rather than a
   fixable defect.

### 7.2 Load test (tipping stability)
Not re-derived from scratch (the spec's own §5 hand-math is thorough); instead **spot-checked the
input assumptions and the one edge case the spec explicitly asked the Tester to check**:
- **Both-tubes-filled case:** spec claims ~46% margin (36.7mm of the 80mm footprint depth) — the
  math checks out arithmetically as written; no independent CAD centroid measurement was available
  to me to confirm the ≈30mm/31.6mm stand-Y_com assumption the spec itself flags as unverified.
- **One-tube-filled, X-axis case (§7 edge case 2, explicitly flagged for Tester spot-check):**
  computed directly — combined system: stand (216g, X_com=0, symmetric) + one filled tube (~88.6g
  at X=17.25mm) → combined X_com ≈ (216×0 + 88.6×17.25)/(216+88.6) ≈ **5.0mm off-center**, against
  a 40mm half-width footprint edge. **Margin ≈35mm (~87.5% of the half-footprint) — comfortably
  tip-safe, confirms the spec's qualitative claim with an actual number.** **PASS.**
- Both the stand's mass (216g) and the payload figures ultimately trace back to an ESTIMATED
  linear-volume-scaling calculation, not a slicer-measured weight. **Recommend getting a real
  sliced/estimated-weight number from the actual print settings (15% gyroid, 3 perimeters) once a
  slicer is available**, as a cheap way to firm up the one hand-computed input in an otherwise
  solid margin.

### 7.3 Fit test
- **Primary bore-to-tube fit: BLOCKED, see §0/§1a** — this is the one fit test that cannot be
  closed out from files alone and is explicitly still open per the spec's own tracking.
  - There is **no secondary mounting hardware** for this design (no screws, clips, or fasteners
    mate to the tube or the stand) — so the general "does the visible opening fit but a hidden
    mounting screw doesn't clear" failure class does not have a direct analog here. The tube-to-
    bore fit *is* the entire fit-test surface area for this part.
- **Insertion/removal path:** confirmed a straight-line axial insertion has no interference —
  nothing else in the geometry (the other bore, the side walls, the top edge) sits in the path of
  inserting or withdrawing a straight tube along the bore's own axis. No issue found.

### 7.4 Use-case edge cases from the spec
- **Blind-bore moisture/algae buildup (§7 edge case 3):** already named as an accepted trade-off in
  the spec; I have nothing to add on the geometry side, but see §8 for a material-choice note that
  partially bears on this same edge case.
- **Uneven fill (§7 edge case 2):** closed out quantitatively in §7.2 above — safe margin,
  confirmed by calculation rather than left as a qualitative claim.

---

## 8. Material check (PLA vs. PETG/ABS)

The spec's PLA reasoning (§3) is sound as far as it goes — the water is contained in the glass
tube, not the printed plastic, and there's no cyclic-flex feature (no snap-fit, no living hinge, no
screw boss under repeated torque) that would be PLA's classic failure mode. However, two things
push back on treating PLA as a fully closed question rather than a default worth re-examining:

1. **The 6mm land between the two bore openings (§7.1 above) is the single most
   mechanically-concentrated feature in the part** — thin relative to everything else in the design
   (even though it's well above the print-minimum), sitting between two sharp internal corners,
   and directly in the path of a drop/knock landing on the top of the stand. PLA's brittleness
   (low impact toughness, tends to snap rather than flex/absorb) is a real, non-hypothetical risk
   specifically at this one feature, even though the part overall has no boss/hinge/snap-fit.
2. **A tube seated in the bore for extended periods will condense moisture on its *exterior*,
   directly against the PLA bore wall** — the spec's "water never touches the plastic" reasoning is
   accurate for the tube's *contents*, but the edge case the spec itself names (§7.3, condensation)
   means the PLA bore surface likely does see repeated, localized moisture contact over the
   product's real service life, which is a milder version of exactly the scenario the spec compares
   against (switch-plate screw bosses, a ratchet pawl) to justify PLA elsewhere in this shop's other
   projects — the comparison is less clean than the spec's confident phrasing suggests.

**Recommendation: PETG for this part**, specifically because of (1) — brittle-fracture risk at the
one genuinely stress-concentrated feature in an otherwise low-load part — with (2) as a secondary,
reinforcing reason. This is not a hard requirement (the part is genuinely low-load and PLA would
likely survive most real-world handling), but it's a specific, reasoned recommendation rather than
leaving PLA as an unexamined default, per this pipeline's standing material-check instruction.

---

## Summary of failures / defects found

**No geometry defects were found.** Every manifold/watertight/dimensional/angle check passed, and
the model was independently confirmed (via STEP BREP data, not just the STL mesh) to be free of
the "trapped void" class of bug the Coder previously fixed. The print-orientation file's overhang
profile is exactly the one accepted region and nothing else.

**Issues found, none of which are "fixable modeling defects" — all route to the product owner or
to slicer/print-setup practice, not to the Coder:**
1. **BLOCKING — Tube OD/bore-diameter fit is still an open, unverified mating dimension** (§0/§1a).
   Routes to the product owner for tube verification, not to the Coder — there is nothing wrong
   with the geometry itself.
2. Slant angle (30°) remains a first-pass estimate per the spec's own tracking, unvalidated by any
   physical fill test — confirmed correctly modeled (exactly 30°, both bores, both orientations),
   but the angle-choice-itself is unvalidated. Routes to the product owner (§8 item 2), not a
   modeling defect.
3. The `.3mf` export is geometry-only, missing the print-profile settings its own file description
   implies it carries (§6). Process/tooling gap, not a geometry defect.
4. Bed adhesion for the print-orientation file is a literal knife-edge (zero native contact area)
   — expected given the accepted tilt trade-off, but concrete enough to warrant an explicit
   brim/supports-required note in whatever print instructions accompany this file (§4a).
5. Material recommendation: PETG over PLA, specifically for the inter-channel land's impact
   resistance (§8) — a recommendation, not a blocking defect.
