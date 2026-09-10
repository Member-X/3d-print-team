# Spec — Pet Memorial Urn (Small / 0–25 lb pet size), v1

## 0. Project structure — read this first

**This project now uses a size-named-subfolder structure.** The existing "Large" build (target
50–90 lb pet, built to ~90 lb, CAD-complete and Reviewer-approved, with an unconfirmed physical
neck-fit test still pending) remains exactly where it is, untouched and unmoved, at the
`pet-memorial-urn/` project root — `step/`, `3mf/`, `stl/`, `dot_pipeline/`, `render/`, `archive/`,
`parameters.md`, `README.md`. **Nothing in this document changes, references-for-editing, or
depends on any of those files being modified.** This spec was produced by reading the Large build's
`dot_pipeline/specs.md`, `parameters.md`, `README.md`, and `concept/brief.md` in full, strictly as
read-only reference for the shared design language (§1 below) — no file under the Large paths above
was written to.

**This build — "Small," target weight bracket 0–25 lb, sized to the top of the range (25 lb) — lives
entirely under `pet-memorial-urn/small/`**, with its own `dot_pipeline/`, `step/`, `3mf/`, `stl/`
subfolders. The Coder, Tester, and Reviewer who work from this spec should write **exclusively**
within `pet-memorial-urn/small/`. Every deliverable filename carries a `-small` suffix specifically
so files are never confused with Large's identically-shaped, differently-sized parts if anyone ever
copies files between the two size folders.

This is a **single-size build** (Small only). It is a sizing/derivation exercise against an
already-approved visual identity, not a new design pass — no concept-designer phase was used, and
none of the identity decisions in §1 below are being re-litigated, only re-scaled and, where the
task specifically calls for it, re-derived with fresh reasoning (§4, §6–§9).

---

## 1. Design identity carried forward as-is (not re-derived)

The following are the established v7 identity decisions for the whole product **line**, not a
Large-only choice, and are carried forward unchanged in kind:

- **No magnet-assisted closure.** No pockets, bosses, or recesses of any kind on the collar top or
  lid underside, on either part.
- **No handle or grip feature of any kind on the lid.** A plain dome, gripped by hand at the
  brim/dome edge. This is the line's confirmed identity as of Large v7 — not re-added here.
- **Body silhouette:** a smooth, continuously-curved "ceramic vase" profile — flat floor, rising
  into a broad low belly (plateau, not a sharp point) at roughly 45% of total height, tapering
  through a shoulder into a neck, then a short constant-radius collar band at the rim. Built as a
  tangent-constrained spline (chained cubic Bezier) through the control points in §5, not straight
  frustum segments.
- **Lid:** a flat brim disc sized to sit **flush** with the body's collar OD (zero overhang), topped
  by a dome rising to a **flattened plateau apex** (not a fully rounded point) — same reasoning as
  Large v7 (a flat spot reads more intentional with no handle, and eliminates apex-drooping print
  risk). Dome base OD follows the same ~0.80 dome-base-to-brim-OD ratio Large used, re-derived
  against *this* build's own brim value (§8), not assumed to be 80mm.
- **Lid underside:** a straight-walled (not tapered/stopper-shaped) hollow cylindrical
  alignment/friction-fit plug hanging into the neck bore, capped at its tip with a solid disc (a
  sealed void), same as Large v7. Large evaluated and rejected a tapered stopper shape because it
  needs a support-unfriendly ~63° overhang; that reasoning is carried forward, not re-litigated.
- **Materials:** body = matte or silk PLA; lid = PETG — kept for general toughness on thin-fillet
  transitions, same carried-forward default Large uses (§10).
- **Printer:** P2S-class FDM, 256×256×256mm build volume, 0.4mm nozzle assumed (ESTIMATED, standard
  shop default per every prior spec in this repo).

Everything below this point is either a straightforward re-scale of a fixed dimension (e.g., "hold
the same absolute FDM clearance because it's a process tolerance, not a part-size-driven fit") or a
**genuinely fresh derivation** for six items the task specifically flagged as not safe to
naive-scale: nominal wall thickness (§7), plug clearance/wall (§9.2), neck opening size (§6), print
orientation/overhang angles (§11), collar reinforcement wall (§7.3), and dome apex plateau size
(§8.3).

---

## 2. Source key (dimension provenance)

Same three-tag convention established on the Large build, used identically here:

| Tag | Meaning |
|---|---|
| **VERIFIED** | Independently confirmed — a real measurement, a manufacturer/competitor spec sheet figure actually found and cited, or (once built) a CAD mass-properties query on the real geometry. |
| **DERIVED — sizing decision** | Computed from the requester's explicit rule-of-thumb math (1 in³ per lb) or from another already-fixed dimension, with the formula shown. |
| **ESTIMATED** | A design convention, judgment call, or competitor-research-informed best guess not independently confirmed against a real object or measurement. |

**Highest-risk item in this spec, named up front:** the neck/collar opening ID is the one dimension
that mates with a real external object (a crematorium remains bag for a 0–25 lb pet) that this team
does not have in hand. Real competitor research was done for it (§6) — it is not a bare guess — but
it remains `ESTIMATED`, not `VERIFIED`, and is called out as a named risk exactly as Large's
equivalent figure was. The `neck-fit-test-small` article (§3) exists specifically to close this out
physically before the full body is printed.

---

## 3. Files (Coder deliverables)

All paths relative to the repo root; all live under `pet-memorial-urn/small/`.

| File | Purpose |
|---|---|
| `pet-memorial-urn/small/step/urn-body-small.step` | Editable CAD source for the Small body, parametric if the tool supports it |
| `pet-memorial-urn/small/step/urn-lid-small.step` | Editable CAD source for the Small lid |
| `pet-memorial-urn/small/3mf/urn-body-small.3mf` | Slicer-ready body, orientation baked in per §11 |
| `pet-memorial-urn/small/3mf/urn-lid-small.3mf` | Slicer-ready lid, orientation baked in per §11 |
| `pet-memorial-urn/small/stl/urn-body-small.stl` | Final body mesh |
| `pet-memorial-urn/small/stl/urn-lid-small.stl` | Final lid mesh |
| `pet-memorial-urn/small/step/neck-fit-test-small.step` | **Standalone neck/collar fit-test article — do not skip.** See note below. |
| `pet-memorial-urn/small/3mf/neck-fit-test-small.3mf` | Slicer-ready fit-test article |
| `pet-memorial-urn/small/stl/neck-fit-test-small.stl` | Final fit-test-article mesh |

Body and lid are two separate printed parts, each independently manifold/watertight, not printed in
place and not glued together — the lid rests removably on the body's collar rim, same as Large.

**`neck-fit-test-small` — required, not optional.** A small standalone print of just the neck-taper
+ collar section (flange-cut at the bottom for bed stability, open bore both ends), sized to this
spec's derived **70mm ID / 74.8mm neck OD / 82mm collar OD** (§6, §7), so the requester can
physically verify a real small-pet remains bag fits before committing to the full body print. This
is the single most load-bearing open item in this spec (§6, §14) — the same category of item that
was flagged as "easy to forget" on the Large build. Approximate size: ~26mm tall, ~100mm max OD at
the stabilizing base flange (§6.5).

---

## 4. Printer constraints (stated up front)

| Constraint | Value | Tag |
|---|---|---|
| Printer | P2S-class FDM | Per user memory / task instruction |
| Build volume | 256 × 256 × 256mm | Per user memory (`user_printer_specs.md`) |
| Nozzle diameter | 0.4mm (assumed standard) | ESTIMATED — standard shop default, per every prior spec in this repo, this one included |
| Minimum wall/boss thickness implied | ≥0.8mm (2× nozzle) for any wall or boss under load | Computed from the line above — this is the floor every wall figure in this spec is checked against, not an afterthought |
| Body fits build volume? | ~98mm max OD (belly) × 75.7mm H (§5) | **Yes**, trivially — over 2.5× margin on every axis |
| Lid fits build volume? | ~81.7mm max OD × 35mm bounding-box H (§8) | **Yes**, trivially |
| `neck-fit-test-small` fits build volume? | ~100mm max OD × ~26mm H (§6.5) | **Yes**, trivially |

Combined assembled height (body rim + lid above its seating plane) is **≈104.7mm** (75.7mm body +
29mm lid, §8) — each part is printed as a separate job, so this is not a bed-fit constraint either
way, exactly as on the Large build; noted here only for completeness.

**Wall-floor compliance, checked at the end of every section that introduces a new wall/boss, and
summarized in one place here:**

| Feature | Thickness | Multiple of the 0.8mm floor |
|---|---|---|
| Nominal body wall (§7.1) | 2.4mm | 3.0× |
| Floor (base) thickness (§7.2) | 3.0mm | 3.75× |
| Collar reinforcement wall (§7.3) | 6.0mm | 7.5× |
| Alignment plug wall (§9.2) | 2.4mm | 3.0× |
| Alignment plug tip cap (§9.3) | 2.5mm | 3.125× |
| Brim thickness (§8.1) | 6.0mm | 7.5× |
| Dome | Solid (no thin-wall feature) | N/A — no thin-wall risk |

Every wall in this design clears the floor with at least 3× margin — none of them are close to it.

---

## 5. Sizing derivation — internal volume target and body dimensions

### 5.1 Volume target

Per the requester's rule of thumb (identical to the one used for Large): ~1 in³ of internal usable
volume per pound of pet body weight, sized to the **top** of the stated 0–25 lb range, since
oversizing capacity is preferable to undersizing it for cremated remains.

```
Target internal volume = 25 lb × 1 in³/lb = 25 in³
25 in³ × 16.3871 cm³/in³ = 409.6775 cm³
```

**Target: 409.6775 cm³ internal cavity volume.** Tagged `DERIVED — sizing decision`, exactly the
same status as Large's original 1474.8 cm³ figure — a deliberate application of the requester's rule
to the top of the stated weight range, not an independently measured or manufacturer-sourced number.

**Routine tolerance band (same ±5% convention as Large):** 389.19 cm³ – 430.16 cm³. If the Coder's
as-built CAD mass-properties query lands outside this band, flag back for a spec revision rather
than silently accepting or silently forcing a fix — the same honesty rule used throughout the Large
build's revision history.

### 5.2 Method — why a cube-root scale baseline, then deliberate departures from it

409.6775 cm³ ÷ 1579 cm³ (Large's current as-built cavity) ≈ 0.2595 of Large's volume. A pure
uniform (isotropic) linear scale that preserves Large's exact silhouette and aspect ratio would use
a scale factor `s = 0.2595^(1/3) ≈ 0.6378` applied to every one of Large's linear dimensions. This
is used below **only as a starting reference baseline**, not as the final answer — the task
explicitly (and correctly) rules out naive-scaling several specific dimensions, and this section
shows where the naive baseline is kept and where it is deliberately overridden, with the reasoning
for each departure spelled out in its own subsection:

| Dimension | Large (mm) | Naive ×0.6378 scale (mm) | What this spec actually uses | Kept naive scale, or deliberately overridden? |
|---|---|---|---|---|
| Nominal body wall | 4.0 | 2.55 | **2.4mm** | Close to naive scale, independently re-justified — §7.1 |
| Floor (base) thickness | 5.0 | 3.19 | **3.0mm** | Close to naive scale, independently re-justified — §7.2 |
| Collar reinforcement wall | 10.0 | 6.38 | **6.0mm** | Close to naive scale, independently re-justified — §7.3 |
| Neck/collar ID | 80.0 | 51.0 | **70.0mm** | **Deliberately overridden** — fresh competitor research, §6 |
| Plug diametral clearance | 0.5 | 0.32 | **0.5mm (unchanged)** | **Deliberately overridden** — treated as a fixed process tolerance, §9.1 |
| Plug wall | 4.0 | 2.55 | **2.4mm** | Re-derived from this build's own nominal wall, not Large's absolute figure — §9.2 |

The neck ID override is the important one, and it cascades: because 70mm is well above the 51mm a
naive scale would give, the shoulder and base radii below it also have to be widened past their own
naive-scaled values to preserve a physically valid, monotonically-tapering silhouette (a wider neck
than a naive-scaled shoulder would allow is a geometric contradiction, the same class of problem
Large's own v4→v5 transition had to correct for). This is worked through explicitly in §7.4.

---

## 6. Neck opening size — fresh competitor research for the small-pet tier (not a scaled-down 80mm)

**This is the single highest-risk decision in this spec**, exactly as the equivalent decision was on
Large. Per the task, this was not proportionally shrunk from Large's 80mm — real research was done
specifically at the small-pet tier.

### 6.1 What was searched, and the honest state of the public data

Multiple targeted searches were run for: small-pet (≤22–35 lb) ceramic and 3D-printed urn opening/
neck/mouth diameters, UK and US retailers' weight-tier size guides, and the specific competitor
weight-tier boundaries named in the task (small ≤22 lb / medium ≈44–55 lb / large ≤132 lb). That
exact tier pattern was independently corroborated by a UK retailer (`dog-urns.co.uk`): **"Small: up
to 10kg (22 lbs); Medium: up to 20kg (44 lbs); Large: over 20kg."** — confirming the task's reference
tier boundary is a real, commonly-used industry convention, not an invented number. **However, no
retailer's public page (ceramic or 3D-printed) states an actual opening/neck diameter figure for
their small tier** — capacity is near-universally given in cubic inches or litres by weight, and
opening diameter is essentially never published as a spec, for any tier, at any retailer checked.
This mirrors what Large's own research found (their 114–121mm/70–100mm figures were the *closest*
available proxies, not a clean tier-matched spec sheet either) — the data quality problem here is
the same in kind, if anything slightly worse, since small-pet openings get even less attention in
product copy than large-pet ones.

### 6.2 Real data points found, and why they're not directly usable as-is

| Source | Product / tier | Opening figure found | Why it's not a direct answer |
|---|---|---|---|
| Amazon listing, "Reminded" brand | Small metal keepsake/scatter urn, **up to 35 lb** | **Lid opening 2-5/8" = 66.7mm** (base dia. 2-3/8" = 60.3mm) | This is a narrow-mouth **keepsake/scatter-style** urn (screw-top, meant for pouring/scooping ash), not a wide-mouth vase-style urn meant to receive a whole sealed bag — a materially different opening use-case from what this project builds |
| Etsy listing | Small pet urn, **up to 25 lb** | **Bottom opening 2.5" = 63.5mm**, threaded closure | Same category problem — a narrow threaded bottom-fill closure, not a bag-insertion opening |
| Industry buying-guide commentary (PetDecorArt cat-urn size guide, and others) | General, all small-tier urns | No number given, but explicit qualitative warning: *"very small urns may have narrow openings that make a sealed bag difficult to place... choose a small urn with a wider opening"*; the guide's own fit-check question is *"can the sealed bag pass through without folding, squeezing, or tearing?"* | This is the most load-bearing finding of this research pass — **it tells us the 60–67mm range represented by the two real data points above is itself a documented, named pain point in this exact weight bracket (25–35 lb)**, not a safe target to replicate |

### 6.3 What this means for the actual number chosen

The two real, sourced small-tier opening figures found (63.5mm, 66.7mm) sit in a range that
industry guidance for this *same* weight bracket explicitly flags as often "too narrow" for a real
sealed remains bag. A naive linear (cube-root-volume) scale of Large's 80mm gives ≈51mm (§5.2) —
*below* even that flagged-problematic range, which would make the naive-scale answer clearly worse,
not just unverified. This is a genuinely useful negative result: it confirms, independently of
Large's own reasoning about not shrinking the neck proportionally, that a proportionally-scaled
opening would land in a size class real crematorium-bag users report problems with.

**Chosen neck/collar ID: 70mm.** Reasoning, not just a number:
- Comfortably above the 60–67mm range flagged as a real-world pain point at this same weight
  bracket (a ≈3–10mm margin over the two sourced data points, not a token increase).
- Meaningfully below Large's 80mm (a 90 lb pet's remains bag is reasonably assumed to be somewhat
  bulkier than a 25 lb pet's, even though — per the reasoning above — the relationship is clearly
  *not* linear with weight; bags don't shrink in proportion to ash mass, since bag material/folding
  convention imposes a practical minimum bulk regardless of how little ash is inside).
- Lands close to the **low end of the 70–100mm range** Large's own research found for a direct
  3D-printed *large*-pet competitor — used here only as a soft outside anchor (not a small-pet
  citation), on the reasoning that a folded/bunched remains bag has a real practical minimum
  clearance need that doesn't scale down purely with pet weight the way ash *volume* does.

**This is `ESTIMATED`, not `VERIFIED`** — it is a reasoned, research-informed compromise, not a
number pulled from a small-pet-tier spec sheet (none was found to exist publicly). This is named
explicitly as a risk in §14 and as edge case 2 (§13), exactly as Large's 80mm figure was. **The
`neck-fit-test-small` article (§3) is what actually closes this out** — print it and test a real (or
mocked) small-pet remains bag before committing to the full body print.

### 6.4 Neck OD and collar OD, derived from the chosen ID

| Parameter | Value | Tag |
|---|---|---|
| Neck ID (constant through collar) | **70mm** (r=35mm) | ESTIMATED — competitor-research-informed compromise, §6.3 |
| Neck OD (at P3, below collar) | **74.8mm** (r=37.4mm) | DERIVED — 70mm ID + 2×2.4mm nominal wall (§7.1) |
| Collar ID | **70mm** | Matches neck ID, same convention as Large |
| Collar OD | **82mm** (r=41mm) | DERIVED — 70mm ID + 2×6mm reinforcement wall (§7.3) |
| Collar wall thickness | **6mm** | ESTIMATED — independently re-derived for this scale, §7.3 |
| Collar height | **9mm** | ESTIMATED — kept close to the naive linear scale (naive: 9.57mm) since no competitor/functional reason was found to deviate from it, unlike the neck ID itself |

### 6.5 `neck-fit-test-small` article — geometry target

A standalone print of just the neck-taper (P2→P3) + collar (P3→P4) section of the body, plus a
stabilizing flange at the bottom (the same construction Large used): flange OD ≈100mm × 5mm tall,
rising through the 12.4mm neck taper to the 9mm collar band, open bore both ends throughout (70mm ID
constant through the collar, narrowing internally toward the shoulder below the taper — see §7.5 for
the exact internal radii it should reproduce). Total article height ≈26.4mm. Print flange-down, same
self-supporting logic as the full body (§11.1). **This must be built to this spec's 70mm ID / 74.8mm
neck OD / 82mm collar OD — do not reuse or adapt Large's neck-fit-test geometry, which is a
completely different, much larger part.**

---

## 7. Wall thickness, floor thickness, and collar reinforcement — re-derived, not scaled

### 7.1 Nominal body wall — why 2.4mm, not a shrunk copy of Large's 4mm

Large's 4mm nominal wall was explicitly an aesthetic/heft convention (5× the 0.8mm print floor), not
a print-minimum — chosen so the part "doesn't feel like plastic" on a vessel with a 98–154mm
diameter range. The task is right to flag this as needing fresh reasoning at Small's scale, and the
reason is a real, quantifiable one, not just a vague sense that thick walls "look wrong" on a small
part:

**Surface-area-to-volume ratio grows as an object shrinks (a basic consequence of the square-cube
relationship), so a fixed absolute wall thickness consumes a growing fraction of a shrinking internal
volume budget.** This isn't a qualitative hand-wave — it's directly computable for this design:

```
Approx. internal lateral surface area of the Small body (avg internal radius ≈40mm,
avg internal height ≈73mm): A ≈ 2π × 40 × 73 ≈ 18,347 mm²

Volume "cost" of using Large's 4mm wall instead of a thinner one, holding external
dimensions fixed, ≈ A × Δwall:
  Δwall = 4.0mm − 2.4mm = 1.6mm
  Volume cost ≈ 18,347 mm² × 1.6mm ≈ 29,355 mm³ ≈ 29.4 cm³

29.4 cm³ ÷ 409.7 cm³ target ≈ 7.2% of the ENTIRE internal volume budget
```

A 7.2% hit to a tight 409.7 cm³ target is a materially different cost than the equivalent 1.6mm of
wall would have imposed on Large's 1579 cm³ cavity (a much smaller percentage there, because the
cavity is nearly 4× bigger for the same absolute wall-thickness delta) — this is the concrete,
worked version of "walls become disproportionately expensive at small scale," not an assumption.

**Chosen nominal wall: 2.4mm** — exactly 3× the 0.8mm print floor (comfortable margin, never close to
the minimum), and close to (not identical to) the 2.55mm a naive linear scale of Large's convention
would give — the naive-scale figure is used here as a corroborating sanity check, not as the
justification itself; the justification is the volume-budget argument above. `ESTIMATED` — a design
convention, reasoned through rather than defaulted to.

### 7.2 Floor (base) thickness — 3.0mm

Large used 5mm (1.25× its own 4mm nominal wall) for base stability under the settled weight of a
bagged-remains payload over years on a shelf. Preserving the **same 1.25× ratio** against this
build's own 2.4mm nominal wall gives exactly 3.0mm (2.4 × 1.25 = 3.0) — chosen for consistency of
design language (the floor-to-wall ratio, not the absolute floor value, is what's being carried
forward) and independently close to the naive linear scale (3.19mm). `ESTIMATED`.

### 7.3 Collar reinforcement wall — 6.0mm, not a shrunk-or-kept copy of Large's 10mm

Large's 10mm collar wall (2.5× its 4mm nominal wall) was an explicit, deliberate choice to keep a
non-nominal reinforcement band for structural margin and rim character (no longer for magnet
housing, since v3) — the task is right to ask whether that absolute figure, or some other figure,
is appropriate here, rather than assuming either "keep 10mm" or "just scale it."

**Two rejected alternatives, worked through rather than skipped:**
- **Keep Large's absolute 10mm unchanged:** on this build's 70mm ID (r=35mm), a 10mm wall would push
  the collar OD to 90mm — equal to or exceeding several of this body's own upper-profile dimensions
  (§7.4) and would visually read as a disproportionately heavy band relative to the rest of a much
  smaller vessel; it would also cost real volume budget for the same square-cube reason as §7.1.
- **Use the bare nominal wall (2.4mm), no extra reinforcement:** this would remove the intentional
  "banded collar" rim-reinforcement identity entirely, making the collar read as a plain continuation
  of the neck wall rather than a distinct seating/reinforcement detail — inconsistent with the
  identity carried forward from Large (§1).

**Chosen: 6.0mm** — preserves Large's own **2.5× multiplier over its own nominal wall** exactly
(6.0 ÷ 2.4 = 2.5, matching 10 ÷ 4 = 2.5 precisely) — the design-language element being carried
forward is the *multiplier*, not the absolute millimeter value, which is the correct level of
abstraction for "same design, different scale." Independently close to the naive linear scale
(6.38mm) as a corroborating check, not the primary justification. `ESTIMATED`.

Both the 1.25× floor-to-wall ratio and the 2.5× collar-to-wall ratio landing exactly on Large's own
multipliers, while the naive linear scale also independently corroborates all three absolute values
within a few tenths of a millimeter, is a reassuring convergence — not a coincidence being leaned on
as proof, but worth naming, same as Large's own practice of naming this kind of corroboration.

### 7.4 Base, belly, and shoulder radii — the neck-ID override cascades upward

Because the chosen neck ID (70mm, §6) is well above what a naive linear scale of Large's design
would put at this body size, the external neck OD (74.8mm) ends up **wider than a naive-scaled
shoulder** would be (naive shoulder OD ≈59.2mm) — a direct geometric contradiction (the profile is
supposed to taper *inward* from shoulder to neck, not flare outward). This is the same class of
problem Large itself found and corrected between v4 and v5 (§4.2.2 of Large's spec, the
geometrically-impossible 57mm-internal-vs-46.42mm-external figure). Rather than patch it after the
fact, it's addressed directly here: the shoulder (and, to preserve the vessel's visual hierarchy, the
base) are deliberately widened past their naive-scaled values, not linearly scaled.

**Base-vs-collar-vs-shoulder hierarchy, re-checked at this build's own dimensions (per the task's
explicit requirement to re-check this, not assume it):**

| Check | Values | Result |
|---|---|---|
| Collar OD (82mm) vs. base OD | Base chosen at **90mm** (r=45mm) | Collar (82mm) does **not** exceed base (90mm) — hierarchy preserved, same check Large ran at its own scale |
| Base OD (90mm) vs. shoulder OD | Shoulder chosen at **88mm** (r=44mm) | Base is barely wider than shoulder (90 > 88, a 2mm/1mm-radius margin) — mirrors Large's own base(98mm)-vs-shoulder(92.84mm) relationship in kind, not magnitude |
| Belly OD (widest point) vs. everything else | Belly = **98mm** (r=49mm) | Belly is unambiguously the widest point (98mm > 90mm base > 88mm shoulder > 82mm collar > 74.8mm neck-OD-at-P3) — visual hierarchy is not inverted anywhere in the profile |

Base was deliberately raised from a naive-scaled ≈62.5mm to **90mm** specifically to satisfy the
collar/shoulder checks above — this is not an incidental rounding choice, it is a direct,
necessary consequence of the neck-ID decision in §6, worked through explicitly rather than left for
the Coder to notice (or not notice) during modeling. Belly OD (98mm) was kept close to its naive
scale (98.18mm) since it already comfortably cleared every other radius without adjustment. All
radii in this table are `DERIVED — sizing decision` (chosen to satisfy both the volume target, §5.1,
and the hierarchy constraint above), except the neck ID itself (`ESTIMATED`, §6).

### 7.5 Full body profile — control points, tangent conditions, and volume hand-calc

Construction: one fit-point spline through P0–P4 with the tangent constraints below, revolved 360°,
same method as Large — internal and external walls each their own spline, offset by wall thickness
at each height (2.4mm nominal, 6.0mm through the collar band, §7.1/§7.3). `Z_ext` measured from the
true external base (0mm); `Z_int` measured from the internal floor's top surface (0mm = 3.0mm up
from the external base, per the 3.0mm floor thickness, §7.2).

| Point | Z_int (mm) | Z_ext (mm) | % of 75.7mm total height | Internal r (mm) | External r (mm) | Tangent condition |
|---|---|---|---|---|---|---|
| P0 — floor/base | 0 | 3.0 | 4.0% | 42.6 | 45.0 | **Horizontal** (dr/dz = 0) — smooth rounded foot, same as Large, replacing a separate fillet callout |
| P1 — belly max (broad plateau) | 30.5 | 33.5 | 44.3% | 46.6 | 49.0 | Broad, nearly-flat plateau, not a sharp point — matches the ~45% concept proportion, same identity as Large |
| P2 — shoulder (inflection) | 51.3 | 54.3 | 71.7% | 41.6 | 44.0 | Tangent-continuous, spline-default; Coder should confirm no curvature reversal/cusp before revolving |
| P3 — neck-taper-end / base of collar | 63.7 | 66.7 | 88.1% | 35.0 | 37.4 | **dr/dz → 0** — must flatten to meet the constant-radius collar band above it |
| P4 — rim / top of collar | 72.7 | 75.7 | 100% | 35.0 | 41.0 | Constant radius P3→P4 internally (true cylinder, 70mm ID bore); externally, a short tangent-blend rises from 37.4mm to 41.0mm within this same span — see §11.1 for the blend geometry and its overhang angle |

**Volume hand-calc (frustum/straight-chord approximation, same method Large used throughout — not
the literal volume of the true tangent-constrained spline, which will bulge slightly outward near
the belly apex and pull slightly inward near the shoulder-to-neck "waist," the same two
partially-offsetting effects Large's own hand-calcs always named and never tried to hand-compute
precisely):**

`V = (π·h/3)(r1² + r1·r2 + r2²)` for each internal segment:

| Segment | Internal r1 → r2 | Height | Volume |
|---|---|---|---|
| 1. Floor (P0) → belly (P1) | 42.6mm → 46.6mm | 30.5mm | 190.73 cm³ |
| 2. Belly (P1) → shoulder (P2) | 46.6mm → 41.6mm | 20.8mm | 127.22 cm³ |
| 3a. Shoulder (P2) → neck-taper-end (P3) | 41.6mm → 35.0mm | 12.4mm | 57.29 cm³ |
| 3b. Collar bore, straight cylinder (P3→P4) | 35.0mm (constant) | 9.0mm | 34.64 cm³ |
| **Total internal volume** | | **72.7mm internal height** | **≈409.87 cm³** |

```
Check: 190.73 + 127.22 + 57.29 + 34.64 = 409.87 cm³ (409,866 mm³)
vs. 409.6775 cm³ target -> +0.046% -- essentially exact, well inside the +/-5% band (S5.1)
Sanity check on heights: 30.5 + 20.8 + 12.4 + 9.0 = 72.7mm internal; + 3.0mm floor = 75.7mm external
```

**Same caveat Large always named, restated here:** this is a straight-chord approximation, not the
true spline volume. **The Coder must verify the real modeled internal volume via CAD mass-properties
once the spline-revolved geometry exists, and flag back for a spec revision if it falls outside the
389.19–430.16 cm³ band (§5.1) by more than the routine ±5%.** Given the hand-calc already lands
within 0.05% of target, there is very little headroom before a real spline-vs-chord deviation would
matter — plausible, not a failure if it happens, exactly Large's own framing.

### 7.6 Body external dimensions summary

| Parameter | Value | Tag |
|---|---|---|
| Overall external height (base to top of collar rim) | **75.7mm** | DERIVED — sizing decision (§7.5) |
| External base OD | **90mm** (r=45mm) | DERIVED — sizing decision, deliberately raised above naive scale to preserve hierarchy (§7.4) |
| External belly max OD (at P1, Z_ext≈33.5mm, ~44.3% of height) | **98mm** (r=49mm) | DERIVED — sizing decision, close to naive scale (§7.4) |
| External shoulder OD (at P2, Z_ext=54.3mm) | **88mm** (r=44mm) | DERIVED — sizing decision, deliberately raised above naive scale (§7.4) |
| External neck OD (at P3, Z_ext=66.7mm, below the collar) | **74.8mm** (r=37.4mm) | DERIVED — 70mm neck ID + 2×2.4mm nominal wall (§6.4) |
| Internal neck/collar ID (constant through collar) | **70mm** (r=35mm) | ESTIMATED — competitor-research-informed, §6 |
| Collar OD (at P4, top of collar/rim) | **82mm** (r=41mm) | DERIVED — 70mm ID + 2×6mm reinforcement wall (§6.4, §7.3) |
| Nominal side wall (body) | **2.4mm** | ESTIMATED — reasoned, §7.1 |
| Floor thickness | **3.0mm** | ESTIMATED — reasoned, §7.2 |
| Collar wall thickness | **6.0mm** | ESTIMATED — reasoned, §7.3 |
| Internal cavity volume (hand-calc) | **≈409.87 cm³** | Hand-calc, verify against real CAD once built (§7.5) |
| External volume (hand-calc) | **≈480.63 cm³** | Hand-calc |
| Material (shell) volume (hand-calc) | **≈70.76 cm³** (480.63 − 409.87) | Hand-calc — used for the cost estimate, §12 |

---

## 8. Lid derivation

### 8.1 Brim — flush with the collar, same identity, own numbers

Per §1, brim OD must be flush (zero overhang) with the collar OD. Large's final brim carried a
deliberate **−0.3mm allowance below the nominal collar OD** (99.700mm brim vs. 100mm collar) as a
hedge against FDM's tendency to print external rims slightly oversized. That allowance is a function
of the printer/material's dimensional repeatability — an absolute process tolerance, not something
that should shrink just because the part is smaller (same reasoning applied to the plug clearance,
§9.1). **Kept unchanged in absolute terms: −0.3mm.**

| Parameter | Value | Tag |
|---|---|---|
| Collar OD (nominal, from body) | 82mm (r=41mm) | DERIVED (§6.4) |
| Brim OD | **81.7mm** (82mm − 0.3mm) | DERIVED — flush-fit identity + fixed process allowance |
| Brim thickness | **6.0mm** | ESTIMATED — close to the naive linear scale of Large's 10mm (6.38mm); needs to be thick enough to form a real ceiling over the plug's hollow section (§9.3) and to read as a deliberate disc, not scaled down further without a specific reason to |

**Named risk, carried forward unchanged from Large:** a brim printed to nominal against a collar
printed to nominal has essentially zero print-tolerance margin to absorb ordinary dimensional
variance. Per this project's own documented FDM tendency (external rims print slightly oversized
more often than undersized), the more likely failure mode on a first print is a lid brim reading
very slightly proud of the collar edge, not a gap. Not a functional problem (the seating interface
itself is unaffected) — named as edge case 3 (§13).

### 8.2 Dome — base OD, height, re-derived by ratio, not scaled

Per §1, dome base OD follows the same ~0.80 dome-to-brim ratio Large used, applied to **this
build's own** brim value (81.7mm), not Large's absolute figure:

```
Dome base OD = 0.80 x 81.7mm = 65.36mm, rounded to 65.4mm (r=32.7mm)
```

**Dome height**, derived the same way Large derived its own (not a linear scale of Large's 29mm):
preserving Large's own dome-base-radius-to-target-apex-height ratio (a=40mm, h=30mm point-apex
target → a/h=1.333) against this build's own dome base radius (32.7mm):

```
Target point-apex height h = 32.7mm / 1.333 = 24.53mm, rounded to 24.5mm
Sphere radius R = (a^2 + h^2) / (2h) = (32.7^2 + 24.5^2) / (2 x 24.5) = 1669.5 / 49 = 34.07mm
```

### 8.3 Dome apex — flattened plateau, checked for print-size viability

Per the task, the ~27% plateau-to-dome-base ratio Large's build actually landed on (21.73mm ÷ 80mm =
27.16%) is preserved as a starting point, then checked that the resulting absolute size is still
comfortably printable at this smaller scale — not assumed to still be fine just because the ratio
carries over:

```
Plateau diameter = 0.2716 x 65.4mm = 17.77mm, rounded to 17.8mm (r=8.9mm)
```

**Checked, not assumed: 17.8mm is comfortably above any print-quality-limiting flat-feature size** —
it is more than 20× the 0.8mm wall/boss floor, and well clear of the "few-millimeter" range where a
flat terminal disc would become a real print-quality concern (excessive top-layer bridging over too
small an area, or an apex too small to read as an intentional flat spot rather than a rounding
artifact). No adjustment to the ratio is needed at this size. `ESTIMATED`.

**Blend consumption, computed the same way Large's was, not assumed to be the same ~1mm:** solving
for the height at which the natural (unblended) spherical-cap curve reaches r=8.9mm:

```
z = h - R + sqrt(R^2 - r_plateau^2) = 24.5 - 34.07 + sqrt(34.07^2 - 8.9^2)
  = 24.5 - 34.07 + sqrt(1160.76 - 79.21) = 24.5 - 34.07 + 32.89 = 23.32mm
```

The natural curve reaches the plateau radius at z≈23.3mm with a non-zero local slope (≈15° from
horizontal — a close independent match to Large's own ≈15.3° finding, a reassuring cross-check that
the ratio-preservation method is internally consistent) — left unblended this would show a visible
kink; a short tangent-matched blend absorbs it over the last ~1.2mm of height, same mechanism Large
used. **Final dome height: ≈23.3mm** (down from the 24.5mm point-apex target — an expected,
immaterial consequence of the blend, same as Large's own ~1mm reduction).

### 8.4 Lid summary table

| Parameter | Value | Tag |
|---|---|---|
| Brim OD | **81.7mm** | DERIVED — flush-fit + fixed allowance, §8.1 |
| Brim thickness | **6.0mm** | ESTIMATED, §8.1 |
| Dome base OD | **65.4mm** (r=32.7mm) | ESTIMATED — 0.80 ratio applied to this build's own brim, §8.2 |
| Dome height above brim top | **≈23.3mm** | ESTIMATED, §8.3 |
| Dome apex — flattened plateau diameter | **≈17.8mm** (r=8.9mm) | ESTIMATED — ratio-preserved and print-size-checked, §8.3 |
| Total lid height (seating plane to plateau top) | **≈29.3mm** (6.0 + 23.3) | DERIVED |
| Total lid bounding-box height (plug tip to plateau top) | **≈35.3mm** (29.3 + 6.0mm plug, §9.3) | DERIVED |
| Lid material volume (hand-calc: brim disc + solid dome cap + plug) | **≈87.6 cm³** | Hand-calc, §12 |

---

## 9. Alignment plug — clearance and wall convention re-derived, not scaled

### 9.1 Diametral clearance — kept at 0.5mm, treated as a process floor, not a part-size ratio

Large used a 0.5mm diametral clearance (0.25mm/side) on a 79.5mm-OD plug into an 80mm-ID bore. The
task rightly asks whether that figure should shrink for a smaller plug, or whether it reflects a
practical minimum tied to the printer/material combination rather than the part's own diameter.

**Reasoning: FDM dimensional repeatability (extrusion width consistency, first-layer squish,
PLA/PETG shrinkage behavior) is governed by the printer and material, not by the diameter of the
feature being printed** — within the range of feature sizes this project deals with (tens to
hundreds of mm), a clearance-fit tolerance like this is closer to a fixed process capability floor
than a dimension that should scale with part size. A naive linear scale would suggest ≈0.32mm
(§5.2) — but shrinking the clearance that far risks landing below what this printer/material
combination can actually resolve reliably, especially given the same cross-material risk Large
named (a PETG lid plug fitting into a PLA body bore — different shrinkage behavior between the two
materials in either direction). The design intent ("secure but not press-fit-tight") does not become
a tighter requirement just because the part is smaller.

**Chosen: 0.5mm diametral clearance, unchanged from Large.** `ESTIMATED`. Same recommended
mitigation as Large: print a small stand-alone clearance-test coupon at the plug's nominal
dimensions and check the fit against `neck-fit-test-small` before committing to the full lid print.

### 9.2 Plug wall — matched to this build's own nominal wall, not Large's absolute 4mm

Large's 4.0mm plug wall was itself just "match the body's nominal wall convention" (Large's nominal
wall was 4mm) — it was never an independently-justified plug-specific figure. The correct thing to
carry forward is that *convention* ("plug wall = this build's own nominal body wall"), not Large's
now-superseded absolute number. This build's nominal wall is 2.4mm (§7.1), so:

**Chosen plug wall: 2.4mm** — comfortably 3× the 0.8mm floor, consistent with every other nominal
wall in this design. `ESTIMATED`. Checked against the alternative of keeping 4mm unchanged: on a
much smaller 69.5mm-OD plug (below), a 4.0mm wall would consume proportionally more of the plug's
own interior area than it does on Large's 79.5mm plug (4mm/79.5mm=5.03% of OD vs. a hypothetical
4mm/69.5mm=5.76% of OD) — not dramatically worse, but consistent with the same square-cube reasoning
used throughout §7, and there's no functional reason (the plug carries no structural load beyond
gravity/light friction) to deviate from this build's own established nominal-wall convention.

### 9.3 Plug geometry — OD, depth, cap

```
Plug OD = neck ID - clearance = 70.0mm - 0.5mm = 69.5mm (r=34.75mm)
Plug interior ID = plug OD - 2 x wall = 69.5mm - 2x2.4mm = 64.7mm
```

**Depth and collision margin.** The body's constant-ID bore zone (P3→P4) is 9.0mm tall (§7.5). Large
used a plug depth that consumed two-thirds of its own 15mm constant-bore zone, leaving a 5.0mm
(33%) margin above the internal taper. Preserving that same **33% margin fraction** (not the
absolute 5mm) against this build's own 9.0mm bore zone:

```
Plug depth = 9.0mm x (1 - 0.33) = 6.0mm; margin = 9.0 - 6.0 = 3.0mm (33%)
```

**Cap split**, preserving Large's own hollow-to-solid depth ratio (6mm hollow : 4mm solid = 60:40 of
a 10mm total) against this build's 6.0mm total depth:

```
Hollow section (nearest brim): 0.60 x 6.0mm = 3.6mm, rounded to 3.5mm
Solid cap (nearest tip):       0.40 x 6.0mm = 2.4mm, rounded to 2.5mm  (sum = 6.0mm)
```

| Parameter | Value | Tag |
|---|---|---|
| Plug OD | **69.5mm** (r=34.75mm) | DERIVED — 70mm ID − 0.5mm clearance (§9.1) |
| Plug wall | **2.4mm** | ESTIMATED — matches this build's own nominal wall (§9.2) |
| Plug interior ID | **64.7mm** | DERIVED |
| Plug total depth | **6.0mm** | ESTIMATED — same 33% bore-zone-margin fraction as Large, §9.3 |
| Collision margin above P3 (internal taper start) | **3.0mm** | Checked, §9.3 |
| Hollow section (nearest brim) | **3.5mm** | ESTIMATED — same 60:40 split as Large |
| Solid tip cap | **2.5mm** (3.125× the 0.8mm floor) | ESTIMATED |

**Same "does capping eliminate the bridge" analysis as Large applies here unchanged in kind:**
capping the tip does not remove the ceiling bridge where the hollow section meets the solid brim
above it (same mechanism, same reason it doesn't matter — sealed, never visible); the tip cap itself
introduces no new risk specifically because of print orientation (§11.2) — it is the literal first
printed layer(s), bed-supported. **Confirm supports are set to "touching build plate only" before
slicing the lid** — same recommendation as Large, for the same reason (a sealed void with no access
path could otherwise generate unremovable interior support under a permissive setting).

---

## 10. Material recommendation

Carried forward unchanged from Large (§1) — not re-derived, per the task framing:

- **Body: matte or silk PLA.** Diffuses surface reflection closer to a stoneware finish than glossy
  PLA — same reasoning as Large.
- **Lid: PETG.** Kept for general toughness on the lid's thin-fillet transitions (brim-to-dome
  fillet, dome-to-plateau fillet, plug wall) and to avoid introducing a new material-behavior
  variable — same carried-forward default Large uses, including Large's own honest caveat that this
  reasoning is a default, not a fresh per-build derivation.
- **Named risk, same as Large:** PLA (including matte/silk variants) can soften/warp under sustained
  heat/UV exposure — accepted here for the same finish-requirement reason as Large; see edge case 3
  (§13) for how this interacts with this build's thinner wall specifically.
- **Finish-mismatch risk**, same as Large: PETG's default sheen is glossier than matte/silk PLA's — a
  sanding pass on both parts, applied more aggressively to the lid, is the same planned mitigation.

---

## 11. Print orientation — re-checked from scratch at this build's own geometry

### 11.1 Body: base down, opening/neck facing up

Matches the natural resting stance, same as Large — but the overhang angles below are freshly
computed from this build's own radii and heights (§7.5, §7.6), not assumed to match Large's figures.

| Transition | Height span | Δr (external) | Angle from vertical | Class | Risk |
|---|---|---|---|---|---|
| Base → belly (P0→P1) | 3.0–33.5mm | Grows 45.0mm→49.0mm | Shallow flare throughout | Radius non-decreasing by construction (same spline method) — flag for Coder confirmation once built, same convention as Large | None — self-supporting |
| Belly → shoulder (P1→P2) | 33.5–54.3mm | Shrinks 49.0mm→44.0mm (Δr=5.0mm over 20.8mm) | avg ≈13.5° | Shrinking-cone class | None — self-supporting regardless of local angle, same reasoning as Large |
| Shoulder → neck-taper-end (P2→P3) | 54.3–66.7mm | Shrinks 44.0mm→37.4mm (Δr=6.6mm over 12.4mm) | avg ≈28.1° | Shrinking-cone class | None — self-supporting |
| **Neck-to-collar external blend (P3→P4)** | 66.7–75.7mm | **Grows 37.4mm→41.0mm** (Δr=3.6mm) | **Peak ≈44.5°**, computed below | Radius grows with height — real overhang class, but a short span on a fully closed 360° revolve | Low — same disclosed "watch it on the first print" class as Large's equivalent zone |

**Neck-to-collar blend, computed freshly, not assumed to still be ~47° (task requirement):** for a
tangent-constrained cubic Bezier/Hermite blend with zero slope at both ends (a standard smoothstep,
`S(t)=3t²−2t³`), the peak local slope is a clean closed-form multiple of the average chord slope:
`peak dr/dz = 1.5 × (Δr/Δz)`. A blend span of **5.5mm** (out of the 9.0mm collar band, chosen
deliberately, see below) was picked specifically to land this build's peak angle in the same
low-risk band Large's own blend landed in, not left to chance:

```
avg slope = Δr/Δz = 3.6mm / 5.5mm = 0.6545  ->  avg angle = 33.2 deg
peak slope = 1.5 x 0.6545 = 0.982  ->  peak angle = atan(0.982) = 44.5 deg
```

44.5° sits just under the conventional 45° guideline — comparable to, marginally better than,
Large's own ~45.6–47.25° figure for this same class of feature. This is a **reasoned estimate from
the standard smoothstep-tangent formula, not a live CAD measurement** — flag for Coder/Tester
confirmation once the real geometry is built, same convention as every other angle figure in this
project. If the Coder's construction ends up using a different blend span than 5.5mm, the peak angle
will differ from this estimate and should be re-measured directly. The remaining 3.5mm of the
9.0mm collar band (75.7mm−5.5mm span down to 72.2mm) sits at a constant 41.0mm external radius —
the flat seating band proper.

**Base flat footprint (90mm OD) gives a stable bed-adhesion base**, proportionally similar to
Large's own base-to-height ratio.

### 11.2 Lid: flat underside down (plug-tip-down), dome facing up

Same reasoning as Large, re-checked rather than assumed to still apply at this build's own geometry:
this is the single flat plane established by the seating interface (§8.1), giving full continuous
bed contact and zero overhang on the primary seating surface. The alternate orientation (plateau-
down, now geometrically tempting with no handle and a flat plateau) was checked and rejected for the
same reasons Large found: flipping the dome would invert its self-supporting "shrinking radius as
height increases" class into a real expanding-cone overhang needing support under nearly the entire
visible dome exterior, and would turn the plug's tip cap (§9.3) from a bed-supported first layer into
an unsupported bridge over a sealed void. **Flat-underside-down remains correct.** The dome's radius
shrinks monotonically from the brim (32.7mm) to the plateau (8.9mm) over its full height in this
orientation — self-supporting throughout, same class as Large's dome.

`neck-fit-test-small` prints flange-down, same self-supporting logic as the body.

---

## 12. Cost estimate

Same method as Large (material volume × density × filament price/kg):

| Part | Material volume (hand-calc) | Density | Mass | Filament cost @ $20–25/kg |
|---|---|---|---|---|
| Body | ≈70.76 cm³ (§7.6) | PLA, 1.24 g/cm³ | ≈87.7g | ≈$1.75–2.19 |
| Lid | ≈87.6 cm³ (§8.4) | PETG, 1.27 g/cm³ | ≈111.3g | ≈$2.23–2.79 |
| **Combined pair** | | | **≈199g** | **≈$4.0–5.0** |

**Named, checked finding, not silently glossed over: the lid comes out heavier than the body.** This
looks counterintuitive at first (the body is the larger, primary vessel) but is fully explained by
construction: the body is a thin hollow shell (2.4mm wall over a 409.87 cm³ cavity → only 70.76 cm³
of material), while the lid's dome and brim are modeled as **solid** revolves (carrying forward
Large's own convention — Large's dome/brim were never hollowed either, only the plug was hollowed-
then-capped). A solid dome+brim at this scale (≈76.5 cm³ combined) plus the plug (≈11.25 cm³) outweighs
the thin-walled body's shell material. **Hollowing the dome/brim is a legitimate Coder-level
implementation option** to reduce material/print time, flagged here as an option rather than
mandated, the same way Large flagged the plug's solid-vs-hollow choice as a Coder-level decision —
no one has decided this needs to happen, but it's disclosed rather than silently left as a
surprising cost line item.

---

## 13. Edge cases

1. **Pet significantly below the 25 lb design target (e.g., a 5 lb cat).** This urn is intentionally
   sized to the top of the stated 0–25 lb range, a deliberate single-size decision, not a
   miscalibration — a 5 lb pet's remains will use noticeably less than the ≈409.87 cm³ built
   capacity. Expected and accepted, same reasoning as Large's equivalent edge case. A future,
   separate "keepsake" or "extra-small" tier is out of scope here.
2. **Remains bag proportionally larger relative to a smaller, narrower opening — the highest-risk
   edge case in this spec (§6, §14).** The chosen 70mm neck ID is a research-informed compromise,
   not a verified fit against a real small-pet remains bag. Real industry commentary found during
   this research explicitly flags narrower (60–67mm) openings as a documented pain point at this
   same weight bracket — this build's 70mm figure was chosen specifically to sit above that flagged
   range, but it remains `ESTIMATED`. The fix, if `neck-fit-test-small` reveals a real bag still
   doesn't clear comfortably, is widening the neck ID further in a future spec revision — not
   resizing the whole body.
3. **Thin, small-scale wall warping/shrinkage sensitivity.** At 2.4mm nominal wall and a much smaller
   overall footprint than Large, this body has shorter perimeter loops and faster per-layer print
   times than Large's much larger, thicker-walled body — both factors that can make small FDM parts
   *more*, not less, prone to localized warping/lifting at high-curvature transitions (belly
   plateau, shoulder) due to faster cooling and lower thermal mass per layer, and the thinner wall
   has less margin to absorb minor under-extrusion or layer-adhesion defects than Large's beefier
   4mm wall did. Not a blocker — but worth a slower first-layer speed and adequate cooling settle
   time, named explicitly rather than assumed to inherit Large's warping risk profile unchanged
   just because both use PLA.

---

## 14. What could not be verified — explicit list for the Director

Per this project's standing honesty convention, named plainly rather than buried:

1. **Neck/collar ID (70mm) — the single highest-risk figure in this spec (§6).** Backed by real,
   cited competitor/industry research (a UK retailer's tier boundaries matching the task's reference
   point exactly; two real small-tier opening figures of 63.5mm/66.7mm; explicit industry commentary
   flagging that range as a documented bag-fit problem at this same weight bracket) — but no
   small-pet-tier, wide-mouth, bag-insertion urn's opening spec was found publicly. `ESTIMATED`, not
   `VERIFIED`. Closing this out requires the physical `neck-fit-test-small` print against a real (or
   mocked) small-pet remains bag.
2. **Nominal wall (2.4mm), floor (3.0mm), and collar wall (6.0mm) — genuinely re-reasoned (§7.1–7.3),
   not naive-scaled, but still design conventions, not measurements.** All three are `ESTIMATED`.
   Cross-checked against a naive linear scale of Large's own values and against Large's own internal
   ratios (1.25× floor-to-wall, 2.5× collar-to-wall) for corroboration, but none of this is a
   substitute for a real print-quality check once built.
3. **Plug clearance (0.5mm, kept unchanged from Large) and plug wall (2.4mm, re-derived from this
   build's own nominal wall) — reasoned, not measured (§9.1–9.2).** The cross-material
   (PETG-plug-into-PLA-bore) shrinkage-mismatch risk Large named applies identically here; the same
   test-coupon mitigation is recommended before committing to the full lid print.
4. **All overhang angles (§11.1) are computed from a closed-form tangent-blend formula applied to
   this build's own chosen dimensions, not measured on real CAD** — flagged for Coder/Tester
   confirmation once the geometry exists, same as every angle figure in Large's own spec history.
5. **The hand-calculated cavity/material volumes (§7.5, §7.6, §8.4) are frustum/spherical-cap
   approximations, not the literal volume of the true spline/solid geometry** — must be verified via
   CAD mass-properties once built, flag back if outside the ±5% band (§5.1).

None of the above are treated as blockers to starting Coder work — they are exactly the kind of
disclosed, named risk this project's own conventions are built to carry forward rather than hide.
Items 1 and 3 carry the most real-world consequence if wrong (a bag that doesn't fit, or a friction
fit that binds or rattles) and are the two most worth a second look before committing to a full
print run.

---

## 15. Question back to the requester

**What slicer settings should be used (layer height, infill)?** No layer height or infill target has
been specified for this build, exactly as was the case for Large. Given this is a decorative,
low-mechanical-stress vessel with no handle or dedicated lift feature (the lid is lifted by gripping
the brim/dome edge, same as Large's current identity), a reasonable default absent other direction
would be **0.16–0.2mm layer height** (finer layers matter more here given the "doesn't feel like
plastic" finish bar, §10, and the lid's flat plateau top surface, §8.3) and **15–20% infill** (the
floor and walls carry only the modest static weight of a small bagged-remains payload — this isn't a
structural load case needing high infill). Please confirm or state a preference before the Coder
locks in export settings. **Also confirm the lid's support setting is "touching build plate only"
before slicing** (§9.3) — bundled into the same settings confirmation since both need to be locked
before export.

---

## 16. Revision history

**v1.1 (manual edit, 2026-09-09)** — the requester added a **5mm-radius fillet to the lid**
directly in Fusion, softening the sharp exterior edge where the flat brim top meets the rising
dome (a `FilletFeature` named `Fillet1`, `parentComponent=urn-lid`, confirmed via the feature's
own radius parameter and independently via the resulting torus geometry: majorRadius=35.85mm,
minorRadius=5.000mm exactly, at z=7.0mm — a different height/radius than the pre-existing 4mm
apex/plateau fillet, majorRadius=8.41mm at z=31.3mm, which is unrelated and untouched). Verified
clean before being recorded here, not assumed: single valid solid maintained (`isValid=True`,
`isSolid=True`), the plug (radius 34.75mm, z=0–6mm) sits at a different height/radius entirely and
is structurally unaffected, `neck-fit-test-small` and the body are both unaffected (the fillet's
`parentComponent` is `urn-lid` only), and the lid volume dropped by ≈1.34 cm³ (91.408 → 90.068
cm³), consistent with rounding a sizeable exterior edge. This is a purely cosmetic addition — no
mating/functional dimension changed. Also resolves an open question from this line's v7 identity
decision (carried forward at every size since): **the requester confirmed the lid is not designed
for repeated removal, so the absence of a handle/grip feature is intentionally fine** — recorded
here as the requester's own explicit rationale, not assumed.

**v1 (2026-09-09)** — initial spec for the Small size, produced by reading the Large build's
`dot_pipeline/specs.md`, `parameters.md`, `README.md`, and `concept/brief.md` in full (read-only) and
carrying forward the shared v7 design identity (§1) while independently re-deriving: the volume
target (§5.1, 409.6775 cm³ = 25 lb × 1 in³/lb), the neck/collar opening size via fresh small-pet-tier
competitor research (§6), the nominal wall/floor thickness (§7.1–7.2), the collar reinforcement wall
(§7.3), the base/belly/shoulder hierarchy cascade from the neck-ID decision (§7.4), the full body
profile and volume hand-calc (§7.5), the lid brim/dome/plateau derivation (§8), the alignment plug's
clearance and wall convention (§9), and the print-orientation overhang angles (§11). No prior
revision of this document exists — this is the first pass, produced as a single, complete spec
rather than an iterative accumulation, since (unlike Large) it did not go through an incremental
CAD-refinement history before being written down.

