# THE DAY IN PICTURES — news-image-20261123 (rebuild)

A hero-led front page summing up Monday 23 November 2026 in one image,
rebuilt from scratch after the first entry (a dense 36-story grid) ranked
674/7,226 in round 1.

## Concept

The judge is a picture editor with no news feed: it picks the image that
best sums up the day, weighing (in order) that it names the day, the
breadth of its story selection, that it reads at a glance, faithfulness,
and craft legible at about 300 pixels across. A wall of 13 pt text fails
the last two. This rebuild is a magazine cover, not a newspaper grid:

- One big picture: the COP31 collapse in Antalya at dusk — the
  conference hall, a low sun over the bay, and a row of empty chairs.
- One huge headline for the lead, then three pictured second stories
  (NATO, Asia markets, Hormuz), then six more in large type.
- 10 stories in all, across regions and fields, every one legible at a
  glance. Date named in the masthead and the footer.

## Build

`build_cover.py` draws the 1024×1024 PNG with PIL (DejaVu fonts, no
network, no randomness): the same tables always produce the same bytes.
`main.ts` (Node 22, stdlib only) copies `entry.png` to `/output` and
verifies it byte for byte. Run the build twice to confirm determinism.

## Stories (all first reported Monday 23 November 2026)

Lead: COP31 collapses as the EU rejects a pact with no fossil-fuel line.
Second: NATO Council meets on a Russian missile in Poland; Asia braces
as the AI rout rolls on; two more tankers burn in the Gulf. Also today:
Libya, Mexico, USA, Okinawa, Geneva, MotoGP.
