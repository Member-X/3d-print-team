# Spec — Multi-Tube Hydroponic Propagation Stand (Dual-Channel Arc)

**New original design.** This is our shop's own take on the general concept of a "glass-tube
propagation stand" — an upright printed body that cradles a glass tube at a slant for rooting
cuttings in water. It is **not** a clone of any commercial product. A comparable single-tube
product (Etsy, "Circle Propagation Station" by RosebudHomeGoods) is referenced below purely as a
market/engineering comparison point — none of its dimensions are treated as verified facts about
our design, and our footprint is deliberately **not** sized to match it (see §3).

No CAD/mesh work has been done yet. This document is the spec only.

---

## 0. Source key (dimension provenance convention)

| Tag | Meaning |
|---|---|
| **VERIFIED** | Sourced from a manufacturer dimensional drawing, a physical measurement, or a ruler-photo of a real reference object. |
| **ESTIMATED** | A convention, calculation input, or best-guess design choice not independently confirmed against a real object. |
| **COMPUTED** | Arithmetic derived from other VERIFIED or ESTIMATED values, shown with the calculation. |

**Nothing in this spec is VERIFIED.** This is a from-scratch original design with no existing
model to measure and no physical tube sample in hand yet. Every dimension below is ESTIMATED or
COMPUTED-from-ESTIMATED. This is called out explicitly, repeatedly, rather than letting the volume
of tables below create a false impression of precision.

---

## 1. What this object is

A **2-tube** upright stand, printed as a single body, that holds two off-the-shelf glass test
tubes at a slant in individual blind (closed-bottom) bores, for rooting plant cuttings in water on
a windowsill/counter. (Originally speced at 3 tubes — see §2.1 and §11 for why the product owner
revised this down to 2.)

**Reference product for comparison only** (Etsy "Circle Propagation Station," 4.8★, 28,600+
sales): single tube, plain black half-circle/ring stand, ~173×140×64mm, holds one ~25mm dia ×
150mm / ~27mm OD tube, seller claims the slant + groove combination prevents spilling even filled
to the brim, sold in PLA at $16–21, seller-stated 8–10 hr print time. These numbers are reference
points for comparison and print-time targeting only — **not** inputs copied into our geometry.

---

## 2. Design decisions and rejected alternatives

### 2.1 Tube count: 2 (product owner decision — reverses this spec's original 3-tube recommendation)

**Final: 2 tubes.** This spec originally recommended 3 tubes (reasoning preserved below, since it
was a real recommendation, not an error); the product owner has since reviewed §§2–8 and decided
on 2 instead. The owner did not state a specific reason back to this spec, so the likely deciding
factors are inferred, not asserted as fact — flagged as inference below rather than overclaimed.

**Original 3-tube reasoning (superseded as the final count, kept for context):**
- The brief's core differentiator versus the single-tube reference is "multi-tube." Two tubes
  satisfies "multi" technically but was judged (in the original recommendation) to under-deliver
  on the differentiation opportunity versus three.
- The added cost of a third channel would have been incremental, not linear, since all channels
  share one base, one profile, and one slant-angle validation (§2.2).
- §5's stability analysis showed 3 tubes filled simultaneously still kept a comfortable margin —
  i.e. 3 tubes was never rejected on stability grounds, only superseded by the owner's own
  preference.

**Likely reasons for the owner's 2-tube decision (inferred, not confirmed by the owner):** a
narrower footprint (80mm vs. 115mm width, §4.5), a smaller, simpler total part, and/or a
preference for a tighter silhouette closer to the reference's single-tube scale. Note that the
recomputed print-time comparison (§6.3) does **not** clearly favor 2 tubes on a strict
per-tube-speed basis — per-tube time is actually slightly *higher* with 2 tubes than the original
3-tube design would have given, so if per-tube print speed was assumed to be the deciding factor,
that assumption doesn't hold up under the recomputed math. **These are this document's own
inference, not something the owner stated** — worth confirming directly if the actual reason
matters for future iterations (e.g. a 4-tube version).

- **Rejected (as of this revision): 3 tubes.** Was this spec's own original recommendation (see
  above) and remains a stability-safe, valid alternative — rejected here only because the product
  owner chose 2 instead, not because of any newly-discovered engineering flaw.
- **Rejected: 4+ tubes.** Widens the footprint and the tipping moment arm further for diminishing
  differentiation benefit, and starts to erode the print-time-per-tube advantage this design is
  built around (see §6). Not chosen, unchanged reasoning from the original spec.

### 2.2 Arrangement: 2 parallel co-planar channels, one shared slant angle

**Chosen:** two straight, parallel bores at the **same** slant angle, side by side across the
width of one shared arc-profile body (like the reference's single diagonal channel, widened to fit
two, side by side, rather than stacked or fanned).

**Rejected alternative — fanned/splayed channels** (each tube at a different compound angle,
radiating outward like a hand of cards): considered because it can look more visually dynamic and
lets tube mouths spread apart while bases stay close. Rejected because:
- It doubles the highest-risk geometry in the whole design (§4) — instead of validating one
  slant-angle/groove relationship, the Coder and Tester would need to validate two independent
  compound angles.
- It removes the single biggest print-time win available (§6.2): because both channels here
  share **one** slant angle, the *entire part* can be rigidly tilted once so both bores print
  with their axis vertical (no per-hole overhang, no supports). Fanned channels at different
  angles cannot all be made print-vertical by one whole-part tilt — at least one would still
  print as an overhanging hole, reintroducing the slow-support-heavy printing this design exists to
  avoid.

**Rejected alternative — tiered/stacked tubes** (one tube mounted higher than the others):
rejected because it raises the body's overall height and the payload's center of mass, working
against both the print-time goal (taller prints take longer even at the same volume) and the
stability goal (§5).

### 2.3 Silhouette: arc/wedge body, scaled down from the reference's proportions, not its size

Kept the reference's general concept (an upright arc-derived body with the tube seated in a bored
channel) since the brief does not require a new aesthetic theme. **Not** kept: the reference's
large, decorative ring/half-circle envelope. Our body is sized purely from the functional minimum
(tube geometry + bore embedment + a stability-driven base extension, see §5) rather than a
decorative disc — this is itself one of the two main print-time levers (§6), the other being
infill/orientation.

---

## 3. Printer / material constraints (stated up front)

| Constraint | Value | Source |
|---|---|---|
| Printer | P2S-class FDM | ESTIMATED — shop default (user's printer memory note) |
| Build volume | 256 × 256 × 256mm | ESTIMATED — shop default (user's printer memory note) |
| Nozzle diameter | 0.4mm (standard) | ESTIMATED — not confirmed this session, standard assumption |
| Minimum wall/boss thickness implied | ≥0.8mm (2× nozzle) for any wall or boss under load | COMPUTED |
| Material | PLA | ESTIMATED — shop default |

**Envelope fit:** overall design envelope (§4.5) is 80mm (W) × 80mm (D) × 91mm (H) — well inside
the 256×256×256mm volume on every axis (largest single axis uses ~36% of available travel).
COMPUTED. (Revised down from the original 3-tube spec's 115mm width — see §2.1/§4.5. Height
revised 85mm→91mm in v3 — see §4.5/§11.)

**Material reasoning (PLA):** this is a static, low-load decorative shelf/windowsill item. The
printed body itself never holds water directly (water is contained inside the glass tube, not the
printed plastic), so PLA's mild hygroscopic/humidity sensitivity is a low-severity concern here,
unlike a part that holds liquid directly. No repeated-flex or cyclic-load feature exists (compare
to switch-plate screw bosses or a ratchet pawl elsewhere in this shop's work, which do justify
PETG) — the tube is inserted once and left in place. PLA is the correct default, not a compromise.
ESTIMATED / project decision.

---

## 4. The tube, the channel, and the slant angle — highest-risk geometry, treated accordingly

### 4.1 Tube dimensions — ESTIMATED, flagged as the top risk in this spec

| Parameter | Value | Tag |
|---|---|---|
| Tube outer diameter (OD) | **27mm** | **ESTIMATED** |
| Tube inner/glass diameter | **~25mm** | **ESTIMATED** |
| Tube length | **150mm** | **ESTIMATED** |
| Tube shape | Round-bottomed (test-tube style), open top | ESTIMATED |
| Tube capacity | ~50mL | ESTIMATED |

**These four numbers come from the reference product's listing, used here only as a plausible
class of off-the-shelf glass tube — nobody on our side has this tube in hand to measure.** Per
explicit instruction, this is **not** silently upgraded to VERIFIED just because it's a common,
often-quoted size. This is the single highest-risk value in the entire spec, because the channel
bore diameter (§4.2) is a mating dimension directly against it: too large and the tube rattles and
sits at the wrong angle; too small and the tube won't seat at all.

**Required before the Coder finalizes the channel bore geometry:** verify the actual tube OD via
either (a) a manufacturer spec sheet for the tube actually being purchased, or (b) a caliper
measurement of a physical sample, or at minimum (c) a ruler-photo of a real tube next to a known
reference length. Do not cut the final bore diameter from the 27mm figure above without this
check.

### 4.2 Channel (bore) geometry, per tube position

| Parameter | Value | Tag |
|---|---|---|
| Bore shape | Straight cylindrical, **blind** (closed bottom), flat floor | ESTIMATED — design choice, see reasoning below |
| Bore diameter | **28.5mm** (27mm tube OD + 1.5mm total diametral clearance, 0.75mm per side) | COMPUTED from §4.1's ESTIMATED OD — **must be re-derived once §4.1 is verified** |
| Bore depth (along its own axis) | **70mm** | ESTIMATED |
| Embedded tube length (= bore depth, tube rests on the blind floor) | 70mm of the tube's 150mm length | COMPUTED |
| Protruding tube length above the bore opening | **~80mm** (150 − 70) | COMPUTED |
| Inter-channel land (solid wall between adjacent bores) | **6mm** | ESTIMATED — well above the 0.8mm (2×nozzle) minimum, sized for real mechanical margin around a load-bearing bore, not just the print-minimum |
| Channel center-to-center spacing | **34.5mm** (28.5mm bore + 6mm land) | COMPUTED |

With 2 channels (revised down from 3, §2.1), there is exactly **one** inter-channel land/gap
instead of two — the per-bore dimensions above (diameter, depth, land, spacing) are unchanged by
tube count; only how many times the spacing is repeated across the body's width changes (§4.5).

**Why a blind bore, not a shallow open groove/notch:** the reference's marketing language ("groove")
suggests a shallow cradle where only the tube's rounded tip rests against an angled surface. We
instead specify a deeper blind bore that embeds ~47% of the tube's length (70 of 150mm). This is a
deliberate choice with two direct payoffs, both explained fully where they matter:
1. **Security of fit** — a longer engagement length gives more contact area and a longer moment
   arm resisting the tube pivoting or working loose in its bore, versus a shallow notch that only
   contacts the tube at one point/edge.
2. **Stability** (§5) — because a large fraction of the tube (and its water) sits *inside* the
   body's own footprint rather than hanging entirely out over the front edge, the payload's center
   of mass stays much closer to the stand's own base than a shallow-cradle design would allow.

**Trade-off, named as an edge case, not hidden:** a closed-bottom bore can't be flushed through if
it ever gets wet inside (condensation, a tube leak) — see §7, edge case 3.

### 4.3 Slant angle — the core "won't spill" claim, reasoned explicitly

**Chosen: 30° from vertical (60° from horizontal).** ESTIMATED design choice, **not yet validated
by a physical print/fill test** — flagged as an open question in §8.

Reasoning for why 30° is a reasonable starting point, and what governs the choice:
- **Too steep (large angle from vertical)**: the tube's open mouth tilts far enough that the
  waterline at the top can approach or exceed the low side of the rim even at rest, and a small
  bump risks pouring water out the low side of the mouth immediately. This is the literal failure
  mode the reference claims to avoid.
- **Too shallow (small angle from vertical, near 0°)**: friction/normal-force retention in the
  bore drops, the tube tends to feel more "stood up" than "reclined" (less of the intended
  aesthetic and viewing-angle benefit of a slanted display), and there is less mechanical reason
  to prefer a blind bore over just standing the tube straight up in a plain cylindrical socket.
- 30° from vertical is a middle-ground value common to this general class of tilted-holder
  designs: steep enough to read visually as "reclined," shallow enough that the open mouth is
  still much closer to vertical than horizontal, so the risk of the waterline reaching the low
  rim edge at rest is low under normal (non-jostled) conditions.
- **This is explicitly presented as an engineering estimate, not a re-derivation of the
  reference's tuned angle.** The reference seller's specific claim ("won't spill even filled to
  the top") implies real empirical tuning of angle + groove geometry on their part. We have not
  reverse-engineered their exact angle (their bounding-box numbers don't cleanly resolve to a
  single angle without knowing their groove's exact position, which we don't have and aren't
  copying anyway). Our 30° is a first-pass estimate for our own, different geometry (deeper blind
  bore, different overall size) and should be confirmed with an actual filled-tube test on a first
  print — see §8, open question 3.

### 4.4 Geometric envelope driven by the bore

| Parameter | Value | Tag |
|---|---|---|
| Vertical reach of one bore (70mm bore × cos 30°) | **60.6mm** | COMPUTED |
| Horizontal reach of one bore (70mm bore × sin 30°) | **35.0mm** | COMPUTED |
| Body height needed above the bore floor (vertical reach + floor retention margin) | 60.6 + ~8mm margin ≈ **~69mm minimum** (original hand estimate) | COMPUTED + ESTIMATED margin |
| Body depth needed to keep the bore clear of front/back faces | 35.0 + ~15mm front margin + ~10mm back margin ≈ **~60mm minimum** (original hand estimate) | COMPUTED + ESTIMATED margin |

**v3 correction, from real CAD geometry (Coder finding, see §11):** the two estimates above treat
the bore as a zero-width centerline. The bore is actually a 28.5mm-diameter cylinder whose blind
floor cap and opening rim are themselves tilted disks, which extend **another ±7.1mm in height**
and **±12.3mm in the front/back direction** beyond what the centerline-only math above implies
(disk extension = bore radius × sin/cos 30°). Modeled in CAD with the exact 8mm base-foot minimum
honored at the floor, this left only **~2.1mm** of real clearance above the bore opening under the
original 85mm height (not the ~16mm of slack the naive 69mm-vs-85mm comparison above would
suggest), and required moving the channel opening position from the originally-estimated Y≈45mm to
**Y≈55mm from the back face** to keep the blind floor's disk from breaking out the back face
(the naive ~60mm-minimum-depth estimate above has the same centerline-only blind spot). Both
corrections are reflected in §4.5. This is flagged as **especially sensitive to the still-ESTIMATED
27mm tube OD (§4.1, open question 1, §8)** — a larger real tube OD would shrink these margins
further.

### 4.5 Overall body dimensions

| Parameter | Value | Tag |
|---|---|---|
| Overall width (X, spans both channels) | **80mm** = 1 × 34.5mm channel spacing + 2 × (bore radius 14.25mm + 6mm edge wall) = 75mm functional minimum, rounded up for margin | COMPUTED — **revised from the original 3-tube spec's 115mm**, since dropping to 2 channels removes one full channel-spacing repeat (§2.1) |
| Overall height (Z) | **91mm** (revised from 85mm in v3 — see §4.4 correction note and §11) | ESTIMATED — height is driven by the per-bore geometry (§4.4), not tube count; the +6mm over the original 85mm is deliberate buffer above the bore opening, added because CAD modeling found only ~2.1mm of real clearance there at 85mm, and no physical tube has verified the 27mm OD / bore-diameter assumption yet (§8) |
| Overall depth (Y) | **80mm — locked by product owner decision**, prioritizing the stability margin (§5) over a more compact silhouette; the ~65mm functional-minimum alternative discussed in the original spec is no longer an option under consideration (see §8) | ESTIMATED / product-owner decision |
| Base foot thickness (solid floor the whole body stands on) | **8mm** | ESTIMATED |
| Channel center positions (X, relative to body center) | **−17.25mm, +17.25mm** | COMPUTED — **revised from the original 3-tube spec's −34.5/0/+34.5mm** |
| Channel opening position (approx, within body) | **Y ≈ 55mm from back face** (revised from the original Y≈45mm estimate in v3 — see §4.4 correction note and §11), near top of body | ESTIMATED, corrected against real bore geometry |

**Fits build volume:** 80 × 80 × 91mm vs. 256 × 256 × 256mm — comfortable margin on every axis
(largest single axis ~36% of travel), even more so than the original 3-tube envelope. COMPUTED.

**Resulting vertical clearance above the bore opening at 91mm height:** ~8.1mm (up from ~2.1mm at
the original 85mm), with the 8mm base-foot minimum still fully honored below the blind floor.
COMPUTED, see §4.4/§11.

---

## 5. Stability analysis — does it tip with 2 filled tubes? (recomputed for the 91mm-height, v4)

This is worked through explicitly (center of mass vs. footprint), not asserted. **v4 fully
recomputes this section for the real 91mm height, and — per explicit instruction — anchors the
stand's mass to the Coder's actual measured CAD solid volume (407,120mm³ at 85mm) rather than
re-scaling this document's own earlier hand-guessed volume again.** The v2 method (guessing a
"solid-equivalent volume" from the envelope, then scaling it by a width ratio) is retired here,
not reused, for the reason in the callout below.

**Honesty-check, carried forward explicitly (per the same standard applied to the 2-vs-3-tube
print-time finding in §2.1/§6.3):** the Coder's real CAD solid volume for the 85mm-height body
(407,120mm³) came out roughly **2–2.3× higher** than this section's v2 hand-estimated
"solid-equivalent volume" (174,000–198,000mm³) for that same height. The v2 scaling method was a
guess extrapolated from an even earlier guess (the original 3-tube envelope estimate), never
checked against real geometry — it was significantly optimistic (i.e., under-estimated the
stand's real mass) once actual CAD existed. This is exactly the kind of thing this spec's own
provenance discipline exists to catch: flagged plainly rather than quietly folded in as if it were
always known.

**Mass estimate, stand — anchored to real CAD volume, scaled for the 91mm height:**
- Real CAD solid volume, 85mm height: **407,120mm³** (Coder measurement, VERIFIED-equivalent —
  this is a real geometry measurement, not a hand guess, even though the spec's own overall
  provenance convention still marks derived figures below as COMPUTED/ESTIMATED since they involve
  further assumptions).
- Scaled linearly to the 91mm height (91/85 = 1.0706), on the simplifying assumption that the
  added 6mm of height carries roughly the same average cross-sectional area as the rest of the
  body (an approximation — the real arc/wedge shape likely tapers somewhat near the top, so this
  is not exact, but it's a reasonable order-of-magnitude method and is explicit about its own
  assumption rather than silently precise):
  `407,120mm³ × (91/85) ≈ 435,860mm³` at 91mm. COMPUTED from a real measurement + an ESTIMATED
  scaling assumption.
- Effective printed mass at ~15% infill + shell walls: using the same ~35–45% effective-material
  fraction convention as before (midpoint 40%): `435,860mm³ × 0.40 ≈ 174,344mm³` effective volume
  → `174,344mm³ × 1.24×10⁻³ g/mm³ ≈ 216g`. **Call it ~216g** (range ~189–243g across the 35–45%
  fraction band). ESTIMATED/COMPUTED — markedly heavier than the v2 estimate (~87g), consistent
  with the honesty-check above.
- Stand's own center of mass (Y, front-back axis): the 85mm-height body's Y_com is assumed
  unchanged from the original ~30mm baseline (no real CAD centroid reading available for this
  session to check against — flagged as an assumption, not a measurement). The **added 6mm of
  height sits near the top of the body, in the reinforced ceiling directly above the bore opening**
  (now at Y≈55mm, §4.5) rather than spread over the full 0–80mm depth — so it pulls the stand's
  overall Y_com slightly forward. Working this through as an incremental-mass calculation (added
  mass ≈216g − 202g[the same-method estimate at 85mm] ≈ 14g, located at Y≈55mm):
  ```
  Y_com,stand(91mm) = (202g × 30mm + 14g × 55mm) / 216g
                    = (6,060 + 770) / 216
                    ≈ 31.6mm
  ```
  **Y_com,stand ≈ 31.6mm** (up slightly from the 30mm baseline). **Note on "raises the center of
  mass":** this ~1.6mm forward (Y) shift is what's used below because it's what matters for the
  static tip/no-tip criterion. The taller body also raises the stand's *vertical* (Z) center of
  mass, which does not enter the static-tipping formula below (that only depends on horizontal
  position within the footprint) — but a higher Z-CoM would make the stand modestly more sensitive
  to *dynamic* disturbances (a bump/knock), which is a real, if secondary, consideration worth a
  physical tip/nudge test alongside the flat tip-test already recommended (§8).

**Mass estimate, payload (2 tubes + water, worst case = both filled to the brim) — also corrected
for the Y≈55mm opening position:**
- Per-tube water + glass mass is unchanged: water ≈ 73.6g, glass ≈ 15g → **≈88.6g per tube**.
  Total for 2 tubes ≈ **177.2g**. COMPUTED, unchanged from v2/v3.
- Payload center of mass (Y): **this needs correcting, independent of the height change** — v2's
  figure of 47.5mm was computed against the *pre-v3* Y≈45mm opening position, which was itself
  superseded in v3 (§4.5) by the corrected Y≈55mm opening position. Re-deriving with the same
  method (tube midpoint ~5mm beyond the bore opening along the 30° axis ≈ 2.5mm forward offset):
  `Y_com,payload = 55mm + 2.5mm ≈ 57.5mm`. **Y_com,payload ≈ 57.5mm** (up from the stale 47.5mm
  figure — this correction was already implied by the v3 opening-position change but had not been
  carried into this section's payload figure until now).

**Combined center of mass (Y-axis, weighted average), 2-tube case, 91mm height:**

```
Y_com,total = (W_stand × Y_com,stand + W_payload × Y_com,payload) / (W_stand + W_payload)
            = (216g × 31.6mm + 177.2g × 57.5mm) / (216g + 177.2g)
            = (6,826 + 10,189) / 393.2
            ≈ 43.3mm
```

**Tipping margin, 2-tube case, 91mm height, at the locked 80mm depth:**

```
margin = Y_edge − Y_com,total = 80mm − 43.3mm = 36.7mm (≈ 46% of the 80mm footprint depth)
```

**Comparison across every version of this number, worked through rather than glossed over:**

| Version | Stand mass basis | Opening position | Y_com,total | Margin |
|---|---|---|---|---|
| v2 (85mm, hand-guessed volume) | ~87g (width-scaled guess) | Y≈45mm (stale) | 41.7mm | 38.3mm (~48%) |
| Coder's informal callout (85mm, real volume) | real CAD volume, fraction/Y_com,stand basis not fully documented | Y≈55mm (corrected) | 46.7mm | 33.3mm (~42%) |
| **v4, this recompute (91mm, real-volume-anchored)** | **~216g (CAD-anchored + height-scaled)** | **Y≈55mm (corrected)** | **43.3mm** | **36.7mm (~46%)** |

**Net finding: still comfortably tip-safe at ~46% margin, essentially in the same range as every
prior estimate (42–48%), not a new risk introduced by either the real-volume correction or the
height increase.** The discrepancy between this recompute (~46%) and the Coder's own quick 85mm
callout (~42%) is most likely explained by differing assumptions about the stand's own Y_com (this
document still assumes ≈30mm as a baseline, never independently verified against real CAD centroid
data — if the Coder has an actual measured centroid position, it should supersede this document's
assumption in a future pass) rather than a math error in either place — flagged honestly rather
than forced into false agreement. The taller/heavier 91mm body is very slightly less favorable
than an (never-built) 85mm-with-corrected-opening case would have been (this recompute's own
internal comparison: a same-method 85mm calculation would give Y_com,total ≈ (202×30 +
177.2×57.5)/379.2 ≈ 42.9mm, margin ≈37.1mm/~46.4%, i.e. height barely moves the needle — well
within the noise of this whole estimate).

**Side-to-side (X) tipping:** unchanged reasoning — the two channels are symmetric about the
body's X-center, so a symmetric (both-filled) fill produces no net X-axis tipping moment. With
only 2 tubes, the meaningful asymmetric case is simply **one tube filled, the other empty**, still
not expected to be a tipping risk given the 80mm width relative to a single ~88.6g tube's offset —
flagged for the Tester to physically spot-check (§7, edge case 2) rather than closed out on
hand-math alone.

**Caveat on this whole analysis:** this is still an order-of-magnitude estimate, now anchored to
one real CAD measurement (407,120mm³ at 85mm) but still built on several ESTIMATED assumptions
layered on top of it (linear height-scaling of volume, the 35–45% effective-material fraction, the
unverified ≈30mm stand Y_com baseline, and the still-unverified 27mm tube OD driving the whole bore
geometry, §8). The ~46% margin is large enough that these individual uncertainties are unlikely to
flip the stable/unstable conclusion, but this should still be confirmed with an actual tip-test on
the first physical 91mm print (fill both tubes, check on a level and on a slightly tilted surface,
and give it a light nudge given the Z-CoM note above) rather than closed out on hand-math alone —
see §8.

---

## 6. Print-time optimization — the explicit design goal

### 6.1 Levers used, and reasoning

| Lever | Choice | Reasoning |
|---|---|---|
| Overall size | 80×80×91mm functional-minimum envelope (§4.5, revised from 80×80×85mm in v3 for bore-clearance margin; revised down from 115×80×85mm for 3 tubes before that), **not** scaled to match the reference's 173×140×64mm single-tube footprint | The brief explicitly does not require matching or exceeding the reference's size — a smaller, function-derived envelope is the single biggest print-time lever available, since print time scales strongly with both height (layer count) and volume (deposition time). |
| Infill | **15% gyroid** (CONFIRMED by product owner, §9) | The body is a mostly-solid arc/wedge, not a thin shell — infill percentage, not wall count, is the main volume/time lever for a part shaped like this. 15% is a light structural fill appropriate for a static, non-flexing decorative item under only the modest static load analyzed in §5. |
| Wall / perimeter count | 3 perimeters (≈1.2–1.35mm at 0.4mm nozzle) | Comfortably above the 0.8mm (2×nozzle) structural minimum (§3) without adding meaningfully to print time on a part this size — walls are not the dominant time cost here, infill and height are. |
| Layer height | 0.2mm (CONFIRMED by product owner, §9) | Standard balance of speed vs. surface quality for a decorative item; not a fine-detail part. |
| Print orientation | See §6.2 | Chosen specifically to eliminate the need for internal hole supports, which is believed to be a major contributor to the reference's own 8–10hr print time. |

### 6.2 Print orientation — chosen to eliminate hole supports

**Because both bores share one common slant angle (§2.2), the whole part can be tilted as a
single rigid rotation so that both bore axes print vertically (parallel to the printer's Z
axis) simultaneously.** A hole printed with its axis aligned to Z requires no internal supports
and prints as a clean circular pocket at normal speed — this is the direct payoff of the "one
shared angle" decision in §2.2, and it is expected to be the single largest per-tube print-time
saving versus a design (like the reference, or a fanned-channel alternative) that has to fight an
overhanging/angled hole.

**What this means concretely:** the part's use-orientation "bottom foot" (the face that rests flat
on a table when in use) is **not** the same face that touches the print bed. The print-bed-facing
orientation is defined by tilting the whole body by the bore's slant angle (30° from the
use-orientation vertical) around the X (width) axis, so the bore axis becomes true vertical. This
is a **modeling reference plane the Coder should construct explicitly** (a rotated build plate
represented in the CAD tool), not something to eyeball from the use-orientation model.

**Support strategy — decided by the product owner, no longer an open question:** tilting the body
this way puts part of the use-orientation base foot into an overhang relative to the print bed (a
wedge-shaped gap under the tilted foot). The product owner has decided to **accept
slicer-generated support material under that overhang**, rather than adding a dedicated flat
"print-jig" bed-contact face to the model. **The Coder should not add a print-jig face** — the
model should reflect only the functional use-orientation geometry (§10 file paths), and the
Coder/Tester should expect and account for support generation in that overhang region when
slicing (support removal, resulting surface finish in that area) rather than treating its presence
as a defect.

### 6.3 Estimated print time and comparison to the reference (recomputed for 91mm height, v4)

**ESTIMATED, order-of-magnitude only — no slicer has run on an actual model yet.** This
supersedes the v2 (2-tube, 85mm) estimate below; figures are re-derived fresh for the 91mm height
locked in v3, using the same fixed/variable heuristic model as before rather than a fresh, unrelated
guess.

- Reference: 8–10 hours for **one** tube, ~173×140×64mm envelope.
- Our design (2-tube, 91mm): bounding-box volume 80×80×91mm = **582,400mm³ total** (up from
  544,000mm³ at 85mm — a 7.1% increase, matching the 91/85 height ratio exactly, as expected since
  only height changed). Per-tube bounding box = 582,400/2 = **291,200mm³**, vs. the reference's
  1,551,680mm³ per tube — **~5.3× smaller bounding box per tube** (down slightly from the v2
  estimate's ~5.7×, since our own bounding box grew a bit — still a large margin).

**Fixed vs. variable time, re-derived correctly for a height change (this is a different case from
the 3→2 tube change, and is worked through separately rather than reusing the old split
unchanged):**
- In the 3→2 tube recompute (v2), height was held constant (85mm in both cases), so the
  height-driven "fixed" component (base layers, perimeter walls printed at every layer) was
  correctly treated as a constant while only the volume-driven "variable" component changed.
  **That assumption does not hold here** — this time it's height itself that's changing (85→91mm),
  so the fixed component must now scale with height too (more layers = more perimeter/travel time),
  not stay flat.
- Fixed component (height/layer-count driven), scaled by the height ratio: `2h × (91/85) ≈ 2.14h`.
- Variable component (volume/infill driven), using the same rate as before (≈2.56×10⁻⁶ h/mm³,
  itself back-solved from the original 3-tube estimate — carried forward unchanged since it's a
  property of the printer/infill setting, not of this specific body): `2.56×10⁻⁶ h/mm³ ×
  582,400mm³ ≈ 1.49h`.
- **Total ≈ 2.14h + 1.49h ≈ 3.63 hours**, i.e. **~3.5–3.75 hours total** for the 91mm 2-tube unit
  (up modestly from the v2 (85mm) estimate of ~3–3.5 hours — consistent with the ~7% height/volume
  increase, not a large jump).
- **Per-tube: ≈3.63h / 2 ≈ 1.8 hours/tube** — up slightly from the v2 (85mm) estimate of
  ≈1.7 hours/tube, again tracking the modest height increase.
- **Net result against the actual differentiation goal:** ~1.8 hours/tube is still roughly
  **~4.5–5.5× faster per tube than the reference's 8–10 hour benchmark** (down very slightly from
  the v2 estimate's ~5–6×, reflecting the added height) — the core print-time goal remains
  comfortably met; the ~6mm bore-clearance safety margin added in v3 costs a small, worthwhile
  amount of print time, not a meaningful one.

**This entire estimate is still a heuristic order-of-magnitude model (assumed fixed/variable time
split, no slicer run performed) — validate on the first real slice, not a committed number.**

---

## 7. Edge cases

1. **Tube OD/length deviates from the 27mm × 150mm ESTIMATE (§4.1).** Real glass tube stock varies
   ±1–2mm OD across suppliers. If the actual tube is narrower than 27mm, it will sit loose and at
   an uncontrolled angle in the 28.5mm bore (defeating the whole slant-angle design intent in
   §4.3); if wider, it won't seat at all. This is the design's single highest-risk item — see §8,
   open question 1, before the Coder cuts final bore geometry.
2. **Uneven/partial fill (only one of the two tubes filled).** With only 2 tubes (revised down
   from 3, §2.1), the only meaningful asymmetric fill case is one tube filled and the other empty
   — shifts the combined center of mass sideways (X) and reduces the total front-back payload
   moment versus the both-filled case analyzed in §5. §5's analysis shows a comfortable margin for
   the worst-case *both-filled* scenario; the single-tube-filled case was reasoned through
   qualitatively (smaller total payload, one-sided X shift) but not fully hand-calculated —
   flagged for the Tester to physically spot-check (fill one tube only, check on a level and
   slightly-tilted surface) rather than trusting the both-filled-case math to cover every fill
   pattern.
3. **Blind-bore moisture/algae buildup.** The closed-bottom bore chosen in §4.2 for its stability
   and retention benefits has a real trade-off: unlike an open through-channel, it can't be flushed
   or fully dried if condensation collects or a tube ever leaks at the seal. Recommend this be
   called out as a user-facing care note (periodically remove tubes and let the bores air-dry), and
   accepted as an inherent trade-off of the deep-embedment strategy rather than something the
   geometry alone can fully prevent.

---

## 8. Open questions / risks requiring a decision before modeling proceeds

**Updated: items 3, 4, and 5 below are now RESOLVED by product-owner decision; items 1 and 2
remain genuinely open.** Resolved items are kept listed (not deleted) so the decision trail stays
visible.

1. **OPEN — Tube OD (27mm) is ESTIMATED and unverified against a real tube** (§4.1). This drives
   the bore diameter (§4.2), which is the design's core mating dimension. **Requesting: a
   manufacturer spec sheet for the tube to be purchased, or a caliper/ruler-photo measurement of a
   physical sample,** before the Coder finalizes the 28.5mm bore diameter. No physical tube has
   been measured yet — still open.
2. **OPEN — The 30° slant angle (§4.3) is a first-pass engineering estimate, not empirically
   validated.** Recommend the Coder produce a low-commitment single-channel test print (or the
   full 2-tube body at draft settings) specifically to fill-test the angle/bore combination before
   treating it as final — the reference's own "won't spill" claim implies this kind of physical
   tuning was done on their side, and we haven't done our own yet. No test print has been done
   yet — still open.
3. **RESOLVED — Print-orientation trade-off (§6.2).** Product owner has decided: accept
   slicer-generated support material under the tilted-foot overhang; do **not** add a dedicated
   print-jig bed-contact face to the model. See §6.2 for the final wording.
4. **RESOLVED — 3-tube vs. 2-tube.** Product owner has decided on **2 tubes**, reversing this
   spec's original 3-tube recommendation. See §2.1 for the revised reasoning and §5/§6.3 for the
   recomputed stability and print-time figures.
5. **RESOLVED — Base depth.** Product owner has decided on **80mm**, prioritizing the stability
   margin over a more compact silhouette. The 65mm functional-minimum alternative is no longer
   under consideration. See §4.5/§5.

---

## 9. Slicer settings — CONFIRMED, no longer an open question

**Confirmed by the product owner: 0.2mm layer height, 15% gyroid infill**, as originally proposed
in §6.1. The Coder should treat these as final production settings, not defaults pending
confirmation.

---

## 10. File paths for the Coder

| Path | Contents |
|---|---|
| `propagation-station/src/propagation_station/propagation_station.stl` | Full 2-tube stand, single body, in **use orientation** (base foot flat, for reference/viewing) |
| `propagation-station/src/propagation_station/propagation_station_print.stl` | Same body, pre-rotated into the **print orientation** described in §6.2 (bore axes vertical), ready to slice without further rotation |
| `propagation-station/src/propagation_station/propagation_station.step` | Parametric/editable source, both orientations or a rotation parameter, per the Coder's tool of choice |
| `propagation-station/src/propagation_station/propagation_station.3mf` | Slicer-ready project export, print orientation, at the settings from §6.1/§9 once confirmed |

---

## 11. Revision history

| Version | What changed | Why |
|---|---|---|
| v1 | Initial spec, new project, no prior revisions. | First pass at an original 3-tube design brief. |
| v2 | Tube count changed 3→2 (§2.1). Overall width recomputed 115mm→80mm and channel centers recomputed to ±17.25mm (§4.2/§4.5). §5 stability analysis fully recomputed for 2 tubes (margin comes out essentially unchanged at ~48%, worked through rather than assumed — payload and stand weight both scale down together). §6.3 print-time estimate recomputed for 2 tubes: total time drops to ~3–3.5h, but per-tube time rises slightly to ~1.7h (from ~1.33h midpoint) since the fixed height-driven cost now spreads over fewer tubes — still ~5–6× faster per tube than the reference. Print-orientation support trade-off (§6.2) locked to "accept slicer support, no print-jig face." Base depth (§4.5) locked at 80mm, no longer an open trade-off. Slicer settings (§9) confirmed at 0.2mm layer height / 15% gyroid infill. §8 updated: 3 of 5 open questions closed out (support strategy, tube count, base depth); tube-OD verification and slant-angle validation remain open. Title changed from "Tri-Channel Arc" to "Dual-Channel Arc" to match. | Product owner reviewed the original spec's open questions (§§8–9) and made decisions, relayed via the 3d-director coordinating session. |
| v3 | Overall height (§4.5) increased **85mm→91mm**. Channel opening position (§4.5) corrected **Y≈45mm→Y≈55mm from back face**. §4.4 gained a correction note explaining both changes: while building the actual CAD model, the Coder found that §4.4's original vertical-reach/depth-clearance math treated the bore as a zero-width centerline, ignoring that the bore's own 28.5mm-diameter cylinder has a floor cap and opening rim that are tilted disks extending a further ±7.1mm vertically and ±12.3mm in the front/back direction beyond the centerline-only estimate. At the original 85mm height this left only ~2.1mm of real clearance above the bore opening (not the ~16mm the original hand math implied) and required the Y≈45mm→55mm opening-position correction to stop the blind floor from breaking out the back face. The Coder flagged the thin 2.1mm margin as a real risk, especially given the bore diameter is still keyed to the unverified 27mm tube OD (§4.1/§8, open question 1). The product owner decided to add real buffer now (cheap insurance) rather than risk redoing geometry after the tube is finally measured, and chose 91mm (of the 90–92mm range offered by the Coder) — giving ~8.1mm of clearance above the bore opening while still honoring the 8mm base-foot minimum below the floor. Both file outputs (§10) and the exported model were rebuilt and re-verified at the new height; body/face counts, the 6mm land, the 8.5mm edge wall, the 8mm floor clearance, and the vertical bore axis in print orientation were all re-confirmed unchanged/correct. **Not yet updated for v3:** §5's stability numbers and §6.3's print-time/bounding-box-volume estimates still narrate the pre-v3 85mm figure and the original (never-CAD-verified) volume/mass guesses; the ~6mm height increase is not expected to materially change either conclusion, but neither section has been formally recomputed against 91mm or against the Coder's actual-CAD volume finding (§5 already carries a separate Coder callout about the real solid volume running ~2–2.3× the original hand estimate) — flagged here rather than silently left inconsistent. | Product owner decision, relayed via the 3d-director coordinating session, in direct response to the Coder's own discovery (during CAD modeling) of the thin 2.1mm margin above the bore opening. |
| v4 (this revision) | Closed out v3's flagged gap: §5 (stability) and §6.3 (print time) fully recomputed for the 91mm height. **§5**: retired the v2 hand-guessed "solid-equivalent volume" scaling method entirely and anchored stand mass to the Coder's real CAD volume (407,120mm³ at 85mm), linearly height-scaled to ~435,860mm³ at 91mm → **~216g estimated stand mass** (vs. v2's ~87g — a ~2.5× correction, consistent with the previously-flagged 2–2.3× CAD-vs-hand-estimate gap). Also corrected the payload's own center-of-mass figure, which had been left stale at the pre-v3 Y≈45mm opening position (47.5mm) even after v3 moved the opening to Y≈55mm — now 57.5mm. Combined center of mass ≈43.3mm, **tipping margin ≈36.7mm (~46% of the 80mm footprint depth)** — still comfortably stable, in the same 42–48% range as every prior estimate; a 3-way comparison table added showing v2/Coder-callout/v4 side by side rather than presenting one number as if it had always been there. Flagged an unresolved ~4-point discrepancy with the Coder's own informal 85mm callout (~42%), most likely from differing stand-Y_com assumptions, and recommended real CAD centroid data supersede this document's ≈30mm baseline assumption if available. Also noted the taller body's *vertical* (Z) center-of-mass rise as a secondary dynamic-tipping consideration distinct from the static Y-position math. **§6.3**: bounding box updated to 80×80×91mm (582,400mm³ total, 291,200mm³/tube); re-derived the fixed/variable print-time split correctly for a *height* change (fixed cost now scales with the height ratio too, unlike the 3→2 tube case where height was constant) → **~3.6 hours total, ~1.8 hours/tube** (up slightly from v2's ~3.4h / ~1.7h/tube), still **~4.5–5.5× faster per tube than the reference's 8–10h benchmark**. | Product owner/Coder found §5 and §6.3 had gone stale relative to the real 91mm model after v3's height/opening-position fix; requested via the 3d-director coordinating session, explicitly asking the volume estimate be anchored to the Coder's real measured figure rather than re-scaled from this document's own earlier guess. |
