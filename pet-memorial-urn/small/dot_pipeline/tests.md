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
| Tolerance band (±5%) | 389.19 cm³ – 430.16 cm³ | Measured value falls **well inside** the band | — |
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

---

# RE-TEST — Small v2 Body-Profile Revision ("thrown-ceramic" rounder body + narrowed base), 2026-09-10/11

**Scope.** specs.md §7.7 (v2, 2026-09-10) rebuilt the body profile **below P3 only** — rounder
belly/shoulder, R5 external + R3 internal foot fillets, base OD narrowed 90→85mm. Lid, plug, and
`neck-fit-test-small` were explicitly out of scope. Per the task, this is an independent cold-start
re-verification against the exported deliverables (STEP entity parsing, 3MF XML, STL mesh analysis)
— none of the Coder's reported numbers (cavity 395.979 cm³, perpendicular wall ~2.07mm, ~24° overhang
peak) were taken on faith; all were independently re-derived from the mesh/BREP geometry below.

**Method note — a real session-hygiene issue, named rather than worked around silently.** Partway
through this pass, a script I had written to the shared scratchpad directory was overwritten on disk
by what was clearly a *different* concurrent agent's analysis script (trimesh-based, hard-coded to
`pet-memorial-urn/medium/...` paths) — visible from a mid-session tool notification and corroborated
by the session's own git-status snapshot showing simultaneous in-progress edits across the Large,
Medium, *and* Small body files this same session. I did not use or trust that clobbered file; I
rewrote my analysis under fresh filenames and re-ran everything from scratch on the Small deliverable
paths only, and re-verified (git status, timestamps, file paths) that every number below traces to
`pet-memorial-urn/small/...` and nothing else. **Flagging for the Director/Coordinator:** the shared
scratchpad is apparently not isolated per concurrent agent thread in this session, which is a real
risk of cross-contamination between simultaneous size-variant passes (Small/Medium/Large all being
touched at once) — worth a process fix independent of this build's own pass/fail result.

## R1. Manifold / topology — all three deliverable formats, independently re-checked

- **STL** (`stl/urn-body-small.stl`, 140,526 triangles, binary, size matches header-declared triangle
  count exactly): vertex-welded topology check gives V=70,265, E=210,789, F=140,526 →
  **V−E+F = 2 exactly**, **0 non-manifold edges, 0 boundary edges, 0 edges shared by >2 faces**.
  Watertight, single closed 2-manifold shell. **PASS.**
- **STEP** (`step/urn-body-small.step`): exactly **1** `PRODUCT_DEFINITION`, **1**
  `MANIFOLD_SOLID_BREP` (`urn-body-solid`), **1** `CLOSED_SHELL`, 409 `ADVANCED_FACE`s (400
  `CONICAL_SURFACE` frusta approximating the revolved spline + 4 `CYLINDRICAL_SURFACE` + 3 `PLANE`
  + **2 `TOROIDAL_SURFACE`**, see R6). Single solid, no orphaned bodies. **PASS.**
- **3MF** (`3mf/urn-body-small.3mf`): exactly **1** `<object>` (`urn-body-solid`), **0**
  `<component>` references, **1** build `<item>` with **no transform** (orientation is baked directly
  into the mesh coordinates — bbox z already runs 0→75.7, confirming print orientation is baked in,
  not left to a transform matrix). Mesh vertex/triangle counts inside the 3MF XML (70,265 / 140,526)
  match the STL exactly. **PASS — single valid manifold solid confirmed across all three formats,
  independently, not re-stated from the Coder's report.**

## R2. Cavity volume — independently measured by two different methods, cross-checked against each other

Two independent numerical methods, not just one, to guard against a single method's blind spots:

1. **Direct slice integration:** sliced the mesh at 0.05mm z-steps from the measured floor-top
   (z=3.000mm exactly, see R8) to the rim (z=75.7mm), took the internal ring radius at each slice,
   integrated `π·r_int(z)²·dz` → **395.93 cm³**.
2. **Cross-check via outer-envelope subtraction:** independently slice-integrated the *external*
   profile's `π·r_ext(z)²` from z=0 to 75.7 → external solid-of-revolution volume = 465.27 cm³;
   independently computed the shell's own material volume via the divergence theorem on the raw
   mesh triangles (watertight, so this is exact for the mesh) = **69.28 cm³**. Cavity = 465.27 −
   69.28 = **395.99 cm³**.

The two methods agree to within 0.06 cm³ (0.015%) of each other — strong internal consistency.

| Quantity | Target / band | Independently measured (this pass) | Coder's reported figure | Result |
|---|---|---|---|---|
| Cavity volume | 409.6775 cm³ target; ±5% band 389.19–430.16 cm³ | **≈395.93–395.99 cm³** (avg ≈395.96) | 395.979 cm³ | **Confirmed — matches the Coder's number to within 0.02 cm³, independently, not just re-stated** |
| Deviation vs target | — | **−3.35%** | −3.34% | Matches |
| Margin above the band's lower edge (389.19 cm³) | — | **≈6.77 cm³ (1.65% of target)** | spec's own hand-calc projected ≈9 cm³ margin | **Real margin is real (in-band) but tighter than the spec's own hand-calc anticipated** — worth noting, not a failure: the hand-calc (398.5 cm³) overestimated the true CAD result by ≈2.5 cm³. No action needed at the current 85mm base OD, but if a future revision narrows the base further, the actual headroom to the floor is ~6.8 cm³, not ~9 cm³. |

**PASS — genuinely in-band, confirmed by independent measurement via two agreeing methods, not
accepted on the Coder's word.**

## R3. Base OD vs. collar OD hierarchy — re-checked, not assumed

- **Base OD, measured directly from the foot's vertical-tangent plateau** (z≈5.0–6.5mm, where the
  R5 external fillet arc has flattened out and the belly rise hasn't started yet): **r = 42.50mm →
  OD = 85.00mm exactly.** Confirmed at 15 samples across z=3.0–7.0, converging on r=42.4961–42.4997.
- **Collar OD, measured directly at the rim band** (z=70–75.6): **r = 41.00mm → OD = 82.00mm
  exactly**, constant across the whole span (5.999–6.000mm collar wall, matches R8).
- **Base (85.00mm) > Collar (82.00mm), margin = 3.00mm exactly.** Matches specs.md §7.7's stated
  "3mm margin, 1.5mm in radius" precisely. **No hierarchy inversion. PASS.**
- (Note: an earlier, wider scan window that included the belly-rise region incorrectly returned
  ~87.3mm as "base OD" — the belly starts rising again almost immediately above the foot's brief
  flat plateau. The correct base OD is the local outer-radius plateau at the foot itself, z≈5–6.5mm,
  which is unambiguous in the data: 42.50–42.50mm across a 1.5mm-tall flat band before the belly
  rise begins. Flagging this here as a reminder that "base OD" must be read at the foot's own
  vertical-tangent point, not just "max radius in the lower third" — an easy measurement trap this
  pass caught and corrected before reporting.)

## R4. Belly max OD — full profile scan for overshoot

Scanned the full mesh (all triangles, `max(hypot(x,y))`) and fine-scanned z=25–45mm at 0.1mm steps:

- **Peak external radius = 48.9999mm → OD = 97.9998mm ≈ 98.000mm**, occurring at z=33.50mm — exactly
  the spec's stated P1 height (z_ext=33.5mm, §7.6/§7.7).
- **Zero samples anywhere in the mesh exceed r=49.0mm (OD 98.0mm). Zero overshoot, confirmed by
  scanning the entire profile, not just the belly region.** **PASS.**
- Not a literal single mathematical point: because P1 has a vertical tangent (dr/dz=0) by design
  (§7.7, "apex stays broad" — the spec explicitly wants a broad low plateau, not a sharp point,
  §1/§7.5), the radius stays within 0.05mm of the 98.0mm peak across z=31.2–35.1mm (a ~3.9mm-tall
  flat zone). This is the designed broad-plateau apex working as intended, not a defect — the "single
  point, zero overshoot" check in the task is about overshoot (zero, confirmed), and the flatness
  near the peak is the spec's own stated design goal, not an accident.

## R5. Shoulder — tangent continuity re-checked directly on the built geometry

Computed the local slope (dr/dz) of the outer profile at 0.5mm steps from z=40 to z=62 (spanning the
belly→shoulder→neck-taper transition):

- Slope increases smoothly and monotonically in magnitude from −0.228 (z=40, 12.9° from vertical) to
  a single smooth maximum of **−0.584 at z=54.1–54.5 (30.3–30.6° from vertical)**, then decreases
  smoothly back to −0.333 at z=62 (18.4° from vertical), continuing to ease toward 0 as it approaches
  P3 (z=66.7).
- **Maximum change in slope between consecutive 0.5mm samples anywhere in z=45–62: 0.0287** — no
  jump, no discontinuity. A second-derivative (curvature) proxy over the same span stays in a small,
  smoothly-varying range (−0.032 to +0.045) with one gentle sign change, consistent with the spec's
  own description ("one gentle distributed inflection, no corner") — not a spike, not a cusp.
- **PASS — tangent-continuous (G1), and by the smoothness of the curvature trace, effectively
  G2-continuous in practice** (no literal G2 zero-crossing claim is being made or required, per the
  task's framing that a single cubic segment can't do a true G2 zero-crossing inflection here — the
  built curve is smooth well beyond the bare G1 requirement).
- The measured local slope at the P2 witness height (z=52, dr/dz=−0.557, ≈29° from vertical) is
  steeper than the spec's stated tangent-at-P2 figure of −0.35 (≈19°, "chord direction"). This is
  expected, not a defect: with vertical tangents pinned at both P1 (z=33.5) and P3 (z=66.7), a smooth
  curve connecting them *must* exceed the P1–P3 chord's average slope somewhere in between (the
  chord slope of −0.349 is the *average*, not the *local* value at any single interior point) — the
  measured smooth single-peaked slope profile is exactly what that geometric constraint predicts, and
  is itself evidence of a well-behaved, non-kinked curve rather than a discrepancy.
- Also checked the P1 apex itself (z≈31–36) for the curvature spike the spec specifically flagged
  as a risk from lengthening the P1 down-handle (§7.7 item 6): the outer radius trace through P1 is a
  smooth rounded maximum (48.966→48.999→48.991→48.954mm at z=33,33.5,34,35) with no visible spike.
  **No shortening of the P1 up-handle was needed — the built curve did not trigger the spec's own
  named contingency.**

## R6. Foot fillets — R5 external / R3 internal, confirmed as real torus faces, independently cross-checked two ways

**From the STEP BREP directly** (ground truth, not inferred from the mesh):
```
#5310=TOROIDAL_SURFACE('',#5735,37.1,3.);   <- internal floor-to-wall fillet
#5311=TOROIDAL_SURFACE('',#5742,37.5,5.);   <- external foot fillet
```
Two `TOROIDAL_SURFACE` entities, major/minor radii **exactly 37.1/3.0mm** and **37.5/5.0mm** — i.e.
**R3 internal and R5 external fillets are real, dedicated torus BREP faces**, not an
approximated/faceted rounding. (The pre-v2 archived body has **zero** `TOROIDAL_SURFACE` entities —
its rounded foot was a spline-approximated curve, not a true fillet — so this is a genuine
construction improvement in v2, not just a relabeling.)

**Independently re-derived from the mesh profile, blind to the STEP values above, then compared:**
- External fillet: outer radius grows from 39.04mm (z=0.25) through 41.49mm (z=2.0), 42.07mm
  (z=3.0), flattening to 42.50mm by z≈5.0. Fitting a circle tangent to the flat underside (z=0) and
  the vertical foot wall (r=42.5) gives a center at (r=37.5, z=5.0), radius 5.0mm. Predicted radius
  at z=1.0: 37.5+√(25−16)=40.5mm vs. measured 40.49mm; at z=2.0: 41.5mm vs. measured 41.49mm; at
  z=3.0: 42.08mm vs. measured 42.07mm. **Matches a true R5 circular arc to ≤0.01mm at every sampled
  height, and matches the STEP's stated major radius (37.5mm) exactly.**
- Internal fillet: inner radius grows from the floor-top value (37.10mm at z=3.0, see R8) to a
  vertical-wall value of 40.10mm by z≈6.0. Fitting a circle tangent to the floor top (z=3.0) and the
  vertical inner wall (r=40.1) gives a center at (r=37.1, z=6.0), radius 3.0mm. Predicted radius at
  z=4.0: 37.1+√(9−4)=39.34mm vs. measured 39.33mm; at z=3.5: 38.76mm vs. measured 38.75mm.
  **Matches a true R3 circular arc to ≤0.01mm, and matches the STEP's stated major radius
  (37.1mm) exactly.**
- Ground-contact ring (flat underside out to the start of the R5 arc): r=37.5mm → **75.0mm diameter
  contact ring**, matching specs.md §7.7's stated ≈75mm exactly.

**PASS — both fillets present as real, correctly-sized torus faces, tangent to their neighboring
flat/vertical faces on both sides, confirmed by two independent methods (STEP entity parsing and
blind mesh-arc-fitting) that agree with each other and with the spec.**

## R7. Overall height

Mesh bounding box: z = **0.0 → 75.7mm exactly** (base flat at z=0.0000, rim at z=75.7000, no
tolerance rounding visible in either STL or 3MF). **PASS — exact match to spec's 75.7mm.**

## R8. Wall thickness — nominal 2.4mm radial through the reshaped span, plus rigorous perpendicular-thickness minimum

**Radial wall**, measured as `outer_r(z) − inner_r(z)` at 0.5mm steps from z=3.5 to z=67:

- **Floor thickness: exactly 3.000mm** — the inner cavity's first cross-section appears precisely at
  z=3.000mm (below that, sections are solid/single-ring). Matches spec exactly.
- **z=3.5–5.5mm (R3 internal fillet zone):** radial "wall" reads inflated (2.44–3.49mm) because the
  fillet pulls the inner radius inboard relative to a simple radial subtraction — this is the
  fillet's geometry, not a wall-thickness measurement, and is not a thin- or thick-wall finding
  either way.
- **z≈6–22mm (belly-rise, P0→P1 span):** radial wall runs from 2.40mm up to a **peak of 2.72mm at
  z≈12.5–13.0mm**, then eases back toward nominal by z≈23–25mm. This is the "note for the record"
  item — confirmed below.
- **z≈22.5–66.5mm (rest of the reshaped span, through the belly plateau, shoulder, and neck taper):
  radial wall holds at 2.398–2.402mm essentially everywhere** — i.e., dead-on the 2.4mm nominal, well
  within mesh-facet noise. **Minimum radial wall found anywhere in z=6–66.7mm: 2.398mm at z=54.5**
  (the shoulder's steepest point) — for all practical purposes exactly 2.4mm, never below it.
- **Collar band (z=70–75.6mm): 5.999–6.000mm** — matches the 6.0mm collar wall exactly.
- **PASS — nominal 2.4mm wall confirmed through the entire reshaped span**, with the one disclosed,
  bounded, safe (thicker, not thinner) exception in the belly-rise zone (see below).

**Perpendicular-thickness minimum on the steepest section — measured two ways, not assumed from the
radial figure:**
1. Simple cosine correction at the steepest point: steepest **inner-wall** slope found at
   z=54.10mm, dr/dz=−0.592 → 30.6° from vertical. Perpendicular ≈ 2.4mm × cos(30.6°) = **2.065mm**.
2. Rigorous method (independent of the cosine approximation): built dense inner and outer polylines
   from the sliced profile and computed, for every point on the outer surface between z=6 and z=67,
   the true minimum Euclidean distance to the inner-surface polyline (not just the same-height
   radial subtraction). This found a **global minimum perpendicular wall of 2.0709mm at z≈54.9mm** —
   consistent with method 1, and pinpointing the same location (the shoulder's steepest point,
   inside the reshaped span).

| Check | Value |
|---|---|
| Coder-reported perpendicular minimum | ~2.07mm |
| Independently measured (cosine method) | 2.065mm |
| Independently measured (rigorous nearest-surface-point method) | 2.0709mm |
| 0.8mm print-floor requirement | 2.07mm ÷ 0.8mm = **2.6× the floor** |

**PASS — matches the Coder's reported figure almost exactly (both independent methods land within
0.01mm of the reported ~2.07mm), confirmed not worse, and well above the 0.8mm floor.** This is the
same accepted cosine consequence of the constant-radial-offset spline-offset method already accepted
on Medium, not a new or worsened condition here.

**Belly-rise inner-wall thickening — the Coder-flagged "note for the record," independently
confirmed:**
- Peak radial wall in the P0→P1 belly-rise span: **2.72mm** at z≈12.5–13.0mm (Coder reported
  ~2.69mm — my independently-measured peak is slightly higher, i.e. **even safer**, not worse).
- **Confirmed thicker, never thinner:** across the entire belly-rise span (z=6–25mm) the radial wall
  never drops below **2.398mm** (essentially nominal) — it only ever exceeds 2.4mm, peaking at
  2.72mm, then re-converges to nominal. **No location anywhere in this span drops below the 2.4mm
  nominal, let alone the 0.8mm floor.** Matches the spec's own description ("z-shifted ~1mm rather
  than a true normal offset... THICKER (safe), localized") exactly. **Confirmed, non-blocking.**

## R9. P3-and-above byte-identical to v1 — cross-checked against the archived pre-v2 body at multiple heights

Sliced **both** the v2 body and the archived pre-v2 body (`archive/pre-v2-rounder-body/stl/urn-body-small.stl`,
confirmed via git-history diff to be an exact, unmodified copy of the last-committed pre-v2 STEP/STL/3MF —
see Method note below) at matching heights from z=66.7 (P3) to z=75.65 (near-rim):

| z (mm) | v2 inner r | v1 (archive) inner r | Δ inner | v2 outer r | v1 (archive) outer r | Δ outer |
|---|---|---|---|---|---|---|
| 66.70 (P3) | 35.0000 | 34.9999 | 0.0000 | 37.3993 | 37.3963 | 0.0029 |
| 68.00 | 34.9980 | 34.9939 | 0.0041 | 37.9146 | 37.9063 | 0.0083 |
| 70.00 | 34.9963 | 34.9886 | 0.0077 | 39.7437 | 39.7407 | 0.0029 |
| 72.00 | 34.9962 | 34.9882 | 0.0080 | 40.9827 | 40.9749 | 0.0079 |
| 74.00 | 34.9976 | 34.9925 | 0.0051 | 40.9961 | 40.9875 | 0.0085 |
| 75.65 (rim) | 34.9999 | 34.9998 | 0.0001 | 40.9998 | 40.9995 | 0.0004 |

**Worst delta anywhere at/above P3: 0.0097mm** — this is mesh-tessellation noise between two STL
exports of different triangle density (v2: 140,526 tris, v1: 74,462 tris), not a real geometry
difference. **PASS — P3, the collar bore (70mm ID), the collar OD (82mm), and the P3→P4 external
blend are confirmed geometrically identical between v2 and v1 to well under 0.01mm, i.e. effectively
byte-identical in the CAD sense the spec claims.**

For contrast, the same comparison **below** P3 (where the reshape is supposed to differ) shows real,
substantial deltas as expected: z=10mm outer Δ=−2.47mm (base narrowing), z=50mm Δ=−1.02mm, z=60mm
Δ=−1.50mm (rounder shoulder pulled inward) — confirming the reshape is real, present, and correctly
**confined to below P3**, not leaking into the collar/neck geometry.

**Method note on the archive's integrity:** `git show HEAD:...urn-body-small.step` and the archived
`archive/pre-v2-rounder-body/step/urn-body-small.step` are byte-identical once the STEP header's
timestamp field is excluded from the diff (`diff` returns clean); the archived STL and 3MF are
byte-identical (matching md5sums) to the last-committed pre-v2 versions. The archive is a faithful,
unmodified reference, not a stand-in that could itself be wrong.

## R10. Print orientation and overhang — re-measured directly, not assumed from the spec's estimates

- **Base-down, Z=0 confirmed baked into both STL and 3MF** (bbox z=0→75.7mm; 3MF build `<item>` has
  no transform — the mesh coordinates are the print orientation).
- **Faired lower body (base→belly, P0→P1):** peak local overhang **23.68° from vertical at
  z=14.80mm** — matches the Coder's reported ~24° almost exactly, independently confirmed. Well
  under the 45° support threshold.
- **R5 foot-fillet underside:** angle from horizontal crosses 45° between z=1.40mm (44.0°) and
  z=1.60mm (47.3°) — i.e., the bottom **~1.5mm** of the fillet arc sits below the 45° guideline,
  matching the task's stated "~1.5mm below 45°" almost exactly. This is routine for any rounded
  base of this radius and is the same disclosed, minor first-print watch item as before — not a
  new or worsened risk from the base-narrowing.
- **Neck-to-collar external blend (P3→P4, unchanged from v1 per R9):** peak **44.41° from vertical
  at z=69.40mm** — consistent with the first test pass's own direct measurement on the v1 body
  (44.8°, on a coarser mesh); both are under 45° and represent the same single disclosed watch zone,
  unaffected by this revision.
- **No new overhang risk anywhere else** — belly→shoulder→neck-taper (P1→P2→P3) remains a
  monotonically shrinking radius throughout (self-supporting by construction regardless of local
  angle), confirmed by the same slope trace used for R5's continuity check.
- **PASS — all overhang figures independently re-measured and confirmed either matching or slightly
  better than the Coder's reported figures; nothing exceeds the 45° guideline.**

## R11. `urn-lid-small.*` and `neck-fit-test-small.*` — confirmed NOT modified

- **`git status --porcelain -- pet-memorial-urn/small/`** shows only `3mf/urn-body-small.3mf`,
  `step/urn-body-small.step`, `stl/urn-body-small.stl`, and `dot_pipeline/specs.md` as modified.
  **No lid or neck-fit-test files appear in the modified set at all.**
- **File timestamps** confirm the same story independently: `urn-lid-small.{step,3mf,stl}` and
  `neck-fit-test-small.{step,3mf,stl}` are all still dated **2026-09-09 15:00** (the v1 build time);
  the three `urn-body-small.*` files are dated **2026-09-10 16:22** (the v2 rebuild).
- **`git log -1` on the lid/neck-fit-test files** shows their last touching commit is `1aeba56`
  (the original Small/Medium size-tier commit) — no commit since then has touched them.
- **PASS — confirmed via two independent signals (git status and filesystem timestamps), not
  assumed from the spec's own claim that the Coder "rebuilds only the body."**

## R12. Standing open risk — restated, not re-litigated

**The 70mm neck/collar ID remains `ESTIMATED` in specs.md §6 and is still untested against a real
small-pet remains bag.** This v2 revision does not touch that geometry at all (confirmed
independently in R9 — P3-and-above, which includes the entire neck/collar, is unchanged to well
under 0.01mm from v1). **This rebuild does not resolve, worsen, or otherwise change that risk** — it
remains this size's single highest-priority open item, still gated behind a physical print-and-fit
check of `neck-fit-test-small` against a real or realistically-mocked small-pet remains bag, exactly
as recorded in the first test pass (§0 above) and specs.md §14 item 1. No new evidence either way was
found this pass.

## Summary of hard numbers — v2 body re-test

| Item | Spec / Coder-reported | Independently measured (this pass) | Result |
|---|---|---|---|
| Manifold/watertight, all 3 formats | required | 0 non-manifold edges (STL); 1 solid/1 shell (STEP); 1 object/0 components (3MF) | PASS |
| Cavity volume | 409.6775 cm³ target, band 389.19–430.16; Coder 395.979 | 395.93–395.99 cm³ (2 methods) | PASS, −3.35% vs target, genuinely in-band |
| Base OD vs collar OD | 85mm > 82mm | 85.00mm > 82.00mm, margin 3.00mm | PASS, no inversion |
| Belly max OD | 98mm, zero overshoot | 97.9998mm peak, 0 samples over 98.0mm anywhere in full-mesh scan | PASS |
| Shoulder continuity | tangent-continuous (G1), no kink | max Δslope 0.0287 over 0.5mm steps; smooth single-peaked curvature | PASS |
| Foot fillets | external R5, internal R3, real torus faces | STEP: TOROIDAL_SURFACE 37.1/3.0 and 37.5/5.0 exactly; mesh arc-fit matches to ≤0.01mm | PASS |
| Overall height | 75.7mm | 75.7000mm exactly | PASS |
| Nominal wall (reshaped span) | 2.4mm | 2.398–2.402mm through z=22.5–66.5; peak 2.72mm (thicker, safe) in belly-rise z=6–22 | PASS |
| Perpendicular wall, steepest section | ~2.07mm (Coder) | 2.065–2.071mm (2 methods), at z≈54.1–54.9 | PASS, matches, 2.6× the 0.8mm floor |
| P3-and-above vs. archived v1 | byte-identical | worst delta 0.0097mm across z=66.7–75.65 | PASS |
| Print orientation / overhang | base-down; ~24° lower body; ~44.5° P3→P4 blend | 23.68° lower body; 44.41° P3→P4 blend; foot-fillet underside crosses 45° at z≈1.5mm | PASS, all under 45° |
| Lid / neck-fit-test untouched | required | git status clean + timestamps unchanged (2026-09-09) vs body's 2026-09-10 rebuild | PASS |
| Neck ID 70mm (standing risk) | must remain flagged | unchanged by this revision (confirmed via R9); still ESTIMATED, still untested | **UNRESOLVED (carried forward, not new)** |
