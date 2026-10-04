# External data sources (public, safe to commit)

All sources retrieved on 2026-10-04.

| File | Series | Geography | How it is used | Source | Notes / limitations |
|---|---|---|---|---|---|
| `tal_rent_adjustment.csv` | TAL "estimation moyenne d'ajustement de base", unheated dwelling, 2022–2026 | Québec | Anchor for **QC renewals** (`external_anchor`) | TAL press releases (official PDFs for 2022–2025); 2026 from the TAL page "Pourcentages applicables aux critères de fixation de loyer" | 2026 = 3.1 % was published 2026-01-19, **after** the data cutoff, so it only enters the labelled central forecast, never the backtests. 2026 uses the new TAL method (3-year average of Québec CPI); under that method the TAL gives 4.5 % for 2025, so 5.9 % → 3.1 % is partly a change of method. 2019–2021 not collected (the official PDFs are no longer at the usual URLs). |
| `ontario_rent_guideline.csv` | Ontario rent increase guideline 2019–2026 | Ontario | **Context only** for The Met (exempt: first residential occupancy after 2018-11-15) | https://www.ontario.ca/page/rent-increase-guideline | All eight values checked on the page. 2026 = 2.1 % was announced mid-2025 (before cutoff). |
| `statcan_cpi_rent_monthly.csv` | CPI, "Rent" component, monthly index (2002=100), 2015-01 → latest | QC, ON (province level; no city-level rent CPI in this table) | Anchor for **QC turnovers** and **both ON segments**: Nov(Y−1)/Nov(Y−2) change (the November CPI comes out mid-December, so it's the latest available at Dec 31) | Statistics Canada table 18-10-0004-01, full-table CSV: https://www150.statcan.gc.ca/n1/tbl/csv/18100004-eng.zip | The notebook drops any month after 2025-12-31 (no leakage). Later rows stay in the file for the ex-post check (§10.4) only. |
| `cmhc_rms_official.csv` | CMHC Rental Market Survey, official data tables (editions 2021–2025): **fixed-sample** % change of 2-bedroom rent (Table 1.0, 2020–2025), vacancy rate (Table 1.0), turnover vs non-turnover rent gap (Table 6.2, 2024–2025) | Montréal CMA, Ottawa-Gatineau CMA (Ont. part), Canada | Reconciliation (§7.3) and **alternative anchor** tested in the backtest (§9.4c); vacancy = context only | `https://assets.cmhc-schl.gc.ca/.../rental-market-report-data-tables/<year>/rmr-canada-<year>-en.xlsx` (exact URL per row in the file) | `published_date` = edition release date (approximate days; the month is what matters for leakage: the 2022 and 2023 editions came out in late January of the next year). 2019/2020 editions are not at the same URL. |

## Regulation and building ages (used in §6.2, `building_regulation`)

| Item | Source(s) | Notes |
|---|---|---|
| TAL 2025 = 5.9 % | https://www.tal.gouv.qc.ca/sites/default/files/COMMUNIQUE_FIXATION_2025_FR.pdf (Tableau 2) | Old method, unheated dwelling |
| TAL 2026 = 3.1 % | https://www.tal.gouv.qc.ca/fr/reconduction-du-bail-et-fixation-de-loyer/pourcentages-applicables-aux-criteres-de-fixation-de-loyer | New method; same page gives 4.5 % for 2025 under the new method |
| Ontario guideline 2019–2026 and the post-2018-11-15 exemption | https://www.ontario.ca/page/rent-increase-guideline | |
| Section F (art. 1955 C.c.Q.) and Bill 31 (maximum rent, from 2024-02-21) | https://www.tal.gouv.qc.ca/fr/reconduction-du-bail-et-fixation-de-loyer/augmentation-de-loyer ; https://www.corpiq.com/fr/nouvelles/2288-aide-memoire-concernant-la-loi-31-pour-les-sections-f-et-g-du-bail.html ; https://www.apq.org/actualites/articles/clause-f-completee-le-prix-du-loyer-doit-pouvoir-evoluer-dans-les-5-premieres-annees-du-bail/ | |
| The Met completed 2023 | https://www.apartments.com/the-met-ottawa-on/e603gqm/ ; https://rentals.ca/ottawa/180-metcalfe-street | Listing sites (secondary) |
| Le Carlyle delivered 2023-07-01 | https://www.guidehabitation.ca/fr/11785/le-carlyle/ ; https://forum.agoramtl.com/t/le-carlyle-7-etages-2023/3911 | Secondary |
| Westpark built 2023 | https://rentals.ca/pointe-claire/265-boul-brunswick | Secondary |
| Daniel-Johnson ph. 1 2018–20, ph. 2 2021–23 | https://www.guidehabitation.ca/fr/10195/equinoxe-daniel-johnson/ | Secondary |
| Lévesque 2017–2019 | https://www.projethabitation.com/Projets/Laval/Chomedey/Equinoxe-Levesque-5552/ ; https://forum.agoramtl.com/t/equinoxe-levesque-27-etages-2019/1125 | Secondary |
| Saint-Elzéar ph. 3 occupancy April 2025 | https://www.guidehabitation.ca/fr/9922/equinoxe-st-elzear-phase-3/ | Secondary |

Building years come from project and listing sites, not official registries, so the notebook says "according to project listings".
