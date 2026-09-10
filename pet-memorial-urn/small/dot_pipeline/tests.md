# Test Report — Pet Memorial Urn, Small (0–25 lb), First Test Pass

Tester: independent QA pass, cold start. Method: read `specs.md` in full; independently
re-measured all deliverable geometry (STEP, 3MF, STL) with scripted mesh/BREP analysis
(divergence-theorem volume, horizontal-plane slicing at the spec's own control-point heights,
edge-manifold checks) rather than trusting the Coder's self-reported numbers. Live Fusion
document (`pet-memorial-urn-small`) was inspected to the extent the available read-only tool
permits — see §6, which documents a real tool limitation, not a clean bill of health.

---

## 0. BLOCKING — unresolved ESTIMATED dimension mating with real hardware

**Neck/collar ID = 70mm is tagged `ESTIMATED` in specs.md §6, and it mates with a real external
object the team does not have in hand (a crematorium remains bag for a 0–25 lb pet).** This is
exactly the class of item the QA process requires be resolved or explicitly risk-accepted before
it's treated as done, not silently passed because the CAD checks out.

- The spec's own research is real and cited (UK retailer tier boundaries, two sourced small-tier
  opening figures of 63.5mm/66.7mm, explicit industry commentary that 60–67mm is a documented
  bag-fit pain point at this weight bracket) — this is not a bare guess, and 70mm is a reasoned
  margin above the flagged-problematic range. But it is still a compromise number, not a
  measurement against a real bag.
- The spec names the `neck-fit-test-small` article (§3, §6.5) as the mechanism to close this out
  physically, and states plainly it is "the single most load-bearing open item in this spec."
- I found no evidence in this project's files that a physical print-and-fit-check against a real
  or mocked small-pet remains bag has happened yet, and no written risk acceptance from the
  requester overriding that gate.

**Verdict on this item: UNRESOLVED. Do not commit the full body to final-material printing until
either (a) `neck-fit-test-small` is printed and physically checked against a real/mocked small-pet
remains bag, or (b) the requester explicitly accepts the risk in writing.** Everything below is a
CAD-correctness and manufacturability pass — it confirms the design was *built* to spec, not that
the spec's own headline estimate is *correct*. A finding of "CAD matches spec exactly" for a wrong
neck size is still a wrong neck size.

Secondary, lower-stakes `ESTIMATED` items also named in specs.md §14 (plug clearance 0.5mm, wall/
floor/collar convention thicknesses) do not mate with external hardware and are not blocking in
the same sense, but are still unverified against a real print — the spec's own recommended
clearance-test coupon has not been run either, per the same absence of evidence.

---

## 1. Body — manifold solid, cavity volume, wall thickness, overhang

**Topology.** `urn-body-small.step`: exactly 1 `PRODUCT_DEFINITION`, 1 `MANIFOLD_SOLID_BREP`
(named `urn-body-solid`), 1 `CLOSED_SHELL`. `urn-body-small.stl` (74,462 triangles): 0 non-manifold
edges out of 111,693 (every edge shared by exactly 2 triangles) — fully closed and watertight.
`urn-body-small.3mf`: 1 `<object>` (`urn-body-solid`), 1 build `<item>`, no transform anomalies.
**PASS — single valid manifold solid, confirmed across all three deliverable formats.**

**Cavity volume — independently measured, not taken from the Coder's report.** I sliced the mesh
at ~750 heights from z=0 to z=75.7 and integrated the internal cross-sectional area (π·r_int²)
via the trapezoidal rule, cross-checked against the exact whole-mesh divergence-theorem volume:

| Quantity | Spec target/hand-calc | Independently measured (this pass) | Delta |
|---|---|---|---|
| Cavity volume | 409.6775 cm³ target / 409.87 cm³ hand-calc | **≈412.2–412.4 cm³** | +0.6% vs target, +0.6% vs hand-calc |
| Tolerance band (±5%) | 389.19–430.16 cm³ | Measured value falls **well inside** the band | — |
| Shell material volume | ≈70.76 cm³ hand-calc | **72.26 cm³** (exact, divergence theorem) / 71.96 cm³ (slice-integration cross-check, 0.4% self-consistent) | +2.1% vs hand-calc |

**PASS.** This is exactly the "Coder must verify real modeled internal volume via CAD
mass-properties" check the spec calls for in §7.5 — done independently here rather than trusted.

**Wall thickness — measured directly at 9 sections, not assumed.** At each height I sliced the
mesh, clustered the resulting radii into inner/outer surfaces, and took the radial difference:

| Z (mm) | Internal r | External r | Wall = ext−int | Spec target | Match |
|---|---|---|---|---|---|
| 3.5 (just above floor) | 42.602 | 45.002 | 2.400mm | 2.4mm nominal | Exact |
| 10.0 | 43.127 | 45.527 | 2.400mm | 2.4mm | Exact |
| 20.0 | 44.931 | 47.330 | 2.400mm | 2.4mm | Exact |
| 30.0 | 46.449 | 48.849 | 2.400mm | 2.4mm | Exact |
| **33.5 (P1, belly)** | **46.600** | **49.000** | 2.400mm | 2.4mm — matches spec table's P1 r-values exactly | Exact |
| **54.3 (P2, shoulder)** | **41.600** | **44.000** | 2.400mm | 2.4mm — matches spec table's P2 r-values exactly | Exact |
| **66.7 (P3, neck-taper-end)** | **35.000** | **37.400** | 2.400mm | 2.4mm — matches spec table's P3 r-values exactly | Exact |
| 75.65 (near rim) | 35.000 | 40.999 | 5.999mm | 6.0mm collar wall | Exact |
| 3.0 → below (floor) | solid, no cavity | 45.0 | Floor thickness **3.0mm exactly** (transition from single-cluster solid to two-cluster hollow lands precisely at z=3.000) | 3.0mm | Exact |

**PASS — every wall/floor measurement matches the spec to within mesh-facet noise (≤0.02mm).**
The P0/P1/P2/P3 control points from specs.md §7.5 were independently re-measured at their exact
stated heights and matched the spec's internal/external radius table **exactly** (to 3–4 decimal
places) — this is a genuinely precise build, not just "close enough."

**Overhang — neck-to-collar blend, independently re-measured, not assumed to equal the estimate.**
specs.md §11.1 computes a closed-form peak angle of 44.5° for this feature and explicitly flags it
as "a reasoned estimate... not a live CAD measurement — flag for Coder/Tester confirmation once the
real geometry is built." I did that confirmation: sliced the mesh every 0.25–0.5mm from z=66.7 to
72.5 and computed local dr/dz slope (finer spacing was dominated by mesh-facet quantization noise;
0.25–1.0mm spacing converged cleanly).

**Measured peak overhang angle: ≈44.8° (converged across 0.25mm/0.5mm/1.0mm sampling), occurring
at z≈69.2–69.7mm — almost exactly the midpoint of the measured 66.7→72.2mm blend span, consistent
with the smoothstep formula's predicted peak-at-midpoint behavior.** This is a 0.3° difference from
the spec's 44.5° closed-form estimate — well within measurement noise, and still just under the
45° support-guideline threshold. **PASS**, confirmed by direct measurement rather than taken on
faith. The flat collar band above it holds constant at r=40.987–41.000mm from z≈72.2 to 75.65,
matching the spec's "remaining 3.5mm... constant 41.0mm" claim exactly.

All other transitions (base→belly growing-radius shallow flare, belly→shoulder and shoulder→neck
shrinking-radius sections) were confirmed monotonic in the expected direction with no unexpected
local reversals — no additional overhang risk found beyond the one already disclosed in the spec.

---

## 2. Lid — solid + void topology, plug dimensions, dome plateau

**Topology — independently confirmed sealed void, not a hole through.** `urn-lid-small.step`
encodes the lid as a single `BREP_WITH_VOIDS` entity named `BrimDomeSolid`: one outer `CLOSED_SHELL`
(8 faces) plus one inner void `CLOSED_SHELL` (3 faces) referenced via an `ORIENTED_CLOSED_SHELL`.
`urn-lid-small.stl` (4,276 triangles): **0 non-manifold edges out of 6,414** — critically, this
means there are no boundary (open) edges anywhere in the mesh, which is what you would see if the
plug void were actually open to the outside. **This directly confirms the void is sealed, not a
hole clean through — PASS**, independently verified, not just re-stated from the Coder's report.

**Plug and lid dimensions — measured by slicing the lid mesh at its own local heights** (z=0 is
the plug tip, the bottom of the printed part in its baked orientation; brim underside sits at
z=6.0; brim top / dome base at z=12.0; dome plateau top at z=35.3):

| Parameter | Spec target | Measured | Match |
|---|---|---|---|
| Plug OD | 69.5mm (r=34.75) | **r=34.75mm constant, z=0–6** | Exact |
| Plug interior ID (void) | 64.7mm (r=32.35) | **r=32.35mm** | Exact |
| Plug total depth | 6.0mm | **6.0mm** (z=0 to 6, confirmed by radius jump to brim OD exactly at z=6.000) | Exact |
| Solid tip cap | 2.5mm | **≈2.5mm** (void first appears between z=2.45 and 2.50) | Exact |
| Hollow section | 3.5mm | **≈3.5mm** (remainder of the 6.0mm depth) | Exact |
| Brim OD | 81.7mm (r=40.85) | **r=40.85mm constant, z=6–12** | Exact |
| Brim thickness | 6.0mm | **6.0mm** (z=6 to 12) | Exact |
| Dome base OD | 65.4mm (r=32.7) | **r=32.6999mm at z=12.0** | Exact |
| Dome height (brim top to plateau) | ≈23.3mm | **23.3mm** (z=12 to 35.3) | Exact |
| Total bounding-box height | ≈35.3mm | **35.29999924mm (bbox)** | Exact |
| **Dome apex plateau diameter** | **≈17.8mm (r=8.9mm)** | **16.82mm (r=8.4103mm, measured directly from the flat top-face vertices)** | **−5.5% vs spec target — see finding below** |

**Finding — minor, non-blocking, flagged for consistency.** The built plateau (16.82mm diameter)
is about 5.5% smaller than the spec's derived target (≈17.8mm). It is still comfortably above any
print-quality-limiting size (16.82mm ÷ 0.8mm floor = 21×, vs. the spec's own claimed >20× — the
built part still clears that bar, just with less margin than the spec assumed). This is not a
print defect and needs no rework, but it's worth naming rather than silently accepting: the
as-built dome-blend geometry (likely a slightly different fillet/blend radius than the ~1.2mm the
spec's closed-form estimate assumed) produced a smaller flat spot than derived. If a future
revision needs the plateau to hit closer to the specified ratio, this is where to look.

---

## 3. Plug/body clearance fit — both mating diameters measured directly, independent of the Coder's stated number

Per the task's explicit instruction not to trust the Coder's stated clearance figure, I measured
both mating surfaces from their own independent mesh files:

- **Neck ID (body), measured:** r=35.000mm (70.000mm ID), constant through the collar bore
  (z=66.7 to 75.7 on the body) — confirmed at 5 different heights in that span, all landing at
  34.98–35.00mm (facet noise only).
- **Plug OD (lid), measured:** r=34.750mm (69.500mm OD), constant through the plug's full 6.0mm
  depth.
- **Diametral clearance = 70.000 − 69.500 = 0.500mm (0.25mm per side).** Matches the spec's stated
  0.5mm exactly — **independently confirmed, not assumed.**

**Collision margin above the internal taper — computed from real measured geometry, not asserted.**
The body's constant-ID bore zone runs from z=66.7 (P3, internal taper ends) to z=75.7 (P4, rim).
If the lid seats with its brim underside flush against the body's collar top (z=75.7, the flush-fit
identity confirmed by brim OD 81.7mm sitting exactly 0.3mm inside collar OD 82.0mm — both measured
exactly as specified), the 6.0mm-deep plug occupies z=75.7 down to z=69.7. That leaves **69.7 −
66.7 = 3.0mm of real, measured margin** above the taper before any collision risk — this matches
the spec's claimed 3.0mm margin exactly, and it was derived here from independently measured plug
depth and independently measured taper location, not copied from the spec. **PASS — confirmed
collision-free with real margin on all sides**, not just the primary bore diameter.

---

## 4. `neck-fit-test-small` — dimensions match the body's own neck/collar

Bounding box (measured from STL): 99.98mm × 99.99mm × 26.40mm. Topology: 1 `MANIFOLD_SOLID_BREP`,
0 non-manifold edges out of 13,422 — single valid solid, watertight. **PASS.**

Sliced profile, compared directly against the body's own measured profile (§1 above), not against
the spec text alone:

| Feature | Body (measured, §1) | `neck-fit-test-small` (measured) | Match |
|---|---|---|---|
| Collar/neck ID | 35.0mm r (70mm) | 35.0mm r (70mm), constant z=17.4–26.3 | Exact |
| Neck OD at taper-end | 37.4mm r (74.8mm) | 37.4mm r at z=17.4 | Exact |
| Collar OD at rim | 41.0mm r (82mm) | 40.999mm r at z=24–26.3 | Exact |
| Shoulder-to-neck-taper height | 12.4mm (P2→P3) | 12.4mm (z=5.0 to 17.4, matching the body's own P2 external r=44.0 and P3 external r=37.4 exactly) | Exact |
| Flange | ≈100mm OD × 5mm tall | **99.98mm OD, 5.0mm tall exactly** (transition at z=5.000) | Exact |
| Total article height | ≈26.4mm | **26.40mm (bbox)** | Exact |

This is a genuine part-to-part cross-check (not just "does it match the spec text") — the
fit-test article's neck/collar geometry is dimensionally identical to the full body's own
neck/collar, confirming it is a faithful, purpose-built proxy for the real fit question rather
than a mismatched or reused geometry from a different size. **PASS on construction fidelity** —
does not by itself resolve §0's physical-bag-fit question, which is the point of printing it.

---

## 5. Document contamination check — partial, with an explicit tool limitation

**What I could confirm:** `document search` on the live Fusion session lists three distinct
documents — `pet-memorial-urn-small`, `pet-memorial-urn` (Large), and `pet-memorial-urn-medium` —
confirming Small's document was not merged with or renamed into either sibling document. Across
all three exported deliverable formats (STEP, 3MF, STL) for all three parts:

- Each STEP file contains **exactly one** `PRODUCT_DEFINITION` and **exactly one** solid
  (`urn-body-solid`, `BrimDomeSolid`, `neck-fit-test-small-solid` respectively) — no orphaned
  second bodies, no stray components.
- Each 3MF contains **exactly one** `<object>` and **one** build `<item>`, correctly named, no
  unexpected `<component>` references or odd transforms.
- Every dimension measured across all three parts matches the **Small** spec's numbers exactly —
  none of Medium's or Large's numbers appear anywhere (e.g., no 80mm/100mm-ish neck IDs, no
  Large-scale wall thicknesses).

This is strong evidence the *exported deliverables* are clean.

**What I could not confirm, and why — a genuine tool limitation, not a clean bill of health.** The
task asked me to check the live Fusion document's browser tree directly for stray sketches/bodies
beyond the expected three. The read-only Fusion tool available to me in this session only exposes
`document` (search/open/recent), `projects`, `licensing`, `apiDocumentation`, and `screenshot`
(of whatever document is currently active in the Fusion UI) — there is no query to list bodies,
components, or sketches inside a specific *non-active* document, and I have no write/activate
permission to bring `pet-memorial-urn-small` to the front. When I called `screenshot`, the active
document was an unrelated `Untitled` document, not `pet-memorial-urn-small` — so I could not visually
inspect the target document's browser tree at all.

**Net finding: the exported deliverables show no contamination. The live document's internal
browser tree (timeline, sketches, any hidden/suppressed bodies not included in the export) was
not independently inspectable with the tools available to me this session, and should still be
opened and checked visually by someone with UI or write access before treating the Coder's own
audit as fully closed out.**

---

## 6. Print orientation and support implications

**Body — base down, confirmed baked into the export.** STL/3MF bounding box z runs 0 → 75.7mm with
the flat 90mm-OD base at z=0 (measured r≈44.997–45.00, essentially flat) — matches spec §11.1.
Only real overhang is the neck-to-collar blend, independently re-measured at ≈44.8° peak (§1) —
low risk, matches spec's own "watch it on the first print" framing. No supports needed anywhere
else — confirmed by direct radius-monotonicity checks (§1), not assumed.

**Lid — plug-tip-down, confirmed baked into the export.** STL/3MF bounding box z runs 0 (plug tip)
→ 35.3mm (dome plateau) — the plug tip is the lowest point, meaning it is bed-supported as the
first printed layers exactly as specs.md §9.3 requires. The dome's radius shrinks monotonically
from base (32.7mm) to plateau (8.41mm measured) — self-supporting, no overhang. **The one real
bridging feature is the brim-underside "ceiling bridge" from the plug OD (34.75mm r) out to the
brim OD (40.85mm r) — a 6.10mm radial / ~12.2mm-diameter unsupported span, printed as a full
circular bridge** (not a straight span), which prints more reliably than an equivalent straight
bridge of the same length. This is disclosed in the spec as an accepted, sealed, never-visible risk
using the same mechanism Large used — confirmed present as described, not a new problem.
**Action required before slicing: confirm supports are set to "touching build plate only"** per
spec §9.3 — a permissive support setting would try to generate unremovable interior support inside
the sealed void, which cannot be extracted after printing. I could not confirm this setting was
actually applied (no slicer project file was found in the deliverables, and headless CLI slicing
with the locally installed Bambu Studio did not produce usable output in this session — see below)
— **this is a manual pre-flight check the person slicing the file must still perform.**

**`neck-fit-test-small` — flange down, confirmed baked into the export.** Bounding box z=0
(flange, annular contact patch r=41.6–50.0mm) → 26.4mm (collar rim) — matches spec.

**Slicer check — attempted, inconclusive.** Bambu Studio is installed locally
(`C:\Program Files\Bambu Studio\bambu-studio.exe`), but it is a GUI-oriented application; CLI
invocation in this sandboxed session did not produce usable slice output or help text in the time
available, and I terminated the resulting background GUI process rather than leave it running
unattended. In place of a slicer's support/adhesion report, I substituted direct geometric
overhang measurement (§1, §6 above), which is more precise than a slicer's default angle-threshold
heuristic and covers the same ground (support need, bed-adhesion footprint). **If exact
slicer-generated support maps are required as a deliverable, that step still needs to be run by
someone with a working GUI session.**

---

## 7. Drop test (simulated accidental knock)

No physical print exists yet to drop-test. Based on measured wall geometry and material choice:

- **Body: 2.4mm nominal PLA wall, thinner in absolute terms than Large's 4mm wall, holding an
  emotionally significant payload (cremated remains).** PLA is well documented as having low
  impact toughness / elongation-at-break compared to PETG or ABS — it tends to crack rather than
  flex under a sudden impact load, and this risk is not meaningfully reduced by matte/silk PLA
  variants (same base polymer behavior). The highest-risk zones for a drop-induced crack are the
  curvature transitions identified in the spec itself (belly plateau, shoulder) — exactly where
  stress concentrates on impact, and exactly the zones specs.md §13 edge case 3 already flags as
  more warp/defect-prone at this thinner wall and smaller scale.
- **This is a real, not hypothetical, risk given the object's purpose.** A cracked structural part
  in a typical print is an inconvenience; a cracked memorial urn that spills its contents on a
  hard-floor drop is a materially worse failure mode for the customer than for most other 3D
  prints this team produces. **Recommendation: print the body in PETG, not PLA, or at minimum
  flag this trade-off explicitly to the requester and get a decision, rather than leaving PLA as
  an unexamined carried-forward default.** The spec (§10) already uses PETG for the lid "for
  general toughness" — the same reasoning applies at least as strongly to the body, which is the
  part actually holding the remains.
- **Lid: PETG, solid brim+dome construction.** No thin-wall drop risk beyond the already-disclosed
  plug wall (2.4mm, 3× the print floor) — acceptable in PETG.

**Verdict: cannot be verified without a physical print (no drop test performed on real plastic).
Material choice for the body is flagged as a real risk, not a pass/fail — see Material Check
below.**

## 8. Load test

The design has no handle, lift point, or cantilevered feature carrying concentrated load — per
spec §1 identity, the lid is gripped at the brim/dome edge and the body has no handle. The only
sustained load is the floor supporting the settled weight of a bagged-remains payload (at most a
few hundred grams for a 25 lb pet's actual cremated remains) over years on a shelf. Floor thickness
was independently confirmed at 3.0mm (§1) — 3.75× the 0.8mm print floor, consistent with the
spec's stated ratio. **PASS — no bending/creep expected under the stated (light, static) load
case.** This is not a heavy-load structural part, and I found no reason to expect otherwise.

## 9. Use-case-specific checks

- **Cable management:** not applicable — no electronics/cabling in this design.
- **Humidity/environmental exposure:** spec already names PLA's heat/UV softening risk (§10) as an
  accepted, disclosed trade-off for the matte finish; this pass did not surface any new
  environmental risk beyond what's already named. No condensation/humidity-specific feature exists
  in this design (sealed plug void is a print-process concern, not an environmental one).
- **Fit test beyond the primary opening — plug's own mounting clearance:** the plug carries no
  separate mounting hardware of its own (it is a hollow-then-capped friction-fit boss, not a
  screwed/fastened component), so there is no secondary "mounting screw clearance" class of failure
  applicable here the way there would be for, e.g., an electronics enclosure. The relevant fit
  check (§3 above) — both diameters, real margin above the taper — was performed directly.

---

## 10. Material check

- **Body (PLA, spec default):** Flagged above (§7) — 2.4mm wall, PLA's brittleness under impact,
  emotionally high-stakes payload. **Recommend PETG (or ABS) for the body**, not just the lid,
  given this combination of thin wall + drop risk + contents. If PLA is kept, this should be an
  explicit, informed decision from the requester, not a silent default.
- **Lid (PETG, spec default):** Reasonable as specified — PETG's greater toughness suits the
  thin-fillet transitions (brim-to-dome, dome-to-plateau) and the plug wall, and its better
  bridging behavior helps with the disclosed ceiling-bridge span (§6).
- **Cross-material fit risk (PETG plug into PLA bore):** specs.md §9.1 already names this — PETG
  and PLA shrink differently, and the 0.5mm clearance is unverified against a real print of either
  material. Not independently resolvable without a physical print; recommend the spec's own
  suggested clearance-test coupon actually be run before the full lid is committed to PETG.

---

## Summary of hard numbers (measured this pass)

| Item | Spec value | Measured value | Result |
|---|---|---|---|
| Body cavity volume | 409.6775 cm³ (±5%: 389.19–430.16) | ≈412.2–412.4 cm³ | PASS (+0.6%) |
| Body nominal wall | 2.4mm | 2.400mm (7 sections) | PASS (exact) |
| Body floor thickness | 3.0mm | 3.000mm | PASS (exact) |
| Body collar wall | 6.0mm | 5.999–6.000mm | PASS (exact) |
| Neck-to-collar peak overhang | 44.5° (estimate) | ≈44.8° (measured) | PASS (within noise) |
| Body max OD / height | 98mm / 75.7mm | 97.98mm / 75.70mm | PASS |
| Neck ID / neck OD / collar OD | 70 / 74.8 / 82mm | 70.00 / 74.80 / 82.00mm | PASS (exact) |
| Plug OD / plug ID | 69.5 / 64.7mm | 69.50 / 64.70mm | PASS (exact) |
| Plug/neck clearance | 0.5mm | 0.500mm (measured both sides independently) | PASS (exact) |
| Collision margin above taper | 3.0mm | 3.0mm (derived from measured plug depth + taper location) | PASS (exact) |
| Brim OD / brim thickness | 81.7 / 6.0mm | 81.70 / 6.000mm | PASS (exact) |
| Dome base OD / dome height | 65.4 / ≈23.3mm | 65.40 / 23.30mm | PASS (exact) |
| Dome plateau diameter | ≈17.8mm | 16.82mm | MINOR DEVIATION (−5.5%, non-blocking) |
| `neck-fit-test-small` ID/OD/flange/height | 70/74.8/82mm, ~100mm flange, ~26.4mm | all confirmed exact | PASS |
| Manifold/watertight (all 3 parts) | required | 0 non-manifold edges, all 3 parts | PASS |
| Sealed void (lid) | required, not a through-hole | confirmed via 0 boundary edges | PASS |
| Document contamination (exports) | none expected | none found in STEP/3MF across all 3 parts | PASS |
| Document contamination (live Fusion tree) | none expected | **not independently inspectable this session — tool limitation** | UNVERIFIED |
| Neck ID 70mm (ESTIMATED, mates with real hardware) | must be verified or risk-accepted | **no evidence of physical bag test or written risk acceptance** | **BLOCKING — unresolved** |
