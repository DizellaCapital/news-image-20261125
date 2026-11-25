[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/DizellaCapital/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/DizellaCapital/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

# Wednesday 25 November 2026 — 36 dated stories, 13 pictures, the day in UTC

One front page that sums up Wednesday 25 November 2026's world news.
The date itself is the masthead — **Wednesday 25 November 2026** — above
three illustrated leads: Asia's chip stocks crash on AI doubts (Kospi
−6.2%), Pakistan's first astronaut reaches China's Tiangong station
aboard Shenzhou-24, and the US proposes tariffs of up to 20% on the EU,
China and 12 more economies. Below them, ten more illustrated stories
(two tankers on fire in Hormuz, the Solomon Islands pact, UK energy
bills up 26%, 26 miners trapped in a flooded Java gold mine, the Gaza
strike, the CIA–ODNI breach, the Hodeidah port strikes, the 36% garment
pay rise, Australian inflation at 4.9%, the WHO pulling its Ebola teams
out of Congo), a strip of six big red figures (−6.2% · 20% · +36% ·
4.9% · 26 · 5,775), a "THE DAY IN UTC" strip timing the day (00:01
Samara refineries · 00:18 Shenzhou-24 lifts off · 00:30 Aus CPI 4.9% ·
03:56 Tiangong docking · 05:30 Taiex −4.8% · 06:30 Kospi −6.2%), region
bars (Europe 9, Americas 7, Asia-Pacific 7, Middle East 5, Africa 6,
World 2), a world map with pins 1–13, and 23 more stories (14–36), each
with its source.

All 36 stories are listed with dates, regions and sources in
`stories_20261125-v3.json`; every number on the page matches the JSON
and this README. Stories were verified against Reuters, AP, AFP, Al
Jazeera, CNBC, Korea Times, Xinhua, the WHO, Ofgem, the ABS, CNN, the
NYT, El Tiempo, the Guardian, the Times of Israel, KCNA, TfL, the BBC,
the UN and Jagran Josh reporting of 25 November 2026, verified to
10:00 UTC.

Numbers on the page: −6.2% Kospi close, worst AI day · 20% top US
tariff, EU + China · +36% Bangladesh garment pay · 4.9% Australian CPI,
October · 26 trapped in a Java pit · 5,775 Ebola deaths, DR Congo.

## How it runs

`main.py` (Python 3.13, standard library only) copies the bundled
`entry.png` (1024×1024, under 1 MiB) verbatim to `/output/entry.png`.
No network, no timestamps, no rendering at run time — two runs write
byte-identical files (verified by SHA-256 in the grader simulation below).

## How it was drawn

`render.py` (Pillow, local only — never run by the grader) draws
`entry.png` from `stories_20261125-v3.json`. It is deterministic: two
runs produce byte-identical output.

```sh
python3 render.py   # writes entry.png (195,493 bytes, 1024x1024)
```

Grader simulation (read-only repo dir, `MAKEFUN_OUTPUT_DIR` set):

```sh
MAKEFUN_OUTPUT_DIR=out python3 -P -s main.py   # exit 0, byte-identical output
```

## Date check

Every story above happened, or was first reported, on Wednesday
25 November 2026. Deliberately left out, because they happened earlier:
Huawei convicted in Brooklyn (Tue 24) · drone hits Riyadh tower
(Tue 24) · Huang back at Nvidia (Mon 23) · leaked count of Russia's war
dead (Mon 23) · COP33 collapse (Sun 22) · first strike at Riyadh PIF
tower (Thu 19).

## Bounty

Entry for [Sum up 25 November's world news in one image](https://make.fun/bounty/news-image-20261125) — $100 shared by the top 50 entries.
