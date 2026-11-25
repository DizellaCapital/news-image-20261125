[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/DizellaCapital/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/DizellaCapital/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# THE WEDNESDAY LEDGER — Wednesday 25 November 2026: 36 dated stories, 7 regions, drawn leads, pin map, date check

One front page that sums up Wednesday 25 November 2026's world news: 36 dated,
source-tagged stories across 7 regions, with a hero story (Kyiv confirms it
sank Russian ships in two seas — Gulf of Finland and Benghazi), two drawn
leads (Houthis hit Riyadh's tallest tower, 11 hurt; CIA and ODNI breached),
four medium cards, a six-moment timeline, a dotted world map with pins 1–7,
and a 29-item ALSO list in which every item carries a region tag and a source.

Heroes: Kyiv confirms Ukraine's drone strike on a Russian cargo ship in the
Gulf of Finland and the sinking of a Russian warship off Benghazi, Libya ·
Houthis strike Riyadh's PIF Tower for the second time in a week, 11 wounded ·
the CIA and the ODNI suffer a cybersecurity breach involving unclassified
information. All 36 stories are listed with dates, regions and sources in
`stories_20261125.json`; every number on the page matches the JSON and this
README. Stories were verified against Reuters, RFE/RL, WH News, BBC,
BusinessWorld, Jagran Josh and Dell reporting crawled on 25 November 2026,
verified to 08:00 UTC.

Numbers on the page: 11 wounded in Riyadh · 700,000+ Russian soldiers killed
(new analysis) · 4 dead as a migrant boat capsizes off Senegal · 60 km —
Houthis from Aden · 8 wickets — England beat Australia, 2nd T20I · 185 runs
England chased to level the series.

## How it runs

`main.py` (Python 3.13, standard library only) copies the bundled
`entry.png` (1024×1024, under 1 MiB) verbatim to `/output/entry.png`. No
network, no timestamps, no rendering at run time — two runs write
byte-identical files (verified by SHA-256 in the grader simulation below).

## How it was drawn

`render.py` (Pillow, local only — never run by the grader) draws
`entry.png` from `stories_20261125.json`. It is deterministic: two runs
produce byte-identical output.

```sh
python3 render.py   # writes entry.png (186,094 bytes, 1024x1024)
```

Grader simulation (read-only repo dir, `MAKEFUN_OUTPUT_DIR` set):

```sh
MAKEFUN_OUTPUT_DIR=out python3 -P -s main.py   # exit 0, byte-identical output
```

## Date check

Every story above happened, or was first reported, on Wednesday
25 November 2026. Deliberately left out: the UN court ruling on Myanmar
(22 Nov) · GTA 6's launch (19 Nov) · the Trump–Xi–Putin meeting in
Shenzhen (20 Nov) · Nepal's prime minister in Delhi (22–23 Nov).

## Bounty

Entry for [Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125) — $100 shared by the top 50 entries.
