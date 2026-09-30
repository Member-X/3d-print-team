"""v2 exports (run inside Blender).  All formats are written from the SAME
float32 vertex arrays, so the parts sit at bit-identical coordinates in the
STL, 3MF and OBJ files.  Print orientation, bottom at z 0, centred on X/Y.

    stl/v2/halloween-cat-v2_<part>.stl, _combined.stl
    3mf/v2/halloween-cat-v2_core-3mf.3mf            plain core-spec 3MF (fallback)
    3mf/v2/halloween-cat-v2_bambu-studio.3mf        Bambu Studio project style:
            ONE object with five parts, filament slots 1 black, 2 orange,
            3 yellow, 4 green, 5 pink, placed at the plate centre (128, 128)
    obj/v2/halloween-cat-v2_5-parts.obj + .mtl      five objects, one material each
    obj/v2/halloween-cat-v2_painted-single-mesh.obj one closed mesh, faces coloured
"""
import datetime
import json
import os
import struct
import uuid
import zipfile

import bpy
import bmesh
import numpy as np

import params as P

ROOT = r"H:\ClaudeStuff\3d-print-team\halloween-cats"
STL = os.path.join(ROOT, "stl", "v2")
TMF = os.path.join(ROOT, "3mf", "v2")
OBJ = os.path.join(ROOT, "obj", "v2")
PREFIX = "halloween-cat-v2"
PARTS = ("black", "orange", "yellow", "green", "pink")
SLOT = {"black": 1, "orange": 2, "yellow": 3, "green": 4, "pink": 5}
BAMBU_APP = "BambuStudio-02.08.02.61"      # the user's installed version (BambuStudio.conf)
PLATE_CENTRE = (128.0, 128.0)             # P2S 256 x 256 bed


def tri_arrays(ob, with_src=False):
    """Triangulated world-space arrays, vertices as float32 (the STL precision).
    with_src: also return, per triangle, the index of the source polygon and
    the polygons' vertex lists (for interface matching at polygon level)."""
    bm = bmesh.new()
    bm.from_mesh(ob.data)
    bm.transform(ob.matrix_world)
    lay = bm.faces.layers.int.new("src_poly")
    bm.faces.index_update()
    polys = []
    for f in bm.faces:
        f[lay] = f.index
        polys.append([v.index for v in f.verts])
    bm.verts.index_update()
    bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='BEAUTY')
    bm.verts.index_update()
    V = np.array([v.co[:] for v in bm.verts], np.float32)
    F = np.array([[v.index for v in f.verts] for f in bm.faces], np.int64)
    S = np.array([f[lay] for f in bm.faces], np.int64)
    bm.free()
    if with_src:
        return V, F, S, polys
    return V, F


def f9(a):
    return "%.9g" % float(a)


# ------------------------------------------------------------------ STL
def write_stl(V, F, path, name):
    Vd = V.astype(np.float64)
    a, b, c = Vd[F[:, 0]], Vd[F[:, 1]], Vd[F[:, 2]]
    n = np.cross(b - a, c - a)
    ln = np.linalg.norm(n, axis=1)
    n = n / np.where(ln > 0, ln, 1)[:, None]
    rec = np.zeros(len(F), dtype=np.dtype([("n", "<f4", 3), ("v", "<f4", (3, 3)), ("a", "<u2")]))
    rec["n"] = n
    rec["v"][:, 0] = V[F[:, 0]]
    rec["v"][:, 1] = V[F[:, 1]]
    rec["v"][:, 2] = V[F[:, 2]]
    hdr = ("halloween-cat v2 %s | mm | print orientation z0 bottom | spec v1.2" % name).encode()
    with open(path, "wb") as f:
        f.write(hdr[:80].ljust(80, b" "))
        f.write(struct.pack("<I", len(F)))
        f.write(rec.tobytes())
    return {"path": path, "triangles": int(len(F)), "bytes": os.path.getsize(path)}


# ------------------------------------------------------------------ 3MF helpers
def mesh_xml(V, F, indent="    "):
    out = [indent + "<mesh>\n", indent + " <vertices>\n"]
    out.append("".join('%s  <vertex x="%s" y="%s" z="%s"/>\n' % (indent, f9(v[0]), f9(v[1]), f9(v[2])) for v in V))
    out.append(indent + " </vertices>\n" + indent + " <triangles>\n")
    out.append("".join('%s  <triangle v1="%d" v2="%d" v3="%d"/>\n' % (indent, t[0], t[1], t[2]) for t in F))
    out.append(indent + " </triangles>\n" + indent + "</mesh>\n")
    return "".join(out)


CT_XML = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n'
          ' <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n'
          ' <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>\n'
          ' <Default Extension="png" ContentType="image/png"/>\n'
          ' <Default Extension="gcode" ContentType="text/x.gcode"/>\n'
          '</Types>\n')
REL_3DMODEL = "http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"


def write_core_3mf(parts, path):
    """Plain core-spec 3MF: five named mesh objects (basematerials colours) +
    one assembly object of five components, one build item (as v1)."""
    out = ['<?xml version="1.0" encoding="UTF-8"?>\n',
           '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">\n',
           ' <metadata name="Title">Halloween cat "Pumpkin Hug" v2 (5 colour parts)</metadata>\n',
           ' <metadata name="Designer">3d-print-team / 3d-blender-modeler</metadata>\n',
           ' <resources>\n  <basematerials id="1">\n']
    for p, _, _ in parts:
        out.append('   <base name="%s" displaycolor="#%sFF"/>\n' % (p, P.COLORS[p].lstrip("#").upper()))
    out.append('  </basematerials>\n')
    for k, (p, V, F) in enumerate(parts):
        out.append('  <object id="%d" type="model" name="%s" pid="1" pindex="%d">\n' % (k + 2, p, k))
        out.append(mesh_xml(V, F, "   "))
        out.append('  </object>\n')
    aid = len(parts) + 2
    out.append('  <object id="%d" type="model" name="%s">\n   <components>\n' % (aid, PREFIX))
    for k in range(len(parts)):
        out.append('    <component objectid="%d"/>\n' % (k + 2))
    out.append('   </components>\n  </object>\n </resources>\n')
    out.append(' <build>\n  <item objectid="%d"/>\n </build>\n</model>\n' % aid)
    rels = ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
            ' <Relationship Target="/3D/3dmodel.model" Id="rel0" Type="%s"/>\n'
            '</Relationships>\n' % REL_3DMODEL)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CT_XML.replace(' <Default Extension="png" ContentType="image/png"/>\n', "")
                   .replace(' <Default Extension="gcode" ContentType="text/x.gcode"/>\n', ""))
        z.writestr("_rels/.rels", rels)
        z.writestr("3D/3dmodel.model", "".join(out))
    return {"path": path, "bytes": os.path.getsize(path)}


def _uuid(seed):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "halloween-cat-v2/" + seed))


def write_bambu_3mf(parts, path, thumb_png=None, detect_thin_wall=True):
    """Bambu Studio project-style 3MF, modelled on files written by Bambu
    Studio 02.08.02 (3D/3dmodel.model with a component object pointing into
    3D/Objects/object_1.model, Metadata/model_settings.config with per-part
    names and extruders, a minimal Metadata/project_settings.config naming the
    P2S presets installed with the user's Bambu Studio)."""
    obj_id = len(parts) + 1                     # parts are 1..5, the object is 6
    today = datetime.date.today().isoformat()
    # --- 3D/Objects/object_1.model: the five meshes
    sub = ['<?xml version="1.0" encoding="UTF-8"?>\n',
           '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
           'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
           'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">\n',
           ' <metadata name="BambuStudio:3mfVersion">1</metadata>\n <resources>\n']
    for k, (p, V, F) in enumerate(parts):
        sub.append('  <object id="%d" p:UUID="%s" type="model">\n' % (k + 1, _uuid("mesh-" + p)))
        sub.append(mesh_xml(V, F, "   "))
        sub.append('  </object>\n')
    sub.append(' </resources>\n <build/>\n</model>\n')
    # --- 3D/3dmodel.model
    ident = "1 0 0 0 1 0 0 0 1 0 0 0"
    place = "1 0 0 0 1 0 0 0 1 %s %s 0" % (f9(PLATE_CENTRE[0]), f9(PLATE_CENTRE[1]))
    main = ['<?xml version="1.0" encoding="UTF-8"?>\n',
            '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
            'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
            'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">\n',
            ' <metadata name="Application">%s</metadata>\n' % BAMBU_APP,
            ' <metadata name="BambuStudio:3mfVersion">1</metadata>\n',
            ' <metadata name="CreationDate">%s</metadata>\n' % today,
            ' <metadata name="ModificationDate">%s</metadata>\n' % today,
            ' <metadata name="Title">Halloween cat Pumpkin Hug v2</metadata>\n',
            ' <resources>\n',
            '  <object id="%d" p:UUID="%s" type="model">\n   <components>\n' % (obj_id, _uuid("object"))]
    for k, (p, V, F) in enumerate(parts):
        main.append('    <component p:path="/3D/Objects/object_1.model" objectid="%d" p:UUID="%s" transform="%s"/>\n'
                    % (k + 1, _uuid("component-" + p), ident))
    main.append('   </components>\n  </object>\n </resources>\n')
    main.append(' <build p:UUID="%s">\n  <item objectid="%d" p:UUID="%s" transform="%s" printable="1"/>\n </build>\n'
                % (_uuid("build"), obj_id, _uuid("item"), place))
    main.append('</model>\n')
    # --- Metadata/model_settings.config
    total = sum(len(F) for _, _, F in parts)
    ms = ['<?xml version="1.0" encoding="UTF-8"?>\n<config>\n',
          '  <object id="%d">\n' % obj_id,
          '    <metadata key="name" value="%s"/>\n' % PREFIX,
          '    <metadata key="extruder" value="1"/>\n',
          '    <metadata face_count="%d"/>\n' % total]
    for k, (p, V, F) in enumerate(parts):
        ms += ['    <part id="%d" subtype="normal_part">\n' % (k + 1),
               '      <metadata key="name" value="%s"/>\n' % p,
               '      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>\n',
               '      <metadata key="source_file" value="%s_%s.stl"/>\n' % (PREFIX, p),
               '      <metadata key="source_object_id" value="0"/>\n',
               '      <metadata key="source_volume_id" value="%d"/>\n' % k,
               '      <metadata key="source_offset_x" value="0"/>\n',
               '      <metadata key="source_offset_y" value="0"/>\n',
               '      <metadata key="source_offset_z" value="0"/>\n',
               '      <metadata key="extruder" value="%d"/>\n' % SLOT[p],
               '      <mesh_stat face_count="%d" edges_fixed="0" degenerate_facets="0" facets_removed="0" '
               'facets_reversed="0" backwards_edges="0"/>\n' % len(F),
               '    </part>\n']
    ms += ['  </object>\n',
           '  <plate>\n',
           '    <metadata key="plater_id" value="1"/>\n',
           '    <metadata key="plater_name" value="plate-1"/>\n',
           '    <metadata key="locked" value="false"/>\n',
           '    <metadata key="filament_map_mode" value="Auto For Flush"/>\n',
           '    <metadata key="filament_maps" value="1 1 1 1 1"/>\n']
    if thumb_png:
        ms.append('    <metadata key="thumbnail_file" value="Metadata/plate_1.png"/>\n')
    ms += ['    <model_instance>\n',
           '      <metadata key="object_id" value="%d"/>\n' % obj_id,
           '      <metadata key="instance_id" value="0"/>\n',
           '      <metadata key="identify_id" value="%d"/>\n' % (obj_id + 100),
           '    </model_instance>\n',
           '  </plate>\n',
           '  <assemble>\n',
           '   <assemble_item object_id="%d" instance_id="0" transform="%s" offset="0 0 0" />\n' % (obj_id, place),
           '  </assemble>\n',
           '</config>\n']
    # --- Metadata/project_settings.config (minimal, P2S presets by name)
    n = len(parts)
    ps = {
        "printer_model": "Bambu Lab P2S",
        "printer_settings_id": "Bambu Lab P2S 0.4 nozzle",
        "printer_variant": "0.4",
        "nozzle_diameter": ["0.4"],
        "print_settings_id": "0.20mm Standard @BBL P2S",
        "filament_settings_id": ["Bambu PLA Basic @BBL P2S"] * n,
        "filament_colour": [P.COLORS[p].upper() for p, _, _ in parts],
        "filament_type": ["PLA"] * n,
        "filament_diameter": ["1.75"] * n,
        "filament_is_support": ["0"] * n,
        "printable_area": ["0x0", "256x0", "256x256", "0x256"],
        "printable_height": "256",
        "bed_exclude_area": [],
        "layer_height": "0.2",
        "enable_support": "0",
        "wall_generator": "arachne",
    }
    diff = ["wall_generator;enable_support"]
    if detect_thin_wall:
        ps["detect_thin_wall"] = "1"            # spec 8.2: 0.5 mm skins need "detect thin wall"
        diff = ["wall_generator;enable_support;detect_thin_wall"]
    ps["different_settings_to_system"] = diff + [""] * n + [""]
    rels = ['<?xml version="1.0" encoding="UTF-8"?>\n',
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n',
            ' <Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="%s"/>\n' % REL_3DMODEL]
    if thumb_png:
        rels.append(' <Relationship Target="/Auxiliaries/.thumbnails/thumbnail_3mf.png" Id="rel-2" '
                    'Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail"/>\n')
    rels.append('</Relationships>\n')
    mrels = ('<?xml version="1.0" encoding="UTF-8"?>\n'
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
             ' <Relationship Target="/3D/Objects/object_1.model" Id="rel-1" Type="%s"/>\n'
             '</Relationships>\n' % REL_3DMODEL)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CT_XML)
        z.writestr("_rels/.rels", "".join(rels))
        z.writestr("3D/3dmodel.model", "".join(main))
        z.writestr("3D/_rels/3dmodel.model.rels", mrels)
        z.writestr("3D/Objects/object_1.model", "".join(sub))
        z.writestr("Metadata/model_settings.config", "".join(ms))
        z.writestr("Metadata/project_settings.config", json.dumps(ps, indent=1))
        if thumb_png:
            data = open(thumb_png, "rb").read()
            z.writestr("Metadata/plate_1.png", data)
            z.writestr("Auxiliaries/.thumbnails/thumbnail_3mf.png", data)
    return {"path": path, "bytes": os.path.getsize(path), "object_id": obj_id,
            "extruders": {p: SLOT[p] for p, _, _ in parts}}


# ------------------------------------------------------------------ OBJ
def srgb(hexs):
    h = hexs.lstrip("#")
    return [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]


def write_mtl(path):
    out = ["# halloween-cat v2 materials (spec section 9 viewport colours, sRGB)\n"]
    for p in PARTS:
        r, g, b = srgb(P.COLORS[p])
        out.append("\nnewmtl %s\nKa 0 0 0\nKd %.6f %.6f %.6f\nKs 0 0 0\nd 1\nillum 1\n" % (p, r, g, b))
    with open(path, "w") as f:
        f.write("".join(out))
    return path


def write_obj_parts(parts, path, mtl_name):
    out = ["# halloween-cat v2: five closed parts, one material each; mm, z-up, print orientation\n",
           "mtllib %s\n" % mtl_name]
    base = 1
    for p, V, F in parts:
        out.append("o %s\ng %s\nusemtl %s\n" % (p, p, p))
        out.append("".join("v %s %s %s\n" % (f9(v[0]), f9(v[1]), f9(v[2])) for v in V))
        out.append("".join("f %d %d %d\n" % (t[0] + base, t[1] + base, t[2] + base) for t in F))
        base += len(V)
    with open(path, "w") as f:
        f.write("".join(out))
    return {"path": path, "bytes": os.path.getsize(path)}


def exterior_faces(parts, src=None, drop_leftovers=False):
    """Single closed mesh = all part triangles minus the internal interfaces.
    An interface is matched at POLYGON level when `src` is given (a list, per
    part, of (tri->polygon index, polygon vertex lists)): a boolean output
    polygon whose welded vertex set also occurs in another part is dropped in
    both parts, however each side happened to be triangulated.  Without src,
    matching is per triangle.  Returns welded V, F, the part index per face
    and the number of dropped triangles."""
    allV = np.vstack([V for _, V, _ in parts])
    offs = np.cumsum([0] + [len(V) for _, V, _ in parts])
    allF = np.vstack([F + offs[k] for k, (_, _, F) in enumerate(parts)])
    lab = np.concatenate([np.full(len(F), k) for k, (_, _, F) in enumerate(parts)])
    uniq, inv = np.unique(allV, axis=0, return_inverse=True)
    inv = inv.ravel()
    W = inv[allF]
    if src is None:
        key = np.sort(W, axis=1)
        kv = key[:, 0] * (len(uniq) ** 2) + key[:, 1] * len(uniq) + key[:, 2]
        u_, cnt = np.unique(kv, return_counts=True)
        drop = np.isin(kv, u_[cnt > 1])
    else:
        owner = {}
        pkeys = []
        for k, (S, polys) in enumerate(src):
            keys = [tuple(sorted(int(inv[offs[k] + i]) for i in pl)) for pl in polys]
            pkeys.append(keys)
            for pi, kk in enumerate(keys):
                owner.setdefault(kk, set()).add(k)
        drop_parts = []
        for k, (S, polys) in enumerate(src):
            matched = np.array([len(owner[kk]) > 1 for kk in pkeys[k]], bool)
            drop_parts.append(matched[S])
        drop = np.concatenate(drop_parts)
    keep = ~drop
    V_, F_, L_ = uniq, W[keep], lab[keep]
    n_left = 0
    if drop_leftovers:
        # tested: removing the few unmatched interface patches leaves open
        # T-junction edges instead (the parts' seams do not conform there),
        # so by default they are kept (closed union, a few 4-way edges)
        F_, L_, n_left = _drop_leftover_interfaces(V_, F_, L_, parts)
    return V_, F_, L_, int(drop.sum()) + n_left


def _drop_leftover_interfaces(V, F, L, parts, eps=2e-4):
    """Remove interface triangles that found no exact partner (the two parts
    meshed a tiny interface patch differently; they show as edges used by
    4 triangles).  A triangle next to such an edge is dropped when the points
    just in front of AND just behind it both lie inside some part."""
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    e = np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]])
    und = np.sort(e, axis=1)
    key = und[:, 0] * len(V) + und[:, 1]
    u, inv, cnt = np.unique(key, return_inverse=True, return_counts=True)
    bad_edges = np.nonzero(cnt > 2)[0]
    if len(bad_edges) == 0:
        return F, L, 0
    cand = set((np.nonzero(np.isin(inv, bad_edges))[0] % len(F)).tolist())
    # grow one ring (tiny patches may span a few triangles)
    vset = set(F[list(cand)].ravel().tolist())
    ring = np.nonzero(np.isin(F, list(vset)).any(axis=1))[0]
    cand = sorted(set(ring.tolist()) | cand)
    trees = [BVHTree.FromPolygons([tuple(map(float, v)) for v in Vp], Fp.tolist(), all_triangles=True)
             for _, Vp, Fp in parts]
    Vd = V.astype(np.float64)
    drop = np.zeros(len(F), bool)
    for i in cand:
        a, b, c = Vd[F[i, 0]], Vd[F[i, 1]], Vd[F[i, 2]]
        nrm = np.cross(b - a, c - a)
        ln = np.linalg.norm(nrm)
        if ln < 1e-14:
            drop[i] = True
            continue
        nrm /= ln
        cen = Vector((a + b + c) / 3.0)
        for k, t in enumerate(trees):
            if k == L[i]:
                continue
            loc, n, idx, d = t.find_nearest(cen)
            if loc is not None and d < 1e-5 and n.dot(Vector(nrm)) < -0.9:
                drop[i] = True           # coincides with an opposite face of another part: interface
                break
    return F[~drop], L[~drop], int(drop.sum())


def write_obj_painted(parts, path, mtl_name, src=None):
    V, F, lab, n_int = exterior_faces(parts, src)
    out = ["# halloween-cat v2: ONE closed mesh (outer + inner surfaces), faces coloured by part\n",
           "mtllib %s\no %s\n" % (mtl_name, PREFIX)]
    out.append("".join("v %s %s %s\n" % (f9(v[0]), f9(v[1]), f9(v[2])) for v in V))
    for k, (p, _, _) in enumerate(parts):
        sel = F[lab == k]
        out.append("usemtl %s\n" % p)
        out.append("".join("f %d %d %d\n" % (t[0] + 1, t[1] + 1, t[2] + 1) for t in sel))
    with open(path, "w") as f:
        f.write("".join(out))
    return {"path": path, "bytes": os.path.getsize(path), "faces": int(len(F)), "internal_faces_removed": n_int}


def export_all(master="M2_windows", thumb_png=None):
    for d in (STL, TMF, OBJ):
        os.makedirs(d, exist_ok=True)
    res = {}
    parts = []
    src = []
    for p in PARTS:
        V, F, S, polys = tri_arrays(bpy.data.objects[p], with_src=True)
        res[p] = write_stl(V, F, os.path.join(STL, "%s_%s.stl" % (PREFIX, p)), p)
        parts.append((p, V, F))
        src.append((S, polys))
    # combined = the master M2 (one clean closed 2-manifold).  It equals the
    # union of the parts except at the few seam vertices moved (<= 0.13 mm)
    # when micro-folds were relaxed.
    V, F = tri_arrays(bpy.data.objects[master])
    res["combined"] = write_stl(V, F, os.path.join(STL, "%s_combined.stl" % PREFIX), "combined")
    res["core_3mf"] = write_core_3mf(parts, os.path.join(TMF, "%s_core-3mf.3mf" % PREFIX))
    res["bambu_3mf"] = write_bambu_3mf(parts, os.path.join(TMF, "%s_bambu-studio.3mf" % PREFIX), thumb_png)
    mtl = "%s.mtl" % PREFIX
    write_mtl(os.path.join(OBJ, mtl))
    res["obj_parts"] = write_obj_parts(parts, os.path.join(OBJ, "%s_5-parts.obj" % PREFIX), mtl)
    res["obj_painted"] = write_obj_painted(parts, os.path.join(OBJ, "%s_painted-single-mesh.obj" % PREFIX), mtl, src)
    return res
