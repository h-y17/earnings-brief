---
name: earnings-brief
description: Produces a quick-read digest of a public company's most recent earnings report (quarterly or annual) — revenue, net income, EPS, margins, YoY/QoQ growth, forward guidance, highlights, and risks — sourced entirely from public web search (investor relations pages, earnings press releases, SEC/regulatory filings) rather than any paid data subscription. Use this whenever the user names a public company or ticker and asks how it did, what its latest earnings/results were, for an earnings summary or digest, or a "quick read" / "TL;DR" of a financial report — even if they don't use the word "earnings" explicitly (e.g. "how's Nvidia doing lately", "summarize AAPL's latest quarter", "帮我看看特斯拉最新财报怎么样").
---

# Earnings Brief

## Purpose

Turn a company name or ticker into a short, structured digest of its latest earnings, built from primary public sources rather than secondhand commentary. This skill is meant to work for anyone, with no paid data subscription required — it relies only on general web search and page fetching.

## Workflow

1. **Identify the company and period.** Resolve the name/ticker to the right listed entity (watch for similarly-named private companies or subsidiaries). Unless the user names a specific quarter or year, assume they want the *most recently reported* period — but check the date of that report and flag if it's more than ~4 months old, since the user may actually want a newer one that just hasn't been indexed yet.

2. **Find the primary source, not a secondary summary.** Search for the company's investor relations ("IR") page, its official earnings press release, and — for more precision — its regulatory filing (10-Q/10-K in the US, or the equivalent home-market filing for non-US companies, e.g. 6-K/annual report, HKEX filings, etc.). Prefer fetching the actual press release or filing over a news article *about* it: aggregator articles round numbers, mix up GAAP vs. non-GAAP, or get quarters wrong. If you can only find secondary coverage, say so explicitly in the output rather than presenting it as primary data. See `references/data-sources.md` for where the official disclosure portal lives in each major market (US/SEC EDGAR, Hong Kong/HKEXnews, Japan/TDnet+EDINET, Europe) when a plain web search doesn't turn up the primary filing directly.

3. **Extract the numbers, and mark what's missing as missing.** Don't estimate or infer a number that isn't disclosed — write "not disclosed" instead. Pull, where available:
   - Revenue, and its YoY change (plus QoQ if this is a quarterly report)
   - Net income, and its YoY change
   - EPS — both GAAP and non-GAAP/adjusted if the company reports both (many tech companies do; note which is which, since conflating them is a common source of confusion)
   - Gross margin and operating margin
   - Segment-level revenue breakdown, if the company discloses one and it's central to the story (e.g. cloud vs. ads vs. hardware)

4. **Check the result against analyst consensus, and label it clearly as a third-party number.** Whether a company "beat" or "missed" is often what investors care about most, more than the raw growth rate — a slowing company that still beats a lowered bar reads very differently from one that grew but missed expectations. The company itself never discloses this; search for it separately (e.g. `"<company>" Q<N> analyst estimates consensus revenue EPS` or `"<company>" earnings preview estimates`), since financial news coverage of the release routinely states what "analysts had expected." A few things matter here:
   - Consensus is normally tracked against **non-GAAP/adjusted EPS**, not GAAP — compare like with like, and say which basis you're using
   - Different data providers (Zacks, FactSet, Visible Alpha, LSEG/Refinitiv...) can report slightly different consensus figures; if sources disagree, either use the most commonly cited number or give the range, and always name the source and, if available, its as-of date, since estimates drift right up until the print
   - If you can't find a credible consensus figure at all (small-cap, thinly covered, or non-US company with little analyst coverage), say so rather than presenting a single stray estimate as "the" consensus

5. **Pull a short trend, not just one comparison point.** A single YoY/QoQ number can hide whether a company is accelerating, decelerating, or just had one unusual quarter. Gather revenue and EPS for the trailing periods — the last 4-5 quarters for a quarterly report, or the last 3-5 fiscal years for an annual one — and note it as a compact trend rather than a full re-analysis of each period. Good places to find this without excessive extra fetching:
   - The current release itself often includes a "selected financial data" or multi-quarter table in its supplementary tables
   - The company's IR site usually has a quarterly/annual results archive page listing headline revenue and EPS for each past period, which is much faster to skim than opening every old press release
   - If a proper multi-period breakdown isn't readily available without digging through many individual filings, use what you found already this session (e.g. the prior quarter you looked at for QoQ) rather than going on an open-ended hunt — a partial trend is still useful, and note that it's partial
   - Right after the Trend table, add a fenced ` ```chart-data ` block with the same revenue figures as `label: number` lines (see the output template below) — a table of numbers is precise, but a bar chart makes "is this accelerating or decelerating" legible at a glance. The block is plain data, harmless to read in the raw Markdown; `scripts/export_digest.py` turns it into an actual bar chart in the PDF. Strip units/currency symbols from the values (just the number) and keep the same unit across all entries so the bars are comparable — mixing e.g. millions and billions in one chart would silently misrepresent the trend.

6. **Capture forward guidance.** Companies often give a range for next quarter/year revenue or EPS in the same release or the earnings call. Include it if given; state "no guidance provided" if not — some companies deliberately don't guide.

7. **Note highlights and risks in the company's own words where possible.** Highlights: notable product launches, major deals, management commentary on what drove the quarter. Risks: anything management flagged as a headwind, along with any obvious red flags you notice (e.g. margin compression, guidance cut, one-time items inflating the numbers) — but distinguish your own observation from something management said.

8. **Match the user's language.** Respond in whichever language the user wrote their request in. Keep company/ticker names, GAAP/non-GAAP labels, and other proper nouns in their original form even when the surrounding text is translated.

9. **List your sources.** Always end with links to the pages you actually pulled numbers from, so the user can verify.

10. **Export to a file only if asked.** By default, just answer in the chat — most requests don't need a saved file. If the user asks to save, export, or download the digest:
   - For Markdown, just write the digest text to a `.md` file directly (you already have file-write access; no script needed for this part).
   - For PDF, run `scripts/export_digest.py <the .md file>` on the Markdown file you just saved. By default it uses a bundled pure-Python renderer (`fpdf2`, installed via `pip install -r scripts/requirements.txt` if missing) that needs no system-level dependency — this is the path that works for anyone regardless of what's installed on their machine. It also renders any ` ```chart-data ` block (see step 5) as an actual bar chart, drawn directly with fpdf2 rather than a charting library. If `pandoc` happens to be installed already, pass `--engine pandoc` for noticeably nicer typesetting; it's an optional upgrade, not something to ask the user to install just for this — note that the pandoc path does *not* render the chart-data block into a chart (pandoc doesn't know what it means), so it'll show up as a plain code block instead.
   - **Chinese/Japanese/Korean or other non-Latin digests, specifically:** the fpdf2 path needs a font file that actually contains those glyphs. It auto-detects a common system font first (this generally just works on Windows and macOS, which ship one by default), but on a machine without one — a bare Linux server is the typical case — it will stop with an error rather than silently produce a PDF full of missing-glyph boxes, and tell you to pass `--font path/to/a/unicode/font.ttf`. If that happens, point the user at a free option like [Noto Sans SC](https://fonts.google.com/noto/specimen/Noto+Sans+SC) (or the Japanese/Korean equivalent) to download once and reuse.

## Output template

Use this structure (translate headers into the user's language; keep the shape):

```
# [Company Name] ([Ticker]) — [Fiscal Period] Earnings Brief

**Reported:** [date] | **Source:** [primary source type, e.g. "Q3 FY2026 press release"]

## Headline numbers
| Metric | This period | YoY | QoQ (if quarterly) |
|---|---|---|---|
| Revenue | | | |
| Net income | | | |
| EPS (GAAP) | | | |
| EPS (non-GAAP) | | | |
| Gross margin | | | |
| Operating margin | | | |

## vs. Analyst Consensus
| Metric | Actual | Consensus estimate | Result |
|---|---|---|---|
| Revenue | | | Beat / Miss / In-line |
| EPS (non-GAAP, unless noted) | | | Beat / Miss / In-line |
*Consensus source: [outlet], as of [date]. Not disclosed by the company — third-party estimate.*

## Trend (last [N] periods)
| Period | Revenue | Net income | EPS |
|---|---|---|---|
| ... | | | |

​```chart-data
title: Revenue Trend ([unit])
[Period]: [number, no currency/unit symbols]
...
​```

## Guidance
[Forward guidance, or "No guidance provided."]

## Highlights
- ...

## Risks / watch items
- ...

## Sources
- [links]

---
*This is a summary for quick orientation, not investment advice. Verify figures against the primary filing before acting on them.*
```

## Edge cases

- **Can't find a recent report at all** (pre-IPO, delisted, thinly covered foreign company): say so plainly instead of presenting stale or unrelated data as current.
- **Non-USD reporting currency**: keep the company's native reporting currency; don't silently convert to USD (an unlabeled conversion is more misleading than useful, and exchange rates move).
- **Report just released / earnings call still ongoing**: note that some figures (like a full guidance breakdown) may still be incomplete, and that a call transcript may add more color once published.
- **User asks to compare two periods or two companies**: extend the table with extra columns rather than producing two separate digests — that's usually what they actually want to see side by side.
- **Too little history to show a trend** (recent IPO, spinoff, or a company that just changed its segment/reporting structure): show whatever periods are genuinely comparable and say why the trend is short, rather than reaching further back into numbers that aren't apples-to-apples (e.g. don't splice pre- and post-restructuring segment revenue into one row).
- **No consensus estimate found**: drop the "vs. Analyst Consensus" section (or state "no consensus estimate found") rather than presenting one stray blog/forum number as if it were the market's view — a single unverified estimate is worse than none.
- **Trend is only 1-2 periods** (e.g. right after an IPO): skip the `chart-data` block — a bar chart of two points doesn't add anything over just reading the two numbers, and drawing one anyway would overstate how much trend data actually exists.
