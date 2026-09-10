# Reviewer — Pet Memorial Urn, Small (0–25 lb), First Review Pass

Cold start. Read `specs.md` and `tests.md`/`verdict.md` (Tester) in full, read Large's
`README.md`, `parameters.md`, and `concept/brief.md` as the reference for the shared v7 design
identity (per specs.md §1, Small is a re-scale/re-derivation exercise against that identity, not a
new concept pass), and independently re-derived the Tester's headline numbers from the exported
STEP/STL files using my own scripts rather than re-reading their reported figures. I also had
intermittent live access to the `pet-memorial-urn-small` Fusion document this session — enough to
confirm topology and apply a material appearance, but not enough to reliably capture a screenshot of
it (see §5). Everything below is organized around the five things I was asked to check.

## Overall verdict: APPROVED, with one explicit BLOCKING condition on production printing

**The CAD build is sound, precisely matches its own spec, and is a faithful, if not perfectly
proportion-matched, re-derivation of the Large v7 design identity at a smaller scale (see §1).**
Independent re-measurement (my own scripts against the exported STEP/3MF/STL files, not a re-read of
the Tester's numbers — see §2) confirms cavity volume, wall thickness at multiple heights, the
plug/bore clearance, and the neck-to-collar overhang all match the spec closely, corroborating the
Tester's own independent pass. This is approved to proceed to the next stage of production
preparation.

**This does not clear the design for a full-scale production print run.** Per this project's own
standing convention (identical to how the 80mm/72mm neck-ID risk was handled on Large and Medium),
the following remains a named, unresolved blocker, not a routine watch-item:

> **The 70mm neck/collar ID is tagged `ESTIMATED` in specs.md §6 and mates with a real external
> object (a crematorium remains bag for a 0–25 lb pet) this team does not have in hand.** The
> spec's own research is real and reasoned (a corroborated industry tier boundary, two sourced
> small-tier opening figures of 63.5mm/66.7mm, and explicit commentary that range is a documented
> bag-fit pain point at this weight bracket) — but it is a compromise number, not a measurement.
> I found no evidence anywhere in this project's files that `neck-fit-test-small` has actually been
> printed and checked against a real or mocked small-pet remains bag, and no written risk
> acceptance from the requester overriding that gate. **Do not commit `urn-body-small` to a
> full-scale production print until either (a) that physical test has been run and passed, or
> (b) the requester explicitly accepts the risk in writing.** This is a routing item back to the
> Planner/requester, not something a modeling fix resolves — the CAD is already an accurate build
> of the estimate.

**On material:** the body is PLA at a 2.4mm wall, thinner in absolute terms than Large's 4mm. The
Tester flagged this as a drop/impact-risk concern and recommended PETG. Per the task brief for this
review, the requester was already asked and explicitly chose to keep PLA for the body despite that
recommendation — **this is a confirmed, informed decision, not an unexamined default, and I am not
reopening it.** It should be recorded as such in the size's own parameter sheet once written (§4),
so a future reader doesn't mistake it for an oversight.

---

## 1. Business fit / concept fidelity

**Reads as the same design, smaller — with one real, worth-naming proportional drift.** Small
carries forward every identity-defining feature of Large's v7 lineage correctly: no handle, no
magnet pockets, a flush-fit brim (81.7mm brim vs 82.0mm collar, the same −0.3mm allowance
convention Large uses), a flattened dome-plateau apex rather than a rounded point, a plain
undecorated body, and a straight-walled capped alignment plug rather than a tapered stopper. All of
these are qualitatively present and correctly built, not merely claimed in the spec.

**The one thing worth naming plainly:** because the neck ID (70mm) was deliberately *not*
naive-scaled from Large's 80mm (specs.md §6 — a reasoned, cited departure, not an error) while the
belly was scaled close to naive, Small's **collar-OD-to-belly-OD ratio comes out at ≈83.7% (82mm ÷
98mm)**, versus **≈65% on Large (100mm ÷ 153.9mm)**. Small will read as a noticeably
wider-mouthed, less pinched-neck vessel relative to its own belly than Large does — a legitimate,
disclosed, function-driven consequence of not being able to shrink a bag-clearance opening in
proportion to volume, but a real silhouette difference, not just a linear shrink. This isn't a
defect and doesn't block approval (the spec's own hierarchy checks in §7.4 — belly > base > shoulder
> collar — are still satisfied), but whoever signs off on the finished look should know the two
sizes won't sit side by side looking like pure scale copies of each other. I was not able to
independently confirm this visually against a real hero render this session (§5) — it should be
double-checked once one exists.

**Concept-image provenance, for completeness:** Small has no `concept/` folder of its own — per
specs.md §0, this is a deliberate, correct choice (a re-scale exercise against an already-approved
identity, not a fresh concept pass), and it explicitly does not re-litigate the identity decisions.
I compared Small's built geometry against Large's *actual, current* v7 identity as documented in
`README.md`/`parameters.md` (no handle, flush brim, flattened apex) rather than against the original
`concept-v2.png` image directly, since that image still shows the now-deliberately-removed bail
handle — Large's own README is explicit that the handle removal knowingly supersedes the original
concept brief, and Small correctly inherits the post-handle-removal identity, not the original
image's literal appearance. This is the right reference to hold Small to, and Small clears it.

---

## 2. Independent geometry spot-check (my own scripts, not a re-read of the Tester's numbers)

I wrote a fresh STL parser/analyzer (binary STL → numpy triangle arrays) and computed volumes via
the divergence theorem and cavity cross-sections via plane–triangle intersection + radius
clustering at chosen heights — a different implementation from the Tester's approach, run
independently against the same exported files.

| Check | My independent measurement | Spec target | Tester's figure | Result |
|---|---|---|---|---|
| Body shell (material) volume, whole-mesh divergence theorem | **72.259 cm³** | ≈70.76 cm³ hand-calc | 72.26 cm³ | Matches Tester almost exactly, +2.1% vs. hand-calc |
| Body cavity volume, own plane-slice + trapezoidal integration (600 samples, 0–75.7mm) | **412.13 cm³** | 409.6775 cm³ (±5%: 389.19–430.16) | 412.2–412.4 cm³ | PASS, +0.6% vs. target, matches Tester |
| Nominal wall thickness, sampled at 5 heights below the collar (z=5,15,25,45,60mm) | **2.4000mm mean** (range 2.396–2.404mm across 483 samples) | 2.4mm | 2.400mm | Exact match |
| Collar-band wall thickness (z>73mm) | **5.997mm mean** (22 samples) | 6.0mm | 5.999–6.000mm | Exact match |
| Neck ID (body, at collar) | **35.00mm r → 70.00mm ID** | 70mm | 70.000mm | Exact match |
| Plug OD (lid) | **34.745mm r → 69.49mm OD** | 69.5mm | 69.50mm | Exact match |
| Plug/bore diametral clearance | **≈0.51mm** (0.255mm/side, both surfaces measured on their own separate files) | 0.5mm | 0.500mm | PASS, matches |
| Plug interior void ID | **32.345mm r → 64.69mm ID** | 64.7mm | 64.70mm | Exact match |
| Lid brim OD | **40.845mm r → 81.69mm OD** | 81.7mm | 81.70mm | Exact match |
| Dome apex plateau diameter | **16.821mm** (r=8.4103mm, read directly off the flat top-face vertices, z=35.3mm exactly) | ≈17.8mm derived | 16.82mm | Confirms the Tester's flagged −5.5% minor deviation is real, reproducible on a second, independent method — not a Tester artifact |
| Peak neck-to-collar overhang (numeric dr/dz between z≈69.0–69.7mm) | **≈44.4°** (coarse differencing) | 44.5° estimate | 44.8° measured | Consistent within method noise, all three under 45° |
| `neck-fit-test-small`: ID/neck-OD/collar-OD/flange | **70.00 / (41.33–43.47 through taper, consistent with 44→37.4mm shoulder-to-taper-end shrink) / ~82.0mm / ~100mm×5mm** | 70/74.8/82mm, ~100mm flange | All exact | Matches body's own numbers, confirms it's a faithful proxy, not reused/mismatched geometry |

**All of these independently corroborate the Tester's pass — this is a genuinely precise build**, not
just internally self-consistent. The one real finding worth carrying forward is the dome-plateau
size (5.5% under its derived target) — cosmetic/documentation-accuracy only, still >20x the print
floor, not a rework trigger.

---

## 3. Documentation — required follow-up, not written here

**`pet-memorial-urn/small/` currently has `dot_pipeline/` (specs.md, tests.md, verdict.md, and now
this review.md) but no `README.md` and no `parameters.md` of its own.** Checking this project's own
established convention: Large has both at its project root, written and kept current through every
revision; Medium — which was built before Small but has not yet had its own Reviewer pass — also
does not have them yet either. That's consistent with a real pattern in this project: these two
documents get written **once a size clears Reviewer approval**, not before. Small has now cleared
that bar (§0, conditionally). **Flagging as a required follow-up, not writing it myself** (out of
scope for this pass, per the task brief): someone needs to produce `small/README.md` (what it is,
current dimensions, the neck-fit-test blocker, material choice and the fact PLA-for-the-body was a
confirmed informed decision, print orientation, known limitations) and `small/parameters.md` (the
as-built dimension table, VERIFIED vs. ESTIMATED tags, revision history) mirroring Large's format.
This is genuinely cheap to produce from the material already in `specs.md`/`tests.md` and should not
be skipped just because the CAD itself is done.

---

## 4. Cost sanity check

Spec's own estimate: body ≈$1.75–2.19, lid ≈$2.23–2.79, combined ≈$4.0–5.0 in filament (PLA body,
PETG lid, §12 of specs.md). Using my own independently-measured material volumes instead of the
spec's hand-calc (body 72.26 cm³ vs. 70.76 assumed; lid 91.28 cm³ vs. 87.6 assumed — both a few
percent higher, as expected since real spline/revolve geometry usually bulges slightly past a
straight-chord hand-calc):

- Body: 72.26 cm³ × 1.24 g/cm³ ≈ 89.6g ≈ **$1.79–2.24**
- Lid: 91.28 cm³ × 1.27 g/cm³ ≈ 115.9g ≈ **$2.32–2.90**
- **Combined ≈ $4.11–5.14** — within a few percent of the spec's own estimate, still a trivially
  small production cost for a decorative memorial piece. **Cost-effective, no concern.** (This is
  filament cost only, consistent with how Large/Medium's own cost sections are scoped — it doesn't
  include print time/labor, same convention as the rest of this project.)

---

## 5. Render — partially completed; a real tool limitation, not a skip

I had intermittent live access to the `pet-memorial-urn-small` Fusion document this session (three
documents are open concurrently in this shared session: Small, Medium, and an unrelated "MI
Lightbox"). I was able to:

- Confirm, via a script that checked component/occurrence names in the same call as activation, that
  the live document genuinely contains `urn-body:1` / `urn-lid:1` / `neck-fit-test-small:1` matching
  the expected Small signature (not contaminated with Medium's or Large's components).
- **Apply a real material appearance to the live geometry**, matching the spec's material choice and
  Large's own naming convention: `Matte PLA - Stoneware Tan (urn-body-small)` on `urn-body-solid`
  and `Matte PETG - Stoneware Tan (urn-lid-small)` on `BrimDomeSolid` (both copied from the Fusion
  Appearance Library's "Plastic - Matte (White)" and recolored to a tan/stoneware tone). This was
  confirmed applied while the document was verified active, and should persist for whenever a render
  can actually be captured.

**I was not able to reliably capture a screenshot of it.** Every screenshot call I made after that
point — including three consecutive attempts, each immediately preceded by a script call that
re-activated Small and printed confirmation that `app.activeDocument.name == 'pet-memorial-urn-small'`
at that exact moment — returned the **identical image of an unrelated part**: the Medium size's
`neck-fit-test-medium` article, in default steel-gray, not Small's urn. Changing the camera direction
parameter (`front` vs. `iso-top-right`) did produce a genuinely different image, proving the tool
itself isn't frozen or cached — it is consistently bound to whatever the *other* concurrent session
(evidently mid-session work on the Medium build) has focused, regardless of what my own script's
`Document.activate()` call reports back as successful. This is the same class of limitation the
Tester already flagged in `tests.md` §5 (their screenshot call landed on an unrelated `Untitled`
document); I'm able to confirm it's a real, reproducible, non-probabilistic problem in this
specific shared session, not something more retries would fix.

**I am not substituting a screenshot of the wrong part, or an AI-generated image, for the real
render** — per the task's own requirement that this must be the actual model. **No render file has
been produced for Small this pass.** This is carried forward as a required follow-up: someone with
exclusive or reliable UI/session access to the `pet-memorial-urn-small` Fusion document needs to
capture the hero screenshot (the appearance is already set up and waiting) and save it to
`pet-memorial-urn/small/render/pet-memorial-urn-small-hero.png`, consistent with this project's
convention of producing one on approval. This also means the concept-fidelity question in §1 (the
wider collar-to-belly ratio) still needs a real visual gut-check once that render exists — I could
not do that check with a picture this pass.

**Side observation, out of scope for Small but worth flagging so it isn't lost:** while comparing
render conventions, I found that Large's own root-level `render/pet-memorial-urn-hero.png` currently
has an uncommitted, unsaved working-tree change (per this session's git status) that appears to be a
raw, un-styled viewport screenshot of the *no-handle* v7 geometry (grid lines visible, default
appearance), replacing what's committed in git history — a properly lit, tan-appearance studio
render that still shows the *handle* (i.e., pre-v7 geometry). Neither version is both "v7 geometry"
and "properly styled" at the same time in the current working tree. I have not touched or reverted
this file — it belongs to Large, not this review — but given the same concurrent-session behavior
documented above, it looks like a plausible casualty of the same cross-session contention, and
whoever next touches Large's files should check it before assuming the committed or working-tree
version is the correct, current hero image.

---

## Summary for the Director

- **Approved to proceed**, blocked from full production printing on the neck-ID physical test —
  exactly the same shape of condition this project has applied consistently to Large and Medium.
- Independent geometry re-check (own scripts, own methods): clean pass, matches spec and the
  Tester's numbers closely across cavity volume, wall thickness, plug/bore clearance, and overhang.
- Concept fidelity: correct in kind (no handle, flush lid, flattened apex, plain body), with one
  real, disclosed proportional drift (wider mouth-to-belly ratio than Large) worth a visual
  gut-check once a render exists.
- Documentation: `small/README.md` and `small/parameters.md` do not exist yet and are a required
  follow-up, not written in this pass.
- Cost: sanity-checked independently, still trivially cheap (~$4.10–5.15 combined filament).
- Render: appearance applied to the live document; screenshot capture blocked by a real,
  reproducible shared-session tool limitation (confirmed, not assumed) — flagged as a follow-up,
  not silently skipped.
