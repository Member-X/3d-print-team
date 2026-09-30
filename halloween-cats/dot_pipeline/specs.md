# Halloween Cat "Pumpkin Hug" Light-Up Figurine - Technical Spec

Status: v1, 2026-09-24. Consumer: `3d-blender-modeler` (builds directly from this file + reference images). Nothing here has been modeled or test-printed.
Authority order when sources disagree: (1) requirements stated in this spec, (2) `concept/concept-a.png` front view, (3) other turnaround views (generator-invented, see section 12).

Provenance tags used in every table:
- **VERIFIED** - read from the supplier drawing `reference/light-kit-drawing.png` (re-read for this spec) or measured on a real object. No physical measurement of the real puck exists yet.
- **USER** - fixed requirement given by the user.
- **MEAS-IMG** - measured from `concept-a.png` (an AI concept, not a physical object). This is ESTIMATED by definition.
- **DERIVED** - calculated from other rows. **ASSUMED** - convention or guess, needs checking (each is listed in section 13).

## 1. Product summary and intended lit result
A chubby black cat sits upright hugging a jack-o'-lantern on a round base. The figure is one hollow print. A removable USB LED puck sits in a pocket in the underside of the base, lit face up, and floods one shared black-walled chamber (base plenum, torso, head, pumpkin) with light.
Lit result: light escapes ONLY through six thin yellow windows: the cat's two eyes (yellow ring around an opaque black pupil) and the pumpkin's two eyes, nose and mouth. The orange pumpkin shell, black cat, base, pink nose/mouth and green stem stay opaque. Cat eyes will be dimmer than the pumpkin face (accepted by user). No translucent filament is used: windows are thin skins (about 0.5 mm) of light yellow PLA, recessed from the inside so the outside stays smooth.

## 2. Printer constraints, material, orientation (fixed inputs)
| Item | Value | Tag |
|---|---|---|
| Printer / bed | Bambu Lab P2S, 256 x 256 x 256 mm (web-confirmed spec) | VERIFIED (vendor) |
| Nozzle | 0.4 mm (P2S standard; user has not confirmed which is installed) | ASSUMED |
| Layer height | 0.20 mm (assumed; user's "2-3 layers = 0.4-0.6 mm" implies it) | ASSUMED |
| Filament / AMS | PLA, 5 colors (black, orange, yellow, green, pink); user has 8 AMS slots | USER |
| Min wall under load | >= 2 x nozzle = 0.8 mm. Modeled walls: 2.0 mm cat/base, 3.0 mm pumpkin; min feature 1.2 mm (window skins excepted) | DERIVED |
| Material reason | PLA: user default, prints all 5 colors on the AMS, indoor decor with a cool LED. Use the palest, most translucent yellow PLA available (window colour); matte black. | - |

**Orientation:** print upright, exactly as modeled (Z up). Bed-facing face = the flat underside of the base (Z = 0). Reasons: largest flat face; the puck pocket opens downward so the puck loads from the bottom as required; the figure needs no rotation in the slicer; head/ears/stem build in the strong axis; most windows are near-vertical walls (see section 8). Export already in print orientation, bottom at Z = 0, centered on X/Y.

## 3. Files to produce (project root `H:\ClaudeStuff\3d-print-team\halloween-cats\`)
- `blender/halloween-cat.blend` (save early and after every milestone; keep v1, v2 ... rather than overwrite)
- `stl/halloween-cat_black.stl`, `_orange.stl`, `_yellow.stl`, `_green.stl`, `_pink.stl`, `stl/halloween-cat_combined.stl`, and `3mf/halloween-cat.3mf` (5 named parts) if a valid multi-part 3MF is possible
- `stl/skin-calibration-tile.stl` (section 8.3), `stl/base-fit-coupon.stl` (optional but strongly recommended, section 6.4)
- `parameters.md`: every named parameter in section 5/6/8 with its final value (build parametrically, at minimum SKIN_T_CAT, SKIN_T_PUMPKIN, POCKET_D, TAB_ENGAGE, APERTURE_D, TUNNEL_W/H, WALL_CAT, WALL_PUMPKIN, so a revision is a re-run, not a rebuild)
- Non-exported reference dummies in the .blend: `REF_puck` (cyl 60 x 8 + ring dummy 50 dia x 3 mm on the lit face), `REF_cable_4` and `REF_cable_5` (4 and 5 mm dia), for clearance checks.
- Build report per `3d-blender-modeler` rules, including cross-section screenshots through the puck pocket, neck, and each window.

## 4. Coordinates and measurement method
Origin: center of base underside. +Z up. The cat faces -Y (Blender numpad-1 front view). +X = image right in `concept-a.png` = cat's left = tail side. +Y = back; the cable tunnel exits at +Y. Figure is mirror-symmetric about X = 0 except the tail.

Method for all MEAS-IMG values: `concept-a.png` (1024 px square) is a front view from about 13 deg above level (base ellipse minor/major about 145/650 px). Ear tips at y about 85 px, base front-bottom edge y about 965 px, base width about 650 px, concept base about 45 px (about 8 mm) thick. Solving "150 mm = ear tip to base bottom" with that foreshortening gives about 5.52 px/mm for the concept as drawn, and a base width of about 118 mm. The required base is 16 mm, not 8, so the figure above it is scaled (150-16)/(150-8) = 0.944, giving **figure features: mm = px / 5.85** horizontally. I read pixel positions by eye (no image-analysis tool was available): treat every MEAS-IMG value as about +/-2 mm horizontally and +/-3 mm vertically (perspective tilt shifts frontal features). Front-view silhouette overlay against the concept (criterion A12) is the final judge.

## 5. Dimension table
| Item | Value (mm) | Tag / how |
|---|---|---|
| Overall height, Z0 to ear-tip top | **150.0** | USER |
| Base | dia **120.0** x **16.0** high (top edge fillet 1.5, bottom edge chamfer 0.6 for elephant foot) | DERIVED: concept base about 118 dia; 120 leaves 29 mm ring around the pocket for tabs/tunnel and 5.5 mm margin beyond the 109 mm arm span. 16 = 11.0 pocket + 2.0 shelf + 3.0 plenum (section 6) |
| Puck | dia **60.0** x **8.0** thick | VERIFIED (drawing; caliper check requested) |
| Puck ring (lit face) | inner concentric circle about 48-50 dia, about 5 mm inside the rim; height NOT shown (side view hints at a step about 3 mm from one face) | ASSUMED, unverified, named risk R1 |
| Puck back holes | 3 holes, outer pair 28 apart | VERIFIED, ignored per user |
| Cable | dia **4.0** assumed (drawing stroke looks nearer 5); leaves puck RIM radially, height on rim not shown; 705 + 45 (switch box) + 740 = 1490 total | dia ASSUMED (user to measure); lengths VERIFIED (sum checks) |
| Figure width (arms) | 109 | MEAS-IMG (640 px) |
| Head | ellipsoid-like, W 84 x D 66 x H 52; center (0, +14, 113); z 87 to 139 | MEAS-IMG (492 px wide; y 148-445 px; depth from side views) |
| Ears | tips at x = +/-36, top at z = 150.0; base 28 wide; outer edge about 24 tall; tip radius >= 2.5; thickness >= 6 at mid-height; **solid** | MEAS-IMG + brief (blunt tips) |
| Torso | egg/gumdrop, widest about z 40, W about 92, y -20 to +52, top (shoulders) about z 100 | ASSUMED blocking, front view rules |
| Paws | about 20 W x 22 H x 26 D, centers x = +/-43, z about 62; arms are thick tubes shoulder to paw, **solid** | MEAS-IMG |
| Hind feet | mitten, about 25 W x 28 D x 22 H, centers x = +/-36, y about -22, sitting on base deck; **solid** | MEAS-IMG (depth ASSUMED, side views disagree) |
| Tail | thick curl on +X side, low, tube dia >= 18, entirely inside base footprint (r <= 57); **solid** | ASSUMED (views disagree) |
| Pumpkin body | ellipsoid W **87** x D **80** x H **70**, center (0, -15, 51), bottom z = 16 (on deck), top z = 86; front-most point 5 mm inside base edge (y = -55) | W,H MEAS-IMG; D ASSUMED (side views disagree) |
| Stem | 14 tall (z 82-96), top dia 11, base dia 16, solid, may fuse <= 2 mm into chin; top must stay >= 3 mm below mouth line | MEAS-IMG |
| Pumpkin ribs | optional; <= 1.0 deep; must fade out within 2 mm of any window | ASSUMED (brief allows smooth) |
| Cat eyes (yellow ring) | outer dia **17.5**, centers x = +/-17, z about 115 | MEAS-IMG (101 px) |
| Cat pupils | dia **8.0** concentric, black | MEAS-IMG (45 px), min 6 |
| Cat nose (pink) | rounded triangle, apex down, 8.5 W x 6.5 H, center (0, z about 111), inlay depth 1.0 | MEAS-IMG |
| Cat mouth (pink) | smile/"w" arc about 22 W, sag about 3, centered z about 104, **line width 1.6** (min 1.2), depth 1.0 | shape MEAS-IMG; width ADJUSTED (concept about 0.9 mm) |
| Pumpkin eyes | rounded triangles apex up, 16 W x 15 H each, corner r >= 2, centers x = +/-16.3, z about 67 | MEAS-IMG |
| Pumpkin nose | rounded triangle apex up, 9 W x 8 H, center (0, z about 57.5) | MEAS-IMG |
| Pumpkin mouth | wide grin, 52 W x 19 H, center (0, z about 46), corners up; 3 chunky square orange teeth (2 hanging from top edge, 1 rising from bottom edge, each >= 6 W x 4 H) | MEAS-IMG |

Blockout above is guidance; the front view is authoritative. Exact contours are the modeler's call so long as criteria A1-A14 pass.

## 6. Base and light-kit interface
Vertical stack at the puck (Z from bed, all DERIVED unless noted):

| Feature | Value |
|---|---|
| Pocket | dia **POCKET_D = 61.2** (60 puck + 1.2 total: about 0.3 fit + 0.3 for printed holes coming out small), from Z 0 to **11.0**; 0.6 mm x 45 deg entry chamfer |
| Puck seat | puck back face rests on tab tops at **Z 2.4**; front (lit) face at Z 10.4; **0.6 mm vertical slack** to shelf underside at **Z 11.0** |
| Shelf | Z 11.0-13.0 (2.0 thick), inner edge = light aperture; pocket top corner chamfered 0.8 x 45 deg so the shelf overhang is <= 4 mm and self-supporting |
| Light aperture | dia **APERTURE_D = 54** through the shelf (covers the estimated 48-50 ring with about 2 mm clearance; shelf still overlaps the puck rim by 3 mm) |
| Plenum | dia 54 bore continuing up from Z 13.0 through the base deck (Z 16.0) into the figure chamber. It gives >= 3 mm above the puck face for a raised ring (ring height unknown). May flare (widening upward) to improve connectivity. |

### 6.1 Retaining lip (3 snap tabs)
Three tabs at **60, 180, 300 deg from +Y** (none at the tunnel). Each tab: 9 mm chord, radial protrusion from pocket wall to r = 29.1 (**TAB_ENGAGE = 0.9** over the puck rim at r = 30), Z 0 to 2.4, flat top face (retains the puck), lower face a 45 deg lead-in ramp (self-supporting, lets the puck push past). Rigid PLA tabs will not let a 60 mm puck past, so each tab sits on the free end of a tangential **flex arm**: arm 1.6 mm radial x 4.0 tall x about 14 long, curved to the pocket wall, fixed at one end, isolated by a 1.2 mm arc slot on its outer side and a 0.8 mm relief gap above (slot open to the bed face). If the modeler judges the arm impractical, fall back to rigid tabs with TAB_ENGAGE = 0.6 and report; the fit coupon decides (6.4). Puck must be insertable and removable by hand without tools.

### 6.2 Cable tunnel
Groove in the underside of the base along +Y from the pocket wall to the base edge (about 29 mm long), **TUNNEL_W = 7.0 wide x TUNNEL_H = 10.0 high** (Z 0-10; v1.1 amendment, was 8.0), open to the bed face, ends open at the base edge, top corners chamfered 45 deg so the roof needs no support. Sized so a 4-5 mm cable leaving the puck rim at mid-thickness (Z about 6.4; a 5 mm cable then spans Z 3.9-8.9) passes with margin. The roof above the tunnel is 6 mm thick. The cable lies on the table in the groove, so the figure sits on the full base ring: contact = annulus dia 61 to 120 minus the 7 mm groove, plus tab bottoms. The 45 mm switch box and USB plug never enter the base (cable only).

### 6.3 Leak notes
Puck edge light may seep through the 0.6 mm slack into the pocket and out the tunnel or under the base. Accepted (faint, at table level, back of figure). Not a reason to add geometry.

### 6.4 Base fit coupon (optional, recommended, cheap)
`base-fit-coupon.stl`: a 90 dia x 16 mm cylinder (black) containing exactly the pocket, tabs/arms, shelf, aperture and tunnel at the same coordinates. About 1 h print. The user checks puck insertion/removal, tab hold and cable exit BEFORE committing to the full print. This targets the highest-risk mating dimensions (R1, R2).

## 7. Hollow geometry
- **Hollow only:** torso, head, pumpkin, plenum. Ears, arms, paws, feet, tail, stem and the base outside the pocket/tunnel/plenum are **solid volumes** (slicer infill handles them).
- **One connected void.** Chamber = union of: plenum, torso cavity (offset of torso envelope inward by WALL_CAT = **2.0**), head cavity (2.0), pumpkin cavity (offset of pumpkin envelope inward by WALL_PUMPKIN = **3.0**, measured at rib valleys if ribs exist), and a neck bore. Shell = outer envelope minus chamber. No other openings (chamber opens only through the puck pocket).
- **Minimum connections:**
  - Neck opening (head to torso) at the seam plane **z = 93 +/- 3**: >= 40 mm (X) x 30 mm (Y), area >= 940 mm2.
  - Plenum to pumpkin cavity: >= 900 mm2 and >= 30 mm in the smaller dimension. Plenum to torso cavity: same.
  - Pumpkin-to-torso overlap is large by design (pumpkin back half tucks into the belly); keep it >= 1500 mm2.
- **Wall rules:** black walls >= 1.8 mm everywhere except windows (nominal 2.0); orange >= 2.8 (nominal 3.0). Thicker is allowed where needed for self-supporting ceilings, never thinner.
- **Interior finish:** smooth, no ribs, bosses or steps, so the user can spray it white or foil-line it later.
- **Self-supporting interior (no supports can be removed inside).** Angles measured from vertical: prefer <= 45 deg; up to 60 deg allowed; anything flatter is a bridge and must span <= 30 mm (pumpkin roof) / <= 20 mm (head roof) / <= 10 mm elsewhere. Do this by shaping ceilings as truncated cones/pointed teardrop vaults (thickening the shell above them), not domes. Head interior: keep vertical-ish walls to about z 120, then 45 deg flanks to a flat roof <= 20 mm wide, under the 139 mm outer top. Any ellipsoid cap flatter than 45 deg over more than 30 mm across must be replaced by a cone. Report each ceiling's angle/span from cross-sections.
- **No undercuts at the base:** every form meeting the deck (torso, feet, pumpkin, tail) either goes vertical or tapers inward at <= 45 deg from vertical near the deck. Prefer blending the pumpkin underside into the deck with a 45 deg tangent skirt so it needs little or no support; the crease between pumpkin, paws and feet is where supports are expected.
- **Seams for a later split (no geometry needed beyond this):** keep a visible concave crease at the neck (head over shoulders, seam plane z = 93) and along the pumpkin-to-arm/torso junction, and the large openings above, so a cut at those planes gives clean open shells.

## 8. Light windows

### 8.1 Rules
- Six window regions, all **yellow**: W1/W2 cat eyes (annulus dia 17.5 outer around the dia 8 pupil), W3/W4 pumpkin eyes, W5 pumpkin nose, W6 pumpkin mouth. Nothing else transmits.
- Skin thickness: **SKIN_T = 0.5 mm target, tolerance 0.40-0.60**, measured along the local outer-surface normal. Separate params SKIN_T_CAT and SKIN_T_PUMPKIN (both 0.5) so the dimmer cat eyes can be thinned later.
- Construction: keep the outer surface smooth and continuous. Window outline is defined as a 2D shape in the front (X,Z) plane, projected along Y onto the outer surface. Remove **all** material between the skin and the chamber inside that outline (pocket depth = wall - skin: 1.5 mm cat, 2.5 mm pumpkin; deeper if the shell is locally thicker). Nothing but the skin may remain in the light path.
- Pocket flanks flare **45 deg** (opening toward the chamber) on all sides so the pocket roof is self-supporting and light spreads. Consequence: teeth and webs taper inward; keep the orange web between any two windows >= 4 mm at the outer surface and every yellow gap >= 3 mm wide at the outer surface.
- **Pupils (v1.2 amendment, replaces the v1 plug):** NO plug. Each pupil is a black disc, dia 8.0 at the outer surface, that is part of the SAME thin window skin: same thickness SKIN_T, flush with the outer surface, sharing the skin plane with the yellow ring, with a crisp circular boundary and no material behind it (the pocket behind the whole eye disc, dia 17.5, is cut as one). The user rejected the v1 floating plug. A 0.5 mm black skin is nearly opaque but may pass a faint glow; the user can check this by printing the skin tile in black. If more opacity is needed, add a black backing boss (dia 8, up to 0.7 mm thick, 45 deg flank) on the inner face of the pupil skin. Do not add spokes unless the user asks.
- Yellow part = skin patches only; window edges meet the black/orange parts with no gap or overlap (section 9).

### 8.2 Slicer reality (important, changes the user's mental model)
The "2-3 layers" idea holds only for near-horizontal skins. Cat eyes and most pumpkin windows are **near-vertical walls**, where thickness is set by perimeter width, not layers: a 0.5 mm skin prints as ONE wall loop (about 0.42-0.45 mm), and the slicer needs "detect thin wall" (Bambu Studio, Strength > Advanced) on or it may drop or double it. Under 0.4 mm risks holes; 0.8-0.9 mm (two loops) will look dim. Modeled 0.5 mm is therefore right for both cases, but the calibration tile (8.3) must be printed in both orientations.

### 8.3 Calibration tile (`skin-calibration-tile.stl`, yellow)
Plate 60 x 34 x 2.4 mm. Four pockets 11 W x 22 H cut from the back at x = -21, -7, +7, +21 (45 deg flanks), leaving skins **0.40, 0.60, 0.80, 1.00 mm** (= 2, 3, 4, 5 layers at 0.2 mm); 1-4 raised dots (dia 1.6 x 0.4) on the front face above each pocket to identify them. Integral L-foot (60 x 10 x 3 mm) on the back bottom edge so it can stand. **Print A, standing:** skins are perimeter-limited, the real cat-eye case. **Print B, flat, front face down:** skins are the first 2-5 layers. The user lays each on the lit puck in a dim room, picks the thickness, and sets SKIN_T_* for the final build.

## 9. Part / color plan (AMS: 5 of 8 slots)
| Part (mesh name) | Filament | Contents | Expected shells |
|---|---|---|---|
| `black` | black | base, torso, head, ears, arms, paws, feet, tail, cat pupils | 3 (body + 2 pupils) |
| `orange` | orange | pumpkin shell (3 mm), incl. teeth and webs | 1 |
| `yellow` | light yellow | 6 window skins | 6 |
| `green` | green | stem (outside the pumpkin envelope) | 1 |
| `pink` | pink (DEFAULT, user can change) | cat nose and mouth inlays | 2 |
Viewport colors: black #111111, orange #FF6A00, yellow #FFE01A, green #2E8B2E, pink #FF6FA3.
- **Tile by construction:** build ONE watertight master shell (envelope minus chamber, windows/pockets already cut), then split it with disjoint zone volumes (priority: paws/arms/feet/tail/base/torso/head/ears black > pumpkin orange > stem green; windows yellow and inlays pink override). Each part = master shell intersect its zone. No gaps, no overlaps.
- Pink inlays are flush (or a dome <= 0.8 mm), 1.0 mm deep in the 2.0 mm wall, so >= 1.0 mm black remains behind them and no light passes.
- Boundaries are crisp on the outer surface; color regions stay flat (no gradients, no texture).
- Orange part must never be reachable from a chamber-side line of sight through less than 2.8 mm.

## 10. Supports, first layer, bed fit
- **Internal supports: none allowed** (section 7).
- **Expected external supports** (tree/organic, touching model, user's slicer): under paw/forearm undersides where they overhang the pumpkin bulge or deck; the pumpkin lower flank/crease beside the feet (reduced by the 45 deg skirt); under the chin/head front where it overhangs the pumpkin shoulder; under the tail curl if it lifts off the deck. **Not expected:** ears (outer edge vertical, no underside), stem, tunnel roof (chamfered), tab ramps, pocket shelf (<= 4 mm chamfered ledge), window pockets (flared). If the shelf droops in the coupon, allow supports inside the pocket only (reachable from below).
- **First layer:** annulus dia 61-120 (minus 7 mm groove) plus tab feet. Expect slight elephant foot at the pocket mouth; the 0.6 mm chamfers absorb it. Do not put anything fragile on layer 1 except the 3 tab feet (each attached to the pocket wall).
- **Bed fit:** footprint 120 x 120 (tail inside r <= 57), height 150; bed 256 x 256 x 256. Leaves about 68 mm each side for prime/purge tower. Passes with large margin.

## 11. Measurable acceptance criteria
| ID | Check | Pass |
|---|---|---|
| A1 | Bounding box | Z min = 0.00 (bottom flat within 0.01); Z max = 150.0 +/- 0.5; X,Y extents <= 120.3, centered within 1 mm |
| A2 | Base | dia 120.0 +/- 0.2, top deck at z = 16.0 +/- 0.2 |
| A3 | Pocket | dia 61.2 +/- 0.1, depth 11.0; shelf underside z = 11.0, aperture dia 54 +/- 0.2; 3 tabs at 60/180/300 deg, engagement 0.9 +/- 0.1 (or 0.6 fallback, stated); tab top z = 2.4 |
| A4 | Dummy fit | `REF_puck` at z 2.4-10.4 intersects the shell only at the tabs; ring dummy (dia 50 x 3 above face) intersects nothing; `REF_cable_5` runs from the puck rim (exit z anywhere in 4.5-7.5, mid-thickness 6.4 expected) along +Y out of the base with zero intersection |
| A5 | Tunnel | 7.0 x 10.0 +/- 0.2, reaches the base edge at +Y; base still rests flat (deck contact annulus intact) |
| A6 | Chamber | Exactly one connected void (excluding pocket/tunnel); neck opening >= 40 x 30 and >= 940 mm2 at z = 93 +/- 3; plenum-pumpkin and plenum-torso >= 900 mm2 each; no internal feature protrudes into the void |
| A7 | Walls | Ray/thickness probe >= 500 points: black >= 1.8, orange >= 2.8 (excluding windows); report min and median |
| A8 | Windows | Exactly 6 yellow shells; skin 0.40-0.60 mm at >= 5 points per window (center + 4 edge points), reported per window; no material other than skin between window outline and chamber; pumpkin windows sit on smooth (rib-free) surface |
| A9 | Pupils (v1.2) | dia 8.0 +/- 0.3, flush with the outer surface, thickness = SKIN_T (0.40-0.60) measured at >= 5 points; no plug or free-standing piece behind it; nothing yellow inside the pupil outline; pupil and yellow ring share one skin plane |
| A10 | Parts | Each part manifold (0 non-manifold edges, 0 self-intersections); shell counts per section 9; sum of part volumes = combined volume within 0.1%; pairwise part intersections < 0.1% of the smaller part |
| A11 | Inlays and features | pink mouth line 1.6 +/- 0.2 wide, both pink inlays 1.0 +/- 0.1 deep; ear tip radius >= 2.5; all features >= 1.2 mm; stem top >= 3 mm below mouth line; pumpkin teeth >= 6 W x 4 H |
| A12 | Silhouette | Front orthographic silhouette overlaid on `concept-a.png` (scaled per section 4): head W 84 +/- 3, pumpkin W 87 +/- 3, arm span 109 +/- 4, cat eye centers x = +/-17 +/- 1.5, both ear tips within 3 mm of the concept; deviations explained |
| A13 | Interior overhang | Every internal ceiling face <= 60 deg from vertical, except listed bridges within span limits (section 7); table of exceptions in the report |
| A14 | Tile | four skins 0.40 / 0.60 / 0.80 / 1.00 +/- 0.02, measured; bed-fit check assertion for the figure |

## 12. Concept conflicts and turnaround disagreements
Conflicts with the user's requirements (front view was NOT followed here):
1. Concept base is about 8 mm thin disc; required 16 mm base with pocket. Figure scaled 0.944 to keep 150 mm.
2. Cat eyes are chartreuse in the concept; they must be yellow to glow. Keep the shape and black pupils.
3. Cat mouth is a thin (about 0.9 mm) black line on black. Becomes a 1.6 mm pink line. Pink is a default the user can change.
4. Concept is solid; the product is hollow with thin-skin windows. Pumpkin carving is not a raised/inset color patch but the six windows.
5. Concept tail slightly overhangs the base in front and back views; keep it inside the base.
6. Ear tips are fragile in the concept; blunt (r >= 2.5) and thicken.
7. Concept stem touches the chin/mouth; keep the mouth line clear.

Turnaround views (front wins; all generator-invented): pumpkin depth differs between side views (about 270 px vs about 370 px in front of the belly) -> D = 80 assumed, front-most point 5 mm inside the base edge (side views say 1.5 mm and 7 mm). Tail shape differs in every view -> one thick tail on the +X side. Side views wrap eyes/nose onto the cheek and show no yellow on the pumpkin; keep features on the front only. Top view shows a yellow sliver at the pumpkin's front rim and wing-like ears; ignore both. Left/three-quarter views show a slimmer tail and a rump bump; ignore.

## 13. Edge cases, risks, open items
**Three design edge cases**
1. Real puck or ring differs from the drawing (dia 60 +/- tolerance, ring OD/height unknown). Handled by 0.6 mm per side pocket margin, 54 aperture, 3 mm plenum height above the face. If the ring is taller than 3 mm or wider than 52, revise APERTURE_D / plenum.
2. Cable thicker than 4 mm or leaving the rim at a different height. Tunnel 7 x 10 covers a 5 mm cable exiting anywhere in Z 4.5-7.5. A higher exit, thicker or stiffer cable: revise TUNNEL_W/H.
3. Wrong glow: orange or black leaks light, or yellow windows too dim/hot. Tune SKIN_T_* from the tile; for orange leakage, spray the interior black (or request a black inner liner variant of the pumpkin, still 5 filaments); a white or foil lining brightens windows but also raises leak risk, so re-test.

**Named risks (all unverified numbers are ESTIMATED)**
- R1 (highest): puck ring height/OD, puck true diameter and tolerance. Only the 60 x 8 body is drawn. Need caliper values or a ruler photo.
- R2: snap arms may be too stiff/weak in PLA; validate on the coupon.
- R3: cable diameter (assumed 4 mm) and exit height on the rim.
- R4: layer height 0.2 assumed; 0.4 mm nozzle assumed; Bambu "detect thin wall" behavior on 0.5 mm skins is unverified (web guidance only says thin walls below about two line widths fall back to a single loop).
- R5: puck brightness/lumens unknown; whether yellow at about 0.45 mm glows enough, and whether 3 mm orange stays dark, cannot be known before the tile test.
- R6: all figure proportions are read by eye from an AI concept (+/-2-3 mm); pumpkin depth, tail, foot depth are guesses.
- R7 (v1.2): the pupil is now a flush black disc in the thin skin. Remaining risks: faint light leaking through 0.5 mm of black, and the bond between the pupil disc and the yellow ring (side by side in the same layers, normal multi-color adjacency).
- R8: large flat-ish pumpkin roof (bridge up to 30 mm) may sag inside; unfixable after printing, hence the cone-ceiling rule.
- R9: five-color AMS print with many color changes wastes filament and time; not controllable here.
- Heat: USB puck is low power, PLA softens around 55-60 C; check the base after a long run.

## 14. Questions for the requester
1. **Slicer settings:** layer height (spec assumes 0.20 mm) and infill (suggest 10-15% gyroid, 3 walls, "detect thin wall" on, tree supports touching model)? Any change moves the skin math.
2. Please measure the real puck with calipers (or a ruler photo): diameter, thickness, ring OD and how far the ring stands proud, and the cable OD and where it exits the rim (height above the back face). Also confirm the installed nozzle is 0.4.
3. Which yellow PLA (brand/shade) will be used? Palest is best; print the tile in that exact spool.
4. OK to print the fit coupon and the tile first, before the full figure?
5. Keep pink as the cat mouth color, or choose another?

## 15. Revision history
- v1 (2026-09-24): initial spec. No downstream feedback yet. Any reject from Modeler/Tester/Reviewer with a specific reason will be logged here with the changed value.
- v1.1 (2026-09-24, coordinator): TUNNEL_H 8.0 -> 10.0 (an 8 mm tunnel could not pass a cable leaving the rim at mid-thickness, Z 6.4). User decisions confirmed: light approach is the open shared chamber (option 1, no light pipes, interior stays smooth so a white/foil lining can be added later); user has 2 AMS units (8 slots), so the 5-filament plan is fine; pink stays the DEFAULT for the cat's nose and mouth pending the user's word. Still open with the user: puck and cable measurements (R1, R3), layer height and nozzle, yellow PLA choice.
- v1.2 (2026-09-25, coordinator): user rejected the v1 floating black pupil plug. Pupils are now flush black discs in the same thin window skin (see section 8.1 and A9). Base geometry is confirmed by the user's printed fit test and must not change. Pink confirmed for the cat's nose and mouth. User will load the five part STLs into the slicer as one object with parts and assign filaments.
