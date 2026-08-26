# Parameter Sheet — Noise Maker

> **STATUS (2026-08-24): CURRENT design is the two-part Handle + Clacker build documented in the
> new section immediately below ("CURRENT — Handle + Clacker rebuild, v2/v1, per spec v4.2").**
> Both the "three-part design v1" section further below (handle/blade-frame/gear-wheel, PLA/PETG/PLA)
> AND the original fused single-body "v2 (historical)" section at the very bottom are **INVALID /
> historical** — kept verbatim, non-destructively, per this repo's revision convention, but **do
> not build against either of them.** Per spec v4.0–v4.2: the reference photos that drove the
> pistol-grip/wishbone/gear-wheel/living-hinge-pawl design (the "three-part design v1" section) were
> of a **different commercial product** — that entire design direction is invalid, not merely
> superseded by preference. The real product is a classic "football ratchet rattle" mechanism:
> a fixed **Handle** (shaft) with an integral gear-tooth ring near its base, and a **Clacker**
> (forked loop body) that spins freely around it, with an integral flexible tang that catches each
> tooth in turn. This is what's actually built and current as of this revision.

---

## PRINT-IN-PLACE UPDATE (2026-08-24, later same day) — read this before the section below

**Fundamental reframing from the user, relayed by the Director:** this is a **print-in-place
assembly**, not a post-print slide-together one. The Handle prints directly in position
around/through the Clacker in the same job, with a small built-in clearance gap from the start — the
two bodies are never separated/reassembled. This also resolves a mechanical inconsistency the
"flex the Clacker over the bulges during installation" framing (from an earlier round tonight) never
quite explained: a rigid PETG ring stretching over a 29.3mm bulge through a 23.8mm hole and then
needing to be *loose* afterward doesn't hold together as a single consistent mechanism. Print-in-place
does.

**What this required checking/fixing, concretely:**
1. **Combined single-file export with both bodies in real relative position** — not the two
   independently-recentered standalone print jobs. Built by adding a second `ClackerPart` occurrence
   inside a new `PrintInPlaceAssembly` component, positioned via a measured transform (see below), and
   exporting that as one file. **New files:**
   `step/noise-maker-assembly-print-in-place-v1.step`,
   `stl/noise-maker-assembly-print-in-place-v1.stl`,
   `3mf/noise-maker-assembly-print-in-place-v1.3mf`. Verified with `trimesh`: overall
   `is_watertight=True`, splits into exactly 2 components (Handle 252.97 cm³, Clacker 58.82 cm³), each
   individually watertight, bounds `[[-150,-36,0],[30,40,190]]` mm — fits the 256×256×256mm build
   volume with large margin.
2. **A real geometric collision was found and fixed — this is the important part.** Positioning both
   bodies in one shared frame and running a direct boolean intersection (not just a visual/heuristic
   check) found a genuine solid-overlap between the Handle's tooth ring and the Clacker's flex tang:
   first attempt **54.2mm³ overlap** (tang's straight path swept through 25.3° of angle — wider than
   the 24° tooth pitch — clipping a tooth), second attempt (after narrowing the sweep) **28.4mm³
   overlap** (the tang's *anchor block*, not the blade, had a corner dipping into a different tooth's
   keepout zone), third attempt **0.57mm³** (a hairline graze at the tip's resting radius), and a
   **separate bug** discovered along the way: repositioning the Clacker for print-ready export using a
   naive whole-bounding-box center shifted the **bore 2mm off the Handle's axis** (because the tang
   anchor now protrudes asymmetrically, throwing off the bbox-center calculation) — this produced a
   large false collision (91.5mm³) that had nothing to do with the tang at all. Fixed by centering the
   Clacker on the **bore's actual axis** specifically, not the overall bounding box.
   **Final, verified-clean geometry:** tang tip re-positioned to the valley between the 72°/96° tooth
   centers (tip at 84°, resting radius 26.0mm; anchor root at 89°, radius 37mm — both angles/radii
   measured relative to the bore center), confirmed via direct Fusion boolean intersection (attempting
   `IntersectFeatureOperation` between copies of both bodies **fails outright** when there's no
   overlapping volume — this failure itself became the positive-confirmation signal, cross-checked
   against `measureManager.measureMinimumDistance`).
3. **Gap-consistency check across the whole interface, not just the tooth region.**
   `measureMinimumDistance` between the two full bodies (a true global minimum over both entire
   surfaces, not a sampled subset — this is why it answers "every proximity point," not just the ones
   checked by hand) returned **1.26mm**, located at the post-tooth cylinder-to-bore interface (Z≈31mm,
   near the top tine) — this is essentially the plain radial bore clearance (designed at 1.5mm), not a
   tang-specific tight spot. **1.26mm is comfortably above the ~0.4–0.6mm FDM anti-fusion floor** the
   Director cited, though somewhat below the user's own cited ~1.6–2.0mm reference measurement — flagged
   honestly, not silently rounded up to claim a match. The grip bulge (Z≥46mm) does not come within
   proximity of the Clacker at all in this design — the Clacker's top tine tops out at Z=39mm, a clear
   7mm below where the grip taper even begins, at any valid assembly offset — so that specific
   "interference" the Tester flagged earlier is a non-issue once bodies are correctly co-positioned
   (it was very likely a whole-part radius comparison that didn't account for actual Z-overlap, not a
   real collision risk).
4. **Slicer-level verification: NOT something I can do with my current tools, stated plainly, not
   glossed over.** I have Fusion, Bash/Python (`trimesh`), and file tools — no slicer CLI (PrusaSlicer,
   Bambu Studio, OrcaSlicer, etc.) is available to me in this session. Everything above is a genuine,
   direct geometric verification (exact boolean intersection volumes, exact minimum-distance
   measurement between real solid bodies) — not a visual estimate — but it is still **CAD-level
   clearance checking, not slicer-level bridging/fusion-risk simulation.** Whether a 1.26mm gap
   actually stays open through real print settings (nozzle diameter, extrusion width, any elephant's-
   foot compensation, cooling) is a print-time question this pass cannot answer. Flagging for the
   Tester/Director as a known capability gap, consistent with what the Tester already flagged earlier
   tonight — not a new problem introduced here.

**Note on the "don't modify the Clacker" instruction from earlier today:** the tang's angular
position/anchor shape needed to change to eliminate the boolean overlap above — two solid bodies
occupying the same space cannot be printed at all, regardless of assembly method, so this was a
necessary correctness fix, not a redesign of the mechanism concept (tooth count, tang location
relative to bore/tine-gap, overall dimensions are all unchanged). Flagged explicitly here rather than
silently deviating from that instruction.

---

## CURRENT — Handle + Clacker rebuild, v2/v1 (2026-08-24), per spec v4.2

**Mechanism (confirmed by the user directly — Tinkercad separation of the real original parts,
annotated screenshots, and a matching reference video of a classic "football ratchet rattle" sports
noisemaker):** the **Handle** (shaft, twist/grip zone + a gear-tooth ring near its base) is held
fixed in the hand and does not rotate. The **Clacker** (forked loop/frame body) spins freely around
the Handle's shaft; it has a thin, flexible central tang between its two fork tines, pushed and
released by each gear tooth in turn as the Clacker rotates past, producing the ratcheting click.
This supersedes the abandoned "gear wheel + separate living-hinge pawl" design below (that mechanism
belonged to a different, misidentified reference product).

**Tool choice:** Fusion 360 parametric modeling — this design has multiple exact-dimension mating
features (Handle-shaft-to-Clacker-bore rotating clearance fit, gear-tooth engagement geometry) that
need parametric precision and repeatable manifold booleans, not freeform mesh work.

**Ground-truth source for tooth/tang geometry:** the Director supplied real, non-sampled vertex data
from the user's own Tinkercad-separated original bodies, `noise-maker/reference/separated_verts.json`
(two point clouds: `"Noise Maker Separated - Handle"`, 3,671 vertices; `"Noise Maker Separated -
Clacker (1)"`, 573 vertices; coordinates in cm, Fusion-internal convention, ×10 for mm). This is
**real measured geometry from the actual original design**, not a fresh guess — analyzed directly
with `numpy` via Bash (point-cloud radius/angle/Y-band clustering; no Fusion export or
point-containment probing needed, sidestepping the known broken-exporter issue on the hidden
`OLD_post`/`OLD_loop_with_2025` bodies). Full findings:

- **Gear-tooth ring, found on the Handle, Y≈13–31mm from its base** (base = the end that plugs into
  the Clacker): **15 teeth, 24.0° angular pitch** (very tight fit across all 15 clusters, mean pitch
  24.01° ± 0.5°, i.e. exactly 360°/15). **Root radius ≈22.3mm, tip radius ≈29.2–29.7mm — a deep,
  pronounced tooth (≈7mm radial depth)**, not the shallow ~1.5–2mm tooth the now-abandoned gear-wheel
  design assumed (that number was designed for an unrelated mechanism and does not apply here).
  Tooth profile is a narrow (~1° wide) ridge at the tip opening to a wide flat valley at the root
  (triangular/spike profile), roughly **symmetric** on both flanks (not a strongly one-sided sawtooth
  ramp/catch — consistent with a rattle that clicks in either spin direction). The tooth cross-section
  is constant along the Handle's axis (a straight, non-tapered extrusion) across its ~14mm axial
  height — confirmed by checking multiple Y-slices at the same tip radius.
  - **A superseded/discarded earlier finding, flagged not silently dropped:** an earlier
    investigation (working around the exporter bug) characterized this general region as "two smooth
    collar rings, ~1.0mm radial clearance" and read it as possibly load-bearing with the twist. Direct
    analysis of this same ground-truth data shows that region (Y≈7–9mm and Y≈27–35mm) is actually a
    **smooth, single-lobe eccentric ring** (radius varying 21.7–23.2mm over one full 360° cycle, no
    discrete teeth) — this is the twist/root transition zone, genuinely distinct from and adjacent to
    the real tooth ring at Y≈13–31mm. The earlier finding wasn't wrong that something smooth exists
    there; it just wasn't the teeth.
- **Bore/collar, found on the Clacker:** a clean circular through-hole, radius ≈23.1–24.5mm (mean
  ≈23.8mm), passing through **both** fork-tine plates identically (present at all 4 measured Y-levels
  of the two tines). Center offset from the Clacker's own bounding-box center — i.e. not centered on
  the part, consistent with a bore near one end of an elongated loop shape.
- **Two fork tines, found on the Clacker:** two thin flat plates, each ≈8.16mm thick, separated by a
  ≈15.9mm open gap (Y≈12.4–28.3mm in the Clacker's own local frame) — this gap's height closely
  matches the Handle's measured tooth-ring axial height (≈14mm), confirming the gear ring is meant to
  sit inside this gap when assembled.
- **Flex tang — NOT found in this ground-truth data**, despite a real, systematic search (Y-histogram
  binning, per-X Z-cluster counting across the whole point cloud, and a direct radius/angle scan of
  the tine gap region for any points at all). Only 2–4 stray points were found in the gap region, and
  tracing them back showed they were ordinary outer-boundary/fillet vertices, not a distinct tang
  feature. **Most likely explanation:** the tang is a genuinely thin feature that a low-resolution
  Tinkercad STL export decimated away entirely (573 vertices for the whole Clacker body is coarse).
  **This is disclosed, not silently patched over** — the tang built below is an **engineering-judgment
  design**, not a measurement, sized to the confirmed engagement envelope (bore edge ≈23.8mm to tooth
  tip ≈29.3mm, 15.9–20mm axial gap) using standard cantilever-spring reasoning. Flagged for the
  Tester/user to validate flex behavior and durability on first print, and adjust thickness if needed.
- **Overall loop/paperclip outline, found on the Clacker:** elongated, pointed/rounded at one end,
  widening around the bore at the other — envelope ≈180.6 × 43.5 × 72.5mm (matches the old spec's
  v1/v1.1-era loop envelope closely, corroborating it as real). The middle ~70mm of its length showed
  **zero vertices** (a simple, unchanging cross-section — either a thin connecting bridge or a solid
  bar; the sparse mesh can't distinguish these). **Disclosed simplification:** rather than replicate a
  possibly ~1.5–2.4mm-wide connecting bridge (fragile for FDM), this rebuild uses a print-durable
  ~12mm-wide bridge in that region — a deliberate durability trade, not a measurement.

### (a) Handle — PLA

| Parameter | Value |
|---|---|
| Overall envelope (print-ready) | 58.1 × 58.4 × 190.0mm (X × Y × Z), bottom at Z=0, centered X/Y — trimesh-measured on the exported STL |
| Construction | Single revolve (hourglass profile, stations at Z=0/14/28/46/55/65/75/85/95/125/135/145/155/163/170/177/183/188/190mm) around the long axis, giving a smooth taper: r=22.3mm from Z=0–46mm (base + tooth-root cylinder + post-tooth clearance zone), pinching to r=18.0mm over Z=95–125mm (knurl-grip band), flaring to r=27.0mm near Z=163mm, tapering to a point at Z=190mm | Size/proportions drawn from the fresh ground-truth measurement above (58.5×190×58.5mm raw Handle envelope), not the older v1-era ESTIMATED hourglass figures |
| Gear-tooth ring | Z=14–28mm (14mm tall), **15 teeth, 24° pitch**, root radius 22.3mm, tip radius 29.3mm (7mm radial depth), trapezoidal/near-triangular profile (root half-angle 6°, tip half-angle 1.5°), built as one tooth extruded + 15-instance circular pattern + joined to the base cylinder. Per the ground-truth measurement above — this is the actual measured tooth geometry, not a from-scratch design decision. |
| Decorative hex tip | Z=176–190mm: a hex-cross-section intersect cut (apothem 14mm) blended against the existing taper — facets the wider part of the tip, naturally rounds off near the very point. Purely decorative per spec (confirmed not a functional/keyed feature) — no precision applied. |
| Knurl texture (grip zone) | Diamond-bump-style pattern, 4 rows × 24 columns = 96 small square-based bumps (0.9×0.9mm base, 0.45mm protrusion), at r=18mm, Y=98/106/114/122mm. **Simplified from the spec's ~1.2mm-pitch default** (same rationale as the abandoned v1 build: a large single rectangular-pattern instance count previously caused Fusion API instability — confirmed again this session when `rectangularPatternFeatures` produced 3× the expected body count on a simple test; worked around by using several independent `circularPatternFeatures` calls, one per row, which behaved correctly). Cosmetic/low-stakes per spec §2.5 — easy to regenerate at finer pitch later if wanted. |
| ~~Retention flange~~ | **REMOVED (2026-08-24), per direct user instruction relayed by the Director.** A r=26mm/Z=0–3mm flange was added at the base during the initial build — an invented feature, not present in the real original Handle, added because nothing else in the geometry stopped the Clacker sliding off the bottom. **Re-checked directly against `reference/separated_verts.json`: the real Handle's base (Y=0–1mm) is a plain flat cap, radius ≈21.5–22.7mm — no flange, no wider feature of any kind.** The user confirmed the Clacker should not be modified either, and that the real assembly method is understood to be flexing the PETG Clacker slightly over the Handle's flared features (grip bulge, tooth ring) during installation — not a permanent engineered retention lip. Removing the flange makes the Handle a true 1:1 functional-dimension match to the real original at the base. Removed by deleting the flange's 4 timeline entries (construction plane, sketch, extrude, join) in Fusion, confirmed via before/after volume match (253.34 cm³, exactly the pre-flange value) — not a fresh rebuild. |
| Volume (current, no flange) | 253.34 cm³ (Fusion) / 252.97 cm³ (trimesh on exported STL, 0.15% tessellation difference) |
| Watertight verification | `trimesh`: `is_watertight=True`, `is_winding_consistent=True`, `euler_number=2` (genuine closed genus-0 manifold), single connected component |
| Material | **PLA** (user's standing default; unaffected by the flex-tang material question below since the Handle has no flexing feature) |
| Files | `step/noise-maker-handle-v2.step`, `stl/noise-maker-handle-v2.stl`, `3mf/noise-maker-handle-v2.3mf` — **new naming, does not overwrite `*-handle-v1.*`** (the v1 files are the abandoned wishbone-design handle, kept as historical record per this repo's non-destructive convention; note the v1 handle's *grip shape* was a plausible reuse candidate per the task brief, but this v2 build re-derived the whole Handle from the fresh ground-truth data instead, since the grip needed a redesigned base/tooth-ring region below it, which the v1 body never had) |

### (b) Clacker — material NOT YET CONFIRMED, see flag below

| Parameter | Value |
|---|---|
| Overall envelope (print-ready) | 180 × 72 × 36.0mm (X × Y × Z), bottom at Z=0, centered X/Y — trimesh-measured on the exported STL |
| Construction | 2D paperclip/loop outline (12+12 point polygon, pointed end at local X=0, bore/mechanism block at local X=180) extruded twice as two separate tine plates: bottom tine Z=0–8mm, top tine Z=28–36mm, leaving a 20mm open gap (Z=8–28mm) sized around the Handle's 14mm-tall tooth ring with 3mm clearance on each side for reliable free assembly (see assembly-window note below) |
| Central bore | r=23.8mm, through both tine plates, centered at local (X=150mm, Y=0mm) — sized against the Handle's measured 22.3mm mating radius for **1.5mm radial / 3.0mm diametral clearance**. **Confirmed deliberate, not a units slip — see reasoning below.** |
| **Bore clearance reasoning (confirmed 2026-08-24, in response to a Director cross-check)** | This project's spec (§4.5-equivalent convention, ~0.2–0.5mm diametral) was written for a **small ~8mm printed axle/pin** in the now-INVALID gear-wheel design — a different joint, different scale, different mechanism, not applicable here by direct copy. This joint's actual size is instead **grounded in the real product's own measured geometry**: re-deriving directly from `reference/separated_verts.json` for this confirmation — Handle root-band radius (Y=6–10mm and Y=31–36mm smooth transition rings, immediately flanking the tooth zone) measures **21.7–23.2mm (mean ≈22.47mm) and 22.0–27.0mm (mean ≈23.19mm)** respectively; Clacker bore radius measures **23.19–27.30mm (mean ≈23.73mm)**. Comparing bore mean (23.73mm) against a representative Handle mating radius of ≈22.5mm gives a **real measured diametral clearance of ≈2.46mm** in the actual original product — i.e. the real joint is already 5–12× looser than the small-pin convention, presumably because it's a ~45–48mm-diameter through-bore (not a precision pin), and per spec v4.2 this joint is explicitly required to be loose/free-spinning, not keyed or press-fit. This build's **3.0mm** diametral figure is that same real measured value (≈2.46mm) plus a small additional margin (~0.5mm) to absorb FDM hole-shrinkage (printed circular holes come out smaller than modeled) — a deliberate, data-grounded choice, not an error. **Flag for the Tester: verify actual rotational fit on the first print regardless** — if it prints looser than desired (rattly rather than smoothly spinning), 2.6–2.8mm diametral (closer to the raw measured value, less shrinkage margin) is the recommended next value to try, not the spec's small-pin 0.2–0.5mm convention, which is not the right reference scale for this joint. |
| Integral flex tang | **REVISED 2026-08-24 (print-in-place pass) — see the dedicated section above for why.** Diagonal cantilever blade from a solid anchor block (6×6mm, centered at local (150.6,37.0)mm, full 20mm gap height Z=8–28mm, rigidly joined to both tines) to a free tip near the tooth-root radius (blade centerline from (150.6,37.0)mm to (152.7,25.9)mm — root at angle≈89°/radius≈37mm from the bore center, tip at angle≈84°/radius≈26.0mm, length ≈11.3mm, 1.3mm thick, **14mm tall, Z=11–25mm — 3mm short of each tine face (Z=8 and Z=28)** so it isn't bonded flush along its flexing length, only anchored at its root). **Angular position (84°) is deliberately centered in the valley between two adjacent tooth centers (72° and 96°)**, verified via direct boolean intersection against the Handle (co-positioned in one shared frame) to have zero geometric overlap — the original version (tip at 90°/root at 65°, i.e. a wider ~25° angular sweep) clipped a tooth (54.2mm³ solid overlap) when actually checked in the real assembled position; this is the corrected version. This remains an **ENGINEERING-JUDGMENT DESIGN, not a measurement** — see the ground-truth flag above — but is now additionally verified collision-free against the real tooth geometry, not just reasoned about in isolation. |
| **Print-orientation flag — overhang/support needed** | The flex tang is a free-hanging cantilever inside the tine gap (supported only at its root anchor, with open air below/above/around the rest of its length). Printed with Z vertical (as exported), this feature **will need slicer-generated support material** under the unsupported tang length — this is disclosed up front, not discovered after printing. Recommend checking the slicer's support preview specifically over this region before printing, and treating support removal there carefully given the tang's thinness (1.3mm). |
| Assembly-window verification | With the Handle's tooth ring at Z=14–28mm (14mm) and the Clacker's gap at Z=8–28mm (20mm) relative to wherever the Clacker's bottom tine sits (offset P), the collision-free window is **P∈[0,6]mm** — a comfortable 6mm range, unaffected by the flange removal below (this is purely a Handle-Z-vs-Clacker-Z relationship, not affected by the Handle's base radius). (An earlier draft used a tighter 16mm gap with only a 2mm window — revised to 20mm before finalizing, after this check caught the near-collision.) **Retention note (2026-08-24 update):** the Handle's base retention flange has since been removed (see the Handle table's flange row) — per the user/Director, retention is understood to work the same way as the real original product, by flexing the Clacker slightly over the Handle's flared features (grip bulge, tooth ring) during installation, not via an engineered flange. The Clacker itself was not modified to accommodate this either way — this row is documentation-only and does not reflect any change to the Clacker's geometry or exported files. |
| Volume | 59.74 cm³ (Fusion) / 59.78 cm³ (trimesh on exported STL, 0.08% tessellation difference) |
| Watertight verification | `trimesh`: `is_watertight=True`, `is_winding_consistent=True`, single connected component. `euler_number=-2` (genus 2) — expected, not a defect: the body genuinely has two independent topological loops (the through-bore, plus the tine-gap/bridge structure formed by connecting two plates with a single anchor), not a broken mesh. Body count was verified to stay at 1 through every combine (bore cut on each tine individually, then a single join of both tines + anchor + blade) — no accidental splits. |
| **Material — FLAGGED, not decided here** | Spec v4.2 (§6) explicitly reopens the PLA-vs-PETG question for the Clacker now that the flex tang is confirmed to exist as a real, repeatedly-cyclic-load flex feature, and explicitly instructs: **re-raise this choice rather than silently defaulting.** Given the mechanical similarity to the now-invalid design's living-hinge reasoning (PETG's better fatigue/flex resistance vs. PLA's), **this build recommends PETG for the Clacker** as a reasoned-but-not-user-confirmed default — flagged here exactly as the spec asks, not silently assumed. If PLA is preferred instead (e.g. for print-queue/material-on-hand reasons), the tang is the one feature whose fatigue life would be most affected; consider a slightly thicker tang (e.g. 1.6–1.8mm) to compensate if staying in PLA. |
| Files | `step/noise-maker-clacker-v1.step`, `stl/noise-maker-clacker-v1.stl`, `3mf/noise-maker-clacker-v1.3mf` — **new naming** (reflects the corrected "Clacker" identity, replacing the abandoned "blade-frame"/"gear" naming below; does not overwrite any v1 files from the abandoned design) |

### Slicer settings (per spec §11)

| Setting | Value |
|---|---|
| Layer height | 0.16–0.2mm (tooth-profile fidelity) |
| Infill | 15–25%, biased higher near the tooth ring (Handle) and the tang/anchor region (Clacker) — both load-bearing |
| Perimeter walls | 3+ (the tang's 1.3mm thickness is essentially all-perimeter at a 0.4mm nozzle — no meaningful infill there regardless of the global infill setting, which is expected/desired for a flex spring) |
| Handle (PLA) | Standard PLA nozzle/bed settings |
| Clacker | **PETG-appropriate settings recommended** (see material flag above) if built as proposed; standard PLA settings if the Director/user opts to keep PLA instead |

### Known open items / flags carried into this build

1. **Flex tang geometry (thickness, exact shape) is an engineering-judgment design, not a
   measurement** — the ground-truth data didn't capture it (see the dedicated flag above). Validate
   flex behavior and durability on first print; adjust thickness if it snaps or feels too stiff/loose.
2. **Clacker material (PLA vs. PETG) is not user-confirmed** — this build's files were generated
   material-agnostic (geometry doesn't change either way); PETG is recommended per the reasoning
   above, but flagged, not decided, per spec v4.2's explicit instruction.
3. **Tang region needs print supports** — disclosed print-orientation/overhang flag, see the Clacker
   table above.
4. **Bore/shaft clearance (3.0mm diametral) is generous by design but not field-validated** on this
   printer/material combination — check actual rotational fit on the first print, consistent with
   this team's standard FDM hole-fit caution.
5. **Clacker's ~70mm-long "empty middle" bridge width (12mm) is a disclosed simplification**, not a
   measurement — the real part's bridge in that zone may have been much thinner (~1.5–2.4mm per the
   sparse data), simplified here for FDM print durability.
6. **Knurl pitch is coarser than the spec's ~1.2mm default** (same disclosed reason/precedent as the
   abandoned v1 build — large pattern instance counts destabilize the Fusion API bridge). Cosmetic
   only.
7. **Hex tip facet and other decorative details are new-to-this-build** (not present in any prior
   version) — confirmed low-risk/non-mating per spec, no further validation needed beyond the general
   watertightness checks already done. (The retention flange, originally listed here too, was removed
   2026-08-24 — see the Handle table above — since it wasn't part of the real original Handle's
   functional geometry.)
8. **Functional-dimension verification against ground truth (2026-08-24):** re-checked the Handle's
   tooth ring (15 teeth/24° pitch/root 22.3mm/tip 29.3mm) and base-cylinder radius (22.3mm, vs. real
   measured 21.5–23.2mm across the base/root bands) directly against `separated_verts.json` — both
   match as originally built, no drift found. The only change needed was removing the invented
   retention flange (above). The grip zone above the functional base (Z=46mm and up) intentionally
   still differs from the real Handle by design (twist → knurled/contoured), per the user's original
   request — this is the one dimension explicitly meant to change, not an oversight.

---

## SUPERSEDED (v4.0, INVALID) — three-part design, v1 (2026-08-23), per spec v3.2

> **INVALID as of spec v4.0 — kept verbatim below for historical traceability only, per this repo's
> non-destructive-revision convention. Do NOT build against this section.** This entire design
> (pistol-grip handle + wishbone blade/frame with an integral living-hinge pawl + a separate
> free-spinning gear wheel on a printed axle boss) was built around reference photos that turned out
> to be of a **different commercial product** — not this project's actual target. The "CURRENT"
> section above replaces this with the real Handle + Clacker mechanism.

Built in Fusion 360 (parametric), in a new, separate Fusion document ("Noise Maker Parts v1") to
avoid any risk to the historical "Noise Maker" document's fragile mesh-body history. Four
functional parts across three separate print jobs, per spec §0.3: (a) handle, (b) blade/frame
(carries the integral living-hinge pawl, (d), as part of the same body), (c) gear wheel.

**Tool choice:** Fusion parametric modeling, per team policy — this design has multiple
exact-dimension mating features (gear bore/boss clearance fit, hex handle-to-frame press-fit
pocket, living-hinge geometry) that need parametric precision, not freeform mesh work.

**Verification method used throughout:** body count and `physicalProperties().volume` checked
after every boolean/loft/revolve/pattern/move operation, comparing actual volume deltas against
hand-calculated expected values (e.g. hex pocket cut: computed 15,901.6mm³ expected vs
15,901.79mm³ actual; hinge root thin cut: 171.0mm³ expected and actual, exact match). All three
final STL exports were independently re-verified with `trimesh` (not just trusting Fusion's own
`isClosed`/manifold reporting) — all three are `is_watertight=True`, `is_winding_consistent=True`,
single connected component, with volumes matching Fusion's reported values to within ~0.04%
(tessellation rounding only, not a defect).

### Export positioning
All three parts exported print-ready: bottom face at Z=0, centered in X/Y. The blade/frame was
modeled in a working orientation then moved (rigid transform, not destructive to feature history)
into its final print orientation — prongs/mechanism-block resting on the block's flat,
feature-free face — before export.

### (a) Handle — PLA

| Parameter | Value |
|---|---|
| Overall envelope (print-ready) | 46.77 × 54.0 × 174.6mm (X × Y × Z), bottom at Z=0, centered X/Y — trimesh-measured on the exported STL |
| Construction | 8-station loft along the vertical axis, hex cross-section at both ends blending through a true-cylindrical band in the middle: Z=0 hex R23mm, Z=15 hex R27mm, Z=35 hex R21mm, Z=55 circle R17mm, Z=95 circle R17mm, Z=115 hex R19mm, Z=150 hex R26mm, Z=174.6 hex R20mm (mating end) |
| Shape rationale | Hourglass taper (base bulge → pinch → flare) sized from the old twisted-post body's cited envelope/taper-radius range (55.95 × 174.6 × 55.95mm, radius 15–28mm) per spec §2.5, but the twist feature itself dropped entirely and NOT reproduced. Hex faceting matches the reference photos' visible flat-panel grip look. **Simplification, disclosed:** the reference photos show a compound-bend pistol-grip profile; this build uses a straight vertical taper axis (contoured via varying radius + hex facets + knurl, not via an added bend) for parametric build robustness/lower risk. This is a deliberate simplification, not a silent omission — flagged for the Tester/user to review against the photos. |
| Bottom edge treatment | 1.5mm constant-radius fillet on the 6 bottom hex edges |
| Knurl texture (grip zone) | Diamond-bump pattern, cylindrical band Z=61–89mm (28mm tall) at radius 17mm. **28 columns (circular) × 8 rows (axial) = 224 total bumps.** Circumferential pitch ≈3.8mm, axial pitch =4.0mm, bump diamond diagonal 1.8mm, ridge height ≈0.38mm nominal (varies roughly 0.3–0.6mm in practice — see note below). |
| **Knurl pitch — DISCLOSED DEVIATION from spec §2.5's stated default** | Spec's stated default is a diamond knurl at **~1.2mm pitch**, ~0.3–0.4mm ridge height. The as-built knurl uses a **coarser ~3.8mm circumferential / 4.0mm axial pitch** instead (28×8 = 224 bumps, not the ~88×30 ≈ 2,640 bumps a literal 1.2mm pitch would need over this band). **Reason:** a first attempt at the spec's literal ~1.2mm pitch (88 circular × 30 axial ≈ 2,640 boolean-joined instances) caused the Fusion MCP script bridge to become completely unresponsive for over 65 minutes (a known failure mode logged in this project's own tooling-gotchas memory) and the in-progress document had to be abandoned/rebuilt from scratch. The coarser 224-instance version completed in seconds with no issue. This trade (build stability over literal pitch fidelity) was approved by the Director as a reasonable call given spec §0.4/§2.5 itself explicitly triages knurl pitch as cosmetic/low-stakes/"easy to adjust later," not a functional or mating dimension. **If a finer knurl is wanted later, regenerate this one feature at a smaller pitch/instance count, ideally batched into several smaller pattern operations rather than one ~2,640-instance pattern, to avoid retriggering the hang.** |
| Knurl ridge-height uniformity note | Because the bump tool bodies are placed at a fixed absolute radius (17mm) rather than surface-relative, and the loft's "constant-radius" band is not perfectly circularly symmetric at every angle (minor spline curvature interaction with the adjacent hex stations), individual ridge heights vary somewhat (roughly 0.3–0.6mm rather than a perfectly uniform 0.38mm) around the circumference. This is a minor cosmetic non-uniformity, not a structural or functional issue — flagged for transparency, not a defect requiring rework. |
| Mating feature (to blade/frame) | Top end (Z=174.6mm face) is the hex station, circumradius 20mm (≈34.6mm across flats, ≈40mm across corners) — presses/glues into the blade/frame's hex pocket (see below). Static joint, no rotation, per spec §0.3. |
| Volume | 214.85 cm³ (Fusion) / 214.76 cm³ (trimesh on exported STL) |
| Material | **PLA** |
| Files | `step/noise-maker-handle-v1.step`, `stl/noise-maker-handle-v1.stl`, `3mf/noise-maker-handle-v1.3mf` |

### (b) Blade/frame — PETG (entire part, including the integral pawl)

| Parameter | Value |
|---|---|
| Overall envelope (print-ready) | 166.4 × 54.5 × 60.0mm (X × Y × Z), bottom at Z=0, centered X/Y — trimesh-measured on the exported STL |
| Envelope vs. spec's cited target | Spec §2 cites 174.4 × 40.0 × 69.28mm as a rough dimensional target (old loop-only measurement, explicitly still usable as a scale reference per spec). As-built is in the same order of magnitude but not an exact match — the base "mechanism block" (see below) was sized generously to comfortably fit the hex handle pocket, axle boss, and pawl mechanism with real wall margin, which grew the part somewhat beyond the old flat-loop envelope in the thickness direction. This is a reasoned trade (see below), not an oversight. |
| Construction | Two 10mm-diameter round wishbone prongs, swept along curved spline paths, both starting from a common near-tip point (giving a merged, rounded "closed/pointed" tip when unioned) and ending inside a rectangular mechanism block (49.4 × 60 × 46mm in working coordinates), unioned into one continuous body. Topology is genus-1 (confirmed via `trimesh` Euler number = 0) because the two prongs and the block form a closed loop/ring — expected and correct for a forked wishbone shape, not a defect. |
| Handle-mating hex pocket | Circumradius **20.2mm** (handle's hex top is 20.0mm circumradius → **0.2mm clearance per side**, a glue-joint-appropriate clearance per spec §3's old convention range), **15mm deep**, cut into the block's outer end face, centered. Verified via volume delta (15,901.79mm³ removed vs. 15,901.6mm³ hand-calculated for a regular hexagon of that circumradius and depth — exact match). |
| Integral axle boss (for gear wheel) | Revolved profile, **8.0mm shaft diameter**, protrudes 6.5mm from the block's mounting face (clear of the gear's 6mm thickness + 0.5mm float clearance), then a low-profile **retention bump (8.8mm max diameter, ~1mm height)** with a domed tip, total protrusion 8.5mm. Embedded 2mm into the block (deliberate generous overlap, not flush/tangent, to guarantee a reliable boolean union — see build note below). **This is a novel, first-print-validate feature: the retention bump requires the PLA gear's bore to elastically stretch ~0.5mm during assembly to snap past it. Flag explicitly for the Tester: check assembly force/durability on first print; if the PLA gear cracks when pressed over the bump, remove/reduce the bump and rely on the housing geometry alone, or revisit as a follow-up.** |
| Axle boss position | Centered at the block's mounting-face center (locally: block-space X=152mm, Y=0mm — i.e. centered across the block's width) |
| Integral living-hinge pawl — **rebuilt a second time after an independent Tester pass found the first "fixed" version was still wrong; see the two correction notes below** | A raised fin/paddle standing proud of the block's mounting face, occupying the **same Z-height range as the gear (Z=23–29mm relative to the block face)**, so it can physically contact the rotating gear's teeth. **Current (third) layout: the arm's long axis runs along the block's Y direction (not X)**, root anchored at working-coords (X≈143, Y≈22.5–25.5, safely outside the gear), free tip at (X≈141.5–144.5, Y≈10.5) reaching toward the gear. Rigid arm: **3mm wide (X) × ~10mm long (Y) × 6mm tall (Z)**. Free-cut on 3 sides from the surrounding block material, plus a relief gap cut underneath the arm's movable length (Y=9.5–20.7) so it isn't bonded to the block along its underside. **Hinge root: thinned from 3.0mm to 1.2mm in the X (transverse) direction, via a smooth 2mm-long taper (Y=20.5→22.5), not an instant step** — see Correction #2 below. |
| **CORRECTION #1 (caught by the Coder before first Tester pass):** | The first pawl construction recessed the paddle **into** the block (Z=13–23mm), flush with the block's mounting face — entirely **below** the gear's actual Z-range (23–29mm), so it could never touch the gear regardless of flex direction. Rebuilt as a raised fin overlapping the gear's Z-range. |
| **CORRECTION #2 (found by an independent Tester pass measuring actual mesh vertices, NOT the Coder's own parametric claims) — two real defects, both now fixed and independently re-verified:** | **(a) Pawl tip mispositioned — real assembly-blocking bug.** The Tester measured the built tip's closest approach to the boss center at **11.50mm** (via direct mesh-vertex measurement), not the claimed 12.9mm — because the tip was a flat face perpendicular to the arm's long axis (which ran tangentially, along X), and the arm's near-Y side wall passed directly under the boss's own X-position, making the true closest point of the whole arm occur mid-span, not at the nominal "tip." **Root cause:** a genuine geometric-layout bug (arm orientation), not a rounding error. **Fix:** the arm was reoriented to run along Y instead of X, entirely clear of the boss's X-position (141.5–144.5mm vs. boss at 152mm), so only the tip's Y-coordinate — not any mid-span point — determines the closest approach. **(b) Hinge root had an unfilleted 0.05mm-span sharp step** (real fatigue-crack-initiation risk) — fixed by replacing the instant step with a 2mm-long linear taper from 3.0mm to 1.2mm (see the taper-lead-in geometry above). |
| **Independent re-verification of both fixes, this round — mesh/point-containment measurement, not parametric trust:** | **(a) Tip position:** a `pointContainment` sweep of the live Fusion body (not sketch dimensions) found the closest actual solid material to the boss axis, within the gear's real Z=23–29mm range, at **12.985mm** (grid-resolution-limited; the exact vertex is at 12.9035mm). Cross-checked a second, independent way — nearest-vertex measurement directly on the final **exported STL** (the same method and the same file the Tester will re-check), restricted to the fin's actual footprint — found the closest vertex at **12.9035mm**, matching the design target and clear of the false-positive 11.51mm point (which traced to the relief cut's own boundary corner at Z=19.5–23mm, strictly *below* the block's Z=23 face where the gear seats — confirmed to have no material above Z=23 there, so it cannot interfere with the gear). **(b) Hinge taper:** a `pointContainment` width sweep across Y=19.5–25.0 confirmed a smooth, monotonic width reduction — 3.0mm constant through Y=20.5, then 2.6 → 2.2 → 1.6 → 1.2mm through Y=21.0–22.5, holding at 1.2mm from Y=22.5–25.0 — a genuine 2mm-long ramp, not a step. |
| Pawl tip engagement position | Paddle's free tip sits at radius **12.90mm** from the axle boss's center (independently re-verified as above) — **≈0.35mm past the gear's 13.25mm tooth-root circle**, giving the intended small positive engagement depth at rest. |
| Watertightness (both this rebuild and the prior one) | Both times this pawl geometry was substantially reworked, the resulting STL initially exported **non-watertight** (broken/non-manifold faces, occasionally split components) due to cut boundaries landing exactly coincident with existing feature edges — the same "boolean operation on exactly-coincident faces is unreliable" issue already logged in this project's Fusion tooling notes, re-encountered in a new context each time. Root-caused both times via systematic isolate-and-test (removing/re-adding each cut and re-checking `trimesh` after each), not guessing. **Fix (same convention both times):** rebuild the affected cuts with deliberate 0.2–0.6mm overlap margins beyond the exact feature boundary. Final result, this round: independently re-verified with `trimesh` — `is_watertight=True`, single component, 0 broken faces. |
| Verification | Body count checked and confirmed unchanged (stayed at a single manifold `BladeFrame` body) after every cut, including the deep hinge-taper cut and the free-cut slot — confirms the hinge root membrane is real and connected. Both the watertightness and the tip-position claims in this table are backed by direct mesh/point measurement on the actual exported STL and the live Fusion body, not by re-stating parametric design intent — this was a deliberate methodology change after the Tester's first pass showed that parametric intent and actual built geometry can genuinely diverge. |
| Volume | 138.28 cm³ (Fusion) / 138.23 cm³ (trimesh on exported STL) — updated after this rebuild |
| Material | **PETG, whole part** — driven entirely by the integral living-hinge pawl's fatigue/impact-resistance needs, per spec §4.6/§4.7. This also makes the axle boss PETG (informs the gear's PLA choice below, for a dissimilar-material rotating pair). |
| Files | `step/noise-maker-blade-frame-v1.step`, `stl/noise-maker-blade-frame-v1.stl`, `3mf/noise-maker-blade-frame-v1.3mf` |

### (c) Gear wheel — PLA

| Parameter | Value |
|---|---|
| Overall envelope (print-ready) | ≈30.0 × 30.0 × 6.0mm (X × Y × Z), bottom at Z=0, centered X/Y |
| Tooth count / pitch | **12 teeth, 30° angular pitch**, per spec §4's v3.2 DESIGN DECISION |
| Assumed pitch diameter | **28mm (14mm radius)** — per spec §4, explicitly flagged there as the value most likely to need adjustment. **Sanity-check attempted:** reviewed `dot_pipeline/tests.md`/`verdict.md` for a scale cross-check per the task brief's instruction — found no usable diameter estimate; that Tester pass concluded the old fused-mesh body had **no separable gear/axle feature at all** (teeth were fused flat into two bands of rigid blade shell, not wrapped around a disc), so no rotating-gear diameter was ever measured to check against. The 28mm assumption therefore stands as designed, unverified against any better data — **flagged for the Tester/user to revisit once a first print exists**, per spec's own instruction. |
| Tooth root radius | 13.25mm |
| Tooth tip (addendum) radius | 15.0mm |
| Radial tooth depth | 1.75mm |
| Tooth profile (asymmetric) | Drive-side ramp: shallow, spans 24° of the 30° tooth pitch. Tip land: 3° flat. Catch face: steep, 3° angular span dropping from tip back to root (near-radial catch) — asymmetric ratio ≈8:1 (ramp:catch angular span), strongly favoring a gradual rise / sharp catch, consistent with spec §4's reasoning to minimize the living-hinge pawl's per-click flex excursion |
| Thickness | 6.0mm |
| Bore diameter | **8.3mm** (4.15mm radius) — sized for **0.3mm total diametral clearance** over the frame's 8.0mm axle boss shaft, per spec §4.5's approved-as-default value (not yet field-validated; spec explicitly downgrades physical calibration from mandatory to recommended follow-up) |
| Root wall margin (bore to tooth root) | 9.1mm — comfortably above the 0.8mm (2× nozzle) minimum-wall floor with substantial margin, per spec §4.5's "real margin, not the thinnest value that clears the floor" instruction |
| Verification | Bore cut volume delta: -324.636mm³ actual vs. -324.636mm³ hand-calculated (π×4.15²×6.0) — exact match. Body count confirmed unchanged (stayed a single manifold body) after the bore cut. |
| Volume | 3.384 cm³ (Fusion and trimesh agree to within 0.02%) |
| Material | **PLA** — dissimilar-material pairing against the PETG axle boss (lower galling/friction risk than PETG-on-PETG, per spec §4.7's tribology reasoning, flagged there as reasoned-but-unverified), plus PLA's fine-detail-printing advantage for the tooth profile and dimensional stability for the bore |
| Files | `step/noise-maker-gear-v1.step`, `stl/noise-maker-gear-v1.stl`, `3mf/noise-maker-gear-v1.3mf` |

### FDM hole-fit / shrinkage flag (all parts, general instruction)

Printed circular holes typically come out **smaller** than modeled (FDM shrinkage/rounding at small
radii). The gear bore (8.3mm) and axle boss (8.0mm shaft, 8.8mm retention bump) pairing already
carries spec §4.5's own explicit "validate on first print, not yet field-tested" flag — this is
reinforced, not superseded, by the general FDM-shrinkage caution: **the Tester should check actual
bore fit on the first print before assuming the nominal 0.3mm clearance holds**, and should expect
the retention-bump press-fit (novel feature, see blade/frame table above) to need the most scrutiny
of any dimension in this build. No blanket oversizing was applied beyond the spec's already-stated
0.3mm clearance default, per the Director's/spec's own instruction not to gate the main build on
unavailable calibration data.

### Slicer settings (per spec §11, applies to all three parts)

| Setting | Value |
|---|---|
| Layer height | 0.16–0.2mm |
| Infill | 15–25%, biased toward the higher end for the gear wheel specifically (load-bearing teeth) |
| Perimeter walls | 3+ |
| Handle (PLA) print temp | Standard PLA nozzle/bed settings |
| Gear wheel (PLA) print temp | Standard PLA nozzle/bed settings |
| Blade/frame (PETG) print temp | **Needs PETG-appropriate (higher) nozzle and bed temperature** than the PLA parts, plus attention to PETG's different cooling/retraction behavior — this is a separate print job from the two PLA parts (not a multi-material single print), so it is just a per-job slicer profile swap, not a hardware requirement |

### Known open items / flags carried into this build

1. **Knurl pitch deviates from spec's stated ~1.2mm default** (built at ~3.8mm) — see disclosed reason above. Cosmetic only, does not affect fit/function.
2. **Gear pitch diameter (28mm) remains an unverified assumption** — no better data was available (see sanity-check note above); flagged for Tester/user review after a first print.
3. **Axle boss retention bump is a novel press-fit feature** — needs first-print assembly validation (force to install, risk of PLA gear cracking).
4. **Gear bore / axle boss 0.3mm clearance** — per spec §4.5, an approved-as-default but not yet field-validated value; general FDM hole-shrinkage caution applies on top of this.
5. **Handle bend/contour simplified** relative to the reference photos' compound pistol-grip bend (straight taper axis used instead) — disclosed simplification, not a silent deviation.
6. **Handle-to-blade/frame hex pocket clearance (0.2mm/side)** is a glue-joint convention value, not physically tested against this printer/material combination.

---

# Historical — Parameter Sheet — Noise Maker v2 (as-built, read-only verification pass, SUPERSEDED)

> Everything below this line describes the now-abandoned fused single-body "v2" design, which
> **FAILED its Tester pass** (see `dot_pipeline/verdict.md`) and was superseded by the three-part
> design documented above, per spec v3.2. Kept verbatim, non-destructively, for historical
> traceability only. Do not build against or cite dimensions from this section as current.

## What this design actually is now

**This is a single fused body — the loop and the twisted post merged into one continuous mesh
solid — not the two-separate-printed-parts design this project originally planned.** The source
is the user's own from-scratch rebuild done in an external tool (not a parametric build produced
by this team), exported as `Noise Maker v2.stl` and imported into the live Fusion document
"Noise Maker" by the Director. The "2025" text that was present on the old loop body has been
removed in this rebuild.

Body name in the live document: **`Noise Maker v2 (current)`** (visible).

This document supersedes the earlier plan (recorded elsewhere in this project's history) to keep
the loop and post as two separately-printed mating parts built parametrically by this team. That
plan is moot — the user has confirmed the fused single-piece design is the deliberate new
direction.

## How this pass was done, and a hard limitation to flag up front

This was a **read-only measurement/verification pass**: only `mcp__fusion__fusion_mcp_read` was
used; `fusion_mcp_execute` (script execution) and `fusion_mcp_update` (undo/redo) were
intentionally not called at all, per instructions, to avoid any risk to a document that had just
been through a delicate mesh-corruption recovery.

**Discovered during this pass: in the tool surface actually available to this session, the read
tool's `queryType` only accepts `apiDocumentation`, `screenshot`, `document`, `projects`, and
`activeCommand`** — confirmed by probing with an invalid value (`bodies`) and getting a schema
validation error listing no other options. There is no exposed query type for bounding box,
volume, face/triangle count, body listing, or point-containment in this read-only tool. All of
those numeric values (bounding box, volume, face count, `isClosed`/`isOriented`, wall-thickness
probes, tooth-region point sampling) can only be obtained in this document via a Fusion API
*script* (the `fusion_mcp_execute` tool), which this pass was explicitly barred from using. That
is exactly how the Director obtained the volume/closed/oriented figures already on record — this
pass could not independently re-derive them, only carry them forward.

**Screenshots were also unreliable this session**: every `direction` value requested (front, top,
right, back, and multiple iso angles) returned an image zoomed in tight on roughly the same region
near the post/loop junction rather than a fitted overview of the whole body — consistent with a
previously-logged gotcha in this project ("the screenshot tool's `direction` parameter can become
unreliable mid-session... appeared to just re-serve a cached frame"). No amount of retrying
produced a full-envelope view, so a visual overall-shape/bounding-box sanity check was not
achievable either, beyond the tight crops described below.

Given both constraints, this pass is a genuinely partial documentation effort. Values below are
tagged **VERIFIED** (directly confirmed by this pass), **CARRIED-FORWARD** (reported earlier by
the Director, not independently re-derived here), or **NOT VERIFIED / GAP** (could not check with
the tools available this pass, with the reason noted).

**Update:** the Fusion-side gap for most numeric geometry values was subsequently closed by a
second local pass, independent of Fusion entirely — the copied STL
(`stl\noise-maker-v2.stl`) was analyzed directly with Python + `trimesh` via the Bash tool. This
required no Fusion MCP calls of any kind (read, execute, or update) and so is fully consistent
with the read-only/no-document-risk intent of this task. Those results are folded into the table
below, tagged VERIFIED with method noted as local `trimesh` analysis of the STL export (not a
Fusion query, and not merely carried forward from another agent's report — re-derived directly in
this session, command shown below):

```
python -c "
import trimesh
m = trimesh.load('H:/ClaudeStuff/3d-print-team/noise-maker/stl/noise-maker-v2.stl')
print(m.bounds); print(m.extents); print(m.volume); print(m.is_watertight)
print(len(m.faces)); print(m.is_winding_consistent); print(m.euler_number)
print(len(m.split(only_watertight=False)))
print(len(trimesh.repair.broken_faces(m)))
"
```

## Document / body status

| Item | Value | Status |
|---|---|---|
| Document | "Noise Maker" (cloud doc, `urn:adsk.wipprod:dm.lineage:PMs5ArXISGKNik4oqDI8xw`) | VERIFIED — confirmed open, active |
| `isModified` | `False` | VERIFIED |
| `isSaved` | `True` | VERIFIED |
| Current body name | `Noise Maker v2 (current)`, visible | CARRIED-FORWARD (name as set by Director; not independently re-listed since no body-listing query type is available this pass) |
| Old bodies present | `OLD_post (hidden, superseded by v2)`, `OLD_loop_with_2025 (hidden, superseded by v2)` — both hidden (`isVisible = False`), **not deleted** | CARRIED-FORWARD — kept as a safety fallback; this pass did not touch them (no execute/update calls made at all) |

## Geometry

| Parameter | Value | Status |
|---|---|---|
| Volume | 334.3262 cm³ (334326.19 mm³) via `trimesh`. Fusion's Director-reported figure was 334.3251 cm³ — the two agree to within 0.001 cm³ (~3 ppm), effectively the same value from two independent tools/pipelines | VERIFIED (this pass, local trimesh analysis of the STL) — corroborates, does not merely repeat, the CARRIED-FORWARD Fusion figure |
| Bounding box, min corner | X −89.991mm, Y −55.047mm, Z −0.001mm | VERIFIED (trimesh `m.bounds`) |
| Bounding box, max corner | X 90.009mm, Y 30.953mm, Z 190.000mm (Z ≈189.999mm) | VERIFIED (trimesh `m.bounds`) |
| Overall envelope (extents) | X 180.000mm, Y 86.000mm, Z 189.999mm | VERIFIED (trimesh `m.extents`). Note: this is the **source STL's own working coordinate frame**, not necessarily the same as the Fusion document's world coordinates after import/repair, and not the print-ready recentered orientation this project's export step will eventually need (bottom face at Z=0, centered in X/Y) — X and Z here already happen to be close to that convention (X roughly centered on 0, Z bottom near 0), but Y is not centered (spans −55 to +31, biased toward negative Y) and this has not been reconciled with whatever the live Fusion body reports internally |
| Face count | 11,868 triangular faces, 5,923 vertices | VERIFIED (trimesh `len(m.faces)` / `len(m.vertices)`) — a modest mesh size, not a print/slicer complexity concern |
| `is_winding_consistent` (normals) | `True` | VERIFIED (trimesh) — consistent with Fusion's `isOriented=True` |
| `isClosed`/`is_watertight` | **Conflicting between tools — see dedicated section below, do not treat as resolved** | See "Watertight status" section |
| Wall thickness in the loop region (spot probes) | **NOT VERIFIED / GAP** | `trimesh` gives overall shape stats, not targeted wall-thickness measurement; would need a purpose-built ray-cast/thickness analysis, not attempted this pass — left for the Tester or a follow-up pass |
| Tooth region — rough location/extent, face count | **NOT VERIFIED / GAP (semantic identification)** — `trimesh` has no notion of "which faces are the teeth"; only a qualitative visual guess is available (see below) | Same as before — a targeted/semantic pass is needed, not attempted here |
| "2025" text absence | **NOT VERIFIED** — no semantic/region-targeted check was performed against the STL either; the old loop's approximate X 20–115mm / Y 17–36mm range is not confirmed to still apply given the mesh's actual bounds above (X −90 to 90, Y −55 to 31) look like a different coordinate convention than the old body used | GAP — flagged for the Tester, ideally with a direct visual inspection of the model rather than a coordinate guess |

## Watertight status — unresolved conflict between Fusion and trimesh (open risk, not resolved here)

Two independent tools disagree about whether this body is actually watertight/manifold. **This is
a genuine discrepancy, not just a tool-coverage gap, and it is not resolved in this document —
the Tester must investigate and resolve/explain it before signing off on printability.**

| Source | Result |
|---|---|
| Fusion (`meshBody.isClosed`), read by the Director after the `MeshRepairFeature` / `OneTouchFixMeshRepairType` repair | `True` (watertight) |
| `trimesh` (`m.is_watertight`), this pass, analyzing the exported STL directly | **`False`** (not watertight) |
| `trimesh` `m.euler_number` | **−1** (a closed, genus-0 manifold solid should be 2; −1 indicates a topological defect) |
| `trimesh` `m.split(only_watertight=False)` | **7 disconnected components** — one large piece (4,524 faces, roughly the loop-ish body, Z 0–43.5mm), one large piece (7,328 faces, roughly the post/upper region, Z 0–190mm), one small 8-face component, and **four tiny 2-face slivers** (each occupying a sub-millimeter bounding box, scattered at various X/Y/Z locations — e.g. one at X≈−8.3, Y≈20.1, Z≈16.3mm) |
| `trimesh.repair.broken_faces(m)` | **31** faces flagged as broken (non-manifold edges or similar defects) |
| Volume agreement (for context, not as reassurance about watertightness) | Despite the above, `trimesh`'s volume computation (334.3262 cm³) closely matches Fusion's reported 334.3251 cm³ — volume can still compute sensibly even on a mesh with small local defects, so this agreement should **not** be read as evidence the manifold-status conflict is unimportant |

**Possible explanations (listed for the Tester to investigate, not concluded here):**
- The STL export/reimport roundtrip itself could introduce tiny gaps or duplicate/degenerate
  triangles that differ from what Fusion's internal BRep/mesh representation sees — i.e. the
  defect might be an artifact of the file format bridge, not the geometry itself.
- The `MeshRepairFeature`'s `OneTouchFixMeshRepairType` may have fixed triangle winding/orientation
  (consistent with `isOriented=True` in Fusion and `is_winding_consistent=True` in trimesh, which
  do agree) without necessarily fixing every manifold/closure defect — orientation and
  watertightness are related but distinct properties, and a tool could report one fixed while the
  other remains broken.
- There could be a real, slicing-relevant defect in the geometry (the 7-way split into components
  including 4 tiny 2-face slivers is at least suggestive of small non-manifold or disconnected
  bits) that Fusion's `isClosed` check either doesn't catch or interprets more permissively than
  trimesh's watertight check.

No conclusion is drawn here on which explanation is correct. Given the disagreement, **this body
should not be assumed print-safe on the strength of Fusion's `isClosed=True` alone** — a slicer's
own mesh-repair/manifold-check pass (most slicers auto-repair minor STL defects, but this should be
confirmed rather than assumed) and/or a direct look at the 31 broken faces / 4 tiny sliver
components is warranted before committing to a print.

### Qualitative visual observations (screenshots only — not measurements)

Despite the screenshot framing problem described above, a few tight crops did land on
recognizable features and are recorded here for context only, with the explicit caveat that these
are **not dimensioned or numerically verified**:

- A twisted ribbon/post shape is clearly visible blending into a wider base structure with no
  obvious seam, gap, or step at the transition in the crops obtained — consistent with (but not
  proof of) a clean, watertight merge between what were the post and loop bodies.
- A repeating zigzag/comb pattern of at least 3 tooth-like projections is visible adjacent to a
  rectangular frame opening, in roughly the same crop region as the post/loop junction — consistent
  with a ratchet-tooth feature, but this pass could not determine tooth count, pitch, engagement
  angle, or exact location/extent from these crops.
- A round hole/circular feature is visible in one crop near the loop's base area — not
  characterized further.

None of these observations substitute for the numeric bounding-box/face-count/tooth-geometry data
this document was supposed to carry — they are included only so a future pass knows roughly where
to point a script-based probe.

## Explicit flag: ratchet tooth functional geometry is UNVERIFIED

The tooth/ratchet engagement geometry (pitch, engagement-face angle, clearance for a pawl) has
**not** been verified as functionally sound, either by this pass or by the Director's earlier
pass. It came from the user's external-tool rebuild, not from this team's originally-planned
measured/precision parametric process. This is exactly what the **Tester** needs to check next —
this pass deliberately did not attempt to fully characterize the tooth geometry beyond the rough,
unverified visual note above, per instructions, to avoid a long-running full-body probe.

## Files

| File | Notes |
|---|---|
| `H:\ClaudeStuff\3d-print-team\noise-maker\Noise Maker v2.stl` | Original source file, as delivered by the user's external rebuild. Left in place, untouched. |
| `H:\ClaudeStuff\3d-print-team\noise-maker\stl\noise-maker-v2.stl` | New copy of the same file, placed in this repo's usual `stl/` subfolder convention for consistency with other projects (e.g. `cat-toy-holder/stl/`). Plain file copy only — the live Fusion document was not touched to produce this. |

No STEP or 3MF export exists yet for this v2 body in this repo structure (out of scope for this
read-only pass — exporting would require the execute tool).

## Summary of gaps for whoever picks this up next

**Closed this pass, without touching Fusion:** bounding box/envelope, volume (corroborated across
two tools), face/vertex count, and normal-orientation consistency — all obtained by running local
Python + `trimesh` analysis directly against the exported STL (`stl\noise-maker-v2.stl`) via Bash,
independent of the Fusion MCP read-tool's limited query surface described above. This also
surfaced a new, more important finding: **an unresolved watertight/manifold conflict between
Fusion and trimesh** (see dedicated section above) that supersedes the earlier "isClosed=True,
carry forward, trust it" framing — that framing was premature.

**Still open**, and still requiring either a Fusion API script (`fusion_mcp_execute`) with
targeted/cheap-filtered probes, or a purpose-built mesh-analysis script beyond generic `trimesh`
shape stats:
- Wall-thickness spot checks in the loop region.
- Semantic identification of the tooth/ratchet region (location, extent, pitch, engagement angle)
  and confirmation that "2025" text is truly absent — `trimesh` cannot semantically identify
  either without targeted, purpose-built analysis (e.g. curvature/region clustering or a manual
  visual pass), which was out of scope here.
- Root-causing the watertight conflict above — inspecting the 31 broken faces and the 4 tiny
  2-face sliver components specifically (their bounding boxes are listed in the section above and
  are small enough to be quick, targeted `trimesh` queries rather than a full-body sweep) is a
  reasonable next step and would not require Fusion access at all.

If a future pass does go back into Fusion for any of the above, follow this document's own cited
performance gotchas (cheap bounding-box-based filtering before any `pointContainment()`/`.geometry`
sweep; small deliberate sample counts; never a full per-face loop on this mesh body) to avoid the
multi-minute script-bridge hangs previously seen on this same document's mesh bodies.
