"""2D outline utilities for the stage-2 figure (pure numpy, no Blender).

Outlines are closed polylines in a 2D plane given as (N, 2) float arrays
(first point not repeated).  For the face features the plane is the front
(X, Z) plane of the spec frame.

    polygon_sdf(pts, loops)      exact signed distance (negative inside,
                                 even-odd rule over all loops)
    raster_sdf(loops, h, pad)    sample it on a raster, returns (F, x0, z0)
    trace(F, x0, z0, h)          marching squares -> closed loops
    opening(loops, r)            morphological opening (min corner radius r)
    closing(loops, r)
"""
import math
import numpy as np


# ------------------------------------------------------------------ basics
def as_loops(loops):
    if isinstance(loops, np.ndarray):
        return [loops]
    return [np.asarray(l, dtype=np.float64) for l in loops]


def loop_area(l):
    x, y = l[:, 0], l[:, 1]
    return 0.5 * float(np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y))


def bbox(loops):
    a = np.vstack(as_loops(loops))
    return a[:, 0].min(), a[:, 0].max(), a[:, 1].min(), a[:, 1].max()


def resample(l, step):
    """Uniform arc-length resampling of a closed loop."""
    l = np.asarray(l, float)
    seg = np.linalg.norm(np.roll(l, -1, 0) - l, axis=1)
    L = seg.sum()
    n = max(8, int(math.ceil(L / step)))
    s = np.concatenate([[0.0], np.cumsum(seg)])
    t = np.linspace(0.0, L, n, endpoint=False)
    ext = np.vstack([l, l[:1]])
    x = np.interp(t, s, ext[:, 0])
    y = np.interp(t, s, ext[:, 1])
    return np.stack([x, y], 1)


def smooth(l, iters=10, lam=0.5):
    l = np.asarray(l, float).copy()
    for _ in range(iters):
        l = l + lam * (0.5 * (np.roll(l, 1, 0) + np.roll(l, -1, 0)) - l)
    return l


# ------------------------------------------------------------------ SDF
def polygon_sdf(pts, loops, chunk=400000):
    """Exact 2D signed distance from pts (M,2) to the region bounded by loops
    (even-odd fill).  Negative inside."""
    pts = np.asarray(pts, float)
    loops = as_loops(loops)
    out = np.empty(len(pts))
    for c0 in range(0, len(pts), chunk):
        p = pts[c0:c0 + chunk]
        px, py = p[:, 0], p[:, 1]
        d2 = np.full(len(p), np.inf)
        sgn = np.ones(len(p))
        for l in loops:
            vj = np.roll(l, 1, 0)
            for (ax, ay), (bx, by) in zip(l, vj):     # edge from v_i to v_j
                ex, ey = bx - ax, by - ay
                wx, wy = px - ax, py - ay
                ee = ex * ex + ey * ey
                t = np.clip((wx * ex + wy * ey) / ee, 0.0, 1.0) if ee > 0 else 0.0
                bx_, by_ = wx - ex * t, wy - ey * t
                np.minimum(d2, bx_ * bx_ + by_ * by_, out=d2)
                c1 = py >= ay
                c2 = py < by
                c3 = ex * wy > ey * wx
                flip = (c1 & c2 & c3) | (~c1 & ~c2 & ~c3)
                sgn[flip] *= -1.0
        # sgn starts at +1 and flips once per crossing: inside -> -1
        out[c0:c0 + chunk] = sgn * np.sqrt(d2)
    return out


def raster_sdf(loops, h, pad=3.0, extra_bbox=None):
    x0, x1, z0, z1 = bbox(loops)
    if extra_bbox:
        x0, x1 = min(x0, extra_bbox[0]), max(x1, extra_bbox[1])
        z0, z1 = min(z0, extra_bbox[2]), max(z1, extra_bbox[3])
    x0 -= pad; z0 -= pad; x1 += pad; z1 += pad
    xs = np.arange(x0, x1 + h, h)
    zs = np.arange(z0, z1 + h, h)
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    F = polygon_sdf(np.stack([X.ravel(), Z.ravel()], 1), loops).reshape(X.shape)
    return F, xs[0], zs[0]


# ------------------------------------------------------------------ marching squares
def trace(F, x0, z0, h, level=0.0):
    """Closed contour loops of {F < level} (F indexed [ix, iz]).  Loops are
    oriented counter-clockwise for outer boundaries (positive area)."""
    G = F - level
    nx, nz = G.shape
    inside = G < 0
    # edge crossing points
    pts = {}

    def xpt(i0, j0, i1, j1):
        key = (min(i0, i1), min(j0, j1), 0 if j0 == j1 else 1)
        if key not in pts:
            a, b = G[i0, j0], G[i1, j1]
            t = a / (a - b)
            pts[key] = (x0 + h * (i0 + t * (i1 - i0)), z0 + h * (j0 + t * (j1 - j0)))
        return key
    # cells with mixed corners
    c = (inside[:-1, :-1].astype(np.uint8) | (inside[1:, :-1].astype(np.uint8) << 1)
         | (inside[1:, 1:].astype(np.uint8) << 2) | (inside[:-1, 1:].astype(np.uint8) << 3))
    ii, jj = np.nonzero((c != 0) & (c != 15))
    nxt = {}
    for i, j in zip(ii.tolist(), jj.tolist()):
        k = int(c[i, j])
        # corners: 0=(i,j) 1=(i+1,j) 2=(i+1,j+1) 3=(i,j+1)
        eB = lambda: xpt(i, j, i + 1, j)          # bottom (z=j)
        eR = lambda: xpt(i + 1, j, i + 1, j + 1)  # right
        eT = lambda: xpt(i, j + 1, i + 1, j + 1)  # top
        eL = lambda: xpt(i, j, i, j + 1)          # left
        # segments oriented so the inside is on the LEFT (CCW outer loops).
        # bits: 1 = BL(i,j), 2 = BR(i+1,j), 4 = TR(i+1,j+1), 8 = TL(i,j+1)
        if k in (5, 10):
            mid = 0.25 * (G[i, j] + G[i + 1, j] + G[i + 1, j + 1] + G[i, j + 1])
            if k == 5:   # BL and TR inside
                segs = [(eB(), eR()), (eT(), eL())] if mid < 0 else [(eB(), eL()), (eT(), eR())]
            else:        # BR and TL inside
                segs = [(eL(), eB()), (eR(), eT())] if mid < 0 else [(eR(), eB()), (eL(), eT())]
        else:
            table = {1: (eB, eL), 2: (eR, eB), 3: (eR, eL), 4: (eT, eR), 6: (eT, eB),
                     7: (eT, eL), 8: (eL, eT), 9: (eB, eT), 11: (eR, eT), 12: (eL, eR),
                     13: (eB, eR), 14: (eL, eB)}
            a, b = table[k]
            segs = [(a(), b())]
        for a, b in segs:
            nxt[a] = b
    loops = []
    seen = set()
    for s in list(nxt.keys()):
        if s in seen:
            continue
        loop = []
        cur = s
        while cur not in seen and cur in nxt:
            seen.add(cur)
            loop.append(pts[cur])
            cur = nxt[cur]
        if len(loop) >= 3:
            loops.append(np.array(loop))
    return loops


# ------------------------------------------------------------------ morphology
def offset(loops, r, h=0.05, min_area=0.05):
    """Region {sdf < r} (r > 0 dilates, r < 0 erodes), traced."""
    F, x0, z0 = raster_sdf(loops, h, pad=abs(r) + 4 * h)
    out = trace(F, x0, z0, h, level=r)
    return [l for l in out if abs(loop_area(l)) > min_area]


def opening(loops, r, h=0.05):
    return offset(offset(loops, -r, h), r, h)


def closing(loops, r, h=0.05):
    return offset(offset(loops, r, h), -r, h)


def min_inscribed_check(loops, r, h=0.05):
    """True if the region equals its opening by r (every point of the region
    lies in a disc of radius r inside the region) within one raster cell."""
    op = opening(loops, r, h)
    F0, x0, z0 = raster_sdf(loops, h, pad=1.0)
    xs = x0 + h * np.arange(F0.shape[0])
    zs = z0 + h * np.arange(F0.shape[1])
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    F1 = polygon_sdf(np.stack([X.ravel(), Z.ravel()], 1), op).reshape(X.shape)
    lost = (F0 < -h) & (F1 > h)
    return int(lost.sum()) == 0, float(lost.sum() * h * h)
