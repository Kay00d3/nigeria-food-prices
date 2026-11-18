# Nigerian Food Prices and Economic Shocks (Group B)

Do fuel prices (PMS) and the exchange rate help predict next month's food prices in Nigerian markets, and how did prices change after the fuel subsidy removal (May 2023) and the naira float (June 2023)?

## Team and responsibilities

| Member | Main responsibilities |
|---|---|
| Olukayode Ogunmoroti (Leader) | Repo management, merged dataset, evaluation framework, XGBoost (Models A and B), model comparison, final report |
| Egede Darryl | WFP food price data: cleaning, market/commodity selection, monthly conversion |
| Farid Aderogba | Exchange rate and PMS data: cleaning, monthly alignment, lag features |
| Chukwudi Nwanokwai | Descriptive before/after analysis, tables and charts |
| Akachukwu Ugwu | Linear Regression and Random Forest (Models A and B), feature importance |

## Data sources

- Food prices: WFP VAM Food Prices (data.humdata.org)
- Exchange rate: Central Bank of Nigeria (cbn.gov.ng)
- PMS price: NBS PMS Price Watch (nigerianstat.gov.ng)

## Folder structure

- `data/raw/`: original downloads, never edited
- `data/processed/`: cleaned and merged data
- `notebooks/`: one notebook per task, named `firstname_task.ipynb` (e.g. `farid_clean_fx_pms.ipynb`)
- `src/`: reusable Python scripts
- `reports/`: report sections (e.g. `reports/egede_data_methods.md`) and `reports/figures/`

## Git rules

1. Never commit directly to `main`. Work on your own branch: `firstname/task-name`.
2. Commit small and often, with a clear message ("Clean CBN exchange rate data").
3. Push at the end of every work session.
4. `git pull origin main` before you start working.
5. Open a pull request when a task is done. The leader merges after review.
6. Only edit your own notebook files.
7. Never commit passwords or API keys.

## Setup

```bash
pip install -r requirements.txt
```
