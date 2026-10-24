# Data

| Path | What it is |
|---|---|
| `sources.yaml` | Source catalog (see `docs/katalog-izvora.md`) |
| `archive/YYYY-MM.jsonl` | Collected items, one JSON object per line, by month first seen |
| `state/seen.json` | IDs of items already seen (kept 180 days) — prevents re-collecting |
| `state/health.json` | Per-source status: last success, errors, item counts |
| `state/runs.jsonl` | One summary line per run |
| `reports/latest.md` | **Inflow report** — new items of the last 48 hours and source problems |

Written by `pipeline/ingest.py`, run every 3 hours by `.github/workflows/ingest.yml` — started by the Worker's Cron Trigger (GitHub's own schedule did not fire for this repository).

Item `status`: `baseline` = present when a source was first added (not news), `new` = appeared later.
`duplicate_of` points to an earlier item from another source with a near-identical title.
Only titles, links and a short excerpt (≤300 characters) are stored; the full text stays with the source.

## AI drafting (phase 4)

`pipeline/draft.py` runs after collection when the `ANTHROPIC_API_KEY` repository secret is set:
new items are scored in batches (Claude Haiku 5.5); items above the threshold (importance ≥ 3 for core
topics, ≥ 4 for Data & AI) are fetched and drafted (Claude Opus 5.5), and each draft is opened as a pull
request assigned to the editor. Merge = publish.

| Path | What it is |
|---|---|
| `state/ai.json` | Triage decision per item (skipped / selected / drafted / failed / duplicate) and monthly API spend |
| `reports/drafts.md` | Last drafting run, monthly spend against the budget, recently skipped items |

Limits: at most 6 drafts per run (`MAX_DRAFTS_PER_RUN`), monthly budget $12 (`AI_MONTHLY_BUDGET_USD`);
when the budget is reached, selected items wait for the next month.
