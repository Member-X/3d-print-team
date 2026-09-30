# Halloween cat "Pumpkin Hug": build parameters

Source of truth: `blender/params.py` (importable; every script reads it). This page lists the same values for people. Spec: `dot_pipeline/specs.md` v1.2. Last updated 2026-09-25 (v2 build).
- The stage-2 values are in "Stage 2: the figure" near the bottom; the v2 changes are in "Stage 2 v2" at the very end.
- The base values below are unchanged, and the figure's base is geometrically identical to the printed coupon.
- The v1 scripts are kept unchanged in `blender/v1_scripts/`.

Units are mm and degrees. Coordinates follow spec section 4:
- The origin is the centre of the base underside, and +Z is up.
- The cat faces -Y, +Y is the back (the tunnel exits there), and +X is the cat's left (tail side).
- Base-feature angles PHI are measured from +Y toward +X (clockwise seen from above), so x = r sin PHI and y = r cos PHI.
- The Blender scene uses 1 unit = 1 mm (unit scale 0.001, millimetres).

Tags: USER, VERIFIED, MEAS-IMG, DERIVED and ASSUMED mean what they mean in the spec. MODELER marks a value the modeller added or changed; each one is explained in "Modeller changes" at the bottom.

Stage column: S1 = used in the stage-1 test parts (coupon or tile). S2 = figure guidance only, not yet built.

Scripts (all in `blender/`):
- `build_test_parts.py`: `build_all()` rebuilds the coupons, the tiles and the REF dummies from these numbers.
- `verify_test_parts.py`: numeric checks, the STL writer and an independent STL read-back.
- `screenshots_test_parts.py`: section views and viewport screenshots.

A rebuild from scratch reproduced all four delivered STLs byte for byte.

## Section 2: printer and process
| Name | Value | Tag | Stage |
|---|---|---|---|
| BED_X / BED_Y / BED_Z | 256 / 256 / 256 | VERIFIED | both |
| NOZZLE | 0.4 | ASSUMED | both |
| LAYER_H | 0.20 | ASSUMED | both |
| MIN_LOAD_WALL | 0.8 | DERIVED | both |
| MIN_FEATURE | 1.2 | DERIVED | both |

## Section 5: dimensions
| Name | Value | Tag | Stage |
|---|---|---|---|
| OVERALL_H | 150.0 | USER | S2 |
| BASE_D | 120.0 | DERIVED | S2 |
| BASE_H | 16.0 | DERIVED | S1 (coupon height) |
| BASE_TOP_FILLET | 1.5 | DERIVED | S2 |
| BASE_BOTTOM_CHAMFER | 0.6 | DERIVED | S1 (coupon outer bottom edge) |
| PUCK_D x PUCK_T | 60.0 x 8.0 | VERIFIED (drawing, not calipered) | S1 (REF_puck) |
| PUCK_RING_D x PUCK_RING_H | 50.0 x 3.0 | ASSUMED (R1) | S1 (REF_puck_ring) |
| PUCK_BACK_HOLE_SPACING | 28.0 | VERIFIED, ignored | - |
| CABLE_D | 4.0 | ASSUMED (R3) | S1 (REF_cable_4) |
| CABLE_D_CHECK | 5.0 | DERIVED worst case | S1 (REF_cable_5) |
| CABLE_LEN_TO_SWITCH / CABLE_SWITCH_BOX_L / CABLE_LEN_SWITCH_TO_USB / CABLE_TOTAL_L | 705 / 45 / 740 / 1490 | VERIFIED | - |
| FIGURE_W (arm span) | 109 | MEAS-IMG | S2 |
| HEAD_W x HEAD_D x HEAD_H | 84 x 66 x 52 | MEAS-IMG | S2 |
| HEAD_CENTER | (0, 14, 113) | MEAS-IMG | S2 |
| HEAD_Z_RANGE | 87 to 139 | MEAS-IMG | S2 |
| EAR_TIP_X / EAR_TOP_Z | +/-36 / 150.0 | MEAS-IMG / USER | S2 |
| EAR_BASE_W / EAR_OUTER_EDGE_H | 28 / 24 | MEAS-IMG | S2 |
| EAR_TIP_R_MIN / EAR_T_MIN | 2.5 / 6.0 (solid) | brief | S2 |
| TORSO_W / TORSO_WIDEST_Z / TORSO_Y_RANGE / TORSO_TOP_Z | 92 / 40 / -20 to 52 / 100 | ASSUMED | S2 |
| PAW_W x PAW_H x PAW_D | 20 x 22 x 26 (solid) | MEAS-IMG | S2 |
| PAW_CENTER_X / PAW_CENTER_Z | +/-43 / 62 | MEAS-IMG | S2 |
| HINDFOOT_W x HINDFOOT_D x HINDFOOT_H | 25 x 28 x 22 (solid) | MEAS-IMG (D ASSUMED) | S2 |
| HINDFOOT_CENTER_X / HINDFOOT_CENTER_Y | +/-36 / -22 | MEAS-IMG | S2 |
| TAIL_TUBE_D_MIN / TAIL_MAX_R | 18 / 57 (+X side, solid) | ASSUMED | S2 |
| PUMPKIN_W x PUMPKIN_D x PUMPKIN_H | 87 x 80 x 70 | W,H MEAS-IMG; D ASSUMED | S2 |
| PUMPKIN_CENTER / PUMPKIN_FRONT_Y | (0, -15, 51) / -55 | MEAS-IMG | S2 |
| STEM_H / STEM_Z_RANGE / STEM_TOP_D / STEM_BASE_D | 14 / 82 to 96 / 11 / 16 | MEAS-IMG | S2 |
| STEM_CHIN_FUSE_MAX / STEM_MOUTH_CLEAR_MIN | 2.0 / 3.0 | spec | S2 |
| RIB_DEPTH_MAX / RIB_WINDOW_FADE | 1.0 / 2.0 | ASSUMED | S2 |
| CAT_EYE_OD / CAT_EYE_X / CAT_EYE_Z | 17.5 / +/-17 / 115 | MEAS-IMG | S2 |
| PUPIL_D / PUPIL_D_MIN | 8.0 / 6.0 | MEAS-IMG | S2 |
| CAT_NOSE_W x CAT_NOSE_H / CAT_NOSE_Z | 8.5 x 6.5 / 111 | MEAS-IMG | S2 |
| INLAY_DEPTH (pink) | 1.0 | spec | S2 |
| CAT_MOUTH_W / CAT_MOUTH_SAG / CAT_MOUTH_Z | 22 / 3 / 104 | MEAS-IMG | S2 |
| CAT_MOUTH_LINE_W / CAT_MOUTH_LINE_W_MIN | 1.6 / 1.2 | ADJUSTED | S2 |
| PK_EYE_W x PK_EYE_H / PK_EYE_CORNER_R_MIN / PK_EYE_X / PK_EYE_Z | 16 x 15 / 2.0 / +/-16.3 / 67 | MEAS-IMG | S2 |
| PK_NOSE_W x PK_NOSE_H / PK_NOSE_Z | 9 x 8 / 57.5 | MEAS-IMG | S2 |
| PK_MOUTH_W x PK_MOUTH_H / PK_MOUTH_Z | 52 x 19 / 46 | MEAS-IMG | S2 |
| PK_TEETH_TOP / PK_TEETH_BOTTOM / PK_TOOTH_W_MIN x PK_TOOTH_H_MIN | 2 / 1 / 6 x 4 | MEAS-IMG | S2 |

## Section 6: base and light-kit interface (all S1, built into the coupon at the full-base coordinates)
| Name | Value | Tag | Measured on the coupon |
|---|---|---|---|
| POCKET_D (POCKET_R) | 61.2 (30.6) | DERIVED | 61.200 at Z 6, 38 probes |
| POCKET_DEPTH (shelf underside Z) | 11.0 | DERIVED | 11.000 |
| POCKET_ENTRY_CHAMFER | 0.6 x 45 deg at Z 0 | DERIVED | r 30.90 at Z 0.3 |
| POCKET_TOP_CHAMFER | 0.8 x 45 deg (wall to shelf) | DERIVED | r 30.20 at Z 10.6 |
| PUCK_SEAT_Z = TAB_TOP_Z | 2.4 | DERIVED | 2.400 (all 3 tabs) |
| PUCK_FACE_Z | 10.4 | DERIVED | REF_puck 2.4 to 10.4 |
| PUCK_SLACK_Z | 0.6 (0.4 at the puck's rim edge, because of the top chamfer) | DERIVED | see note 4 |
| SHELF_Z0 / SHELF_T / SHELF_Z1 | 11.0 / 2.0 / 13.0 | DERIVED | shelf overhang 2.8 (<= 4) |
| APERTURE_D | 54.0 | DERIVED | 53.998 to 54.000 |
| PLENUM_D / PLENUM_Z0 / PLENUM_Z1 | 54.0 / 13.0 / 16.0 | DERIVED (may flare in S2) | 53.998 to 54.000 |
| TAB_ANGLES | 60, 180, 300 | DERIVED | centres 60.00 / 180.00 / 300.00 |
| TAB_CHORD | 9.0 at the tip radius | DERIVED | 8.95 (0.05 deg probe step) |
| TAB_ENGAGE | 0.9 (tip r 29.1) | DERIVED | 0.900 (flex coupon) |
| TAB_ENGAGE_FALLBACK | 0.6 (tip r 29.4) | DERIVED | 0.600 (rigid variant) |
| TAB_RAMP_DEG | 45 (lower lead-in) | DERIVED | r 30.10 at Z 0.5, 29.60 at Z 1.0 |
| ARM_T x ARM_H | 1.6 radial x 4.0 tall | DERIVED | 1.600 x 4.000 |
| ARM_LEN | 14.0, root to the tab (bare flexing arm); tab beyond it | MODELER reading of "about 14" | root at tab centre -34.44 deg |
| ARM_TIP_MARGIN | 0.3 (arm runs past the tab) | MODELER | free end at tab centre +9.44 deg |
| ARM_SLOT_W | **2.2** (spec 1.2) | **MODELER change** | 2.200, open to the bed |
| ARM_RELIEF | 0.8 minimum, as a 45 deg self-supporting ceiling (plane r + Z = 39.2) | MODELER shape | ceiling Z 7.8 over the arm centreline, 4.9 at the slot's outer wall |
| ARM_END_GAP | 1.2 radial gap at the arm tip | MODELER | 1.18 to 1.21 |
| ARM_ROOT_SIDE | root at smaller PHI (all 3 arms, 120 deg rotational symmetry) | MODELER | - |
| TUNNEL_W x TUNNEL_H | 7.0 x 10.0 (v1.1) | DERIVED | 7.000 x 10.000 |
| TUNNEL_CHAMFER | 2.0 x 45 deg top corners, 3.0 flat roof | MODELER | side-wall top at Z 8.0 |
| TUNNEL_PHI | 0 (+Y) | DERIVED | clear from pocket to edge |
| TUNNEL_ROOF_T | 6.0 | DERIVED | 6.000 |
| CABLE_EXIT_Z_NOM / MIN / MAX | 6.4 / 4.5 / 7.5 | DERIVED | zero intersection over the whole range |
| COUPON_D x COUPON_H | 90 x 16 | spec 6.4 | 90.0 x 16.0 |
| COUPON_BOTTOM_CHAMFER / COUPON_TOP_CHAMFER | 0.6 / 1.0 | spec / MODELER | - |

Arm layout per tab (PHI, degrees), for tab centre c:
- the tab spans c +/- 8.896;
- the root is at c - 34.442;
- the free end is at c + 9.443;
- the end gap runs to c + 11.633.

For the 60 deg tab that gives: root 25.56, tab 51.10 to 68.90, free end 69.44, gap to 71.63. The closest arm cutout to the tunnel (at 0 +/- 6.6) starts at 25.6 deg.

## Section 7: hollow geometry (S2; listed because spec section 3 names the wall params)
| Name | Value |
|---|---|
| WALL_CAT / WALL_CAT_MIN | 2.0 / 1.8 |
| WALL_PUMPKIN / WALL_PUMPKIN_MIN | 3.0 / 2.8 |
| NECK_SEAM_Z | 93 +/- 3; neck opening >= 40 x 30 and >= 940 mm2 |
| PLENUM_LINK_MIN_AREA / PLENUM_LINK_MIN_DIM | 900 mm2 / 30 |
| PUMPKIN_TORSO_OVERLAP_MIN_AREA | 1500 mm2 |
| BRIDGE_MAX_PUMPKIN_ROOF / HEAD_ROOF / OTHER | 30 / 20 / 10 |
| HEAD_ROOF_W_MAX | 20 |
| CEILING_PREF_DEG / CEILING_MAX_DEG (from vertical) | 45 / 60 |

## Section 8: light windows and calibration tile
| Name | Value | Tag | Stage / measured |
|---|---|---|---|
| SKIN_T_CAT / SKIN_T_PUMPKIN | 0.5 / 0.5 (to be set from the tile test) | spec | S2 |
| SKIN_T_TOL | 0.40 to 0.60 | spec | S2 |
| WINDOW_FLANK_DEG | 45 | spec | S1 (tile), S2 |
| WINDOW_POCKET_DEPTH_CAT / _PUMPKIN | 1.5 / 2.5 | DERIVED | S2 |
| WINDOW_WEB_MIN / WINDOW_GAP_MIN | 4.0 / 3.0 | spec | S2 |
| PUPIL_SPOKE_W | 1.6 (only if pupils detach) | spec | S2 |
| TILE_W x TILE_H x TILE_T | 60 x 34 x 2.4 | spec | S1: 60.0 x 34.0 x 2.4 |
| TILE_POCKET_W x TILE_POCKET_H | 11 x 22 (skin size; widens 45 deg toward the back) | spec | S1: 11.0 x 22.0 at the skin |
| TILE_POCKET_X | -21, -7, +7, +21 | spec | S1 |
| TILE_SKINS | 0.40 / 0.60 / 0.80 / 1.00 | spec | S1: 0.4000 / 0.6000 / 0.8000 / 1.0000 at 7 points each |
| TILE_POCKET_ZC | 17.0 (skins at Z 6 to 28) | MODELER | S1 |
| TILE_DOT_D x TILE_DOT_H | 1.6 x 0.4 | spec | S1 |
| TILE_DOT_PITCH / TILE_DOT_Z | 2.6 / 31.0 | MODELER | S1 |
| TILE_FOOT_W x TILE_FOOT_D x TILE_FOOT_T | 60 x 10 (from the front face) x 3 | spec | S1 |

## Section 9: viewport colours
black #111111, orange #FF6A00, yellow #FFE01A, green #2E8B2E, pink #FF6FA3.

Mesh resolution: full revolves use 360 facets (chord sag 0.001 mm at r 30). Partial sweeps use 0.5 deg. Each operand in a boolean chain has a different angular phase, so the EXACT solver never meets nearly coincident edges.

## Modeller changes and why (stage 1)
1. **Flex-arm slot widened, 1.2 to 2.2 mm; ARM_LEN read as the bare arm, with the tab beyond it.** The 9 mm tab is stiff, so bending the arm rotates it rather than moving it straight out. Every point of the tab tip has to clear the puck rim, which means the tab's root-side end must retract the full 0.9 mm. In a cantilever the free tip then moves much further. Estimates from beam theory, with PLA E about 3000 MPa (not measured):
   - **Literal "14 mm arm including the tab":** tip travel about 3.3 to 3.8 mm and root strain about 7 to 9%. PLA cracks.
   - **14 mm arm to the tab, spec 1.2 mm slot:** the tip needs about 1.8 to 1.9 mm, so it hits the slot wall first. The puck cannot pass.
   - **As built (14 mm arm + 9 mm tab, 2.2 mm slot):** tip travel about 1.8 to 1.9 mm, leaving 0.3 mm spare in the slot. Root strain is about 1.0 to 1.1% at full engagement, and about 1.3% when the slot bottoms out. Push-in force is about 2.7 to 4 N radial per tab, roughly 15 to 25 N total. The slot wall acts as an over-travel stop.
2. **Relief above the arm** is a 45 deg ceiling, not a flat 0.8 mm gap. A flat 3.8 mm ledge 0.8 mm above the arm would droop onto it or need unremovable supports. The ceiling starts 0.8 above arm-top level at the slot's outer wall (Z 4.8 at r 34.4) and rises inward at 45 deg. Directly above the arm the gap is 3.0 at its outer top edge, 3.8 at the centreline and 4.6 at its inner edge.
3. **Tunnel top chamfers** are 2.0 mm legs; the spec gave no size. Larger legs would clip a 5 mm cable exiting at Z 7.5. With 2.0 the chamfer margin is at least 0.33 over the whole 4.5 to 7.5 exit range.
4. **Puck slack at the rim edge is 0.4, not 0.6.** This is a consequence of the spec's own 0.8 top chamfer, not a change: a sharp-edged puck touches that chamfer after 0.4 mm of lift, or after 0.4 mm of sideways play at the top edge. Along the rest of the wall the gaps are 0.6 radial and 0.6 to the shelf.
5. **Rigid-tab fallback exported as a separate variant.** It is `base-fit-coupon_rigid-tabs-0.6`, as spec 6.1 allows. With rigid tabs, the 0.6 engagement exactly equals the 0.6 pocket clearance. The puck then goes in only by tilting and shifting it, with zero margin at the last tab, so treat this variant as the comparison piece, not the first choice.
6. **Tile identification dots:** the spec version has raised dots, which suit Print A (standing). On Print B (front face down) raised dots would lift the whole plate 0.4 mm off the bed. `skin-calibration-tile_flat-print` has the same dots sunk 0.4 mm into the front face and works for both prints.

---

# Stage 2: the figure

## How it is built, and how to re-run it
Scripts in `blender/`:
- `params.py`: all values below.
- `face_outlines.py`: run once with system Python. It traces the concept and writes `face_outlines.json`.
- `figure_shapes.py`: implicit fields for every body part.
- `build_figure.py`: the pipeline steps.
- `verify_figure.py` and `stl_check.py`: the checks.
- `export_figure.py`: the STL and 3MF files.
- `render_figure.py`: the renders.
- `overlay_figure.py`: the concept overlay (A12).

Pipeline (inside Blender): `step_fields` -> `step_outer` -> `step_master` -> `step_base_void` -> `column_data` + `build_window_cutters` (cat, pk) -> `step_windows` -> `step_zones` -> the part booleans (`boolean_seq`) -> `fix_crossings`. A revision is a re-run of the steps downstream of the changed value. For example:
- a new SKIN_T_* only needs `column_data` onward;
- a wall change needs `step_master` onward.

Method in short:
- The envelope is a smooth union of implicit shapes on a 0.5 mm grid, meshed with OpenVDB.
- The chamber is derived from the exact distance to the outer mesh, so the walls are uniform.
- The base void, the window pockets and the colour zones are applied with EXACT booleans.

## Grid and meshing
| Name | Value | Note |
|---|---|---|
| GRID_H | 0.5 | outer envelope and chamber |
| GRID_LO / GRID_HI | (-62, -62, -2) / (62, 62, 152) | |
| FINE_H | 0.2 | local grids for window pockets, yellow and pink zones |
| Quad split | BEAUTY triangulation right after meshing | fold-free; the fixed diagonal gave 448 crossing triangle pairs |

## Shapes (mm; the cat faces -Y, +X is the cat's left)
| Name | Value | Tag |
|---|---|---|
| HEAD_ZW / HEAD_A / HEAD_B / HEAD_YC | 106 / 42 / 33 / 14 | MEAS-IMG; widest at the cheeks (concept) |
| HEAD_C_UP / HEAD_C_DN | 33 (crown 139) / 19 (chin 87) | spec |
| HEAD_NX_UP, HEAD_NX_DN / HEAD_NY_UP, HEAD_NY_DN | 2, 3 / 2, 2.2 | MODELER (boxy cheeks, receding chin) |
| EAR_TRI, EAR_R | core (-31.41, 141.5) (-31.57, 116.66) (-21.84, 135.17); R 8.5 | MODELER fit to the concept outline, rms 0.27 |
| EAR_Y, EAR_Z_PIVOT, EAR_TILT_DEG | 12, 128, 8 | MODELER |
| EAR_T_BASE / EAR_T_TIP (z 125 / 146), EAR_EDGE_R | 16 / 9, 3.0 | spec min 6 |
| EAR_CUP (x, z, rx, rz, ry, depth) | (-28, 139, 5.5, 8, 5.5, 1.3) | MODELER inner-ear dish |
| TORSO_ZW / TORSO_A / TORSO_B / TORSO_YC | 40 / 45.5 / 35 / 15 | spec blocking (y -20..50) |
| TORSO_C_UP, N_UP / C_DN, N_DN | 60, 2.2 / 40, 2.0 | 43 deg taper at the deck |
| HAUNCH_C / HAUNCH_R / HAUNCH_BLEND | (+-37, -4, 40) / (16, 21, 17) / 8 | MODELER: thighs give the concept's +-53 silhouette |
| ARM_PTS (x, y, z, r) | (34, 12, 86, 12), (45, 3, 67, 10), (42.5, -11, 62, 9.5) | MODELER |
| PAW_C / PAW_R | (+-43, -18, 62) / (10.5, 12, 12.5) | spec centre; W 21 x D 24 x H 25 |
| FINGERS / FINGER_R / blend | 3 bumps at z 70.3, 62, 53.7 / (5.6, 6.4, 4.6) / 1.2 | MODELER (concept) |
| FOOT_C / FOOT_R | (+-36, -24, 23) / (12.5, 15, 13) | spec |
| TAIL_PTS (x, y, z, r), Catmull-Rom sweep | (5, 45, 19.5, 8.5) ... (41.5, 20, 41, 9) | MODELER; centreline + radius <= 56.44 |
| PK_ZW / PK_A / PK_B / PK_YC | 51 / 43.5 / 40 / -15 | spec |
| PK_C_UP, N_UP / C_DN, N_DN | 35, 2.0 / 35, 2.5 | MODELER: broader seat |
| RIB_N / RIB_DEPTH / RIB_POWER | 10 / 0.8 / 6 | <= 1.0 spec |
| RIB_FACE_CLEAR / RIB_FADE_W | 4 / 4 | rib-free face panel (spec >= 2) |
| STEM_XY / STEM_Z0..Z1 / R0 / R1 / top round | (0, -20) / 82..96 / 8 / 5.5 / 1.5 | MODELER: y -20, 5 mm forward to clear the chin |
| PAD_PROFILE (r, z) | r 31.5 to z 17, 45 deg chamfer to r 27.5 at z 21 | MODELER plinth, see changes |
| Blends: SHOULDER / ARM / PAW / FOOT / TAIL / EAR / NECK / PUMPKIN / STEM / PAD / DECK | 2.5 / 4 / 4 / 3 / 1.5 / 4 / 2 / 1 / 2.5 / 2.5 / 2 | small at the neck and pumpkin keeps the seam creases |
| SKIRT_DEG / SKIRT_Z_TOP | 45 / 34 | automatic self-supporting skirt under forms that meet the deck |

## Chamber
| Name | Value |
|---|---|
| WALL_CAT / WALL_PUMPKIN | 2.0 / 3.0. The wall rises to 3.0 wherever the chamber is within 3 mm of the pumpkin surface |
| CHAMBER_FLOOR_Z | 16 (on the deck) |
| CHAMBER_SELECT_SLACK | 0.3 |
| CEIL_CONE_DEG / CEIL_FRONT_DEG / CEIL_FRONT_HALF / CEIL_FRONT_BLEND | 45 / 58 / 50 / 20 (roof cones: 58 deg in the sector facing the windows, 45 deg elsewhere) |
| HEAD_ROOF_XY / HEAD_ROOF_R | (0, 12) / 10. Flat bridge Ø20 at z 134.28 |
| PK_ROOF_SEEDS | (0, -17), R 15. Flat bridge Ø30 at z 78.95 |
| Window apex roofs | a 58 deg cone apex behind every window column at the natural wall depth: 1,912 apexes (cat), 3,977 (pumpkin) |
| NECK_STADIUM / NECK_Z / TORSO_ROOF_Z | 44 x 32 (1,188 mm2) / 84..97 / 97 |
| PLENUM_STUB_R / Z0 / FLARE_Z / DIAMOND_Z | 25 / 12.5 / 14.5 / 19 |
| BASE_VOID_TOP | 18 (the stage-1 bore runs 2 mm into the chamber) |

## Windows and inlays
| Name | Value |
|---|---|
| SKIN_T_CAT / SKIN_T_PUMPKIN | 0.5 / 0.5 (measured 0.4997 to 0.5078 at 4,341 points) |
| Pocket flank | 45 deg along Y, from the skin floor |
| WINDOW_EPS | 0.08: the pocket floor runs this far past each outline |
| WINDOW_BACK_OVERLAP | 0.6 |
| Pocket back limit | never deeper than the chamber behind the nearest window point |
| YELLOW_BACK / INLAY_FRONT / INLAY_DEPTH | 0.3 / 1.5 / 1.0 |
| Pumpkin face | traced from the concept, one vertical shift of +8.0. Eyes 16.0 x 15.95 at x +-16.06, z 68.0; nose 8.2 x 7.5; mouth 50.9 x 17.9 |
| Pumpkin face rules | corner opening r 2 (eyes, nose); opening r 1.5 on the mouth (yellow gaps >= 3); webs >= 5.7 |
| Cat eyes | OD 17.5, pupil 8.0 concentric, at (+-17, 115) |
| Cat nose | traced, scaled to 8.5 x 6.5, centre z 109.97 |
| Cat mouth | two circular arcs through the cusp (0, 103.95), the bottom (+-6.2, 100.95) and the end (+-10.2, 104.75). Line 1.6, round caps |

## Modeller changes and deviations (stage 2)
1. **Roof cone angle.** 58 deg in the front sectors, 45 deg elsewhere (spec prefers 45, allows 60). Plus a point-apex cone behind every window column. With 45 deg all round, 98% of each pumpkin eye and about 50% of each cat eye sat behind 5-15 mm of solid wall.
2. **Plinth.** A hidden pad (r 31.5, top z 21) under the figure. Without it the Ø54 plenum bore came within 0.5-0.8 mm of the outside in small crease gaps at the front sides.
3. **Pocket back limit** (never deeper than the chamber behind the nearest window point). Stops flanks tunnelling into thick wall above the eyes.
4. **Stem moved 5 mm forward** (y -20) so it fuses at most 1 mm into the chin while staying on the pumpkin top.
5. **Head shape.** Widest at z 106 (concept cheeks), not a plain ellipsoid at z 113. It keeps the spec's W 84 x D 66 x z 87..139.
6. **Torso narrower than the concept's lower-body silhouette.** Thighs carry that width, so the tail can wrap the rear inside r 57.
7. **Pupils concentric** (spec). The concept has them offset 2 mm toward the nose, which would make a 2.75 mm yellow gap (< 3 rule).
8. **Cat nose raised 1.0 mm** from the concept layout (z 109.97, spec about 111). This keeps 1.97 mm of black between the nose and the mouth.
9. **Orange wall thins next to the pumpkin windows (fails spec 7 / 9 "orange >= 2.8" in a band 3.5-5 mm wide).** Measured with 12,000 surface samples, by distance from a window edge:

   | Distance from edge | Min wall | Share below 2.8 |
   |---|---|---|
   | 3.5-4 mm | 2.08 | 74% |
   | 4-5 mm | 2.49 | 18% |
   | 5 mm and beyond | >= 2.88 | 0% |

   Outside the 3.5 mm flank band, 3.0% of the orange surface is below 2.8.
   - Cause: the flank is 45 deg to Y (the window projection axis). Where the pumpkin surface leans away from Y, the pocket roof or side runs nearly parallel to the outer surface: above the eyes, beside their outer edges and under the mouth. On a flat front the 2.8 mm would come back 3.46 mm from the edge.
   - Possible fix: tilt those flanks up to the allowed 60 deg, relative to the surface. Or accept a faint orange glow ring around the pumpkin face.
10. **Mesh clean-up after the EXACT booleans.**
    - Specks, duplicate faces, flaps and tiny holes were repaired.
    - Crossing triangles were relaxed by moving vertices, at most 0.13 mm.
    - 12 zero-area micro-triangles remain in each of black, orange and yellow. Deleting them opens edges. They are manifold, and slicers ignore them.

## Outputs (v14)
- `stl/halloween-cat_{black,orange,yellow,green,pink}.stl` and `stl/halloween-cat_combined.stl`.
- `3mf/halloween-cat.3mf`: 5 named mesh objects under one assembly. It follows the core 3MF spec but has not been opened in Bambu Studio.
- `blender/halloween-cat.blend`: the 5 parts in collection FIGURE_PARTS, already in print orientation (Z=0, centred). Versions v1-v14 are in `blender/versions/`.
- `renders/`: the views, the cross-sections and the A12 overlays.

---

# Stage 2 v2 (2026-09-25)

## How v2 is built
The v2 file is `blender/halloween-cat-v2.blend`, with versions `halloween-cat_v15..v18` in `blender/versions/`.

Scripts, with the v1 helpers reused:
- `build_figure_v2.py`;
- `bgrun.py` (runs long steps from a Blender timer);
- `verify_v2.py`, `export_figure_v2.py`, `stl_check_v2.py`.

Order of steps:
1. `step_fields`, `step_outer`, `step_master`, `step_base_void`.
2. `flank_table` and `column_grid` (for `cat` and `pk`), then `window_fields`.
3. `decimate_inputs` on the cutters and zones.
4. `step_windows`, `step_zones` (orange/green zones decimated), `join_yellow`.
5. `step_part` x 5, then `fix_crossings_synced`, then `clean_micro`.

## Changed values
| Name | v2 value | v1 value | Why |
|---|---|---|---|
| SKIN_T | 0.5 | (separate names) | One skin parameter. SKIN_T_CAT and SKIN_T_PUMPKIN are now derived from it |
| RIB_POWER | 4.0 | 6.0 | Softer, rounder grooves |
| RIB_POLE_R0 / R1 | 17 / 30 | linear fade r 6..14 | Grooves fade out (C1) well before the stem: no puckering |
| RIB_Z0 / Z1 | 27 / 37 | none | No grooves on the lower band, skirt or plinth: no dimples |
| Rib face / front fades | smoothstep | linear | C1 transitions |
| SKIRT_SMOOTH_PASSES | 3 (binomial blur, sigma about 0.6, z 14..38) | none | The discrete 45 deg skirt left ripples on the pumpkin underside |
| HEAD_ROOF_R | 9.4 (flat Ø18.8) | 10.0 | Measured bridge 19.0 x 19.0 (v1 20.5 x 20.6; limit 20) |
| WINDOW_FLANK_MAX_DEG | 40 (from the surface normal) | 45 (to the Y axis) | Orange >= 2.8 from 3.5 mm out (flat-wall theory: 3.00 at 3.5 mm) |
| POCKET_CEIL_PREF_DEG / MAX | 55 / 60 | (none) | Pocket ceiling limits used to pick phi per outline point |
| FLANK_SMOOTH_MM | 1.5 | - | phi smoothed along the outline |
| WINDOW_EPS_V2 | 0.08 (surface distance) | 0.08 (projected) | Same lip |
| PUPIL_BOSS_T | 0.0 = OFF (max 0.7, 45 deg flank) | - | Optional black backing boss behind each pupil skin. Tested at 0.5: it removes 48 mm3 from the pocket cutters as expected |
| DEC_ENV_TRIS / DEC_CHAMBER_TRIS | 180,000 / 60,000 | (no decimation) | Lighter meshes |
| DEC_CUTTER_RATIO / DEC_ZONE_RATIO | 0.30 / 0.25 | - | Lighter meshes |

## Windows in surface-normal coordinates
Each fine-grid voxel p is placed on the outer surface before it is classified:
- depth v = exact distance to the decimated outer surface;
- foot point q = the nearest point on that surface;
- s = projected outline distance at q x local stretch, which gives the distance along the surface.

With those:
- **Pocket:** v >= SKIN_T, and s <= EPS + (v - SKIN_T) tan(phi), and v <= the chamber depth behind the nearest window point + 0.6.
- **Yellow zone:** s <= 0 and v <= SKIN_T + 0.3.
- **Pink zone:** s_inlay <= 0 and v <= 1.0.

phi is chosen per outline sample:
- Take the largest phi <= 40 deg whose pocket ceiling is <= 55 deg from vertical.
- If none, take the largest phi with a ceiling <= 60 deg.
- If none, take the least steep phi and report that spot as a short bridge.

| Window | phi range | Worst pocket ceiling |
|---|---|---|
| Cat eyes | 2.7-40 | 59.9 deg |
| Pumpkin eyes | 19.5-40 | 60.0 deg |
| Pumpkin nose | 40 | 67.9 deg, only at the apex (1.5 mm of outline, a 3.8 x 3.2 mm bridge) |
| Mouth | 40 | 54.6 deg |

Cat eyes (spec v1.2):
- The pocket is the whole Ø17.5 disc.
- The pupil is black skin, 0.5 thick, flush with the outer surface and in the same skin plane as the ring. No plug.

## Mesh budget (triangles)
| Mesh | v1 | v2 |
|---|---|---|
| Outer envelope | 783k | 180k (decimated) |
| Chamber | 437k | 60k (decimated) |
| Parts black / orange / yellow / green / pink | 1,050,976 / 383,152 / 177,416 / 10,124 / 14,484 | 250,442 / 121,028 / 56,408 / 4,792 / 5,318 |
| Parts total | 1,636,152 | 437,988 |
| Combined (master) | 1,391,760 | 309,630 |

## Outputs (v2)
- `stl/v2/halloween-cat-v2_{black,orange,yellow,green,pink}.stl` and `_combined.stl`. The combined file is the master M2.
- `3mf/v2/halloween-cat-v2_core-3mf.3mf`: plain core-spec 3MF, the fallback.
- `3mf/v2/halloween-cat-v2_bambu-studio.3mf`: Bambu Studio project style.
  - One object with five parts; filament slots 1 black, 2 orange, 3 yellow, 4 green, 5 pink.
  - Placed at the plate centre (128, 128).
  - P2S presets named; detect_thin_wall on.
  - Not tested in Bambu Studio.
- `obj/v2/halloween-cat-v2_5-parts.obj` + `halloween-cat-v2.mtl`: five closed objects, one material each.
- `obj/v2/halloween-cat-v2_painted-single-mesh.obj`: one closed mesh with coloured faces, for OBJ colour import.
- `renders/v2/`: the views, the cross-sections and the A12 overlays.
