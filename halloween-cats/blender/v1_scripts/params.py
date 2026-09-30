"""Halloween cat "Pumpkin Hug" - shared build parameters.

Single source of truth for every named dimension in dot_pipeline/specs.md (v1.1)
sections 5, 6, 7 and 8, so stage 2 (the full figure) reuses exactly the numbers
the stage-1 test parts were built and printed with.

Units: millimetres and degrees. Blender scene: 1 BU = 1 mm (unit scale 0.001).

Coordinates (spec section 4): origin = centre of the base underside, +Z up,
the cat faces -Y, +Y = back (cable tunnel exits at +Y), +X = cat's left (tail).
Base-feature angles PHI are measured from +Y toward +X (clockwise seen from
above):  x = r*sin(PHI), y = r*cos(PHI).

Tags: USER, VERIFIED, MEAS-IMG, DERIVED, ASSUMED (spec meanings), MODELER = value
chosen or changed by the 3d-blender-modeler (see parameters.md for why).

Import from a Blender script:
    import sys; sys.path.insert(0, r"H:/ClaudeStuff/3d-print-team/halloween-cats/blender")
    import params as P
"""
import math

SPEC_VERSION = "1.1"

# ---------------------------------------------------------------- section 2
BED_X = BED_Y = BED_Z = 256.0          # VERIFIED (vendor)
NOZZLE = 0.4                            # ASSUMED
LAYER_H = 0.20                          # ASSUMED
MIN_LOAD_WALL = 0.8                     # DERIVED 2 x nozzle
MIN_FEATURE = 1.2                       # DERIVED (window skins excepted)

# ---------------------------------------------------------------- section 5
OVERALL_H = 150.0                       # USER, Z0 to ear-tip top
BASE_D = 120.0                          # DERIVED
BASE_H = 16.0                           # DERIVED (11 pocket + 2 shelf + 3 plenum)
BASE_TOP_FILLET = 1.5                   # DERIVED
BASE_BOTTOM_CHAMFER = 0.6               # DERIVED (elephant foot)

PUCK_D = 60.0                           # VERIFIED (drawing)
PUCK_T = 8.0                            # VERIFIED (drawing)
PUCK_RING_D = 50.0                      # ASSUMED dummy (48-50 drawn, R1)
PUCK_RING_H = 3.0                       # ASSUMED dummy (height not drawn, R1)
PUCK_BACK_HOLE_SPACING = 28.0           # VERIFIED, ignored
CABLE_D = 4.0                           # ASSUMED (R3)
CABLE_D_CHECK = 5.0                     # DERIVED worst case for REF_cable_5
CABLE_LEN_TO_SWITCH = 705.0             # VERIFIED
CABLE_SWITCH_BOX_L = 45.0               # VERIFIED
CABLE_LEN_SWITCH_TO_USB = 740.0         # VERIFIED
CABLE_TOTAL_L = 1490.0                  # VERIFIED

FIGURE_W = 109.0                        # MEAS-IMG arm span
HEAD_W, HEAD_D, HEAD_H = 84.0, 66.0, 52.0          # MEAS-IMG
HEAD_CENTER = (0.0, 14.0, 113.0)                    # MEAS-IMG
HEAD_Z_RANGE = (87.0, 139.0)                        # MEAS-IMG
EAR_TIP_X = 36.0                        # MEAS-IMG (+/-)
EAR_TOP_Z = 150.0                       # USER
EAR_BASE_W = 28.0                       # MEAS-IMG
EAR_OUTER_EDGE_H = 24.0                 # MEAS-IMG
EAR_TIP_R_MIN = 2.5                     # brief (blunt tips)
EAR_T_MIN = 6.0                         # at mid-height, solid
TORSO_W = 92.0                          # ASSUMED blocking
TORSO_WIDEST_Z = 40.0                   # ASSUMED
TORSO_Y_RANGE = (-20.0, 52.0)           # ASSUMED
TORSO_TOP_Z = 100.0                     # ASSUMED (shoulders)
PAW_W, PAW_H, PAW_D = 20.0, 22.0, 26.0  # MEAS-IMG, solid
PAW_CENTER_X = 43.0                     # MEAS-IMG (+/-)
PAW_CENTER_Z = 62.0                     # MEAS-IMG
HINDFOOT_W, HINDFOOT_D, HINDFOOT_H = 25.0, 28.0, 22.0   # MEAS-IMG (D ASSUMED)
HINDFOOT_CENTER_X = 36.0                # MEAS-IMG (+/-)
HINDFOOT_CENTER_Y = -22.0               # MEAS-IMG
TAIL_TUBE_D_MIN = 18.0                  # ASSUMED, +X side, solid
TAIL_MAX_R = 57.0                       # inside base footprint
PUMPKIN_W, PUMPKIN_D, PUMPKIN_H = 87.0, 80.0, 70.0      # W,H MEAS-IMG, D ASSUMED
PUMPKIN_CENTER = (0.0, -15.0, 51.0)     # bottom z 16, top z 86
PUMPKIN_FRONT_Y = -55.0                 # 5 mm inside base edge
STEM_H = 14.0                           # MEAS-IMG
STEM_Z_RANGE = (82.0, 96.0)
STEM_TOP_D = 11.0
STEM_BASE_D = 16.0
STEM_CHIN_FUSE_MAX = 2.0
STEM_MOUTH_CLEAR_MIN = 3.0
RIB_DEPTH_MAX = 1.0                     # ASSUMED, optional
RIB_WINDOW_FADE = 2.0
CAT_EYE_OD = 17.5                       # MEAS-IMG (yellow ring)
CAT_EYE_X = 17.0                        # +/-
CAT_EYE_Z = 115.0
PUPIL_D = 8.0                           # MEAS-IMG
PUPIL_D_MIN = 6.0
CAT_NOSE_W, CAT_NOSE_H = 8.5, 6.5       # pink, rounded triangle apex down
CAT_NOSE_Z = 111.0
INLAY_DEPTH = 1.0                       # pink inlays
CAT_MOUTH_W = 22.0
CAT_MOUTH_SAG = 3.0
CAT_MOUTH_Z = 104.0
CAT_MOUTH_LINE_W = 1.6                  # ADJUSTED from concept 0.9
CAT_MOUTH_LINE_W_MIN = 1.2
PK_EYE_W, PK_EYE_H = 16.0, 15.0         # rounded triangles apex up
PK_EYE_CORNER_R_MIN = 2.0
PK_EYE_X = 16.3                         # +/-
PK_EYE_Z = 67.0
PK_NOSE_W, PK_NOSE_H = 9.0, 8.0
PK_NOSE_Z = 57.5
PK_MOUTH_W, PK_MOUTH_H = 52.0, 19.0
PK_MOUTH_Z = 46.0
PK_TEETH_TOP = 2
PK_TEETH_BOTTOM = 1
PK_TOOTH_W_MIN, PK_TOOTH_H_MIN = 6.0, 4.0

# ---------------------------------------------------------------- section 6
POCKET_D = 61.2                         # DERIVED (60 + 1.2)
POCKET_R = POCKET_D / 2.0               # 30.6
POCKET_DEPTH = 11.0                     # Z of shelf underside
POCKET_ENTRY_CHAMFER = 0.6              # 45 deg at Z0
POCKET_TOP_CHAMFER = 0.8                # 45 deg, pocket-wall/shelf corner
PUCK_SEAT_Z = 2.4                       # puck back face on tab tops
PUCK_FACE_Z = PUCK_SEAT_Z + PUCK_T      # 10.4 (lit face)
PUCK_SLACK_Z = POCKET_DEPTH - PUCK_FACE_Z   # 0.6
SHELF_Z0 = POCKET_DEPTH                 # 11.0
SHELF_T = 2.0
SHELF_Z1 = SHELF_Z0 + SHELF_T           # 13.0
APERTURE_D = 54.0
PLENUM_D = 54.0                         # coupon value; stage 2 may flare upward
PLENUM_Z0 = SHELF_Z1                    # 13.0
PLENUM_Z1 = BASE_H                      # 16.0 (deck)

# Snap tabs (6.1)
TAB_ANGLES = (60.0, 180.0, 300.0)       # PHI from +Y; none at the tunnel
TAB_CHORD = 9.0                         # measured at the tab tip radius (min chord)
TAB_ENGAGE = 0.9                        # over the puck rim (r = 30)
TAB_ENGAGE_FALLBACK = 0.6               # rigid-tab fallback (spec)
TAB_TOP_Z = PUCK_SEAT_Z                 # 2.4, flat top
TAB_RAMP_DEG = 45.0                     # lower lead-in ramp
def tab_tip_r(engage=TAB_ENGAGE):
    return PUCK_D / 2.0 - engage        # 29.1 (29.4 fallback)

# Flex arm (6.1).  MODELER changes, see parameters.md: the spec's 1.2 mm outer
# slot cannot let the root-side end of a 9 mm rigid tab retract 0.9 mm (tip
# would need ~1.9 mm travel), so ARM_SLOT_W = 2.2; ARM_LEN is the bare
# flexing arm from its root to the tab, the tab (TAB_CHORD) sits beyond it.
ARM_T = 1.6                             # radial (bending) thickness, spec
ARM_H = 4.0                             # height Z0-4.0, spec
ARM_LEN = 14.0                          # root -> tab start, along arm centreline (spec "about 14")
ARM_TIP_MARGIN = 0.3                    # MODELER: arm runs 0.3 past the tab (clean boolean)
ARM_SLOT_W = 2.2                        # MODELER (spec 1.2): outer arc slot, open to bed
ARM_SLOT_W_SPEC = 1.2
ARM_RELIEF = 0.8                        # spec minimum gap above the arm; built as a 45 deg
                                        # self-supporting ceiling starting ARM_RELIEF above
                                        # ARM_H at the slot's outer wall (gap grows inward)
ARM_END_GAP = 1.2                       # MODELER: radial gap freeing the arm tip
ARM_ROOT_SIDE = -1                      # root lies at smaller PHI than the tab
ARM_R_IN = POCKET_R                     # 30.6 (arm inner face = pocket wall)
ARM_R_OUT = POCKET_R + ARM_T            # 32.2
ARM_R_MID = POCKET_R + ARM_T / 2.0      # 31.4
SLOT_R_OUT = ARM_R_OUT + ARM_SLOT_W     # 34.4
RELIEF_CEIL_C = SLOT_R_OUT + ARM_H + ARM_RELIEF   # ceiling plane r + z = C (45 deg)

# Cable tunnel (6.2)
TUNNEL_W = 7.0                          # spec
TUNNEL_H = 10.0                         # spec v1.1 (was 8.0)
TUNNEL_CHAMFER = 2.0                    # MODELER: 45 deg top-corner chamfer leg (flat roof 3.0)
TUNNEL_PHI = 0.0                        # toward +Y
TUNNEL_ROOF_T = BASE_H - TUNNEL_H       # 6.0
CABLE_EXIT_Z_NOM = PUCK_SEAT_Z + PUCK_T / 2.0   # 6.4 (mid-thickness)
CABLE_EXIT_Z_MIN = 4.5
CABLE_EXIT_Z_MAX = 7.5

# Base fit coupon (6.4)
COUPON_D = 90.0
COUPON_H = BASE_H                       # 16.0
COUPON_BOTTOM_CHAMFER = BASE_BOTTOM_CHAMFER   # 0.6
COUPON_TOP_CHAMFER = 1.0                # MODELER (outer top edge, handling only)

# ---------------------------------------------------------------- section 7
WALL_CAT = 2.0
WALL_CAT_MIN = 1.8
WALL_PUMPKIN = 3.0
WALL_PUMPKIN_MIN = 2.8
NECK_SEAM_Z = 93.0                      # +/- 3
NECK_OPEN_MIN_X, NECK_OPEN_MIN_Y, NECK_OPEN_MIN_AREA = 40.0, 30.0, 940.0
PLENUM_LINK_MIN_AREA, PLENUM_LINK_MIN_DIM = 900.0, 30.0
PUMPKIN_TORSO_OVERLAP_MIN_AREA = 1500.0
BRIDGE_MAX_PUMPKIN_ROOF = 30.0
BRIDGE_MAX_HEAD_ROOF = 20.0
BRIDGE_MAX_OTHER = 10.0
HEAD_ROOF_W_MAX = 20.0
CEILING_PREF_DEG = 45.0                 # from vertical
CEILING_MAX_DEG = 60.0

# ---------------------------------------------------------------- section 8
SKIN_T_CAT = 0.5
SKIN_T_PUMPKIN = 0.5
SKIN_T_TOL = (0.40, 0.60)
WINDOW_FLANK_DEG = 45.0
WINDOW_POCKET_DEPTH_CAT = WALL_CAT - SKIN_T_CAT          # 1.5
WINDOW_POCKET_DEPTH_PUMPKIN = WALL_PUMPKIN - SKIN_T_PUMPKIN  # 2.5
WINDOW_WEB_MIN = 4.0                    # orange web between windows, outer surface
WINDOW_GAP_MIN = 3.0                    # every yellow gap, outer surface
PUPIL_SPOKE_W = 1.6                     # only if pupils detach in testing

# Skin calibration tile (8.3). Tile frame: plate in X-Z, front face at y = 0
# facing -Y, back face at y = TILE_T, standing on the L-foot at z = 0.
TILE_W = 60.0
TILE_H = 34.0
TILE_T = 2.4
TILE_POCKET_W = 11.0                    # skin (pocket floor) size
TILE_POCKET_H = 22.0
TILE_POCKET_X = (-21.0, -7.0, 7.0, 21.0)
TILE_SKINS = (0.40, 0.60, 0.80, 1.00)
TILE_FLANK_DEG = 45.0
TILE_POCKET_ZC = 17.0                   # MODELER: pockets centred on the plate height
TILE_DOT_D = 1.6
TILE_DOT_H = 0.4
TILE_DOT_PITCH = 2.6                    # MODELER
TILE_DOT_Z = 31.0                       # MODELER: 2.2 above the skin top edge
TILE_FOOT_W = 60.0
TILE_FOOT_D = 10.0                      # measured from the front face (y 0..10)
TILE_FOOT_T = 3.0

# ---------------------------------------------------------------- section 9
COLORS = {"black": "#111111", "orange": "#FF6A00", "yellow": "#FFE01A",
          "green": "#2E8B2E", "pink": "#FF6FA3"}

# ---------------------------------------------------------------- mesh resolution
SEG_FULL = 360                          # full revolves: 1 deg facets (sag 0.001 mm at r 30)
SEG_DEG_PARTIAL = 0.5                   # partial sweeps (arms, tabs)


# ================================================================= STAGE 2
# Full figure.  Everything below is used by figure_shapes.py / build_figure.py.
# Values tagged MEAS-IMG were re-measured numerically from concept-a.png pixels
# (axis column 502.3, x mm = (col-502.3)/5.85, level z mm = 139-(row-148)/5.71).

# ---- implicit-field grid (outer envelope + chamber)
GRID_H = 0.5                            # voxel (mm); marching surface sag << 0.01 mm
GRID_LO = (-62.0, -62.0, -2.0)          # grid origin (multiples of GRID_H)
GRID_HI = (62.0, 62.0, 152.0)
FINE_H = 0.2                            # local grids for window/inlay cutters and zones

# ---- head: lofted elliptical sections, a(z)=HEAD_A*s(z), b(z)=HEAD_B*s(z)
# s(z) = (1-|t|^n)^(1/n), t=(z-HEAD_ZW)/c.  Concept: widest at the cheeks
# (level z ~105), still 39 half-width at the neck crease (z 93) -> boxy lower
# half in X (n 4), rounder in Y (n 2.2) so the chin recedes for the stem.
HEAD_ZW = 106.0                         # z of widest section (MEAS-IMG)
HEAD_A = 42.0                           # half width  (84 total, spec)
HEAD_B = 33.0                           # half depth  (66 total, spec)
HEAD_YC = 14.0                          # spec
HEAD_C_UP = 33.0                        # -> crown z 139 (spec)
HEAD_C_DN = 19.0                        # -> chin z 87 (spec)
HEAD_NX_UP, HEAD_NX_DN = 2.0, 3.0
HEAD_NY_UP, HEAD_NY_DN = 2.0, 2.2

# ---- ears (front-view triangle in the ear plane, core triangle + rounding)
# concept left ear: outer edge x -36.4 (z 149) .. -40.2 (z 139), inner edge
# -28.4 (z 149) .. -13.4 (z 139), tip x about -33.
# Least-squares fit of a rounded triangle to the concept's left-ear outline
# (68 edge samples, rms 0.27 mm): core triangle + corner radius 8.5.  The top
# of the rounded tip lands on z 150.0 exactly (tip z + EAR_R).
EAR_R = 8.5                             # 2D corner rounding = tip radius (>= 2.5 spec)
EAR_TRI = ((-31.41, 141.5), (-31.57, 116.66), (-21.84, 135.17))   # core triangle (x,z), left ear
EAR_Y = 12.0                            # ear mid-plane y at the pivot
EAR_Z_PIVOT = 128.0
EAR_TILT_DEG = 8.0                      # top leans back (+Y)
EAR_T_BASE = 16.0                       # slab thickness (Y) at z 125
EAR_T_TIP = 9.0                         # slab thickness at z 146 (>= 6 everywhere)
EAR_T_Z = (125.0, 146.0)
EAR_EDGE_R = 3.0                        # rounding of the slab edges
EAR_CUP = (-28.0, 139.0, 5.5, 8.0, 5.5, 1.3)   # inner-ear dish: x, z, rx, rz, ry, depth (front face)
EAR_BLEND = 4.0

# ---- torso: lofted, widest at z 40
TORSO_ZW = 40.0
TORSO_A = 45.5                          # half width (spec W ~92); thighs give the +/-53 silhouette
TORSO_B = 35.0                          # half depth (y -20 .. 50, spec -20 .. 52)
TORSO_YC = 15.0
TORSO_C_UP, TORSO_N_UP = 60.0, 2.2      # top z 100 (inside the head)
TORSO_C_DN, TORSO_N_DN = 40.0, 2.0      # 43 deg taper at the deck (<= 45 rule)
# thighs (haunches): the concept shows the body side bulging to x +/-53 at z ~45;
# placed forward (over the feet) so the tail can curl up behind them
HAUNCH_C = (37.0, -4.0, 40.0)
HAUNCH_R = (16.0, 21.0, 17.0)
HAUNCH_BLEND = 8.0

# ---- arms (round-cone chain shoulder -> elbow -> wrist) and paws (ellipsoids)
ARM_PTS = ((34.0, 12.0, 86.0, 12.0), (45.0, 3.0, 67.0, 10.0), (42.5, -11.0, 62.0, 9.5))  # (x,y,z,r), +X side
PAW_C = (43.0, -18.0, 62.0)             # spec centre (y moved 2 back to sit on the pumpkin side)
PAW_R = (10.5, 12.0, 12.5)              # W 21 x D 24 x H 25 (concept paw 25 tall)
# three finger bumps on the paw's inner-front side, stacked vertically (concept)
FINGERS = ((37.8, -26.5, 70.3), (37.2, -27.8, 62.0), (37.8, -26.5, 53.7))
FINGER_R = (5.6, 6.4, 4.6)
FINGER_BLEND = 1.2
ARM_BLEND, PAW_BLEND, SHOULDER_BLEND = 4.0, 4.0, 2.5

# ---- hind feet (ellipsoids sitting on the deck)
FOOT_C = (36.0, -24.0, 23.0)            # +X side, mirrored
FOOT_R = (12.5, 15.0, 13.0)             # W 25 x D 30 x H ~20 above the deck
FOOT_BLEND = 3.0

# ---- tail: round-cone chain on the +X side, lying on the deck around the
# rear-right of the torso and curling up behind the right thigh.  Centreline
# kept at r <= 47.5 so tube radius 9.5 stays inside r 57 (spec).
TAIL_PTS = ((5.0, 45.0, 19.5, 8.5), (21.0, 41.5, 20.0, 9.5), (34.0, 32.0, 21.0, 9.5),
            (42.0, 20.5, 24.5, 9.5), (43.5, 17.0, 33.0, 9.5), (41.5, 20.0, 41.0, 9.0))
TAIL_BLEND = 1.5                        # crisp crease so it reads as a separate tail

# ---- pumpkin: lofted, lower half boxier (broader seat -> larger plenum link)
PK_ZW = PUMPKIN_CENTER[2]               # 51
PK_A, PK_B = PUMPKIN_W / 2.0, PUMPKIN_D / 2.0     # 43.5, 40
PK_YC = PUMPKIN_CENTER[1]               # -15
PK_C_UP, PK_N_UP = 35.0, 2.0
PK_C_DN, PK_N_DN = 35.0, 2.5
RIB_N = 10                              # grooves around; the face segment centred on -Y
RIB_DEPTH = 0.8                         # <= RIB_DEPTH_MAX 1.0
RIB_POWER = 6.0                         # narrow valleys
RIB_FACE_CLEAR = 4.0                    # ribs fully faded this far outside any window (>= 2 spec)
RIB_FADE_W = 4.0                        # fade band width beyond that

# ---- stem (solid, green)
STEM_XY = (0.0, -20.0)                  # moved 5 mm forward of the pumpkin axis to clear the chin
STEM_Z0, STEM_Z1 = 82.0, 96.0           # spec
STEM_R0, STEM_R1 = STEM_BASE_D / 2.0, STEM_TOP_D / 2.0
STEM_TOP_ROUND = 1.5
STEM_BLEND = 2.5

# ---- plinth: low hidden pad on the deck under the figure.  Without it the
# figure's footprint left the deck bare (or 0.5 mm covered) in small gaps
# between the pumpkin skirt, the feet and the torso right at the Ø54 plenum
# bore edge, so the bore wall came within 0.5-0.8 mm of the outside
# (measured, A7).  The pad covers r <= 29.5 up to z 19 with >= 3 mm over the
# bore; it is hidden under the figure except in those crease gaps.
PAD_PROFILE = ((0.0, 12.0), (31.5, 12.0), (31.5, 17.0), (27.5, 21.0), (0.0, 21.0))
PAD_BLEND = 2.5

# ---- blends and base fillet
NECK_BLEND = 2.0                        # small: keeps the visible neck crease (spec 7 seams)
PUMPKIN_BLEND = 1.0                     # pumpkin vs cat: crisp crease
DECK_BLEND = 2.0                        # figure-to-deck fillet
SKIRT_DEG = 45.0                        # auto 45 deg skirt under forms meeting the deck
SKIRT_Z_TOP = 34.0                      # skirt recursion band 16..34

# ---- chamber
CHAMBER_FLOOR_Z = BASE_H                # cavity floors on the deck (16)
CHAMBER_SELECT_SLACK = 0.3              # component selector is 0.3 looser than the wall
CEIL_CONE_DEG = 45.0                    # roof cone angle from vertical (spec prefers 45)
# In the front sector of each roof cone (toward the face windows) the cone is
# steeper-sided at CEIL_FRONT_DEG (spec allows <= 60; 2 deg kept for meshing).
# With 45 deg all round, 98% of each pumpkin eye and ~50% of each cat eye sat
# behind 5-15 mm of solid wall (measured), starving the windows of light.
CEIL_FRONT_DEG = 58.0
CEIL_FRONT_HALF = 50.0                  # sector half-angle about -Y (deg)
CEIL_FRONT_BLEND = 20.0                 # transition width (deg) to CEIL_CONE_DEG
HEAD_ROOF_R = 10.0                      # flat head roof dia 20 (bridge <= 20)
HEAD_ROOF_XY = (0.0, 12.0)
PK_ROOF_R = 15.0                        # flat pumpkin roof dia 30 (bridge <= 30)
PK_ROOF_XY = (0.0, -17.0)
# roof seeds (flat bridge discs); first = main roof.  The two extra seeds sit
# behind the upper part of each pumpkin eye so the chamber reaches the whole
# window; cones from different seeds meet in arch-shaped creases (highest in
# the middle, descending to the walls), which stay self-supporting.
PK_EYE_SEED_XY = (15.5, -31.0)
PK_EYE_SEED_R = 6.0
PK_ROOF_SEEDS = [(PK_ROOF_XY, PK_ROOF_R)]
# (tested: extra disc seeds behind the eyes did not help; replaced by point
# apexes behind every window column, figure_shapes.window_apex_roof)
NECK_STADIUM = (0.0, 15.0, 6.0, 16.0)   # neck bore (cx, cy, half-length along X, radius): 44 x 32, 1188 mm2
NECK_Z = (84.0, 97.0)                   # neck bore prism z range (inside torso and head cavities)
TORSO_ROOF_Z = 97.0                     # torso funnel apex plane (inside the head cavity)
PLENUM_STUB_R = 25.0                    # SDF plenum stub (inside the exact r 27 bore)
PLENUM_STUB_Z0 = 12.5
PLENUM_FLARE_Z = 14.5                   # 45 deg flare starts here (meets r 27 at z 16.5)
PLENUM_DIAMOND_Z = 19.0                 # flare widens to here (r 29.5), then closes at 45 deg
BASE_VOID_TOP = BASE_H + 2.0            # exact stage-1 void extended to z 18 (inside chamber)

# ---- windows (outer-surface outlines, projected along Y)
WINDOW_EPS = 0.08                       # pocket floor runs this far past the outline (no coincident edges)
WINDOW_BACK_OVERLAP = 0.6               # pocket cutter reaches this far into the chamber
YELLOW_BACK = 0.3                       # yellow zone back face this far behind the skin (in the pocket void)
INLAY_FRONT = 1.5                       # zone front caps this far in front of the surface
PK_FACE_Z = {"eye": PK_EYE_Z, "nose": PK_NOSE_Z, "mouth": PK_MOUTH_Z}

# ================================================================= end stage 2


def hex_to_rgba(h, a=1.0):
    h = h.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    return (lin[0], lin[1], lin[2], a)


def arm_angles(phi_c):
    """Angular layout (deg) of one flex arm around tab centre phi_c.
    Returns dict: tab (lo, hi), root, free, gap_end."""
    a_t = math.degrees(math.asin((TAB_CHORD / 2.0) / tab_tip_r()))
    to_deg = lambda s: math.degrees(s / ARM_R_MID)
    if ARM_ROOT_SIDE < 0:
        root = phi_c - a_t - to_deg(ARM_LEN)
        free = phi_c + a_t + to_deg(ARM_TIP_MARGIN)
        gap_end = free + to_deg(ARM_END_GAP)
    else:
        root = phi_c + a_t + to_deg(ARM_LEN)
        free = phi_c - a_t - to_deg(ARM_TIP_MARGIN)
        gap_end = free - to_deg(ARM_END_GAP)
    return {"tab": (phi_c - a_t, phi_c + a_t), "root": root, "free": free,
            "gap_end": gap_end, "tab_half_deg": a_t}


def as_dict():
    return {k: v for k, v in globals().items()
            if k.isupper() and not k.startswith("_")}
