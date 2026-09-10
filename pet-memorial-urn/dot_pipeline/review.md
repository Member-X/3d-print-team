# Reviewer Verdict — Pet Memorial Urn (Large, single-size build)

## APPROVED — print-ready, with one required documentation follow-up (non-blocking for print) and several named non-blocking watch items

The geometry in `step/`, `3mf/`, and `stl/` for `urn-body` and `urn-lid` is sound, independently
re-verified by me from scratch (not just re-read from `tests.md`/`verdict.md`), and matches the
approved concept well. Nothing found here reopens any of the settled Coder/Tester round-trips.
The one real gap I found that isn't already on record anywhere in this project is a **missing
top-level `README.md` and `parameters.md`** — every other completed project in this repo has
both, this one has neither. That's cheap to fix and shouldn't be skipped just because the CAD
itself is done. Full detail below.

---

## 1. Business fit — PASS

The design solves the stated problem: a memorial urn sized to the requester's own 90 lb / 1 in³-
per-lb rule (§4.1 of `specs.md`), with a genuinely liftable, open-loop lid handle and a
magnet-assisted (not airtight-dependent) closure appropriate for remains that are already
bagged. The plain, undecorated body and the loop-handle lid are the two features the concept
brief explicitly calls out as load-bearing to the design's identity, and both are intact in the
shipped files (verified independently in §3 below, not just asserted).

## 2. Technical/concept parity — PASS, independently re-verified, one honest departure named

I did not treat the chain of Coder/Tester agreement as sufficient on its own. I opened the live
Fusion document (`pet-memorial-urn`, 3 components: `urn-body`, `urn-lid`, `neck-fit-test` — no
size-variant scope creep, confirming §12's single-size constraint) and independently re-measured
the shipped `stl/urn-body.stl`, `stl/urn-lid.stl`, `3mf/urn-body.3mf` via `trimesh`, using my own
script, not the Tester's. Results, cross-checked against `tests.md`'s claims:

| Check | My independent measurement | Tester's claim | Match |
|---|---|---|---|
| Belly position | peak radius **73.0000mm at exactly z=72.0mm** (45.00% of 160mm), single clean symmetric peak | 73.000mm @ z=72.0mm, 45.00% | Exact |
| Base cleanliness (the historically-defective feature) | 0.1–5mm z-sweep: single boundary loop, **zero interior holes**, at every sampled height, in both STL and re-confirmed via collar cross-section area math | Clean, 77/136 vertices at uniform 49mm radius | Confirmed independently, different method |
| Collar magnet pockets | cross-section area drops by ~90.1mm² exactly at z=157.8mm (3 × π×3.1² ≈ 90.6mm²) — 3 pockets, correct size/depth | 3× 6.2mm dia, 34mm bolt circle, 2.2mm deep | Confirmed independently, different method (area-based, not vertex-based) |
| Shoulder→neck taper self-support | radius **monotonically non-increasing** at every 0.5mm step from z=119–145mm, zero increasing steps; peak local angle **54.499° at z=137mm** | Monotonic, 54.5° at z≈137mm | Exact |
| Neck-to-collar external blend | slope changes gradually across z=145–152mm (max single-step slope-jump **0.2275**), no discontinuity; peak angle **45.564° from vertical** | Smooth S-curve, largest step ~0.23, peak ~45.6° | Exact — the fix is real, not re-asserted |
| Plain-body / no engraving | radial std-dev **0.001–0.007mm** at 7 heights (z=20–130) — essentially perfect circles | 0.23–0.30mm (STL-facet-noise-limited method) | Confirmed, more tightly than the original test |
| Handle open-loop | 2 boundary loops (a hole) present at y=−4mm to +4mm, 1 loop (solid) outside that range | Same window (y=−4 to +4) | Exact |
| Body/lid material volumes | 293.14 cm³ / 150.82 cm³ (mesh) | 293.14 cm³ / 150.82 cm³ | Exact |

I regard this as a genuine, from-scratch re-derivation (I hit and fixed my own methodology bug
along the way — an unconverted local-frame projection that initially gave a false 75mm belly
radius — which is exactly the kind of thing a fresh pass is supposed to catch), not a rubber
stamp of the pipeline's own numbers.

**Concept-fidelity spot-check, done independently rather than accepted on the Tester's
"looks consistent" read:** I pixel-measured `concept/concept-v2.png` directly (edge-traced the
jar's silhouette against its background) — the belly reads as sitting roughly mid-height to
slightly-below-mid-height in the photo, consistent with (not contradicting) the low, wide belly
the exact 45%/z=72mm geometry produces. Photo-edge-detection on a textured, softly-lit product
photo has real error bars (my own estimate lands in a 45–50%-up-from-base band, not a single
precise number), so I'm treating the Tester's exact 3D ray-cast (73.000mm/45.00%) as the
authoritative figure and the photo check as corroborating, not competing, evidence.

**One honest, fresh finding — a real but small concept departure, not previously named this way:**
comparing a live Fusion screenshot of `urn-body` side-by-side against `concept-v2.png`'s own
neck/rim close-up, the built model's neck-to-collar area reads as a distinctly **banded,
partially-cylindrical rim** (the 15mm-tall constant-radius collar, required to give the magnet
pockets a flat home, per spec §6.2) where the concept shows one **continuous, softly rolling
curve** with no comparable straight/cylindrical segment. The recent blend-smoothing work
(R9/R21 in `tests.md`) fixed the *sharp-kink* version of this problem, and it's genuinely fixed —
but even the smoothed version is still a visibly more "banded" rim than the concept's fully
organic silhouette. This is a disclosed, functionally-necessary tradeoff (the magnet pockets
need a flat, constant-thickness wall under the lid's flat seating plane), not an oversight, and
it still plausibly reads as "a rim reinforcement detail on a ceramic vessel" — I'm not blocking
on it, but I want it named explicitly as a real, if minor, visual drift from the signed-off
reference, per the instruction not to silently wave through drift. **The lid, by contrast, is an
excellent match** — dome proportions, brim overhang, and open-loop handle shape all track
`concept-v2.png`'s lid close-up closely.

## 3. Hard constraints — all three independently reconfirmed, not re-read from prior passes

1. **Plain/smooth body, no engraving/plaque/text anywhere.** Reconfirmed via my own radial
   cross-section analysis at 7 heights spanning base to neck (table above) — deviation is
   essentially zero (mesh-tessellation-level noise only), no trace of a plaque or recessed panel
   anywhere I sampled. **Confirmed.**
2. **Handle is a genuine open through-hole loop, not a blind cavity.** Reconfirmed via my own
   y-axis cross-section sweep of `stl/urn-lid.stl` — a real hole (2 boundary loops) exists from
   y=−4mm to +4mm and vanishes (1 loop, solid) immediately outside that band. **Confirmed.**
3. **Single-size build, no variant scope creep.** The live Fusion document contains exactly 3
   components (`urn-body`, `urn-lid`, `neck-fit-test`) — no hidden/alternate-size bodies or
   duplicate scaled components anywhere in the document. **Confirmed.**

## 4. Overhang angles — independent assessment, not a rubber-stamp of the chain of agreement

Per the specific request for my own fresh take:

- **Shoulder-to-neck internal taper (locally up to ~54.5°):** I agree with the self-supporting
  assessment, and I checked the actual mechanism myself rather than accepting the "shrinking
  cone" argument by description — I directly confirmed **zero locally-increasing radius steps**
  across the entire z=119–145mm span at 0.5mm resolution. Since the argument's validity depends
  strictly on the sign of `dr/dz`, not its magnitude, and the sign is confirmed negative
  everywhere in this span, I concur this transition is inherently self-supporting regardless of
  local angle. No print-support risk.
- **Neck-to-collar external blend (~45.6° peak, now a genuine smooth curve):** I independently
  confirmed this is now a real, continuous S-curve (no discontinuous jump anywhere in a 0.1mm
  resolution scan) — the earlier hard-chamfer defect is genuinely gone. My own take on the
  ~45.6° peak, arrived at independently rather than inherited: this is a few degrees over the
  conventional guideline, on a fully closed 360° revolve (not a one-sided cantilever), for a span
  of only a few millimeters at the peak — I agree this is low risk, but I'd stop short of calling
  it zero risk the way the shrinking-taper case is; it's a genuine (if narrow and shallow)
  widening-with-height transition. **Practical recommendation, stated plainly for whoever
  slices this: treat the z≈147–151mm band as a "watch it on the first print" zone — a touch more
  cooling / a modest local speed reduction there is cheap insurance, not a redesign.**
- **Neck opening (58mm) vs. a real cremation bag:** unchanged status — still an `ESTIMATED`,
  physically-untested dimension per spec §4.4, exactly as the spec itself flags it. This is a
  genuine open item, correctly not silently treated as resolved anywhere in this pipeline. It
  does not block this review (it requires a physical bag, which no CAD reviewer can supply), but
  it is carried forward below as a named, must-not-be-forgotten item, per the task's own framing
  that an `ESTIMATED` mating dimension is a review blocker if silently dropped rather than a
  non-issue if explicitly carried forward with a real plan to close it out (the `neck-fit-test`
  article exists for exactly this).

## 5. Documentation — the one real gap found in this pass

`dot_pipeline/specs.md` is excellent as a planning document (VERIFIED/DERIVED/ESTIMATED tagging
throughout, a real §13 revision history). But **this project has no `README.md` and no
`parameters.md` at the project root** — every other completed project in this repo
(`cat-toy-holder/`, `noise-maker/`, `switch-plate-covers/`, `lightswitch-cover-single/`) has both.
`dot_pipeline/*` is pipeline working history; `README.md`/`parameters.md` at the project root is
this shop's own established convention for the lightweight, durable reference a future editor or
the requester would actually reach for — known limitations, print orientation, material
reasoning, and a short parameter sheet distinct from the much longer planning narrative in
`specs.md`. Nothing here blocks the physical print (the exported files are correct and complete),
but per this shop's own completion-workflow convention this should be produced before the project
is called finished. **Required follow-up, not a print blocker.**

Two smaller, related observations from independently inspecting the files themselves:

- **Material intent is only partially captured in exported file metadata, not "not captured" as
  broadly stated in `tests.md`/`verdict.md`.** I opened `3mf/urn-body.3mf`'s raw XML directly: it
  actually does carry a `<metadata name="Description">` field with the full "Material: matte/silk
  PLA..." text (Fusion exported the component description verbatim). `3mf/urn-lid.3mf`, by
  contrast, has no such field at all — it was exported before the PETG description was written
  onto the component. Practically this changes nothing (no slicer auto-selects material from a
  free-text 3MF Description field, so "must be set manually" remains correct either way), but the
  blanket claim that material "is also not captured in any file metadata" isn't quite accurate for
  the body file specifically — worth a precise footnote rather than a repeated broad claim.
- **Minor repo hygiene:** `pet-memorial-urn/nul` is a stray leftover file (a Python traceback —
  `AttributeError: 'NoneType' object has no attribute 'to_2D'` — apparently redirected to a
  literal file named `nul` from a Windows/POSIX shell mismatch during a Tester script run). Not a
  design issue, just noise; safe to delete.

## 6. Cost — PASS, trivially cost-effective

Material-shell volumes (mesh-measured, independently): body 293.14 cm³, lid 150.82 cm³. At PLA
density (~1.24 g/cm³) the body is on the order of 300–360g of filament depending on how much of
the nominal solid volume the slicer's stated 15–20% infill actually reduces (the walls are only
4mm nominal, leaving little room for an internal infill lattice in the curved wall itself — most
of the infill percentage will only matter in the thicker floor/collar sections); the PETG lid
(~1.27 g/cm³) is on the order of 150–190g. At typical consumer PLA/PETG pricing this is roughly
**$8–12 in filament for the pair** — trivially cost-effective for a decorative memorial piece.
Print *time* for a ~160mm tall part at 0.16–0.2mm layers will be substantial (many hours), but
that's a scheduling consideration, not a material-cost one, and nothing in the geometry (no
unnecessary solid mass, no oversized infill requirement) works against it.

## 7. What's carried forward, not re-litigated, not a blocker on this review

1. **Neck-opening-vs-real-bag physical test** — the `neck-fit-test` article is sound (I did not
   re-verify it from scratch since its represented dimensions were untouched by the last several
   rounds of change and were already independently confirmed in `tests.md` R5/R16/R24). This is
   the requester's physical test to run; no CAD reviewer can close it out.
2. **Magnet fit test coupons** (PLA body pockets, PETG lid pockets) — recommended before a full
   production print, per `tests.md`. Not re-litigated here.
3. **Slicer settings must be set manually** — 0.16–0.2mm layer height, 15–20% infill, plus
   PETG-specific temperature/cooling tuning for the lid (and, per §4 above, a specific watch-item
   band at the lid's — no, at the **body's** neck-to-collar z≈147–151mm region). None of this is
   embedded in the 3MF files.
4. **PETG-for-lid tradeoffs** (magnet pocket oversize possibly tight for PETG; dome-apex cooling)
   — already well-reasoned in `tests.md` R4, not reopened here.

## 8. Final render

Produced from the actual, current Fusion geometry (not a generated image) via
`mcp__fusion__fusion_mcp_execute`: applied a custom matte tan "stoneware" appearance (copied from
the Fusion Appearance Library's `Plastic - Matte (White)` base, recolored to a warm tan
consistent with `concept-v2.png` and the spec's matte/silk PLA / sanded-PETG material call) to
`urn-body` and `urn-lid` separately, assembled the lid onto the body at its true seated height
(160mm), set the Photo Booth lighting environment plus ground shadow/ambient occlusion, and
exported a hero-angle isometric shot at 1800×2000 directly from `Viewport.saveAsImageFile`.

Saved to: `H:\ClaudeStuff\3d-print-team\pet-memorial-urn\render\pet-memorial-urn-hero.png`

Honest caveat on the render itself: a faint background reference-grid/axis overlay is visible in
the image (a Fusion viewport-chrome element I could not fully suppress via the available API —
`SketchGridOff` and disabling ground-plane/canvas effects did not remove it). It does not affect
the model, material, or lighting shown, but it is not a fully "clean" studio backdrop — flagging
this plainly rather than presenting the image as more polished than it is.

**Concept-match note on the render specifically:** the render's overall silhouette and lid/handle
proportions match `concept-v2.png`'s spirit well. The one visible difference a careful side-by-side
would show is the same one named in §2 above — the built model's neck-to-collar area is a bit more
"banded" than the concept's fully continuous curve. This is disclosed here rather than left for
someone to discover only by comparing images later.

---

## Bottom line

**Approved.** The exported STEP/3MF/STL files for `urn-body` and `urn-lid` are geometrically
sound, independently re-verified against the spec and against the concept image using my own
methods (not a re-read of prior passes), and all three hard constraints (plain body, open-loop
handle, single-size) are confirmed true in the shipped files. Two required actions before this
project is fully "done" (neither blocks printing today):

1. **Add `README.md` and `parameters.md` at the project root**, matching this shop's convention
   for every other completed project — known limitations, print orientation, material reasoning,
   and a short parameter sheet with VERIFIED/DERIVED/ESTIMATED tags and revision history.
2. Delete the stray `pet-memorial-urn/nul` debug artifact.

Everything else (neck-fit-test physical validation, magnet fit coupons, manual slicer settings,
the minor neck-to-collar "banded rim" concept drift, the ~45.6° watch-item band) is a named,
non-blocking, carried-forward item — not a reason to withhold approval.

---
---

# ADDENDUM — 2026-08-27: third manual-edit incident, post-approval — re-confirmation

## Context

This project's original APPROVED verdict above was written by a prior Reviewer instance whose
transcript is no longer accessible. Since that approval, **a third manual/direct edit occurred
in the live Fusion document** (two others — a cross-component `participantBodies` leak and a
manual sketch-drag collapsing the neck profile — happened mid-pipeline, before the original
approval, and are already covered in the review above). This third incident: a user-described
edit "near the lid magnet pocket" turned out, on investigation, to have left the **lid entirely
untouched** — the actual damage was a manual drag on the **body's** neck/collar region (collar
ID/OD ballooned from 58mm/78mm to ~70.7mm/~90.4mm), which indirectly clipped the magnet pockets
down to abnormal ~3×1.9mm cuts as the growing bore ate into the 34mm pocket bolt circle. This was
not a delegated design change — it was treated as an unintended regression and recovered by
reproducing the exact previously-verified control-point/tangent recipe (this time `Revolve1`
picked up the corrected profile cleanly — no cascade rebuild of `Extrude1` was needed, unlike the
second incident).

The Tester independently re-verified this recovery against its own prior independent numbers
(not just the Coder's math) — see `tests.md` Re-test Pass 4 (R25-R29) and the corresponding
verdict in `verdict.md`. Per every number checked there, the recovered geometry matches the
pre-incident, already-approved state exactly or to within normal mesh-resolution noise, including
several genuinely bit-for-bit-identical floating-point figures (shell volume, face/vertex counts).

## My own independent spot-check (not accepted from the Coder/Tester chain alone)

I re-measured the current `stl/urn-body.stl` (freshly re-exported, timestamp 21:35) and
`3mf/urn-body.3mf` from scratch using my own `trimesh` script, cross-checked against the
untouched `stl/urn-lid.stl` (timestamp 12:01) as a control. Full results in my message to the
orchestrating agent; summary:

- **Manifold**: watertight, single component, Euler=2, bounds identical to every prior recorded
  state (±73.0mm XY, 0-160mm Z).
- **Shell volume**: 293.1365 cm³ — bit-for-bit identical to the Tester's R25 figure.
- **Face/vertex counts**: 47,298 / 23,651 — bit-for-bit identical to R25.
- **Belly apex**: exactly 73.000mm at z=72.0mm (45.00% of height) — exact match, after I
  independently hit and fixed the same local-frame-projection artifact that both the Tester (R2)
  and the original Reviewer (above, §2) separately flagged catching in their own scripts on this
  same geometry. A third independent party hitting and correcting the identical measurement
  pitfall is reassuring, not concerning — it confirms this is a known quirk of one specific
  technique on this curved geometry, not evidence of an actual defect.
- **Collar OD**: exactly 78.000mm at three sampled heights within the collar band. **Collar ID**:
  ~57.9-57.95mm (normal mesh-tessellation variance from the 58mm nominal).
- **Base cleanliness**: 77 vertices, all at exactly r=49.00mm, zero interior vertices — bit-for-bit
  identical to R25/R27, confirming the base-pocket defect from earlier in the project has not
  resurfaced.
- **Magnet pockets**: 3 pockets, bolt-circle radius exactly 34.000mm, diameter exactly 6.200mm,
  at 0°/120°/-120°, depth consistent with 2.2mm — exact match to R27, not the abnormal
  ~3×1.9mm cuts the incident produced.
- **Neck-to-collar blend**: smooth, gradually-changing slope across z=145-152mm with no
  discontinuous jump, anchor points exact (r=33.0000mm at z=145, r=39.0000mm at z=152) — consistent
  with R29, confirming the earlier collar-blend smoothness fix survived this recovery too.
- **Lid (control)**: watertight, 17,664 faces, bounds 100×100×75mm, 150.82 cm³, genuine open-loop
  handle confirmed via y-sweep — identical to every prior measurement, confirming it was genuinely
  untouched by this incident.
- **File timestamps**: `urn-body.*` fresh at 21:35; `urn-lid.*`/`neck-fit-test.*` unchanged at
  12:01/13:00 — consistent with the claimed incident scope.

I also confirmed the stray `pet-memorial-urn/nul` debug artifact (flagged as a minor hygiene item
in the original review, §5 above) has been deleted, and that `README.md`/`parameters.md` remain
in place and substantive.

## Determination: the original APPROVED verdict stands, unchanged

Every independently-checked figure matches the pre-incident, already-approved geometry exactly or
within normal mesh-resolution noise. This is not new geometry requiring a fresh review — it is a
faithful, independently-confirmed reproduction of the exact design this document already approved
above. None of the original approval's reasoning (business fit, technical parity, hard-constraint
compliance, documentation, cost) changes as a result of this incident or its recovery. The
**APPROVED** verdict at the top of this document stands as-is.

## Standing risk note, separate from the CAD verdict itself

This live Fusion file has now had **three manual/direct-edit incidents** across this project's
lifetime:

1. A scripted direct-BRep cut with an unset `participantBodies` property, leaking across
   components and producing stray base pockets (pre-approval).
2. A manual sketch-drag that collapsed the body's neck profile into a degenerate fragment,
   requiring a full profile/Revolve/Extrude rebuild (pre-approval).
3. A manual drag on the collar/neck region that ballooned the collar ID/OD and indirectly
   clipped the magnet pockets (post-approval, this addendum).

All three have been independently verified as fully recovered, with no residual damage found
anywhere checked, across three separate rounds of scrutiny. The recovery *process* on this
project is demonstrably working. But three incidents in one project's lifetime is a pattern, not
a coincidence, and it is worth flagging plainly for whoever edits this file next: **this document
and its predecessors' repeated recommendation stands** — prefer timeline-native, script-driven
parametric edits over direct manual dragging of sketch/BRep geometry in the Fusion UI for this
file, and if a manual edit is ever unavoidable, treat it as a higher-scrutiny change requiring an
explicit before/after geometry check (volume, face count, slope continuity), not a visual glance.
This is a file-handling/process risk, independent of and not a reason to revisit the CAD verdict
itself.

## Is the project's CAD work done?

**Yes**, modulo the same three non-CAD, requester-owned items already carried forward through
every prior pass and unaffected by this incident:

1. The physical neck-fit-test print-and-check (does a real remains bag pass through 58mm) —
   `neck-fit-test.*` files are confirmed untouched and still valid.
2. Magnet fit test coupons (PLA body, PETG lid) — never slicer-verified, unchanged status.
3. Manual slicer settings (layer height, infill, PETG-specific temps) — not embedded in any
   exported file, unchanged status.

None of these are CAD gates. The exported `step/`, `3mf/`, and `stl/` files for both `urn-body`
and `urn-lid` are geometrically sound, independently re-confirmed (again) to match the approved
design, and ready to print as-is.


---
---

# ADDENDUM 2 — 2026-08-28: magnet-assisted closure removed from CAD (targeted addendum, not a full re-review)

## Scope of this addendum

Per a direct request (relayed by `3d-director`, geometry side already settled through
Planner/Coder/Tester — see `specs.md` §6 v3 and `tests.md` Re-test Pass 5, R30-R34), the user
decided to remove the magnet-assisted lid closure entirely from the CAD. Both parts no longer
have any pre-modeled magnet pockets; the lid rests on the collar by flat-seating alone, and any
magnet assist the user wants is now their own print-time (slicer pause-and-embed) or post-print
(drill-and-glue) decision, outside this CAD. This addendum does not re-derive the geometry
conclusions from scratch — the Tester's Re-test Pass 5 is thorough and I did a quick corroborating
spot-check of my own (below) rather than a full independent re-analysis, per the scope requested.

**Quick corroboration (not a full re-derivation):** re-measured `stl/urn-body.stl` and
`stl/urn-lid.stl` directly — body remains watertight/single-component/Euler=2 with the same
bounds as every prior pass, and a sweep of the collar band (z=155-159.9mm) now shows exactly 2
boundary loops (outer wall + inner bore only) at every sampled height, versus the 5 loops
(outer + inner + 3 pockets) present in every pre-removal measurement — confirming the pockets are
genuinely gone, not capped over. Lid underside sweep (z=0-2.5mm) shows exactly 1 loop at every
height (plain flat plane, no pocket remnant), and the handle through-hole is unaffected
(2 loops from y=-4 to +4mm, 1 loop outside — same as every prior pass). This is consistent with
R30-R33 and gives me my own basis for the two points below, not just an inherited claim.

## 1. Business fit — re-confirmed PASS under flat-seating-only closure

My original "Business fit — PASS" finding (§1 above) cited "a magnet-assisted (not
airtight-dependent) closure appropriate for remains that are already bagged" as part of why the
design solves the stated problem. That specific mechanism is gone. Re-examining whether this
still holds:

- **The magnet assist was never load-bearing for the core business requirement.** The market
  research already on record in this project (cited in both `specs.md` §6 and my original
  review) established that no airtight seal is needed, because the crematorium's remains are
  already in their own sealed bag before they ever go in this urn. That finding is about the
  *seal*, not about the magnets specifically — a flat-seating lid was always functionally
  adequate for the actual containment requirement, independent of whether magnets existed. The
  magnets were an added "settled feel" nicety (per `specs.md` §6's original framing — "no airtight
  seal is needed... this is a 'settled feel' assist, not a latch"), not a functional requirement
  the business case depends on.
- **The approved concept brief itself never specifies a magnet closure at all.**
  `concept/brief.md` describes the lid as "domed, sized to seat on top of the neck opening" with
  the open-loop bail handle as "the key differentiating feature" — it says nothing about
  magnets, latches, or any closure hardware. The magnet-assist was a Planner-level spec addition
  (`specs.md` §6, made after the concept was approved), not something the signed-off concept
  itself promised. Removing it doesn't walk back anything the concept review approved.
- **The two features the concept brief does call load-bearing to the design's identity — the
  plain undecorated body and the open-loop lid handle — are both untouched by this change.**
  Independently reconfirmed above: handle through-hole still open, body still plain/smooth.
- **The removal is a legitimate, informed user decision, not a corner cut discovered after the
  fact.** The user explicitly chose to take on magnet placement themselves (pause-and-embed or
  drill-and-glue) rather than have it pre-modeled — this is a scope reduction the user asked for
  with a real alternative plan, not a silent regression the pipeline is asking me to wave through.

**Conclusion: business fit still holds.** The design continues to solve the stated problem (a
properly-sized, liftable-lid memorial urn for already-bagged remains) without the magnet
mechanism. Nothing the original approval actually depended on functionally has been undermined —
only a tactile nicety was removed, by the user's own informed choice, with a stated plan to
handle it outside the CAD if still wanted.

## 2. Correction to Addendum 1 (third manual-edit incident) — stale cross-reference fixed

Addendum 1 above (dated 2026-08-27, covering the third manual-edit incident) discusses the collar
magnet pockets as a present, currently-relevant feature (e.g. it describes the *legitimate*
collar/lid magnet pockets as intact and correctly restored after the incident, separately from
the unrelated *base-pocket defect* fixed earlier in the project). **That framing is now stale as
of this addendum's 2026-08-28 change**: the magnet pockets discussed there — both the body's
collar pockets and the lid's underside pockets — have since been intentionally and completely
removed from the current design, per `specs.md` §6 v3.

To be clear about what does and doesn't change as a result:
- **The third-incident history itself remains accurate and unchanged.** The incident happened,
  it was correctly diagnosed as a manual collar/neck drag that clipped the (then-still-existing)
  magnet pockets, and the recovery was correctly verified against the design as it existed at the
  time. None of that narrative is being rewritten.
- **What's stale is only the implication that the magnet pockets discussed in that addendum are
  still a current feature of the shipped design.** They are not — they were deliberately removed
  one day later, for unrelated reasons (a user preference to handle magnets outside the CAD), not
  because of any defect. Anyone reading Addendum 1 today should understand its magnet-pocket
  content as historical (accurate at the time it was written, describing a feature that has since
  been intentionally deleted), not as a description of the current print files.
- The **collar geometry itself** (78mm OD / 58mm ID, the neck-to-collar blend smoothness fix) that
  Addendum 1 also discusses is unaffected by the magnet-pocket removal and remains current and
  accurate — `specs.md` §6.2 v3 confirms the collar dimensions were explicitly held fixed even
  though its stated *purpose* changed from "magnet housing" to "reinforced seating band."

## Is `review.md` now internally consistent?

**Yes**, with this addendum in place. The original approval's business-fit and technical-parity
reasoning both still hold under the flat-seating-only closure (§1 above), and the one stale
cross-reference (Addendum 1's magnet-pocket discussion) is now explicitly flagged as describing a
since-removed feature rather than the current design (§2 above), without rewriting or discarding
that addendum's still-valid incident history.

## Final verdict

**Approval stands.** The removal of the magnet-assisted closure is a legitimate, user-driven
scope reduction that does not undermine any functional requirement the original approval actually
depended on, is consistent with the approved concept brief (which never specified magnets in the
first place), and has been independently verified (by the Tester in full, and by my own quick
corroborating spot-check above) as a clean, complete, regression-free removal on both parts.
`urn-body` and `urn-lid` remain approved and print-ready as currently exported. The same
non-CAD, requester-owned open items carried forward through every prior pass are unchanged: the
physical neck-fit-test bag check, and manual slicer settings. (Magnet fit test coupons are no
longer applicable, since there are no magnet pockets left in the CAD to test-fit against — this
item is now moot rather than open.)

---
---

# ADDENDUM 3 — 2026-08-28: capacity target change (~1477.8 cm³ → ~1579 cm³, +6.85%), fresh overhang re-check, render refresh

## Scope of this addendum

Per a direct follow-up request, this addendum covers three things prompted by `specs.md` v4 and
Tester `verdict.md` RE-TEST PASS 6 (the belly-fuller / wall-rebalance / neck-crease-fix round):
(1) a business-fit re-confirmation now that the built cavity volume has grown from the original
~1477.8 cm³ target to ~1579 cm³ — a change that explicitly crosses the spec's own ±5% tolerance
band (+6.85%), which the Tester correctly flagged as needing more than Coder-level sign-off;
(2) my own independent, from-scratch geometry spot-check of the current `urn-body` (not accepted
from the Coder/Tester chain alone); (3) a fresh overhang-angle check against the *current* belly
profile, since `specs.md` §9 explicitly disclosed that its overhang analysis was never recomputed
after the belly edit. This is a targeted addendum, not a full re-review — the geometry has already
been through multiple rigorous independent verification rounds (Tester RE-TEST PASSES 1–6, my own
Addenda 1–2 above), and nothing here reopens settled ground.

## 1. Independent geometry spot-check — my own measurement, live Fusion document, third independent method

I opened the live `pet-memorial-urn` Fusion document directly and wrote my own scripts against the
actual B-rep geometry (not the exported STL/3MF, and not a re-read of the Coder's or Tester's
numbers) — sampling the outer-wall and inner-wall NURBS faces directly via `Face.evaluator`, then
doing my own numerical revolution-integral for cavity volume. This is a **third independent
method**, distinct from both the Coder's Fusion mass-properties query and the Tester's mesh-based
integration:

| Check | My measurement (own method) | Coder | Tester | Agreement |
|---|---|---|---|---|
| Cavity volume | **1578.79 cm³** (direct integral of π·r(z)² over the sampled inner-wall profile, z=5–145mm, plus the exact bore cylinder z=145–160mm) | 1578.9824 cm³ | 1578.11 cm³ | Within 0.012% of Coder, 0.044% of Tester — solid |
| Belly apex (external radius) | **76.9659mm** at z=69.00mm | 76.97mm | 76.97mm | Exact match |
| Belly apex height | **43.12%** of 160mm (plateau spans z=66.9–71.4mm, i.e. 41.8%–44.6%) | ~43–44% (plateau) | ~43–44% (plateau) | Matches, confirms it's a genuine broad plateau, not a sharp point, at this same resolution |
| Wall thickness (belly/shoulder span) | **~4.000mm exactly** at every sampled height z=10–140mm | ~4.00mm (3.98–4.03mm) | ~4.00mm (3.98–4.03mm) | Matches, tighter than the claimed worst-case range at my sampling resolution |
| Material (shell) volume | **276.1556 cm³** (Fusion `physicalProperties.volume` on the live body) | 275.9651 cm³ | — | Within 0.07% |

I regard the cavity-volume match as the most meaningful confirmation here: three genuinely
different computational methods (Fusion's own mass-properties kernel, a mesh-integration on the
exported STL, and my own direct numerical integration of the sampled parametric surface) converge
on the same number to within four significant figures. **~1579 cm³ is not on shaky ground.**

## 2. Business fit — re-confirmed PASS, this is a *more generous* design, not a regression

Applying the same reasoning framework I used for the magnet-removal business-fit re-check
(Addendum 2, §1):

- The original ~1474.8/1477.8 cm³ figure was always framed as a **minimum**, not a fixed target —
  `specs.md` §4.1 derives it as `90 lb × 1 in³/lb`, explicitly choosing the top of the stated 50–90
  lb range because "oversizing capacity slightly is preferable to undersizing it for cremated
  remains." The new ~1579 cm³ figure, run back through the same rule the requester chose
  (`1579 cm³ ÷ 16.3871 cm³/in³ ≈ 96.3 in³ ≈ 96.3 lb` equivalent capacity), still describes a design
  comfortably serving the same "large, 50–90 lb" market segment — it does not push the product into
  a different weight bracket, misrepresent what it's for, or create a mismatch with a smaller/larger
  size in a lineup (this is explicitly the only size being built, §12).
- Nothing about the *shape* of the business case changed: this is still a single-size, large-pet
  urn, still with the same plain body and open-loop handle the concept brief calls
  load-bearing to its identity (both independently reconfirmed unaffected by this round — the belly
  edit and wall rebalance are internal-cavity/wall-thickness changes, not changes to the handle or
  the plain-body constraint).
- The mechanism by which this happened — a user-directed aesthetic choice (fuller belly, "kept
  intentionally") that had a volume side-effect the user then explicitly chose to accept rather
  than correct by thinning the wall — is a deliberate, informed tradeoff, not a defect discovered
  after the fact and rationalized. This is the same category of legitimate, disclosed scope
  decision as the magnet-removal round, just running in the opposite direction (adding capacity
  instead of removing a feature).
- **This does cross the spec's own ±5% routine-tolerance threshold**, which is exactly why
  `specs.md` was correctly bumped to a formal v4 revision rather than left as an informal
  Coder/Tester understanding — I agree with the Tester's judgment call that this warranted a
  written revision and a fresh business-fit look, and I'm making that look now rather than treating
  "the user already said it's fine informally" as sufficient on its own.

**Conclusion: Business fit — PASS, re-confirmed.** The original "Business fit — PASS" section at
the top of this document (§1) is updated by this addendum: the design's capacity is now ~1579 cm³
against the original ~1477.8 cm³ minimum target, a **deliberate, accepted, +6.85% increase in
generosity**, not a shortfall — the design continues to solve the stated problem for the same
50–90 lb target market, arguably with more safety margin against undersizing than the original
number carried.

## 3. Fresh overhang-angle check against the *current* (post-belly-edit) profile

`specs.md` §9 explicitly flagged that its overhang analysis was computed against the **pre-v4**
profile and never recomputed against the fuller/repositioned belly — the Planner and Tester both
named this as an open gap rather than silently carrying old numbers forward. I did the fresh check
directly on the live geometry rather than requiring another Tester round-trip, per the specific
request to fold this in:

**Method:** sampled the *entire* outer-wall surface continuously from z=0 (base) to z=160mm (rim)
— stitching together all four outer-wall face patches (`Body5` faces 7, 8, 9, 10, which together
span base→belly→shoulder→neck-taper→collar-blend→collar-cylinder) at sub-millimeter resolution,
computed local `dr/dz` at every step, and searched the **whole span** for any zone where the local
angle from vertical exceeds the 45° self-supporting guideline — not just re-checking the
previously-known trouble spot.

**Findings:**

- **The only zone anywhere on the entire outer wall exceeding 45° is the already-known, already-
  disclosed neck-to-collar external blend (z≈145–152mm).** Peak local angle there is now
  **47.25° at z=147.25mm** — about 1.6° higher than the ~45.6° figure reported for the pre-v4
  profile, but the same location, the same already-disclosed "watch it on the first print" zone
  (a few degrees over the guideline, on a short span of a fully closed 360° revolve), not a new
  concern and not a new site. `specs.md`/`parameters.md` should be updated with this refreshed
  number, but I don't think this needs a fresh Tester pass — it's the same disclosed risk,
  quantitatively confirmed, not a new one.
- **The belly region itself — both the base-to-belly flare (P0→apex) and the belly-to-neck-taper
  descent (apex→P3) — remains entirely in the self-supporting "shrinking/growing-monotonically"
  class.** I checked this directly rather than assuming it still holds on the new, bigger belly:
  - Base→apex (z=0–69mm): **zero locally-decreasing radius steps** across 1,382 sampled steps —
    genuinely monotonic non-decreasing, confirming the outward flare never reverses.
  - Apex→neck-taper-end (z=69–145mm): local angle stays negative (radius shrinking) at virtually
    every sampled point; the only positive-angle noise found (123 of 2,016 steps, max **0.409°**)
    sits at floating-point/sampling-noise level, concentrated right at the broad, nearly-flat belly
    plateau where the profile is *supposed* to be near-zero slope — this is not a real reversal,
    and it's two orders of magnitude below anything that would matter for print behavior.
  - This confirms the project's standing "shrinking-cone, self-supporting regardless of local
    angle magnitude" argument holds exactly as well on the current, fuller/lower belly as it did
    on the pre-edit profile — the belly getting bigger and moving slightly lower did **not**
    introduce a new overhang risk anywhere in this region.
- **Documentation discrepancy found in the process (not a geometry defect):** `specs.md` §4.3's
  shoulder OD row (122mm OD / 61mm radius at z=119mm) — which the spec itself already flagged as
  "not independently re-verified... may be stale" — **is confirmed stale by my direct
  measurement.** The actual current radius at z=119mm is **46.42mm (≈92.8mm OD)**, roughly 30mm of
  diameter off from the documented figure. This doesn't change any pass/fail conclusion (cavity and
  material volumes were verified directly via mass-properties, not derived from this figure), but
  it should be corrected in the next documentation pass so nobody designs against the stale number.

**Conclusion: no new problematic overhang was introduced by the v4 belly edit.** The body's
base-down print orientation remains sound; the one elevated-angle zone is the same one this
project has tracked since the collar-blend fix, marginally higher but not qualitatively different.
This is a manufacturability question I was able to close out directly from the live geometry —
I don't think it needs a dedicated Tester round-trip, but flagging that judgment call explicitly
per the request, in case the director wants a second, independent confirmation anyway given this
project's history of needing extra scrutiny in exactly this body region.

## 4. Incidental finding, fixed: body appearance had silently reverted to a default material

While setting up the render (below), I found `urn-body`'s `Body5` was displaying the default
**"Steel - Satin"** appearance rather than the custom **"Matte PLA - Stoneware Tan (urn-body)"**
appearance used in the original hero render — almost certainly a side effect of the `Revolve1`
recreation during this round's belly/neck work resetting the body's appearance override. The
correct custom appearance was still defined in the document (untouched), just not applied to the
current body. **I reapplied it and saved the document.** This is not a geometry defect and has no
bearing on the printed part, but it would have caused any future render or visual QA pass to show
the wrong (generic gray-steel) material look despite `specs.md`/`README.md`'s material recommendation
being unchanged — worth knowing about since this is the second time in this project that a
timeline-native rebuild has silently reset something adjacent to the geometry it touched (the
first being the `participantBodies` default itself, back in the original defect).

## 5. Documentation currency — real gap, required follow-up (same category as the original review's finding)

**`README.md` and `parameters.md` at the project root have not been updated to reflect `specs.md`
v4.** Both still describe the pre-v4 state throughout:

- `README.md` states "≈1512 cm³ (≈92 in³) internal capacity" — the actual current figure is
  ≈1579 cm³ (≈96.3 in³).
- `parameters.md` §1's body table still lists "External belly max OD: 146mm (r=73mm)" and
  "Internal cavity volume: 1511.8 cm³" — both superseded by the current 76.97mm-radius belly and
  ~1579 cm³ cavity. There's no mention anywhere in either document of the belly-fuller edit, the
  inner-wall rebalance to a constant ~4mm offset, or the neck-to-collar crease repair — all three
  of which are now fully documented in `specs.md` v4 but not propagated to the two documents this
  shop's own convention says a future editor or the requester would actually reach for.

This is the same category of finding as my original review's §5 (documentation lagging the
as-built design), just recurring: the pipeline is doing excellent work keeping `specs.md`/
`tests.md`/`verdict.md` current and rigorous, but the lightweight top-level docs are drifting out of
sync after a material design change, again. **Required follow-up before this project is called
fully "done" a second time** — not a print blocker (the exported STEP/3MF/STL files are correct
and reflect the current geometry; only the human-readable summaries are stale).

## 6. Cost — re-confirmed PASS, and this round is actually a mild cost *improvement*, not a tradeoff

Despite the +6.85% larger cavity, the body's actual material (shell) volume **decreased** slightly,
from ~293.4 cm³ (pre-v4, post-magnet-removal figure) to **~276.16 cm³** (my measurement, matching
the Coder's 275.9651 cm³) — the reshaped profile (fuller belly, but a shoulder-to-neck taper that
now converges noticeably faster) uses somewhat less total wall material overall despite enclosing
more internal volume. At the same PLA/PETG pricing basis used in the original review (§6), this
is, if anything, a fractionally cheaper body than before, not a more expensive one. **Cost verdict
unchanged: trivially cost-effective, ~$8–12 in filament for the pair**, and this round's design
change improves rather than worsens that number.

## 7. Render — refreshed to reflect the current, final geometry

The existing hero render (`render/pet-memorial-urn-hero.png`, produced 2026-08-27) predated this
round's belly/wall/neck-crease edits and no longer depicted the shipped design (it showed the
pre-v4, ~73mm-radius belly). Since a materially different silhouette is now the actual product,
I produced a fresh render from the live, current Fusion geometry rather than leave a stale image
as the project's "final" preview:

- Fixed the body's reverted appearance (§4 above) and confirmed the lid retains its correct
  **"Matte PETG - Stoneware Tan (urn-lid, sanded)"** appearance.
- Temporarily raised the lid occurrence to its true seated height (160mm) and made it visible for
  the render only, then **reverted both changes** afterward (transform back to identity, visibility
  back to hidden) so the live working document isn't left in a staged/assembled state — the only
  permanent change saved to the document is the appearance fix, which is a genuine correction.
- Confirmed the Photo Booth lighting environment (used in the original render) was already active,
  disabled the sketch grid, and captured an isometric hero angle via `Viewport.saveAsImageFile`
  directly from the API (the real geometry, not a generated image).
- Saved to `render/pet-memorial-urn-hero.png` (replacing the stale image); the pre-v4 render is
  preserved, not deleted, at `archive/pre-v4-belly-render/pet-memorial-urn-hero.png` for reference.
- **Same honest caveat as the original render:** a faint background reference-grid overlay is still
  visible and could not be fully suppressed via the available API — this is a rendering-tool
  limitation, not a model defect, consistent with what the original Reviewer found and disclosed.

## 8. Concept-fidelity check on the refreshed render — a real, incremental drift worth naming, not silently waved through

Comparing the new render directly against the approved `concept/concept-v2.png`, per the specific
instruction to flag (not silently approve) if the built design has drifted from what was actually
signed off on visually:

**The built design's belly-to-neck proportions are now noticeably more pronounced/pinched than the
concept image's considerably gentler taper.** `concept-v2.png` shows a wide-mouthed, gradually
tapering pot — the belly-to-opening width ratio is modest, and there's no sharp constriction
anywhere in the silhouette. The shipped design already had a narrower neck/collar than the concept
for a disclosed, functional reason (the reinforced lid-seating band, named as the "banded rim"
drift in my original review, §2), and the v4 belly enlargement (73mm→76.97mm external radius) has
widened that gap further by making the belly comparatively even bigger relative to the same-sized
neck/collar. The current render reads more like a rounded "ginger jar" silhouette with a distinct
shoulder pinch than the concept's smoother, more gradual vase shape.

**I'm naming this plainly rather than either blocking on it or silently letting it pass:**

- This is not a pipeline error or an undisclosed drift — the user directed this exact change with
  full awareness of its visual consequence (`specs.md` §4.1: "a deliberate aesthetic decision, not
  a defect... the user explicitly chose to keep it rather than revert").
- The concept brief's own words — "wider through the belly, tapering inward to a narrower neck" —
  are, if anything, *more* true of the current shape than of the original concept photo; this
  reads as an intensification of the same design language, not a departure into a different one.
- The two features the concept brief explicitly calls load-bearing to the design's identity (the
  plain undecorated body, the open-loop bail handle) are both fully intact and correctly
  proportioned in the current build, independently reconfirmed above and in prior passes.
- That said, "more pronounced than what was actually shown in the signed-off image" is a real,
  cumulative visual gap (on top of the already-disclosed banded-rim drift), not a null finding —
  **I'd recommend a quick, low-stakes visual check-in with the requester** (a side-by-side glance
  at the new render vs. `concept-v2.png`) before this is treated as fully final, purely as a
  courtesy confirmation that the more-bulbous look still reads as "right" to them now that it's
  built, not because I think the geometry needs to change.

## Final verdict for this addendum

**Approval stands.** Business fit is re-confirmed under the new ~1579 cm³ capacity (more generous,
not a regression) — the original "Business fit — PASS" conclusion at the top of this document is
hereby updated to reflect this. My own independent, from-scratch geometry spot-check (a third
method beyond the Coder's and Tester's) confirms the cavity volume, belly apex, and wall thickness
figures in `specs.md` v4 are solid. The fresh overhang-angle check requested against the current,
post-belly-edit profile found **no new problematic overhang anywhere** — the one elevated-angle
zone is the same previously-disclosed neck-to-collar blend, marginally higher (47.25° vs. ~45.6°)
but not a new site or a new category of risk; I don't believe this needs a dedicated Tester
round-trip, though the director may want one anyway given this body region's history. Two real,
non-blocking follow-ups are carried forward: **(1)** `README.md`/`parameters.md` need updating to
the v4 figures (capacity, belly OD, the three v4 edits) — required before the project is called
fully documented, not before it can be printed; **(2)** a quick requester visual check-in on the
now-more-pronounced belly-to-neck proportions vs. the originally approved concept image, as a
courtesy confirmation rather than a rework requirement. The refreshed hero render at
`render/pet-memorial-urn-hero.png` now depicts the actual, current, final geometry — the previous
render is preserved at `archive/pre-v4-belly-render/pet-memorial-urn-hero.png`. `urn-body` and
`urn-lid` remain approved and print-ready as currently exported.


---
---

# FULL RE-REVIEW — 2026-08-31: v5 major revision (neck/collar widened 58mm→80mm ID, height trimmed 160mm→153.5mm, lid resized brim+22%/dome+21%)

## Why this gets a full pass, not another addendum

I agree with the Tester's routing recommendation and the director's framing. My prior three
addenda (2026-08-27/28) were each scoped to a single, contained change layered on an already-
approved base (an incident recovery, a subtractive feature removal, a capacity-drift
consolidation). This revision is different in kind: it rewrites the spec's single most-discussed
named risk (the neck opening, flagged `ESTIMATED`/untested since v1) based on genuinely new market
research — a business-fit judgment call, not a dimensional correction — and it reworks the lid's
two headline dimensions by 21–22%, which `specs.md` itself describes as "shown with the same rigor
as the original lid derivation, not a cosmetic pass." Height, neck ID/OD, collar ID/OD, and both
lid headline dimensions all moved in the same pass. That's a second-original-build footprint, and
it gets reviewed like one below: business fit, concept fidelity, hard constraints, my own
independent geometry spot-check, documentation, and cost — each addressed fresh, not inherited.

**What is not being re-litigated:** the belly-fullness/wall-rebalance saga (v4, addressed in
Addendum 3), the magnet-pocket removal (v3, Addendum 2), and the three earlier manual-edit
incidents (Addendum 1) are settled ground. Nothing in v5 touches the belly's shape or the magnet
question, and I did not re-open them.

## 1. Business fit — the neck-widening judgment call — PASS, a well-reasoned, genuine de-risking, correctly not oversold as a full resolution

This is the question the director specifically asked me to make a judgment on, not just measure.

**The problem being solved is real and was correctly identified.** The 58mm ID has been an
`ESTIMATED`, physically-untested named risk since v1 of this spec — never closed out, only ever
carried forward with a test article that (until this revision) nobody had reason to believe was
actually going to pass. The new competitor research changes that from "an untested assumption we
hope is fine" to "an untested assumption we have good outside reason to think was probably too
small." Comparable ceramic pet urns running 114–121mm openings, and even a direct 3D-printed
competitor estimated at 70–100mm, both sit well above 58mm — that's not a marginal miss, it's a
significant outlier, and market benchmarking is exactly the right tool to catch it (a dimension
like this was never going to be validated by CAD review alone).

**80mm is a defensible, honestly-characterized compromise, not the strongest possible choice —
and the spec is right not to oversell it.** Two things I weighed independently rather than
accepting the spec's own framing at face value:

- 80mm sits at the **low end** of the cited 3D-printed-competitor range (70–100mm) and well below
  the ceramic-competitor range (114–121mm). If I were optimizing purely for bag-fit risk reduction,
  I'd have leaned closer to 100mm. The spec is transparent about this trade-off (§4.2.2, §4.4) —
  it explicitly frames 80mm as "a deliberate compromise short of the full 100mm initially
  considered," not as "the number the research says is safe." I agree with that framing; I would
  push back if the spec had instead presented 80mm as fully validated by the competitor data,
  which it does not.
- The stated reason for stopping at 80mm — keeping the collar OD (100mm) from exceeding the base OD
  (98mm) — is a real, coherent identity/proportion concern, not an arbitrary line. A collar wider
  than the base would invert the vessel's visual hierarchy (the belly is supposed to be the widest,
  most dominant feature of a "ceramic vase" silhouette per the concept brief) and would very likely
  read as top-heavy or unstable-looking regardless of whether it's structurally fine. Trading some
  bag-fit margin for base-vs-collar identity preservation is a legitimate business/design call, and
  100mm-vs-98mm is a sensible place to draw that line (rather than, say, letting the collar reach
  110–120mm to hit the ceramic-competitor range and only then discovering the proportion problem
  after the fact).

**My own independent visual check on the base-vs-collar proportion (not just accepting R52):** I
took a fresh screenshot of the current live geometry (below) — the belly remains unambiguously the
widest, most visually dominant feature of the silhouette; the base and the now-100mm collar read as
comparably narrow bookends at each end, not top-heavy. I agree with the Tester's R52 conclusion,
reached independently rather than rubber-stamped.

**Where I land:** this is a **PASS** as a business-fit judgment call — it's a genuine, evidence-
based improvement over 58mm, reasoned honestly about its own limits, and it doesn't trade away the
vessel's core visual identity to get there. But I want to state plainly, in my own words rather
than deferring to the spec's own self-assessment: **80mm meaningfully reduces the risk, it does not
retire it.** It is still below every cited real-world comparable except the low end of one
estimated range. The `neck-fit-test` article (now correctly rebuilt at 80mm, independently
confirmed below) is not a formality here — it is the one piece of validation that actually matters
for this specific business decision, more so than for any other named risk this project has
carried. **I'd treat "has the requester actually printed and tried a real or mocked bag through the
new 80mm test article" as the single most important open item coming out of this review** — more
important than it was before this revision, because this revision's entire justification rests on
an assumption about bag size that remains unverified.

## 2. Concept fidelity — independent visual comparison against `concept-v2.png` — no new meaningful drift; the neck/opening change is, if anything, a partial correction, not an addition, to prior drift

The director specifically asked whether this round reads as a bigger step away from the approved
concept than prior rounds, given the already-disclosed "banded collar" (v2/v3) and "ginger jar
belly pinch" (v4) drift. I did this by rendering the current, live v5 geometry fresh (not reusing
the v4 render) and comparing it directly against `concept-v2.png`, the same way I did after v4.

**Render:** appearances were already correctly set on both bodies (the "Matte PLA - Stoneware Tan"
/ "Matte PETG - Stoneware Tan" custom appearances survived this round's rebuild, unlike v4's
incidental appearance reset — nothing to fix this time). I temporarily raised the lid to its new
153.5mm seated height, captured an isometric hero angle via `Viewport.saveAsImageFile`, then
reverted the staging transform/visibility back to what I found. Saved to
`render/pet-memorial-urn-hero.png` (the v4-era render is preserved at
`archive/pre-v5-neck-widening-render/pet-memorial-urn-hero.png`).

**My assessment, point by point:**

- **The wider neck/collar moves the design closer to the concept's proportions, not further away.**
  Eyeballing `concept-v2.png`, the concept's opening reads as a fairly generous fraction of the
  belly's max width — nowhere near as pinched as a classic "ginger jar." The pre-v5 collar
  (78mm OD against a 153.9mm belly, ≈51% ratio) was noticeably narrower relative to the belly than
  the concept shows. The new 100mm collar against the same 153.9mm belly is ≈65% — still narrower
  than the concept's apparent proportions, but a real, substantial step in the concept's direction,
  not away from it. If anything, this revision **partially corrects** the belly-to-neck pinch that
  the v4 belly-fullness edit introduced, rather than compounding it.
- **The shoulder-to-neck-taper transition reads visibly smoother in the new render.** This tracks
  the structural finding in §3 below (the external radius delta across this span shrank from
  13.4mm to 2.4mm) — a gentler, more continuous-looking curve there, closer to the concept's
  smooth single-curve silhouette than the old, more abrupt version.
- **The "banded," constant-radius collar band itself is unchanged in kind** — it's still a distinct
  15mm cylindrical section, just larger in absolute terms (100mm vs. 78mm OD) than before. This is
  the same disclosed, functionally-justified drift named in my original review and in Addendum 3
  (the reinforced lid-seating band the concept's continuous neck curve doesn't show) — growing it
  doesn't newly introduce this departure, and I don't think it makes it meaningfully more
  noticeable either; it's the same visual "character," just re-scaled.
- **The lid's brim now overhangs far more dramatically in absolute terms** (11mm/side margin is
  unchanged as a *design choice*, but the brim itself grew from 100mm to 122mm) — in the fresh
  render this still reads as a plausible, deliberate "cap" proportion, not oversized or cartoonish;
  the dome-to-brim ratio was deliberately held at 0.80, the same ratio the original (approved-by-
  implication) v1–v4 lid used, so the lid's own internal proportions didn't change, only its
  absolute scale relative to the now-larger collar it has to cover.

**My conclusion, stated plainly per the director's specific ask:** I do **not** think this round
adds meaningfully more cumulative concept drift than the prior (v4) round did — on the single
dimension most visible in a side-by-side comparison (how pinched the neck looks relative to the
belly), this revision is a partial improvement, not a further departure. The design is still
"recognizably the approved concept" — same plain body, same open-loop handle, same general
low-belly silhouette — with the same one disclosed structural departure (the banded collar/rim)
now simply larger. I'm not blocking on this, and I don't think it needs to be flagged as "bigger
than prior rounds" the way the director's question raised as a possibility — my independent read is
the opposite of that concern, though I understand exactly why the question was worth asking given
how large the absolute numbers moved.

**Courtesy check-in — renewed, not new:** I recommended a quick visual check-in with the requester
after v4 (comparing the fuller belly against `concept-v2.png`). That recommendation was not
resolved before this v5 round shipped (there's no record of it happening in `tests.md`/`verdict.md`
between then and now). Two rounds of aesthetic change have now accumulated since the last time the
requester actually looked at a render side-by-side with the concept. **I'm renewing this
recommendation, not dropping it** — a quick "does the current build (render attached) still look
right to you against the original concept image" check is cheap and would close out two rounds of
carried-forward uncertainty at once, especially now that my own read is reassuring rather than
alarming.

## 3. My own independent geometry spot-check — third method, live Fusion document, not the Coder/Tester chain

I wrote fresh scripts against the live `pet-memorial-urn` document's actual B-rep geometry
(sampling the outer/inner NURBS faces directly via `Face.evaluator`, plus a direct
`BRepBody.pointContainment` query for the handle — a different, more direct method than the mesh
cross-section sweep Coder/Tester both used for that specific check).

| Check | My measurement | Coder | Tester | Agreement |
|---|---|---|---|---|
| Cavity volume | **1580.2542 cm³** (own numerical revolution-integral) | 1580.25 cm³ | 1579.31 cm³ | Essentially identical to Coder, within 0.06% of Tester |
| Belly apex (external radius / height) | **76.9660mm at z=69.076mm** (45.00% of 153.5mm) | 76.966mm / z≈69.11mm | 76.964mm / z=69.0mm | Exact match — confirmed genuinely unmoved by the height trim |
| Shoulder (P2) ext/int radius, z=112.5mm | **46.4200mm / 42.4200mm** | 46.42mm / 42.42mm | 46.420mm / 42.420mm (upgraded from `ESTIMATED`) | Exact |
| Neck-taper-end (P3) ext/int radius, z=138.5mm | **44.0000mm / 40.0000mm** | 44mm / 40mm | 44.000mm / 40.000mm | Exact |
| Collar (P4 band) ext/int radius | **50.0000mm / 40.0000mm**, constant z=145.5–153.5mm | 50mm / 40mm | 50.000mm / 40.000mm | Exact |
| Base OD | **98.00mm** (r=49mm, face area 75.43cm² = π·49² exactly) | 98mm | 98mm | Exact |
| Internal floor radius | **45.0000mm** (face area 63.62cm² = π·45² exactly) | 45mm (implied) | not separately reported | Exact, independent confirmation |
| Handle through-hole | **Genuine open air confirmed by direct point-containment query** at (0,0,46/50/58mm) — `PointOutsidePointContainment` at all three; solid material confirmed inside both legs at (±18,0,48mm) — `PointInsidePointContainment` | 22×24mm, unaffected by scale | 22×24mm, y=−4 to +4mm | Confirmed by an independent method (solid-body point-containment, not a mesh cross-section sweep) — arguably a more direct test of "is this really open" than a boundary-loop count |
| Neck-to-collar blend peak angle | **46.41° at z=141.9mm** (0.1mm-binned scan) | 45.81° | 45.56° (bit-identical to pre-widening v4 blend) | Same zone, same low-risk band; the ~0.6–0.9° spread across three independent methods is consistent with this project's normal sampling/binning variance, not a real disagreement |
| Overhang, full outer wall | Only zone >45° anywhere on the entire 0–153.5mm span is the known neck-to-collar blend (z≈140.6–143.4mm) | — | Confirmed monotonic elsewhere | Confirms no new overhang risk introduced anywhere else |
| Lid brim OD | **122mm** (bounding box ±61.0mm at z=0) | 122mm | 122.00mm | Exact |
| Lid dome base OD | **~97.2mm** (r=48.61mm at the brim-fillet/dome handoff, z≈7.65mm) | ~97.2mm | ~97.3mm | Matches within 0.1mm |
| Component count | 3 (`urn-body`, `urn-lid`, `neck-fit-test`) | — | — | Confirms §12's single-size constraint still holds, no scope creep |

I regard the point-containment handle check as a genuine methodological addition, not just a
repeat of the prior mesh-sweep check: it directly asks the CAD kernel "is this point inside solid
material or not" at the exact center of the claimed opening (and, as a control, inside both legs
and inside the dome), which is about as direct a test of "is this actually a through-hole" as is
available short of a physical print. It came back exactly as expected at every sampled point.

**On the ~1° spread in the neck-to-collar blend angle across three independent methods:** I don't
think this represents any real disagreement about the geometry — it's the same pattern seen
throughout this project (e.g., the original Reviewer and Tester have each independently measured
slightly different peak angles for this same feature in prior rounds, always within about a degree
of each other, always attributable to sampling resolution/binning choices on a continuously curved
surface). The genuinely load-bearing fact — that this is the same disclosed, low-risk "watch it on
the first print" zone, not a new or worse one — is confirmed by all three methods in agreement.

## 4. Hard constraints — reconfirmed, none touched by this revision's scope

1. **Plain/smooth body, no engraving.** Untouched by v5's scope (neck/collar/height/lid only); my
   own face enumeration of the rebuilt body shows the same clean set of rotationally-symmetric
   revolve/cylinder/plane faces as every prior pass, no new features anywhere on the body's outer
   surface. **Confirmed by scope, not re-derived from scratch** — there was no plausible mechanism
   for this constraint to have been affected by a neck/collar/height change, and the geometry
   inspection above didn't turn up anything on the outer wall besides the expected revolve faces.
2. **Handle is a genuine open through-hole loop.** Directly reconfirmed above via point-containment
   query — the more rigorous of the two methods available, not just re-accepted from the mesh
   sweep. **Confirmed.**
3. **Single-size build, no variant scope creep.** The live document still contains exactly 3
   components. **Confirmed.**

## 5. Documentation — the same gap I flagged after v4, now worse and more urgent

I flagged after v4 that `README.md`/`parameters.md` had not been updated to the v4 figures. **That
follow-up did not happen before v5 shipped, and v5 has now moved past those documents by a second,
larger margin.** I checked both files directly against the current, verified-above v5 geometry:

- `README.md` still states the neck opening is 58mm (now 80mm), the body height is ~160mm (now
  153.5mm), the collar is 78mm OD (now 100mm), and the brim is 100mm (now 122mm) — every one of
  these appears in prose the requester would plausibly read at face value (e.g., "print this first
  to physically check a real crematorium remains bag fits through **the 58mm neck opening**" —
  §Files table).
- `parameters.md`'s entire body/lid parameter tables are still the pre-v4 *and* pre-v5 numbers in
  most rows (158mm height, 58mm neck ID, 78mm collar OD, 100mm brim) — none of the v5 §4.2.2
  re-derivation is reflected anywhere in this document.

**Why I'm treating this more seriously than the equivalent v4 finding:** this is no longer just
"the docs are one revision behind the CAD" — it's now two revisions behind, and the specific gap
(58mm vs. 80mm neck) is the exact number this whole revision exists to fix. A requester who reads
only `README.md`'s instruction to test "the 58mm neck opening" and then prints the (correctly
rebuilt, 80mm) `neck-fit-test` article would be confused about which number they're actually
validating — not a safety issue (the physical files are correct), but a real, avoidable
documentation-trust problem that compounds every round it's deferred. **This remains non-blocking
for printing** (the exported STEP/3MF/STL files are correct and reflect the current v5 geometry,
confirmed independently above), but I'm flagging it more emphatically this time: **this should not
be allowed to reach a third stale revision.**

## 6. Cost — still comfortably cost-effective in absolute terms, but this round is a real, double-digit cost increase, driven almost entirely by the lid — worth stating plainly rather than reflexively repeating "trivially cost-effective"

Material (shell) volumes, measured directly from the live model:

| Part | v4 material volume | v5 material volume | Change |
|---|---|---|---|
| Body | ~276.16 cm³ | **278.94 cm³** | +1.0% (larger collar wall at a bigger OD) |
| Lid | ~151.0 cm³ | **219.20 cm³** | **+45.2%** (brim +22%/dome +21% linear growth compounds substantially in volume) |

At PLA (~1.24 g/cm³) and PETG (~1.27 g/cm³) densities: body ≈346g (~$7–8.7 at typical filament
pricing), lid ≈278g (~$5.6–7). **Combined pair: roughly $12.5–16**, up from the ~$8–12 figure
carried in every prior pass of this review. This is still a small, entirely reasonable cost for a
decorative memorial piece — I'm not flagging this as a problem — but the lid alone grew by nearly
half its material volume, and repeating "trivially cost-effective" without naming that specific,
real increase would understate what actually changed. **Cost verdict: PASS, with the increase
named plainly** rather than silently absorbed into an unchanged-sounding conclusion.

## 7. Final render

See §2 above for the render methodology. Saved to
`H:\ClaudeStuff\3d-print-team\pet-memorial-urn\render\pet-memorial-urn-hero.png` (current v5
geometry, matte stoneware appearances on both parts, Photo Booth lighting, isometric hero angle,
lid shown seated at its true 153.5mm height). The v4-era render is preserved at
`H:\ClaudeStuff\3d-print-team\pet-memorial-urn\archive\pre-v5-neck-widening-render\pet-memorial-urn-hero.png`.
Same honest caveat as every prior render in this project: a faint background reference-grid overlay
remains visible and could not be fully suppressed via the available API — a rendering-tool
limitation, not a model defect.

## Final verdict

**APPROVED, with named watch-items — not blocked, and not a rubber stamp.**

- **Business fit (the neck-widening decision):** PASS. A genuine, evidence-based, honestly-
  characterized de-risking of this project's longest-standing named risk, with a coherent
  proportion-preservation rationale for stopping at 80mm rather than 100mm. It reduces the risk,
  it does not retire it — the physical `neck-fit-test` print-and-check is more important now than
  it has ever been in this project, since this revision's entire premise rests on it.
- **Concept fidelity:** PASS. Independently compared against `concept-v2.png` from a fresh render —
  no meaningful new drift; the wider neck/gentler shoulder-taper is, if anything, a partial
  correction of the v4 belly-pinch drift, not an addition to it. The banded-collar departure
  persists unchanged in kind, just at a larger absolute scale. A courtesy visual check-in with the
  requester is renewed (not new) given two rounds of accumulated change since one last happened.
- **Independent geometry spot-check:** PASS on every checked dimension (cavity volume, belly apex,
  shoulder/neck/collar radii, base/floor radii, handle integrity via a more direct method, overhang
  angles) — confirmed via my own third method, not accepted from the Coder/Tester chain.
- **Hard constraints:** all three intact, confirmed.
- **Documentation:** real, worsening gap — `README.md`/`parameters.md` are now two revisions stale
  and contain the exact number (58mm neck) this revision exists to fix. Non-blocking for printing,
  but should not be deferred a third time.
- **Cost:** PASS, with a real ~30–40% increase in combined material cost named plainly (driven
  almost entirely by the lid's resize) rather than reflexively restated as unchanged.

`urn-body`, `urn-lid`, and `neck-fit-test` remain approved and print-ready as currently exported.
The single most important next step, more so than in any prior pass of this project, is the
requester actually printing and testing the rebuilt `neck-fit-test` article against a real or
mocked remains bag — this revision's central business decision is sound reasoning applied to real
market data, but it is still, honestly, an estimate until that physical test happens.


---
---

# ADDENDUM 4 — 2026-09-01: v6 candidate, lid-underside alignment plug (targeted addendum, not a full re-review)

## Scope of this addendum

I picked this up cold after the prior Reviewer session expired. Per the routing recommendation
in `tests.md` RE-TEST PASS 8 / `verdict.md` (which I agree with, independently, having read the
full v5 full-re-review above first for context): this is a purely additive change — a straight
cylindrical alignment plug added to the lid's underside (79.5mm OD × 10mm deep, hollow, 4.0mm
wall, 0.5mm diametral clearance against the body's 80mm bore) — that does not touch the neck,
collar, belly, height, handle, or any previously-reviewed dimension or business-fit judgment.
`urn-body` and `neck-fit-test` are confirmed untouched (file timestamps: both dated 2026-08-31,
matching the v5 round exactly; only `urn-lid.step/.3mf/.stl` carry a fresh 2026-09-01 timestamp).
This gets a targeted look, not the full-pass treatment the v5 revision got.

## 1. My own independent spot-check — not accepted from the Coder/Tester chain alone

I wrote my own `trimesh` script against the actual shipped `stl/urn-lid.stl` and `stl/urn-body.stl`
(a fourth independent method on this project, after the Coder's/Tester's/my own prior passes),
rather than re-reading `tests.md` R53–R60 and taking the numbers on faith:

| Check | My independent measurement | Tester (R53–R60) | Match |
|---|---|---|---|
| Lid manifold/watertight, bounds | Watertight, Euler=0, bounds z=0–85mm | Watertight, Euler=0, z=0–85mm | Exact |
| Body manifold/watertight, bounds | Watertight, bounds z=0–153.5mm | Watertight, z=0–153.5mm (unaffected) | Exact |
| Plug wall (outer/inner radius) | **39.750mm / 35.750mm**, constant 4.000mm wall at every sampled height 0–9.9999mm | 39.750mm / 35.750mm, 4.000mm constant | Exact |
| Internal bridge cap location | Interior loop (hollow) present at every z up to **9.9999mm**; at **z=10.0000mm exactly**, the interior loop vanishes and the cross-section becomes fully solid to r=61mm | Same transition, same z=10.00mm | Exact |
| Bridge diameter | **71.500mm** (2× 35.750mm), confirmed constant-radius (i.e., a genuine full 360° ring, not a partial arc) at every sampled height through the full 10mm depth | 71.5mm, "anchored around its entire perimeter" | Exact — I directly confirmed the full-perimeter claim myself, not just the diameter |
| Body bore at P3 (z=138.5mm) | outer=44.000mm / inner=**40.000mm** | 44.000mm / 40.000mm | Exact |
| Body bore, collar band (z=145.5–153.4mm) | outer=50.000mm / inner=~40.00mm (mesh noise 39.96–40.00) | outer=50.000mm / inner=40.000mm | Exact |
| Collision margin | Plug tip at body-Z=143.5mm (85mm lid height − 10mm plug region... i.e. seating plane 153.5mm − 10.0mm depth), body taper starts at 138.5mm → **5.0mm margin** | 5.0mm margin | Exact |
| Clearance | 80.000mm bore − 79.500mm plug OD = **0.500mm diametral** | 0.500mm | Exact |
| Handle through-hole | Interior loop (open air) present from **y=−4.0mm to +4.0mm**, solid outside that band | Same window, 22×24mm | Exact (same window; I didn't re-measure the exact mm² footprint, just the loop presence/absence, which is the load-bearing hard-constraint check) |

Every figure I derived independently matches the Tester's reported numbers exactly, at the same
precision. I regard this as solid corroboration by a fourth independent method, not a rubber
stamp — I did not accept the "fully enclosed, anchored around its entire perimeter" framing on
description alone; I confirmed it directly by sampling the interior-ring radius at high resolution
through the full depth and finding it is a genuine constant-radius closed ring (not a partial arc,
not an off-center hole) at every sampled height, which is exactly what "anchored around its entire
perimeter" requires to be true.

## 2. The bridging-risk framing — my independent read, since this is the one judgment call actually being asked of me

Having confirmed the geometry myself (71.5mm-diameter fully enclosed void, capped by a flat 5mm
brim ceiling, anchored on a genuine continuous 4mm-wide ring around its full perimeter, on a PETG
part), I side with the **Tester's framing over the Coder's**, and for the same reason the Tester
gives: these are two different questions, and the Coder's "cosmetic non-issue, just watch cooling"
collapses them into one.

- **Likelihood of an imperfect bridge is real, not a low-probability edge case.** 71.5mm is roughly
  1.5–1.8× the ~40–50mm span most FDM guidance treats as the top of the reliably-bridgeable range
  even for PLA — and this is PETG, a material every reputable source (and this project's own prior
  material-risk discussion, `tests.md` original pass §3) already treats as a *worse* bridging
  material than PLA, not a neutral one. Full 360° anchoring genuinely helps versus a two-sided
  bridge, but it doesn't erase a 2× overshoot past the normal guidance band — the center of the
  span is still the same distance from any anchor point regardless of how many anchor points exist
  around the rim. I'd expect visible sag and likely some stringing on the first bridging layer(s)
  under default slicer settings. This should be stated in the record as an expected outcome, not a
  contingency.
- **Consequence is genuinely near-zero, but specifically because the surface is both hidden and
  functionally inert — not because the print risk itself is small.** I confirmed this directly:
  the cavity's boundary (the 35.75mm inner radius) has no relationship to any fit-critical surface
  (the plug's fit-critical OD is the *outer* 39.75mm wall, unaffected by anything happening in the
  hollow interior) and no relationship to any visible surface (it's sealed under a solid brim,
  never exposed once printed). A sagged or stringy ceiling here cannot be seen, cannot be felt, and
  cannot affect the plug's clearance fit.
- **Recommended record framing:** "expect a real, visible-if-you-could-see-it bridge sag/stringing
  under default settings; this has no functional or cosmetic consequence because the surface is
  permanently sealed and disconnected from every fit-critical or visible feature" — not "cosmetic
  non-issue, just watch cooling," which reads as minimizing the print-quality event itself rather
  than correctly locating why it doesn't matter. This is a framing/documentation correction, not a
  disagreement about whether to block — I agree this does not block.

## 3. Trapped-support risk (item 3) — confirmed real, agree it needs a documentation callout

I agree this is a genuine, previously-unflagged gotcha, and I confirmed the geometric precondition
myself in §1 above: the void is **fully sealed** (0 interior loops at z≥10.0mm, confirmed on the
actual shipped mesh) — so any support material a "supports everywhere" slicer setting generates
inside the 71.5mm cavity before that ceiling closes over it would be permanently trapped with no
access path to remove it. Functionally inert (rattling debris sealed in a spot nobody will ever
open), but a real, avoidable annoyance if not called out. **This must go into the shipped
documentation**, not just this review record — see §5 below, since it currently isn't anywhere.

## 4. Tilt-angle reasoning (item 4) — confirmed, no pushback

I agree with the Tester's reasoning without needing to redo it: the outer support annulus is a
discontinuous radial step (Δr=21.25mm within one layer transition, from the 39.75mm plug wall out
to the 61mm brim radius), not a sloped or curved surface — tilting a part converts an *already-
sloped* surface into a self-supporting one, it does not turn a literal vertical cliff into a slope.
Confirmed by inspecting the actual transition myself in §1 (z=9.9999mm still shows the 39.75mm-
radius plug cross-section; z=10.0000mm jumps straight to the full 61mm brim radius with nothing in
between — a genuine one-layer discontinuity, not a short taper a tilt could exploit). Any tilt
large enough to meaningfully un-bridge the internal void would also reintroduce overhang on the
dome/handle, which are deliberately flat-oriented today specifically to avoid that. Keeping the
flat orientation and handling the bridge via layer-band-scoped slicer settings (max cooling, reduced
speed for that z-band) is the right call.

## 5. Test-coupon recommendation (item 5) — confirmed, reasoning holds

I agree with the Tester's sharpened framing: FDM's systematic tendency (inward corner rounding,
extrusion overlap compensation, general shrinkage) is for bores to print undersized and
bosses/plugs to print oversized relative to nominal CAD — meaning the realized clearance on this
0.5mm-nominal fit is more likely to land tighter, not looser, before even accounting for the
already-named PETG-plug/PLA-body shrinkage-mismatch risk in `specs.md` §5.2.1. This is a
directionally-specific risk, not a generic "test your fits" disclaimer, and is worth a small
stand-alone coupon print before committing an ~85mm-tall, multi-hour PETG lid print to an untested
fit. I have no basis to push back on this and see no reason to.

## 6. Documentation — real, currently-unaddressed gap, consistent with this project's recurring pattern

I checked `README.md` and `parameters.md` directly rather than assuming they'd been updated
alongside the lid re-export. **They have not been.** Both still describe the v5 flat-seating-only
interface as current (`README.md` line 20: "a flat brim that rests on the body's flat 100mm-OD
collar rim (**no plug/skirt** — deliberately...)"; `parameters.md` line 201: "Single flat plane on
the body's flat 100mm-OD collar rim. **No plug/skirt/alignment lip.**"). Neither document mentions
the plug, its dimensions, the accepted support tradeoff, the bridging-risk framing, or the
trapped-support slicer callout from §3 above. This is the same category of gap this document has
flagged after v4 and again (more emphatically) after v5 — and it is worth naming plainly again
rather than letting a fourth round pass with stale top-level docs: **before this project is called
"done" again, `README.md`/`parameters.md` need**:
1. The plug's dimensions and purpose (79.5mm OD × 10mm deep, hollow, 4mm wall, 0.5mm clearance).
2. The accepted print-support tradeoff on the outer annulus (user already informed and accepted —
   just needs to be on record in the docs a future editor would read, not only in `specs.md`).
3. A one-line slicer callout: **confirm supports are set to "touching build plate only" before
   slicing the lid**, to avoid permanently trapping unremovable support material in the now-sealed
   internal void (§3 above).
4. A recommendation to print a small clearance test coupon before committing to the full lid print,
   with the tighter-not-looser directional note from §5.

This is non-blocking for printing — the exported STEP/3MF/STL files are correct and reflect the
current design, independently confirmed in §1 above — but it is a real, accumulating gap in
exactly the category this project has repeatedly (and correctly) been called out for before.

## 7. Cost — no material change worth flagging

The added plug is hollow (4mm wall, per the spec's stated Coder-level choice), roughly
π×(39.75²−35.75²)×10mm ≈ 9.5 cm³ of added material — negligible against the lid's existing ~219 cm³
(v5 figure, `review.md`'s v5 section §6), well under 5% of the lid's material volume. No
cost-verdict change from the v5 figures (~$12.5–16 combined pair, PASS).

## 8. Business fit / concept fidelity — unaffected, confirmed by scope and by direct inspection

This feature is entirely internal to the assembled neck opening — it has zero effect on the
exterior silhouette in any view. I confirmed this directly: the plug sits entirely below the lid's
flat underside/seating plane, inside the body's neck bore once assembled, with no external face
change to the brim, dome, or handle. `concept/brief.md` and `concept-v2.png` never depicted or
implied anything about a below-the-seating-plane fit mechanism (the original concept doesn't even
show the lid removed), so there is no concept-fidelity question raised by this addition at all —
it's a pure fit-and-function improvement with no visual footprint. Business fit is unaffected for
the same reason: it doesn't touch the neck-opening-size business decision (§4.4/v5) or any of the
concept's load-bearing identity features (plain body, open-loop handle).

## 9. Final render — not re-shot, and I don't think it needs to be

The existing hero render at `render/pet-memorial-urn-hero.png` (produced during the v5 full
re-review, §8 above) still accurately depicts the current, final, as-shipped exterior geometry — I
confirmed this is true rather than assuming it, since the plug is, by construction and by my own
direct inspection in §1, entirely hidden below the lid's underside once seated, with zero effect on
any externally-visible surface. Re-rendering would produce a pixel-for-pixel-equivalent image (same
appearances, same lighting, same silhouette). I'm treating "no new render needed" as the correct,
proportionate call for a change with literally zero visible footprint, rather than mechanically
re-running the render step — this is consistent with this project's own established practice of
scoping effort to what a round's change actually touches (e.g. Addendum 2's "quick corroborating
spot-check... rather than a full independent re-analysis, per the scope requested").

## Final verdict for this addendum

**APPROVED, with named watch-items — not blocked.**

- **Geometry:** independently re-confirmed via a fourth method (my own `trimesh` script against the
  actual shipped files) — every checked figure (manifold integrity, plug wall thickness, bridge
  diameter and full-perimeter anchoring, collision margin, clearance, handle integrity) matches the
  Tester's reported numbers exactly. No pushback on any of the five originally-requested checks.
- **Bridging-risk framing:** I side with the Tester's sharper characterization over the Coder's
  "cosmetic non-issue" framing. The record should say plainly: a real, visible-grade bridge
  sag/stringing event is the *expected* outcome under default settings on this 71.5mm PETG span,
  not a low-probability edge case — and it doesn't matter, specifically because the surface is
  sealed, invisible, and disconnected from every fit-critical and visible feature. Both halves of
  that sentence are load-bearing; neither should be dropped.
- **Trapped-support risk:** confirmed real (the void is genuinely fully sealed, independently
  verified), needs a one-line slicer callout — not yet in any shipped documentation.
- **Tilt-angle question:** confirmed, no pushback — a single orientation can't fix both overhang
  zones, and the current flat orientation is the right call.
- **Test-coupon recommendation:** confirmed, no pushback — the tighter-not-looser directional
  framing is correct and worth stating plainly rather than as a generic disclaimer.
- **Documentation:** real, non-blocking gap — `README.md`/`parameters.md` still describe the v5
  flat-seating-only interface with no mention of the plug, the accepted support tradeoff, the
  bridging-risk framing, or the trapped-support slicer callout. This is the same recurring
  documentation-lag pattern flagged after v4 and v5; it should not be allowed to compound into a
  fourth stale round before being closed out, though it does not block printing today.
- **Cost:** no material change worth flagging (~9.5 cm³ added, negligible against the lid's ~219 cm³).
- **Business fit / concept fidelity:** unaffected — the feature is entirely internal, zero visible
  footprint, doesn't touch the neck-opening business decision or either of the concept's
  load-bearing identity features.
- **Render:** not re-shot; the existing v5 hero render remains an accurate, fully representative
  image of the current exterior geometry, since this change has no visible footprint.

`urn-lid` (with the new plug) remains approved and print-ready as currently exported, alongside the
unaffected `urn-body` and `neck-fit-test`. The most important next step is unchanged from the v5
verdict: the requester actually printing and testing the `neck-fit-test` article against a real or
mocked remains bag. Two new, non-blocking, concrete recommendations from this round: (1) print a
small clearance-test coupon for the plug fit before committing to the full ~85mm PETG lid print, and
(2) confirm slicer supports are set to "touching build plate only" before slicing the lid, to avoid
trapping unremovable support material in the now-sealed internal void.


---
---

# FULL RE-REVIEW — 2026-09-02: v7 major lid revision (handle removed entirely, plug tip capped, brim thickened+shrunk to flush, dome apex flattened)

## Why this gets a full pass, not another addendum

Agreed with the framing this was handed to me under. Every prior addendum in this document (v6's plug, the magnet removal, the capacity consolidation) was scoped to a change layered on an already-settled identity. This round is different in kind: it reverses a constraint the concept brief itself called "the key differentiating feature" of the entire design and "load-bearing to the design's identity" — a hard constraint stated at the project's very first approval gate and re-verified as intact by every single prior Reviewer pass in this document. That reversal, plus four other coordinated lid changes shipping in the same round, gets the full six-part treatment requested: concept fidelity, documentation adequacy, an independent geometry spot-check using my own method (not a re-read of the Coder/Tester chain), print-orientation re-confirmation, a usability re-assessment, and a fresh render.

**What is not being re-litigated:** the body (neck/collar/belly/height) is untouched by this round and was already fully reviewed through v5 — confirmed unaffected below by direct measurement, not by assumption.

---

## 1. Concept-fidelity assessment — the real substance of this review

**I looked at this directly, not through the pipeline's characterization of it.** I re-read `concept/brief.md`, looked again at `concept-v2.png`, pulled the archived pre-v7 lid (`archive/pre-v7-handle-removal/`) and rendered it back-to-back against the new v7 geometry (both saved as real renders below, not composited), and I raised the live lid to its true seated height on the untouched body for the comparison rather than judging the lid in isolation.

**The brief's own words are unambiguous, and worth quoting again because they are the entire basis for this judgment call:** "Centered on top of the lid is **the key differentiating feature**: a thick, rounded, open-loop bail-style handle... It reads as an intentional, load-bearing part of the lid, not a decorative nub." And, in the iteration history: "The open-through-hole handle geometry... should be preserved **as a hard constraint** when the Planner moves to CAD." This was not a minor styling note. It was framed, at the one moment in this project's history when a human actually looked at a picture and said "yes, build this," as the single thing that made this design something other than a copy of the reference commercial urn the project explicitly set out to differentiate from (v1's own iteration history: "took the reference commercial urn's shape and added the loop-handle lid").

**With it gone, what's actually left is a plain domed lid on a plain-bodied jar — and I don't think that reads as a coherent, differentiated identity anymore, it reads as generic.** Side-by-side, `archive/pre-v7-handle-removal/pet-memorial-urn-hero.png` (v6, handle + overhanging brim) against my fresh `render/pet-memorial-urn-hero.png` (v7): the v6 lid at least had a raised, sculptural element breaking its silhouette. The v7 lid is a smooth dome with a subtle two-stage fillet into a flush brim and a flattened plateau that is only visible if you look down on it from almost directly above — at any normal viewing angle (including the one a customer would see in a product photo, which is exactly how `concept-v2.png` itself is framed) it reads as an unbroken dome. That is close to a textbook description of "generic ceramic ginger-jar lid," which is precisely the category this project's own concept brief was written to escape.

**This isn't happening in isolation — it's landing on top of two already-disclosed drifts, and the combination is the part worth naming plainly:**
- The v4 belly edit made the body read as a more pronounced "ginger jar" silhouette than the concept's gentler taper (my predecessor's own words, `review.md` Addendum 3 §8) — a shape that, on its own, is *more* generic-decorative-jar, not less, even though it was independently judged a legitimate aesthetic call.
- The collar has read as a "banded, partially-cylindrical" reinforcement ring rather than the concept's continuous neck curve since v2/v3, accepted every round as a disclosed, functionally-necessary tradeoff.
- Neither of those, alone, was judged serious enough to block — and I agree with that judgment, looking at each in isolation. **But both were previously tolerated specifically because the handle was still there anchoring the design's identity against them.** Every prior Reviewer pass that waved through the belly-pinch or the banded collar did so in a document that, in the very same paragraph, could still point to "the plain undecorated body and the open-loop bail handle are both fully intact... independently reconfirmed" as the load-bearing counterweight. That counterweight is now gone. I don't think the belly-pinch or the banded collar independently got worse this round (they didn't — confirmed unaffected below), but the **thing that made them tolerable** — a distinctive lid identity elsewhere on the object — did.

**Is there anything left that functions as a differentiator?** I looked for one specifically before concluding there isn't. The flattened plateau (21.73mm, §5.1.4) is a real, deliberate, concept-image-approved styling choice — but it is subtle to the point of being nearly invisible in a normal three-quarter product shot (confirmed directly in my own render below), and it was motivated by print-quality and "reads as intentional now that there's no handle" reasoning, not by an intent to replace the handle as a standalone identity marker. The flush 99.7mm/100mm brim edge is a real refinement, but it is the kind of detail a buyer notices on the object in hand, not in a photo, and it isn't visually distinctive either way (a flush edge and an overhanging edge both just read as "a lid"). Neither is a plausible substitute for what the brief called "the key differentiating feature."

**My judgment, stated plainly per the specific instruction not to soften this:** the cumulative effect of v4 + the persistent banded collar + this round's full handle removal is enough that I think this has genuinely reverted toward being visually indistinguishable from the generic reference product the project was written to differentiate from. I am not blocking on it — this was an explicit, informed, directly-confirmed user decision (the user was told in advance it reversed the brief's own "hard constraint" framing, and confirmed anyway, per `specs.md` §7 and the task framing this review was commissioned under), the practical reasoning behind it is sound (a genuine, disclosed competitive-height concern; a real, substantial print-time/material/support reduction; a lid that's meaningfully less top-heavy), and nothing here is a defect — it is a legitimate creative and business call that belongs to the requester, not to me. But "the requester already decided this" and "the requester was shown the full cumulative visual consequence of this specific decision, on top of the drifts already banked from v4/v2" are two different claims, and I don't think the second one is true yet (see §2 — nothing in any document the requester would actually read describes this trade-off in these terms). **I am recommending, not requiring, that this go back to the requester as an explicit visual check-in before being treated as fully final** — not "does the handle removal seem fine" in isolation (which it apparently already was), but "here is the finished object next to the original concept image and next to the v6 version you approved before this — does this still feel like the differentiated product you set out to build, or does it now read as a generic jar with a lid to you too." That is a business/creative judgment only the requester can make, and I don't think it has actually been made against the real, cumulative, rendered evidence yet.

---

## 2. Documentation adequacy — specs.md meets the standard; the two documents a future editor would actually read do not, and this is worse than any prior round of this recurring problem

**`specs.md` §7 and §13's v7 row meet the bar.** The handle removal is documented as a direct, explicit, user-confirmed override of the concept brief's own "hard constraint" language, with the brief quoted verbatim, the reversal stated in the same breath as the original constraint (not edited out or silently contradicted), the ripple effects (height, orientation, the now-retired hard-constraint count) worked through explicitly, and the business-fit question expressly punted to the Reviewer rather than pre-judged. This is exactly the standard this project has held itself to, and I have no note on `specs.md` itself.

**`README.md` and `parameters.md` were not touched for v7 at all — not "one revision behind," genuinely untouched.** I checked both directly rather than assuming the pattern from v4/v5/v6 continued:

- `parameters.md`'s own header still reads "current as-built state, **v6**, 2026-09-01" and contains zero occurrences of "v7" anywhere in the file. Its lid table still lists the handle's full dimensions (24×22mm opening, 9mm bail, 40mm height above the dome apex, 4mm root fillet) as **current**, still lists the 122mm brim and ~97–98mm dome base, still gives 85mm as the overall lid height. None of the five v7 changes — handle removal, plug cap, brim resize to flush, dome flattening, or the resulting height drop to 49mm — appear anywhere in this document.
- `README.md` is the same: it still describes "an open-loop carry handle" in its own summary line, still says "the open-loop handle — remain fully intact" in its concept-fidelity section, still tables the lid at 85mm/122mm OD with no plug-cap or flush-brim language, and contains zero occurrences of "v7."

**Why I'm treating this as more serious than the recurring documentation-lag pattern already on record in this document (§5 of the v5 full re-review, and Addendum 4 §6), not just another instance of it:** every prior instance of this pattern was a *numbers* problem — a stale dimension, a stale capacity figure, a missing new feature's spec sheet. This is different in kind: **the single most identity-defining fact about the current design — that the handle the brief called load-bearing to its identity no longer exists — is completely absent from both documents a future editor or the requester would actually reach for.** Someone reading only `README.md` today would come away believing this urn still has its signature handle. That is exactly the failure mode this project has repeatedly and explicitly said it exists to avoid ("never letting a Reviewer discover an unexplained identity-level change" is the standard the task itself invoked, and it is squarely `specs.md`'s standard too, met there — but the two lightweight documents fail a milder, adjacent version of the same standard: never letting *the next reader* discover an unexplained identity-level change either, since that's the entire stated purpose of these two files per every prior round of this review).

**This is not a print blocker** — the exported STEP/3MF/STL files are correct and independently re-verified below, and the slicer doesn't read `README.md`. But I'm elevating this beyond the usual "required, non-blocking follow-up" framing used in every prior round: **this project should not be called done, and arguably should not be handed back to the requester as finished, with its own README describing a feature that was deliberately and explicitly removed one round ago.** This is a five-minute fix (both documents already have the right section structure from prior updates; they need the v7 numbers dropped in and the handle language struck), but it is the single most important non-CAD action item coming out of this pass.

---

## 3. Independent geometry spot-check — my own method, live Fusion B-rep queries, not a re-read of the Coder/Tester chain

I queried the live `pet-memorial-urn` document's actual `BRepBody` object model directly (via the Fusion API's own `faces`, `shells`, and `boundingBox` collections) — a different method again from the Tester's two (`trimesh` mesh-split on the exported STL, and text-parsing the STEP file's native entities). This is arguably the most authoritative of the three methods available on this project, since it queries the CAD kernel's own live object model with no export/tessellation step in between at all.

| Check | My independent measurement (live B-rep query) | Spec/Tester claim | Match |
|---|---|---|---|
| Plug cap topology | `urn-lid` body: **13 faces, 2 shells** — shell 0: 3 faces (the void), shell 1: 10 faces (the outer envelope) | 2 components / `BREP_WITH_VOIDS`, 13 faces (3+10) | Exact — confirmed at the live-model level, not just in an exported file |
| Brim OD (flush fit) | Cylindrical face **r=49.8500mm** (OD **99.700mm**), z=10.0–17.0mm | 99.700mm | Exact |
| Body collar OD (mating surface) | Cylindrical face **r=50.0000mm** (OD **100.000mm**), z=145.5–153.5mm | 100.000mm | Exact — confirms the claimed 0.3mm deliberate negative allowance is real, not a rounding artifact |
| Dome plateau diameter | Flat top face, **z=49.0000mm**, bounding box **21.7283 × 21.7283mm** | 21.7283mm | Exact |
| Dome sphere | R=**41.4849mm**, center z=9.0000mm | R=41.4849370254mm, center z=9.0mm | Exact |
| Total lid height (seating plane to plateau) | 49.0mm (bbox top) − 10.0mm (seating plane) = **39.0000mm** | 39.000mm | Exact |
| Total lid bounding-box height | **49.0000mm** exact (`boundingBox`) | 49.000mm | Exact |
| Body overall height | **153.5000mm** exact, confirmed live, body file untouched by this round | 153.500mm | Exact |
| Combined assembled height | 153.5 + 39.0 = **192.500mm** | ≈192.5mm | Exact |
| Body/lid volumes | Body **278.9394 cm³**, lid **194.2929 cm³** | Body 278.94 cm³ (Reviewer, prior round); lid 194.2929 cm³ (Coder, STEP-analytic) | Exact |
| `neck-fit-test` bounds | **144.000 × 144.000 × 35.000mm** (live, exact) | ~143.97–143.98mm (mesh-measured) | Consistent — live parametric value is the more precise of the two, as expected |
| Component/scope check | 3 occurrences in the document (`urn-body`, `urn-lid`, `neck-fit-test`), no hidden/duplicate bodies | Same | Confirmed, no scope creep |

**Every headline number the task asked me to spot-check is confirmed exactly**, via a method independent of both the Coder's and the Tester's.

**One genuine, if minor, refinement to the record — a partial correction to the Tester's own R67 documentation-accuracy finding, found by this more direct method:** the Tester's R67 (RE-TEST PASS 9) states the two brim-to-dome fillet toruses meet "with no flat annular face modeled between them." Enumerating the actual face list directly, I find a real `PlaneSurfaceType` face at **exactly Z=20.0000mm**, normal (0,0,1), spanning radius ≈41.50–46.85mm (bounding box 93.70×93.70mm, area 1485.92mm²) — sitting precisely between the two toruses the Tester correctly identified (major r=46.85mm/minor 3mm below it, major r≈41.50mm/minor 2mm above it). This is a genuine, physically-real flat annular shelf (about 5.35mm wide), not a tangency artifact or a zero-area seam — it has real, nonzero area and would print as an actual flat horizontal step. It is unrelated to and unaffected by the RE-TEST PASS 10 dome-apex fix (it sits on the *outer* torus, which R75 confirms is unchanged digit-for-digit from RE-TEST PASS 9). **Net effect on the record:** the spec's original "10mm flat brim ring, r=40–50mm" claim (§5.1.3) is still wrong as stated (that's not where or how wide this flat feature actually is), and the Tester's R67 correction is *also* not quite right in the other direction (there is a flat face, just a narrower and differently-positioned one than either document describes). Practically this changes nothing — it's self-supporting either way (radius never increases with height across this span, confirmed independently below), fully consistent with every prior pass's PASS verdict — but the documentation fix already planned for R67 should describe a genuine ~5.35mm flat step nested between two fillets, not "no flat face at all."

---

## 4. Print-risk re-assessment — orientation

**I agree with the Planner/Coder's flat-underside-down (plug-tip-down) call, and I checked the alternative myself rather than taking the rejection on faith.** With the handle gone and the apex flattened, plateau-down is real to consider — genuinely new options the pre-v7 geometry never had. But flipping the part inverts the entire dome's overhang class: today, every sampled point from the plug tip (Z=0) to the plateau (Z=49mm) has non-increasing radius with height (confirmed independently in my own face/geometry pass above — the one place radius is locally flat rather than decreasing is the Z=20mm shelf identified in §3, which is a *flat* step, not an *increasing* one, so it does not break this class either). Flip the part plateau-down and that entire relationship inverts: the dome becomes a classic expanding cone from a ~21.7mm top down to an 80mm base, needing support under virtually the whole visible dome exterior — trading one small, sealed, invisible bridge (the plug's internal ceiling, already accepted as consequence-free) for full-surface support on the one cosmetically-critical surface the flat orientation was chosen specifically to protect. It would also flip the plug's tip cap from a bed-supported first layer into an unsupported last layer over a sealed void, reintroducing a bridging risk that capping-then-orienting-tip-down was specifically designed to avoid. I don't think this is a close call once the whole dome and the plug's cap are both accounted for, not just the plateau's own flatness in isolation — flat-underside-down remains the right call.

---

## 5. Usability / drop-risk note — confirm and slightly sharpen

**I agree with the Tester's R70.1 finding, and I'd state it a notch more seriously than a routine watch-item given what this object actually holds.** Gripping a smooth dome by hand is less secure than a purpose-built handle loop — the *survivability* of a drop is fine (solid PETG, no thin unsupported features outside the sealed internal bridge), but the *likelihood* of one plausibly goes up with no dedicated grip, and this is true specifically at the moment (transferring a filled urn, likely during an emotionally difficult task) where a slip is most consequential. This container holds irreplaceable cremated remains — the failure mode here isn't "cosmetic damage to a decorative object," it's a genuinely distressing accident for the owner. I'd recommend the shipped documentation go slightly further than a one-line note: a short, explicit care instruction (lift with a full hand under the dome/brim, not a fingertip pinch on the edge; consider lifting the lid and setting it down before moving the filled body, rather than carrying the assembled unit by the lid) is cheap to write and directly addresses the specific new risk this round introduces. This is a documentation recommendation, not a geometry or business-fit blocker.

---

## 6. Fresh hero render — produced from the live, current v7 geometry

Both `urn-body` and `neck-fit-test` had been hidden in the live document (a user visibility toggle, not a design change) — both were unhidden first, confirmed via `Occurrence.isLightBulbOn`, and left visible afterward (a reasonable default state for the document, not a render-only stage). Both custom appearances survived intact and required no repair this round (`Matte PLA - Stoneware Tan (urn-body)` on the body, `Matte PETG - Stoneware Tan (urn-lid, sanded)` on the lid — confirmed via direct query, not assumed).

For the render itself: the lid was temporarily raised to its true seated height (153.5mm, on top of the untouched body) and `neck-fit-test` was temporarily re-hidden for the shot (consistent with every prior hero render in this project, which has only ever depicted the two-part product, not the standalone test article) — both reverted immediately after capture. Captured via `Viewport.saveAsImageFile` (the real, current geometry, not a generated image) and saved to `H:\ClaudeStuff\3d-print-team\pet-memorial-urn\render\pet-memorial-urn-hero.png`, replacing the stale v6 image.

**The previous (v6) hero render was not yet archived anywhere before I overwrote it — I found and fixed this as part of this pass.** I recovered it from git history (`git show HEAD:pet-memorial-urn/render/pet-memorial-urn-hero.png`) and saved it to `archive/pre-v7-handle-removal/pet-memorial-urn-hero.png`, alongside that folder's existing pre-v7 STEP/3MF/STL, so the handle-vs-no-handle comparison this review's §1 relies on remains available to whoever looks at this project next, consistent with this project's own established practice of never deleting a superseded render outright.

**Same honest, disclosed limitation as every prior render in this project:** a faint background reference-grid overlay remains visible and could not be suppressed via the available API (confirmed again this round — no sketch grid, no origin-folder visibility, and no scriptable grid-preferences API were found to control it; this appears to be a viewport-chrome element, not model geometry). This does not affect the model, material, or lighting shown.

---

## Final verdict

**APPROVED — the exported STEP/3MF/STL files for `urn-lid` are geometrically sound and independently re-confirmed via a fourth/fifth method (live B-rep query) at every headline dimension the task asked me to check. `urn-body` and `neck-fit-test` are confirmed unaffected. This is not blocked.** But two items carry more weight than a routine watch-item, and I want them read as such rather than filed away with the rest:

1. **Required before this project is called done (non-blocking for print):** `README.md` and `parameters.md` must be brought current to v7. This is not a routine "one revision behind" instance of this project's recurring documentation-lag pattern — both documents currently describe a handle that has been deliberately and explicitly removed, on the exact question ("does this design still have its stated identity") this review round exists to answer. A future reader relying on either document today would be actively misled about the single most identity-defining fact of the current design.
2. **A genuine, non-blocking business/creative flag, not just a watch-item:** the cumulative effect of this round's handle removal, layered on the already-disclosed v4 belly-pinch and the persistent banded collar, is that this design reads to me as having lost the "key differentiating feature" the concept brief built its entire identity around, and now presents as visually close to the generic reference product this project was originally written to differentiate from. I am not overriding the requester's own explicit, informed decision — the practical reasoning behind it is sound, and nothing here is a defect. But I don't think the requester has yet seen the *cumulative*, rendered consequence of this decision stacked on top of the two drifts already banked from earlier rounds, and I'm recommending — plainly, not as a footnote — a real visual check-in (concept image, v6 render, and this v7 render, side by side) before this is treated as fully final.

Everything else checked in this pass — the plug-cap topology, the flush brim/collar fit, the dome plateau dimensions, all headline heights, the print orientation, cost (a real, if modest, ~6–9% *decrease* versus v6, driven by the handle's removal outweighing the thicker brim and capped plug), and the two remaining hard constraints (plain body, single-size build) — is sound, independently confirmed, and does not block. The usability note on drop-likelihood (§5) is worth a slightly more deliberate care-instruction than a single line, given what this specific object holds, but is not a structural or business-fit blocker.

Render: `H:\ClaudeStuff\3d-print-team\pet-memorial-urn\render\pet-memorial-urn-hero.png` (current, final v7 geometry). Superseded v6 render preserved at `H:\ClaudeStuff\3d-print-team\pet-memorial-urn\archive\pre-v7-handle-removal\pet-memorial-urn-hero.png`.
