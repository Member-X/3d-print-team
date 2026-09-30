"""Stage-1 test parts for the Halloween cat "Pumpkin Hug": base fit coupon,
rigid-tab fallback coupon, skin calibration tile (+ flat-print variant) and the
non-exported reference dummies.  Every dimension comes from params.py.

Run inside Blender:
    import sys, importlib
    sys.path.insert(0, r"H:/ClaudeStuff/3d-print-team/halloween-cats/blender")
    import build_test_parts as B; importlib.reload(B); B.build_all()
"""
import bpy
import bmesh
import math
import sys
import importlib

HERE = r"H:\ClaudeStuff\3d-print-team\halloween-cats\blender"
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import params as P  # noqa: E402
importlib.reload(P)

COLL_PARTS = "TEST_PARTS"
COLL_REF = "REF_dummies_no_export"
COLL_WORK = "WORK_temp"

NAME_COUPON = "base-fit-coupon"
NAME_COUPON_RIGID = "base-fit-coupon_rigid-tabs-0.6"
NAME_TILE = "skin-calibration-tile"
NAME_TILE_FLAT = "skin-calibration-tile_flat-print"

DISPLAY_OFFSET = {NAME_COUPON: (0.0, 0.0, 0.0),
                  NAME_COUPON_RIGID: (-110.0, 0.0, 0.0),
                  NAME_TILE: (100.0, 0.0, 0.0),
                  NAME_TILE_FLAT: (100.0, 45.0, 0.0)}


# ------------------------------------------------------------------ helpers
def coll(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c


def remove_obj(name):
    ob = bpy.data.objects.get(name)
    if ob is None:
        return
    me = ob.data if ob.type == 'MESH' else None
    bpy.data.objects.remove(ob, do_unlink=True)
    if me is not None and me.users == 0:
        bpy.data.meshes.remove(me)


def bm_to_obj(bm, name, collection, color=None):
    remove_obj(name)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    collection.objects.link(ob)
    if color is not None:
        ob.color = color
    return ob


def _xy(r, phi_deg):
    a = math.radians(phi_deg)
    return r * math.sin(a), r * math.cos(a)


def revolve_bm(profile, phi0=None, phi1=None, seg=None, seg_deg=None, phase=0.0):
    """Revolve a closed (r, z) polygon about Z.  Full revolve when phi0 is None
    (points with r == 0 become poles); otherwise a capped sweep phi0..phi1 (deg,
    PHI from +Y toward +X).
    phase: fraction of a facet by which the angular grid is shifted.  Every
    part of one boolean chain uses a different phase so facet edges of two
    operands never nearly coincide (near-coincident edges make the EXACT
    solver emit near-duplicate vertices and micro-slivers)."""
    seg = seg or P.SEG_FULL
    seg_deg = seg_deg or P.SEG_DEG_PARTIAL
    bm = bmesh.new()
    full = phi0 is None
    if full:
        angs = [360.0 * (k + phase) / seg for k in range(seg)]
    else:
        lo, hi = min(phi0, phi1), max(phi0, phi1)
        j0 = int(math.floor(lo / seg_deg)) - 1
        j1 = int(math.ceil(hi / seg_deg)) + 1
        guard = 0.1 * seg_deg
        grid = [(j + phase) * seg_deg for j in range(j0, j1 + 1)]
        inner = [g for g in grid if lo + guard < g < hi - guard]
        angs = [lo] + inner + [hi]
    rings = []
    for (r, z) in profile:
        if full and r <= 1e-9:
            rings.append(bm.verts.new((0.0, 0.0, z)))
        else:
            if r <= 0:
                raise ValueError("partial sweep profile touches the axis")
            rings.append([bm.verts.new((*_xy(r, a), z)) for a in angs])
    m = len(profile)
    L = len(angs)
    nseg = L if full else L - 1
    for i in range(m):
        A, B = rings[i], rings[(i + 1) % m]
        ar, br = isinstance(A, list), isinstance(B, list)
        if not ar and not br:
            continue
        for k in range(nseg):
            k1 = (k + 1) % L
            if ar and br:
                f = (A[k], A[k1], B[k1], B[k])
            elif ar:
                f = (A[k], A[k1], B)
            else:
                f = (A, B[k1], B[k])
            bm.faces.new(f)
    if not full:
        bm.faces.new([rings[i][0] for i in range(m)])
        bm.faces.new([rings[i][-1] for i in reversed(range(m))])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return bm


def prism_bm(poly, axis, a0, a1):
    """Extrude a closed 2D polygon along an axis.  axis 'Y': poly is (x, z);
    axis 'X': poly is (y, z)."""
    bm = bmesh.new()

    def co(p, a):
        return (p[0], a, p[1]) if axis == 'Y' else (a, p[0], p[1])
    va = [bm.verts.new(co(p, a0)) for p in poly]
    vb = [bm.verts.new(co(p, a1)) for p in poly]
    n = len(poly)
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((va[i], va[j], vb[j], vb[i]))
    bm.faces.new(va)
    bm.faces.new(list(reversed(vb)))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return bm


def cyl_y_bm(bm, cx, cz, r, y0, y1, seg=48):
    """Append a closed cylinder along Y to an existing bmesh."""
    a = [bm.verts.new((cx + r * math.cos(2 * math.pi * k / seg), y0,
                       cz + r * math.sin(2 * math.pi * k / seg))) for k in range(seg)]
    b = [bm.verts.new((v.co.x, y1, v.co.z)) for v in a]
    for k in range(seg):
        j = (k + 1) % seg
        bm.faces.new((a[k], a[j], b[j], b[k]))
    bm.faces.new(a)
    bm.faces.new(list(reversed(b)))
    return bm


def frustum_y_bm(xc, zc, w, h, y0, y1, flank_deg):
    """Pocket cutter: w x h rectangle at y0 (the skin side), flaring by
    flank_deg (from the pocket axis) toward y1."""
    e = (y1 - y0) * math.tan(math.radians(flank_deg))
    bm = bmesh.new()

    def rect(y, ex):
        return [bm.verts.new((xc + sx * (w / 2 + ex), y, zc + sz * (h / 2 + ex)))
                for sx, sz in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    a = rect(y0, 0.0)
    b = rect(y1, e)
    for i in range(4):
        j = (i + 1) % 4
        bm.faces.new((a[i], a[j], b[j], b[i]))
    bm.faces.new(a)
    bm.faces.new(list(reversed(b)))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    return bm


def apply_boolean(target, cutter, op):
    """Apply an EXACT boolean (op: DIFFERENCE / UNION / INTERSECT) in place."""
    mod = target.modifiers.new("bool_tmp", 'BOOLEAN')
    mod.operation = op
    mod.solver = 'EXACT'
    mod.object = cutter
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    ev = target.evaluated_get(dg)
    new = bpy.data.meshes.new_from_object(ev)
    old = target.data
    target.modifiers.remove(mod)
    new.name = old.name
    target.data = new
    if old.users == 0:
        bpy.data.meshes.remove(old)
    return target


# ------------------------------------------------------------------ coupon
def pocket_void_profile(height):
    rp, ce, ct = P.POCKET_R, P.POCKET_ENTRY_CHAMFER, P.POCKET_TOP_CHAMFER
    ra, rpl, D = P.APERTURE_D / 2, P.PLENUM_D / 2, P.POCKET_DEPTH
    zb = -1.0
    prof = [(0.0, zb), (rp + ce - zb, zb), (rp, ce), (rp, D - ct), (rp - ct, D), (ra, D)]
    if abs(rpl - ra) > 1e-9:
        prof += [(ra, P.SHELF_Z1), (rpl, P.SHELF_Z1)]
    prof += [(rpl, height + 1.0), (0.0, height + 1.0)]
    return prof


def tunnel_poly():
    w, h, c = P.TUNNEL_W, P.TUNNEL_H, P.TUNNEL_CHAMFER
    return [(-w / 2, -1.2), (w / 2, -1.2), (w / 2, h - c), (w / 2 - c, h),
            (-w / 2 + c, h), (-w / 2, h - c)]


def tab_profile(engage):
    rp = P.POCKET_R
    rt = P.tab_tip_r(engage)
    return [(rp + 0.5, -0.5), (rt, rp - rt), (rt, P.TAB_TOP_Z),
            (rp + 0.8, P.TAB_TOP_Z), (rp + 0.8, -0.5)]


def tab_half_deg(engage):
    return math.degrees(math.asin((P.TAB_CHORD / 2.0) / P.tab_tip_r(engage)))


def build_coupon(name=NAME_COUPON, variant="flex"):
    """variant 'flex' = snap tabs on flex arms (TAB_ENGAGE);
    'rigid' = spec fallback, rigid tabs, TAB_ENGAGE_FALLBACK."""
    parts, work = coll(COLL_PARTS), coll(COLL_WORK)
    engage = P.TAB_ENGAGE if variant == "flex" else P.TAB_ENGAGE_FALLBACK
    R, H = P.COUPON_D / 2, P.COUPON_H
    cb, ct = P.COUPON_BOTTOM_CHAMFER, P.COUPON_TOP_CHAMFER
    solid = bm_to_obj(revolve_bm([(0, 0), (R - cb, 0), (R, cb), (R, H - ct), (R - ct, H), (0, H)]),
                      name, parts, P.hex_to_rgba(P.COLORS["black"]))
    # angular grid phases: solid 0, void 0.5 deg, arm cutter +0.25, arm body +0.125, tab +0.375
    void = bm_to_obj(revolve_bm(pocket_void_profile(H), phase=0.5), "_void", work)
    tun = bm_to_obj(prism_bm(tunnel_poly(), 'Y', 20.0, R + 5.0), "_tunnel", work)
    apply_boolean(void, tun, 'UNION')
    remove_obj("_tunnel")
    if variant == "flex":
        for phi in P.TAB_ANGLES:
            g = P.arm_angles(phi)
            lo, hi = sorted((g["root"], g["gap_end"]))
            C = P.RELIEF_CEIL_C
            f_prof = [(30.0, -1.5), (P.SLOT_R_OUT, -1.5), (P.SLOT_R_OUT, C - P.SLOT_R_OUT),
                      (30.0, C - 30.0)]
            F = bm_to_obj(revolve_bm(f_prof, lo, hi, phase=0.5), "_armcut", work)
            # arm body extends 2 deg past the root so its root cap lies outside F
            if P.ARM_ROOT_SIDE < 0:
                a_lo, a_hi = g["root"] - 2.0, g["free"]
            else:
                a_lo, a_hi = g["free"], g["root"] + 2.0
            a_prof = [(29.5, -2.0), (P.ARM_R_OUT, -2.0), (P.ARM_R_OUT, P.ARM_H), (29.5, P.ARM_H)]
            A = bm_to_obj(revolve_bm(a_prof, a_lo, a_hi, phase=0.25), "_arm", work)
            apply_boolean(F, A, 'DIFFERENCE')
            remove_obj("_arm")
            apply_boolean(void, F, 'UNION')
            remove_obj("_armcut")
    ht = tab_half_deg(engage)
    for phi in P.TAB_ANGLES:
        T = bm_to_obj(revolve_bm(tab_profile(engage), phi - ht, phi + ht, phase=0.75), "_tab", work)
        apply_boolean(void, T, 'DIFFERENCE')
        remove_obj("_tab")
    apply_boolean(solid, void, 'DIFFERENCE')
    remove_obj("_void")
    solid["variant"] = variant
    solid["tab_engage"] = engage
    solid["export"] = True
    return solid


# ------------------------------------------------------------------ dummies
def build_refs():
    ref = coll(COLL_REF)
    puck = bm_to_obj(revolve_bm([(0, P.PUCK_SEAT_Z), (P.PUCK_D / 2, P.PUCK_SEAT_Z),
                                 (P.PUCK_D / 2, P.PUCK_FACE_Z), (0, P.PUCK_FACE_Z)], seg=180),
                     "REF_puck", ref, (0.35, 0.6, 1.0, 1.0))
    z1 = P.PUCK_FACE_Z + P.PUCK_RING_H
    ring = bm_to_obj(revolve_bm([(0, P.PUCK_FACE_Z), (P.PUCK_RING_D / 2, P.PUCK_FACE_Z),
                                 (P.PUCK_RING_D / 2, z1), (0, z1)], seg=180),
                     "REF_puck_ring", ref, (0.1, 0.9, 0.9, 1.0))
    ring.parent = puck
    y0, y1 = P.PUCK_D / 2, P.BASE_D / 2 + 10.0
    out = [puck, ring]
    for d, nm, colr in ((P.CABLE_D, "REF_cable_4", (1.0, 0.15, 0.15, 1.0)),
                        (P.CABLE_D_CHECK, "REF_cable_5", (0.85, 0.2, 0.9, 1.0))):
        bm = bmesh.new()
        cyl_y_bm(bm, 0.0, P.CABLE_EXIT_Z_NOM, d / 2, y0, y1, seg=64)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
        out.append(bm_to_obj(bm, nm, ref, colr))
    for o in out:
        o["export"] = False
    return out


# ------------------------------------------------------------------ tile
def build_tile(name=NAME_TILE, dots="raised"):
    """dots 'raised' (spec: 1.6 x 0.4 bumps on the front face) or 'recessed'
    (same dots sunk 0.4 into the front face so the front can lie flat)."""
    parts, work = coll(COLL_PARTS), coll(COLL_WORK)
    T, W, Ht = P.TILE_T, P.TILE_W, P.TILE_H
    fd, ft = P.TILE_FOOT_D, P.TILE_FOOT_T
    L = [(0.0, 0.0), (fd, 0.0), (fd, ft), (T, ft), (T, Ht), (0.0, Ht)]
    tile = bm_to_obj(prism_bm(L, 'X', -W / 2, W / 2), name, parts,
                     P.hex_to_rgba(P.COLORS["yellow"]))
    y1 = T + 0.5
    for x, t in zip(P.TILE_POCKET_X, P.TILE_SKINS):
        cut = bm_to_obj(frustum_y_bm(x, P.TILE_POCKET_ZC, P.TILE_POCKET_W, P.TILE_POCKET_H,
                                     t, y1, P.TILE_FLANK_DEG), "_pocket", work)
        apply_boolean(tile, cut, 'DIFFERENCE')
        remove_obj("_pocket")
    bm = bmesh.new()
    r = P.TILE_DOT_D / 2
    for i, x in enumerate(P.TILE_POCKET_X):
        n = i + 1
        for k in range(n):
            dx = (k - (n - 1) / 2.0) * P.TILE_DOT_PITCH
            if dots == "raised":
                cyl_y_bm(bm, x + dx, P.TILE_DOT_Z, r, -P.TILE_DOT_H, 0.3, seg=32)
            else:
                cyl_y_bm(bm, x + dx, P.TILE_DOT_Z, r, -0.3, P.TILE_DOT_H, seg=32)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    dob = bm_to_obj(bm, "_dots", work)
    apply_boolean(tile, dob, 'UNION' if dots == "raised" else 'DIFFERENCE')
    remove_obj("_dots")
    tile["dots"] = dots
    tile["export"] = True
    return tile


def place_for_display():
    for nm, off in DISPLAY_OFFSET.items():
        ob = bpy.data.objects.get(nm)
        if ob:
            ob.location = off


def cleanup_work():
    c = bpy.data.collections.get(COLL_WORK)
    if c:
        for o in list(c.objects):
            remove_obj(o.name)
        bpy.data.collections.remove(c)


def build_all():
    build_refs()
    build_coupon(NAME_COUPON, "flex")
    build_coupon(NAME_COUPON_RIGID, "rigid")
    build_tile(NAME_TILE, "raised")
    build_tile(NAME_TILE_FLAT, "recessed")
    cleanup_work()
    place_for_display()
