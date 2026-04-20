"""
Healthcare analytics engine —
patient outcomes, readmission risk, and quality metrics.
"""
import pandas as pd
import numpy as np
import sqlite3


def calculate_readmission_risk(admissions_df: pd.DataFrame,
                                patients_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate readmission risk score per patient."""
    merged = admissions_df.merge(patients_df, on="patient_id")
    patient_stats = merged.groupby("patient_id").agg(
        total_admissions=("admission_id", "count"),
        readmissions=("is_readmission", "sum"),
        avg_los=("length_of_stay", "mean"),
        avg_cost=("total_cost", "mean"),
        avg_mortality_risk=("mortality_risk", "mean"),
    ).reset_index()
    patient_stats["readmission_rate"] = (
        patient_stats["readmissions"] /
        patient_stats["total_admissions"]
    ).round(3)
    patient_stats["risk_level"] = pd.cut(
        patient_stats["readmission_rate"],
        bins=[-0.01, 0.1, 0.25, 0.5, 1.01],
        labels=["Low", "Medium", "High", "Critical"]
    )
    return patient_stats.sort_values(
        "readmission_rate", ascending=False)


def calculate_department_performance(admissions_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate performance metrics by department."""
    dept_stats = admissions_df.groupby("department").agg(
        total_admissions=("admission_id", "count"),
        avg_los=("length_of_stay", "mean"),
        avg_cost=("total_cost", "mean"),
        readmission_rate=("is_readmission", "mean"),
        avg_satisfaction=("patient_satisfaction", "mean"),
        medication_errors=("medication_errors", "sum"),
        avg_mortality_risk=("mortality_risk", "mean"),
    ).round(2).reset_index()
    return dept_stats.sort_values("avg_satisfaction", ascending=False)


def calculate_outcome_analysis(admissions_df: pd.DataFrame,
                                patients_df: pd.DataFrame) -> pd.DataFrame:
    """Analyze treatment outcomes by diagnosis."""
    merged = admissions_df.merge(patients_df, on="patient_id")
    outcome_stats = merged.groupby("diagnosis").agg(
        total_cases=("admission_id", "count"),
        avg_los=("length_of_stay", "mean"),
        avg_cost=("total_cost", "mean"),
        readmission_rate=("is_readmission", "mean"),
        avg_mortality_risk=("mortality_risk", "mean"),
        avg_satisfaction=("patient_satisfaction", "mean"),
    ).round(3).reset_index()
    return outcome_stats.sort_values("total_cases", ascending=False)


def detect_medication_errors(medications_df: pd.DataFrame) -> pd.DataFrame:
    """Identify medication error patterns."""
    error_summary = medications_df.groupby("medication").agg(
        total_administrations=("med_id", "count"),
        errors=("is_error", "sum"),
        error_rate=("is_error", "mean"),
    ).reset_index()
    error_summary["error_rate"] = error_summary["error_rate"].round(3)
    error_summary["high_risk"] = error_summary["error_rate"] > 0.05
    return error_summary.sort_values("error_rate", ascending=False)


def calculate_data_quality_score(patients_df: pd.DataFrame,
                                  admissions_df: pd.DataFrame) -> dict:
    """Calculate overall data quality metrics."""
    patient_nulls = patients_df.isnull().sum().sum()
    admission_nulls = admissions_df.isnull().sum().sum()
    total_cells = (len(patients_df) * len(patients_df.columns) +
                   len(admissions_df) * len(admissions_df.columns))
    completeness = round((1 - (patient_nulls + admission_nulls) /
                         total_cells) * 100, 2)
    duplicate_patients = patients_df["patient_id"].duplicated().sum()
    duplicate_admissions = admissions_df["admission_id"].duplicated().sum()

    bmi_valid = admissions_df["length_of_stay"].between(1, 365).all()
    cost_valid = (admissions_df["total_cost"] > 0).all()
    satisfaction_valid = admissions_df[
        "patient_satisfaction"].between(1, 5).all()

    return {
        "completeness_pct": completeness,
        "duplicate_patients": int(duplicate_patients),
        "duplicate_admissions": int(duplicate_admissions),
        "los_validity": bool(bmi_valid),
        "cost_validity": bool(cost_valid),
        "satisfaction_validity": bool(satisfaction_valid),
        "overall_quality_score": round(
            (completeness / 100) * 0.4 +
            (1 - duplicate_patients / len(patients_df)) * 0.3 +
            (1 - duplicate_admissions / len(admissions_df)) * 0.3, 3
        ),
    }


def run_sql_queries(db_path: str = "data/healthcare.db") -> dict:
    """Run clinical SQL investigation queries."""
    conn = sqlite3.connect(db_path)
    queries = {
        "top_diagnoses": """
            SELECT diagnosis,
                   COUNT(*) as cases,
                   ROUND(AVG(length_of_stay), 2) as avg_los,
                   ROUND(AVG(total_cost), 2) as avg_cost,
                   ROUND(100.0 * SUM(is_readmission) / COUNT(*), 2)
                   as readmission_pct
            FROM admissions
            GROUP BY diagnosis
            ORDER BY cases DESC
            LIMIT 10
        """,
        "department_summary": """
            SELECT department,
                   COUNT(*) as admissions,
                   ROUND(AVG(length_of_stay), 2) as avg_los,
                   ROUND(AVG(total_cost), 2) as avg_cost,
                   ROUND(AVG(patient_satisfaction), 2) as avg_satisfaction,
                   SUM(medication_errors) as total_errors
            FROM admissions
            GROUP BY department
            ORDER BY admissions DESC
        """,
        "high_cost_admissions": """
            SELECT a.admission_id, p.age, p.insurance,
                   a.diagnosis, a.department,
                   a.length_of_stay, a.total_cost,
                   a.outcome
            FROM admissions a
            JOIN patients p ON a.patient_id = p.patient_id
            WHERE a.total_cost > 100000
            ORDER BY a.total_cost DESC
            LIMIT 10
        """,
        "readmission_by_insurance": """
            SELECT insurance,
                   COUNT(*) as total_admissions,
                   SUM(is_readmission) as readmissions,
                   ROUND(100.0 * SUM(is_readmission) /
                   COUNT(*), 2) as readmission_rate
            FROM admissions
            GROUP BY insurance
            ORDER BY readmission_rate DESC
        """,
        "medication_errors_summary": """
            SELECT medication,
                   COUNT(*) as administrations,
                   SUM(is_error) as errors,
                   ROUND(100.0 * SUM(is_error) / COUNT(*), 2)
                   as error_rate_pct
            FROM medications
            GROUP BY medication
            ORDER BY error_rate_pct DESC
        """,
        "outcomes_by_age_group": """
            SELECT p.age_group, a.outcome,
                   COUNT(*) as count,
                   ROUND(AVG(a.total_cost), 2) as avg_cost
            FROM admissions a
            JOIN patients p ON a.patient_id = p.patient_id
            GROUP BY p.age_group, a.outcome
            ORDER BY p.age_group, count DESC
        """,
    }
    results = {}
    for name, query in queries.items():
        results[name] = pd.read_sql_query(query, conn)
    conn.close()
    return results
