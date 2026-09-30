"""Criterion A12: silhouette of the model overlaid on concept-a.png at the
spec section 4 scale.  Runs inside Blender (numpy + mathutils).

Two projections are produced:
  'level'  : orthographic front view (along +Y); concept pixel (col, row) ->
             x = (col - 502.3) / 5.85, z = 139 - (row - 148) / 5.71.  This is
             exactly the mapping the spec used for every MEAS-IMG value.
  'tilt13' : orthographic view from 13 deg above (the concept's camera, base
             ellipse 145/650 px); screen-up = (0, sin13, cos13), 5.85 px/mm,
             anchored so the head top (0, 14, 139) lands on row 148.
Both render a 1024 x 1024 composite: concept image, model silhouette tinted,
model outline in red, and a label.  Also returns silhouette widths.
"""
import math
import numpy as np
import bpy
import bmesh
from mathutils import Vector
from mathutils.bvhtree import BVHTree

CONCEPT = r"H:\ClaudeStuff\3d-print-team\halloween-cats\concept\concept-a.png"
AXIS_COL, PXX, PXZ = 502.3, 5.85, 5.71
TILT = math.radians(13.0)


def load_concept():
    img = bpy.data.images.load(CONCEPT, check_existing=True)
    w, h = img.size
    a = np.empty(w * h * 4, np.float32)
    img.pixels.foreach_get(a)
    return a.reshape(h, w, 4)[::-1].copy()          # row 0 = top


def tree_for(names, parts_colors=None):
    """One BVH over several objects (world space); returns tree and a per-
    triangle object index."""
    verts, tris, owner = [], [], []
    off = 0
    for i, n in enumerate(names):
        ob = bpy.data.objects[n]
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        bm.transform(ob.matrix_world)
        bmesh.ops.triangulate(bm, faces=bm.faces[:])
        bm.verts.index_update()
        verts += [v.co[:] for v in bm.verts]
        for f in bm.faces:
            tris.append([off + v.index for v in f.verts])
            owner.append(i)
        off += len(bm.verts)
        bm.free()
    return BVHTree.FromPolygons(verts, tris, all_triangles=True), np.array(owner)


def project_mask(tree, owner, mode, size=1024, step=1):
    """For every concept pixel, cast a ray; return (hit mask, owner index or -1)."""
    H = W = size
    hit = np.zeros((H, W), bool)
    who = np.full((H, W), -1, np.int32)
    if mode == "level":
        d = Vector((0.0, 1.0, 0.0))
        for r in range(0, H, step):
            z = 139.0 - (r - 148.0) / PXZ
            for c in range(0, W, step):
                x = (c - AXIS_COL) / PXX
                loc, nrm, idx, dist = tree.ray_cast(Vector((x, -300.0, z)), d, 1000.0)
                if loc is not None:
                    hit[r, c] = True
                    who[r, c] = owner[idx]
    else:
        up = Vector((0.0, math.sin(TILT), math.cos(TILT)))
        d = Vector((0.0, math.cos(TILT), -math.sin(TILT)))
        right = Vector((1.0, 0.0, 0.0))
        v0 = Vector((0.0, 14.0, 139.0)).dot(up)          # head top -> row 148
        for r in range(0, H, step):
            v = v0 - (r - 148.0) / PXX
            for c in range(0, W, step):
                x = (c - AXIS_COL) / PXX
                o = right * x + up * v - d * 400.0
                loc, nrm, idx, dist = tree.ray_cast(o, d, 1000.0)
                if loc is not None:
                    hit[r, c] = True
                    who[r, c] = owner[idx]
    return hit, who


def outline_of(mask):
    m = mask
    e = np.zeros_like(m)
    e[1:-1, 1:-1] = m[1:-1, 1:-1] & ~(m[:-2, 1:-1] & m[2:, 1:-1] & m[1:-1, :-2] & m[1:-1, 2:])
    return e


def concept_silhouette(img):
    rgb = img[..., :3] * 255.0
    bg = rgb[5, 5]
    return np.abs(rgb - bg).sum(-1) > 40


def compose(img, mask, path, tint=(0.1, 0.6, 1.0), alpha=0.35, extra_outline=None):
    out = img.copy()
    out[..., :3] = np.where(mask[..., None], out[..., :3] * (1 - alpha) + np.array(tint) * alpha, out[..., :3])
    edge = outline_of(mask)
    # thicken the outline to 2 px
    edge2 = edge.copy()
    edge2[1:, :] |= edge[:-1, :]
    edge2[:, 1:] |= edge[:, :-1]
    out[edge2, :3] = (1.0, 0.0, 0.0)
    if extra_outline is not None:
        ce = outline_of(extra_outline)
        out[ce, :3] = (0.0, 0.8, 0.0)
    H, W = mask.shape
    im = bpy.data.images.new("_overlay", W, H, alpha=True)
    out[..., 3] = 1.0
    im.pixels.foreach_set(np.ascontiguousarray(out[::-1]).ravel())
    im.filepath_raw = path
    im.file_format = 'PNG'
    im.save()
    bpy.data.images.remove(im)
    return path


def run(names, path_level, path_tilt, step=1):
    img = load_concept()
    cs = concept_silhouette(img)
    tree, owner = tree_for(names)
    res = {}
    for mode, path in (("level", path_level), ("tilt13", path_tilt)):
        hit, who = project_mask(tree, owner, mode, step=step)
        compose(img, hit, path, extra_outline=cs)
        inter = (hit & cs).sum()
        union = (hit | cs).sum()
        res[mode] = {"path": path, "model_px": int(hit.sum()), "concept_px": int(cs.sum()),
                     "IoU": round(float(inter) / float(union), 4)}
    return res
