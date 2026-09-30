# Santa Candle Holder — Spec

Source: user-supplied reference images (`../concept/reference-spec-diagram.png` — dimensioned
product photo, `../concept/reference-photo.webp` — styled reference render). Not a purchased/
owned physical reference; built to visually match a commercial "Santa holding a candle tray"
decor piece for personal home use.

## Description
Santa Claus figure (bust-down-to-flared-base, no visible legs), arms raised overhead holding a
circular tray sized for a standard 3-wick jar candle. Full Santa costume: hat w/ pom-pom, fur
trim (hat band, cuffs, hem, collar), beard/mustache, belt with buckle, gloved hands.

## Dimensions (from reference image, VERIFIED against the image's own printed callouts —
not independently measured against a physical object, since none exists)
- Total height (base to top of tray): **~180mm**
- Tray outer diameter: **136–138mm**
- Tray inner diameter (candle-retaining lip ID): **~104mm**
- Retaining lip height (proud of tray floor): **3–5mm**
- Tray overall height (floor + lip): **~12mm**
- Target candle: standard 3-wick jar, ~104mm diameter (candle itself NOT part of this build —
  user provides their own candle or jar)

## Printer / material
- P2S (256×256×256mm bed) or Bambu A1 — both comfortably fit a 180mm-tall part. See
  [[user_printer_specs]].
- PLA, user's default.

## Construction decisions (from user, 2026-09-18)
- **Detail level: high-detail attempt.** User explicitly chose to push sculpted detail (face,
  beard texture, fur trim, robe folds) as far as reasonably achievable via procedural Blender
  modeling, accepting that FDM PLA at this scale won't resolve fine texture as sharply as the
  reference photo, and that this is more iteration-prone than a stylized pass (flagged risk,
  user accepted — see cat-bowl precedent in memory for what "too complex" looked like before).
- **Print approach: split into 2 parts.** Body+arms (Part A) and tray (Part B) print separately
  and join via alignment pegs, avoiding the heavy overhead support a single-piece
  arms-overhead pose would need under the tray. Modeled after the jason-candle-holder
  ring-platform precedent.

## Build method
Organic/sculptural figure — built directly in Blender (not Fusion/3d-coder), per
[[feedback_blender_vs_fusion_tool_choice]]. Techniques: bmesh lathe/spin for the robe body,
curve-deform for the raised arms, boolean union for hat/face/trim features, procedural
displacement (Musgrave/Voronoi noise) for beard and fur bump texture.

## Open items
- No real candle/jar on hand to verify tray fit against — dimensions taken directly from the
  reference image's own callouts. If the user has a specific candle in mind, worth confirming
  its actual diameter before finalizing the lip ID.
