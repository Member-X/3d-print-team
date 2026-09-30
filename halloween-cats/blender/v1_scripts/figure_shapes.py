"""Implicit-field model of the "Pumpkin Hug" figure (stage 2).

All shapes are (approximately) signed distance fields in mm, negative inside,
sampled on one regular grid (params GRID_*, voxel GRID_H).  The three lofted
bodies (head, torso, pumpkin) are first written as sign-correct implicits,
meshed with OpenVDB and turned back into TRUE signed distance fields, so
every blend radius, skirt and zone bisector below works in real millimetres.

Main entry points (used by build_figure.py):
    g = Grid()
    comps = components(g)          # dict of per-component SDF arrays
    fields = compose(g, comps)     # envelope E, zone fields, selectors
    C = chamber(g, fields, D_out)  # chamber field (needs D_out, see build)
Runs inside Blender (numpy + openvdb); no bpy needed here.
"""
import json
import math
import os

import numpy as np

import params as P

HERE = os.path.dirname(os.path.abspath(__file__))
FAR = 60.0
SQ2 = math.sqrt(2.0)


# ================================================================== grid
class Grid:
    def __init__(self, lo=P.GRID_LO, hi=P.GRID_HI, h=P.GRID_H):
        self.h = float(h)
        self.i0 = [int(round(v / h)) for v in lo]
        self.i1 = [int(round(v / h)) for v in hi]
        self.n = tuple(int(b - a + 1) for a, b in zip(self.i0, self.i1))
        self.ax = [(np.arange(a, b + 1) * self.h).astype(np.float32) for a, b in zip(self.i0, self.i1)]

    def full(self, v=FAR):
        return np.full(self.n, v, np.float32)

    def sub(self, lo, hi):
        sl = []
        for d in range(3):
            a = max(0, int(math.floor(lo[d] / self.h)) - self.i0[d])
            b = min(self.n[d], int(math.ceil(hi[d] / self.h)) - self.i0[d] + 1)
            sl.append(slice(a, b))
        X = self.ax[0][sl[0]][:, None, None]
        Y = self.ax[1][sl[1]][None, :, None]
        Z = self.ax[2][sl[2]][None, None, :]
        return tuple(sl), X, Y, Z

    def ijk(self, sl):
        return tuple(int(self.i0[d] + sl[d].start) for d in range(3))

    def kz(self, z):
        return int(round(z / self.h)) - self.i0[2]


# ================================================================== ops
def smin(a, b, k):
    if k <= 0:
        return np.minimum(a, b)
    h = np.maximum(k - np.abs(a - b), 0.0) / k
    return np.minimum(a, b) - h * h * (k * 0.25)


def smax(a, b, k):
    return -smin(-a, -b, k)


def put(F, sl, D, k=0.0):
    """F[sl] = smooth-union(F[sl], D) in place."""
    F[sl] = smin(F[sl], D.astype(np.float32), k)


def profile(t, n):
    t = np.clip(t, 0.0, 1.0)
    return np.power(np.maximum(1.0 - np.power(t, n), 0.0), 1.0 / n)


# ================================================================== primitives
def sd_ellipsoid(X, Y, Z, c, r):
    x = (X - c[0]) / r[0]
    y = (Y - c[1]) / r[1]
    z = (Z - c[2]) / r[2]
    k0 = np.sqrt(x * x + y * y + z * z)
    k1 = np.sqrt((x / r[0]) ** 2 + (y / r[1]) ** 2 + (z / r[2]) ** 2)
    # at (and right next to) the exact centre the formula is 0/0; use the
    # true value there (minus the smallest semi-axis)
    return np.where(k1 < 1e-4, -min(r), k0 * (k0 - 1.0) / np.maximum(k1, 1e-9))


def sd_round_cone(X, Y, Z, a, b, r1, r2):
    """Exact SDF of a round cone (capsule with radii r1 at a, r2 at b)."""
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    ba = b - a
    l2 = float(ba @ ba)
    rr = r1 - r2
    a2 = l2 - rr * rr
    il2 = 1.0 / l2
    pax, pay, paz = X - a[0], Y - a[1], Z - a[2]
    y = pax * ba[0] + pay * ba[1] + paz * ba[2]
    z = y - l2
    qx = pax * l2 - ba[0] * y
    qy = pay * l2 - ba[1] * y
    qz = paz * l2 - ba[2] * y
    x2 = qx * qx + qy * qy + qz * qz
    y2 = y * y * l2
    z2 = z * z * l2
    k = math.copysign(1.0, rr) * rr * rr * x2
    d1 = np.sqrt(x2 + z2) * il2 - r2
    d2 = np.sqrt(x2 + y2) * il2 - r1
    d3 = (np.sqrt(np.maximum(x2 * a2 * il2, 0.0)) + y * rr) * il2 - r1
    return np.where(np.sign(z) * a2 * z2 > k, d1, np.where(np.sign(y) * a2 * y2 < k, d2, d3))


def sd_polygon2(px, py, poly):
    """Exact 2D SDF (negative inside) of one closed polygon, vectorised over
    arbitrary broadcastable arrays px, py."""
    d2 = None
    s = np.ones(np.broadcast(px, py).shape, np.float32)
    n = len(poly)
    for i in range(n):
        ax, ay = poly[i]
        bx, by = poly[i - 1]
        ex, ey = bx - ax, by - ay
        wx, wy = px - ax, py - ay
        ee = ex * ex + ey * ey
        t = np.clip((wx * ex + wy * ey) / ee, 0.0, 1.0)
        dx, dy = wx - ex * t, wy - ey * t
        dd = dx * dx + dy * dy
        d2 = dd if d2 is None else np.minimum(d2, dd)
        c1 = py >= ay
        c2 = py < by
        c3 = ex * wy > ey * wx
        flip = (c1 & c2 & c3) | (~c1 & ~c2 & ~c3)
        s = np.where(flip, -s, s)
    return s * np.sqrt(d2)


def sd_triangle2(px, py, a, b, c):
    return sd_polygon2(px, py, [a, b, c])


def sd_revolve(X, Y, Z, prof_rz, cx=0.0, cy=0.0):
    """SDF of a solid of revolution about the vertical axis through (cx, cy);
    prof_rz is the half-profile polygon (r >= 0); it is mirrored so the axis is
    not a boundary."""
    prof = np.asarray(prof_rz, float)
    right = [p for p in prof if p[0] > 1e-9]
    mirror = [(-p[0], p[1]) for p in reversed(right)]
    poly = [tuple(p) for p in right] + mirror
    r = np.sqrt((X - cx) ** 2 + (Y - cy) ** 2)
    return sd_polygon2(r, Z + 0.0 * r, poly)


def arc_pts(cx, cz, rad, a0, a1, n):
    return [(cx + rad * math.cos(a0 + (a1 - a0) * i / n), cz + rad * math.sin(a0 + (a1 - a0) * i / n))
            for i in range(n + 1)]


def base_profile():
    R, H = P.BASE_D / 2.0, P.BASE_H
    cb, rf = P.BASE_BOTTOM_CHAMFER, P.BASE_TOP_FILLET
    prof = [(0.0, 0.0), (R - cb, 0.0), (R, cb)]
    prof += arc_pts(R - rf, H - rf, rf, 0.0, math.pi / 2, 24)
    prof += [(0.0, H)]
    return prof


def stem_profile():
    """Half profile (r, z) of the stem: frustum r0 at z0 -> r1 at z1 (flat top)
    with the top outer edge rounded by STEM_TOP_ROUND; bottom 1 mm below z0
    (buried in the pumpkin)."""
    z0, z1 = P.STEM_Z0, P.STEM_Z1
    r0, r1, rr = P.STEM_R0, P.STEM_R1, P.STEM_TOP_ROUND
    dr, dz = r1 - r0, z1 - z0
    L = math.hypot(dr, dz)
    nr, nz = -dz / L, dr / L                    # side normal pointing into the solid (toward the axis)
    cz = z1 - rr                                # fillet centre: rr below the top ...
    cr = r0 + (rr - (cz - z0) * nz) / nr        # ... and rr inside the side line
    a_side = math.atan2(-nz, -nr)               # centre -> side tangency
    a_top = math.pi / 2                         # centre -> top tangency
    rb = r0 + dr * (-1.0) / dz                  # side line extended 1 mm below z0
    prof = [(0.0, z0 - 1.0), (rb, z0 - 1.0)]
    prof += arc_pts(cr, cz, rr, a_side, a_top, 12)
    prof += [(0.0, z1)]
    return prof


# ================================================================== lofted bodies
def lofted_G(X, Y, Z, zc, A, B, yc, c_up, nx_up, ny_up, c_dn, nx_dn, ny_dn):
    """Sign-correct implicit (roughly mm) of a body whose horizontal sections
    are ellipses a(z) x b(z) about (0, yc); a = A*s(t, nx), b = B*s(t, ny),
    s = (1-t^n)^(1/n), t = |z-zc|/c (c, n per half)."""
    up = Z >= zc
    t = np.where(up, (Z - zc) / c_up, (zc - Z) / c_dn)
    nx = np.where(up, nx_up, nx_dn)
    ny = np.where(up, ny_up, ny_dn)
    a = np.maximum(A * profile(t, nx), 1e-3)
    b = np.maximum(B * profile(t, ny), 1e-3)
    rn = np.sqrt((X / a) ** 2 + ((Y - yc) / b) ** 2)
    G = (rn - 1.0) * np.minimum(a, b)
    zpole = np.where(up, zc + c_up, zc - c_dn)
    G = np.where(t >= 1.0, np.sqrt(X * X + (Y - yc) ** 2 + (Z - zpole) ** 2), G)
    return G.astype(np.float32)


def to_true_sdf(g, G, sl, band_vox=18):
    """Mesh the implicit G (sub-block sl of grid g) with OpenVDB and return the
    true SDF on the same sub-block (clamped to +/- band_vox*h)."""
    import openvdb as vdb
    tr = vdb.createLinearTransform(voxelSize=g.h)
    grid = vdb.FloatGrid(background=float(FAR))
    grid.transform = tr
    grid.copyFromArray(np.ascontiguousarray(np.clip(G, -FAR, FAR).astype(np.float32)), ijk=g.ijk(sl))
    pts, quads = grid.convertToQuads(0.0)
    ls = vdb.FloatGrid.createLevelSetFromPolygons(
        pts.astype(np.float32), quads=quads.astype(np.uint32), transform=tr,
        exBandWidth=float(band_vox), inBandWidth=float(band_vox))
    out = np.zeros(G.shape, np.float32)
    ls.copyToArray(out, ijk=g.ijk(sl))
    return out, len(pts), len(quads)


def body_head(g):
    pad = 12.0
    lo = (-P.HEAD_A - pad, P.HEAD_YC - P.HEAD_B - pad, P.HEAD_ZW - P.HEAD_C_DN - pad)
    hi = (P.HEAD_A + pad, P.HEAD_YC + P.HEAD_B + pad, P.HEAD_ZW + P.HEAD_C_UP + pad)
    sl, X, Y, Z = g.sub(lo, hi)
    G = lofted_G(X, Y, Z, P.HEAD_ZW, P.HEAD_A, P.HEAD_B, P.HEAD_YC,
                 P.HEAD_C_UP, P.HEAD_NX_UP, P.HEAD_NY_UP, P.HEAD_C_DN, P.HEAD_NX_DN, P.HEAD_NY_DN)
    D, nv, nq = to_true_sdf(g, G, sl)
    return sl, D


def body_torso(g):
    pad = 12.0
    lo = (-P.TORSO_A - pad, P.TORSO_YC - P.TORSO_B - pad, 8.0)
    hi = (P.TORSO_A + pad, P.TORSO_YC + P.TORSO_B + pad, P.TORSO_ZW + P.TORSO_C_UP + pad)
    sl, X, Y, Z = g.sub(lo, hi)
    G = lofted_G(X, Y, Z, P.TORSO_ZW, P.TORSO_A, P.TORSO_B, P.TORSO_YC,
                 P.TORSO_C_UP, P.TORSO_N_UP, P.TORSO_N_UP, P.TORSO_C_DN, P.TORSO_N_DN, P.TORSO_N_DN)
    # the torso continues straight down into the base below z 12 (hidden)
    G = np.where(Z < 12.0, np.maximum(G[:, :, [g.kz(12.0) - sl[2].start]], 12.0 - Z - 20.0), G)
    D, nv, nq = to_true_sdf(g, G, sl)
    return sl, D


def body_pumpkin(g):
    pad = 12.0
    lo = (-P.PK_A - pad, P.PK_YC - P.PK_B - pad, 8.0)
    hi = (P.PK_A + pad, P.PK_YC + P.PK_B + pad, P.PK_ZW + P.PK_C_UP + pad)
    sl, X, Y, Z = g.sub(lo, hi)
    G = lofted_G(X, Y, Z, P.PK_ZW, P.PK_A, P.PK_B, P.PK_YC,
                 P.PK_C_UP, P.PK_N_UP, P.PK_N_UP, P.PK_C_DN, P.PK_N_DN, P.PK_N_DN)
    D, nv, nq = to_true_sdf(g, G, sl)
    return sl, D


# ================================================================== face outlines
_OUTL = None


def outlines():
    global _OUTL
    if _OUTL is None:
        with open(os.path.join(HERE, "face_outlines.json")) as f:
            d = json.load(f)
        _OUTL = {k: [np.asarray(l, float) for l in v] for k, v in d["outlines"].items()}
    return _OUTL


def outline_sdf2(name, px, pz):
    loops = outlines()[name]
    d = sd_polygon2(px, pz, loops[0])
    for hole in loops[1:]:
        d = np.maximum(d, -sd_polygon2(px, pz, hole))
    return d


PK_WINDOWS = ("pk_eye_L", "pk_eye_R", "pk_nose", "pk_mouth")
CAT_WINDOWS = ("cat_eye_L", "cat_eye_R")
WINDOWS = CAT_WINDOWS + PK_WINDOWS
INLAYS = ("cat_nose", "cat_mouth")


# ================================================================== small parts
def part_ear(g, side):
    """side -1 = left ear (x < 0), +1 = right ear (mirror)."""
    lo = (-45.0 if side < 0 else 8.0, -5.0, 112.0)
    hi = (-8.0 if side < 0 else 45.0, 30.0, 153.0)
    sl, X, Y, Z = g.sub(lo, hi)
    xq = X if side < 0 else -X
    al = math.radians(P.EAR_TILT_DEG)
    yw, zw = Y - P.EAR_Y, Z - P.EAR_Z_PIVOT
    yl = yw * math.cos(al) - zw * math.sin(al)
    zl = yw * math.sin(al) + zw * math.cos(al) + P.EAR_Z_PIVOT
    a, b, c = P.EAR_TRI
    d2 = sd_triangle2(xq + 0.0 * zl, zl + 0.0 * xq, a, b, c) - P.EAR_R
    z0, z1 = P.EAR_T_Z
    tt = np.clip((zl - z0) / (z1 - z0), 0.0, 1.0)
    t = P.EAR_T_BASE + (P.EAR_T_TIP - P.EAR_T_BASE) * tt
    dw = np.abs(yl) - 0.5 * t
    rr = P.EAR_EDGE_R
    q1, q2 = d2 + rr, dw + rr
    d = np.minimum(np.maximum(q1, q2), 0.0) + np.sqrt(np.maximum(q1, 0.0) ** 2 + np.maximum(q2, 0.0) ** 2) - rr
    # inner-ear dish on the front face (-Y side)
    cxp, czp, rx, rz, ry, depth = P.EAR_CUP
    t_c = P.EAR_T_BASE + (P.EAR_T_TIP - P.EAR_T_BASE) * min(max((czp - z0) / (z1 - z0), 0.0), 1.0)
    front = -0.5 * t_c
    cup = sd_ellipsoid(xq + 0.0 * yl, yl, zl, (cxp, front - ry + depth, czp), (rx, ry, rz))
    d = smax(d, -cup, 1.0)
    return sl, d


def part_arm(g, side):
    s = 1.0 if side > 0 else -1.0
    pts = [(s * x, y, z, r) for (x, y, z, r) in P.ARM_PTS]
    lo = (min(p[0] for p in pts) - 16, -40.0, 40.0)
    hi = (max(p[0] for p in pts) + 16, 30.0, 102.0)
    sl, X, Y, Z = g.sub(lo, hi)
    d = None
    for (p, q) in zip(pts[:-1], pts[1:]):
        dd = sd_round_cone(X, Y, Z, p[:3], q[:3], p[3], q[3])
        d = dd if d is None else smin(d, dd, P.ARM_BLEND)
    pc = (s * P.PAW_C[0], P.PAW_C[1], P.PAW_C[2])
    paw = sd_ellipsoid(X, Y, Z, pc, P.PAW_R)
    for (fx, fy, fz) in P.FINGERS:
        fg = sd_ellipsoid(X, Y, Z, (s * fx, fy, fz), P.FINGER_R)
        paw = smin(paw, fg, P.FINGER_BLEND)
    d = smin(d, paw, P.PAW_BLEND)
    return sl, d


def part_foot(g, side):
    s = 1.0 if side > 0 else -1.0
    c = (s * P.FOOT_C[0], P.FOOT_C[1], P.FOOT_C[2])
    r = P.FOOT_R
    lo = (c[0] - r[0] - 6, c[1] - r[1] - 6, 8.0)
    hi = (c[0] + r[0] + 6, c[1] + r[1] + 6, c[2] + r[2] + 6)
    sl, X, Y, Z = g.sub(lo, hi)
    return sl, sd_ellipsoid(X, Y, Z, c, r)


def part_haunch(g, side):
    s = 1.0 if side > 0 else -1.0
    c = (s * P.HAUNCH_C[0], P.HAUNCH_C[1], P.HAUNCH_C[2])
    r = P.HAUNCH_R
    lo = (c[0] - r[0] - 10, c[1] - r[1] - 10, 8.0)
    hi = (c[0] + r[0] + 10, c[1] + r[1] + 10, c[2] + r[2] + 10)
    sl, X, Y, Z = g.sub(lo, hi)
    return sl, sd_ellipsoid(X, Y, Z, c, r)


def catmull_rom(ctrl, per_seg=8):
    """Centripetal-free (uniform) Catmull-Rom through all control rows of
    ctrl (N, k); end tangents by reflection."""
    c = np.asarray(ctrl, float)
    ext = np.vstack([2 * c[0] - c[1], c, 2 * c[-1] - c[-2]])
    out = []
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        for s in range(per_seg):
            t = s / per_seg
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(c[-1])
    return np.array(out)


def tail_path():
    return catmull_rom(P.TAIL_PTS, per_seg=8)


def part_tail(g):
    pts = tail_path()
    lo = (pts[:, 0].min() - 14, pts[:, 1].min() - 14, 6.0)
    hi = (pts[:, 0].max() + 14, pts[:, 1].max() + 14, pts[:, 2].max() + 14)
    sl, X, Y, Z = g.sub(lo, hi)
    d = None
    for (p, q) in zip(pts[:-1], pts[1:]):
        dd = sd_round_cone(X, Y, Z, p[:3], q[:3], p[3], q[3])
        d = dd if d is None else np.minimum(d, dd)
    return sl, d


def part_stem(g):
    cx, cy = P.STEM_XY
    lo = (cx - 14, cy - 14, P.STEM_Z0 - 3)
    hi = (cx + 14, cy + 14, P.STEM_Z1 + 3)
    sl, X, Y, Z = g.sub(lo, hi)
    return sl, sd_revolve(X, Y, Z, stem_profile(), cx, cy)


def part_base(g):
    R = P.BASE_D / 2.0
    sl, X, Y, Z = g.sub((-R - 2, -R - 2, -2.0), (R + 2, R + 2, P.BASE_H + 8))
    return sl, sd_revolve(X, Y, Z, base_profile())


def part_pad(g):
    sl, X, Y, Z = g.sub((-40.0, -40.0, 8.0), (40.0, 40.0, 28.0))
    return sl, sd_revolve(X, Y, Z, P.PAD_PROFILE)


# ================================================================== ribs
def rib_offset(g, sl):
    """Groove depth field (>= 0, mm) to ADD to the pumpkin SDF on sub-block sl."""
    X = g.ax[0][sl[0]][:, None, None]
    Y = g.ax[1][sl[1]][None, :, None]
    Z = g.ax[2][sl[2]][None, None, :]
    phi = np.arctan2(X, -(Y - P.PK_YC))
    gr = ((1.0 - np.cos(P.RIB_N * phi)) * 0.5) ** P.RIB_POWER
    rh = np.sqrt(X * X + (Y - P.PK_YC) ** 2)
    pole = np.clip((rh - 6.0) / 8.0, 0.0, 1.0)
    # face fade: a smooth rib-free panel = rounded box around ALL pumpkin
    # windows (x, z projection); ribs start RIB_FACE_CLEAR outside it and are
    # at full depth RIB_FADE_W further out.  Only on the front half (y < yc).
    xs = g.ax[0][sl[0]]
    zs = g.ax[2][sl[2]]
    XX, ZZ = np.meshgrid(xs, zs, indexing="ij")
    x0, x1, z0, z1 = face_box()
    cx, cz, hx, hz = 0.5 * (x0 + x1), 0.5 * (z0 + z1), 0.5 * (x1 - x0), 0.5 * (z1 - z0)
    qx = np.abs(XX - cx) - hx
    qz = np.abs(ZZ - cz) - hz
    dface = np.sqrt(np.maximum(qx, 0) ** 2 + np.maximum(qz, 0) ** 2) + np.minimum(np.maximum(qx, qz), 0)
    fade2 = np.clip((dface - P.RIB_FACE_CLEAR) / P.RIB_FADE_W, 0.0, 1.0)[:, None, :]
    front = np.clip((P.PK_YC - Y) / 8.0, 0.0, 1.0)          # 0 at the back, 1 in front
    fade = 1.0 - front * (1.0 - fade2)
    return (P.RIB_DEPTH * gr * pole * fade).astype(np.float32), dface


def face_box():
    """Bounding box (x0, x1, z0, z1) of all pumpkin windows."""
    pts = np.vstack([l for w in PK_WINDOWS for l in outlines()[w]])
    return float(pts[:, 0].min()), float(pts[:, 0].max()), float(pts[:, 1].min()), float(pts[:, 1].max())


# ================================================================== skirt
def skirt(g, F, z_lo=P.BASE_H, z_hi=P.SKIRT_Z_TOP, deg=P.SKIRT_DEG):
    """45 deg self-supporting skirt under overhangs within z_lo..z_hi (in place).
    F'[k] = min(F[k], F'[k+1] + h sin(deg)): a planar 45 deg surface is a fixed
    point of this recursion, flatter overhangs are replaced by it."""
    step = g.h * math.sin(math.radians(deg))
    k1 = g.kz(z_hi)
    k0 = g.kz(z_lo)
    for k in range(k1 - 1, k0 - 1, -1):
        np.minimum(F[:, :, k], F[:, :, k + 1] + step, out=F[:, :, k])
    return F


# ================================================================== components
def components(g, log=print):
    """Every component as (sl, SDF sub-block).  Lofted bodies are true SDFs."""
    c = {}
    c["head"] = body_head(g); log("head done")
    c["torso"] = body_torso(g); log("torso done")
    c["pumpkin_noribs"] = body_pumpkin(g); log("pumpkin done")
    sl, D = c["pumpkin_noribs"]
    rib, dface = rib_offset(g, sl)
    c["pumpkin"] = (sl, D + rib)
    c["rib_offset"] = (sl, rib)
    for s, tag in ((-1, "L"), (1, "R")):
        c["ear_" + tag] = part_ear(g, s)
        c["arm_" + tag] = part_arm(g, s)
        c["foot_" + tag] = part_foot(g, s)
        c["haunch_" + tag] = part_haunch(g, s)
    c["tail"] = part_tail(g)
    c["stem"] = part_stem(g)
    c["base"] = part_base(g)
    c["pad"] = part_pad(g)
    log("parts done")
    return c


def compose(g, c, log=print):
    """Envelope E and the helper fields (all full-grid float32)."""
    f = {}
    # torso group (skirted as a group: torso + thighs), then solid limbs
    T = g.full()
    put(T, *c["torso"])
    f["torso_alone"] = T.copy()
    for tag in ("L", "R"):
        sl, D = c["haunch_" + tag]
        put(T, sl, D, P.HAUNCH_BLEND)
    skirt(g, T)
    for tag in ("L", "R"):
        FT = g.full()
        put(FT, *c["foot_" + tag])
        skirt(g, FT)
        T = smin(T, FT, P.FOOT_BLEND)
        del FT
    for tag in ("L", "R"):
        sl, D = c["arm_" + tag]
        put(T, sl, D, P.SHOULDER_BLEND)
    sl, D = c["tail"]
    put(T, sl, D, P.TAIL_BLEND)
    # head group
    H = g.full()
    put(H, *c["head"])
    f["head_alone"] = H.copy()
    for tag in ("L", "R"):
        sl, D = c["ear_" + tag]
        put(H, sl, D, P.EAR_BLEND)
    cat = smin(H, T, P.NECK_BLEND)
    del H, T
    # pumpkin (true SDF + ribs), skirted
    PK = g.full()
    put(PK, *c["pumpkin"])
    skirt(g, PK)
    f["pumpkin"] = PK
    PK0 = g.full()
    put(PK0, *c["pumpkin_noribs"])
    skirt(g, PK0)
    f["pumpkin_noribs"] = PK0
    ST = g.full()
    put(ST, *c["stem"])
    f["stem"] = ST
    BA = g.full()
    put(BA, *c["base"])
    PD = g.full()
    put(PD, *c["pad"])
    fig = smin(cat, PK, P.PUMPKIN_BLEND)
    fig = smin(fig, ST, P.STEM_BLEND)
    fig = smin(fig, PD, P.PAD_BLEND)
    E = smin(fig, BA, P.DECK_BLEND)
    BA = np.minimum(BA, PD)             # the pad belongs to the black group
    f["E"] = E
    f["black"] = np.minimum(cat, BA)
    del cat, fig, BA
    log("compose done")
    return f


def zone_fields(f):
    """Orange and green zone fields (negative inside the zone)."""
    PK, ST, BL = f["pumpkin"], f["stem"], f["black"]
    Zo = np.maximum(np.maximum(PK - BL, PK - ST), np.maximum(PK - 6.0, -PK - 30.0))
    Zg = np.maximum(np.maximum(ST - PK, ST - BL), np.maximum(ST - 6.0, -ST - 12.0))
    return Zo.astype(np.float32), Zg.astype(np.float32)


# ================================================================== chamber
def stadium_dist(X, Y, cx, cy, L, R):
    """Exact 2D distance (>= 0 outside, negative inside) to a stadium: segment
    (cx-L, cy)-(cx+L, cy) swept by radius R."""
    qx = np.maximum(np.abs(X - cx) - L, 0.0)
    return np.sqrt(qx * qx + (Y - cy) ** 2) - R


def natural_top(g, Csel, xy, R):
    """Highest z where Csel < 0 over every column of the disc (xy, R):
    returns the MIN over the disc of the column-top z."""
    xs, ys, zs = g.ax
    ix = np.nonzero(np.abs(xs - xy[0]) <= R + 1e-6)[0]
    iy = np.nonzero(np.abs(ys - xy[1]) <= R + 1e-6)[0]
    tops = []
    for i in ix:
        for j in iy:
            if (xs[i] - xy[0]) ** 2 + (ys[j] - xy[1]) ** 2 > R * R:
                continue
            col = Csel[i, j, :]
            neg = np.nonzero(col < 0)[0]
            if len(neg) == 0:
                return None
            k = neg.max()
            # interpolate the crossing between k and k+1
            a, b = col[k], col[k + 1]
            tops.append(zs[k] + g.h * a / (a - b))
    return float(min(tops))


def roof_cot(X, Y, cx, cy):
    """cot(ceiling angle) as a function of direction from the roof centre:
    CEIL_FRONT_DEG within +/-CEIL_FRONT_HALF of -Y, CEIL_CONE_DEG elsewhere,
    smooth transition.  Any mix stays <= CEIL_FRONT_DEG from vertical because
    the azimuthal variation only adds slope."""
    ang = np.degrees(np.abs(np.arctan2(X - cx, -(Y - cy))))      # 0 = straight to the front
    t = np.clip((ang - P.CEIL_FRONT_HALF) / P.CEIL_FRONT_BLEND, 0.0, 1.0)
    t = t * t * (3 - 2 * t)
    c_front = 1.0 / math.tan(math.radians(P.CEIL_FRONT_DEG))
    c_back = 1.0 / math.tan(math.radians(P.CEIL_CONE_DEG))
    return (c_front + (c_back - c_front) * t).astype(np.float32)


def window_apex_roof(g, Cnat, E, windows, cot, margin=0.6):
    """Upper envelope of cones (slope cot) with apexes at the natural cavity
    entry point behind every window column: for column (x, z) inside an
    outline (+margin), the first y behind the outer surface where Cnat < 0.
    Returns (h(x, y) array on the grid's XY plane or None, apex list)."""
    xs, ys, zs = g.ax
    apex = []
    for w in windows:
        pts = np.vstack(outlines()[w])
        x0, x1 = pts[:, 0].min() - margin, pts[:, 0].max() + margin
        z0, z1 = pts[:, 1].min() - margin, pts[:, 1].max() + margin
        ix = np.nonzero((xs >= x0) & (xs <= x1))[0]
        iz = np.nonzero((zs >= z0) & (zs <= z1))[0]
        XX, ZZ = np.meshgrid(xs[ix], zs[iz], indexing="ij")
        ins = outline_sdf2(w, XX, ZZ) < margin
        for a, i in enumerate(ix):
            for b, k in enumerate(iz):
                if not ins[a, b]:
                    continue
                e = E[i, :, k]
                jo = np.nonzero(e < 0)[0]
                if len(jo) == 0:
                    continue
                c = Cnat[i, :, k]
                jc = np.nonzero((c < 0) & (np.arange(len(c)) > jo[0]))[0]
                if len(jc) == 0:
                    continue
                j = jc[0]
                yst = ys[j - 1] + g.h * c[j - 1] / (c[j - 1] - c[j])
                apex.append((float(xs[i]), float(yst + 0.25), float(zs[k])))
    if not apex:
        return None, apex
    A = np.array(apex)
    H = np.full((len(xs), len(ys)), -1e3, np.float32)
    XX, YY = np.meshgrid(xs, ys, indexing="ij")
    for c0 in range(0, len(A), 256):
        blk = A[c0:c0 + 256]
        d = np.sqrt((XX[..., None] - blk[:, 0]) ** 2 + (YY[..., None] - blk[:, 1]) ** 2)
        H = np.maximum(H, (blk[:, 2] - cot * d).max(axis=-1))
    return H, apex


def chamber(g, f, D_out, log=print):
    """Chamber field C (negative inside the void) from the exact outer
    distance D_out.  Returns C and a dict of design values."""
    info = {}
    X = g.ax[0][:, None, None]
    Y = g.ax[1][None, :, None]
    Z = g.ax[2][None, None, :]
    cot = 1.0 / math.tan(math.radians(P.CEIL_CONE_DEG))
    PK = f["pumpkin"]
    w = (P.WALL_CAT + (P.WALL_PUMPKIN - P.WALL_CAT) *
         np.clip((6.0 - np.abs(PK)) / 3.0, 0.0, 1.0)).astype(np.float32)
    wall = (D_out + w).astype(np.float32)
    del w
    slack = P.CHAMBER_SELECT_SLACK
    floor = (P.CHAMBER_FLOOR_Z - Z).astype(np.float32)
    # ---- head cavity with a cone roof over a flat disc (bridge <= 20)
    Ch = np.maximum(f["head_alone"] + (P.WALL_CAT - slack), wall)
    zf_h = natural_top(g, Ch, P.HEAD_ROOF_XY, P.HEAD_ROOF_R)
    zf_h -= 0.3
    info["head_roof_z"] = zf_h
    dh = np.maximum(np.sqrt((X - P.HEAD_ROOF_XY[0]) ** 2 + (Y - P.HEAD_ROOF_XY[1]) ** 2) - P.HEAD_ROOF_R, 0.0)
    roof_h = zf_h - roof_cot(X, Y, *P.HEAD_ROOF_XY) * dh
    del dh
    cot_f = 1.0 / math.tan(math.radians(P.CEIL_FRONT_DEG))
    Hw, apx = window_apex_roof(g, Ch, f["E"], CAT_WINDOWS, cot_f)
    info["head_window_apexes"] = len(apx)
    if Hw is not None:
        roof_h = np.maximum(roof_h, Hw[:, :, None])
    Ch = np.maximum(Ch, Z - roof_h)
    del roof_h
    # ---- pumpkin cavity: roof = max of cones from several flat seed discs
    # (main Ø30 bridge + one small bridge behind each pumpkin eye's upper part)
    Cp = np.maximum(np.maximum(PK + (P.WALL_PUMPKIN - slack), wall), floor)
    roof = None
    info["pumpkin_roof_seeds"] = []
    for (sx, sy), sr in P.PK_ROOF_SEEDS:
        zs_ = natural_top(g, Cp, (sx, sy), sr) - 0.3
        info["pumpkin_roof_seeds"].append([sx, sy, sr, round(zs_, 3)])
        dp = np.maximum(np.sqrt((X - sx) ** 2 + (Y - sy) ** 2) - sr, 0.0)
        hz = zs_ - roof_cot(X, Y, sx, sy) * dp
        roof = hz if roof is None else np.maximum(roof, hz)
        del dp
    info["pumpkin_roof_z"] = info["pumpkin_roof_seeds"][0][3]
    zf_p = info["pumpkin_roof_z"]
    Hw, apx = window_apex_roof(g, Cp, f["E"], PK_WINDOWS, cot_f)
    info["pumpkin_window_apexes"] = len(apx)
    if Hw is not None:
        roof = np.maximum(roof, Hw[:, :, None])
    Cp = np.maximum(Cp, Z - roof)
    del roof
    # ---- torso cavity: 45 deg funnel converging on the neck bore
    cx, cy, L, R = P.NECK_STADIUM
    dn = np.maximum(stadium_dist(X, Y, cx, cy, L, R), 0.0)
    Ct = np.maximum(np.maximum(f["torso_alone"] + (P.WALL_CAT - slack), wall), floor)
    Ct = np.maximum(Ct, Z - (P.TORSO_ROOF_Z - cot * dn))
    # ---- neck bore prism (vertical walls)
    Cn = np.maximum(stadium_dist(X, Y, cx, cy, L, R) + 0.0 * Z,
                    np.maximum(P.NECK_Z[0] - Z, Z - P.NECK_Z[1]))
    Cn = np.maximum(Cn, wall)
    del dn
    # ---- plenum stub + 45 deg diamond (covers the exact r 27 bore to z 18+)
    r = np.sqrt(X * X + Y * Y)
    zf, zd = P.PLENUM_FLARE_Z, P.PLENUM_DIAMOND_Z
    rpl = P.PLENUM_STUB_R + np.maximum(0.0, np.minimum(Z - zf, 2 * zd - zf - Z))
    rpl = np.where(Z > 2 * zd - zf, P.PLENUM_STUB_R - (Z - (2 * zd - zf)), rpl)
    Cpl = np.maximum(np.maximum(r - rpl, P.PLENUM_STUB_Z0 - Z), wall)
    del r, rpl
    C = np.minimum(np.minimum(np.minimum(Ch, Cp), np.minimum(Ct, Cn)), Cpl).astype(np.float32)
    parts = {"head": Ch, "pumpkin": Cp, "torso": Ct, "neck": Cn, "plenum": Cpl}
    log("chamber done: head roof z %.2f, pumpkin roof z %.2f" % (zf_h, zf_p))
    return C, parts, info
