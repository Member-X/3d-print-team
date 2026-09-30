"""Quick section images straight from the cached fields (design inspection).
Solid = dark, chamber = light yellow, outside = grey; grid lines every 10 mm.
Runs inside Blender (saves PNG via bpy)."""
import numpy as np
import bpy
import figure_shapes as FS


def section_png(path, E, C, axis, value, scale=4, extra=None):
    g = FS.Grid()
    i = int(round(value / g.h)) - g.i0["xyz".index(axis)]
    if axis == "x":
        e, c = E[i, :, :], C[i, :, :]          # (y, z)
        h_ax, v_ax = g.ax[1], g.ax[2]
    elif axis == "y":
        e, c = E[:, i, :], C[:, i, :]          # (x, z)
        h_ax, v_ax = g.ax[0], g.ax[2]
    else:
        e, c = E[:, :, i], C[:, :, i]          # (x, y)
        h_ax, v_ax = g.ax[0], g.ax[1]
    solid = (e < 0) & (c > 0)
    void = (e < 0) & (c <= 0)
    img = np.full(e.shape + (4,), 0.72, np.float32)
    img[..., 3] = 1
    img[solid, :3] = (0.12, 0.12, 0.14)
    img[void, :3] = (1.0, 0.97, 0.75)
    if extra is not None:
        for m, col in extra:
            mm = m if axis == "z" else m
            img[mm, :3] = col
    for k, a in enumerate(h_ax):
        if abs(a / 10 - round(a / 10)) < 1e-4:
            img[k, :, :3] *= 0.8
    for k, a in enumerate(v_ax):
        if abs(a / 10 - round(a / 10)) < 1e-4:
            img[:, k, :3] *= 0.8
    img = np.transpose(img, (1, 0, 2))          # rows = vertical axis, bottom-up
    img = np.repeat(np.repeat(img, scale, 0), scale, 1)
    H, W = img.shape[:2]
    im = bpy.data.images.new("_sec", W, H, alpha=True)
    im.pixels.foreach_set(np.ascontiguousarray(img).ravel())
    im.filepath_raw = path
    im.file_format = 'PNG'
    im.save()
    bpy.data.images.remove(im)
    return path
