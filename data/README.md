# Data

| Path | What it is |
|---|---|
| `sources.yaml` | Source catalog (see `docs/katalog-izvora.md`) |
| `archive/YYYY-MM.jsonl` | Collected items, one JSON object per line, by month first seen |
| `state/seen.json` | IDs of items already seen (kept 180 days) — prevents re-collecting |
| `state/health.json` | Per-source status: last success, errors, item counts |
| `state/runs.jsonl` | One summary line per run |
| `reports/latest.md` | **Inflow report** — new items of the last 48 hours and source problems |

Written by `pipeline/ingest.py`, run three times a day by `.github/workflows/ingest.yml`.

Item `status`: `baseline` = present when a source was first added (not news), `new` = appeared later.
`duplicate_of` points to an earlier item from another source with a near-identical title.
Only titles, links and a short excerpt (≤300 characters) are stored; the full text stays with the source.
