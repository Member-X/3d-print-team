# Test Report — Lightswitch-Cover-Single

Independent QA pass against the Fusion document `Lightswitch-Cover-Single`
(`urn:adsk.wipprod:dm.lineage:SszZxJywRyKQ40XwWnR3GQ`). All numbers below were
read directly from the live Fusion geometry via the Fusion MCP script tool
(`adsk.core`/`adsk.fusion` face/edge/vertex introspection), not copied from
`specs.md` or the Coder's notes. Internal Fusion units are cm; all values are
converted to mm. Axis convention used throughout: X = width, Y = thickness
(5mm), Z = height.

Bodies in the document:

| Index | Name | Role |
|---|---|---|
| 0 | `Body1` | Original reference, background only, not tested |
| 1 | `Lightswitch Cover Single V2 (corrected jumbo)` | **Primary test target** |
| 2 | `Lightswitch Cover Single V2 (tapered edge)` | **Secondary test target** (cosmetic variant) |

---

## 1. Body count / topology sanity

| Body | isSolid | lumps | faces | edges | vertices | volume | surface area |
|---|---|---|---|---|---|---|---|
| corrected jumbo | True | 1 | 35 | 82 | 58 | 22.4765 cm³ | 281.7788 cm² |
| tapered edge | True | 1 | 51 | 114 | 74 | 22.0409 cm³ | 275.9237 cm² |

Both target bodies are single connected solids (`lumps.count == 1`,
`isSolid == True` on both) — no accidental splits or free-floating shells.
Face/edge/vertex counts are internally consistent between the two bodies once
the added fillet is accounted for (see §2).

Overall envelope for both bodies, measured directly from the bounding box:
**88.9000mm (X) × 139.7000mm (Z) × 5.0000mm (Y)** — exact match to the
3.5"×5.5"×5mm jumbo single-gang spec.

## 2. Tapered-edge body: diff against corrected-jumbo

A full face-geometry-type histogram (cylinder/cone/torus/plane, grouped by
radius/angle) was taken on both bodies and compared. Every feature radius
present on the corrected-jumbo body is present on the tapered-edge body in
identical counts:

- Countersink cones, 45° half-angle (90° included): 2 on each body
- Shank cylinders, r=2.3813mm: 2 on each
- Boss collar cylinders, r=4.5mm: 2 on each
- Toggle-opening corner cylinders, r=1.59mm: 4 on each
- Outer corner fillet cylinders, r=2.35mm: 4 on each
- Pocket-corner fillet cylinders, r=0.7mm: 4 on each

The **only** addition on the tapered-edge body is:
- 8× cylindrical faces, r=1.5mm (4 straight edges × 2 loops — front and back
  outer perimeter)
- 8× toroidal corner-blend faces, minor radius=1.5mm (4 corners × 2 loops)

This is exactly the 1.5mm-radius edge fillet on the front and back outer
perimeter edges described in the background, and **nothing else** differs —
no stray geometry changes, no accidental modification to the screw holes,
toggle opening, or pocket. 16 new faces (8+8) accounts for the 35→51 face
count delta precisely.

**Finding: no unexpected differences between the two bodies.** The tapered
variant is confirmed to be the corrected-jumbo body plus only the documented
1.5mm edge fillet.

## 3. Screw hole verification (measured on corrected-jumbo; identical on tapered-edge)

Measured directly on the hole at Z=+30.1625mm (mirror-identical at
Z=−30.1625mm):

| Feature | Measured value | Notes |
|---|---|---|
| Screw hole spacing (center-to-center) | **60.3250mm** exact | Matches 2.375" NEMA spec exactly |
| Countersink half-angle | **45.00°** (90° included) | Genuine `Cone` surface type — confirmed NOT a straight counterbore/cylinder |
| Countersink top diameter | **7.9375mm** exact | = 5/16", matches retail spec |
| Countersink depth (Y 3.4125→5.0000) | **1.5875mm** | |
| Shank cylinder diameter | **4.7625mm** exact (r=2.3813mm) | = 3/16", matches retail spec |
| Shank straight-section depth (Y 3.1000→3.4125) | **0.3125mm** | |
| **Total guide-channel depth** (countersink + shank) | **1.9000mm exact** | Matches background's "~1.9mm" claim precisely |
| Boss collar outer diameter | **9.0000mm** exact | Matches noted 9mm boss diameter |
| Boss collar wall thickness (radial, around shank) | **2.1188mm** (4.5 − 2.3813mm) | |

**Open-path verification (critical check):** the corrected-jumbo body's
complete face list (all 35 faces) was enumerated and inspected. Only 8 faces
touch either screw-hole location (cone, shank cylinder, flat boss annulus,
collar wall — ×2 holes). No other face — not the ceiling, not the outer
rim, not any other feature — occupies the space at the hole's (X,Z) location
for Y between 0 (back face) and 3.10mm (boss floor). Since every face on the
body was enumerated (not sampled), this is a definitive confirmation that the
channel opens into completely open, unobstructed space all the way to the
back opening: **a screw inserted from the front can pass all the way
through.**

## 4. Wall thickness vs. 0.4mm-nozzle minimum (0.8mm)

| Location | Measured thickness | Margin over 0.8mm min |
|---|---|---|
| General cavity skin (front face Y=5.0 → interior ceiling Y=3.35) | **1.6500mm** | +0.85mm (106% over) |
| Perimeter side wall (outer edge → pocket wall) | **1.6500mm** | +0.85mm (106% over) |
| Boss/collar radial wall (around shank bore) | **2.1188mm** | +1.3188mm (165% over) |

No wall anywhere in the enumerated geometry falls below 1.65mm. All measured
walls clear the nozzle minimum with substantial margin.

## 5. Structural risk points

- **Boss/collar floor is an unsupported "hanging" feature.** The flat annulus
  at Y=3.10mm (9mm OD / 4.76mm ID ring) connects to the rest of the solid
  *only from above*, via the 0.25mm-tall collar wall up to the skin ceiling
  at Y=3.35mm. Below it (Y=0→3.10mm) is fully open per §3 — meaning in the
  documented print orientation (5mm/Y axis vertical, back face down), this
  ring is the first material deposited at that layer with open air
  underneath: a small unsupported bridge/island (~9mm OD, ~2.1mm-wide ring
  band) inside the hollow cavity. This is a real geometric characteristic,
  not a defect — the diameter is small enough that PETG/PLA should bridge it
  without issue — but it is worth a slicer bridging-setting check and a
  visual check of the first layer of this feature on a test print, since it
  is fragile-by-shape even though it meets nozzle-width minimums.
- No other fragile features found. Toggle-opening corners (r=1.59mm) sit
  ~14mm clear of the nearest screw hole; outer edge fillets don't create any
  adjacent thinning.

## 6. Fit / clearance against real hardware

Measured relief-pocket footprint (at the ceiling boundary, Y=3.35mm, which
defines the usable open cavity): **85.6000mm (X) × 136.4000mm (Z)**, relief
depth **3.35mm** (back face Y=0 → ceiling Y=3.35).

**Spec deviation found:** `specs.md` §5 states rim inset ≈4mm and pocket
footprint 80.9×131.7mm. The actual built geometry uses a **1.65mm** rim
inset (same as the general shell wall thickness measured in §4), giving a
pocket **85.6×136.4mm** — larger than the spec describes on both axes. This
should be treated as a spec inaccuracy to correct, not a build defect: the
deviation is in the favorable direction (more clearance, not less).

Clearance against real hardware (switch yoke 1.75"×2.938" = 44.45×74.625mm,
centered on the toggle opening):

| Axis | Yoke half-extent | Pocket half-extent | Margin per side |
|---|---|---|---|
| X (width) | 22.225mm | 42.800mm | **20.575mm** |
| Z (height) | 37.3125mm | 68.200mm | **30.8875mm** |

Mounting-screw spacing (60.325mm, Z=±30.1625mm) falls within the yoke's
Z-extent (±37.3125mm), as expected for real hardware — the plate screws land
near the yoke's ends, outside the yoke body itself. The boss collars
protrude only 0.25mm deeper than the general ceiling, in a small 9mm-diameter
zone right at each screw location — negligible, no encroachment on yoke
clearance.

**Fit check passes with large margin** (>20mm clearance on the tightest
axis) — even before accounting for the pocket being larger than spec assumed.

## 7. Material check

Measured wall thicknesses (1.65mm general skin/side wall, 2.12mm boss/collar
wall) reaffirm the PETG-over-PLA rationale in `specs.md` §6 — these are thin
walls subject to repeated screw-insertion/removal stress, and PETG's ductility
over PLA's brittleness remains the right call. No revision needed; the
thinnest wall found (1.65mm) matches what the existing rationale already
assumed. (Note: the Fusion body `material` property currently reads "Steel" —
this is just Fusion's default placeholder material and is unrelated to the
print-material recommendation, which is a documentation-level decision.)

## 8. Unresolved / ESTIMATED items (flagged, not gaps)

| Item | Value | Status |
|---|---|---|
| Boss/collar diameter | 9.0mm (exact as modeled) | **ESTIMATED** — explicit structural design choice, not a verified real-world hardware spec. No action needed. |
| Tapered-edge fillet radius | 1.5mm (exact as modeled) | **ESTIMATED** — approximation of Body1's edge treatment, not a verified match to Body1's (ambiguous/possibly compound) edge geometry. No action needed. |
| Rim inset / pocket footprint | 1.65mm / 85.6×136.4mm (geometry) vs. ~4mm / 80.9×131.7mm (spec text) | **Spec inaccuracy**, not a model defect — flagged in §6. Recommend updating `specs.md` §5 to match the built geometry. |

Every other dimension checked (shank diameter, countersink top diameter,
screw spacing, toggle opening size + corner radius, overall envelope, general
wall thickness) was measured directly from geometry and found to exactly
match the corresponding "VERIFIED" spec value.
