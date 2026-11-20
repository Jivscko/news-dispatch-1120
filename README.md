# The World Dispatch - 20 November 2026

One 1024x1024 PNG that sums up the world news of Friday, 20 November 2026,
drawn as a newspaper front page: masthead, date line, a lead story and a
three-by-three grid of the day's other dispatches.

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/Jivscko/news-dispatch-1120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/Jivscko/news-dispatch-1120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

## The day

Friday, 20 November 2026. The lead story is Russia's retaliatory missile
barrage on the bridges of Kyiv. Around it, nine more dispatches: the White
House removing its cyber-security chief after a run of federal tech outages;
the US Senate passing a bipartisan energy bill over environmental objections;
a Texas death-row execution that ran past an hour; the US Army delaying
detonation of lead explosives after public concern and a lawsuit; Mamdani's
plan to close Rikers Island; the EU and UK agreeing to reset relations ten
years after Brexit; Estonia closing its border with Russia, which Moscow
called a new Iron Curtain; Anthropic's stock falling on its first day of
trading after IPO; and China's AI firms short of Nvidia chips.

Every line on the page comes from those ten reported items and the date.
Nothing else is asserted.

## Files

- `main.py` - entry runner. Copies `entry.png` byte-for-byte into
  `$MAKEFUN_OUTPUT_DIR` (default `/output`), verifies the copy, prints `OK`.
  Python 3.13, standard library only, no network.
- `entry.png` - the finished 1024x1024 front page.
- `render_news.py` - build script that draws the page with Pillow.
  Deterministic, no external assets, no network.

## Run

    MAKEFUN_OUTPUT_DIR=out python3 main.py

The output directory is created if missing, including nested paths. The
runner copies `entry.png`, re-reads both files, and compares size plus
SHA-256; any mismatch is an error. It prints `OK` and exits 0 on success,
prints an `ERROR:` line to stderr and exits 1 on any failure. With
`MAKEFUN_OUTPUT_DIR` unset or empty it writes to `/output`.

## Rebuild the image

    python3 render_news.py

Requires Pillow. Writes `entry.png` next to the script in about a second. The
renderer is fully deterministic - no randomness, no network, no external
assets beyond the system serif and sans fonts - and it asserts that
20 November 2026 falls on a Friday before drawing anything.

## Check the build

    python3 render_news.py
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
    python3 -c "from PIL import Image; im=Image.open('out/entry.png'); print(im.size)"

Expect `(1024, 1024)` and a file of about 102 KiB, well under the 1 MiB cap.

## License

MIT. See `LICENSE`.

https://make.fun/r/s9rnvy2k
