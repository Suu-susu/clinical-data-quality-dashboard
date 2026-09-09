from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "synthetic_healthcare_monitoring.csv"
OUTPUT_DIR = ROOT / "outputs"
REVIEWED = OUTPUT_DIR / "reviewed_records.csv"
SUMMARY = OUTPUT_DIR / "evaluation_summary.csv"


def parse_bool(value: str) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def parse_reading(value: str):
    value = str(value).strip()
    return float(value) if value else None


def previous_valid(row, rows):
    previous = [
        item for item in rows
        if item["patient"] == row["patient"]
        and item["date"] < row["date"]
        and item["reading"] is not None
    ]
    return sorted(previous, key=lambda item: item["date"])[-1] if previous else None


def issues_for(row, rows):
    issues = []
    previous = previous_valid(row, rows)

    if row["reading"] is None or not row["complete"]:
        issues.append("Missing reading")
    if row["signal"] < 90:
        issues.append("Low signal")
    if row["duplicate"]:
        issues.append("Duplicate pattern")
    if row["reading"] is not None and row["reading"] >= 18.5:
        issues.append("High outlier")
    if previous and row["reading"] is not None and row["reading"] - previous["reading"] >= 1.2:
        issues.append("Sharp increase")
    if any(term in row["note"].lower() for term in ["drift", "review", "follow-up"]):
        issues.append("Review trend")

    return issues


def score_record(row, rows):
    issues = issues_for(row, rows)
    score = 100
    if "Missing reading" in issues:
        score -= 28
    if "Low signal" in issues:
        score -= 24 if row["signal"] < 75 else 14
    if "Duplicate pattern" in issues:
        score -= 16
    if "High outlier" in issues:
        score -= 18
    if "Sharp increase" in issues:
        score -= 10
    if "Review trend" in issues:
        score -= 8

    score = max(0, score)
    if score < 60 or "High outlier" in issues:
        risk = "High"
    elif score < 82:
        risk = "Medium"
    else:
        risk = "Good"

    if "Missing reading" in issues:
        action = "Verify source record before modelling"
    elif "High outlier" in issues or "Sharp increase" in issues:
        action = "Review clinical context and confirm anomaly"
    elif "Low signal" in issues:
        action = "Check device signal and exclude from sensitive analysis if unresolved"
    elif "Duplicate pattern" in issues:
        action = "Check timestamp and remove duplicate before reporting"
    elif risk == "Medium":
        action = "Keep in monitored dataset with analyst note"
    else:
        action = "Use for summary reporting"

    return {
        **row,
        "quality_score": score,
        "risk": risk,
        "issues": "; ".join(issues) if issues else "Clean",
        "recommended_action": action,
    }


def load_rows():
    with INPUT.open("r", newline="", encoding="utf-8") as file:
        rows = []
        for row in csv.DictReader(file):
            rows.append({
                "patient": row["patient"],
                "cohort": row["cohort"],
                "date": row["date"],
                "reading": parse_reading(row["reading"]),
                "signal": int(row["signal"]),
                "complete": parse_bool(row["complete"]),
                "duplicate": parse_bool(row["duplicate"]),
                "reviewed": parse_bool(row["reviewed"]),
                "note": row["note"],
            })
    return rows


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def summarise(rows):
    by_cohort = defaultdict(list)
    for row in rows:
        by_cohort[row["cohort"]].append(row)

    output = []
    for cohort, cohort_rows in sorted(by_cohort.items()):
        output.append({
            "cohort": cohort,
            "records": len(cohort_rows),
            "average_quality_score": round(mean(row["quality_score"] for row in cohort_rows), 1),
            "flagged_records": sum(row["risk"] != "Good" for row in cohort_rows),
            "high_risk_records": sum(row["risk"] == "High" for row in cohort_rows),
            "missing_readings": sum("Missing reading" in row["issues"] for row in cohort_rows),
            "low_signal_records": sum("Low signal" in row["issues"] for row in cohort_rows),
        })
    return output


def main():
    rows = load_rows()
    reviewed = [score_record(row, rows) for row in rows]
    write_csv(REVIEWED, reviewed)
    write_csv(SUMMARY, summarise(reviewed))
    print(f"Input records: {len(rows)}")
    print(f"Flagged records: {sum(row['risk'] != 'Good' for row in reviewed)}")
    print(f"High risk records: {sum(row['risk'] == 'High' for row in reviewed)}")
    print(f"Wrote {REVIEWED}")
    print(f"Wrote {SUMMARY}")


if __name__ == "__main__":
    main()
