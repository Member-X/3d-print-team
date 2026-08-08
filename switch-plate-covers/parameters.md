# Parameter Sheet — Switch Plate Covers

All dimensions in inches unless noted. These are the values used to generate the parametric
sketches in Fusion (`Double Gang Switch Plate.f3d`). Where a value was corrected mid-project,
the superseded value is noted for traceability.

## Double-Gang Toggle Switch Plate

| Parameter | Value | Notes |
|---|---|---|
| Overall width | 4.5625" (4-9/16") | |
| Overall height | 4.500" | |
| Thickness | 0.15625" (5/32") | |
| Outer corner radius | 0.09375" (3/32") | Typical injection-molded convention; not separately spec'd by sources |
| Toggle opening size | 0.40625" × 0.9375" (13/32" × 15/16") | Per gang |
| Toggle opening corner radius | 0.0625" (1/16") | |
| Gang spacing (opening center-to-center) | 1.8125" (1-13/16") | |
| Mounting screw spacing (vertical, per gang) | 2.375" (2-3/8") | NEMA toggle-switch strap standard |
| Mounting screw hole diameter | 0.140" | Clearance for 6-32 screw |
| Back relief pocket (per gang) | 1.60" W × 3.00" H, 0.15" corner radius, 0.06" deep | Clears switch yoke, screws, toggle mechanism — see README |
| Front screw counterbore | 0.27" dia × 0.05" deep | Seats screw head flush |

## Decora-Style Single-Gang Plate (also covers GFCI/rocker/dimmer)

| Parameter | Value | Notes |
|---|---|---|
| Overall width | 2.75" | |
| Overall height | 4.500" | |
| Thickness | 0.15625" (5/32") | |
| Outer corner radius | 0.09375" (3/32") | |
| Device opening size | 1.3125" × 2.625" (1-5/16" × 2-5/8") | Universal Decora/GFCI/rocker/dimmer cutout |
| Device opening corner radius | 0.1875" (3/16") | |
| Mounting screw spacing (vertical) | **3.28" (3-9/32")** | Corrected value — see below |
| Mounting screw hole diameter | 0.140" | |
| Front screw counterbore | 0.27" dia × 0.05" deep | Flat "Example" body only — see Known Issues in README |

### Screw spacing correction

Initial build used 2.375" (borrowed from the toggle-switch spec above, which several
switchplate references imply applies universally). That number puts the screw holes
*inside* the 2.625"-tall device opening — physically impossible. A ruler photo of an
installed GFCI/Decora outlet plate showed the screws clearly outboard of the opening.
3.28" is the standard NEMA WD1 duplex-receptacle strap screw spacing, which applies to
receptacle/GFCI/rocker-style Decora devices (as opposed to the narrower toggle-switch
strap). This is the value baked into the final model and exports.

## Shell / Fillet (cosmetic "shelled" copies)

| Parameter | Value | Notes |
|---|---|---|
| Back shell wall thickness | 1 mm (0.03937") | Removes back face, hollows interior |
| Front edge fillet radius (current) | **1.5 mm (0.0591")** | Reduced by project owner from the original 3.75mm — see revision note below |
| Front edge fillet radius (superseded) | 3.75 mm (0.1476") | Original value; still present, unchanged, on `decora-single-gang-plate-shelled-original-no-holes` |

Values re-measured directly from solid geometry (cylindrical/toroidal face radii), not read
from Fusion's feature history, since the fillet edits were made by hand in the Fusion UI.
Small secondary radii (roughly 1.4mm, 2.8mm, 4.4mm, 5.8mm) also appear on the filleted bodies —
these are Fusion's automatic corner-blend surfaces generated where two 1.5mm edge fillets meet
at a corner, not separate fillet inputs.

### Fillet revision history

1. **Original (3.75mm)** — the double-gang shelled copy and the Decora "original, no holes"
   shelled copy were built manually in the Fusion UI by the project owner with a 1mm back
   shell and a 3.75mm front-face edge fillet.
2. **Regenerated Decora shelled body** — `decora-single-gang-plate-shelled` was rebuilt by
   script from the corrected flat Decora body (see screw-spacing correction above) using the
   same 1mm shell / 3.75mm fillet values, since cutting screw holes into the original shelled
   copy split it into two disconnected solids.
3. **Fillet reduced to 1.5mm** — the project owner subsequently reduced the front-edge fillet
   to 1.5mm on `double-gang-toggle-plate-shelled` and `decora-single-gang-plate-shelled`, and
   added a new 1.5mm fillet to the previously sharp-edged flat `decora-single-gang-plate` body.
   `decora-single-gang-plate-shelled-original-no-holes` was left untouched and still carries
   the original 3.75mm fillet.

## Body list and source of dimensions

| Body | Base spec used |
|---|---|
| `double-gang-toggle-plate` | Double-Gang Toggle table above — flat, no fillet |
| `double-gang-toggle-plate-shelled` | Same + 1mm shell / **1.5mm fillet** |
| `decora-single-gang-plate` | Decora table above, with corrected 3.28" screw spacing + **1.5mm fillet** (added — see revision history) |
| `decora-single-gang-plate-shelled-original-no-holes` | Decora table above, no screw holes, 1mm shell / 3.75mm fillet (superseded — kept for reference) |
| `decora-single-gang-plate-shelled` | Decora table above + 1mm shell / **1.5mm fillet** |

> **Note:** the exported STEP/3MF/STL files in `../step/`, `../3mf/`, `../stl/` were generated
> *before* the fillet reduction described above. They still reflect the 3.75mm fillet
> (or no fillet, for `decora-single-gang-plate`). Re-export is needed before those files match
> the dimensions in this table.
