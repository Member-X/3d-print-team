# Pet Memorial Urn (Large)

**Current design state: v7 (2026-09-02) — lid only.** A two-part memorial urn for pet cremated
remains, sized for the top of a 50–90 lb pet weight range (~90 lb), with an **80mm neck opening**
(widened in v5), a resting-cap lid closure with a capped hollow alignment/friction-fit plug (added
in v6, capped in v7; no magnets/latch hardware), and **no handle of any kind** (removed entirely in
v7 — this is a deliberate, confirmed reversal of the original concept brief's "hard constraint,"
not an oversight — see below). **v7 touches the lid only** — `urn-body` and `neck-fit-test` are
unchanged from v5 (still dated 2026-08-31); see "Design evolution" below for what changed and why,
including the Reviewer's honest concept-fidelity assessment of this round's cumulative effect.

## What it is

- **Body** — a single smooth, rounded "ceramic vase" silhouette (wide low belly, tapering
  through a shoulder into a neck/collar), plain on all sides (no engraving/plaque — a hard
  design constraint), holding **≈1579–1580 cm³ (≈96.3–96.4 in³) internal capacity** — sized
  against the requester's own rule of thumb (1 in³ of internal volume per lb of pet body weight,
  at the top of the stated 50–90 lb range) and comfortably *exceeding* the original ≈1475 cm³
  minimum target by design (see "Design evolution" below and `parameters.md` for the full story).
  The neck/collar opening is **80mm ID** (widened from 58mm in v5, market-research-driven — see
  below); overall height is **153.5mm** (trimmed from 160mm in v5 to hold the cavity volume
  steady despite the wider neck). **Unchanged by v6 or v7** — both rounds touched the lid only.
- **Lid — a plain domed cap, no handle (v7).** Flat brim **99.700mm OD × 10mm thick** (shrunk and
  thickened in v7 — flush with the body's 100mm-OD collar, zero overhang, replacing every prior
  version's overhanging brim) rests directly on the body's flat 100mm-OD collar rim. Above the
  brim, a dome **80mm base OD × 29mm tall** (shrunk from v5/v6's ~97–98mm base, re-derived to match
  the new flush brim) rises to a **flattened plateau, 21.73mm diameter** (replacing every prior
  version's fully-rounded point apex). Hanging from the underside, a hollow cylindrical alignment
  plug (**79.5mm OD, 10mm deep**) reaches down into the body's 80mm neck opening for a secure,
  self-centering friction fit — **now capped at its tip (new in v7): 6mm hollow nearest the brim,
  4mm solid disc nearest the tip**, sealing what was an open-ended tube in v6. **There is no handle
  or grip feature of any kind anywhere on this lid** — see "Handle" below and "Design evolution"
  for why, and for the Reviewer's honest assessment of what removing it does to the design's
  visual identity.
- **Closure — flat seating plus a capped alignment plug (v6, capped in v7); still no magnet/latch
  hardware.** The lid's flat underside rests on the body's flat 100mm-OD collar rim exactly as
  before, and a hollow 79.5mm-OD × 10mm-deep plug hanging from the underside engages the body's
  80mm neck bore for a 0.5mm diametral friction fit — this is an alignment/centering feature, not
  a magnet, latch, or airtight seal (still not needed — the crematorium's remains are already in
  their own sealed bag). An earlier version of this design had 3+3 magnet pockets (6mm × 2mm N42
  discs on a 34mm bolt circle); the user decided to handle any magnet placement themselves at
  print time (slicer pause-and-embed) or after printing (drill-and-glue) instead, so those pockets
  were removed from the CAD (2026-08-28). The pre-removal files are preserved at
  `archive/v2-with-magnet-pockets/` — see `parameters.md` §3/§9 for the full story.
- **Handle — REMOVED ENTIRELY in v7, no replacement grip feature of any kind.** Every version of
  this design through v6 had an open-loop bail handle on top of the dome (24×22mm opening, 9mm
  bail, 40mm tall above the dome apex) — the concept brief that originally launched this project
  called that handle **"the key differentiating feature"** of the entire design and named its
  open-through-hole geometry **"a hard constraint when the Planner moves to CAD."**
  **The requester explicitly and directly confirmed removing it anyway, with no replacement grip
  feature, fully aware this reverses that original hard constraint** — this is a deliberate,
  informed decision, not an oversight or something a future reader would need to reconstruct from
  context. The lid is now a plain dome with a flattened apex plateau; you grip the brim/dome edge
  by hand to lift it, the same way you'd lift any domed lid with no dedicated handle. See "Design
  evolution" (v7) below for the full reasoning and the Reviewer's concept-fidelity assessment of
  this change.

Body and lid are separate printed parts — not printed in place, not glued together. The lid
lifts off by hand — **there is no handle to grip as of v7; see the handling note in "Print
notes" below.**

## Design evolution

### v4 (2026-08-28) — why the capacity grew past the original target

The body was originally derived to hit ≈1475 cm³ (90 lb × 1 in³/lb) and, once built, first
measured out to ≈1512 cm³ (+2.3%, still within the spec's own ±5% routine-tolerance band). Since
then, the user made a direct, deliberate manual edit to the body's outer belly in Fusion to make
it visibly fuller — an aesthetic choice, explicitly kept rather than reverted. That left the
inner wall not tracking the new outer wall (uneven thickness); the user then had the inner wall
reworked to track the fuller outer wall at a constant ~4mm offset, matching the wall-thickness
approach used everywhere else in the body, rather than thinning the wall further just to force
the volume back down. The result — **≈1579 cm³, +6.85% over the original minimum target** — is
the accepted, explicit consequence of that sequence of choices, not a defect. It's also a
*more*, not less, generous capacity for the same 50–90 lb market segment the urn was always sized
for.

### v5 (2026-08-31) — neck/collar widened, height trimmed, lid resized

Competitor-benchmarking market research found the pre-v5 **58mm neck opening a significant
outlier** against comparable pet urns (114–121mm top openings) and even a direct 3D-printed
competitor (~70–100mm estimated opening) — this had been flagged as an untested `ESTIMATED`
assumption since the very first version of this spec and was never closed out until this research
gave a concrete outside reason to revisit it.

The requester chose **80mm** as the new neck ID — a deliberate compromise short of the full 100mm
initially considered, specifically to keep the collar OD (100mm) from exceeding the body's own
98mm base OD (which would have inverted the vessel's visual hierarchy, making the opening wider
than the base). 80mm sits at the **low end** of the cited 3D-printed-competitor range (70–100mm),
meaningfully reducing — though not eliminating — the risk that a real crematorium remains bag
won't pass through comfortably.

Widening the neck/collar unavoidably adds internal volume near the top of the body. Rather than
letting the ≈1579 cm³ target established in v4 grow further, this was compensated by **trimming
6.5mm out of the belly-to-shoulder segment specifically** (160mm → 153.5mm total height) — the
belly itself (76.966mm/72.966mm external/internal radius) is completely unchanged in absolute mm;
only the segment below it got shorter, keeping the cavity volume essentially flat at the same
≈1579–1580 cm³ target rather than growing it. The collar's 10mm reinforcement wall was explicitly
**kept** (not reverted to the nominal 4mm) even though it lost its magnet-housing purpose back in
v3 — it now serves purely as structural margin and rim character at the new, larger size.

The **lid** was resized to match (at the time): brim 100mm → 122mm OD (preserving the original
11mm/side overhang margin over the now-wider collar), dome base ~80mm → ~97–98mm OD (preserving
the original 0.80 dome-to-brim ratio). This was done via a non-uniform scale (X=Y=1.22, Z=1.0)
applied *before* the handle/plinth features were modeled — the handle's 24×22mm opening, 9mm
bail, and 40mm height were all independently confirmed unchanged at the time. **The 122mm
brim/~97–98mm dome figures described in this subsection were superseded by v7 (below) — the
current brim/dome are 99.700mm/80mm.**

**Honest visual note, updated for v5:** the v4 belly-fullness edit had made the design read more
pinched/"ginger jar"-like against the original concept photo (`concept/concept-v2.png`) than the
earlier build did. **v5's wider neck is a genuine, if partial, correction of that drift, not an
additional one** — independently measured, the collar-OD-to-belly-OD ratio moves from ~51%
(pre-v5) to ~65% (v5), which is closer to the concept image's own visibly wider-mouthed
proportions. The shoulder-to-neck-taper transition also now reads visibly smoother in the current
render. The already-disclosed "banded collar" drift (the collar's flat, constant-radius band vs.
the concept's fully continuous neck curve, needed as a robust lid-seating surface) is unchanged in
kind — just larger in absolute terms now — and was already an accepted tradeoff before this
revision. **At the time of this v5 pass**, both features the concept calls load-bearing to the
design's identity — the plain body and the open-loop handle — remained fully intact; **the handle
has since been removed in v7 (below)**, which materially changes the concept-fidelity picture — see
the v7 section for the Reviewer's updated, cumulative assessment.

Full numbers and independent three-way verification for both rounds: `parameters.md` §1, §2,
§10, §11.

### v6 (2026-09-01) — lid-underside alignment plug added (lid only; body/neck-fit-test unchanged)

**What changed:** the lid gained a **hollow cylindrical alignment/friction-fit plug** hanging
10mm down from its flat underside — **79.5mm OD, 35.75mm ID (4.0mm wall), 10mm deep** — that
engages the body's 80mm-ID neck bore for a **0.5mm diametral clearance friction fit**. This
supersedes the v5 flat-on-flat-only seating interface described above; the flat brim-on-collar
seat itself is unchanged, the plug is purely additive below it. Nothing about the neck, collar,
belly, height, handle, or body cavity volume is touched — this is a lid-underside-only addition
(confirmed by Coder, Tester, and Reviewer independently; see `parameters.md` §12). **The plug's
tip was open at this stage — it was capped in v7, below.**

**Why:** the v5 flat-on-flat seat (above) had no built-in alignment or secure engagement — the
lid simply rests on the collar by gravity, centered "by eye/feel." The plug gives the lid a real,
snug, self-centering engagement into the neck opening once the user has decided print supports
are an acceptable tradeoff for that improvement (they weren't, when this exact idea was first
considered and rejected during the original v1 seating-interface design — see
`dot_pipeline/specs.md` §5.2/§5.2.1 for that history).

**A tapered stopper/bung shape (wide at the plug's top, narrowing toward the tip, "cork in a
bottleneck") was seriously considered and rejected in favor of this simpler straight-walled
design.** The tapered version would have added genuine self-centering/progressive-friction feel,
but a genuinely stopper-shaped taper requires an angle (~63° from vertical) well past the ~45°
self-supporting guideline — meaning it needs *more* total print support than the straight plug,
not less, despite looking like the "simpler" shape. The straight-walled plug's own wall is a true
vertical cylinder (0° from vertical, zero overhang along its full depth), which is why it was
chosen instead. Full numbers for both options: `dot_pipeline/specs.md` §5.2.1.

**Print/support implications, as they stood at v6 (see the v7 section below for what changed
when the tip was capped):**

- **Outer support annulus, on the visible decorative overhang ring — an accepted, deliberate
  tradeoff, not an oversight.** The plug creates a sharp radial step up to the (then-122mm) brim.
  Support material is required under that whole annulus, and part of it is visible once the urn is
  assembled — support-removal witness marks may show there. The user weighed this against the
  alternative and chose to accept it for the alignment benefit.
- **A 71.5mm internal bridge inside the lid — expect a real sag/stringing event, and know why it
  doesn't matter.** The plug's hollow interior (at v6, the full 10mm depth was hollow) was capped
  by the underside of the solid brim disc, creating a fully enclosed, unsupported ~71.5mm-diameter
  horizontal span. **This is unaffected by the v7 tip-cap change, below** — the ceiling bridge is
  a function of the hollow-to-brim transition, which exists regardless of what happens at the
  plug's other end.
- **Slicer setting callout:** confirm supports are set to "touching build plate only" before
  slicing the lid, or a permissive "everywhere" setting may generate unremovable support material
  inside the sealed void.
- **Orientation: flat-underside-down.** Unchanged by v7 — see the v7 section for why this remains
  correct even with the handle gone and the apex flattened.

**Material impact (as of v6):** the hollow plug added **~9.49 cm³** to the lid. Lid material
volume at v6: **~219.2 cm³ → ~228.7 cm³**. **These lid-volume figures are superseded by v7's
194.2929 cm³ — see below.**

**Verification:** independently confirmed by three separate methods (Coder, Tester, Reviewer) —
collision-free fit against the body's internal taper (5.0mm margin), exact 4.000mm wall thickness,
a single valid manifold solid, handle geometry completely unaffected (at the time), and exact
0.500mm diametral clearance. Full cross-verification table: `parameters.md` §12.

### v7 (2026-09-02) — handle removed entirely, plug capped, brim shrunk+thickened to flush, dome apex flattened (lid only; body/neck-fit-test unchanged)

**This is the most significant identity-level change this project has made since its original
concept approval, and it's documented here with that weight, not folded in as a routine lid
tweak.** Five coordinated changes landed in this single revision.

**1. Handle removed entirely — deliberate, confirmed reversal of the concept brief's own "hard
constraint."** `concept/brief.md` describes the open-loop bail handle as **"the key
differentiating feature"** of the whole design, states it should "read as an intentional,
load-bearing part of the lid, not a decorative nub," and calls its open-through-hole geometry
**"a hard constraint when the Planner moves to CAD."** Every revision from v1 through v6 treated
that constraint as binding, and every Reviewer pass independently re-verified the handle's
open-loop integrity as one of this project's three named hard constraints. **The requester has
explicitly and directly confirmed removing the handle entirely, fully aware this reverses that
original hard constraint** — the concept brief's own language is not being edited or walked back;
it is being knowingly superseded by this later, direct instruction. There is no nub, knob, raised
boss, or any other replacement grip feature. You lift the lid by gripping the brim/dome edge by
hand.

**2. Concept-fidelity — carrying the Reviewer's actual finding, not a softened version of it.**
The Reviewer's full v7 review looked at this cumulatively, not the handle removal in isolation:
layered on top of the already-disclosed v4 "ginger jar" belly-pinch drift and the persistent
"banded, partially-cylindrical" collar (both previously accepted as minor, functionally-necessary
tradeoffs specifically *because* the handle was still there anchoring the design's identity
against them), **removing the handle too leaves this design reading as generic rather than
differentiated from the reference commercial urn this project was originally written to
differentiate from.** The Reviewer is explicit that this is not a defect and does not block —
it's a legitimate, informed, user-confirmed creative/business call, and the CAD itself is sound —
but recommends a real visual check-in with the requester (the original concept image, the archived
v6 render, and the new v7 render, side by side) asking plainly whether this still reads as the
differentiated product originally set out to build, before treating it as truly final. **That
check-in has not yet happened and is carried forward as an open item — see "Status" below.**

**3. Plug capped.** The v6 plug (79.5mm OD × 10mm deep, hollow, 4.0mm wall, 0.5mm diametral
clearance) was open at its tip — a plain tube, sealed at the top where it meets the brim, open at
the bottom. As of v7 the tip is **capped**: the last **4mm nearest the tip is now a solid disc**
(full 79.5mm OD), and the remaining **6mm nearest the brim stays hollow** (same 4.0mm wall as
before, just over a shorter run). This creates a genuine sealed internal void — the plug's hollow
interior is now fully enclosed, with no opening to the outside anywhere. **The resulting topology
(13 faces total — 6 planes, 3 cylinders, 1 sphere, 3 toruses — arranged as one outer shell of 10
faces plus one internal void shell of 3 faces, i.e. a `BREP_WITH_VOIDS` solid; 2 disjoint
components when tessellated to a mesh) is the correct, expected signature of a genuinely sealed
cavity, not a defect or a fragmented/broken part.** This was independently confirmed correct by
**four separate methods** across this project: the Coder's construction reasoning, the Tester's
mesh-split analysis, the Tester's direct text-level parsing of the STEP file's native B-rep
entities, and the Reviewer's live query of the actual Fusion `BRepBody` object model. **If you
ever inspect this file and a mesh tool reports "2 solids," that is expected — do not attempt to
"fix" it by merging or re-sealing anything.**
- The plug's fit-critical outer wall (79.5mm OD, 0.5mm clearance against the body's 80mm bore) is
  completely unaffected by the cap — same numbers as v6, re-verified.
- The pre-existing ~71.5mm internal bridge (where the hollow tube meets the solid brim above it)
  is unchanged by the cap — same span, same expected sag/stringing under default settings, same
  reason it doesn't matter (fully sealed, never visible). Capping the *other* end doesn't touch it.
- The new tip cap itself introduces no new bridging risk, specifically because of print
  orientation: it's the literal first layer(s) printed, resting directly on the build plate — a
  solid disc is if anything a *better*-supported first layer than the open ring it replaces.
- Capping likely makes the standing "supports must be set to touching-build-plate-only" mitigation
  more reliable (a sealed void has no unobstructed path back to the bed for a slicer to detect),
  though this is reasoned from how that slicer setting generally works, not confirmed against a
  real slice — **check your slicer's print preview to confirm no support is generated inside the
  sealed cavity** before committing to the full lid print.

**4. Brim — shrunk to flush, thickened.** OD **99.700mm** (down from 122mm) — a deliberate
**-0.3mm allowance below the nominal 100mm**, landing flush with the body's 100mm-OD collar with
zero overhang, replacing the overhanging-brim design used in every prior revision (100mm in
v1–v4, 122mm in v5–v6). Thickness **10mm** (up from 5mm). **Geometry correction, worth stating
plainly because earlier notes got this wrong:** the transition from the brim's vertical wall into
the dome is **not** a simple flat "10mm ring," as described in `specs.md`'s original corroborating
math and repeated in an earlier Tester pass. The Reviewer's own live B-rep query of the built part
found the true shape is a **smooth, compound two-stage fillet** (two tangent toruses) with a
genuine, if narrow, **flat annular plane face nested between them — about 5.35mm wide, at Z≈20mm,
spanning roughly r=41.5–46.85mm** — a real, nonzero-area flat step, not a tangency artifact, but
also not the "10mm flat ring, matching the collar's own wall band" originally described. This
doesn't change anything functionally (it's self-supporting either way, confirmed by radius-
monotonicity and crease-detection sweeps) — it's a documentation-accuracy correction, not a
geometry fix.
- **Named risk unique to this exact-match edge:** a brim printed to nominal 100mm against a
  collar also printed to nominal 100mm has none of the comfortable overhang margin every prior
  brim/collar pairing had to absorb ordinary FDM dimensional variance. FDM's systematic tendency is
  for external bosses/rims to print slightly *oversized*, not undersized — so the more likely
  failure direction is the lid brim overshooting the collar's edge by a fraction of a millimeter
  (reading as a small proud lip), not the collar peeking out past an undersized lid. The -0.3mm
  allowance is a deliberate hedge against exactly this. If the first print still reads proud
  rather than flush, a further small negative allowance is the fix, not a redesign.

**5. Dome apex — flattened plateau, replacing the fully-rounded point apex.** Base OD **80mm**
(down from ~97–98mm, re-derived to match the new flush 99.700mm brim via the same 0.80
dome-to-brim ratio this project has used since v1 — notably converging back on the same absolute
80mm figure v1–v4 used, for an unrelated reason). Height **29mm** above the brim top. The apex is
now a **flattened plateau, 21.73mm diameter** — chosen over a fully-rounded alternative because,
with no handle occupying the apex anymore, a flat spot reads as more intentional, and it also
eliminates the previously-disclosed apex-drooping/ribbing print-quality risk (a rounded apex
closing to a near-degenerate point is what causes that artifact; a flat terminal disc removes the
mechanism entirely, not just reduces it).

**The honest story behind the 21.73mm figure, not just the final number.** The original target
was **~22.00mm** (roughly a quarter of the 80mm dome base, sized against a concept-comparison
reference image, `concept/v7-dome-apex-flattened.png`). The first attempt reused the dome's
existing sphere radius (left over from the pre-flattening, point-apex design) and landed at only
17.70mm — a bigger miss, and one the Tester correctly flagged as *not* mathematically forced (a
slightly smaller sphere could hit the original targets much more closely). That finding was acted
on: the sphere radius was corrected to the exact value that makes the *raw, unblended* curve pass
through 22mm at 29mm of height — and it does, exactly, independently confirmed. **What still keeps
the final built figure at 21.73mm rather than a clean 22.00mm is the tangent blend itself**, which
has to consume a small amount of the curve's radius to smoothly fillet the sphere into a flat
plateau without a visible kink (the same class of transition this project has treated as worth
fixing properly since v2, not left as a sharp corner). At this geometry, **hitting exactly 22.00mm
and achieving genuine tangency turned out to be mutually exclusive — tangency was correctly
prioritized**, both because the spec's own precision requirement on 22mm was always soft ("an
aesthetic judgment call... roughly a quarter," never a tight tolerance) while the tangency
requirement is explicit and reasoned from a real, previously-documented print-defect class. The
practical difference is negligible: 21.73mm ÷ 80mm = **27.16%**, against the **27.5%** the 22mm
figure was itself approximating — a 0.34-percentage-point difference, not visually distinguishable
from the reference image the original figure was eyeballed against. Independently confirmed via
two methods (mesh vertices at the plateau and the STEP file's native torus parameters, agreeing to
6 significant figures) and independently re-verified as genuinely tangent (zero creases, monotonic
radius) on both sides of the blend.

**6. Total heights — a substantial, positive change.** Lid height (seating plane to top of
plateau) drops from **75mm to 39mm** — a **-48% reduction**, driven almost entirely by the
handle's removal (the handle alone accounted for 40mm of the old height). Lid bounding-box height
(plug tip to plateau top) drops from **85mm to 49mm** — a **-42% reduction**. **Combined assembled
height (body rim + lid above its seating plane) drops from ≈228.5mm (v6) to ≈192.5mm** (153.5mm
body + 39mm lid) — each part still individually clears the 256mm build volume with enormous
margin regardless, but this is a real, substantial reduction on its own terms. This connects
directly to an earlier competitive-research concern (raised in conversation with the requester,
not written into a prior spec revision, but real context worth stating here) about this design's
overall height running long versus competitor pet urns — the height drop is a genuine, positive
side effect of the handle removal, not something separately engineered for.

**7. Material volume and cost — a real decrease.** Lid material volume drops from **~228.7 cm³
(v6) to 194.2929 cm³ (v7)** — a real reduction (the shrunk/flush brim and removed handle outweigh
the thicker brim disc and the plug's new solid tip cap). Body is unchanged at ~278.94 cm³. At PLA
(~1.24 g/cm³) and PETG (~1.27 g/cm³) densities: body ≈346g (~$7.0–8.7 in filament, unchanged), lid
≈247g (~$5.0–6.2, down from ≈290g/~$5.6–7.0 at v6). **Combined pair: roughly $12.0–14.9** — down
from ~$12.6–16.3 at v6, a real (if modest, ~6–9%) decrease, driven by the handle's removal
outweighing the thicker brim and capped plug tip.

**8. Print orientation — unchanged, and the alternative was checked, not assumed away.**
Flat-underside-down (plug-tip-down) remains the print orientation. With the handle gone and the
apex flattened, a plateau-down orientation is genuinely worth naming as a new option this geometry
didn't have before — and it was specifically considered and rejected, independently by both the
Coder and the Reviewer. Flipping the part would invert the entire dome's overhang class: today,
radius is non-increasing from the plug tip all the way to the plateau (self-supporting
throughout); flipped, the dome becomes a classic expanding cone needing support under virtually
its whole visible exterior, and the plug's new tip cap would go from a bed-supported first layer to
an unsupported last layer over a sealed void — reintroducing the exact bridging risk that
capping-then-orienting-tip-down was designed to avoid. Flat-underside-down remains the right call.

**9. Usability — dropping the lid is now more likely, not just a routine watch-item.** With no
dedicated handle, gripping a smooth dome by hand is less secure than a purpose-built grip loop.
This is **not** a survivability/durability concern (solid PETG, no fragile features outside the
sealed internal bridge) — it's a **likelihood-of-dropping** concern, and the Reviewer elevated it
specifically because this object holds irreplaceable cremated remains, at a moment (transferring a
filled urn) where a slip is genuinely distressing, not just cosmetically costly. **Handling
recommendation: lift with a full hand cradling the dome/brim, not a fingertip pinch on the edge;
consider lifting the lid off and setting it down separately before moving the filled body, rather
than carrying the assembled unit by the lid.**

Full numbers and independent four-way verification: `parameters.md` §13. Full review:
`dot_pipeline/review.md`, "FULL RE-REVIEW — 2026-09-02: v7 major lid revision."

## Files

| Path | Contents |
|---|---|
| `step/urn-body.step`, `3mf/urn-body.3mf`, `stl/urn-body.stl` | **Current body — still v5 geometry, UNCHANGED by v6 or v7.** Neck/collar widened (58mm→80mm ID), overall height trimmed (160mm→153.5mm) to hold cavity volume steady; belly/wall untouched from v4. Timestamp remains 2026-08-31 — neither the v6 lid-plug round nor the v7 lid revision re-exported this file. |
| `step/urn-lid.step`, `3mf/urn-lid.3mf`, `stl/urn-lid.stl` | **Current lid (v7)** — handle removed entirely (no replacement grip), plug tip capped (6mm hollow + 4mm solid), brim shrunk+thickened to 99.700mm OD × 10mm (flush with the 100mm collar, zero overhang), dome base re-derived to 80mm OD × 29mm tall with a flattened 21.73mm-diameter plateau apex (replacing the fully-rounded point apex). Re-exported 2026-09-02 (17:32); overall part height now 49mm (was 85mm at v6). |
| `archive/v2-with-magnet-pockets/` | Superseded body + lid STEP/3MF/STL from before the 2026-08-28 magnet-pocket removal, preserved unmodified — reference only |
| `archive/pre-plug-lid-v5/` | Superseded lid STEP/3MF/STL — the v5 lid (122mm brim, ~97–98mm dome, handle intact) from just before the v6 plug was added — reference only |
| `archive/pre-v7-handle-removal/` | Superseded lid STEP/3MF/STL **and hero render** from before the v7 revision — the v6 lid with its open-loop handle, overhanging 122mm brim, ~97–98mm dome base, and open-tip plug. Kept specifically so the handle-vs-no-handle comparison (and the concept-fidelity check-in recommended below) has a real reference image and geometry to compare against, not just a written description. |
| `archive/pre-v4-belly-render/pet-memorial-urn-hero.png` | Superseded hero render, from before the v4 belly-fullness edit — reference only |
| `archive/pre-v5-neck-widening-render/pet-memorial-urn-hero.png` | Superseded hero render (v4-era, 58mm neck/78mm collar/160mm height) — from before the v5 neck/collar widening and lid resize — reference only |
| `step/neck-fit-test.step`, `3mf/neck-fit-test.3mf`, `stl/neck-fit-test.stl` | Small standalone test article (just the neck + collar, ~35mm tall) — print this first to physically check a real crematorium remains bag fits through the neck opening before committing to the full ~153.5mm body print. **Still v5 geometry, UNCHANGED by v6 or v7** (80mm ID / 88mm neck OD / 100mm collar OD, timestamp 2026-08-31) — not the old 58mm/78mm/66mm figures from v1–v4. See `parameters.md` §7 for the full correction and what it does/doesn't need to be re-printed for again in the future. |
| `concept/` | Approved concept brief and reference images, including the two dome-apex comparison mockups (`v7-dome-apex-rounded.png` vs. `v7-dome-apex-flattened.png`) used to decide the v7 plateau |
| `render/pet-memorial-urn-hero.png` | **Current hero render — v7 geometry** (handle removed, plug/brim/dome all reflecting the live v7 geometry) — the pre-v7 (v6, handle + overhanging brim), pre-v5, and pre-v4 versions are archived, see above |
| `dot_pipeline/` | Full planning/build/test/review history (`specs.md`, `tests.md`, `verdict.md`, `review.md`) — the detailed narrative behind every decision below, if needed |
| `parameters.md` | Full dimensional/technical reference for rebuilding or editing this design |

## Print notes

- **Material: body = matte or silk PLA, lid = PETG.** Different materials for the two parts, on
  purpose — see `parameters.md` §5 for the reasoning. **Note on the lid's original justification:**
  PETG was originally chosen in part because the (now-removed) handle's root fillet was the
  feature most exposed to a knock or repeated grip load. That specific reasoning no longer applies
  as of v7, since there is no handle — PETG is being kept anyway for its general toughness on the
  lid's remaining thin-fillet transitions (the brim-to-dome compound fillet, the dome-to-plateau
  fillet, the plug wall) and to avoid introducing a new material-behavior variable into an
  otherwise-settled design. This is a carried-forward default, not a fresh v7-specific derivation
  — stated plainly rather than silently re-asserting the original (now partly stale) reasoning.
- **Orientation:** body prints base-down, opening/neck facing up (matches its natural resting
  stance, self-supporting everywhere except one named watch-item band, below). Lid prints
  flat-underside-down (plug-tip-down), dome facing up — **unchanged by v7's handle removal or dome
  flattening**: with no handle and a flattened apex, a plateau-down orientation is a new option
  this geometry didn't have before, and it was specifically considered and rejected (independently,
  by both the Coder and the Reviewer) — flipping the part would invert the whole dome's
  self-supporting "shrinking radius" class into a real expanding-cone overhang needing support
  under nearly its entire visible exterior, and would turn the plug's new tip cap from a
  bed-supported first layer into an unsupported bridge over a sealed void. Flat-underside-down
  remains the right call. `neck-fit-test` prints flange-down, same self-supporting logic as the
  body.
- **Overhang watch-item on the body (same disclosed risk as every prior revision, unaffected by
  v6/v7's lid-only changes):** the only zone on the entire body that exceeds the conventional 45°
  self-supporting guideline is the neck-to-collar external blend, just below the rim. It measures
  **~45.6–46.4°** from vertical depending on measurement method — a short span on a fully closed
  360° revolve, not a one-sided cantilever. A touch more cooling or a modest local speed reduction
  there is cheap insurance.
- **Watch-items on the lid, updated for v7:**
  1. The outer support annulus below the plug (where the 39.75mm plug wall meets the wider brim
     above it) still needs support material, and part of that annulus lands on the visible brim
     surface — an accepted tradeoff, not a defect.
  2. The ~71.5mm internal bridge capping the plug's hollow interior (now a 6mm hollow run, was
     10mm pre-cap) is still expected to sag/string under default settings — still fine, because
     that surface remains sealed and never visible or fit-critical. **New in v7:** the plug's tip
     is now a solid cap rather than an open end — this is the literal first-printed layer in the
     specified orientation (bed-supported, not a bridge) and should need no special attention.
  3. Confirm your slicer's supports are set to "touching build plate only," not "everywhere,"
     before slicing the lid — more important than before, since the plug's interior is now fully
     sealed at both ends and has zero access path for support removal if any gets generated inside
     by mistake. Check the print preview to confirm no support appears inside the sealed cavity.
  4. **New named risk (v7): the flush 99.700mm brim-to-100mm-collar fit has essentially zero
     print-tolerance margin**, unlike every prior overhanging-brim design. FDM external features
     tend to print slightly oversized, so expect the more likely failure mode to be a small proud
     lip rather than a gap — the -0.3mm allowance already baked into the 99.700mm brim OD is a
     hedge against this, not a guarantee. If the first print still reads proud rather than flush,
     a further small negative allowance is the fix, not a redesign.
- **Bed fit:** body ~154×154×153.5mm (unchanged from v4/v5/v6), lid ~99.7×99.7×49mm (**shrunk
  substantially in v7** — down from ~122×122×85mm at v6, driven by the flush brim and the handle's
  removal), `neck-fit-test` ~144×144×35mm — all clear a 256×256×256mm bed with large margin.
  Printed as separate jobs, so combined assembled height (**≈192.5mm, down from ≈228.5mm at v6**)
  is not a bed-fit constraint either way.
- **Cost:** combined filament for the pair is now roughly **$12.0–14.9** (down from ~$12.6–16.3 at
  v6) — a real, if modest, decrease driven by the lid's material volume dropping from ~228.7 cm³ to
  194.2929 cm³ (the shrunk/flush brim and the removed handle outweigh the thicker 10mm brim disc
  and the plug's new solid tip cap). Body cost is unchanged (~$7.0–8.7). Still a small, reasonable
  cost for a decorative memorial piece.
- **Slicer settings are not embedded in any exported file** — set manually: 0.16–0.2mm layer
  height, 15–20% infill (both a reasonable default, not yet explicitly confirmed by the requester),
  plus PETG-appropriate temperature/cooling for the lid. **For the lid specifically, confirm
  supports are set to "touching build plate only" before slicing** (see watch-item 3, above) — this
  matters more now that the plug's interior is fully sealed at both ends.
- No magnet pockets exist in the current CAD (removed 2026-08-28), so there is nothing left to
  hole-size-verify for that feature. If you add a magnet assist yourself later (slicer
  pause-and-embed or post-print drill-and-glue), that fit is entirely yours to check — it's outside
  this CAD by design now.
- **Hole/circular-feature shrinkage:** the **80mm** neck/collar ID (widened from 58mm in v5) is
  the one circular dimension a mating object (the remains bag) actually needs to clear. FDM parts
  typically print circular holes slightly undersized versus the model. No compensation has been
  baked into this dimension because there is no hard target diameter to compensate toward — it's
  an `ESTIMATED`, untested fit against a real bag, not a hardware spec. **Check the actual
  as-printed ID on the first `neck-fit-test` print** (the v5-rebuilt version, representing 80mm —
  not any older copy of this file) before assuming 80mm nominal is what you'll actually get.
- **Plug clearance test coupon recommended before the full lid print (unchanged since v6).** The
  plug's 0.5mm nominal diametral clearance is more likely to print **tighter**, not looser, than
  designed — FDM systematically tends to print bores undersized and bosses/plugs oversized, and
  this fit crosses a PETG plug against a PLA body opening (a named material-shrinkage mismatch
  risk). Print a small stand-alone clearance-test coupon at the plug's nominal dimensions and check
  the fit before committing to the full lid print.
- **Handling note (new in v7 — read this if you're handling a filled urn):** with the handle
  removed, there is no dedicated grip anywhere on the lid — lift it with a full hand cradling the
  dome/brim, not a fingertip pinch on the edge, and consider lifting the lid off and setting it
  down separately before moving the filled body, rather than carrying the assembled unit by the
  lid. This is a likelihood-of-dropping concern, not a durability one (the lid itself is solid,
  sturdy PETG) — but the object holds irreplaceable remains, so it's worth stating plainly rather
  than leaving it as an implied risk.

## Status

**Approved by Reviewer** for the v5 neck/collar widening/height trim/lid resize (a full,
from-scratch re-review — business fit, concept fidelity, hard constraints, an independent
third-method geometry spot-check, documentation, and cost — see `dot_pipeline/review.md`, "FULL
RE-REVIEW — 2026-08-31: v5 major revision"), the v6 lid-underside alignment plug (a targeted
addendum — geometry independently re-confirmed by a fourth method, the bridging/support risk
framing given plainly rather than minimized — see "ADDENDUM 4 — 2026-09-01"), and the **v7 handle
removal / plug cap / brim+dome rework** (a second full, from-scratch re-review — concept fidelity,
hard constraints, an independent geometry spot-check via a live Fusion B-rep query, print
orientation, and a usability re-assessment — see "FULL RE-REVIEW — 2026-09-02: v7 major lid
revision"). **This "Large" build is one of three sizes now in the lineup** — see
[`small/README.md`](small/README.md) (0–25 lb, CAD-complete and reviewed) and
[`medium/README.md`](medium/README.md) (25–50 lb, CAD-complete and reviewed) for the other two.
Both carry forward this build's v7 design identity (no handle, flush brim, flattened dome plateau)
at independently re-derived dimensions, and both have their own still-open physical neck-fit-test
requirement, exactly as this build does below.

**Two items are carried forward as genuinely open, not routine watch-items — read both before
treating this project as finished:**

1. **Whether a real crematorium remains bag actually fits through the 80mm neck opening.** This
   has been the single most load-bearing open item in this project since v5, is unaffected by v6
   or v7 (both lid-only rounds), and remains physically unverified. Print the (v5-rebuilt)
   `neck-fit-test.stl` and try a real or mocked remains bag through it before treating this project
   as fully validated.
2. **A genuine, non-blocking business/creative flag from the v7 Reviewer pass, stated here without
   softening it:** the cumulative effect of removing the handle — the concept brief's own "key
   differentiating feature" — layered on top of the already-disclosed v4 belly-pinch drift and the
   persistent banded collar, leaves this design **reading as generic rather than differentiated**
   from the reference commercial urn this project was originally written to differentiate from.
   The Reviewer is explicit that this is not a defect and does not block approval — it was an
   explicit, informed, user-confirmed decision, and the CAD itself is sound — but recommends a real
   visual check-in with the requester (the original concept image, the archived v6 render at
   `archive/pre-v7-handle-removal/pet-memorial-urn-hero.png`, and the current v7 render at
   `render/pet-memorial-urn-hero.png`, side by side) asking plainly whether this still reads as the
   differentiated product originally set out to build, or now reads as a generic jar with a lid —
   before this design is treated as truly final.
   **Resolved (2026-09-09): the requester has confirmed directly that this lid is not designed for
   repeated removal, so the absence of a handle/grip feature is intentionally fine** — this closes
   out the concern raised by the Reviewer's "reads as generic" flag from a usability standpoint
   (the object isn't meant to be picked up and set down often the way a jar with a handle would be).
   This confirmation has been carried forward to the Small and Medium size builds as well (see
   below) rather than re-litigated at each size.

**Handling note:** with the handle removed, lifting the assembled unit is now a more deliberate
task than before — see the handling note in "Print notes," above. This is a likelihood-of-dropping
consideration the Reviewer specifically elevated given what this object holds, not a structural
concern.

Five real incidents (manual/direct edits or feature-rebuild side effects disturbing the model) —
plus three deliberate, user-directed scope/feature changes narrated alongside them (the v3
magnet-pocket removal, the v6 plug addition, and the v7 handle removal/lid rework) — have been
found and handled across this build. The most recent incident (a stray, unexplained pair of fillet
features, caught and cleanly removed before the v5 body rebuild even started, and never reaching a
shipped export) is the fifth. See `parameters.md`'s incident notes (§6) if you're editing this file
further and want to avoid repeating them. All five incidents were independently re-verified as
fully recovered/handled; none left residual damage in the shipped files.
