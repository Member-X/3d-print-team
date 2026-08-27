# Etsy Market Research — Findings Log

Running log of market research passes for new 3D-printable product ideas. Append new dated
sections below rather than overwriting prior research.

---

## 2026-08-25 — Initial pass, base keyword "3d printed"

### Method note: Phase 1 autocomplete mining was blocked

The planned Phase 1 sweep (typing "3d printed a" through "3d printed z" into Etsy's live search
box and reading the autocomplete dropdown) did not work. Etsy's search box silently ignored all
synthetic input — standard `type`, character-by-character key presses, direct value-setting, and
click+type were all tried; the autocomplete dropdown never left its default "Popular right now"
state, and pressing Enter never navigated. Meanwhile plain URL navigation
(`etsy.com/search?q=...`) worked completely normally. No visible CAPTCHA appeared, but silently
no-op'd synthetic input while normal navigation works is the standard signature of client-side
anti-automation defenses, not a UI bug — treated as the same category of blocker as a CAPTCHA and
the sweep was stopped rather than pushed through.

**Fallback method used instead:** `WebSearch` for trend/seller-forum signal, plus direct Etsy
**URL-based** search/listing navigation (not typing) — this worked fine and produced real
price/review/competition data. There is no autocomplete/search-suggestion keyword list from this
pass; treat demand signals below as listing- and shop-level evidence, not search-volume evidence.
**Future passes should default straight to this URL-navigation + WebSearch method** rather than
re-attempting the autocomplete sweep each time, unless Etsy's automation defenses are known to have
changed.

### Context: Etsy's August 2026 policy change

Etsy's updated Prohibited Items Policy (effective Aug 11, 2026) now requires items made with
computerized tools (3D printers, laser cutters, CNC, etc.) to be based on the **seller's own
original design** — the old allowance for manufacturing/listing from a purchased or templated
design file is gone. Many "flooded" listings in the categories below are resellers of
downloaded/purchased STLs, now non-compliant. This shop's actual workflow (original
parametric/mesh designs via the 3d-planner pipeline) is structurally compliant — a real, if
hard-to-quantify, tailwind.

### Existing shop products checked (not to be duplicated)

`cat-toy-holder/` (wall-mounted cat toy holder), `cat-bowl/` (sleeping-cat bowl concept),
`noise-maker/` (print-in-place ratchet noisemaker), `switch-plate-covers/` +
`lightswitch-cover-single/` (decora/toggle/jumbo plates).

### Ranked shortlist

**1. Plant propagation stations (printed stand + purchased glass test tube) — strongest pick**
- Demand: live listing (RosebudHomeGoods, "Circle Propagation Station") sits inside a shop with a
  shop-wide 4.8 rating from 5,300+ reviews and 28,600+ sales over 6 years — durable category
  demand. Multiple other active shops (LindaMakess, EverBloomGift "Bestseller," Habitatable
  "Etsy's Pick") confirm this.
- Competition: moderate, not flooded — real design variety (arch, circle, hanging ladder,
  music-box carousel), not just clones.
- Printability: good — simple stand holding an angled channel for a purchased ~25×150mm glass
  tube. No multi-color, no fragile features, small footprint (reference part 6.8"×5.5"×2.5").
  Design the tube channel to avoid supports.
- Margin: price $16–24, but the seller's own listing states 8–10 hour print time per unit — long
  relative to price. Material cost low (~$2–3); throughput (~1 unit/printer/night) is the real
  constraint. Worth designing a leaner/shorter version or batching multiple per plate.
- Caveat: requires sourcing glass tubes as a bought-in component, not pure print-and-ship.

**2. Minimalist earring / jewelry organizer stands**
- Demand: live listing (SpeedySnail3D, $15 minimalist earring holder) — 4.9 rating (88 reviews),
  327 sales over 2.5 years, explicitly a small/home-based shop succeeding at solo scale. $15–30 is
  a normal price band across other shops (OneAr3D $23.79, NovaflairDesign $29.99).
- Competition: present but not brutal — real style variety (minimalist rack, compartment tray,
  fluted/stacked, novelty designs).
- Printability: very good — small, flat/vertical, no supports, no multi-color, likely under 2hr
  print. Easiest item on this list to actually produce.
- Margin: best $/print-hour ratio found — ~$1 or less material cost, 1–2hr print, sells $15–30.
- Design note from real review data: one buyer complained slots were too close together for larger
  earrings — leave generous slot spacing or offer a "large earring" variant.

**3. Adaptive/assistive kitchen grip tools (jar & bottle-cap openers)**
- Demand: mixed. A checked listing (3DOnePro, $5.99 arthritis bottle opener) had 42 reviews at 4.5
  stars — real repeat demand — but is now sold out/not visibly relisted, and that shop spans many
  unrelated novelty niches rather than specializing.
- Competition: moderate, ~a dozen shops, $3.50–$18 spread, several near-identical designs.
- Printability: excellent — chunky ergonomic shapes, no supports, fast (well under an hour).
- Margin: the weak point — most listings cluster $4–15; fine per-unit margin but low absolute
  revenue per unit, needs volume. Best pursued with a differentiated angle (e.g.,
  prescription-bottle or OXO-style caps) rather than a generic "arthritis opener."
- Value-add: diversifies buyer motivation (functional/assistive, aging-population tailwind) away
  from purely aesthetic desk decor.

**4. Dice towers / tabletop-gaming accessories**
- Demand: real hobbyist niche; elaborate themed towers ($18–35: Iverson3DPrinting collapsible
  castle $28, JoyThroughColor spiral staircase $18, BearKainHatsNPrints $25) clearly outsell plain
  ones ($7–15).
- Competition: moderate-to-high, but aesthetic/theme differentiation is clearly rewarded.
- Printability flag: elaborate interior-baffle designs carry real overhang/support risk — supports
  are hard to remove from an enclosed tower interior, and a bad baffle also just doesn't randomize
  dice well. Needs deliberate geometry design at the 3d-planner stage, not a naive print. Fits bed
  easily (~7" tall).
- Margin: fine if print time stays 3–6hr; an 8+ hour design would erode the price advantage.

### Flagged as poor opportunities (researched, not recommended)
- **Articulated fidget animals** ("flexi" dragons/axolotls/etc.): huge demand signal but badly
  saturated — small ones pushed down to $2.25–$8, below what covers a solo shop's time. Only
  larger/detailed ($18–20) versions clear a healthy price. At most a low-effort add-on, not a
  flagship.
- **Cable/cord organizers**: extremely commoditized, $2.69–$12, little differentiation, further
  undercut by digital-download STL bundles. Skip.

### Worth a follow-up look (thin data — not validated this pass)
- **Pet treat/puzzle dispensers** — natural extension of the existing cat-toy-holder/cat-bowl
  line; general trend signal positive but no specific listing/review data pulled this round.
- **Other switch/wall-plate hardware variants** — adjacent to existing switch-plate-covers work;
  not researched at all this pass.

### Handoff

Once an idea is picked (or a follow-up niche investigated), the next step is `3d-director` (or
`3d-planner` directly) to turn it into a design spec — carrying forward the printability notes
above (e.g., propagation-station channel angle for no supports, dice-tower baffle geometry,
earring-slot spacing).

### Sources
- [Etsy Circle Propagation Station listing](https://www.etsy.com/listing/1414079589/circle-propagation-station-3d-printed)
- [Etsy Minimalist Earring Holder listing (SpeedySnail3D)](https://www.etsy.com/listing/1697070971/3d-printed-earring-holder-minimalist)
- [Etsy Arthritis Bottle Opener listing (3DOnePro)](https://www.etsy.com/listing/1783100477/3d-printed-arthritis-bottle-opener)
- [Best-Selling 3D Printed Items on Etsy 2026 — 3DSEARCH Blog](https://3dsearch.net/blog/best-selling-3d-printed-items-etsy-2026)
- [15 Best Selling 3D Printed Items on Etsy (2026 Profit Guide) — Hyper3D](https://hyper3d.ai/blog/best-selling-3d-printed-items)
- [Tom's Hardware: Etsy cracks down on 3D printed products](https://www.tomshardware.com/3d-printing/etsy-cracks-down-on-3d-printed-products-new-rules-exclude-many-3d-printed-items-from-listings)
- [ShieldMyShop: Etsy's August 2026 Policy Changes](https://www.shieldmyshop.com/blog/2026-04-28-etsy-august-2026-policy-changes-original-design-pod-sellers)

---

## 2026-08-26 — Focused pass: pet urn / pet memorial niche

Base keywords: "pet urn" and "pet memorial." This is a grief-adjacent category — the research
itself is treated as a normal, legitimate Etsy niche, but the write-up uses measured, respectful
language given the subject matter, since this is a real business decision about products bought by
people grieving a pet.

### Method note: autocomplete sweep re-confirmed blocked, one attempt only

Made exactly one attempt before falling back (per the updated agent process): typed "pet urn p"
into Etsy's live search box — keystrokes were not registered at all, no autocomplete dropdown
appeared. Matches the 2026-08-25 finding exactly. No CAPTCHA/explicit bot-detection page was shown.
Moved directly to `WebSearch` + Etsy `search?q=` URL navigation.

### Existing shop products checked (not to be duplicated)

`switch-plate-covers/`, `lightswitch-cover-single/`, `cat-toy-holder/`, `cat-bowl/`,
`noise-maker/`, `propagation-station/` (in progress). None overlap with pet urns/memorials.

### Two distinct product angles on Etsy

- **Functional urns** (must hold ashes): dominated by ceramic/wood/metal, $30–$250+, almost no 3D
  printed competition — but this also signals buyers default-expect a crafted, non-plastic material.
- **Memorial keepsakes/plaques that don't hold ashes**: mostly engraved metal/slate/granite/wood
  **outdoor** grave markers — PLA is a poor material match here (UV/weather degradation); skip
  outdoor plaques entirely as a PLA line. One indoor sub-niche (paw-print keepsake stands) is a
  strong printable fit instead — see shortlist #1.

### Ranked shortlist

**1. Paw-print keepsake display stand — safer bet, recommend starting here**
- A small printed base/frame holding a clay/plaster paw-print impression the customer already owns
  (from a vet/crematorium), with an optional raised-lettering name plate.
- Demand: live listing (BuiltByPhil, $39) — 5.0 stars/9 item reviews spread Feb–Aug 2026, Star
  Seller, shop-wide 5.0/76 reviews/243 sales over 11 years.
- Competition: thin — most "pet memorial stand" competitors sell the paw-print casting kit itself
  (different, non-printable product), not a stand for one you already have.
- Printability: excellent, safest item on the list — simple base + sized cutout/lip, optional
  text, no supports, no multi-color, well under bed size, likely under 2hr print.
- Margin: very strong — rough estimate &lt;40g/&lt;$1 material vs. $39 price.
- Why safer: doesn't touch ashes/remains directly, doesn't have to *be* the emotional keepsake
  itself (the paw print is) — lowest "does plastic feel appropriate" risk on this list.

**2. Minimalist geometric pet urn (functional, holds ashes) — highest upside, more execution risk**
- A small faceted/geometric lidded box, tiered by pet size, optional engraved name+dates, printed
  in a premium matte/silk PLA.
- Demand: strongest single data point this pass — listing (Weenielabpeturns, $54.71–$91.27) has a
  **Bestseller** tag despite the shop being only 3 months old, 236 sales, 5.0/33 shop reviews, all
  7 item reviews 5-star and dated Jul–Aug 2026 (genuine recent velocity, not legacy reviews).
- Competition/risk: a near-identical listing (MrYaushop, $36.68–$63.35) with close-to-verbatim
  marketing copy appeared one week old with zero reviews — the format is being cloned in
  near-real-time; expect more fast-followers and price pressure.
- Printability: better than expected — the Weenielabpeturns listing explicitly instructs buyers to
  place ashes in the crematorium's sealed bag inside the urn, not loose. **The urn itself doesn't
  need to be airtight** — a standard lidded-box print (faceted walls, friction-fit or magnet lid),
  no supports if angled correctly. Sizes small (9.9–16cm), well within bed size.
- Finish-expectation flag (real risk, not just marketing): both live listings emphasize the piece
  doesn't "feel like plastic" — implies matte/silk filament choice and likely a light sanding pass
  per unit, a real post-processing step beyond typical Etsy printables.
- Margin: best raw numbers on the list if the finish bar is met — small size likely &lt;100g/
  ~$1.50–2 material, 3–5hr print, vs. $54.71+ price, even accounting for finishing time.

**3. Generic low-poly pet sculpture/figurine (sold as decor, organically bought as memorial)**
- A stylized low-poly animal figurine (breed silhouette, not custom photo likeness).
- Demand: shop-level evidence strong (DiDiSensei, 4-year shop, 7.1k shop reviews, 25.9k sales,
  Star Seller) though this specific SKU's own reviews are thin (10, 4.2 stars) — one directly
  confirms memorial-motivated purchase of a non-memorial-marketed item ("I bought it because my
  puppy passed away... wanted to keep him there with me").
- Competition: DiDiSensei is large/established across many breeds — hard to compete head-on, but
  breed coverage is inherently incomplete, leaving room for a narrower, well-executed breed set.
- Printability: very good — low-poly faceted geometry, minimal overhangs, no supports, single
  color, no personalization pass required.
- Margin: solid but not spectacular, and size-dependent — 6" (~113g/$2-3 material) sells $16.79;
  10" (~369g/$7-8 material) sells $53.89–76.99. Favor 8"+ variants for better $/hour economics.
- Lowest emotional/operational risk of the three — no ash/remains handling, can be marketed as
  general decor first, repositioned toward memorial buyers later via an optional name-plate add-on.

### Flagged as poor opportunities (researched, not recommended)
- **Custom photo-realistic pet portrait sculptures/urns**: decent prices ($43–76) but require
  per-order sculpting/photogrammetry or multi-color layered-lithophane technique — closer to a
  bespoke commission business than a repeatable print-and-ship product. Note: multi-color pieces
  need a confirmed AMS unit on the shop's Bambu A1 (not confirmed as attached) — treat as out of
  scope until verified.
- **Outdoor pet memorial plaques/garden stones/headstones**: dominated by metal/granite/slate/
  laser-engraved wood for weather exposure — PLA is a wrong-material-for-use-case problem, not a
  design problem. Skip outright.

### Worth a follow-up look (thin data)
- Small personalized name-tag/plate add-ons sold alongside a purchased urn/keepsake — could pair
  with shortlist #1 or #2 as an upsell.
- Pet memorial nightlights/lithophane-style backlit portraits — came up in adjacent searches, not
  investigated in depth.

### Handoff notes for whichever idea is picked
- Paw-print stand needs a parametric/made-to-order dimension (fits the customer's specific print
  size, not one fixed size).
- Geometric urn: carry forward that ashes stay in the crematorium's sealed bag (removes the
  airtight-seal requirement) and the finish-quality bar (matte/silk filament, likely light sanding)
  both live competitors call out explicitly.

### Sources
- [Etsy: Durable Personalized Dog Urn — 3D Printed Biodegradable PLA (Weenielabpeturns, Bestseller)](https://www.etsy.com/listing/4518884203/durable-personalized-dog-urn-minimalist)
- [Etsy: Durable Personalized Pet Urn — 3D Printed Biodegradable PLA (MrYaushop)](https://www.etsy.com/listing/4544280145/durable-personalized-pet-urn-minimalist)
- [Etsy: Pet Memorial Stand with Personalized Name Plate (BuiltByPhil)](https://www.etsy.com/listing/4389416904/custom-pet-memorial-holder-personalized)
- [Etsy: Yorkie Sculpture - Low Poly Style, 3D Printed (DiDiSensei)](https://www.etsy.com/listing/1454534629/yorkie-sculpture-low-poly-style-sitting)
- [Etsy market: Pet Urn 3D Printed](https://www.etsy.com/market/pet_urn_3d_printed)
- [Etsy market: Pet Memorial 3D Printed](https://www.etsy.com/market/pet_memorial_3d_printed)
- [Etsy market: Paw Print Memorial Stand](https://www.etsy.com/market/paw_print_memorial_stand)
- [Pet Memorial Products Market Outlook Report 2026-2032 — GlobeNewswire](https://www.globenewswire.com/news-release/2026/01/16/3220372/28124/en/pet-memorial-products-market-outlook-report-2026-2032-lucrative-growth-opportunities-presented-by-personalized-design-led-offerings-that-blend-physical-and-digital-remembrance.html)
- [Pet Memorials Market Size and CAGR — EconMarketResearch](https://www.econmarketresearch.com/industry-report/pet-memorials-market)
- [7 Pet Memorial Trends in 2026 — Pawtrove Feltever](https://pawtrovefeltever.com/blogs/pet-memorial-guides/7-pet-memorial-trends-in-2026-why-more-pet-owners-are-choosing-custom-pet-replicas)
- [Foreverence Pets: 3D Printed Urns/Keepsakes — 3DPrint.com](https://3dprint.com/45593/foreverance-pets-3d-print-urn/)
