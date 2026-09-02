# Primary data sources by market

Where to find a company's own filed/released numbers, market by market — read this when step 2 of the main workflow ("find the primary source") needs a concrete starting point beyond "search for the IR page." These are official disclosure systems: filings go here whether or not any news outlet picks them up, so they're the most reliable way to confirm a number or find one that hasn't been widely reported yet.

Regardless of market, a company's own investor relations site is usually the fastest single starting point (it links directly to the current release and often mirrors the regulatory filing) — use the market-specific portal below when you need to double-check a number, find the underlying regulatory filing rather than just the press release, or the IR site itself is hard to locate.

## US-listed companies

**SEC EDGAR** — https://www.sec.gov/cgi-bin/browse-edgar or https://www.sec.gov/edgar/search/ (full-text search)

- Quarterly results: look for **Form 8-K** with an "Exhibit 99.1" earnings press release attached — companies file this within a day or two of announcing
- Full detail: **Form 10-Q** (quarterly) or **10-K** (annual) — filed a few weeks after the 8-K, with complete financial statements and footnotes
- Foreign private issuers listed in the US (e.g. many non-US companies with US-listed ADRs) file **Form 6-K** (furnished press releases/reports) and **20-F** (annual report) instead of 10-Q/10-K
- To go straight to a company's filing history: full-text search by company name/ticker at the URL above, or look up its **CIK** (SEC's permanent company ID number) and browse `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=<CIK>&type=8-K`
- `data.sec.gov` also exposes structured XBRL data (machine-readable financial statement values) if you need to pull a specific figure programmatically rather than reading a filing

## Hong Kong-listed companies

**HKEXnews (披露易)** — https://www.hkexnews.hk

- Search by stock code or company name under "Listed Company Information" for results announcements, annual/interim reports, and other regulatory filings
- Quarterly reporting isn't mandatory in Hong Kong the way it is in the US — main boards typically report **interim (half-year)** and **annual** results, so "latest quarter" often means "latest half-year" for an HK-listed company; check what cadence the company actually reports on before assuming a Q1/Q3-style update exists

## Japan-listed companies

Two complementary systems:

- **TDnet** (Timely Disclosure network, run by the Tokyo Stock Exchange) — https://www.release.tdnet.info/inbs/I_main_00.html — this is where earnings announcements ("tanshin" / 決算短信) land first, usually same-day; closest equivalent to a US 8-K/press release
- **EDINET** (run by Japan's Financial Services Agency) — https://disclosure2.edinet-fsa.go.jp — hosts the fuller statutory filings (securities reports / 有価証券報告書), closer to a 10-K/10-Q in depth, filed somewhat later than the TDnet announcement

## European-listed companies

There's no single EU-wide portal in wide practical use yet (ESMA's European Single Access Point is still rolling out) — disclosure is organized per country/exchange, so the company's own IR "regulatory news" or "investor news" page is typically the most efficient route. Where a country-level system helps:

- **UK**: London Stock Exchange's **RNS** (Regulatory News Service) — searchable at https://www.londonstockexchange.com/news?tab=news-explorer — and the FCA's **National Storage Mechanism** (https://data.fca.org.uk/#/nsm/nationalstoragemechanism) for the underlying regulated filings
- **Germany**: company IR pages are the practical default; the **Unternehmensregister** (https://www.unternehmensregister.de) hosts statutory filings if you need to go further
- **France**: the **AMF** (Autorité des Marchés Financiers) publishes regulated information via its BALO/info-financière system (https://www.info-financiere.fr), though company IR pages are usually faster for the headline release
- For other European markets, search `<company> investor relations regulatory news` — most exchanges (Euronext, SIX, etc.) run their own news-distribution page linked from the company's IR site

## Everywhere else

If a market isn't listed above, search for `<company> investor relations` plus the local term for "results announcement" or "regulatory filing," and check whether the local exchange runs its own disclosure/announcements portal (most do — Australia has ASX Announcements, India has BSE/NSE corporate announcements, etc.). The pattern is consistent even where the specific system isn't: exchange-run disclosure portal (most authoritative, sometimes hard to search) → company IR page (fastest, usually complete) → regulatory filing (most detailed, filed latest).
