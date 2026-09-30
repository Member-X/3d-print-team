"""Export the five colour parts + combined master as STL, and a multi-part
3MF.  Runs inside Blender.  All parts keep their shared design coordinates
(already print orientation: bottom at z 0, centred on X/Y) - no per-part
offsets, so they stay registered to each other.

    import export_figure as EX; EX.export_all()
"""
import os
import struct
import zipfile

import bpy
import bmesh
import numpy as np

import params as P

ROOT = r"H:\ClaudeStuff\3d-print-team\halloween-cats"
STL = os.path.join(ROOT, "stl")
TMF = os.path.join(ROOT, "3mf")
PARTS = ("black", "orange", "yellow", "green", "pink")


def tri_arrays(ob):
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.transform(ob.matrix_world)
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')
    bm.verts.index_update()
    V = np.array([v.co[:] for v in bm.verts], np.float64)
    F = np.array([[v.index for v in f.verts] for f in bm.faces], np.int64)
    bm.free()
    return V, F


def write_stl(V, F, path, name):
    a, b, c = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    n = np.cross(b - a, c - a)
    ln = np.linalg.norm(n, axis=1)
    n = n / np.where(ln > 0, ln, 1)[:, None]
    rec = np.zeros(len(F), dtype=np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")]))
    rec["n"] = n
    rec["v"][:, 0] = a
    rec["v"][:, 1] = b
    rec["v"][:, 2] = c
    hdr = ("halloween-cat %s | mm | print orientation z0 bottom | spec v%s" % (name, P.SPEC_VERSION)).encode()
    with open(path, "wb") as f:
        f.write(hdr[:80].ljust(80, b" "))
        f.write(struct.pack("<I", len(F)))
        f.write(rec.tobytes())
    return {"path": path, "triangles": int(len(F)), "bytes": os.path.getsize(path)}


def write_3mf(parts, path):
    """Core-spec 3MF: one mesh object per part (named, coloured through a
    basematerials group) + one assembly object made of the five components,
    with a single build item.  Units mm."""
    cols = [P.COLORS[p].lstrip("#").upper() for p, _, _ in parts]
    out = []
    out.append('<?xml version="1.0" encoding="UTF-8"?>\n')
    out.append('<model unit="millimeter" xml:lang="en-US" '
               'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">\n')
    out.append(' <metadata name="Title">Halloween cat "Pumpkin Hug" (5 colour parts)</metadata>\n')
    out.append(' <metadata name="Designer">3d-print-team / 3d-blender-modeler</metadata>\n')
    out.append(' <resources>\n  <basematerials id="1">\n')
    for (p, _, _), c in zip(parts, cols):
        out.append('   <base name="%s" displaycolor="#%sFF"/>\n' % (p, c))
    out.append('  </basematerials>\n')
    for k, (p, V, F) in enumerate(parts):
        oid = k + 2
        out.append('  <object id="%d" type="model" name="%s" pid="1" pindex="%d">\n   <mesh>\n    <vertices>\n'
                   % (oid, p, k))
        out.append("".join('     <vertex x="%.5f" y="%.5f" z="%.5f"/>\n' % tuple(v) for v in V))
        out.append('    </vertices>\n    <triangles>\n')
        out.append("".join('     <triangle v1="%d" v2="%d" v3="%d"/>\n' % tuple(f) for f in F))
        out.append('    </triangles>\n   </mesh>\n  </object>\n')
    aid = len(parts) + 2
    out.append('  <object id="%d" type="model" name="halloween-cat">\n   <components>\n' % aid)
    for k in range(len(parts)):
        out.append('    <component objectid="%d"/>\n' % (k + 2))
    out.append('   </components>\n  </object>\n </resources>\n')
    out.append(' <build>\n  <item objectid="%d"/>\n </build>\n</model>\n' % aid)
    ct = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n'
          ' <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n'
          ' <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>\n'
          '</Types>\n')
    rels = ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
            ' <Relationship Target="/3D/3dmodel.model" Id="rel0" '
            'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>\n'
            '</Relationships>\n')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("3D/3dmodel.model", "".join(out))
    return {"path": path, "bytes": os.path.getsize(path)}


def export_all(master="M2_windows"):
    os.makedirs(STL, exist_ok=True)
    res = {}
    parts = []
    for p in PARTS:
        V, F = tri_arrays(bpy.data.objects[p])
        res[p] = write_stl(V, F, os.path.join(STL, "halloween-cat_%s.stl" % p), p)
        parts.append((p, V, F))
    V, F = tri_arrays(bpy.data.objects[master])
    res["combined"] = write_stl(V, F, os.path.join(STL, "halloween-cat_combined.stl"), "combined")
    res["3mf"] = write_3mf(parts, os.path.join(TMF, "halloween-cat.3mf"))
    return res
