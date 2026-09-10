# Reviewer — Pet Memorial Urn, Medium (25–50 lb), First Review Pass

Cold start. Read `medium/dot_pipeline/specs.md` (including the v1.1 brim-tolerance revision),
`medium/dot_pipeline/tests.md` (both the original pass and the brim-fix RE-TEST pass), and
`medium/dot_pipeline/verdict.md` (both passes) in full. Also read the Large build's
`concept/brief.md` and `concept-v2.png`, Large's own `README.md` (full v4–v7 revision history),
and the Small build's `specs.md`/`verdict.md`/`review.md` for cross-size context (proportion
comparison and precedent on how this project handles the recurring neck-ID risk). Independently
re-derived the Tester's headline numbers from the exported STEP/STL files using my own scripts
(Python/trimesh, a different toolchain from the Tester's), not a re-read of their reported figures.
I also had live (if contentious — see §5) access to the `pet-memorial-urn-medium` Fusion document
this session.

## Overall verdict: CONDITIONAL PASS — BLOCKED for production printing on the 72mm neck-ID item

**The CAD build itself is a clean, high-confidence pass.** My own independent re-measurement,
using a different method and toolchain than the Tester's, corroborates every headline number in
`tests.md` to within noise: cavity volume, wall thickness at multiple control points, the brim-OD
fix, and the plug/bore clearance and collision-free fit all check out. No contamination from the
concurrent Small/Large sessions was found in any exported file.

**This does not clear the design for a full production print run.** Per this project's own standing
convention — applied identically to Large's 80mm and Small's 70mm — the following remains a named,
unresolved blocker, not a routine watch-item:

> **The 72mm neck/collar ID (specs.md §4.3) is tagged `ESTIMATED` and mates with a real external
> object (a 25–50 lb pet's crematorium remains bag) this team does not have in hand.** The spec's
> own research is real, and the spec itself is unusually explicit that this is a *larger* compromise
> than Large's or Small's equivalent decisions — 72mm sits *below* the entire 79–89mm real-competitor
> cluster the spec's own fresh research found for this exact capacity tier (Large's 80mm and Small's
> 70mm each sat at least at the edge of their own researched ranges; Medium's 72mm sits outside its
> range entirely). I found no evidence in this project's files that `neck-fit-test-medium` has
> actually been printed and checked against a real or mocked medium-pet remains bag, and no written
> risk acceptance from the requester overriding that gate. **Do not commit `urn-body-medium` to a
> full-scale production print until either (a) that physical test has been run and passed, or (b)
> the requester explicitly accepts the risk in writing.** This routes back to the Planner/requester,
> not a modeling fix — the CAD is already an accurate, precise build of the estimate spec'd.

**On material:** the body is PLA at a 3.2mm wall (thinner than Large's 4.0mm). The Tester flagged
this as a drop/impact-risk concern and recommended PETG. Per the task brief for this review, the
requester was already asked and explicitly chose to keep PLA for the body despite that
recommendation — this is a confirmed, informed decision, not an unexamined default, and I am not
reopening it. It should be recorded as such once `medium/parameters.md` exists (§3).

---

## 1. Business fit / concept fidelity

**Reads as the same design, mid-size — correctly carrying forward the post-v7 identity (no handle,
flush brim, flattened dome plateau, plain undecorated body, straight-walled capped plug), not the
original concept brief's handle-bearing image.** This is the right reference to hold Medium to:
Large's own README is explicit that the v7 handle removal knowingly supersedes the literal
`concept-v2.png` appearance, and every size since (Small, now Medium) correctly inherits the
post-removal identity rather than the original picture. Medium's spec and built geometry are
internally consistent with that lineage — no magnet pockets, no handle, no engraving, flush
zero-overhang brim, capped straight plug — all qualitatively present and correctly built, confirmed
by my own independent measurement (§2), not merely claimed in the spec.

**The collar-to-belly proportion drift the task asked me to check — confirmed, and it continues the
same trend Small's review already flagged, at a magnitude in between the other two sizes:**

| Size | Collar OD | Belly OD | Collar ÷ Belly |
|---|---|---|---|
| Large | 100mm | 153.9mm | **≈65.0%** |
| **Medium** | **88mm** | **120.4mm** (independently measured, §2) | **≈73.1%** |
| Small | 82mm | 98mm | **≈83.7%** |

This is a real, monotonic, geometrically-forced trend, not noise: because the neck ID is
deliberately *not* shrunk in proportion to volume at any size (each size's spec treats a bag-fit
opening as a near-fixed practical minimum, not a linearly-scalable dimension), and because each
smaller size resolves the resulting base/collar-vs-belly tension by widening the base to meet the
collar rather than shrinking the collar further, every step down in size necessarily produces a
*proportionally* wider collar relative to its own belly. Medium sits exactly where you'd expect
given that mechanism — between Large's 65% and Small's 84%, not closer to either edge. **This isn't
a defect and doesn't block approval** (the belly is still unambiguously the widest feature at every
size, hierarchy never inverts), but it means the three sizes will not read as pure linear scale
copies of one another sitting side by side — the smaller sizes progressively read as more
"wide-mouthed jar," less "narrow-necked vase," than Large does. Whoever signs off on the finished
product-line look should know this before treating the three sizes as visually interchangeable.

**A second, compounding item worth naming plainly, not buried:** Large's own v7 review recommended
a real visual check-in with the requester — comparing the original concept image, the pre-v7
handle render, and the v7 no-handle render side by side — specifically to confirm the no-handle
design still reads as differentiated rather than generic. Large's own `README.md` states in its
"Status" section that **this check-in has not yet happened**. Two more sizes (Small, now Medium)
have since been built on top of that same unconfirmed identity decision, each independently
re-deriving dimensions but not re-litigating (correctly, per their own scope) the visual identity
itself. This is not a defect introduced by Medium, and I am not re-opening the identity decision
here — but the gap is now three sizes deep without ever having been closed out, and it's worth the
Director flagging at the product-line level rather than letting it quietly age further with each new
size.

---

## 2. Independent geometry spot-check (own script, own methodology — Python/trimesh, cross-section
   slicing, polygon-hole integration, and boolean intersection — not a re-read of the Tester's
   figures)

| Check | My independent measurement | Tester's figure | Spec target | Result |
|---|---|---|---|---|
| Body: watertight/manifold | `is_watertight=True`, `is_winding_consistent=True`, 1 component | Same | — | Match |
| Body material (shell) volume, divergence theorem | **182.465 cm³** | 182.47 cm³ (orig.), 182.465 cm³ (RE-TEST) | 145.0 cm³ hand-calc (spec flagged as rough) | Exact match to Tester |
| Body cavity volume, own plane-slice + polygon-hole trapezoidal integration (400 z-samples) | **805.30 cm³** (−1.72% vs. target) | 806.1 cm³ (−1.63%) | 819.4 cm³ (±5%: 778.4–860.3) | PASS, matches Tester within method noise |
| Body extents (belly OD × height) | **120.400mm × 131.000mm** | Not stated as extents | 120.4mm × 131mm | Exact match |
| Wall thickness at P1 (belly, z=59mm) | **3.2000mm** | 3.200mm | 3.2mm | Exact |
| Wall thickness at P2 (shoulder, z=77mm) | **3.2000mm** | 3.200mm | 3.2mm | Exact |
| Wall thickness at P3 (neck-taper-end, z=119mm) | **3.2000mm** | 3.200mm | 3.2mm | Exact |
| Collar wall (rim, z≈131mm) | **8.000mm** (44.000−36.000) | 7.995mm | 8.0mm | Match |
| Floor thickness | Cavity begins between z=3.9–4.1mm | 4.00mm | 4.0mm | Consistent |
| Body collar OD (top of rim, z=130.999mm) | **87.9999mm ≈ 88.000mm** | Collar unchanged at 88.000mm (RE-TEST RT-4) | 88.000mm (unchanged by brim fix) | Exact — confirms the brim fix was correctly *not* applied to the body |
| Lid brim OD | **87.700mm** (r=43.850, flat z=8–12mm, all-format-independent) | 87.700mm (all 3 formats, RT-1) | 87.700mm (post v1.1 fix) | Exact match |
| Lid net volume | **123.811 cm³** | 123.8109 cm³ (RE-TEST RT-5) | — | Exact match |
| Lid extents | **87.700 × 87.687 × 41.000mm** | — | 87.7mm brim, 41mm total height | Match |
| Plug OD | **71.500mm** (constant, z=0–7.9mm lid-local) | 71.500mm | 71.5mm | Exact |
| Plug wall | **3.200mm** (35.750−32.550) | 3.200mm | 3.2mm | Exact |
| Body bore ID through collar (constant) | **72.000mm** (z=119–131mm) | 72.000mm | 72mm | Exact |
| Plug/bore nominal diametral clearance | **0.500mm** (72.000−71.500) | 0.500mm | 0.5mm | Exact |
| Plug/bore boolean collision check (lid seated at correct world offset, +123mm) | **0.0 mm³ intersection — collision-free** | 0.0mm³ | — | Confirmed independently |
| Collision margin above P3 | **4mm** (plug bottom at world z=123mm vs. taper-start at z=119mm) | 4mm | 4mm | Exact |
| `neck-fit-test-medium`: ID / neck OD / collar OD | **72.00 / 78.4 (r=39.68 near transition) / 88.00mm** | 72.000 / 78.400 / 87.988mm | 72 / 78.4 / 88mm | Match, all within tessellation noise |

**No cross-contamination found.** None of Medium's measured values match Large's signature numbers
(80mm ID / 100mm collar / 153.9mm belly / 4.0mm wall) or Small's (70mm ID / 82mm collar / 98mm
belly / 2.4mm wall) — every figure lands on Medium's own spec, independently, via a completely
different measurement toolchain than the Tester used. This is strong corroborating evidence the
build is sound and unmixed.

**Cost sanity check, using my own independently-measured volumes (not the spec's hand-calc):** body
182.465 cm³ × 1.24 g/cm³ ≈ 226.3g; lid 123.811 cm³ × 1.27 g/cm³ ≈ 157.2g. At $20–25/kg: body
≈$4.53–5.66, lid ≈$3.14–3.93, **combined ≈$7.67–9.59** — matches the Tester's own recomputed figure
($7.68–9.60) almost exactly, and sits sensibly between Small's actual ≈$4.11–5.14 and Large's
≈$12.0–14.9. **Cost-effective for a decorative memorial piece — no concern.** (Filament cost only,
consistent with how this project scopes cost throughout.)

---

## 3. Documentation — required follow-up, not written here

**`pet-memorial-urn/medium/` currently has `dot_pipeline/` (specs.md, tests.md, verdict.md, and now
this review.md) but no `README.md` and no `parameters.md`.** This matches the project's own
established pattern (confirmed on Small's review too): these two documents get written once a size
clears Reviewer approval, not before. Medium has now cleared that bar, conditionally. **Flagging as
a required follow-up, not writing it myself**, per task scope: someone needs to produce
`medium/README.md` (what it is, current dimensions, the neck-fit-test blocker stated as plainly as
this document states it, the confirmed PLA-for-the-body decision, print orientation, known
limitations including the collar/belly proportion drift in §1) and `medium/parameters.md` (as-built
dimension table, VERIFIED vs. ESTIMATED tags, the v1→v1.1 brim-fix revision history). This is cheap
to produce from material already in `specs.md`/`tests.md` and should not be skipped.

---

## 4. Render — produced, but only after real, reproducible shared-session interference; documented
   in full rather than silently retried away

**First: verified the active-document assumption rather than trusting it, per instruction.**
`document/open` showed **`pet-memorial-urn-small` was active, not Medium** (three documents open:
Small, Medium, and an unrelated "MI Lightbox"). This matches exactly the standing risk named in the
task brief.

**What followed was a genuinely reproducible, bidirectional concurrent-session problem, not a
one-off glitch — documented here in the level of detail the task asked for rather than glossed
over:**

- Activating Medium via the `document` execute tool succeeded and was confirmed via `document/open`
  immediately after (isActive: true) — but on the **next separate tool call**, the active document
  had silently reverted to `pet-memorial-urn-small` again, every single time, across at least five
  separate occurrences this session. This happened regardless of tool type (read-only script,
  write script, or the dedicated `document/open` query).
- Every single execute-script call, regardless of what it actually did, returned trailing output
  lines I never wrote — `"Activated: pet-memorial-urn-small, isModified=False"` /
  `"Save result: True, isModified now=False"` — appended after my own script's print statements.
  This indicates a **separate, live, concurrently-running process in this same shared Fusion
  session is repeatedly re-activating and saving the Small document**, on some cadence independent
  of my own tool calls, and its log output is bleeding into my own tool results.
- The standalone `screenshot` MCP query captured **Small's geometry**, not Medium's, even
  immediately after a script call had just confirmed (within that same script's execution)
  `app.activeDocument.name == 'pet-memorial-urn-medium'`. This is the exact same failure mode the
  Small reviewer already documented in reverse (their screenshots landed on Medium's
  `neck-fit-test-medium` instead of Small's own geometry) — now independently confirmed from the
  other side, which rules out "user error on one side" and confirms it's a real property of this
  shared session's screenshot binding, not either reviewer's mistake.
- Separately, and worth naming on its own: an occurrence-level model **transform I set (moving the
  lid to its assembled seating position) was found reverted back to its pre-edit position** on a
  later, separate tool call, even though nothing in my own script sequence undid it. This suggests
  the interference is not limited to camera/active-document state — it can touch live model data in
  the shared document, not just view state.

**Workaround that ultimately worked, documented so it can be reused:** rather than chaining separate
MCP tool calls (activate → screenshot) with a gap between them for another process to exploit, I
used the Fusion API directly, inside a single non-interruptible script execution, to (1) activate
the document by name, (2) assert the activation succeeded, (3) apply the material appearances, (4)
reposition the lid to its assembled seating position, (5) set the camera, and (6) call
`Viewport.saveAsImageFile()` directly to write the PNG to disk — all within one script, with no
intervening separate tool call for the concurrent session to interleave with. This produced a
verified-correct, uncontaminated capture. The first two attempts at this still showed
stale/incorrect state (the lid unassembled, or a bird's-eye framing) because I had other API calls
(appearance library lookups) between the reposition step and the camera/save step — moving the
reposition to be the **last** action immediately before camera+save, with nothing else in between,
resolved it. This is a real, actionable technique for the next agent hitting this same class of
problem in this shared session, not just a note that it eventually worked.

**Result: material appearances applied and a correct, verified hero render produced.**
- Body: `Matte PLA - Stoneware Tan (urn-body-medium)` — copied from the Fusion Appearance Library's
  "Plastic - Matte (White)" and recolored to a tan/stoneware tone (RGB 195,170,140), matching this
  project's established naming convention (Small used the identical pattern).
- Lid: `Matte PETG - Stoneware Tan (urn-lid-medium)` — same source appearance and color, applied to
  the lid body, per the spec's material recommendation (§7 of specs.md).
- The `neck-fit-test-medium` occurrence was hidden for the render (it is a test article, not part of
  the product presentation); the lid was positioned at its correct assembled seating height (+123mm
  in body-local Z, derived from and independently confirmed against §2's own measured geometry —
  131mm collar top minus the plug's 8mm seating-plane offset) so the render shows the real,
  as-assembled product, not the two parts sitting unassembled at a shared origin as they are by
  default in the live document.
- Saved to **`pet-memorial-urn/medium/render/pet-memorial-urn-medium-hero.png`** (1920×1920,
  confirmed written to disk and visually verified to show the correct, fully assembled Medium
  geometry — belly, shoulder, neck taper, collar, and the seated domed lid with its flattened
  plateau apex — in the applied tan matte appearance).
- **Caveat, stated plainly:** this is a clean Fusion viewport capture (via the direct API, not the
  higher-fidelity ray-traced Render workspace, which was not scriptably reachable in the time
  available given the session contention above) — light gridlines and a faint origin-axis line are
  still visible in the background. This is a real limitation of the approach, not a hidden defect;
  a fully polished, grid-free studio composite (there is an unrelated "MI Lightbox" document open in
  this same session that may be intended for exactly this purpose) is a reasonable follow-up but
  was out of scope to chase further given how much of this pass was already consumed by the
  session-contention issue above.
- **Persistence caveat:** the appearance/visibility/position changes were applied and confirmed live
  in the shared session and captured correctly in the exported PNG, but whether they persist in the
  saved Fusion document going forward depends on when/whether that document is next saved — which,
  per the automated save behavior observed above, is not fully under this review's control. The
  exported render file itself is the durable artifact; if a future session finds the live document's
  view state reset, that is expected and does not invalidate this render.

---

## Summary for the Director

- **Approved to proceed, blocked from full production printing** on the neck-ID physical test —
  the same shape of condition already applied to Large and Small, and, per the spec's own honest
  framing, the single most load-bearing instance of this recurring risk across all three sizes so
  far (72mm sits *outside* its own tier's researched competitor range, not just at the low end of
  it).
- Independent geometry re-check (own script, own methodology, different toolchain from the Tester's):
  clean pass, matches spec and the Tester's numbers closely across cavity volume, wall thickness,
  brim OD, plug/bore clearance, and boolean collision-free fit. No contamination found.
- Concept fidelity: correct in kind relative to the established post-v7 identity; one real,
  quantified proportional finding (collar-to-belly ratio continues the same trend Small's review
  flagged, landing at ≈73% — between Large's 65% and Small's 84%), named rather than hidden. The
  line-wide "does no-handle still read as differentiated" check-in recommended after Large's v7 has
  still never happened, now three sizes into the product line — worth the Director's attention at
  the line level.
- Documentation: `medium/README.md` and `medium/parameters.md` do not exist yet — required
  follow-up, not written in this pass.
- Cost: independently sanity-checked, ≈$7.67–9.59 combined filament — cost-effective, no concern.
- Render: produced and verified correct (`medium/render/pet-memorial-urn-medium-hero.png`) only
  after working around real, reproducible, bidirectional shared-session interference (documented in
  full in §4, including the specific technique that worked) — not silently skipped after one
  attempt, per instruction.
