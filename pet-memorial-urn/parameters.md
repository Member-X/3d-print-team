# Parameter Sheet — Pet Memorial Urn (Large, current as-built state, v7, 2026-09-02)

**This document describes the actual final as-built geometry**, not the original planning
derivation. `dot_pipeline/specs.md` has gone through revisions during the build (v1
frustum-stack → v2 tangent-constrained spline → v3 magnet-pocket removal → v4 belly-fullness
edit/wall-rebalance/neck-crease-fix → v5 neck/collar widening + height trim + lid resize → v6
lid-underside alignment plug → v7 handle removal + plug cap + brim/dome rework); where anything
below differs from an earlier section of `specs.md`, this document — and the final export files —
reflect what was actually built and shipped. Full narrative (why each change happened, rejected
approaches, the independent Tester/Reviewer verification at each step) is in
`dot_pipeline/specs.md`, `tests.md`, `verdict.md`, and `review.md` — this document intentionally
doesn't repeat that story in full, only the numbers needed to rebuild or edit the design, plus a
consolidated incident history (§6) since this file has had a real, instructive pattern of
manual-edit incidents worth keeping in one place.

**2026-09-02 update (spec v7, LID ONLY — body and `neck-fit-test` remain unaffected): the handle
was removed entirely, the plug's open tip was capped, the brim was shrunk and thickened to sit
flush with the collar, and the dome base/apex were re-derived to match.** This is the most
significant identity-level change in this project's history — the concept brief that launched this
project named the open-loop handle **"the key differentiating feature"** of the whole design and
called its geometry **"a hard constraint when the Planner moves to CAD."** The requester explicitly
and directly confirmed removing it anyway, fully aware of that reversal. Four other coordinated
changes landed in the same round: the plug's open tip is now capped (6mm hollow + 4mm solid,
creating a genuine sealed void — a `BREP_WITH_VOIDS` solid, confirmed correct by four independent
methods, not a defect); the brim shrank from 122mm to **99.700mm OD** (a deliberate -0.3mm
allowance, flush with the body's 100mm collar, zero overhang) and thickened from 5mm to 10mm; the
dome base shrank from ~97–98mm to **80mm** OD to match; and the dome apex changed from a fully
rounded point to a **flattened 21.73mm-diameter plateau**. Net effect: lid height dropped from 75mm
to 39mm (bounding box 85mm→49mm, a **-42%** reduction), combined assembled height dropped from
≈228.5mm to **≈192.5mm**, and lid material volume dropped from ~228.7 cm³ to **194.2929 cm³**. See
the new §13 below for the full derivation, the honest 21.73mm-vs-22mm-target tradeoff, and the
Reviewer's concept-fidelity assessment — the cumulative effect of this change, layered on the
already-disclosed v4 belly-pinch and persistent banded collar, **reads as generic rather than
differentiated**, per the Reviewer's own words, stated here without softening it. This is not a
blocker (it was an explicit, informed, user-confirmed decision, and the CAD itself is sound), but
the Reviewer recommends a real visual check-in with the requester before this is treated as fully
final — see `README.md`'s "Status" section.

**2026-09-01 update (spec v6, LID ONLY — body and `neck-fit-test` are unaffected): a hollow
cylindrical alignment/friction-fit plug was added to the lid's underside.** The plug hangs 10mm
down from the flat brim underside into the body's 80mm-ID neck bore — **79.5mm OD, 35.75mm ID
(4.0mm wall), 0.5mm diametral clearance** — for a more secure, self-centering engagement than the
v5 flat-on-flat-only seat. A tapered stopper/bung shape was seriously considered and rejected
(full analysis: §5.2.1 of `specs.md`) in favor of this simpler straight-walled design, which
carries less total print-support burden. This is a purely additive lid-underside feature — it does
not touch the neck, collar, belly, height, handle, or body cavity volume, and `urn-body`/
`neck-fit-test` were not re-exported this round. See the new §12 below for the full numbers,
print/support tradeoffs (stated plainly, both the risk and why it doesn't matter), and three-way
independent verification.

**2026-08-31 update (spec v5): the neck/collar were substantially widened (58mm→80mm ID), the
body's overall height was trimmed to compensate (160mm→153.5mm), and the lid was resized to match
(brim 100mm→122mm OD, dome base ~80mm→~97–98mm OD).** This was driven by competitor-benchmarking
market research that found the pre-v5 58mm neck opening a significant outlier against comparable
pet urns (114–121mm openings) and even a direct 3D-printed competitor (~70–100mm estimated) — see
the new §11 for the full numbers, business-fit reasoning, and three-way independent verification.
**The ≈1579 cm³ cavity-volume target established in v4 is unchanged** — it was deliberately held
steady, not grown further, by trimming height to offset the volume the wider neck/collar added.
**This is also the pass that finally brings this document and `README.md` current** — both had
drifted two full revisions behind the as-built CAD (still describing the pre-v4 58mm neck/78mm
collar/160mm height in most places); every section below has been checked and corrected against
the actual v5 geometry, not just patched in the places that were flagged.

**2026-08-28 update (spec v4): the body's belly was manually edited fuller, the inner wall was
reworked to keep tracking it at a constant ~4mm offset, and a separate neck-to-collar crease was
found and fixed.** This grew the internal cavity from ~1511.8 cm³ to **≈1579 cm³** — see §1, §2,
and §10 for the full numbers and verification. The lid was **not** touched by this round (it was
touched by v5, see §4/§11).

**2026-08-28 update (spec v3): the magnet-assisted closure was removed from the CAD entirely**,
per explicit user decision (handle magnet placement themselves at print time or post-print,
outside this model). §3 below is retired — it now only records what existed historically, for
anyone reading old renders/photos or the incident notes in §6, which still narrate real defects
that happened *while the magnet pockets existed*. The pre-removal STEP/3MF/STL (the exact files
described by the original §3) are preserved, unmodified, at `archive/v2-with-magnet-pockets/` for
anyone who needs to see or re-derive that version. §9 has the full removal writeup.

All dimensions in mm unless stated otherwise. Coordinate convention: Z = height from the part's
own base (Z=0), revolved 360° about the Z axis, both parts centered in X/Y at the world origin
in the exported files — print-ready as exported, no repositioning needed.

---

## 1. Body — overall

| Parameter | Value | Notes |
|---|---|---|
| Overall height (base to top of collar rim) | **153.5mm** | **v5** — down from 160mm (v1–v4). The 6.5mm trim came entirely out of the belly-to-shoulder segment (P1→P2, 50mm → 43.5mm) to offset the internal-volume gain from widening the neck/collar; base, belly (absolute height and radius), neck-taper height, and collar height are all otherwise unchanged. |
| External base OD | **98mm** | r=49mm — unchanged through every revision |
| External belly max OD | **~153.93mm** (r=76.966mm ext.) | Plateau spans Z≈66.9–71.4mm — **absolute height and radius unchanged by v5** (the height trim came entirely from the segment below the shoulder, not from the belly itself). Now reads as **~45.0%** of the shorter 153.5mm total (up from ~43–44% of the old 160mm total — the belly didn't move, the denominator it's measured against just got shorter). Internal radius at the apex ≈72.966mm (external minus the verified ~4.00mm wall). |
| External shoulder OD | **~92.84mm** (r=46.42mm ext.) at **Z=112.5mm** (moved down 6.5mm from the pre-v5 Z=119mm) | External radius unchanged since v4 (Reviewer-verified). **Internal radius now VERIFIED at exactly 42.420mm** (Tester, RE-TEST PASS 7, R43) — upgraded from the `ESTIMATED` 42.42mm carried in `specs.md` §4.2.2 (itself a correction of a stale, geometrically-impossible 57mm internal figure that predates v4 — 57mm internal cannot sit inside a 46.42mm external radius). This closes out that flagged estimation risk. |
| External neck OD (below collar, at P3) | **88mm** (r=44mm) at **Z=138.5mm** | **v5** — up from 66mm (r=33mm) at the pre-v5 Z=145mm. DERIVED: 80mm new neck ID + 2×4mm nominal wall (holds the same wall convention used everywhere else in the profile). |
| Collar OD | **100mm** (r=50mm) | **v5** — up from 78mm. DERIVED: 80mm ID + 2×10mm reinforcement wall. The 10mm wall was explicitly **kept**, not reverted to the nominal 4mm, per the requester's own decision — it has had no magnet-housing purpose since v3 and now serves purely as a lid-seating/reinforcement band, kept for structural margin and rim character. |
| Internal neck/collar ID (constant) | **80mm** (r=40mm) | **v5** — up from 58mm. Requester's explicit target, a deliberate compromise short of the 100mm initially considered — see §11 for the full business-fit reasoning (competitor benchmarking, why 80mm and not more). |
| Nominal side wall (design target) | **4mm** | Unchanged — a design convention (heft/"doesn't feel like plastic"), not a print-minimum; well above the 0.8mm (2× 0.4mm nozzle) print-floor |
| Side wall thickness (as-built, verified) | **~4.00mm**; re-confirmed **exactly 4.000mm** at the shoulder (Z=112.5mm) and neck-taper-end (Z=138.5mm) in this round's independent re-test (Tester, R43) | The v4 belly/shoulder-span verification (3.98–4.03mm across ~60 sampled heights) is unaffected by v5 — v5 didn't touch the belly/wall construction, only the ID/OD of the neck/collar downstream of the shoulder and the height allocation between the shoulder and the belly. |
| Floor thickness | **5mm** | Unchanged through every revision |
| Collar wall thickness | **10mm** | (100−80)/2 in v5, was (78−58)/2 = 10 in v2–v4 — same 10mm value carried forward and explicitly re-affirmed at the new, larger size, not reverted to the 4mm nominal wall |
| Internal cavity volume (current, v5) | **≈1579–1580 cm³** — Coder: 1580.25 cm³ (Fusion mass-properties), Tester (independent): 1579.31 cm³ (mesh integration), Reviewer (independent, third method): 1580.2542 cm³ (own numerical revolution-integral of the sampled parametric surface) | Three genuinely different computational methods again converge to within ~0.1% of each other — this number is solid. **The ≈1579 cm³ target established in v4 is unchanged**; the neck/collar widening's estimated +69.16 cm³ volume gain was deliberately offset by the 6.5mm height trim, holding capacity essentially flat rather than letting it climb further (§11). |
| Body material-shell volume (current, v5) | **~278.94 cm³** (Reviewer-measured, live Fusion `physicalProperties.volume`) | Up ~1.0% from the v4 figure (~276.16 cm³) — the larger-diameter collar wall accounts for the small increase. Not separately re-measured by the Coder or Tester as a standalone material-volume check this round (their v5 passes focused on cavity volume and dimensional accuracy); noted here as Reviewer-only, consistent with this project's practice of naming which party measured which figure rather than blending sources. |

## 2. Body profile — final spline-based construction, v4 manual belly edit, v5 neck/collar re-derivation

The body's internal/external profile was originally built as **two tangent-constrained cubic
Bezier-spline curves** (inner cavity boundary + outer wall), not a stack of straight frustum
segments — a full rebuild partway through the project specifically to fix two problems found by
direct visual comparison against `concept/concept-v2.png`: the belly sat too high (56% of height
instead of ~45%), and the straight-line-segment construction produced a visibly faceted body
instead of a smooth curve. **In v4, the belly/shoulder region was directly, manually edited in
Fusion (making the belly fuller)** — a sculpted change layered on top of the spline construction,
not a re-run of the spline math. **In v5, the neck/collar region (P2→P3→P4) was re-derived at new
radii and the shoulder (P2) was relocated 6.5mm lower** to compensate for the added volume,
while the belly (P0→P1) was left completely untouched.

### 2.1 Control points (internal profile; the external wall is built the same way, offset by wall thickness at each corresponding height)

| Point | Z (from base, v5) | Z (from base, pre-v5) | Internal radius | External radius | Tangent condition |
|---|---|---|---|---|---|
| P0 — floor/base | 5mm | 5mm | 45mm | 49mm (at Z=0mm, the true base edge) | Vertical (dr/dz=0) — smooth rounded transition off the flat floor. Unchanged through every revision. |
| P1 — belly apex (broad plateau) | ~68–70mm (plateau, **absolute Z unchanged by v5**) | ~68–70mm | ~72.966mm (derived: external minus the verified ~4.00mm wall) | 76.966mm | Broad, nearly-flat plateau, not a sharp single point. Unchanged in absolute mm by v5 — only its % of total height moved (43–44% of 160mm → ~45.0% of 153.5mm), purely because the denominator shrank. |
| P2 — shoulder (inflection) | **112.5mm** (moved down 6.5mm) | 119mm | **42.420mm — now VERIFIED** (Tester, R43; upgrades the prior `ESTIMATED` figure) | **46.42mm** (Reviewer-verified, v4, unchanged) | All of the v5 height trim (6.5mm) was applied to the P1→P2 segment (50mm → 43.5mm); P1's and P2's own radii are unchanged, only P2's Z-position and the segment height leading to it changed. |
| P3 — neck-taper-end / base of collar | **138.5mm** | 145mm | **40mm** (was 29mm) | **44mm** (was 33mm) | ID/OD widened per §11; P2→P3 segment height held at **26mm, unchanged**. |
| P4 — rim / top of collar | **153.5mm** (= new total height) | 160mm | **40mm** (was 29mm) | **50mm** (was 39mm) | Collar height held at **15mm, unchanged**; constant-radius bore through the collar, same convention as before. |

Construction (pre-v5, still the basis outside the neck/collar): each spline is 3 chained cubic
Bezier segments (P0→P1→P2→P3), built via exact Hermite-to-Bezier control-point math, then inserted
as a `SketchFittedSpline`. This construction method is retained everywhere except the belly (a v4
manual sculpt) and the neck/collar (re-derived at new radii in v5, same tangent conditions). Per
the Tester's RE-TEST PASS 7 (R45), hitting the ≈1579 cm³ target with the new neck/collar radii
required the Coder to tune the spline's tangent-vector scaling — a first-pass construction using
default tangent magnitudes reportedly landed ~6.25% off target before this tuning; the final,
shipped result lands the cavity volume essentially dead-on (§1), independently confirmed.

### 2.2 Volume history — four steps, not a single derivation (why the actual volume isn't a close match to the original ~1475 cm³ target)

A hand-calculable straight-chord (frustum) approximation of the original v2 control-point table
predicted ≈1477.8 cm³ (vs. the 1474.8 cm³ / 90 in³ target — within 0.2%). The **real** v2 spline,
once built, measured **1511.8 cm³ — +2.3% over the target**, because a true tangent-constrained
curve through a true apex bulges outward past the straight-chord approximation near the belly.
This first deviation was within the spec's own pre-authorized ±5% band and was accepted without a
formal spec revision at the time.

**Then, in v4, the user made a direct, intentional manual edit to the outer belly**, making it
visibly fuller, and explicitly chose to **keep** that change. This left the inner wall not
tracking the new outer wall, so the inner wall was reworked to track the outer wall at a constant
~4mm offset (§1). The resulting cavity, **≈1579 cm³, is +6.85% over the original 1474.8 cm³
target** — crossing the spec's own ±5% routine-tolerance band, which is why `specs.md` was
correctly bumped to a formal v4 revision. The user explicitly chose to **accept the larger
capacity** rather than thin the wall below ~4mm to force the volume back down.

**Then, in v5, the neck/collar were widened (58mm→80mm ID)**, which — holding the shoulder and
segment heights fixed — would have added an estimated +69.16 cm³ (a frustum-delta calculation,
`specs.md` §4.2.2, holding the un-recomputable sculpted belly/shoulder region fixed and only
computing the change from the ID/OD widening itself). Rather than letting the ≈1579 cm³ v4 target
grow further, the requester directed a compensating height trim (6.5mm, taken from the
belly-to-shoulder segment) — landing the hand-calculated estimate at ≈1578.6 cm³ (−0.03% vs. the
v4 target). The as-built, independently-verified figure (§1: ≈1579–1580 cm³) confirms this
estimate held essentially exactly. **Net effect: v5 is a re-derivation of the geometry hitting the
same ≈1579 cm³ target established in v4, not a new target.**

### 2.3 Neck-to-collar external blend — three fixes across three revisions, all at the same location (relative to the collar)

The P0–P4 spline above only governs the **internal bore**. The external wall's transition from
the neck OD to the full collar OD has been touched three separate times:

**Fix #1 (pre-v4):** the transition was initially left as a straight conical chamfer (a leftover
from the pre-spline design) — found to be a literal straight line with two sharp corners. Replaced
with a single tangent-constrained cubic Bezier segment, vertical tangent at both ends. Verified via
0.1mm-resolution slope sampling: a genuine smooth S-curve, peak local angle at that time ~45.6°
from vertical.

**Fix #2 (v4, 2026-08-28):** a separate, pre-existing crease at the neck-to-collar junction — a
leftover in the outer wall from how the belly edit reshaped that region — was found and repaired
with a narrowly-scoped fix (only the final 5mm of the outer wall's tail near the rim). Net result
after Fix #1 + Fix #2: peak local angle ~47.25° at Z=147.25mm (pre-v5 Z-coordinates).

**Fix #3 (v5, 2026-08-31):** the neck/collar widening (§11) relocated this blend to
Z≈138.5–145.5mm (from Z=145–152mm) but did **not** require a fresh curve-fitting exercise — the
same tangent-constrained construction method, applied to the same 6mm radius delta (collar OD
minus neck OD — unchanged in both v4 and v5, because the 10mm collar wall sits over the same 4mm
neck wall in both revisions) and the same 7mm height span, reproduces the **identical curve
shape**, just relocated and re-scaled to the new radii. **Independently confirmed to a striking
degree by the Tester** (RE-TEST PASS 7, R46): the measured peak slope value (1.0198915009043685,
45.564° from vertical at Z=143.04mm) matches the pre-widening v4 blend's independently-measured
peak slope (1.0198915009041667, 45.564° from vertical) to **10 significant figures** — confirming
this is mathematically the same curve, not merely "about the same." The Coder independently
measured 45.81°, and the Reviewer (a third, independent method) measured 46.41° at Z=141.9mm — the
~1° spread across three methods is consistent with this project's normal sampling/binning variance
on a continuously curved surface, not a real disagreement; all three land in the same low-risk
band. **Net result: this is the same disclosed, low-risk "watch it on the first print" zone as
every prior revision — not made meaningfully better or worse by v5, just relocated to a lower Z.**

### 2.4 Overhang summary (current, v5)

| Transition | Z range (v5) | Angle from vertical | Category | Risk |
|---|---|---|---|---|
| Base → belly apex | 0–~69mm | Gentle flare throughout | Radius grows with height, but confirmed monotonically non-decreasing (v4 Reviewer re-check, unaffected by v5) | None — genuinely self-supporting |
| Belly apex → shoulder | 69–112.5mm (was 69–119mm) | Average slope steepened slightly (≈31.4°→≈35.1°) due to the shorter 43.5mm span (was 50mm) | Radius shrinks monotonically throughout (shrinking-cone class) | None — steepening the *rate* of shrinking is not the failure mode the overhang guideline protects against |
| Shoulder → neck-taper-end | 112.5–138.5mm (was 119–145mm) | Markedly **gentler** — external Δr shrank from 13.4mm (v4) to 2.4mm (v5), average angle ≈5.3° | Radius shrinks monotonically (shrinking-cone class) | None — meaningfully lower risk than the pre-v5 equivalent segment |
| Neck-to-collar blend | ~138.5–145.5mm | **~45.6–46.4°** peak, depending on method (Coder 45.81°, Tester 45.56° at Z=143.04mm, Reviewer 46.41° at Z=141.9mm) — bit-identical (10 sig figs, Tester) to the pre-v5 blend's peak slope | Radius grows with height (real overhang class, but on a short, fully closed 360° revolve) | Low — same disclosed "watch it on the first print" band as every prior revision, just relocated. This is the **only** zone anywhere on the entire outer wall that exceeds 45° (confirmed by full-span sweep, Tester R46). |

## 3. Magnet-assisted closure — REMOVED 2026-08-28, this section is historical only

**As of spec v3 (2026-08-28), this feature no longer exists in the model**, and v5 did not touch
this decision. The table below is kept verbatim as a historical record — it does **not** describe
the current geometry. The current body and lid have no pockets, bosses, or recesses of any kind;
the collar top and the lid underside are both plain, uninterrupted flat surfaces (re-confirmed
clean in v5's own re-test, R44).

| Parameter | Value (historical — no longer modeled) |
|---|---|
| Magnet type | 6mm diameter × 2mm thick neodymium disc, N42 (commodity size) |
| Count | 6 total — 3 in the body collar top, 3 in the lid underside |
| Bolt circle radius | **34mm** (the true midline of the *then*-10mm-thick collar wall at its *then*-78mm OD) |
| Spacing | 120° apart (3-fold symmetry) |
| Pocket size | 6.2mm diameter × 2.2mm deep (0.2mm oversize) |
| Embedding method | Post-print: print open-face pockets, insert magnets after printing, secure with CA glue or epoxy |
| Polarity | Mark before gluing — all 3 lid magnets same pole down, all 3 body magnets same pole up |
| Verified margin | 1.9mm of solid material on both the inner and outer side of every pocket |

**Why it was removed:** the user decided to handle any magnet placement themselves, either via a
slicer-level pause-and-embed workflow or a fully manual post-print drill-and-glue step, rather
than have it pre-modeled. This was a deliberate scope reduction, not a defect fix.

## 4. Lid

**Substantially reworked in v5** (brim OD and dome base OD both resized to match the wider collar),
**further modified in v6** (a hollow alignment/friction-fit plug added to the underside, §12), and
**substantially reworked again in v7** (handle removed entirely, plug tip capped, brim shrunk to
flush and thickened, dome base/apex re-derived — §13). **The handle no longer exists as of v7** —
every row below describing it is retained for historical comparison only.

| Parameter | Value (v7, CURRENT) | Value (v6, superseded) | Value (v5, superseded) | Value (v1–v4, superseded) |
|---|---|---|---|---|
| Total lid height, seating plane to top of dome/plateau (excludes plug) | **39mm** (10mm brim + 29mm dome, §13) | 75mm | 75mm | 75mm |
| Total lid bounding-box height (includes plug hanging below the seating plane) | **49mm** (39mm + 10mm plug, §13) | 85mm | N/A — no plug | N/A — no plug |
| Flat brim disc OD | **99.700mm** — flush with the body's 100mm collar, zero overhang; a deliberate -0.3mm allowance below nominal 100mm (§13) | 122mm | 122mm | ~~100mm~~ |
| Brim thickness | **10mm** (§13) | 5mm | 5mm | 5mm |
| Dome height above brim top | **29mm** (§13 — a ~1mm reduction from 30mm, an expected consequence of blending the apex to a flat plateau rather than a point) | 30mm | 30mm | 30mm |
| Dome base OD (where it meets the brim) | **80mm exact** (§13 — re-derived via the same 0.80 dome-to-brim ratio used since v1, applied to the new 99.700mm brim; independently confirmed via live STEP sphere/placement math) | ~97–98mm | ~97–98mm | ~~80mm~~ (same absolute value as v7, for an unrelated reason) |
| Dome apex | **Flattened plateau, 21.7283mm diameter** (r=10.8642mm) — replaces the fully-rounded point apex used in every prior revision. Target was ~22mm; genuine tangency and an exact 22.00mm turned out to be mutually exclusive at this geometry, and tangency was correctly prioritized (§13) — 27.16% of the 80mm base vs. the 27.5% originally intended, a negligible practical difference. | N/A — fully rounded point apex | N/A — fully rounded point apex | N/A — fully rounded point apex |
| Plug — OD / wall / depth | **79.5mm OD, 4.000mm wall, 10mm total depth — now CAPPED at the tip (v7): 6mm hollow nearest the brim + 4mm solid disc nearest the tip** (§13) | 79.5mm OD, 4.000mm wall, 10mm deep — **open at the tip** | N/A — no plug | N/A — no plug |
| Seating interface | Flat brim plane, **flush** on the body's flat 100mm-OD collar rim (zero overhang, replacing the prior overhanging designs), **plus the capped alignment plug** above — 0.500mm diametral clearance friction fit into the body's 80mm-ID neck bore, plug tip 5.0mm clear of the body's internal taper (P3), no collision. Full derivation: §13 below, `specs.md` §5.1/§5.2.2. | Flat brim plane on the 100mm collar rim, **11mm/side overhang** (122mm brim), plus the same plug **open at the tip**. | Single flat plane only, 11mm/side overhang. **No plug/skirt/alignment lip.** | Same flat-only interface, 78mm-OD collar, 11mm/side overhang. |
| Handle clear opening | **REMOVED ENTIRELY, v7 — no handle, no opening, no replacement grip feature of any kind** (§13 — confirmed clean removal via a full face-inventory audit: 13 `ADVANCED_FACE` entities exactly accounted for, no orphaned geometry) | 24mm wide × 22mm tall | 24×22mm | 24×22mm |
| Handle bail cross-section | **REMOVED, v7 — N/A** | 9mm round | 9mm round | 9mm round |
| Handle height above dome apex | **REMOVED, v7 — N/A** (the flattened dome plateau is now the top of the part) | 40mm | 40mm | 40mm |
| Fillet at handle-to-lid junction | **REMOVED, v7 — N/A** | 4mm | 4mm | 4mm |
| Handle load case | **REMOVED, v7 — N/A.** User grips the brim/dome edge by hand instead; see the usability/drop-risk note in §13. | Rated only for lifting the lid's own weight | Same | Same |
| Lid material-shell volume | **194.2929 cm³** (§13 — a real decrease from v6, despite the thicker brim and capped plug tip, because the shrunk brim and removed handle outweigh them) | ~228.7 cm³ (~219.2 cm³ v5 base + ~9.49 cm³ from the hollow plug) | ~219.2 cm³ (Reviewer-measured) | ~151.0–151.16 cm³ |

**Construction method note (historical, v5/v6 — the handle it describes no longer exists as of
v7):** the brim/dome were grown via a **non-uniform scale (X=Y=1.22, Z=1.0) applied to the v4 lid
geometry, before the handle/plinth features were added**. Because the handle was modeled *after*
the scale, at its own absolute dimensions, it was never itself scaled — this is why the 24×22mm
opening measured identical to every pre-v5 figure for this feature at v5/v6, confirmed
independently by two different methods (mesh cross-section sweep and solid point-containment
query). **As of v7, the handle and its supporting plinth features were deleted from the timeline
entirely**, and the brim/dome were rebuilt via a fresh sketch/revolve targeting the new
99.700mm/80mm/29mm/21.73mm figures directly (not a further scale operation). The clean removal was
independently confirmed by a full face-inventory reconciliation (13 `ADVANCED_FACE` entities — 6
planes, 3 cylinders, 1 sphere, 3 toruses — exactly matching the expected count, with no leftover
handle/plinth fragment) and a component-count reconciliation (2 mesh components, fully explained by
the sealed plug void, no unexplained third island) — see §13 for the full verification.

**Brim OD reasoning, v5/v6 (historical — superseded by v7's flush-fit derivation below):** the
v1–v4 lid overhung its 78mm collar by 11mm/side with a 100mm brim. Preserving that *ratio*
(100/78 = 1.282) onto the new 100mm collar would give ≈128.2mm and grow the *absolute* overhang to
~14.1mm/side. Preserving the *absolute* overhang margin instead (11mm/side) gave 100 + 22 = 122mm —
the value built at v5/v6. **v7 replaces this entire overhang-preservation approach with a
flush-fit derivation** — see §13.

**Dome base OD reasoning, v5/v6 (historical — superseded by v7's re-derivation below):** the
v1–v4 dome base (~80mm) sat inside a 100mm brim at a ratio of 0.80. Applying the same ratio to the
v5/v6 122mm brim gave ~97.6–98mm. **v7 re-applies the identical 0.80 ratio to the new 99.700mm
brim, landing back on 80mm exactly** — see §13.

## 5. Material assignments

| Part | Material | Why |
|---|---|---|
| Body | Matte or silk PLA | The body's large smooth, undecorated curved surfaces are what most need the matte/silk "not plastic-feeling" finish — PLA has a wider selection of matte/silk filament options than PETG. Unaffected by v5's dimensional changes. |
| Lid | **PETG** | Originally chosen (v1) because the handle root fillet was the feature most exposed to a knock or repeated cyclic grip load — PETG's better impact toughness and interlayer adhesion addressed that directly. **This specific justification is now stale as of v7: the handle no longer exists.** PETG is being kept anyway for its general toughness on the lid's remaining thin-fillet transitions (the brim-to-dome compound fillet, the dome-to-plateau fillet, the plug wall) and to avoid introducing a new material-behavior variable into an otherwise-settled design — this is a carried-forward default, not a fresh v7-specific derivation, stated here plainly rather than silently re-asserting the original (now partly moot) reasoning. |

**PETG-specific considerations:** higher print temperature and slower cooling than PLA (relevant
at the dome apex — previously a known, minor, cosmetic-only drooping risk on the fully-rounded
point apex; **as of v7 the apex is a flattened plateau, which eliminates this specific risk
mechanism entirely, not just reduces it** — see §13); no orientation change needed
(flat-underside-down remains best-case for PETG's bed-adhesion/warping tendencies too, and remains
the correct orientation post-v7 — see §13's print-orientation re-check).

**Fusion appearance (render-only, not a printed property):** body = **"Matte PLA - Stoneware Tan
(urn-body)"**, lid = **"Matte PETG - Stoneware Tan (urn-lid, sanded)"**. Both custom appearances
survived the v5 rebuild intact this time — unlike the v4 round, where the body's appearance was
found silently reverted to Fusion's default "Steel - Satin" after a timeline rebuild (§6.5) and
had to be reapplied, the Reviewer confirmed in the v5 pass that both custom appearances were
already correctly set when preparing the fresh v5 render, with nothing to fix this round.

Neither material assignment is embedded in the exported files in a slicer-readable way — both
must be set manually in the slicer. The body's `3mf` carries a free-text 3MF
`<metadata name="Description">` field with the material note; the lid's does not.

## 6. Incident notes — eight recorded events across this build: five real incidents plus three deliberate scope/feature changes (read before editing further)

This live Fusion document has a real, repeating pattern worth keeping in one place for future
editors: **eight recorded events** across the project's lifetime — five genuine incidents (a mix
of scripted-cut mistakes, direct manual UI edits, one silent side effect of an otherwise-legitimate
timeline rebuild, and one stray/unexplained feature pair caught before it could do any damage)
plus **three deliberate, user-directed changes that are not incidents** (§6.4 — the magnet-pocket
removal; §6.7 — the v6 lid-underside alignment plug addition; §6.8 — the v7 handle removal/lid
rework; all narrated here for continuity since they touch the same region of the file/project
history, not because any of them was a mistake). Listed chronologically; full technical detail is
in the subsection or cross-referenced section named for each.

**Standing recommendation, reaffirmed after every incident below:** prefer timeline-native,
script-driven parametric edits over direct manual dragging of sketch/BRep geometry in the Fusion
UI for this file. If a manual edit is ever unavoidable, treat it as a higher-scrutiny change
requiring an explicit before/after geometry check (volume, face count, slope continuity, and
appearance/material assignment — §6.5), not just a visual glance in the viewport.

### 6.1 Cross-component `participantBodies` leak (original base-pocket defect) — pre-approval

**Root cause:** `ExtrudeFeatureInput.participantBodies` defaults to "all bodies geometrically
intersected by the cut" when left unset. Because `urn-body`, `urn-lid`, and `neck-fit-test` are
all separate components sharing the same local origin, an unrestricted cut in one component's
sketch leaked into a completely unrelated body, producing 3 unintended pockets on the body's base
— dimensionally identical to the legitimate collar pockets, which is why it initially looked
plausible rather than a bug. This is a standing risk for this file, not a one-off mistake; every
subsequent cut/extrude has explicitly restricted `participantBodies`.

### 6.2 Manual sketch edit corruption + recovery — pre-approval

A direct manual edit to the `BodyProfile` sketch (in the Fusion UI, not via script) left the
sketch as an open, non-closed loop, collapsing the neck opening. `Revolve1` was left running on a
degenerate 4.45 cm³ fragment. The profile was rebuilt from the last fully-verified configuration
(not salvaged from the broken edit's implied intent), cascade-deleting and recreating the
dependent `Extrude1` with `participantBodies` explicitly restricted this time. Independently
re-verified afterward: cavity volume, belly position, and shoulder-region radii all matched the
pre-incident measurements exactly.

### 6.3 Third manual-edit incident — collar/neck manual drag (post-approval, 2026-08-27)

A user-described edit "near the lid magnet pocket" turned out to have left the lid untouched — the
actual damage was a manual drag on the body's neck/collar region, ballooning the collar ID/OD from
58mm/78mm to ~70.7mm/~90.4mm, which indirectly clipped the (then-still-existing) magnet pockets.
Recovered by reproducing the exact previously-verified control-point/tangent recipe. Independently
re-verified by both the Tester and the Reviewer (own `trimesh` script) against the pre-v4 design
state then in effect — every checked figure matched exactly or to normal mesh-resolution noise.

### 6.4 Magnet-assisted closure removed from CAD (2026-08-28, spec v3) — deliberate scope reduction, not a defect

Per explicit user decision, both magnet-pocket cut features were deleted outright from both parts.
This was **not** a defect fix — see §3 for the historical record of what was removed and §9 for
the full removal writeup and re-verification.

### 6.5 v4 belly-fullness edit, inner-wall rebalance, neck-to-collar crease fix, and appearance-reversion catch (2026-08-28, spec v4)

A deliberate, user-directed aesthetic edit (fuller belly) with a genuine volume consequence the
user explicitly chose to accept, plus one incidental side-effect catch: the body's render
appearance had silently reverted to Fusion's default "Steel - Satin" (a side effect of the
`Revolve1` recreation resetting the body's appearance override). The correct custom appearance was
still defined in the document, just not applied; it was reapplied and saved. This is the second
time a timeline-native rebuild silently reset something adjacent to the geometry it touched (the
first being the `participantBodies` default itself, §6.1). Full detail: §10.

### 6.6 Stray, unexplained fillet-feature pair found and removed before the v5 body rebuild (2026-08-31, spec v5)

At the start of this round's work — **before any v5 geometry changes began** — a pair of stray,
unexplained fillet features (`Fillet4`/`Fillet5`) was found in the live Fusion timeline. Their
origin is unexplained: no record of who or what created them, and no correspondence to any
documented feature or spec requirement anywhere in this project's history. They were cleanly
removed before the v5 body rebuild started. **This is the fifth genuine incident on this file**
(the magnet-pocket removal, §6.4, is a deliberate scope change and is not counted in this tally).
Unlike incidents 6.1–6.3/6.5, this one never made it into any shipped export — it was caught in
time during pre-work inspection, not discovered after the fact in an already-exported file — so no
re-verification of previously-shipped files was needed for this specific item. It is recorded here
anyway because it fits this file's established pattern (five incidents now, all on the same live
document) and because the standing recommendation above (prefer scripted, timeline-native edits;
treat any manual edit as a higher-scrutiny change) is worth reaffirming again at this frequency.

### 6.7 Lid-underside alignment plug added (2026-09-01, spec v6) — deliberate feature addition, not a defect

Per explicit user request, a hollow cylindrical alignment/friction-fit plug (79.5mm OD × 10mm
deep, 4.0mm wall) was added to the lid's underside, engaging the body's 80mm neck bore for a
0.5mm diametral clearance fit. This was **not** a defect or incident recovery — it is a deliberate
feature addition, built and exported cleanly on the first attempt, independently re-verified by
Coder, Tester, and Reviewer with no residual issues found. Full detail: §12. Listed here (not
counted in the five-incident tally, same convention as §6.4's magnet removal) purely for
continuity, since this section is this project's running change/incident log.

### 6.8 Handle removed entirely, plug capped, brim shrunk+thickened to flush, dome apex flattened (2026-09-02, spec v7) — deliberate feature change, not a defect

Per explicit, direct user confirmation — made with full awareness that it reverses the original
concept brief's own "hard constraint" language around the open-loop handle — the handle was deleted
entirely from the lid, the plug's open tip was capped with a solid 4mm disc, the brim was shrunk to
99.700mm OD (flush with the collar) and thickened to 10mm, and the dome base/apex were re-derived
(80mm base, 29mm height, 21.73mm flattened plateau). This was **not** a defect or incident recovery
— it is the largest deliberate feature change in this project's history, built and exported
cleanly, independently re-verified by Coder, Tester (two methods), and Reviewer (a live B-rep
query) with no residual issues found and no orphaned geometry from the handle's removal. Full
detail: §13. Listed here (not counted in the five-incident tally, same convention as §6.4/§6.7)
purely for continuity, since this section is this project's running change/incident log.

## 7. `neck-fit-test` standalone article

**Rebuilt in v5 to represent the new neck/collar dimensions — this is a real correction to
previous documentation, read this section even if you've read an earlier version of this file.**
**Unaffected by v6 or v7** — both rounds only touched the lid (a plug addition in v6; handle
removal/plug cap/brim+dome rework in v7); this article was not re-exported by either and still
represents the same 2026-08-31 v5 geometry described below.

A small (~35mm tall, ~144mm max OD at the stabilizing base flange — up from ~122mm in the pre-v5
article, sized proportionally larger for the wider collar) standalone print of just the neck taper
+ collar section (flange-cut at the bottom for bed stability, open bore both ends), built
specifically so the requester can physically test whether a real crematorium remains bag fits
through the neck opening.

Confirmed (Tester, RE-TEST PASS 7, R50): **80mm ID** (r=40.000mm constant, Z≈20.5mm to top),
**88mm neck OD** (r=44.0–44.4mm at the P3 handoff), **100mm collar OD** (r=50.000mm constant,
Z=28–35mm), ~4.00mm wall through the flange-to-neck taper — all exactly matching the body's own
current v5 neck/collar dimensions. Watertight, single manifold solid, self-supporting in its
natural flange-down orientation (the flange-to-neck taper shows zero locally-increasing-radius
steps, the shrinking-cone self-supporting class; the collar-widening blend peaks at ~40.6° from
vertical, comfortably under the 45° guideline).

**Correction to earlier documentation:** prior revisions of this document and of `README.md`
described this article as "unaffected by the belly/collar edits" and representing "58mm ID,
78mm/66mm collar/neck OD." **That description was accurate through v4 but is now wrong.** As of
v5, this file was explicitly and deliberately rebuilt (per `specs.md` §2's "v5 flag — the
`neck-fit-test` article is easy to overlook and MUST NOT be forgotten this round") to represent
the new **80mm ID / 88mm neck OD / 100mm collar OD** geometry. This correction matters concretely:
the entire purpose of this article is a physical go/no-go test, and printing it under the old,
stale description would validate the wrong opening size and give a false sense of confidence about
geometry that no longer matches the shipped body.

**This is the requester's own physical test to run, and it has not been run yet.** Per both the
Tester's and Reviewer's v5 assessments, **this is now the single most load-bearing open item in
the entire project** — this whole v5 revision's business justification (choosing 80mm) rests on an
assumption about real remains-bag size that remains physically unverified. See `README.md`'s
Status section.

**Note on hole shrinkage:** FDM parts typically print circular IDs slightly undersized versus the
model. No compensation has been baked into the 80mm nominal ID for the same reason as before —
there's no fixed target diameter to compensate toward, since this is an untested fit against a
real bag, not a hardware spec. Check the actual as-printed ID on this test article before assuming
80mm nominal is what comes off the printer.

## 8. Files

| File | Contents |
|---|---|
| `step/urn-body.step` | Current body — **still v5 geometry, UNCHANGED by v6 or v7** — re-editable, reflects the neck/collar widening + height trim (§1, §2, §11). Not re-exported since. |
| `3mf/urn-body.3mf` | Current body — **still v5, UNCHANGED by v6 or v7**, slicer-ready. Timestamp remains 2026-08-31 08:27. |
| `stl/urn-body.stl` | Current body — **still v5, UNCHANGED by v6 or v7**, universal fallback. Timestamp remains 2026-08-31 08:27, independently re-verified watertight. |
| `step/urn-lid.step`, `3mf/urn-lid.3mf`, `stl/urn-lid.stl` | Current lid (**v7**) — handle removed entirely, plug tip capped, brim shrunk+thickened to 99.700mm OD × 10mm (flush with the collar), dome base/apex re-derived to 80mm OD × 29mm tall with a 21.73mm-diameter flattened plateau (§4, §13). Re-exported 2026-09-02 17:32. |
| `archive/v2-with-magnet-pockets/urn-body.{step,3mf,stl}`, `archive/v2-with-magnet-pockets/urn-lid.{step,3mf,stl}` | Superseded pre-magnet-removal versions, preserved unmodified — not the current print files |
| `archive/pre-plug-lid-v5/urn-lid.{step,3mf,stl}` | Superseded lid — the v5 lid (122mm brim, ~97–98mm dome, handle intact) from just before the v6 plug was added — preserved unmodified — not the current print files |
| `archive/pre-v7-handle-removal/urn-lid.{step,3mf,stl}` | Superseded lid — the v6 lid (open-loop handle, 122mm overhanging brim, ~97–98mm dome, open-tip plug) from just before the v7 revision — preserved unmodified, kept specifically for a real handle-vs-no-handle comparison, not the current print files |
| `step/neck-fit-test.step`, `3mf/neck-fit-test.3mf`, `stl/neck-fit-test.stl` | Standalone neck/collar fit-test article, **rebuilt in v5, UNCHANGED by v6 or v7** — represents the 80mm ID / 88mm OD neck / 100mm OD collar dimensions (§7). Timestamp remains 2026-08-31 08:27. |
| `render/pet-memorial-urn-hero.png` | **Current** hero render — depicts the v7 exterior geometry (handle removed, flush brim, flattened dome plateau); re-shot fresh for v7 since the handle removal materially changes the exterior silhouette (§13) |
| `archive/pre-v7-handle-removal/pet-memorial-urn-hero.png` | Superseded hero render — the v6 exterior (handle + overhanging brim), recovered from git history and archived alongside the pre-v7 STEP/3MF/STL above (it had existed but was not previously archived) — preserved for reference and for the recommended visual check-in, `README.md` "Status" |
| `archive/pre-v5-neck-widening-render/pet-memorial-urn-hero.png` | Superseded hero render from before the v5 neck/collar widening (v4-era, dated 2026-08-28) — preserved for reference |
| `archive/pre-v4-belly-render/pet-memorial-urn-hero.png` | Further-superseded hero render from before the v4 belly edit — preserved for reference |
| `dot_pipeline/specs.md` | Full spec, including the v1→v2→v3→v4→v5→v6→v7 revision history |
| `dot_pipeline/tests.md`, `verdict.md` | Full independent verification history across all build/fix rounds, including RE-TEST PASS 7 (v5), RE-TEST PASS 8 (v6 plug), and RE-TEST PASSES 9–10 (v7) |
| `dot_pipeline/review.md` | Reviewer's independent re-verification and approval, including the "FULL RE-REVIEW — v5 major revision" pass, "ADDENDUM 4 — v6 lid plug," and "FULL RE-REVIEW — v7 major lid revision" |

## 9. Magnet-pocket closure removal (2026-08-28, spec v3) — what changed, how it was verified

**What was removed:** the two magnet-pocket cut features only — `Extrude1` in `urn-body` and
`Extrude5` in `urn-lid`, both deleted outright from the timeline. Re-verification at the time
confirmed: body count unchanged (1 solid per component), face/edge counts dropped by exactly the
expected amount, volume increased by the exact theoretical filled-pocket volume, both parts
remained single-connected-component and fully edge-manifold. Full detail preserved from the
original documentation pass below.

**Note: the collar OD/ID/wall figures quoted in the original writeup below (78mm/58mm/10mm) were
accurate as of the v3 removal and remained accurate through v4.** They are **superseded by v5's
neck/collar widening** (§1, §11) — current values are 100mm/80mm/10mm. Nothing about the removal
itself or its verification is affected by that later change; this note exists purely so a reader
doesn't mistake the historical figures below for current ones.

**What was explicitly not touched, confirmed by the checks at the time:** body profile/spline/
belly/shoulder/neck (as they existed at the time — subsequently changed by v4 and then v5), collar
OD/ID/wall/height (78/58/10/15mm at the time — subsequently changed by v5's neck/collar widening),
lid dome/brim/handle geometry (subsequently changed by v5's resize), material assignments, print
orientations, `neck-fit-test` (subsequently rebuilt by v5).

## 10. v4 belly-fullness edit, inner-wall rebalance, and neck-to-collar crease fix (2026-08-28, spec v4)

**This section describes the v4 round specifically and is kept as historical record — its
neck/collar/height figures (66mm neck OD, 78mm collar OD, 160mm total height) were accurate at the
time but are superseded by v5 (§1, §2, §11). Nothing below is inaccurate about what happened in
v4; it simply predates the v5 changes.**

### Sequence of changes

1. The user manually edited the body's outer belly in Fusion to make it visibly fuller, and
   explicitly chose to keep that change.
2. This left the inner wall not tracking the new, fuller outer wall. The user directed a rework of
   the inner wall to track the outer wall at a constant ~4mm offset.
3. The resulting cavity volume, ≈1579 cm³, is structurally larger than the original target allows.
   The user explicitly chose to accept the larger capacity. This crossed the spec's own ±5%
   routine-tolerance band, which is why `specs.md` was formally revised to v4.
4. A separate, unrelated crease at the neck-to-collar junction was found and repaired with a
   narrowly-scoped fix (§2.3, Fix #2).
5. Incidental catch: the body's Fusion appearance was found silently reverted to the default
   "Steel - Satin" — a side effect of the `Revolve1` recreation. Reapplied and saved.

### Independent cross-verification (three parties, three methods) — v4 figures, since superseded by v5 for neck/collar/height (unaffected for belly/wall)

| Check | Coder | Tester | Reviewer |
|---|---|---|---|
| Cavity volume (v4) | 1578.9824 cm³ | 1578.11 cm³ | 1578.79 cm³ |
| Material (shell) volume (v4) | 275.9651 cm³ | — | 276.1556 cm³ |
| Belly apex, external radius | 76.97mm | 76.97mm | 76.9659mm at Z=69.00mm |
| Belly apex, height (as % of 160mm) | ~43–44% (plateau) | ~43–44% (plateau) | 43.12% (plateau Z=66.9–71.4mm) |
| Wall thickness (belly/shoulder span) | ~4.00mm | ~4.00mm | ~4.000mm exactly, Z=10–140mm |

The belly apex external radius (76.97mm) and wall-thickness figures above remain current and
unaffected by v5. The cavity/material volumes above are the v4 figures — see §1 for the current v5
figures (which land at essentially the same ≈1579 cm³ cavity target, by design, §11).

### Concept-fidelity note (v4) — a real, incremental drift, named plainly at the time

Comparing the v4 render against the approved `concept/concept-v2.png`: the built design's
belly-to-neck proportions read noticeably more pronounced/pinched than the concept image's
gentler taper — a "ginger jar" silhouette layered on top of the already-disclosed "banded collar"
drift. **This finding is directly addressed by v5** — see §11's concept-fidelity note below, which
found the wider v5 neck actually *improves* this ratio rather than worsening it further.

## 11. v5 neck/collar widening, height trim, and lid resize (2026-08-31, spec v5)

### Why this happened

Competitor-benchmarking market research found the pre-v5 58mm neck ID to be a significant outlier
against comparable pet urns (114–121mm top openings) and even a direct 3D-printed competitor
(~70–100mm estimated opening) — the 58mm figure had been flagged as an untested `ESTIMATED`
assumption since v1 of this spec and was never closed out. This research is what finally gave a
concrete, external reason to revisit it.

### The business-fit decision — why 80mm, not the full 100mm considered

The requester considered widening the neck all the way to 100mm (matching the top end of what the
research suggested) but settled on **80mm** as a deliberate compromise, specifically to avoid the
collar OD exceeding the body's 98mm base OD. At 80mm ID + the kept 10mm collar wall, the collar OD
lands at 100mm — essentially at parity with the 98mm base (a 2mm/1mm-radius difference), preserving
the vessel's visual hierarchy (belly is still unambiguously the widest, most dominant feature,
independently confirmed via a live Fusion screenshot, Reviewer R52/§11.2 below) rather than
inverting it. 80mm sits at the **low end** of the cited 3D-printed-competitor range (70–100mm) and
well below the ceramic-competitor range (114–121mm) — the Reviewer's own independent judgment,
reached without accepting the spec's framing at face value: **"80mm meaningfully reduces the risk,
it does not retire it."** The `neck-fit-test` article (§7) is what actually closes this out, and it
has not been printed/tested yet.

### Target numbers (requester's decision, re-derived in `specs.md` §4.2.2)

| Feature | Old (v4) | New (v5) |
|---|---|---|
| Neck ID (constant through collar) | 58mm (r=29mm) | **80mm (r=40mm)** |
| Neck OD, below collar (P3) | 66mm (r=33mm) | **88mm (r=44mm)** |
| Collar ID | 58mm | **80mm** |
| Collar OD | 78mm (r=39mm) | **100mm (r=50mm)** |
| Collar wall thickness | 10mm | **10mm — unchanged, kept deliberately** |
| Collar height | 15mm | **15mm — unchanged** |
| Body overall height | 160mm | **153.5mm** |

### Volume math summary (full derivation in `specs.md` §4.2.2)

Widening the neck/collar ID, holding the shoulder (P2, r=42.42mm internal) and segment heights
fixed, was estimated to add **+69.16 cm³** (a frustum-delta calculation across the P2→P3 and
P3→P4 segments only — the un-recomputable sculpted belly/shoulder region was deliberately left out
of this recalculation and referenced only by its already-verified radius). Rather than letting the
v4 target (≈1579 cm³) grow to ≈1648 cm³, a compensating **6.5mm height trim** was taken entirely
from the belly-to-shoulder segment (the single largest-volume segment, the only one able to absorb
this trim without a large relative change) — landing the hand-calculated estimate at ≈1578.6 cm³
(−0.03% vs. target). The as-built, independently-verified figure (§1: ≈1579–1580 cm³, three
methods within 0.1% of each other) confirms this estimate held.

### Independent cross-verification (three parties, three methods) — v5

| Check | Coder | Tester | Reviewer |
|---|---|---|---|
| Cavity volume | 1580.25 cm³ | 1579.31 cm³ | 1580.2542 cm³ |
| Belly apex (radius / Z) | 76.966mm / z≈69.11mm | 76.964mm / z=69.0mm | 76.9660mm / z=69.076mm |
| Shoulder (P2) ext/int radius | 46.42mm / 42.42mm | 46.420mm / 42.420mm | 46.4200mm / 42.4200mm |
| Neck-taper-end (P3) ext/int radius | 44mm / 40mm | 44.000mm / 40.000mm | 44.0000mm / 40.0000mm |
| Collar (P4) ext/int radius | 50mm / 40mm | 50.000mm / 40.000mm | 50.0000mm / 40.0000mm |
| Neck-to-collar blend peak angle | 45.81° | 45.56° (bit-identical to pre-widening v4 blend, 10 sig figs) | 46.41° |
| Lid brim OD | 122mm | 122.00mm | 122mm (bounding box ±61.0mm) |
| Lid dome base OD | ~97.2mm | ~97.3mm | ~97.2mm |
| Lid handle opening | 24×22mm, unchanged | 24×22mm, y=−4 to +4mm | Confirmed via direct point-containment query (a more direct method than a mesh sweep) |

Every dimension checked matches to at least 3 significant figures across all three independent
methods. The one figure that moved from `ESTIMATED` to `VERIFIED` this round is the shoulder's
internal radius (42.420mm, Tester R43) — previously flagged in `specs.md` §4.2.2 as needing
re-verification against the actual rebuilt geometry, now closed out.

### Overhang re-check

See §2.4 above for the current full-span summary. **Net finding: no new overhang risk introduced
anywhere.** The belly-to-shoulder segment steepens slightly (still self-supporting, shrinking-cone
class); the shoulder-to-neck-taper segment gets markedly gentler; the one pre-existing risk zone
(neck-to-collar blend) is confirmed — independently, to 10 significant figures by one method — to
be the mathematically identical curve as the pre-v5 blend, just relocated to a lower Z. Same
low-risk "watch it on the first print" band as every prior revision.

### Concept-fidelity note — a genuine partial correction, not an additional drift

The Reviewer's independent visual comparison against `concept/concept-v2.png` found that the wider
neck moves the belly-to-opening (collar OD ÷ belly OD) ratio from **~51% (pre-v5: 78mm/153.9mm)
to ~65% (v5: 100mm/153.9mm)** — closer to the concept image's own visibly wider-mouthed
proportions, not further away. **This is a genuine, if partial, correction of the v4
"belly-pinch"/"ginger jar" drift named in §10 above, not an additional drift layered on top of
it.** The shoulder-to-neck-taper transition also reads visibly smoother in the fresh v5 render, a
direct visual consequence of that segment's angle getting gentler (§2.4). The "banded," constant-
radius collar band itself is unchanged in kind — still a distinct 15mm cylindrical section, just
larger in absolute terms — the same disclosed, functionally-necessary drift from every prior
revision, not made newly more noticeable by v5. Full detail: `review.md`'s v5 full re-review, §2.

### Cost impact — a real, named increase, driven almost entirely by the lid

| Part | v4 material volume | v5 material volume | Change |
|---|---|---|---|
| Body | ~276.16 cm³ | **278.94 cm³** | +1.0% (larger collar wall at a bigger OD) |
| Lid | ~151.0 cm³ | **219.20 cm³** | **+45.2%** (brim +22%/dome +21% linear growth compounds substantially in volume) |

At PLA (~1.24 g/cm³) and PETG (~1.27 g/cm³) densities: body ≈346g (~$7–8.7 in filament), lid
≈278g (~$5.6–7). **Combined pair: roughly $12.5–16**, up from the ~$8–12 figure carried through
every prior revision of this project's documentation. This is still a small, entirely reasonable
cost for a decorative memorial piece — this is not a problem, but it is a real, ~30–40% increase
that should be stated plainly rather than repeating the old range unchanged.

### Documentation currency — this pass

Both `README.md` and this document had fallen two full revisions behind the as-built CAD (still
describing the pre-v4 58mm neck / 78mm collar / 160mm height as of this pass starting), including
in the `neck-fit-test` description — the exact kind of stale-instruction risk that matters most
when a document is telling someone what to physically test. Both documents were brought current in
this pass; the specific stale figures corrected are listed in this repo's task history for this
documentation round.

### Render refresh

The pre-v5 hero render (v4-era, dated 2026-08-28) no longer depicted the shipped design once the
neck/collar/height/lid changed. A fresh render was produced from the live v5 geometry — both custom
appearances were already correctly applied (no reversion this time, unlike v4), the lid was
temporarily raised to its true 153.5mm seated height for the render only and reverted afterward.
Saved to `render/pet-memorial-urn-hero.png`; the v4-era render is preserved at
`archive/pre-v5-neck-widening-render/pet-memorial-urn-hero.png` (and the pre-v4 render remains
further archived at `archive/pre-v4-belly-render/pet-memorial-urn-hero.png`).

## 12. v6 lid-underside alignment plug (2026-09-01) — full derivation, print tradeoffs, and three-way verification

**Scope: lid only.** `urn-body` and `neck-fit-test` were not touched or re-exported this round —
timestamps for both remain 2026-08-31 (v5). Nothing about the neck, collar, belly, height, handle,
or body cavity volume changed.

### Why this was added

The v5 seating interface (§4, "Value (v5)" column) was a single flat plane: the lid's flat
underside resting on the body's flat 100mm-OD collar rim, with no alignment feature reaching down
into the opening — centering was "by eye/feel" only. This exact idea (a downward alignment
feature) had been proposed and rejected once already, during the original v1 seating-interface
design, specifically because a support-free print was a hard requirement at the time and any
downward lip creates an overhang on the lid's primary seating surface. **What changed this round
is that constraint**: the requester explicitly said print supports are an acceptable tradeoff for
a more secure fit, reopening a previously-closed design question for a legitimate reason rather
than silently re-litigating it. Full history: `specs.md` §5.2/§5.2.1.

### Two options were worked out; the straight-walled option (A) was built

| | Option A (built) — straight-walled | Option B (not built) — tapered stopper/bung |
|---|---|---|
| Top/OD | 79.5mm (constant) | 79.5mm (top), 40mm (tip) |
| Depth | 10mm | 10mm |
| Taper angle | 0° (true vertical cylinder) | ~63.1° from vertical |
| Support on plug's own wall | None — zero-overhang cylinder | Full 10mm tapered face needs support (63° exceeds the ~45° self-supporting guideline) |
| Support on outer brim annulus | Yes — same for both options (see below) | Yes — same for both options |
| Self-centering / progressive friction feel | Constant clearance throughout — a uniform slip fit, no progressive engagement | Genuine "cork in a bottleneck" feel — tightest only at full seating |
| Total support material | **Less** — the deciding factor | More (tapered face support is additive on top of the same annulus) |

**Option A (straight-walled) was chosen and built**, specifically because it needs less total
support material than Option B despite Option B's nicer self-centering feel — the tapered shape
that would read as a genuine "stopper" requires an angle well past self-supporting, so it isn't a
free upgrade. This is a corrected finding from the spec's own analysis, not an assumption: tapering
was initially expected to reduce support needs, and turned out not to for a taper this pronounced.

### Final dimensions, as built and verified

| Parameter | Value | Tag / verification |
|---|---|---|
| Plug OD | **79.5mm** | VERIFIED — Coder, Tester (R54/R57), Reviewer, all exact |
| Plug ID (hollow) | **35.75mm** | VERIFIED — wall = (79.5−35.75×2... i.e. (79.5/2 − 35.75/2)) = 4.000mm exactly, constant at every sampled height through the full depth |
| Plug wall thickness | **4.000mm** | VERIFIED — matches this project's nominal 4mm wall convention, well above the 0.8mm (2×0.4mm nozzle) print-minimum |
| Plug depth | **10.0mm** | VERIFIED |
| Solid vs. hollow | **Hollow** (Coder-level implementation choice per `specs.md` §5.2.1, which flagged this explicitly as undecided at spec time) | Chosen to reduce added material — see cost impact below |
| Body bore ID at engagement depth (Z=138.5–153.5mm) | **80.000mm constant** | VERIFIED — re-confirmed on the untouched body file, not assumed unchanged |
| Diametral clearance | **0.500mm exactly** (80.000mm bore − 79.500mm plug) | VERIFIED by Coder, Tester, and Reviewer independently, all exact |
| Collision margin vs. body's internal taper (P3, Z=138.5mm) | **5.0mm** (plug tip at body-Z=143.5mm) | VERIFIED — computed from two independently-measured real dimensions (plug depth + lid seating height), not nominal-vs-nominal arithmetic |
| Overall lid bounding-box height | **85mm** (was 75mm pre-plug) | VERIFIED — 75mm brim-to-handle stack + 10mm plug hanging below the seating plane |
| Handle (24×22mm opening, 9mm bail, 40mm height) | **Confirmed completely unaffected** | VERIFIED by mesh cross-section sweep — identical to every measurement across this entire project |

### Print/support implications — stated plainly, both halves

**Outer support annulus (accepted tradeoff, not an oversight).** The plug's straight wall meets
the flat underside at Z=10mm with a discontinuous radial jump from 39.75mm (plug) straight to
61mm (brim OD) within a single layer — a genuine vertical step, not a taper. This annulus
(r=39.75–61mm, ≈67.3 cm² area) needs support material for its full 10mm height. Part of that
annulus (roughly r=50–61mm) is the same decorative overhang ring that's visible once the lid is
seated on the body — support witness marks may show there after removal. **This was weighed and
accepted by the requester as the cost of the alignment benefit**, not discovered as a surprise
after the fact.

**Internal bridge — both halves of the honest assessment, not just the reassuring one.** The
plug's hollow interior (35.75mm radius, 71.5mm diameter) is capped by the flat underside of the
solid 5mm brim disc, creating a fully enclosed, unsupported horizontal span anchored around its
entire perimeter by the 4mm plug wall (independently confirmed to be a genuine continuous ring at
every sampled height, not a partial arc — Reviewer, Addendum 4 §1).
- **Expect a real, visible-grade sag/stringing event on this bridge as the normal outcome under
  default slicer settings — not a low-probability edge case.** 71.5mm is roughly 1.5–1.8× past the
  ~40–50mm span most FDM bridging guidance treats as reliably clean even for PLA, and this lid is
  PETG, a materially worse bridging filament than PLA (higher melt viscosity, more prone to
  gradual sag). Full-perimeter anchoring genuinely helps relative to a two-sided bridge, but it
  does not change how far the center of a 71.5mm span sits from any anchor point.
- **It doesn't practically matter — specifically because the surface is both hidden and
  functionally inert, not because the print risk is actually small.** The cavity's boundary has no
  relationship to the plug's fit-critical outer wall (39.75mm OD, unaffected by anything in the
  hollow interior) and no relationship to any visible surface (fully sealed under the brim, never
  exposed once assembled). A sagged, stringy, or even partially-incomplete ceiling here cannot be
  seen, felt, or affect the fit.
- **Both halves of this are load-bearing for anyone editing or re-reading this design** — stating
  only "expect a bad bridge" would misrepresent the risk as a blocker it isn't, and stating only
  "doesn't matter, it's hidden" would understate a real, likely print-quality event. Independently
  confirmed by both the Tester (R59) and the Reviewer (Addendum 4 §2), who both explicitly pushed
  back on an earlier, softer "cosmetic non-issue, just watch cooling" framing as understating the
  probability half of this while landing on the correct consequence half.

**Slicer guidance — a new, non-obvious gotcha specific to this feature.** If your slicer's support
setting is "everywhere" rather than "touching build plate only," it may generate support material
*inside* the sealed 71.5mm void before the ceiling closes over it — material with no removal path
once printed. Not a functional failure (inert, hidden, disconnected from the urn's usable cavity —
at worst, rattling debris sealed inside a lid nobody will ever open), but confusing if you don't
know why you can't retrieve it. **Confirm supports are set to "touching build plate only" before
slicing the lid.**

**Orientation: unchanged, flat-underside-down (plug-tip-down).** A single tilt cannot address both
overhang zones at once: the outer annulus is a discontinuous vertical step (not a sloped surface a
tilt would help), and any tilt large enough to meaningfully reduce the internal bridge risk would
reintroduce overhang on the dome/handle, both deliberately kept flat-up to avoid exactly that
risk. **Recommendation: handle the internal bridge via slicer settings scoped to that one z-layer
band** (maximum cooling, reduced print speed, possibly increased bridge flow) rather than a
whole-part orientation change.

### Test-coupon recommendation — risk direction stated explicitly

Print a small stand-alone clearance-test coupon (a short plug/bore section at the nominal 79.5mm/
80.0mm dimensions) before committing to the full ~85mm-tall, multi-hour PETG lid print. **The
realized clearance is more likely to land tighter than the nominal 0.5mm, not looser**: FDM
systematically tends to print internal bores slightly undersized and external bosses/plugs
slightly oversized relative to nominal CAD (inward corner rounding, extrusion overlap
compensation, general dimensional shrinkage). This compounds with the already-named
PETG-plug/PLA-body material-shrinkage-mismatch risk (`specs.md` §5.2.1, both materials shrink
differently as they cool) — this is a directionally-specific risk, not a generic "always test your
fits" disclaimer.

### Material/cost impact

The hollow plug adds **≈9.49 cm³** to the lid (π×(39.75²−35.75²)×10mm) — a **solid** plug of the
same outer dimensions would have cost **≈49.6 cm³**, so the hollow-shelled choice avoided roughly
40 cm³ of unnecessary material and print time, consistent with this project's standing 4mm-wall
convention.

| Metric | v5 (pre-plug) | v6 (with hollow plug) | Change |
|---|---|---|---|
| Lid material-shell volume | ~219.2 cm³ | **~228.7 cm³** | +9.49 cm³ (+4.3%) |
| Lid mass (PETG, ~1.27 g/cm³) | ~278g | **~290g** | +12g (+4.3%) |
| Combined pair filament cost | ~$12.5–16 | **~$12.6–16.3** | Negligible — well under 5% of the lid's own material volume, no material change to the overall cost picture |

### Three-way independent verification

| Check | Coder | Tester (R53–R60) | Reviewer (Addendum 4, 4th independent method) |
|---|---|---|---|
| Manifold/watertight | Yes, single solid, Euler=0 | Yes, zero non-2-count edges across ~18,100 faces | Yes, own `trimesh` script, exact match |
| Plug wall (outer/inner radius) | 39.75mm / 35.75mm | 39.750mm / 35.750mm, constant 4.000mm wall | 39.750mm / 35.750mm, exact match |
| Bridge/void geometry | Fully enclosed at Z=10mm | Confirmed — interior loop vanishes exactly at Z=10.00mm, solid to r=61mm beyond that | Confirmed — genuine continuous 71.5mm-diameter ring anchored around its full perimeter at every sampled height, not a partial arc |
| Collision margin | 5.0mm (nominal) | 5.0mm (measured from real geometry of both parts) | 5.0mm, exact match |
| Clearance | 0.5mm (nominal) | 0.500mm exactly, measured | 0.500mm exactly, measured |
| Handle | Unaffected (by construction) | Directly re-swept — 22×24mm, y=−4 to +4mm, bit-identical to every prior measurement | Directly re-swept, same window, confirmed |
| No unauthorized oversize compensation | Built to nominal 79.5/80.0mm exactly | Confirmed — clearance measured at exactly nominal, not pre-padded | Not independently re-checked this round (not one of the 5 requested checks), no reason to doubt it given the exact clearance match above |

Every figure checked matches across all parties to the same precision. This is a fourth
independent method on this project (after the Coder's Fusion measurements, the Tester's mesh
integration, and the Reviewer's two prior independent methods in the v4/v5 rounds), not a rubber
stamp of the chain.

### Business fit / concept fidelity — unaffected, confirmed by direct inspection

The plug sits entirely below the lid's flat underside/seating plane, inside the body's neck bore
once assembled, with zero effect on the exterior silhouette in any view — confirmed directly by
the Reviewer (Addendum 4 §8), not just assumed from scope. `concept/brief.md` and
`concept-v2.png` never depicted or implied anything about a below-the-seating-plane fit mechanism,
so this addition raises no concept-fidelity question. The existing hero render
(`render/pet-memorial-urn-hero.png`, from the v5 round) still accurately depicts the current
exterior geometry and was not re-shot for this reason.

### Approval status

**Approved**, per `dot_pipeline/review.md` "ADDENDUM 4 — 2026-09-01" — a targeted addendum (not a
full re-review, consistent with this project's practice of scoping review effort to what a round
actually touches). All 5 originally-requested checks passed; the bridging-risk framing was
sharpened (both halves stated plainly, per above) rather than left as the softer "cosmetic
non-issue" framing first proposed; the trapped-support slicer risk and test-coupon
directional-risk recommendations were both confirmed and carried into this document and
`README.md`.

## 13. v7 handle removal, plug cap, brim/dome rework (2026-09-02) — full derivation, honest tradeoffs, and four-way verification

**Scope: lid only.** `urn-body` and `neck-fit-test` were not touched or re-exported this round —
timestamps for both remain 2026-08-31 (v5). This is the largest single lid revision in this
project's history, reversing a constraint (the handle) stated as load-bearing to the design's
identity since the very first concept approval, alongside four other coordinated changes.

### Why this happened — the handle removal specifically

`concept/brief.md`, the document that launched this project, describes the open-loop bail handle
as **"the key differentiating feature"** of the entire design, states it should "read as an
intentional, load-bearing part of the lid, not a decorative nub," and calls the open-through-hole
geometry **"a hard constraint when the Planner moves to CAD."** Every revision from v1 through v6
treated this as binding, and every Reviewer pass independently re-verified the handle's open-loop
integrity as one of this project's three named hard constraints (§4, historical rows above; also
`review.md`, repeated across every prior addendum).

**The requester has explicitly and directly confirmed removing the handle entirely, with no
replacement grip feature, fully aware this reverses that original hard constraint.** This is
recorded here as exactly what it is — a direct, deliberate override of the concept brief's own
"hard constraint" framing, made knowingly and explicitly, not a silent contradiction of it or
something a future reader should need to reconstruct from context. The brief's original language
is not edited or walked back anywhere in this project's history; it is being explicitly superseded
by this later, direct instruction.

### The four other coordinated changes

1. **Plug tip capped.** The v6 plug (79.5mm OD × 10mm deep, hollow, 4.0mm wall) was open at its
   tip. As of v7, the last 4mm nearest the tip is a solid disc (full 79.5mm OD); the remaining 6mm
   nearest the brim stays hollow at the same 4.0mm wall. Total plug envelope (OD, depth, collision
   margin, clearance) is completely unchanged — only the internal makeup of the last 4mm changed.
2. **Brim shrunk to flush, thickened.** OD 122mm → **99.700mm** (a deliberate -0.3mm allowance
   below nominal 100mm, landing flush with the body's 100mm collar — zero overhang, replacing the
   overhanging-brim design used in every prior revision). Thickness 5mm → **10mm**.
3. **Dome base re-derived.** OD ~97–98mm → **80mm exact**, via the same 0.80 dome-to-brim ratio
   this project has used since v1, applied to the new 99.700mm brim.
4. **Dome apex flattened.** Replaced the fully-rounded point apex with a **flattened plateau,
   21.7283mm diameter** — see the honest tradeoff writeup below.

### Plug-cap topology — the sealed void, confirmed correct by four independent methods, not a defect

Capping the tip creates a **fully enclosed internal void** (the 6mm hollow section, floor = new
solid tip cap, ceiling = solid brim underside, walls = the 4mm plug wall). The resulting solid is
topologically a `BREP_WITH_VOIDS` — **13 faces total (6 planes, 3 cylinders, 1 sphere, 3 toruses)**,
arranged as **one outer shell of 10 faces plus one internal void shell of 3 faces**. Tessellated to
a mesh, this shows up as **2 disjoint watertight components** (the outer envelope, +216–218 cm³
depending on export; the void shell, −24.07 cm³ — matching the analytically-expected 6mm-tall,
35.75mm-radius cylinder, π×35.75²×6 ≈ 24.085 cm³, to within tessellation noise).

**This is confirmed correct, not a fragmentation defect, by four independent methods:**

1. **Coder's construction reasoning** — the cap was built as a deliberate feature, and the
   resulting 2-component/`BREP_WITH_VOIDS` signature was the expected, intended outcome.
2. **Tester, mesh-level (`trimesh.split`)** — confirmed exactly 2 components, both individually
   watertight, summing to the correct net material volume; confirmed the negative-volume sign on
   the void component is the textbook signature of a correctly-oriented internal-void shell, not a
   symptom of bad topology.
3. **Tester, B-rep-level (direct text parsing of `step/urn-lid.step`'s native entities)** —
   confirmed `ADVANCED_BREP_SHAPE_REPRESENTATION`=1 (one solid shape, not two), `BREP_WITH_VOIDS(`=1
   (the STEP entity name specifically used for a solid with an internal void, as opposed to
   `MANIFOLD_SOLID_BREP`, which is absent — 0 occurrences), `CLOSED_SHELL(`=2 (one 3-face void
   shell, one 10-face outer shell, 13 faces total matching `ADVANCED_FACE(`=13 exactly). Also
   confirmed via a **differential check against the pre-cap archive**
   (`archive/pre-v7-handle-removal/urn-lid.stl`) that the pre-cap file shows exactly **1** component
   (the void was open to the outside air through the tip before capping, so the void's boundary and
   the outer boundary were the same continuous surface) — confirming the before/after signature
   change is exactly what the capping theory predicts, not just asserted in isolation.
4. **Reviewer, live Fusion `BRepBody` object model query** — independently confirmed **13 faces, 2
   shells** (shell 0: 3 faces, the void; shell 1: 10 faces, the outer envelope) directly against the
   live CAD kernel's own object model, with no export/tessellation step in between — arguably the
   most authoritative of the four methods.

**If a mesh tool ever reports "2 solids" for this file, that is the correct, expected, unavoidable
signature of a genuinely sealed internal cavity — it is not possible for a correctly capped hollow
feature to produce anything other than 2 disjoint mesh components once the tip seals over, since a
sealed interior surface shares no edges with the exterior surface once nothing connects them.** Do
not attempt to "fix" this by merging or re-sealing anything.

**What capping does and doesn't change, stated plainly:**

- The plug's fit-critical outer wall (79.5mm OD, 0.500mm clearance) is completely unaffected.
- The pre-existing ~71.5mm internal bridge (where the hollow tube meets the solid brim above) is
  **unchanged** — same span, same expected sag/stringing under default slicer settings, same reason
  it doesn't matter (fully sealed, never visible, disconnected from every fit-critical surface).
  Capping the *other* end of the tube does not touch this transition in any way.
- The new tip cap itself introduces **zero new bridging risk, specifically because of print
  orientation**: it's the literal first printed layer(s), fully supported by the build plate
  regardless of shape — a solid disc is if anything a *better*-supported first layer than the thin
  open ring it replaces. This conclusion is contingent on keeping the flat-underside-down
  orientation (see below) — it would not hold if the part were ever printed plateau-down instead.
- Capping likely makes the standing "supports touching build plate only" mitigation more reliable
  (a sealed void has no unobstructed path back to the bed for a slicer to detect it through), though
  this is reasoned from how that slicer setting generally works, not confirmed against a real
  slice — **check the print preview to confirm no support is generated inside the sealed cavity**
  before committing to the full lid print.

### Brim — flush fit, and a geometry-description correction

**OD: 99.700mm**, a deliberate **-0.3mm allowance** below the nominal 100mm target, landing flush
with the body's 100mm-OD collar (independently confirmed via live STEP cylindrical-face queries on
both parts: brim r=49.850mm, collar r=50.000mm — the 0.3mm allowance is real, not a rounding
artifact). Thickness **10mm** (up from 5mm).

**Geometry-description correction, worth stating plainly because earlier project notes got this
wrong in both directions.** `specs.md`'s original corroborating math for the dome-base derivation
described the brim-to-dome transition as a **"10mm flat brim ring."** An earlier Tester pass
(RE-TEST PASS 9, R67) checked this directly and found it does **not** exist as a literal flat
surface — the actual transition is a compound two-stage fillet (two tangent toruses) with **no**
intervening flat plateau, and flagged the spec's "10mm flat ring" description as inaccurate. The
Reviewer's own live B-rep query went one step further and found the Tester's correction was *also*
not quite right in the other direction: there **is** a real, physically-present flat face — a
`PlaneSurfaceType` face at **Z≈20.0mm, normal (0,0,1), spanning roughly r=41.5–46.85mm (about
5.35mm wide, area ≈1485.9mm²)** — sitting precisely between the two toruses. This is a genuine,
nonzero-area flat annular shelf, not a tangency artifact, but it is **narrower and differently
positioned** than the "10mm flat ring, matching the collar's own 10mm wall band" the spec
originally described. **Net, corrected description: a smooth compound two-stage fillet with a
genuine but narrow (~5.35mm) flat annular step nested between the two toruses — neither "no flat
face at all" nor "a 10mm flat ring."** This changes nothing functionally (self-supporting either
way, confirmed by radius-monotonicity and crease-detection sweeps below) — it is a
documentation-accuracy correction only.

**Named risk unique to this exact-match edge:** every prior brim/collar pairing had a comfortable
overhang margin (11mm/side minimum) that could absorb normal FDM dimensional variance without
anyone noticing. A brim printed to exactly nominal 100mm against a collar also printed to exactly
nominal 100mm has no such cushion. FDM's systematic tendency is for external bosses/rims to print
slightly *oversized*, not undersized — so the more likely failure direction is a lid brim that
overshoots the collar's edge by a fraction of a millimeter (a small proud lip), not the collar
peeking out past an undersized lid. The -0.3mm allowance is a deliberate hedge against exactly
this; if the first print still reads proud rather than flush, a further small negative allowance is
the fix, not a redesign.

### Dome base — re-derivation

**Method: preserve the 0.80 dome-to-brim OD ratio**, the same method this project has used since
v1 and re-applied at v5. Applied to the new 99.700mm brim: 99.700 × 0.80 ≈ 79.76mm, rounded to an
**80mm exact** target — independently confirmed via live STEP sphere/placement math (the sphere's
natural r=40mm circle lands at global Z=20.0mm, exactly the intended brim-top boundary).
**Corroborating note:** this is the identical absolute figure v1–v4 used, for an unrelated reason
(the original v1–v4 lid also happened to pair an 80mm dome with a 100mm brim) — a reassuring
convergence, not a forced result, since v7's derivation reached it independently via the flush-fit
chain rather than by copying the old number.

### Dome apex — the honest 21.73mm-vs-22mm story

**Target: ~22.00mm** (roughly a quarter of the 80mm dome base, sized against a concept-comparison
reference image, `concept/v7-dome-apex-flattened.png` vs. `v7-dome-apex-rounded.png`) —
`ESTIMATED`, an aesthetic judgment call, never a tight tolerance.

**First attempt (RE-TEST PASS 9): 17.70mm, a real miss, and the causal claim behind it was wrong.**
The first build reused the dome's existing sphere radius (41.6667mm — left over from the
pre-flattening, point-apex design) and landed at only 17.70mm. The Coder's framing at the time
("not simultaneously achievable on a spherical cap") was checked independently by the Tester and
found to be **factually incorrect** — solving the actual three-target system (80mm base, 29mm
height, 22mm plateau diameter) directly gives a closed-form exact answer:

```
z_c = (r_p² + h² − a²) / (2h) = (121 + 841 − 1600) / 58 = −11.0mm
R = sqrt(a² + z_c²) = sqrt(1600 + 121) = sqrt(1721) = 41.4849mm
```

A sphere of radius 41.4849mm — just 0.18mm (0.44%) smaller than the 41.6667mm sphere actually used
— hits the 80mm base, 29mm height, and 22mm plateau **all three, exactly, simultaneously, with no
blending shortfall**. The real constraint was never a mathematical wall — it was a choice to reuse
the pre-flattening sphere's already-verified curvature rather than re-derive and re-verify a new
one. This was a legitimate reason to have made that choice, but it was a choice, and the
documentation at the time incorrectly presented the 17.70mm outcome as unavoidable. This was
corrected, not silently carried forward.

**Second attempt (RE-TEST PASS 10): sphere radius corrected to 41.4849mm, landing at 21.73mm —
still short of exactly 22.00mm, and here's the honest reason why.** The corrected sphere's *raw,
unblended* curve does pass through exactly r=11.0mm (22mm diameter) at z=29mm — independently
confirmed via STEP-level sphere/placement math. But the **built, blended** result is **21.7283mm
diameter (r=10.8642mm)**, not 22.00mm, because the tangent-matched fillet that blends the sphere
into the flat plateau (avoiding a visible ~15° kink — the same class of faceted transition this
project has treated as a real defect worth fixing properly since v2) necessarily consumes a small
amount of the curve's radius to achieve genuine tangency. At this specific geometry, **hitting
exactly 22.00mm and achieving genuine tangency are mutually exclusive — tangency was correctly
prioritized**, independently verified via two checks: a radius-monotonicity sweep (zero
locally-increasing-radius steps across the whole dome+plateau span) and facet-crease detection (max
adjacent-facet angle 12.72°, well below the 20–30°+ range that would indicate a real kink, and
statistically identical to the pre-fix measurement at an unrelated location).

**Why this is the right call, not just an acceptable one:** the spec's own precision requirement on
22mm was always soft — "an aesthetic judgment call... roughly a quarter of the dome's base width,"
never a stated tolerance like "22.00mm ±0.1mm." The tangency requirement, by contrast, is explicit
and reasoned from a real, previously-documented print-quality defect class. **The proportion the
22mm figure was actually standing in for is preserved almost exactly:** 22mm ÷ 80mm = 27.5%
("roughly a quarter"); the built 21.7283mm ÷ 80mm = **27.16%** — a 0.34-percentage-point
difference, not visually distinguishable from the reference image the 22mm figure was itself
eyeballed against. This is a clean resolution of the actual design intent (the proportion), not a
lesser compromise on the specific decimal.

Independently confirmed two ways, agreeing to 6 significant figures: mesh vertices at the plateau
(radius 10.864167mm at every one of 48 sampled vertices) and the STEP file's native
`TOROIDAL_SURFACE` major-radius parameter (10.8641670619166mm).

### Heights, volume, and cost

| Metric | v7 (current) | v6 | Change |
|---|---|---|---|
| Total lid height (seating plane to top of dome/plateau) | **39.000mm** | 75mm | **-48%** |
| Total lid bounding-box height (incl. plug) | **49.000mm** | 85mm | **-42%** |
| Combined assembled height (body + lid) | **192.500mm** (153.5 + 39.0) | ≈228.5mm | -15.7% |
| Lid material-shell volume | **194.2929 cm³** | ~228.7 cm³ | **-15.1%** |
| Lid mass (PETG, ~1.27 g/cm³) | **~247g** | ~290g | -14.8% |
| Combined pair filament cost | **~$12.0–14.9** | ~$12.6–16.3 | Real, modest decrease (~6–9%) |

The height reduction is driven almost entirely by the handle's removal (the handle alone accounted
for 40mm of the old 75mm lid height). This connects to an earlier competitive-research concern
about this design's overall height running long versus competitor pet urns, raised in conversation
with the requester rather than written into a prior spec revision, but real context worth stating
here — the height drop is a genuine, positive side effect of the handle removal, not something
separately engineered for. The volume/cost decrease happens **despite** the brim doubling in
thickness and the plug gaining a solid tip cap, because the much larger reduction from the
shrunk-to-flush brim (122mm→99.7mm OD) and the removed handle (40mm of material eliminated
entirely) outweighs both additions.

### Print orientation — re-checked, not assumed unchanged

**Flat-underside-down (plug-tip-down) remains correct**, independently checked by both the
Coder/Planner and the Reviewer rather than carried forward by default. With the handle gone and the
apex flattened, plateau-down is a genuinely new option this geometry didn't have before — and both
parties rejected it after walking through the whole part, not just the plateau's own flatness in
isolation. Today, radius is non-increasing from the plug tip (Z=0) all the way to the plateau
(Z=49mm) — confirmed via a 390-point radius-monotonicity sweep at 0.1mm resolution, zero
locally-increasing steps anywhere. Flipping the part plateau-down would invert this entire
relationship: the dome becomes a classic expanding cone from a ~21.7mm top to an 80mm base, needing
support under virtually its whole visible exterior (the one surface the flat orientation was chosen
specifically to protect), and the plug's tip cap would flip from a bed-supported first layer into
an unsupported last layer over a sealed void — reintroducing the exact bridging risk that
capping-then-orienting-tip-down was designed to avoid. Not a close call once the whole dome and the
plug's cap are both accounted for.

### Usability — drop-risk, elevated by the Reviewer, not just a routine watch-item

With no dedicated handle, gripping a smooth dome by hand is less secure than a purpose-built grip
loop. This is **not** a survivability/durability concern (solid PETG, no fragile features outside
the sealed internal bridge) — it is a **likelihood-of-dropping** concern, and the Reviewer
specifically elevated it given what this object holds: irreplaceable cremated remains, at a moment
(transferring a filled urn) where a slip is genuinely distressing, not just cosmetically costly.
**Handling recommendation, per the Reviewer:** lift with a full hand cradling the dome/brim, not a
fingertip pinch on the edge; consider lifting the lid off and setting it down separately before
moving the filled body, rather than carrying the assembled unit by the lid.

### Concept-fidelity — the Reviewer's full finding, not a softened version

The Reviewer's full v7 review assessed this cumulatively, not the handle removal in isolation.
Quoting the conclusion directly rather than paraphrasing it away: **"With it gone, what's actually
left is a plain domed lid on a plain-bodied jar — and I don't think that reads as a coherent,
differentiated identity anymore, it reads as generic."** This lands on top of two already-disclosed
drifts — the v4 belly-fullness edit reading as a more pronounced "ginger jar" silhouette than the
concept's gentler taper, and the collar reading as a "banded, partially-cylindrical" reinforcement
ring rather than the concept's continuous neck curve — both previously accepted as minor,
functionally-necessary tradeoffs specifically **because** the handle was still there anchoring the
design's identity against them. The Reviewer looked for a remaining differentiator (the flattened
plateau, the flush brim edge) and concluded neither is a plausible substitute for what the brief
called "the key differentiating feature" — both are real, deliberate refinements, but too subtle at
normal viewing angles to function as a standalone identity marker.

**This is not a blocker.** The Reviewer is explicit: this was an informed, user-confirmed decision,
the practical reasoning behind it is sound (a genuine competitive-height concern, a real
print-time/material/support reduction, a less top-heavy lid), and nothing here is a defect — it is
a legitimate creative and business call belonging to the requester, not to the Reviewer. But the
Reviewer distinguishes between "the requester already decided this" and "the requester has seen the
full cumulative visual consequence of this decision stacked on the drifts already banked from v4/
v2," and does not believe the second is true yet. **Recommendation: a real visual check-in with the
requester** — the original concept image, the archived v6 render
(`archive/pre-v7-handle-removal/pet-memorial-urn-hero.png`), and the current v7 render
(`render/pet-memorial-urn-hero.png`), side by side — asking plainly whether this still reads as the
differentiated product originally set out to build, or now reads as a generic jar with a lid, before
treating this as fully final. **This check-in has not yet happened** — see `README.md`'s "Status"
section.

### Render

Both `urn-body` and `neck-fit-test` had been hidden in the live document (a user visibility toggle,
not a design change) — both were unhidden and left visible. Both custom appearances (`Matte PLA -
Stoneware Tan` on the body, `Matte PETG - Stoneware Tan, sanded` on the lid) survived intact and
required no repair this round. The lid was temporarily raised to its true 153.5mm seated height for
the shot and `neck-fit-test` temporarily re-hidden, both reverted immediately after capture. Saved
to `render/pet-memorial-urn-hero.png`, replacing the stale v6 image.

**The v6 render had not previously been archived** (an oversight in the archive-folder convention
established for v4/v5) — it was recovered from git history (`git show HEAD:.../
pet-memorial-urn-hero.png`) and saved to `archive/pre-v7-handle-removal/pet-memorial-urn-hero.png`,
alongside that folder's pre-v7 lid STEP/3MF/STL, so the handle-vs-no-handle comparison this
revision's concept-fidelity assessment depends on remains available.

**Same disclosed limitation as every prior render in this project:** a faint background
reference-grid overlay remains visible and could not be suppressed via the available API — a
viewport-chrome element, not model geometry.

### Four-way independent verification

| Check | Coder | Tester (R61–R69, RE-TEST PASS 9) | Tester (R72–R75, RE-TEST PASS 10) | Reviewer (live B-rep query) |
|---|---|---|---|---|
| Plug cap (solid/hollow split) | 4mm solid + 6mm hollow | Confirmed exactly, transition at Z=4.0mm exactly | Unaffected, bit-identical | Confirmed via live shell/face query |
| Plug OD / wall | 79.5mm / 4.000mm | 79.500mm / 4.000mm, constant | Unaffected | 79.5mm confirmed (unaffected by this round's fix) |
| Topology (faces/shells) | 13 faces (2 shells) | 13 `ADVANCED_FACE` (6+3+1+3), `BREP_WITH_VOIDS`=1, `CLOSED_SHELL`=2 | 13 faces, `BREP_WITH_VOIDS`=1 confirmed unchanged | 13 faces, 2 shells (3+10), exact |
| Brim OD | 99.700mm | 99.700mm (mesh) | — | 99.700mm (r=49.850mm, live cylindrical face) |
| Body collar OD (mating) | 100.000mm | — | — | 100.000mm (r=50.000mm, live cylindrical face) |
| Dome sphere radius | 41.4849370254mm | 41.6667mm (RE-TEST PASS 9, flagged as a real finding) | **41.4849370253831mm**, corrected | 41.4849mm, exact |
| Dome plateau diameter | 21.7283mm | 17.7012mm (RE-TEST PASS 9, pre-fix) | **21.7283mm**, confirmed two ways to 6 sig figs | 21.7283mm (bbox 21.7283×21.7283mm at Z=49) |
| Dome base OD | 80.000mm | 80.000mm | 80.000mm exact | 80.000mm |
| Total lid height (seating to plateau) | 39.000mm | 39.000mm | 39.000mm | 39.000mm |
| Total bbox height | 49.000mm | 49.000mm | 49.000mm | 49.000mm |
| Combined assembled height | 192.500mm | 192.500mm | — | 192.500mm |
| Lid material volume | 194.2929 cm³ | 192.2807–192.2838 cm³ (mesh, ~0.13% low, expected chord-vs-arc effect) | 194.041–194.038 cm³ (mesh, same effect) | 194.2929 cm³ (exact, live Fusion) |
| Body/`neck-fit-test` unaffected | By scope | Confirmed, timestamps unchanged | Confirmed | Confirmed, body/neck-fit-test file dates unchanged |

Every headline number checked by all four independent methods available on this project agrees
exactly or within the expected mesh-tessellation tolerance. This is the fifth cumulative
independent-verification method applied across this project's lifetime (Coder's Fusion
mass-properties/construction queries, the Tester's mesh integration, the Tester's native-STEP-entity
text parsing, the Reviewer's own numerical-integration script from earlier rounds, and now the
Reviewer's live `BRepBody` object-model query) — not a rubber stamp of the pipeline's own numbers
at any stage.

### Approval status

**Approved**, per `dot_pipeline/review.md` "FULL RE-REVIEW — 2026-09-02: v7 major lid revision" — a
full, from-scratch re-review (not a targeted addendum), consistent with the scale of this round's
identity-level change. Geometry is sound and independently re-confirmed via a fourth/fifth method
at every headline dimension checked; print orientation is correct and was independently re-checked
against the new plateau-down alternative; the two remaining hard constraints (plain body,
single-size build) are intact. **Two items carry more weight than a routine watch-item:** (1)
`README.md`/`parameters.md` needed to be brought current to v7 (addressed by this documentation
pass), since both previously described a handle that had been deliberately and explicitly removed;
(2) the concept-fidelity "reads as generic" finding above, a genuine non-blocking business/creative
flag recommending a real visual check-in with the requester before this design is treated as fully
final.
