# Syndication log

Where each product is posted. `listing-syndicator` reads this first (no duplicate pins or listings) and updates it after each step.

| Product | Etsy | Pinterest | eBay |
|---|---|---|---|
| Cat Wand Toy Holder (`cat-toy-holder/`) | 4472501841 | 1 pin -> Cat Toy Storage & Organization (2026-09-23) | LIVE 178522736668 (2026-09-23), 16 colors, $49.99, qty 10 each |
| Sleeping Cat Catchall Bowl (`cat-bowl/`, prints `Cat.stl` at 125%) | 4580025587 (listed 2026-09-21) | 2 pins: gift shot -> Cat Lover Gifts; entryway shot -> Cute Cat Home Decor (2026-09-23) | LIVE 178523017624 (2026-09-23, published by the user), 5 colors, $34.99, qty 10 each, free ship, no returns. Each color shows its own photo (White verified) |
| Cat Catchall Tray | 4540612311 | 1 pin -> Cute Cat Home Decor (2026-09-23) | not listed. Needs packed weight and box size |

## Color photos (2026-09-23)
- Wand holder eBay 178522736668: all 16 colors now have their own matching photo (revised live; verified by picking Red on the item page). Hot Pink has an Etsy photo but is not an eBay option.
- Bowl eBay 178523017624: all 5 colors have a matching photo. Black, Brown, Orange and White Marble were attached by URL from Etsy; the user uploaded the solid White render from `cat-bowl/Images/Bowl1-White.png` (verified on the item page 2026-09-23).
- Bowl Pinterest pins link to the Etsy listing (Pinterest adds utm_source=Pinterest). No pin points to the eBay listings.

## Notes
- Wand holder eBay package: 1 lb 8 oz, 15 x 11 x 3 in. Real product size about 232 x 230 x 41 mm (the slicer's 193.258 x 193.258 x 230 is a 45-degree-rotated bounding box).
- Bowl eBay package: 0 lb 13 oz, 15 x 11 x 3 in. Real product size 7.10 x 6.70 x 2.73 in (180 x 170 x 69 mm), inner opening about 5.1 x 4.8 in, interior depth about 1.2 in (Cat.stl at 125%). eBay category: Home & Garden > Home Decor > Decorative Accessories > Decorative Plates & Bowls.
- Bowl eBay draft photos (11) are renders and AI lifestyle images, none of a real print; the photo files are in `cat-bowl/ebay-photos/`.
- Pins 1 and 2 for the bowl use AI-generated lifestyle images and are not marked "AI-Modified"; the user has been told.
