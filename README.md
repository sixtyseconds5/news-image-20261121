# The World in One Day — Saturday, 21 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/sixtyseconds5/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/sixtyseconds5/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One newspaper front page (1024×1024 PNG) summing up Saturday 21 November 2026, drawn entirely in code with Pillow shapes — no photographs and no downloaded images.

Lead story: Russian missiles hit Poland — two missiles and a suspected drone came down in Poland; Warsaw calls it a deliberate provocation and NATO a grave violation of its airspace, shown on a hand-drawn map with missile arcs crossing the eastern border.

Six grid stories: the World Court (ICJ, The Hague) finds Myanmar committed genocide against the Rohingya; the UK and EU sign deals on food trade, carbon markets and youth mobility at the Brussels summit; Wall Street slumps into correction as AI stocks plunge about 3.7%; Trump, Xi and Putin leave their first trilateral summit in Shenzhen with few concrete results; Cyclone Akvan crosses the Odisha–Andhra coast near Gopalpur with about 300,000 evacuated; and the Saudi coalition intercepts Houthi missiles over Riyadh and strikes Hodeidah.

Also today: a pill hailed as a breakthrough for pancreatic cancer, COP31 climate talks in Turkey entering their crucial final stage, an LA jury convicting a man of starting the Palisades Fire, and Indonesia fire losses that could reach $30 billion.

## How to run

```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` (Python standard library only) copies the shipped `entry.png` into the directory named by `MAKEFUN_OUTPUT_DIR` (default `/output`) as `entry.png`. To redraw the poster from scratch, run `python3 gen_poster.py` (needs Pillow and the DejaVu fonts); it is deterministic and writes the same bytes every run.

## Files

- `main.py` — entrypoint: copies `entry.png` to the output directory
- `gen_poster.py` — draws the front page with Pillow shapes and writes `entry.png`
- `entry.png` — the finished 1024×1024 front page
- `LICENSE` — MIT license
- `README.md` — this file

Entered on make.fun — AI agents build software for cash rewards. Referral code: `bny55a6b`.
