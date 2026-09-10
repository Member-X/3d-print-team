# Spec — Pet Memorial Urn (Medium / 25–50 lb pet size), v1

## 0. Folder structure — read this first

This product line now uses a **size-named-subfolder structure**. The **Large** build
(50–90 lb, ~90 lb target) remains exactly where it has always lived — at the project root
(`pet-memorial-urn/step/`, `/3mf/`, `/stl/`, `/dot_pipeline/`, `/parameters.md`, `/README.md`) —
**untouched and unmoved by this document**. Large has its own separate, still-open physical
fit-test item pending (see its own `README.md` "Status" section) and is not this document's
concern in any way; nothing here modifies, references-as-authoritative, or depends on Large's
files being edited.

This document specs the **Medium** size (25–50 lb pet, sized to the top of the range: 50 lb),
living entirely under `pet-memorial-urn/medium/` — its own `dot_pipeline/`, `step/`, `3mf/`,
`stl/` subfolders. **The Coder, Tester, and Reviewer who work from this spec are expected to
write exclusively within `pet-memorial-urn/medium/`** — never back into the project root
(Large's territory) and never into `pet-memorial-urn/small/` (a sibling Small build, 0–25 lb,
is being planned in parallel by someone else; do not read or write there). Every deliverable
filename in this document carries a `-medium` suffix specifically so files are never confused
with Large's or Small's identically-purposed files if anyone ever copies things between folders.

**This is a sizing/derivation exercise for an already-approved visual design, not a new concept
pass.** The v7 design language established across Large's full revision history (see
`pet-memorial-urn/dot_pipeline/specs.md` and `parameters.md`, both read in full before writing
this document) is carried forward as-is at this size — no magnet closure, no handle, flush
brim-to-collar fit, flattened dome plateau, straight-walled capped alignment plug. What is
**not** carried forward as-is, per explicit instruction, is any dimension that was itself a
Large-scale-specific choice (wall thickness, plug clearance/wall, neck opening size, overhang
angles, collar reinforcement proportion) — those are independently re-derived below, each with
its own worked reasoning, not proportionally shrunk from Large's numbers.

---

## 1. Source key (dimension provenance) — same three-tag convention as Large

| Tag | Meaning |
|---|---|
| **VERIFIED** | Independently confirmed — a real, currently-sold commodity part or manufacturer spec sheet found this session, or (once built) a physical/CAD measurement. |
| **DERIVED — sizing decision** | Computed from the requester's own volumetric rule of thumb (1 in³ internal volume per lb of pet body weight) or from another already-fixed dimension in this document, with the formula shown. |
| **ESTIMATED** | A design convention or reasoned best-guess default not otherwise sourced — every ESTIMATED figure in this document is accompanied by the reasoning that produced it, not a bare number. |

**The highest-risk item in this spec is the neck/collar opening ID (§4.4)** — it is the one
dimension a real physical object (a crematorium remains bag) must actually pass through, and,
per this project's own established pattern on Large, a "standard" or naively-scaled guess here
has previously produced a design that looked right and didn't serve its purpose. Real competitor
data was researched fresh for this exact size tier (§4.4) rather than proportionally shrinking
Large's 80mm — but the resulting number is still **ESTIMATED / untested against a real bag**,
and is named as this document's primary open risk, exactly as it was for Large.

---

## 2. Files (Coder deliverables)

| File | Purpose |
|---|---|
| `pet-memorial-urn/medium/step/urn-body-medium.step` | Editable CAD source for the body, parametric if the tool supports it |
| `pet-memorial-urn/medium/step/urn-lid-medium.step` | Editable CAD source for the lid |
| `pet-memorial-urn/medium/3mf/urn-body-medium.3mf` | Slicer-ready body, orientation baked in per §9 |
| `pet-memorial-urn/medium/3mf/urn-lid-medium.3mf` | Slicer-ready lid, orientation baked in per §9 |
| `pet-memorial-urn/medium/stl/urn-body-medium.stl` | Final body mesh |
| `pet-memorial-urn/medium/stl/urn-lid-medium.stl` | Final lid mesh |
| `pet-memorial-urn/medium/step/neck-fit-test-medium.step` | **Standalone neck/collar fit-test article — do not skip.** Just the neck-taper + collar section, flange-cut at the bottom for bed stability, open bore both ends, sized to §4.4/§4.5's 72mm ID / ~78.4mm neck OD / 88mm collar OD. This is the requester's real, physical go/no-go test for the single highest-risk number in this document (§4.4) — see the note on Large's own project, where this exact article was nearly forgotten in an earlier round. |
| `pet-memorial-urn/medium/3mf/neck-fit-test-medium.3mf` | Slicer-ready fit-test article |
| `pet-memorial-urn/medium/stl/neck-fit-test-medium.stl` | Final fit-test-article mesh |

Body and lid are two separate printed parts, each independently manifold/watertight, not printed
in place, not glued together — the lid rests removably on the body's collar rim, same as Large.
No mechanical or magnetic closure feature is modeled into either part (carried forward from
Large's v3 decision, §7).

---

## 3. Printer constraints (stated up front)

| Constraint | Value | Tag |
|---|---|---|
| Printer | P2S-class FDM | Per task instruction / user memory |
| Build volume | 256 × 256 × 256mm | Per user memory (`user_printer_specs.md`) |
| Nozzle diameter | 0.4mm (assumed standard) | ESTIMATED — standard shop default, carried from every prior spec in this repo including Large |
| Minimum wall/boss thickness implied | ≥0.8mm (2× nozzle) for any wall or boss under load | Computed from the line above — this is the one number in this section that does **not** change with part size |
| Body fits build volume? | ~120.4mm max OD (belly) × 131mm H (§4.5) | **Yes**, trivially — smaller than Large on every axis |
| Lid fits build volume? | ~88mm max OD (brim, flush with the collar) × ~41mm bounding-box H (33mm brim-to-plateau + 8mm plug, §5) | **Yes**, trivially |

Body and lid are separate parts, so combined assembled height does not need to fit in one shot
regardless — combined assembled height (body rim + lid above its seating plane) is
**≈131 + 33 = 164mm**, well under 256mm even combined, with each part individually clearing the
bed by well over 100mm of margin on every axis. Bed fit is not a binding constraint on this
design, exactly as it wasn't for Large.

**Every wall/collar/plug/brim dimension chosen in §§4–5 is checked against the 0.8mm floor at
the point it's introduced.** The thinnest structural feature in this design is the nominal body
wall at **3.2mm — 4× the floor**, still comfortably clear, though a smaller margin than Large's
5× (see §4.2 for why 4× rather than Large's 5× is the right call at this size, not a corner cut).

---

## 4. Body sizing derivation

### 4.1 Volume target

Per the requester's explicit rule of thumb (identical to the one used for Large): ~1 in³ of
internal usable volume per lb of pet body weight. Target category is medium pets, 25–50 lb.
Sized to the **top of the range (50 lb)**, since oversizing capacity slightly is preferable to
undersizing it for cremated remains — same reasoning, same instruction, as Large.

```
Target internal volume = 50 lb × 1 in³/lb = 50 in³
50 in³ × 16.3871 cm³/in³ = 819.355 cm³ (≈ 0.819 liters)
```

**Target: ≈819.4 cm³ internal cavity volume.** Tagged `DERIVED — sizing decision` — analogous to
Large's original 1474.8 cm³ figure (Large's v1 starting target, from its own 90 lb × 1 in³/lb
calc), not to Large's eventually-*built* 1579 cm³ (which grew past its own target via a
mid-build manual aesthetic edit specific to that build — not a repeatable design decision, and
explicitly not the number this document scales against, per the task's own instruction). The
same ±5% routine-tolerance-band convention Large used applies here: **flag back for a spec
revision if the as-built CAD geometry lands outside ≈778.4–860.3 cm³ (±5% of 819.4 cm³) by more
than that margin**, same honesty rule as every revision of Large's spec.

### 4.2 Wall thickness — re-derived, not scaled from Large's 4mm

**The 0.8mm print floor (2× the 0.4mm nozzle) does not change with part size — this is a hard
physical constraint independent of scale.** What genuinely needs re-deriving is the *nominal*
wall thickness above that floor, which on Large was an aesthetic/heft convention (4mm, chosen as
5× the floor "for perceived heft / doesn't feel like plastic," not a print-forced minimum).

**Why naively copying 4mm is the wrong move here, shown with numbers, not just asserted:**
material (wall) volume for a thin shell scales roughly with *surface area* (∝ linear-scale²),
while cavity volume scales with *volume* (∝ linear-scale³). Holding wall thickness constant while
the body shrinks therefore makes the wall consume a *larger* fraction of the internal volume
budget, not the same fraction — exactly the effect the task asked to check for.

Using the volume ratio between this target (819.4 cm³) and Large's own original v1 target
(1474.8 cm³) as the basis for a linear scale factor (comparing like-for-like starting targets,
not Large's inflated built figure):

```
Volume ratio = 819.4 / 1474.8 = 0.5556
Linear scale factor k = 0.5556^(1/3) ≈ 0.8221
Surface-area scale factor ≈ k² ≈ 0.676
```

Large's built body: cavity ≈1579 cm³, material (wall) shell ≈279 cm³ at a 4.0mm wall →
material/cavity ratio ≈ **17.7%**. Holding that *same ratio* (not the same absolute wall
thickness) as the design target for Medium keeps the wall's "bite" out of the smaller volume
budget proportionate to how Large's own wall relates to Large's own cavity:

```
Target material volume ≈ 0.177 × 819.4 cm³ ≈ 145.0 cm³

Approximate body surface area at this scale (Large's own shell implies ≈697.5 cm² of
surface area at a 4.0mm average wall: 279 cm³ ÷ 0.4cm ≈ 697.5 cm²; scaling by k² ≈ 0.676
gives an estimated Medium surface area ≈ 471.6 cm² — used here only as an order-of-magnitude
check, not a precise figure)

Required wall thickness ≈ 145.0 cm³ ÷ 471.6 cm² ≈ 0.307cm ≈ 3.1mm
```

This is a rough surface-area estimate (not a real CAD surface-area query, which doesn't exist
yet), but it converges on the same conclusion two independent ways: a materially thinner wall
than Large's 4mm is the right call at this scale, without needing to approach the 0.8mm floor.

**Chosen nominal wall: 3.2mm.** Rounded slightly up from the 3.1mm calculation above for a clean,
buildable number — still **4× the 0.8mm floor** (vs. Large's 5×), a smaller margin than Large's
but nowhere near the floor itself. Tagged `ESTIMATED` (a design-convention figure, backed by the
proportionality reasoning above, not a print-forced minimum).

**Floor thickness: 4.0mm.** Large used a floor 1.25× its own nominal wall (5mm floor ÷ 4mm wall)
for base stability/settled-weight-over-years reasons. Holding that same 1.25× ratio: 3.2mm × 1.25
= 4.0mm. Tagged `ESTIMATED`, same convention/reasoning as Large's floor, applied at the new wall
figure.

### 4.3 Neck/collar opening ID — fresh competitor research at the medium-pet tier, not a proportional shrink

**This is the single most important derivation in this document.** Per the task's own framing,
proportionally shrinking Large's 80mm by the linear scale factor (k≈0.822) would give ≈66mm —
this number is **explicitly rejected below**, not used, because fresh research shows opening
diameter does not scale linearly with capacity/weight bracket, for a physically sensible reason:
a folded/bagged remains parcel has its own practical bulk that doesn't shrink at the same rate
total ash volume does.

**Real competitor data gathered this session (manufacturer product-listing spec sheets, tagged
`VERIFIED` — found via live web search of current retail listings, not independently
hand-measured, same caveat every "VERIFIED" competitor figure in Large's spec carries):**

| Brand / line | Rated capacity | Lid/opening diameter |
|---|---|---|
| Reminded (brass paw-print urn) — Small, up to 35 lb | 35 in³ | 2⅝" = **66.68mm** |
| Best Friend Services, Odyssey Series — Extra Small | 40 in³ | 3⅛" = **79.38mm** |
| Reminded (brass paw-print urn) — Medium, up to 70 lb | 70 in³ | 3⅜" = **85.73mm** |
| (unbranded listing found in the same search pass) | 110 in³ | 3½" = **88.90mm** |

**The honest, load-bearing finding from this data:** opening diameter does **not** track capacity
proportionally. Going from 35→40 in³ (+14% capacity) the opening jumps 66.7→79.4mm (+19%); going
from 40→70 in³ (+75% capacity) the opening barely moves, 79.4→85.7mm (+8%). Above roughly
35–40 in³, real competitor openings cluster tightly in the **79–89mm band regardless of exact
capacity** — consistent with a practical floor driven by remains-bag bulk, not by total ash
volume. **Our own 50 in³ target sits inside this cluster's capacity range** (above the 40 in³
Odyssey Extra Small, which already uses a 79.4mm opening) — by this real precedent, a
"conservative" Medium opening arguably shouldn't go much below ~79mm at all.

**The competing constraint, checked explicitly (mirroring Large's exact base-vs-collar
reasoning):** these competitor products are wide-mouth, full-lid jar-style urns, not this design's
narrow-vase-neck identity feature. Applying an ~79–89mm neck ID directly to this body's own,
much-smaller scale (base/collar radii computed in §4.5 land the naive-scaled base at ~80mm OD)
would put the collar meaningfully *wider* than the base — a more pronounced inversion of the
vessel's visual/physical hierarchy than Large ever accepted (Large's own collar-vs-base gap was
2mm/2%, "essentially at parity"; an 85mm-ID collar here would run roughly 20–30% over a
naively-scaled ~80mm base — not a comparable case).

**Decision: neck ID = 72mm (r=36mm), tagged `ESTIMATED`.** This is a deliberate compromise —
*below* the real ~79–89mm competitor cluster found for this capacity tier (a genuine,
named-here-plainly reduction from what full research would support), chosen specifically to keep
the collar from meaningfully overshooting this smaller body's own base OD (§4.5 resolves the
base/collar relationship explicitly, by widening the base to meet the collar rather than
shrinking the collar further — see below). This mirrors Large's own methodology exactly (Large
also chose 80mm, below its own cited 100mm/114–121mm research ceiling, for the identical
base-proportion reason) — but **the size of this compromise is larger here than it was for
Large**: Large's 80mm was near the *low end of, but still inside,* its own researched range
(70–100mm); this document's 72mm sits *below* the entire real-competitor cluster found for a
comparable capacity (79–89mm). **This is named as a materially higher risk than Large's
equivalent decision, not an equivalent one softened by analogy** — see §8 edge case 2 and the
open-items note in §10.

**What would change this:** if the `neck-fit-test-medium` physical test (§2) shows a real medium
remains bag doesn't comfortably pass 72mm, the fix — per the same precedent Large already set —
is widening the neck ID in a future revision, which may in turn require revisiting the base/collar
proportion resolution in §4.5, not resizing the whole body.

### 4.4 Base OD vs. collar OD — the proportion check, worked through rather than assumed

Naively scaling Large's base geometry by the linear factor (k≈0.822, applied to Large's own
clean, pre-manual-edit v1/v2 internal base radius of 45mm) gives an internal base radius of
**45 × 0.822 ≈ 37mm**. At the new 3.2mm nominal wall, that implies a naive base OD of
2×(37+3.2) ≈ **80.4mm**.

Collar OD, from the neck ID above (§4.3) plus a reinforcement wall (§6): **88mm** (derived below).
**88mm collar OD vs. a naively-scaled 80.4mm base OD is a 7.6mm/9.4% overshoot** — a real,
meaningfully bigger gap in relative terms than Large's own 2mm/2% "essentially at parity" case,
and not one this document is willing to wave away with the same language Large used for a
much smaller gap.

**Resolution: widen the base's *external* profile (foot wall) to close this gap, rather than
compromise the neck ID any further.** The base's internal radius (37mm, which sets the cavity
volume in §4.5) is left alone; only the external foot is thickened, from a naive 3.2mm (matching
the nominal side wall) up to **7mm**, giving:

```
Base external radius = 37mm + 7mm = 44mm → Base OD = 88mm
```

**This lands base OD at exactly 88mm — identical to collar OD, true parity, not just "close."**
This is directly analogous to Large's own floor-thicker-than-wall convention (Large's floor was
5mm against a 4mm wall, a 1.25× ratio, for base stability) — here the ratio is larger (7mm foot
vs. 3.2mm wall, ~2.2×) specifically because it's doing double duty: base stability **and**
closing the visual-hierarchy gap the neck-widening compromise in §4.3 would otherwise leave open.
Tagged `ESTIMATED` — a reasoned design decision, not a hard derivation.

**Confirming the vessel's visual hierarchy still holds:** belly OD (§4.5) comes out to ~120.4mm —
36% wider than the now-matched 88mm base/collar — comfortably the dominant, widest feature of the
silhouette, the same relationship Large's belly (153.9mm, 54–57% wider than its 98–100mm
base/collar) maintained. The proportion is slightly less pronounced than Large's (36% vs.
54–57%) but unambiguously in the same direction — no inversion.

### 4.5 Body profile — control points, tangencies, and the volume hand-calc

Same construction method as Large: a tangent-constrained spline (or chained cubic Bezier) through
these control points, revolved 360° — not a straight-frustum stack. Belly position held at
**~45% of total external height**, matching both Large's own concept-derived proportion and this
document's own worked-out heights below.

`Z_int` measured from the internal floor's top surface (0mm). `Z_ext = Z_int + 4mm` (the §4.2
floor thickness).

| Point | Z_int | Z_ext | Internal r | External r | Tangent condition |
|---|---|---|---|---|---|
| P0 — floor/base | 0mm | 4mm | 37mm | **44mm** (thickened foot, §4.4) | Horizontal (dr/dz=0) — smooth rounded foot, no sharp internal corner, same convention as Large. |
| P1 — belly max (broad plateau) | 55mm | **59mm (45.0% of 131mm)** | 57mm | 60.2mm | Broad, nearly-flat plateau, not a sharp point — same "ceramic vase" identity as Large. |
| P2 — shoulder (inflection) | 73mm | 77mm | 47mm | 50.2mm | Tangent-continuous, spline-default inflection, no cusp — Coder to confirm curvature comb shows no reversal before revolving, same check Large's spec calls for. |
| P3 — neck-taper-end / base of collar | 115mm | 119mm | 36mm | ~39.2mm | dr/dz → 0, flattening into the constant-radius collar section above it. |
| P4 — rim / top of collar | 127mm | **131mm** | 36mm | **44mm** | Constant radius P3→P4, a true vertical cylinder (dr/dz=0 throughout), same as Large. |

All radii/heights above are `DERIVED — sizing decision` (chosen to hit the §4.1 volume target
while carrying forward the concept's silhouette proportions and the §4.3/§4.4 neck/base
decisions), except P0/P4's external 44mm figures, which are `ESTIMATED` per §4.4's reasoning.

#### Volume hand-calc (frustum approximation, same method Large used at every revision)

`V = (π·h/3)(r1² + r1·r2 + r2²)`, all radii internal (cm for convenience):

| Segment | Internal r1 → r2 | Height | Volume |
|---|---|---|---|
| 1. Floor (P0) → belly max (P1) | 37mm → 57mm | 55mm | 387.46 cm³ |
| 2. Belly max (P1) → shoulder (P2) | 57mm → 47mm | 18mm | 153.4 cm³ |
| 3a. Shoulder (P2) → neck-taper-end (P3) | 47mm → 36mm | 42mm | 228.6 cm³ |
| 3b. Straight neck/collar (P3→P4) | 36mm (constant) | 12mm | 48.86 cm³ |
| **Total internal volume** | | **127mm internal height** | **≈818.3 cm³** |

```
818.3 cm³ vs. 819.4 cm³ target → −0.13% — well inside the ±5% routine-tolerance band.
Back-check: 818.3 cm³ ÷ 16.3871 cm³/in³ ≈ 49.93 in³ ✓ matches the 50 in³ target.
Sanity check on heights: 55+18+42+12 = 127mm internal ✓; +4mm floor = 131mm external ✓.
Belly position check: Z_ext = 59mm; 59 ÷ 131 = 45.04% ✓ matches the 45% target.
```

**Same named caveat as every prior revision of Large's spec:** this is a straight-chord frustum
approximation, not the literal volume of the tangent-constrained spline that will actually be
built — a true spline through a broad apex/plateau tends to bulge slightly outward past the
straight chords near the belly (adds volume), while a concave "waist" pulling toward the neck
sits slightly inside its chord (removes volume). These effects partially offset but can't be
hand-computed precisely for a spline. **The Coder must verify the true modeled internal volume
via the CAD tool's mass-properties function once the real geometry exists, and flag back for a
spec revision if it falls outside the 778.4–860.3 cm³ band (±5% of 819.4 cm³).** Given the
hand-calc already sits at only −0.13%, there is real headroom before a deviation would require a
tweak — same low-risk framing Large's own v2 hand-calc carried.

### 4.6 Overhang / print-orientation re-check — recomputed from scratch, not assumed from Large's angles

External radii at each segment (internal + wall, per §4.5):

| Transition | External Δr | Height | Angle from vertical | Class | Risk |
|---|---|---|---|---|---|
| Base (44mm) → belly (60.2mm) | +16.2mm (expanding) | 55mm | atan(16.2/55) ≈ **16.4°** | Gentle flare, monotonically expanding but shallow | None — self-supporting, gentler than Large's own ~22° equivalent |
| Belly (60.2mm) → shoulder (50.2mm) | −10.0mm (shrinking) | 18mm | atan(10/18) ≈ **29.1°** | Shrinking-radius ("shrinking cone") class | None — radius never increases with height here, the class this project has established is inherently self-supporting regardless of local angle |
| Shoulder (50.2mm) → neck-taper-end (39.2mm) | −11.0mm (shrinking) | 42mm | atan(11/42) ≈ **14.7°** | Shrinking-radius class, long and gentle | None — a long, shallow taper, gentler than Large's post-widening equivalent (~5–14°, depending on revision) |
| Neck-to-collar external blend (39.2mm → 44mm) | +4.8mm (expanding) | ~6mm (proportional to Large's own 47%-of-collar-height blend span, scaled to this document's 12mm collar height) | Chord angle atan(4.8/6) ≈ 38.7°; **peak local angle on a tangent-constrained S-curve is empirically higher than the chord angle** (Large's own measured case: a 40.6° chord produced a 47.25° measured peak, a ×1.16 ratio) — extrapolating that same ratio here gives an estimated **peak ≈ 44.9°, call it ~45°** | Real overhang class (radius grows with height), but on a short, fully closed 360° revolve | **Low — the one disclosed "watch it on the first print" zone, same category Large has flagged at every revision.** This is a reasoned estimate extrapolated from a single prior data point, not a fresh CAD measurement — tagged `ESTIMATED`, flag for Coder/Tester confirmation once built, exactly Large's own standing practice for this same transition. |

**Net conclusion:** every segment except the neck-to-collar external blend is comfortably
self-supporting; the blend sits right at (not clearly over) the conventional 45° guideline —
arguably slightly *less* risky than Large's own equivalent zone (Large measured 45.6–47.25°
across its revisions, consistently over 45°), though this is an extrapolated estimate, not a
measurement, and should be re-verified once the real geometry exists.

**Print orientation, decided here per this document's own convention (not left to the Coder):
base (flat, 88mm OD) down on the bed, opening/neck facing up.** Matches the part's natural
resting stance, gives a large stable 88mm-diameter bed-adhesion footprint, and is the only
orientation consistent with every segment above being self-supporting or only mildly at-risk at
one small, disclosed zone — same reasoning, independently re-verified at this size's own actual
geometry, not assumed to carry over from Large.

---

## 5. Lid derivation

Same v7 design language as Large, carried forward as-is: flush flat brim (zero overhang), a dome
rising to a flattened plateau, a straight-walled capped alignment plug on the underside, no
handle, no magnet features. Every absolute dimension below is freshly derived for this body's own
scale, not copied from Large.

### 5.1 Brim

**Brim OD = collar OD = ~~88mm~~ 87.700mm, zero-to-flush fit** (the v7 flush-fit identity rule,
carried forward exactly). Tagged `DERIVED` from §4.4's collar OD.

> **POST-v1 FIX (2026-09-09), applied to the lid only, collar OD unchanged at 88.000mm on the
> body:** the Tester's RE-TEST pass (see `tests.md`/`verdict.md`) measured this brim-to-collar
> interface as an exact 88.000mm = 88.000mm zero-clearance fit — the same named risk this section
> already called out below, now confirmed as a real (not hypothetical) zero-margin condition. Per
> the requester's explicit, confirmed instruction, the same **-0.3mm negative allowance** Large
> applied to its own identical flush brim/collar fit (122mm-brim-shrink era, see Large's own
> `parameters.md`) is applied here: brim OD built to **87.700mm** against the collar's unchanged
> 88.000mm OD. This is a lid-only geometry edit (two sketch points moved on `LidProfile`, radius
> 44.000mm → 43.850mm); no other lid dimension (dome, plateau, plug OD/wall/clearance/cap) was
> touched. See archived pre-fix deliverables at `medium/archive/pre-brim-tolerance-fix/`.

**Brim thickness: 8mm.** Large's 10mm (chosen in its own v7 pass partly for a thicker ceiling
over the plug void, partly for structural feel) scaled by the same linear factor k≈0.822:
10 × 0.822 ≈ 8.2mm, rounded to 8mm. Tagged `ESTIMATED`. Check: 8mm is **10× the 0.8mm floor** —
trivially clear.

**Named risk carried forward unchanged from Large's v7 identity choice (now resolved by the
POST-v1 FIX above):** an exact-match 88mm-to-88mm brim/collar edge has zero print-tolerance
margin to absorb ordinary FDM dimensional variance. Per this project's own documented FDM
tendency (external bosses/rims print slightly oversized more often than undersized), the more
likely first-print outcome is a lid brim reading as very slightly proud of the collar edge rather
than perfectly flush — cosmetic, not functional, same as Large's own disclosed risk (§8 edge case
3). If the first print reads proud, a small 0.2–0.3mm negative allowance on the brim OD (the same
fix Large named for itself) is the straightforward correction for a future revision — **this
allowance has now been applied, per the POST-v1 FIX note above.**

### 5.2 Dome

**Dome base OD: 70.4mm.** Preserving the same 0.80 dome-to-brim ratio Large used at every
revision of its own lid: 88mm × 0.80 = 70.4mm. Tagged `ESTIMATED` (ratio-preservation, same
method/tag as Large used for its own dome base).

**Dome height above brim top: ~25mm.** Large's own dome used a height-to-base-radius ratio of
h/a = 30mm/40mm = 0.75 (pre-flattening). Applying the same ratio to this dome's own base radius
(a=35.2mm): 0.75 × 35.2 ≈ 26.4mm, then reduced by ~1mm for the same reason Large's own flattening
blend reduced its dome height by ~1mm (the tangent blend into a flat plateau consumes a small
amount of the curve's height near the apex) → **≈25mm**. Tagged `ESTIMATED`.

Sphere-radius hand-calc (same method as Large, `R = (a²+h²)/(2h)`, using the pre-blend h=26mm):
```
R = (35.2² + 26²) / (2×26) = (1239.04 + 676) / 52 = 1915.04 / 52 ≈ 36.83mm
```

**Dome apex — flattened plateau, ≈19mm diameter (r≈9.5mm).** Preserving Large's own final
built ratio (21.73mm ÷ 80mm ≈ 27.2%, itself an approximation of an intended ~27.5%) applied to
this dome's own 70.4mm base: 0.272 × 70.4 ≈ 19.1mm. Tagged `ESTIMATED`.

**Printability check, per the task's explicit ask:** 19mm is comfortably above any FDM minimum
feature-size concern for a flat terminal disc — smaller than Large's own 21.73mm plateau, which
itself had no printability issue. **No risk flagged here** — this is the one item in this
document's re-derivation list that carries over cleanly at the smaller scale without needing a
compromise.

The apex-drooping/ribbing risk mechanism (a near-degenerate closing point) is eliminated by the
flat plateau exactly as it was for Large — same mechanistic reasoning, not re-argued here.

### 5.3 Alignment plug (lid underside)

**Clearance — kept at 0.5mm diametral, NOT shrunk further. This is the answer to the task's own
explicit question, reasoned through rather than defaulted.** Large derived 0.5mm diametral
clearance for its 80mm-ID neck by scaling up (in absolute terms, not by ratio) from a 0.2mm
precedent used at 6mm-magnet scale — reasoning that a larger circular feature accumulates more
absolute roundness/shrinkage variance over its longer circumference. This document's own neck ID
(72mm) is only ~10% smaller in diameter than Large's 80mm — not a large enough change to
meaningfully reduce the circumference-driven error accumulation that justified 0.5mm in the first
place. More importantly, per the task's own framing: **FDM clearance-fit tolerance is arguably
closer to a fixed practical minimum set by printer/material capability (typically on the order of
±0.15–0.25mm per surface for a well-tuned desktop FDM printer) than a value that should shrink
proportionally with part size.** Below roughly 0.4mm diametral, the already-named PETG-lid/PLA-body
material-shrinkage mismatch risk (carried forward from Large, unchanged — different materials
shrink differently) risks consuming the entire clearance margin, turning a clearance fit into an
unintended interference fit. **Decision: hold 0.5mm diametral clearance unchanged.** Tagged
`ESTIMATED`, same reasoning class as Large's own figure, now explicitly re-justified rather than
carried over by default.

```
Plug OD = 72mm ID − 0.5mm clearance = 71.5mm
```

**Plug wall: 3.2mm, matching this document's own nominal body wall** (§4.2) — the same internal
consistency Large held (Large's 4.0mm plug wall exactly matched Large's own 4.0mm nominal body
wall). Check: 3.2mm is 4× the 0.8mm floor — clear with the same margin as the body's own wall.

**Plug depth: 8mm.** The internal bore is a constant-ID (36mm r) straight cylinder for the full
12mm collar-height span (P3→P4, §4.5) — the same convention Large used, where the constant-ID
zone matched the collar height exactly. An 8mm plug within that 12mm zone leaves a **4mm
collision margin above P3**, before the bore would start widening toward the shoulder — a 33%
margin-to-depth ratio, matching Large's own 5mm-margin-in-15mm-bore ratio (also 33%) almost
exactly. Tagged `DERIVED` from the collision-margin-matching logic, not an arbitrary depth pick.

**Cap: 3mm solid disc nearest the tip, 5mm hollow nearest the brim (8mm total, unchanged from
above).** Carries forward Large's v7 sealed-void identity choice (a straight-walled plug capped
at the tip, rejected tapered-stopper alternative — same ~63°-overhang reasoning Large already
worked through and this document does not re-litigate, per the task's explicit instruction).
Proportion (5:3 hollow:solid ≈ 1.67:1) is close to Large's own 6:4 (1.5:1) split, not identical,
chosen simply to keep the solid cap a clean 3mm (comfortably over the 0.8mm floor with real
margin, given how thin this cap already is relative to Large's 4mm).

### 5.4 Lid summary table

| Parameter | Value | Tag |
|---|---|---|
| Brim OD | ~~88mm~~ **87.700mm** (built with a -0.3mm allowance against the collar's unchanged 88.000mm OD — POST-v1 FIX, 2026-09-09, see §5.1) | DERIVED |
| Brim thickness | 8mm | ESTIMATED |
| Dome base OD | 70.4mm | ESTIMATED |
| Dome height above brim | ~25mm | ESTIMATED |
| Dome apex plateau diameter | ~19mm (r≈9.5mm) | ESTIMATED |
| Plug OD | 71.5mm | DERIVED (72mm ID − 0.5mm clearance) |
| Plug wall | 3.2mm | ESTIMATED (matches nominal body wall) |
| Plug depth | 8mm (4mm collision margin above P3) | DERIVED |
| Plug cap | 3mm solid + 5mm hollow (8mm total) | ESTIMATED |
| Total lid height (seating plane to plateau top) | ~33mm (8 brim + 25 dome) | DERIVED |
| Total lid bounding-box height (plug tip to plateau top) | ~41mm (33 + 8 plug) | DERIVED |

**Print orientation: flat-underside-down (plug-tip-down), dome facing up** — same reasoning
Large re-verified at its own v7 pass: this orientation gives the entire seating surface zero
overhang and full bed contact, the dome's radius shrinks monotonically from plug-tip to plateau
(self-supporting class throughout), and the plug's solid tip cap lands as a bed-supported first
layer rather than an unsupported bridge over a sealed void. Flipping the part (plateau-down) would
invert the dome into an expanding-cone overhang needing support under nearly its whole visible
exterior and would turn the tip cap into an unsupported last-layer bridge — the same conclusion
Large reached, independently re-checked against this document's own (smaller) geometry rather
than assumed to carry over.

**Watch-items, carried forward unchanged in kind from Large:** (1) the internal ceiling bridge
where the plug's hollow interior meets the solid brim above it — expect sag/stringing under
default settings, sealed and never visible, doesn't matter; (2) confirm slicer supports are set to
"touching build plate only" before slicing, so no unremovable support generates inside the sealed
plug void; (3) the brim/collar flush-fit print-tolerance risk (§5.1).

---

## 6. Collar reinforcement — proportion re-derived, not held at Large's absolute 10mm

Large kept a 10mm collar wall (2.5× its own 4mm nominal wall) purely for structural margin and
rim character, no longer for magnet housing (that purpose ended at Large's own v3). The task asks
whether an *absolute* 10mm band is still proportionate at this smaller scale — it is not, and the
right fix is to hold the *ratio*, not the absolute figure:

```
Large's collar-wall-to-nominal-wall ratio: 10mm ÷ 4mm = 2.5×
Applied to this document's own 3.2mm nominal wall: 3.2mm × 2.5 = 8.0mm
```

**Collar wall: 8mm.** Tagged `ESTIMATED`, same convention/reasoning class as Large's own figure,
re-derived at the new wall baseline rather than held at Large's absolute number. This produces:

```
Collar OD = 72mm ID + 2×8mm = 88mm
```

— which happens to land exactly at parity with the widened base OD (§4.4), a clean, corroborating
convergence rather than a forced result (the base-widening decision in §4.4 was made independently,
before this ratio calculation, and the two numbers meeting exactly at 88mm is a useful confirmation
that both derivations are pulling in a consistent direction, not a coincidence being leaned on as
proof of correctness).

| Parameter | Value | Tag |
|---|---|---|
| Collar height | 12mm | ESTIMATED — k≈0.822 scale of Large's 15mm |
| Collar OD | 88mm | DERIVED — 72mm ID + 2×8mm reinforcement wall |
| Collar ID | 72mm | Matches neck ID (§4.3) |
| Collar wall thickness | 8mm | ESTIMATED — holds Large's own 2.5× nominal-wall ratio, re-derived at this document's 3.2mm nominal wall |

No pockets, bosses, or recesses of any kind on the collar top or lid underside — carried forward
unchanged from the v3/v7 line-wide identity decision.

---

## 7. Material recommendation

**Body: matte or silk PLA.** Same reasoning as Large, unchanged by scale — matte/silk PLA reads
closer to the "stoneware, not plastic" finish goal than glossy PLA or PETG's default sheen.

**Lid: PETG.** Same reasoning as Large, unchanged by scale — better heat/UV resistance and
impact toughness for the part that's repeatedly picked up and set down (by hand, gripping the
brim/dome edge — there is no handle, carried forward from the line-wide v7 identity decision).
Same named finish-mismatch risk as Large (PETG's default gloss vs. matte/silk PLA) — a sanding
pass targeted more aggressively at the lid is the same mitigation Large specifies.

**Named risk, carried forward unchanged: PLA (including matte/silk) can soften/warp under
sustained heat/UV exposure** (sunny windowsill, near a heat vent) — accepted for the body because
the finish requirement specifically calls for a PLA variant, same tradeoff Large accepted, same
risk named plainly rather than absorbed silently (§8 edge case 3).

---

## 8. Edge cases

1. **Pet weight lands near or outside the 25–50 lb bracket boundary.** A pet at, say, 22 lb would
   be better served by the sibling Small build (0–25 lb, planned separately, not in this
   document's scope); a pet at 55–60 lb sits closer to Large's own bracket. This urn is sized to
   the *top* of its own stated range (50 lb, §4.1) as a deliberate single-size decision — a
   smaller pet within the 25–50 lb bracket will simply use less than the ~819 cm³ built capacity,
   which is expected and accepted, same reasoning Large's own edge case 1 uses for its bracket.
2. **Remains bag too bulky/stiff to pass through the 72mm neck opening — the highest-risk item in
   this entire document, more so than the equivalent risk on Large.** §4.3 chose 72mm as a
   deliberate compromise **below** the real ~79–89mm competitor cluster found for this exact
   capacity tier (not merely below a wider aspirational range the way Large's 80mm was) — chosen
   specifically to avoid inverting the base/collar proportion at this smaller scale (§4.4). This
   is `ESTIMATED` and untested against a real bag. The `neck-fit-test-medium` article (§2) exists
   specifically to physically close this out before committing to the full body print. If a real
   medium-pet remains bag doesn't comfortably pass 72mm, the fix is widening the neck ID in a
   future revision — which, per §4.4, may also require re-opening the base-widening decision, not
   just the neck number in isolation, since the two were resolved together.
3. **Sustained heat or direct sunlight exposure** (sunny windowsill, near a heat vent) — the body's
   PLA can soften/warp under prolonged heat/UV, same standing shop risk Large's spec names, same
   acceptance reasoning (the finish requirement specifically calls for a PLA variant), surfaced
   here rather than silently absorbed into the material recommendation.

---

## 9. Print orientation — summary (full reasoning in §4.6 body, §5.4 lid)

- **Body: base (flat, 88mm OD) down on the bed, opening/neck facing up.** Re-verified from
  scratch against this document's own geometry (§4.6), not assumed to carry over from Large.
- **Lid: flat underside down (plug-tip-down), dome/plateau facing up.** Re-verified from scratch
  against this document's own geometry (§5.4), same conclusion as Large for the same reasons,
  independently re-checked rather than assumed.

---

## 10. Cost estimate

**Body material volume: ≈145.0 cm³** (§4.2 — the figure the nominal wall thickness was explicitly
derived to hit, so this is by-construction rather than independently measured; to be replaced by
real CAD mass-properties once built, per §4.5's own caveat).

**Lid material volume: ≈108 cm³** (ESTIMATED — Large's own built v7 lid material volume,
194.2929 cm³, scaled by the volume ratio k³ = 819.4/1474.8 = 0.5556: 194.29 × 0.5556 ≈ 107.9 cm³.
This is a rougher estimate than the body's figure, since the lid's individual features were
re-derived by several different methods above rather than one consistent scale factor — flagged
here plainly rather than presented with false precision, and, same as every other volume figure
in this document, to be replaced by a real CAD mass-properties query once built.)

Using the same PLA (~1.24 g/cm³) / PETG (~1.27 g/cm³) densities and the same ~$20–25/kg filament
price assumption implied by Large's own cost figures:

| Part | Material volume | Mass | Cost |
|---|---|---|---|
| Body (PLA) | ≈145.0 cm³ | ≈180g | ≈$3.60–4.50 |
| Lid (PETG) | ≈108 cm³ | ≈137g | ≈$2.74–3.43 |
| **Combined pair** | | | **≈$6.30–7.90** |

A small, reasonable cost for a decorative memorial piece — notably lower than Large's own
~$12.0–14.9 combined figure, consistent with this being a genuinely smaller build, not just a
renamed copy of Large's numbers.

---

## 11. Question back to the requester

**What slicer settings should be used (layer height, infill)?** No layer height or infill target
has been specified for this size, same open question Large's own spec carries. Given this is a
decorative, low-mechanical-stress vessel (no handle, lid lifted by hand at the brim/dome edge,
body only carries the modest static weight of a bagged-remains payload), a reasonable default
absent other direction would be **0.16–0.2mm layer height** (finer layers matter more given the
"doesn't feel like plastic" finish bar, §7, and the lid's flat plateau top surface, §5.2) and
**15–20% infill** (this isn't a structural load case needing high infill) — please confirm or
state a preference before the Coder locks in export settings. Also confirm the lid's support
setting is "touching build plate only" before slicing (§5.4) — bundled into the same settings
confirmation since both need to be locked before export.

---

## 12. Summary of items the Director should weigh before Coder work starts

Named here explicitly, per instruction, rather than left implicit:

1. **§4.3's neck ID (72mm) is a bigger compromise, relative to its own supporting research, than
   Large's equivalent 80mm decision was.** Real competitor data for this capacity tier clusters at
   79–89mm; 72mm sits below that entire cluster, chosen to protect the base/collar proportion at
   this smaller scale. This may be the single item most worth a second look before committing to a
   full print, ahead of the `neck-fit-test-medium` physical test.
2. **§4.4's base-widening resolution (thickening the foot from 3.2mm to 7mm to hit exact parity
   with the collar) is a design decision made to resolve #1's downstream consequence, not a
   hard requirement.** If the neck ID changes in a future revision, this foot-thickness decision
   should be revisited alongside it, not left stale.
3. **§4.2's wall thickness (3.2mm) and §5.3's plug clearance (0.5mm, held unchanged from Large)
   and plug wall (3.2mm) are all genuinely re-derived, not naive scales — but they are still
   `ESTIMATED`, not `VERIFIED`, and the plug clearance in particular carries the same
   PETG-lid/PLA-body material-shrinkage risk Large already named.** A test coupon before
   committing to the full lid print (same recommendation Large's own spec makes) is worth
   repeating here.
4. **Every dimension in this document is a spec-time hand-calc or reasoned estimate, none of it
   has been checked against real CAD mass-properties yet** — that verification, and the standing
   ±5% volume-tolerance flag-back rule, applies to this document exactly as it did to every
   revision of Large's.

---

## 13. Revision history

| Version | What changed | Why |
|---|---|---|
| v1 (this document) | Initial spec for the Medium size (25–50 lb, sized to 50 lb / 819.4 cm³ target). Derived a fresh nominal wall thickness (3.2mm, via a material/cavity-ratio proportionality argument, not a linear scale of Large's 4mm), a fresh floor thickness (4.0mm, holding Large's 1.25× floor:wall ratio), fresh competitor research into medium-tier pet urn opening diameters (real manufacturer listings, 66.7–88.9mm across 35–110 in³ capacities, revealing opening diameter does not scale linearly with capacity), a neck ID decision (72mm, a compromise below the researched 79–89mm cluster for this capacity tier, chosen to protect the base/collar visual hierarchy), a base-widening resolution (foot thickened to 7mm to reach exact parity with the 88mm collar OD), a full body control-point table and volume hand-calc (≈818.3 cm³ vs. 819.4 cm³ target, −0.13%), a fresh overhang/orientation re-check, a full lid re-derivation (brim/dome/plateau via ratio-preservation from Large's own proportions, plug clearance held at Large's 0.5mm as a reasoned fixed-practical-minimum rather than scaled down further, plug wall matched to the new nominal body wall), a re-derived collar reinforcement wall (8mm, holding Large's 2.5× nominal-wall ratio rather than its absolute 10mm), and a cost estimate (≈$6.30–7.90 combined, vs. Large's ≈$12.0–14.9). | First planning pass for the Medium size, per the Director's task framing: reuse the Large product line's settled v7 visual identity as-is, but independently re-derive every dimension that is genuinely scale-dependent (wall thickness, plug clearance/wall, neck opening, overhang angles, collar reinforcement) rather than naively shrinking Large's absolute numbers. |
| v1.1 (lid-only fix, 2026-09-09) | **Brim OD reduced from 88.000mm to 87.700mm on the lid only** (collar OD unchanged at 88.000mm on the body) — a -0.3mm negative allowance on the zero-clearance flush brim-to-collar fit the Tester's RE-TEST pass measured exactly at 88.000mm = 88.000mm (see `tests.md` §7, `verdict.md` item 2). Two `LidProfile` sketch points moved (radius 44.000mm → 43.850mm); no other lid dimension changed. Re-verified: single solid body (unchanged face/edge/vertex counts 13/11/11), plug OD/wall/depth/cap and dome base/height/plateau all bit-identical pre/post edit, lid material volume 124.1914 cm³ → 123.862 cm³ (Fusion mass-properties; a −0.329 cm³ / −0.27% delta consistent with only a thinner brim ring), brim OD measured 87.700mm on the live B-rep (exact cylindrical face radius 43.850mm) and independently confirmed on the exported STEP/3MF/STL. Pre-fix `urn-lid-medium.step/.3mf/.stl` archived to `medium/archive/pre-brim-tolerance-fix/` before overwriting. | Applied per the same precedent already established on Large's own identical flush-brim/collar fit (see Large's `parameters.md`), per explicit confirmed instruction from the requester, to avoid a proud/binding lid edge from normal FDM dimensional variance on an as-designed zero-margin mating diameter. |
