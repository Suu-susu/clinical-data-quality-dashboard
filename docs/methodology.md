# Methodology

## Objective

The project evaluates synthetic monitoring records before they are used for
reporting, modelling or stakeholder decision making. The central question is:
which records are reliable enough for analysis, and which records require
review?

## Data Fields

| Field | Purpose |
| --- | --- |
| patient | Synthetic participant identifier |
| cohort | Programme or research grouping |
| date | Observation date |
| reading | Numeric monitoring value |
| signal | Device or capture quality percentage |
| complete | Whether the record contains the expected primary reading |
| duplicate | Whether the record resembles a duplicate or repeated pattern |
| reviewed | Whether an analyst review flag is already present |
| note | Analyst-readable quality note |

## Quality Checks

The evaluation model checks:

- missing primary readings;
- low signal quality;
- duplicate-like records;
- high outlier readings;
- sharp increases compared with the previous valid reading for the same patient;
- drift, review or follow-up notes.

## Scoring Logic

Each record starts at 100. Penalties are applied for data-quality and
interpretation risks. The final quality score is used to assign:

- **Good:** usable for summary reporting;
- **Medium:** usable with analyst notes or further checking;
- **High:** needs source verification or domain review before modelling.

## Interpretation

The scoring model is deliberately transparent. The goal is not to replace
clinical judgement. The goal is to help analysts, research managers and clients
understand where the data is incomplete, unreliable or risky before drawing
conclusions.

## Limitations

The dataset is synthetic and small. It does not represent real patient outcomes,
clinical decisions or production monitoring systems. The model is a portfolio
demonstration of analytical process, not a validated clinical model.
