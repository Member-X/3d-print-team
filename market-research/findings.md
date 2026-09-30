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

---

## 2026-09-13 — Pet memorial urn silhouette research (competitive shape/family analysis, not a new-product screen)

**Scope note:** this is a targeted comparison task, not the standard Phase-1/Phase-2 autocomplete sweep — invoked to check our in-progress `pet-memorial-urn` classic-vase design against the market. `pet-memorial-urn/` was read for context only (current spec: `dot_pipeline/specs.md` — Large tier, ~1579cm³ cavity, 153.5mm H, 153.9mm belly OD, dome-topped removable lid seated on a 100mm OD collar, rounded foot, no handle, no engraving area called out) — nothing in that directory was modified.

**Method note:** per the known 2026-08-25 issue, Etsy's search-box autocomplete was tested once (typed "pet urn" into the live search box) and confirmed still non-functional — the dropdown stayed on the generic "Popular right now" list regardless of input. No CAPTCHA appeared. Fell back immediately to direct Etsy URL navigation (`etsy.com/search?q=...`, `etsy.com/c/...`, `etsy.com/shop/...`) plus WebSearch for trend/forum signal, exactly as prescribed. All review counts/dates below are from real listing and shop pages fetched this session, not estimates.

### 1. Silhouette families found (with representative, cited listings)

1. **Classic thrown-ceramic vase/jar urn with separate lid (dome, semi-spherical, or flat)** — this is our design's family. Examples: [BarruntandoCeramics — semi-spherical-cover dog urn](https://www.etsy.com/c/pet-supplies/urns-and-memorials/pet-urns) (9,505 reviews, $254.95); [vitrifiedstudio](https://www.etsy.com/shop/vitrifiedstudio) — simple tapered ceramic vase shape, sold as both pet and human/infant urns, 14 years on Etsy, 29,811 total sales, 8.8k shop reviews, sizes XXS–XL at $140–$350; "Stoneware custom pet urn" by claylicious, [listing](https://www.etsy.com/listing/1268257186/stoneware-custom-pet-urn) (9,498 reviews); AmanitaPottery — same base jar shape reused across floral/orange-cat/bunny variants (6,340 reviews each); [Weenielabpeturns](https://www.etsy.com) "minimal and elegant design, made in Italy" (Bestseller tag). A distinctive hybrid within this family: [SkyUrns](https://www.etsy.com/shop/SkyUrns) — bottom half is the ash chamber (filled via a bottom rubber plug, no top lid at all), top half is a real, usable flower vase, joined by a wood disk. 9 years on Etsy, 3,646 sales, 5.0★/1,108 reviews, reviews dated through **Sep 2026** (still actively selling), sustained $123.75–$165 price point.

2. **Wood keepsake/memory box** (rectangular box, engraved-photo lid or inset photo tile) — by far the largest number of distinct competing shops: WagsandWillows ([shop](https://www.etsy.com/shop/WagsandWillows), flagship listing 9,844 reviews), plus a long tail — WoodHandicraftsStore, APEXCRAFTSIN, NashraCraft, EngravedBelovedImage, HarmonyHubGift, PiecesOfHearts, TreeTopUrns, Bharatwoodencrafts, WoodaynaKrafts, PurestShelter, MainelyUrns, TwistedBranchDesigns — clustered at $18–$95 (most $30–$50) with heavy 25–70%-off discount patterns typical of a commoditized segment.

3. **Ceramic jar/urn with a sculpted pet figurine on the lid** (decorated variant of #1): [ThienCeramicArtShop](https://www.etsy.com/shop/ThienCeramicArtShop) "Handmade Memorial Urn with Dog/Cat Figurine" (Bestseller tag, only 1 year on Etsy but 2,091 sales / 4.9★ / 303 reviews already — fast-growing); HeartprintsbyPets (219 reviews, "Stone Finish Tribute"); PetPawsMemory (Bestseller tag).

4. **Full pet-statue/sculpture urns** (entire body sculpted into a recognizable dog/cat pose): PulvisArtUrns "Custom Cat Statue Urn from Photo" ($522.03, bespoke pricing); CozbaySculptures "Sleeping Cat Shaped Ceramic Pet Urn"; StowMillsShop "Sleeping Tabby Cat Urn." Real family, but each is a one-off hand-sculpted commission.

5. **Paw-print-engraved cylindrical canister, threaded screw-on lid**, slate/pewter finish: ["Paw Print Pet Cremation Urn, Slate Finish"](https://www.etsy.com/listing/1074466791/paw-print-pet-cremation-urn-slate-finish) (Small 6"/45cu·in, Medium 7"/85cu·in, Large 8.5"/115cu·in) and ["Classic Paw Print Pet Crimation Urn"](https://www.etsy.com/listing/798673528/classic-paw-print-pet-crimation-urn). The paw print is surface decoration on a plain tapered-cylinder body, not a body-shape feature.

6. **Photo-frame/shadow-box hybrid**: LifeSongMilestones "UV-Printed Cremation Shadow Box Urn"; PawsPortraitsGoods "Personalized Metal Dog Urn... Custom 3D Pet Portrait" (Bestseller, $29.99) — metal box with an embossed photo relief.

7. **Angel/religious motif** — present (CROSSBODYCASE "Angel Wings Pet Urn," $16) but no evidence of a major established shop in this style specifically; thin data.

8. **Heart-shaped urns** — found almost entirely at jewelry/mini-keepsake scale (cremation pendants, palm-sized token-ash keepsakes: [heart_shaped_pet_urn market](https://www.etsy.com/market/heart_shaped_pet_urn)). The one full-capacity heart urn found, [Heart Shaped Pet Urn, Laser Engraved](https://www.etsy.com/listing/1372270586/heart-shaped-pet-urn-laser-engraved), caps at **22 lbs** — well under our 50–90lb target, suggesting the heart silhouette doesn't scale volume-efficiently to large-pet capacity.

9. **Explicitly "3D printed"-labeled urns** — a small, low-price niche: TailoredPetGifts ($49.87), FoamyBloom ($75.99), CustomCharmLab ($42.49), VoxelForge3D-style listings (~$27–36 per [pawprintmemorials.com](https://pawprintmemorials.com/3d-printed-pet-urn-designs/)). No large review counts found for any of these — small/new shops, and prices sit well below the $88–$350 ceramic-vase range.

10. **Geometric/faceted "modern decor" style** — searched for directly; no meaningful pet-urn-specific presence found (this trend shows up in general human-urn/home-decor searches, not pet urns specifically). Flagging as **unconfirmed**, not a real family here.

### 2. Which families sell best / competition level

- **Classic ceramic vase (#1) and wood box (#2) are the two dominant, highest-demand families** — both have flagship listings in the 8,000–10,000-review range, and review dates (checked directly on SkyUrns' shop page) run through **September 2026**, so demand is current, not historical residue.
- **Nuance on #1:** Etsy's dedicated ["Pet Urns" category](https://www.etsy.com/c/pet-supplies/urns-and-memorials/pet-urns) shows only **286 total listings** — a fairly narrow, curated category, not "dozens of near-identical listings." But it's dominated by roughly half a dozen extremely established shops (vitrifiedstudio: 14yr/29.8k sales; claylicious; WagsandWillows; BarruntandoCeramics; AmanitaPottery; ZuzeCeramics; Crystallinekingdom) with hundreds-to-thousands of reviews each. That's "moderate listing count, very high incumbent trust" — different from, and arguably harder to break into than, a flooded low-quality category, because a new plain/undecorated entrant has no reviews to compete on trust.
- **#2 (wood box) has a much longer tail of distinct sellers** at compressed prices with heavy blanket discounting — classic race-to-the-bottom signature. Worse opportunity despite decent demand.
- **More promising, less crowded niches:**
  - The **SkyUrns-style vase-hybrid** (#1 sub-variant) — only one major seller identified, sustained $123–165 pricing, still-current reviews.
  - **Figurine-topped ceramic urn** (#3) — ThienCeramicArtShop is only 1 year old and already at 2,091 sales/Bestseller — shows room for new, well-differentiated entrants in this family.
  - **Paw-print engraved plain-cylinder canister** (#5) — quieter niche, no mega-shop review counts found, simple non-photorealistic aesthetic.
  - **Small-animal (rabbit/guinea pig/hamster) sizing** — same wood-box shape just relabeled/resized smaller; a capacity/marketing niche, not a new silhouette, but a real underserved tier if extending our line downward.
  - **"3D printed"-labeled urns** — low review counts and low prices are a **caution flag**, not an opportunity: explicitly branding as "3D printed" currently reads as budget/commodity to buyers, capping price well below the ceramic ceiling.
  - **Heart-shaped and full pet-statue families are effectively ruled out** for a 50–90lb design: hearts don't hold enough volume at that scale, and statue urns are a bespoke hand-sculpting business model.

### 3. Recurring proportions/features

- **Lid style:** dome/semi-spherical separate lid (matches ours) is common in the premium ceramic tier; flat lid with a figurine standing on it is very common; threaded screw-on lid shows up specifically on the paw-print metal/slate canister family; SkyUrns' bottom-plug (no top lid) is a rarer, differentiated alternative that also lets the object read as ordinary home decor rather than a funeral object.
- **Base:** simple turned pedestal/foot ring across nearly every ceramic-family competitor — matches our existing rounded-foot approach; no trend toward unusual base treatments.
- **Engraving/nameplate area:** essentially universal — a name+date engraving, inset plaque, or photo tile appears on nearly every top listing across every family. **Our current spec has none called out** — this reads as a real gap versus market baseline, not just a nice-to-have.
- **Handles:** not observed on any pet-specific ceramic-vase competitor — confirms our no-handle choice is correct for this category.
- **Size tiers / weight breakpoints:** the ~1 cubic inch of internal volume per pound of body weight convention (matching our own project's rule) recurs across listings. Common breakpoints seen: small ≤~20lb (40–50cu·in), medium ~20–50lb (75–85cu·in), large ~50–100+lb (110–115+cu·in) — closely matching our existing Small/Medium/Large tiering.
- **Price points per tier:** ceramic-vase family ~$60–140 (small/medium) up to $140–$350 (large/premium, vitrifiedstudio's largest tier is $350); wood-box family $18–$95 (most $30–50); figurine-topped ceramic $60–$160; full statue sculptures $95–$520+ (bespoke); "3D printed"-labeled $27–$76.

### 4. Printability notes per family

- **Classic ceramic vase/dome-lid (our family):** geometrically fine on FDM (large-radius curves, no fine overhangs beyond the neck-to-collar transition already handled in the existing spec at ~47° — within printable range). **The real risk is surface finish, not geometry** — buyers here are conditioned to expect glazed/hand-painted ceramic texture; an unfinished PLA print will look visibly "printed" next to $88–$350 pottery competitors unless we budget for finishing (sanding, primer, paint, or a two-tone/silk filament) as a real cost/time line item.
- **Wood box:** poor FDM match — competitors win specifically on real wood grain and laser-engraved photos, hard to replicate credibly in plastic without extra steps (wood-fill filament, actual laser engraving, inset photo panel). Already low-margin/high-competition regardless — not recommended.
- **Figurine-topped urn:** vessel body is printable; the custom-sculpted figurine is the hard part (needs a photo-to-3D pipeline or a limited generic-breed library) — real labor/scalability cost for a solo shop.
- **Full statue urns:** not realistic for a solo FDM shop at the hand-sculpted quality/personalization level these competitors deliver — out of scope.
- **Paw-print threaded canister:** very FDM-friendly — plain body of revolution, printable threads (or heat-set insert), no fine overhangs, easy two-tone via a filament swap for the paw band.
- **Vase-hybrid (SkyUrns-style):** printable as 2–3 separate simple parts, arguably *easier* than our current dome-lid design (no dome to support, bottom-plug access instead), and differentiates by not visually reading as an "urn."
- **Heart/shadow-box hybrids:** geometrically fine but low priority — heart doesn't scale to our capacity target, shadow-box relies on inserted photo materials that add a manufacturing step beyond pure FDM output.

### Handoff

Core vase silhouette is validated, not disproven — no shape change forced. The clearest, lowest-effort gap versus market baseline is the missing engraving/nameplate area (near-universal across every competing family). Two adjacent ideas worth a decision before the next spec revision: the SkyUrns-style bottom-fill/open-top vase hybrid (simpler print, no dome overhang, only one major competitor), and a plainer engraved-band cylinder in the paw-print-canister style (plays to FDM's strengths instead of chasing a ceramic look). Heart-shaped and full-statue families are ruled out for the 50–90lb target. Next step once a direction is chosen: `3d-director` (or `3d-planner` directly) to fold the decision into the spec.

### Sources
- [Pet Urns category](https://www.etsy.com/c/pet-supplies/urns-and-memorials/pet-urns)
- [SkyUrns shop](https://www.etsy.com/shop/SkyUrns)
- [ThienCeramicArtShop](https://www.etsy.com/shop/ThienCeramicArtShop)
- [vitrifiedstudio](https://www.etsy.com/shop/vitrifiedstudio)
- [WagsandWillows](https://www.etsy.com/shop/WagsandWillows)
- [Stoneware custom pet urn listing](https://www.etsy.com/listing/1268257186/stoneware-custom-pet-urn)
- [Heart shaped pet urn market](https://www.etsy.com/market/heart_shaped_pet_urn)
- [Heart Shaped Pet Urn (22lb) listing](https://www.etsy.com/listing/1372270586/heart-shaped-pet-urn-laser-engraved)
- [Paw Print Pet Cremation Urn, Slate Finish](https://www.etsy.com/listing/1074466791/paw-print-pet-cremation-urn-slate-finish)
- [Classic Paw Print Pet Cremation Urn](https://www.etsy.com/listing/798673528/classic-paw-print-pet-crimation-urn)
- [3D Printed Pet Urn Designs — Paw Print Memorials](https://pawprintmemorials.com/3d-printed-pet-urn-designs/)
- [3d printed pet urn market](https://www.etsy.com/market/3d_printed_pet_urn)
- [Custom 3D Printed Pet Urn listing](https://www.etsy.com/listing/1879450771/custom-3d-printed-pet-urn-personalized)
- [Pet Urn Market Size report](https://www.datainsightsmarket.com/reports/pet-urn-441268)

## 2026-09-23 — eBay competitor check: Cat Wand Toy Holder

**Method.** Own browser tab, URL navigation only (no Terapeak, no autocomplete), so none of this is search-volume data. eBay never showed a verification page. Tags: OBSERVED = seen on a page this session, INFERRED = judgment.

**Verdict.** Niche is sparse, but demand is unproven.
- OBSERVED: "cat wand holder" returns 15 active results: 7 fabric bags, 2 rigid holders (nxviii, Feline Ruff), the rest irrelevant.
- OBSERVED: sold searches for 9 holder/organizer/storage phrasings returned zero relevant exact matches. Only holder-type sale found: one fabric hanging bag at $14.38 (tingfarm, Aug 9). Dozens of wand toys sold at $8-$25.
- INFERRED: eBay buyers mostly buy wands, not storage; low competition probably reflects low demand.

| Seller | Type | Price + ship = landed | Sold evidence |
|---|---|---|---|
| steveowensjr (reference) | 3D-printed, rigid, 7 slots | $49.99 + free = $49.99 | None (listed 9/23) |
| nxviii (40 feedback) | Small white rigid holder, ~3 wands (3D-printed per a snippet, unverified) | $14.99 + $6.07 = $21.06 | None seen |
| shloruzdealz613 | Feline Ruff, mass-produced tabletop, 4 slots (per Amazon/Chewy snippets) | $50.43 + free | None seen |
| zonegood (841 feedback) | Hanging organizer, material unverified | $64 or Best Offer, free | None seen |
| ZAVOOS / theatlassupplyco | Fabric 2-packs | $34-$49, free | None seen |
| 5 sellers incl. TEMUORG, buyitshipping | Fabric bags | $11-$23, free | None seen |
| tingfarm | Fabric hanging bag | $14.38, free | 1 sold (Aug 9) |

**Price.** OBSERVED: $49.99 ranks 12th of 15 on lowest-landed sort; only Feline Ruff and zonegood cost more, neither shows sales. Highest sold holder-type price found: $14.38. INFERRED: $49.99 is untested on eBay; nearest rigid comparable asks $21 landed. Print time and eBay fees not checked.

**Keywords.** Title 68/80 chars. Surfaces for "cat wand holder", "cat toy holder wall", "cat wand wall mount"; only loose matches for "3d printed cat wand" (title lacks "3D Printed"). eBay related searches: Wand Holder, Hanging Cat Toys, Wall Mounted Cat, Cat Holder.

**Gaps.** 7 photos + Color dropdown; likely no dimension/keyhole/scale shot (INFERRED). Search results showed "0% positive (19)" and the listing "No feedback yet" (may be a display quirk). No returns vs several competitors offering free returns. eBay prompts for a seller profile photo. Fabric competitors have no rigid, colored or cat-silhouette angle.

**Suggested changes, in order.**
1. Title: "3D Printed Cat Wand Toy Holder Wall Mount Organizer 7 Slots Teaser Wand Storage" (79 chars).
2. Price: test $39.99, or add Best Offer with a floor.
3. Photos: dimension diagram (9.1 x 9.1 in), keyhole back, "7 wands loaded" shot.
4. Item specifics: add Material (PLA), Color, Size.
5. Trust: check feedback display in Seller Hub, add profile photo, consider accepting returns.

**Could not verify.** Terapeak / 1-year sold volume and sold-window length; whether nxviii's holder is 3D printed and its sales; zonegood's material and Feline Ruff's eBay dimensions; competitors' photo counts; the user's description text (did not render); whether buyers actually see "0% positive".

## 2026-09-23 — look-alike check: fish cat bowl

**Verdict.** No finished, 3D-printed, fish-shaped fishbone bowl found on Etsy or eBay (OBSERVED: 4 Etsy and 5 eBay queries, no bot checks). Exact retail source of the reference photo unidentified. Generic fish bowls (ceramic, silicone) are crowded; the rigid fish + skeleton + eye niche looks thin.

**Closest look-alikes.**
- Etsy 4558355178 (mrar97): "Fish-Shaped Cat Food Bowl STL, Dual Compartment", a $3.70 digital file (PLA/PETG, personal-use licence), 3 shop sales, no reviews. Only direct concept match, and it is a file, not a product.
- Fred/Howligans "Slow Food - Cat" (designer Lauren Hastings): molded PP, 7.6 x 4.4 x 1.3 in, 3/4 cup, $14.00 genuinefred.com (sold out) / $14.99 World of Mirth. Fish outline with raised bone; the blue photo shows no eye or head compartment.

**Near matches.** Etsy printed PLA: BoltandBuild3D 4380425937 ($14 + $9.24 ship, 637 sales), Penn3DStore 4548634244 "Campfire Fish" ($29.99 + $15), LostTravelerLee3D 1798198920 ($24.99 free ship), PalmPrintz3D 4414276513 ($23.99 + $11.50). Etsy ceramic fishbone slow feeders $35-$110. eBay active: silicone fish slow-feeder 2-packs $13-$38 (often China-sourced), ceramic tilted fish $29.84. eBay sold (about Jun 26-Sep 22): "fish shaped cat bowl" 7 exact hits mostly ceramic $7-$32 (incl. HING Fish Bowl 185123028554, $30.95 + $8.62 ship); "...slow feeder" 2 exact hits, silicone $7-$8; 5+ ceramic fish-bone tilted feeders $10-$22. No printed items sold.

**Original product.** Could not identify. Fred is closest (no eye/smile/two compartments); HING has the fish shape but no skeleton. Caution, not legal advice: fishbone-in-fish is credited design work at Fred and the photo is probably a branded product, so copying its silhouette or skeleton carries design-patent/trade-dress risk (INFERRED).

**Crowding / price.** Generic fish bowls roughly $6-$22 landed (silicone/molded). Rigid skeleton feeders: one retail brand at about $14-$15 plus one STL. Printed cat bowls on Etsy $14-$30 + $6-$15 shipping. INFERRED: a printed version would sit around $24-$32, capped by Fred at about $15 unless an eye/two-compartment layout justifies a premium.

**Flags.** (a) Food contact: layer lines can hold residue, PLA softens in hot water (INFERRED); sellers say "all PLA so it is food-safe", "certified food-grade PETG", "food-safe* filament", mostly hand-wash only. These are filament-level marketing claims, not certification of the printed part. (b) Printability: Fred-size (about 193 x 112 mm) fits a 256 mm bed; shallow skeleton and low walls likely need no supports (INFERRED); a contrasting eye would need multicolor.

**Not verified.** Photo's exact brand; Etsy review counts; Amazon (fetch errors); Walmart (human-check page, stopped); whether Fred comes in green; sold data beyond eBay's roughly 90-day window.
