# Healthcare Data Quality and Evaluation Dashboard

Portfolio project by Jiashuo Su for data analysis, modelling, research and
evaluation internship applications.

Live dashboard:
https://suu-susu.github.io/clinical-data-quality-dashboard/

## Project Summary

This project uses synthetic healthcare monitoring records to demonstrate how an
analyst can move from raw observations to a defensible evaluation output. It is
designed to show more than front-end dashboard work: it includes data-quality
rules, an explainable scoring model, anomaly review, cohort comparison,
stakeholder findings and exportable review records.

The dataset is synthetic. It is not real patient data, not clinical advice and
not work completed for any company.

## Why This Is More Than A Dashboard

- **Data cleaning:** missing readings, duplicate-like records and signal-quality
  issues are explicitly detected.
- **Modelling logic:** every record receives an explainable quality score and
  risk label.
- **Evaluation thinking:** the dashboard asks whether the data is reliable
  enough for reporting or modelling.
- **Research communication:** findings are written as concise stakeholder
  recommendations, not only charts.
- **Export workflow:** reviewed records can be exported for further analysis.

## Internship Fit

This project maps to data, analysis and modelling internship work:

- analyse, evaluate and interpret research data;
- handle ambiguity, missingness and changing data quality;
- build simple models that translate raw data into insight;
- create dashboard, report and infographic-style outputs;
- explain findings clearly to technical and non-technical stakeholders;
- show attention to detail through transparent validation rules.

## Current Features

- Filters by cohort, patient, risk level, minimum quality score and note text.
- Quality score based on completeness, signal quality, duplicate patterns,
  outliers, sharp increases and drift or review notes.
- Trend chart with high-risk markers and moving average.
- Issue-mix chart.
- Cohort comparison chart.
- Evaluation matrix.
- Reviewed record table with risk, issues and recommended action.
- Auto-generated recommendation report.
- CSV export of filtered reviewed records.

## Repository Structure

```text
.
|-- index.html
|-- README.md
|-- data/
|   `-- synthetic_healthcare_monitoring.csv
|-- analysis/
|   `-- quality_model.py
|-- docs/
|   `-- methodology.md
`-- outputs/
    |-- reviewed_records.csv
    `-- evaluation_summary.csv
```

## Method

The score starts at 100 and applies penalties for known data-quality and
interpretation risks:

- missing readings;
- low signal quality;
- duplicate-like patterns;
- high outliers;
- sharp increases;
- drift or manual review notes.

The result is intentionally explainable. In research and evaluation settings,
simple transparent models are often easier to defend than complex black-box
scores, especially when the task is to communicate quality concerns to clients.

## Next Steps

- Add a Python notebook for exploratory analysis.
- Add formal tests for scoring rules.
- Expand the synthetic dataset with more cohorts and intervention periods.
- Add confidence intervals or simple forecasting for evaluation reporting.
