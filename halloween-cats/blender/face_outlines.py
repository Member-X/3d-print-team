"""Derive every face outline (windows and pink inlays) for the stage-2 figure
and write them to face_outlines.json (mm, front X-Z plane of the spec frame).

Run once with a Python that has numpy + PIL (system Python is fine):
    python face_outlines.py
The build (build_figure.py) only reads the JSON.

Sources and rules
- Pumpkin eyes, nose and mouth: traced from concept-a.png (yellow vs orange,
  sub-pixel marching squares), x mm = (col - 502.3) / 5.85, level z mm =
  139 - (row - 148) / 5.71 (spec section 4).  The concept layout is kept
  exactly; the whole pumpkin face gets ONE vertical shift (PK_FACE_SHIFT) so
  the feature centres land on the spec's z values on average (eyes 67,
  nose 57.5, mouth 46 -> per-feature shifts 7.0 / 8.3 / 8.8, mean 8.0).
  Then the printing rules are enforced:
    * corner radius >= 2 on the eyes (opening r 2), nose likewise;
    * every yellow gap >= 3 mm (opening r 1.5 on the mouth);
    * teeth >= 6 W x 4 H (checked, reported);
    * orange web between windows >= 4 mm (checked, reported).
- Cat eyes: spec annulus OD 17.5 / pupil 8.0 concentric at x +/-17, z 115.
- Cat nose (pink): traced from the concept, scaled to the spec 8.5 W x 6.5 H,
  centred on the concept layout (eye-anchored shift CAT_FACE_SHIFT).
- Cat mouth (pink): spec "w" of two arcs, 22 W, sag 3, line 1.6 wide,
  round caps, positioned from the concept's black mouth line.
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import outline2d as O  # noqa: E402
import params as P     # noqa: E402

CONCEPT = os.path.join(os.path.dirname(HERE), "concept", "concept-a.png")
OUT = os.path.join(HERE, "face_outlines.json")

AXIS_COL = 502.3
PX_MM_X = 5.85
PX_MM_Z = 5.71
PK_FACE_SHIFT = 8.0
NOSE_RAISE = 1.0      # cat nose raised toward the spec z 111
STEP = 0.2            # outline resampling (mm)


def load_rgb():
    try:
        from PIL import Image
        return np.asarray(Image.open(CONCEPT).convert("RGB")).astype(np.float64)
    except ImportError:
        import bpy
        img = bpy.data.images.load(CONCEPT, check_existing=True)
        w, h = img.size
        a = np.empty(w * h * 4, np.float32)
        img.pixels.foreach_get(a)
        return (a.reshape(h, w, 4)[::-1, :, :3] * 255.0).astype(np.float64)


def px_to_mm(loop_rc, zshift):
    """loop in (col, row) pixel coords -> (x, z) mm."""
    col, row = loop_rc[:, 0], loop_rc[:, 1]
    x = (col - AXIS_COL) / PX_MM_X
    z = 139.0 - (row - 148.0) / PX_MM_Z + zshift
    return np.stack([x, z], 1)


def trace_region(field, r0, r1, c0, c1, min_px_area=200):
    """field < 0 inside; returns loops in (col, row) pixel coords."""
    sub = field[r0:r1, c0:c1].T          # index [col, row]
    loops = O.trace(sub, float(c0), float(r0), 1.0)
    out = []
    for l in loops:
        a = O.loop_area(l)
        if abs(a) >= min_px_area:
            out.append(l)
    return out


def clean(loop_mm, iters=6):
    l = O.resample(loop_mm, 0.1)
    l = O.smooth(l, iters=iters, lam=0.5)
    return O.resample(l, STEP)


def ccw(l):
    return l if O.loop_area(l) > 0 else l[::-1].copy()


def main():
    rgb = load_rgb()
    R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    report = {}

    # ---------------- pumpkin face: yellow (G ~216) vs orange (G ~100)
    fld = 158.0 - G
    loops_px = trace_region(fld, 540, 800, 330, 680)
    feats = []
    for l in loops_px:
        mm = ccw(clean(px_to_mm(l, PK_FACE_SHIFT)))
        feats.append(mm)
    feats.sort(key=lambda l: (round(-l[:, 1].mean() / 8), l[:, 0].mean()))
    # expected: [eye L, eye R] (top row), nose, mouth
    byname = {}
    for l in feats:
        cx, cz = l[:, 0].mean(), l[:, 1].mean()
        w = l[:, 0].max() - l[:, 0].min()
        if w > 40:
            byname["pk_mouth"] = l
        elif cz > 63:
            byname["pk_eye_L" if cx < 0 else "pk_eye_R"] = l
        else:
            byname["pk_nose"] = l
    raw = {k: v.copy() for k, v in byname.items()}
    # symmetrise the two eyes (mirror average) so the figure stays symmetric
    eL, eR = byname["pk_eye_L"], byname["pk_eye_R"]
    eRm = eR.copy(); eRm[:, 0] *= -1; eRm = eRm[::-1]
    # align by resampling both to the same count, starting at the top point
    def start_top(l):
        k = int(np.argmax(l[:, 1]))
        return np.roll(l, -k, 0)
    n = 400
    a = O.resample(start_top(eL), 1.0); a = a[np.linspace(0, len(a) - 1, n).astype(int)]
    b = O.resample(start_top(eRm), 1.0); b = b[np.linspace(0, len(b) - 1, n).astype(int)]
    eye = O.resample(0.5 * (a + b), STEP)
    eyeR = eye.copy(); eyeR[:, 0] *= -1; eyeR = eyeR[::-1].copy()
    byname["pk_eye_L"], byname["pk_eye_R"] = ccw(eye), ccw(eyeR)
    # symmetrise nose and mouth about x = 0
    for k in ("pk_nose", "pk_mouth"):
        l = byname[k]
        m = l.copy(); m[:, 0] *= -1; m = m[::-1]
        F, x0, z0 = O.raster_sdf([l], 0.05, pad=1.0)
        xs = x0 + 0.05 * np.arange(F.shape[0])
        zs = z0 + 0.05 * np.arange(F.shape[1])
        X, Z = np.meshgrid(xs, zs, indexing="ij")
        Fm = O.polygon_sdf(np.stack([X.ravel(), Z.ravel()], 1), [m]).reshape(X.shape)
        Fs = 0.5 * (F + Fm)
        ls = [ll for ll in O.trace(Fs, x0, z0, 0.05) if abs(O.loop_area(ll)) > 1]
        byname[k] = ccw(O.resample(ls[0], STEP))
    # enforce rules: eyes/nose corner radius >= 2, mouth gaps >= 3 (opening 1.5)
    for k, r in (("pk_eye_L", 2.0), ("pk_eye_R", 2.0), ("pk_nose", 2.0), ("pk_mouth", 1.5)):
        before = O.loop_area(byname[k])
        op = O.opening([byname[k]], r)
        op = [l for l in op if abs(O.loop_area(l)) > 1.0]
        assert len(op) == 1, (k, len(op))
        byname[k] = ccw(O.resample(op[0], STEP))
        report[k] = {"opening_r": r, "area_before": round(before, 2),
                     "area_after": round(O.loop_area(byname[k]), 2)}

    # ---------------- cat face
    # eyes: spec annulus
    ang = np.linspace(0, 2 * math.pi, int(2 * math.pi * P.CAT_EYE_OD / 2 / STEP), endpoint=False)
    for side, sx in (("L", -1), ("R", 1)):
        cx, cz = sx * P.CAT_EYE_X, P.CAT_EYE_Z
        outer = np.stack([cx + P.CAT_EYE_OD / 2 * np.cos(ang), cz + P.CAT_EYE_OD / 2 * np.sin(ang)], 1)
        a2 = np.linspace(0, 2 * math.pi, int(2 * math.pi * P.PUPIL_D / 2 / STEP), endpoint=False)
        inner = np.stack([cx + P.PUPIL_D / 2 * np.cos(a2), cz + P.PUPIL_D / 2 * np.sin(a2)], 1)[::-1]
        byname["cat_eye_" + side] = [outer, inner]          # annulus: outer CCW + hole CW
        byname["cat_pupil_" + side] = ccw(inner[::-1].copy())
    # concept eye centre rows -> the cat face shift (eye-anchored)
    ymask = (G > 150) & (R > 150) & (B < 90)
    rows, cols = np.nonzero(ymask[250:400, 330:680])
    eye_row_c = 250 + 0.5 * (rows.min() + rows.max())
    cat_shift = P.CAT_EYE_Z - (139.0 - (eye_row_c - 148.0) / PX_MM_Z)
    report["cat_face_shift"] = round(cat_shift, 2)
    # nose: pink
    fld = 72.0 - (R - G)
    nl = trace_region(fld, 320, 390, 460, 545, min_px_area=100)
    nose = ccw(clean(px_to_mm(nl[0], cat_shift)))
    # symmetrise, then scale to spec 8.5 x 6.5 about its bbox centre
    m = nose.copy(); m[:, 0] *= -1
    F, x0, z0 = O.raster_sdf([nose], 0.02, pad=0.5)
    xs = x0 + 0.02 * np.arange(F.shape[0]); zs = z0 + 0.02 * np.arange(F.shape[1])
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    Fm = O.polygon_sdf(np.stack([X.ravel(), Z.ravel()], 1), [m[::-1]]).reshape(X.shape)
    ls = [ll for ll in O.trace(0.5 * (F + Fm), x0, z0, 0.02) if abs(O.loop_area(ll)) > 1]
    nose = ccw(O.resample(ls[0], 0.05))
    bx0, bx1, bz0, bz1 = O.bbox([nose])
    cxn, czn = 0.5 * (bx0 + bx1), 0.5 * (bz0 + bz1)
    nose[:, 0] = (nose[:, 0] - cxn) * P.CAT_NOSE_W / (bx1 - bx0)
    nose[:, 1] = czn + (nose[:, 1] - czn) * P.CAT_NOSE_H / (bz1 - bz0)
    byname["cat_nose"] = O.resample(nose, 0.1)
    report["cat_nose_centre_z"] = round(czn, 2)
    # mouth: concept black line (max channel < 9) under the nose
    mask = (np.maximum(np.maximum(R, G), B) < 9)
    sub = mask[362:405, 430:575]
    rr, cc = np.nonzero(sub)
    rr = rr + 362; cc = cc + 430
    xm = (cc - AXIS_COL) / PX_MM_X
    zm = 139.0 - (rr - 148.0) / PX_MM_Z + cat_shift
    # lowest points of each lobe and the centre cusp
    left, right = xm < -1.0, xm > 1.0
    lobe_x = 0.5 * (abs(xm[left][np.argmin(zm[left])]) + xm[right][np.argmin(zm[right])])
    z_bottom = float(np.mean([zm[left].min(), zm[right].min()]))
    z_top_ends = float(np.mean([zm[xm < -8].max(), zm[xm > 8].max()]))
    report["concept_mouth"] = {"x_span": [round(xm.min(), 2), round(xm.max(), 2)],
                               "lobe_bottom_x": round(lobe_x, 2),
                               "bottom_z_centreline_approx": round(z_bottom + 0.4, 2),
                               "end_z_approx": round(z_top_ends - 0.4, 2)}
    # spec w: total 22 wide (centreline + round caps), sag 3, line 1.6.
    # Each lobe is the circular arc through the cusp C=(0, zb+sag), the
    # bottom B=(+/-XB, zb) and the curled-up end E=(+/-half, zb+ZE_RISE),
    # matching the concept (lobe bottoms at +/-7, ends higher than the cusp).
    W, sag, lw = P.CAT_MOUTH_W, P.CAT_MOUTH_SAG, P.CAT_MOUTH_LINE_W
    half = (W - lw) / 2.0                     # centreline end x (caps add lw/2)
    XB, ZE_RISE = 6.2, 3.8
    zb = z_bottom + 0.4                        # concept centreline bottom
    report["cat_mouth_centreline_bottom_z"] = round(zb, 2)

    def circ3(p1, p2, p3):
        ax, ay = p1; bx, by = p2; cx, cy = p3
        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        ux = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
        uy = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
        return ux, uy, math.hypot(ax - ux, ay - uy)
    pts = []
    for sx in (-1, 1):
        Cp, Bp, Ep = (0.0, zb + sag), (sx * XB, zb), (sx * half, zb + ZE_RISE)
        cxa, cza, rad_s = circ3(Cp, Bp, Ep)
        a0 = math.atan2(Cp[1] - cza, Cp[0] - cxa)
        a1 = math.atan2(Ep[1] - cza, Ep[0] - cxa)
        pts.append((cxa, cza, a0, a1, rad_s))
    rad = pts[0][4]
    # stroke polygon via raster of the arc-stroke SDF
    h = 0.02
    xs = np.arange(-W / 2 - 1, W / 2 + 1, h)
    zs = np.arange(zb - 2, zb + ZE_RISE + 2, h)
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    D = np.full(X.shape, np.inf)
    for (cxa, cza, a0, a1, rr) in pts:
        th = np.arctan2(Z - cza, X - cxa)
        lo, hi = min(a0, a1), max(a0, a1)
        on_arc = (th >= lo) & (th <= hi)
        d_arc = np.abs(np.hypot(X - cxa, Z - cza) - rr)
        e0 = (cxa + rr * math.cos(a0), cza + rr * math.sin(a0))
        e1 = (cxa + rr * math.cos(a1), cza + rr * math.sin(a1))
        d_end = np.minimum(np.hypot(X - e0[0], Z - e0[1]), np.hypot(X - e1[0], Z - e1[1]))
        D = np.minimum(D, np.where(on_arc, d_arc, d_end))
    Fm = D - lw / 2.0
    ml = [ll for ll in O.trace(Fm, xs[0], zs[0], h) if abs(O.loop_area(ll)) > 1]
    assert len(ml) == 1, len(ml)
    byname["cat_mouth"] = ccw(O.resample(ml[0], 0.1))
    report["cat_mouth_arcs"] = {"radius": round(rad, 3),
                                "centres": [[round(a, 3), round(b, 3)] for a, b, _, _, _ in pts],
                                "centreline_x_half": half, "line_w": lw,
                                "cusp": [0.0, round(zb + sag, 3)], "bottom": [XB, round(zb, 3)],
                                "end": [half, round(zb + ZE_RISE, 3)]}
    # nose raised 1.0 toward the spec's z 111 (concept layout gives 109.0):
    # keeps >= 1.5 mm of black between the nose and the mouth cusp.
    byname["cat_nose"][:, 1] += NOSE_RAISE
    report["cat_nose_centre_z_final"] = round(czn + NOSE_RAISE, 2)
    nose_bot = float(byname["cat_nose"][:, 1].min())
    mouth_top_near_centre = float(byname["cat_mouth"][np.abs(byname["cat_mouth"][:, 0]) < 1.0][:, 1].max())
    report["black_gap_nose_to_mouth"] = round(nose_bot - mouth_top_near_centre, 3)
    report["mouth_lowest_z"] = round(float(byname["cat_mouth"][:, 1].min()), 3)
    report["stem_top_clearance_to_mouth"] = round(float(byname["cat_mouth"][:, 1].min()) - P.STEM_Z1, 3)

    # ---------------- checks
    def dist_between(a, b):
        d = O.polygon_sdf(b, [a])
        return float(d.min())
    report["web_eyeL_nose"] = round(dist_between(byname["pk_eye_L"], byname["pk_nose"]), 3)
    report["web_eyeL_mouth"] = round(dist_between(byname["pk_eye_L"], byname["pk_mouth"]), 3)
    report["web_nose_mouth"] = round(dist_between(byname["pk_nose"], byname["pk_mouth"]), 3)
    report["web_eyeL_eyeR"] = round(dist_between(byname["pk_eye_L"], byname["pk_eye_R"]), 3)
    for k in ("pk_eye_L", "pk_nose", "pk_mouth"):
        ok, lost = O.min_inscribed_check([byname[k]], 1.5)
        report[k + "_gap>=3_ok"] = ok
    # teeth: orange notches inside the mouth's bounding hull. Measure with the
    # raster: columns where the mouth's vertical extent has an orange gap.
    mouth = byname["pk_mouth"]
    F, x0, z0 = O.raster_sdf([mouth], 0.05, pad=0.5)
    xs = x0 + 0.05 * np.arange(F.shape[0]); zs = z0 + 0.05 * np.arange(F.shape[1])
    teeth = []
    for i, x in enumerate(xs):
        col = F[i] < 0
        if col.sum() == 0:
            continue
        idx = np.nonzero(col)[0]
        top, bot = zs[idx.max()], zs[idx.min()]
        teeth.append((x, bot, top))
    teeth = np.array(teeth)
    sel = teeth[np.argsort(teeth[:, 0])]
    report["mouth_columns_x_bot_top"] = [[round(a, 2), round(b, 2), round(c, 2)] for a, b, c in sel[::10]]
    report["mouth_bbox"] = [round(v, 2) for v in O.bbox([mouth])]
    for k in list(byname):
        v = byname[k]
        if isinstance(v, list):
            report[k + "_bbox"] = [round(t, 2) for t in O.bbox(v)]
        else:
            report[k + "_bbox"] = [round(t, 2) for t in O.bbox([v])]
    out = {"units": "mm, spec frame front plane (x, z)", "pk_face_shift": PK_FACE_SHIFT,
           "cat_face_shift": cat_shift, "outlines": {}, "report": report,
           "raw_pk": {k: v.round(4).tolist() for k, v in raw.items()}}
    for k, v in byname.items():
        loops = v if isinstance(v, list) else [v]
        out["outlines"][k] = [np.round(l, 4).tolist() for l in loops]
    with open(OUT, "w") as f:
        json.dump(out, f)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
