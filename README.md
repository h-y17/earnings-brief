# earnings-brief

A Claude Code skill that turns a company name or ticker into a quick-read earnings digest — sourced from public web search only (investor relations pages, press releases, regulatory filings), no paid data subscription required.

## What it does

Given a public company, it finds the primary source for its latest earnings report and produces a structured summary:

- Revenue, net income, EPS (GAAP and non-GAAP), gross/operating margin — with YoY and QoQ change
- **Trend** across the last 4-5 periods, not just one comparison point
- **vs. analyst consensus** (beat/miss/in-line), clearly labeled as third-party data the company doesn't disclose itself
- Forward guidance (if disclosed)
- Highlights and risks, distinguishing management's own words from the skill's own observations
- Source links for every number — see `earnings-brief/references/data-sources.md` for the official disclosure portal in each major market (US/SEC EDGAR, HK/HKEXnews, Japan/TDnet+EDINET, Europe)
- A "not financial advice, verify against the primary filing" disclaimer

It responds in whatever language you ask in, and can export the digest to Markdown or PDF on request (`earnings-brief/scripts/export_digest.py` — pure-Python by default, no system-level install needed).

## Usage

**Install:**
1. Import `earnings-brief.skill` into Claude Code (or copy the `earnings-brief/` folder into your skills directory).
2. Ask about a company's results — no need to name the skill explicitly. It triggers on things like:
   - "How did Apple do in their most recent earnings report?"
   - "Summarize AAPL's latest quarter"
   - "腾讯最新一季财报表现怎么样?给我一个速览。"

**Validate the skill source** (optional, requires the `skill-creator` skill's scripts):
```bash
python -m scripts.quick_validate "path/to/earnings-brief"
```

## Example

**Input:**
> 腾讯最新一季财报表现怎么样?给我一个速览。

**Output (abridged):**
```
# 腾讯控股(00700.HK)— 2026年第二季度(2Q2026)财报速览

**发布日期:** 2026年8月12日 | **数据来源:** 公司官方新闻稿

## 核心数据
| 指标 | 本季度 | 同比 YoY | 环比 QoQ |
|---|---|---|---|
| 总营收 | RMB 2,047.85亿 | +11% | +4.2% |
| 净利润(非IFRS) | RMB 684.15亿 | +9% | +0.8% |
| 每股收益(非IFRS) | RMB 7.433 | +9% | +0.9% |

## 亮点
- AI战略推进:Hy3大模型正式发布,WorkBuddy/CodeBuddy用户增长迅猛
- 广告业务受AI推荐模型驱动,增速达22%

## 风险 / 关注点
- 资本开支同比激增176%,反映AI基础设施投入大幅加码
- 自由现金流转负,主因AI算力采购的大额预付款

## 数据来源
- [Tencent Announces 2026 Second Quarter Results](...)

---
*以上内容为快速了解用的摘要,不构成投资建议。*
```

(Full template also includes a Trend table and a vs. Analyst Consensus section, omitted here for brevity — see `earnings-brief/SKILL.md`.)

## Status

v0.1.0 [released](https://github.com/h-y17/earnings-brief/releases/tag/v0.1.0). Tested on real cases across markets and reporting standards (US, HK, Mandarin and English output). Feedback and issues welcome.
