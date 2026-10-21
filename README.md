# AI StackWatch 24

Daily market-intelligence publication tracking the 36 companies building the AI
revolution across six layers (Energy, Chips, Cloud & Infrastructure, AI Models,
Platforms, Applications). Static HTML — no build step at serve time, no JS
frameworks; all content is in the pages (bots and AI crawlers read everything).

- Market data: Yahoo Finance end-of-day (chart API, no key), pulled after the US close.
- Prices are never estimated: a failed fetch renders "Data pending".
- 31 public tickers + 5 private/watch-only names (xAI, Mistral AI, Anthropic, OpenAI, Databricks).

## Daily refresh pipeline (design — cron to be enabled after owner's v1 review)

1. **Pull** — `python3 tools/fetch_data.py` refetches all 31 tickers into
   `data/prices.json` (close, day change, 30-session history, 52-week range,
   volume, fetch timestamp).
2. **Research** — an editor pass collects the day's verified headlines for
   universe companies (source + date recorded); confirmed catalysts are added
   to `VERIFIED_HEADLINES` in `tools/build_site.py` and to `STORIES` (rotated
   into `breakthroughs.html`), each with a verbatim source URL. No invented
   stories, no unlinked claims.
3. **Regenerate** — `python3 tools/og_images.py` (only when branding changes)
   and `python3 tools/build_site.py` re-render every page, the daily brief,
   sitemap lastmod dates and the ticker strip from the fresh data file.
4. **Republish** — upload the changed files to `main` (GitHub web flow) and let
   GitHub Pages deploy; verify home + one company page + sitemap live.
5. **Index** — ping IndexNow with the changed URLs and confirm the sitemap in
   Google Search Console; robots.txt already allows search + AI crawlers
   (GPTBot, ClaudeBot, PerplexityBot, Google-Extended), and `llms.txt` maps the
   property for AI readers.
6. **Video** — the day's lead breakthrough gets its short vertical briefing
   rendered into the story's video spot on `breakthroughs.html`.

## Local build

```
python3 tools/fetch_data.py     # refresh data/prices.json
python3 tools/build_site.py     # render the whole site into this folder
```
