# Équinoxe: 2026 rent increase (JADCO « Clés en main » · CodeML 2026)

Team J-LLM (Josha, Leo, Leonardo, Mohamed). How much will Collection Équinoxe's rents go up in 2026? The full analysis is in `equinoxe_2026.ipynb`. `column_guide.ipynb` shows the four data files with our own column names: the first rows with the new names, then what each column really contains.

## Setup
Python 3.11+ (tested with 3.13). From this folder:
```bash
python -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```
Library versions we used: pandas 3.0.6, numpy 2.5.3, matplotlib 3.11.2, pyarrow 25.0.1, nbformat 5.11.1, nbconvert 7.17.1,
ipykernel 7.4.0, jupyter 1.1.1 (Python 3.13.5, Windows 11).

## Our answer

| Figure | 2026 | What it means |
|---|---|---|
| **HEUC-2026** (headline) | **3.0 %**. Discount scenarios: 0.7 % / 5.2 % | Yearly growth of **effective** rent (after concessions), each apartment compared with its own previous lease (`sPropCode + sUnitCode`). Four segments, {QC, ON} × {renewal, new tenant}, weighted by their expected number of leases. |
| HCUC-2026 | 5.2 % | Same thing on **contract** rent (what renewal notices and the TAL / Ontario rules apply to) |
| Strict variant | 3.7 % effective / 5.9 % contract | Only uses what was public on 2025-12-31 (TAL 2025 instead of TAL 2026) |

### Running it
1. The CRM extract is confidential and **not included here**. Ask a teammate for the 4 files and copy them unchanged into `data/raw/`:
   `equinoxe_listings.csv`, `equinoxe_lease_history.csv`, `equinoxe_concessions.csv`, `equinoxe_asking_history.csv`.
2. Build everything (about 20 minutes):
   ```bash
   python scripts/assemble_notebook.py --sections   # runs nb/00..10, then builds and runs equinoxe_2026.ipynb
   ```
   Then open `column_guide.ipynb` (runs in a few seconds once the step above has been done). Its outputs are cleared
   in this repository because they show rows of the confidential files; run it with the data to see them.
   You can also open any `nb/XX_*.ipynb` on its own. Its first cell (tagged `io-only`) loads what it needs.

### How we got there
1. **Mix effect (§3).** The plain median says +10.8 % in 2023. Most of that is three upscale buildings joining the extract (Le Carlyle, The Met, Westpark), not prices going up.
2. **Same-apartment pairs (§4).** Each lease is compared with the previous lease of the same apartment (`prop_code + unit_code`; `sSite + sUnitCode` would merge 248 units). We keep gaps between 0.5 and 2.5 years and annualise: `(rent / prev_rent)^(1 / gap_years) − 1`.
3. **Concessions (§5).** `rent_effective` is our source of truth. `PromoPay` is a one-time credit, not a monthly fee. From 2024 effective growth falls behind contract growth because discounts got **deeper** (≈ 4 % → 9 % of rent), not just more common.
4. **Renewals vs new tenants, QC vs ON (§6).** In Québec the TAL calculation is a reference for renewals, not a cap. We checked building ages phase by phase. In 2026, Section F (buildings ready ≤ 5 years) probably covers Le Carlyle, Westpark, Daniel-Johnson phase 2 and Saint-Élzéar phase 3. The Met (Ottawa, completed 2023) is exempt from Ontario's guideline (first occupied after 2018-11-15), so no cap is applied to it.
5. **External data (§7).** TAL, Ontario guideline, Statistics Canada rent CPI (18-10-0004-01) and the official CMHC Rental Market Survey tables (fixed-sample 2-bedroom rent change, vacancy, turnover premium), reconciled with our numbers year by year. A side finding we liked: the press reported "+10.7 % in Ottawa in 2024", but CMHC's fixed sample says +5.0 %. The same mix effect shows up in public statistics.
6. **Forecast (§8).** Per segment: `0.5 × our trend (last 3 years, recent years weigh more) + 0.5 × a public anchor` (TAL for QC renewals, rent CPI for the rest). Contract growth is then converted to effective growth with `(1 + g_eff) = (1 + g_contract) × (1 − d_new) / (1 − d_old)`.
7. **Backtest (§9).** Same function, data cut at Dec 31 of the year before, external data limited to what was published by then. Effective MAE ≈ 1.3 pt over 2023–2025, better than repeating last year (1.6), our trend alone (1.9) and the naive median (3.6), and about the same as the anchor alone (1.35). The weights were fixed beforehand, not tuned on these years. We also checked that:
   - picking the weight by leave-one-year-out does worse (1.6);
   - a CMHC anchor instead of CPI gives almost the same error (1.25) and 2.7 % for 2026;
   - a simple regression does worse (1.9).

### What we're less sure about
Only 3 backtest years, and Ontario only has pairs from 2024. The concession persistence (0.5) is a neutral choice, which is why we show low/high scenarios. Building years come from project and listing sites, and we can't see whether the Section F box is ticked on each lease. The TAL changed its method in 2026, so 5.9 % → 3.1 % is not a like-for-like drop. Full list: notebook §10.6.

## Public sources
TAL (tal.gouv.qc.ca) · Government of Ontario rent increase guideline (ontario.ca/page/rent-increase-guideline) ·
Statistics Canada table 18-10-0004-01 · CMHC Rental Market Survey data tables, 2021–2025 editions (cmhc-schl.gc.ca).
Full list with URLs: `data/external/sources.md`.

## Tools
Python (pandas, numpy, matplotlib, pyarrow), Jupyter. We used Claude (Anthropic) for coding help and document search, and checked the results ourselves.

## Confidentiality
The CRM extract is never shared, published or included here. The main notebook only shows aggregates; `column_guide.ipynb` shows the first 3 rows of each file, as the organisers' starter notebook does. Keep this repository private.
