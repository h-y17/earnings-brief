---
name: earnings-brief
description: Produces a quick-read digest of a public company's most recent earnings report (quarterly or annual) — revenue, net income, EPS, margins, YoY/QoQ growth, forward guidance, highlights, and risks — sourced entirely from public web search (investor relations pages, earnings press releases, SEC/regulatory filings) rather than any paid data subscription. Use this whenever the user names a public company or ticker and asks how it did, what its latest earnings/results were, for an earnings summary or digest, or a "quick read" / "TL;DR" of a financial report — even if they don't use the word "earnings" explicitly (e.g. "how's Nvidia doing lately", "summarize AAPL's latest quarter", "帮我看看特斯拉最新财报怎么样").
---

# Earnings Brief

## Purpose

Turn a company name or ticker into a short, structured digest of its latest earnings, built from primary public sources rather than secondhand commentary. This skill is meant to work for anyone, with no paid data subscription required — it relies only on general web search and page fetching.

## Workflow

1. **Identify the company and period.** Resolve the name/ticker to the right listed entity (watch for similarly-named private companies or subsidiaries). Unless the user names a specific quarter or year, assume they want the *most recently reported* period — but check the date of that report and flag if it's more than ~4 months old, since the user may actually want a newer one that just hasn't been indexed yet.

2. **Find the primary source, not a secondary summary.** Search for the company's investor relations ("IR") page, its official earnings press release, and — for more precision — its regulatory filing (10-Q/10-K in the US, or the equivalent home-market filing for non-US companies, e.g. 6-K/annual report, HKEX filings, etc.). Prefer fetching the actual press release or filing over a news article *about* it: aggregator articles round numbers, mix up GAAP vs. non-GAAP, or get quarters wrong. If you can only find secondary coverage, say so explicitly in the output rather than presenting it as primary data.

3. **Extract the numbers, and mark what's missing as missing.** Don't estimate or infer a number that isn't disclosed — write "not disclosed" instead. Pull, where available:
   - Revenue, and its YoY change (plus QoQ if this is a quarterly report)
   - Net income, and its YoY change
   - EPS — both GAAP and non-GAAP/adjusted if the company reports both (many tech companies do; note which is which, since conflating them is a common source of confusion)
   - Gross margin and operating margin
   - Segment-level revenue breakdown, if the company discloses one and it's central to the story (e.g. cloud vs. ads vs. hardware)

4. **Pull a short trend, not just one comparison point.** A single YoY/QoQ number can hide whether a company is accelerating, decelerating, or just had one unusual quarter. Gather revenue and EPS for the trailing periods — the last 4-5 quarters for a quarterly report, or the last 3-5 fiscal years for an annual one — and note it as a compact trend rather than a full re-analysis of each period. Good places to find this without excessive extra fetching:
   - The current release itself often includes a "selected financial data" or multi-quarter table in its supplementary tables
   - The company's IR site usually has a quarterly/annual results archive page listing headline revenue and EPS for each past period, which is much faster to skim than opening every old press release
   - If a proper multi-period breakdown isn't readily available without digging through many individual filings, use what you found already this session (e.g. the prior quarter you looked at for QoQ) rather than going on an open-ended hunt — a partial trend is still useful, and note that it's partial

5. **Capture forward guidance.** Companies often give a range for next quarter/year revenue or EPS in the same release or the earnings call. Include it if given; state "no guidance provided" if not — some companies deliberately don't guide.

6. **Note highlights and risks in the company's own words where possible.** Highlights: notable product launches, major deals, management commentary on what drove the quarter. Risks: anything management flagged as a headwind, along with any obvious red flags you notice (e.g. margin compression, guidance cut, one-time items inflating the numbers) — but distinguish your own observation from something management said.

7. **Match the user's language.** Respond in whichever language the user wrote their request in. Keep company/ticker names, GAAP/non-GAAP labels, and other proper nouns in their original form even when the surrounding text is translated.

8. **List your sources.** Always end with links to the pages you actually pulled numbers from, so the user can verify.

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

## Trend (last [N] periods)
| Period | Revenue | Net income | EPS |
|---|---|---|---|
| ... | | | |

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
