[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/DizellaCapital/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/DizellaCapital/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# Wednesday 25 November 2026 — 36 dated stories, 6 regions, three illustrated leads

One front page that sums up Wednesday 25 November 2026's world news.
The date itself is the masthead — **Wednesday 25 November 2026** — above
three illustrated leads: Huawei found guilty of stealing trade secrets
(New York), a Houthi missile hitting Riyadh's tallest tower (11 hurt),
and the WHO pulling its Ebola teams out of a Congo hospital (5,775 dead).
Below them, five more illustrated stories (Kyiv's ships in two seas, the
CIA breach, the Australia–Solomon Islands pact, a 15-year-old's 204 off
53 balls, Giuliani's Medal of Freedom), a strip of six big red figures
(5,775 · 204 · 11 · 700,000+ · 8 wkts · 185), region bars (Europe 9,
Americas 8, Asia-Pacific 8, Middle East 6, Africa 3, World 2), a world
map with pins 1–8, and 28 more stories (9–36), each with its source.

All 36 stories are listed with dates, regions and sources in
`stories_20261125.json`; every number on the page matches the JSON and
this README. Stories were verified against Reuters, RFE/RL, WH News,
BBC, BusinessWorld, Jagran Josh, CNN, Daily Sabah, the WHO, AFP, FT,
The Hindu and Dell reporting crawled on 25 November 2026, verified to
08:00 UTC.

Numbers on the page: 5,775 Ebola deaths in DR Congo · 204 runs off 53
balls — Sooryavanshi, 15 · 11 wounded in the Riyadh tower strike ·
700,000+ Russian soldiers killed (new analysis) · 8 wickets — England's
win over Australia · 185 runs England chased to level the series.

## How it runs

`main.py` (Python 3.13, standard library only) copies the bundled
`entry.png` (1024×1024, under 1 MiB) verbatim to `/output/entry.png`.
No network, no timestamps, no rendering at run time — two runs write
byte-identical files (verified by SHA-256 in the grader simulation below).

## How it was drawn

`render.py` (Pillow, local only — never run by the grader) draws
`entry.png` from `stories_20261125.json`. It is deterministic: two runs
produce byte-identical output.

```sh
python3 render.py   # writes entry.png (177,964 bytes, 1024x1024)
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
