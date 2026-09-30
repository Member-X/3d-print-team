# Syndication defaults (shop-wide)

Read by `listing-syndicator`. Change a value here and every future run follows it.

## Accounts
- **Etsy:** shop Elevat3dPrintsUS, ships from Brandon, FL 33511. Source of truth for every listing.
- **eBay:** seller account steveowensjr. The user signs in and clears any bot check in the browser pane.
- **Pinterest:** personal account "Steve O" (also has unrelated boards: Comics, Food, Funny, Recipes, Tech...). The user signs in.
- Etsy-to-Pinterest auto-sync is currently down (user report, 2026-09-23), so pins are made manually.

## eBay listing defaults
| Setting | Value |
|---|---|
| Brand (item specific) | Elevat3d Prints |
| Country of origin | United States |
| Condition | New |
| Format / price | Buy It Now, same price as Etsy |
| Quantity | 10 per option (made to order, so this is a cap) |
| Shipping service | USPS Ground Advantage, "Offer free shipping" on (seller pays the eBay label, roughly $5.78-$12.87 for 1.5 lb) |
| Handling time | 3 business days (max eBay's dropdown offers; user's Etsy range is 3-5) |
| Returns | No returns accepted |
| Best Offer, subtitle, bold title, Gallery Plus | Off |
| Tool | eBay "business tool" (the quick tool has no package/handling/returns fields) |
| Color options | Same colors as the Etsy listing, as a "Color" variation |
| Material claim | Only if the product spec confirms it (wand holder text says PLA) |

**Color photos:** each Color option shows a photo of that color (eBay "Add variation photos" -> Color -> "Upload from web" with the Etsy photo URL). An option without a matching photo is reported, never given a wrong-color photo.

Per-product inputs that must be supplied, never guessed: packed weight and box size, real product dimensions, material.

## Pinterest defaults
- Boards: Cat Lover Gifts, Cute Cat Home Decor, Cat Toy Storage & Organization. New boards are public and need user approval.
- 1-2 pins per product, different image and board each. Title <= 100 chars, description <= 500 chars, alt text on every pin.
- Vertical 2:3 images perform best. Landscape works but expect less reach.
- Never "Promote your Pin" (paid). Mark AI-generated images with the "AI-Modified" toggle.

## Content and photo rules
- Only real photos of the item being sold. Flag AI-generated images, recolored copies of one photo, and customer photos (confirm reuse is OK).
- The cat bowl is a decorative dish: always say "not for food or pets".
- Layer lines are normal on FDM prints: say so rather than implying a smooth finish.
- Publishing anything requires the user's yes each time.

## Known browser-pane limits
- Cannot upload files: real photos go in `<project>/ebay-photos/` and the user drags them into eBay.
- eBay shows a "Please verify yourself" bot check; the user must clear it.
- The pane can close between steps: reopen with `preview_start` and a url.
