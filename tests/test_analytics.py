"""
Tests for healthcare analytics calculations.
"""
import pytest
import pandas as pd
import sys, os
sys.path.insert(0, os.path.abspath("."))
from scripts.data_generator import (
    generate_patients, generate_admissions,
    generate_medications, save_to_sqlite
)
from scripts.analytics import (
    calculate_readmission_risk, calculate_department_performance,
    calculate_outcome_analysis, detect_medication_errors,
    calculate_data_quality_score, run_sql_queries
)


@pytest.fixture(scope="module")
def patients():
    return generate_patients(500)


@pytest.fixture(scope="module")
def admissions(patients):
    return generate_admissions(patients, 1000)


@pytest.fixture(scope="module")
def medications(admissions):
    return generate_medications(admissions)


@pytest.fixture(scope="module")
def db(patients, admissions, medications):
    save_to_sqlite(patients, admissions, medications)
    return "data/healthcare.db"


class TestReadmissionRisk:

    def test_returns_dataframe(self, admissions, patients):
        result = calculate_readmission_risk(admissions, patients)
        assert isinstance(result, pd.DataFrame)

    def test_readmission_rate_within_range(self, admissions, patients):
        result = calculate_readmission_risk(admissions, patients)
        assert result["readmission_rate"].between(0, 1).all()

    def test_risk_level_values_valid(self, admissions, patients):
        result = calculate_readmission_risk(admissions, patients)
        valid = {"Low", "Medium", "High", "Critical"}
        actual = set(result["risk_level"].dropna().astype(str).unique())
        assert actual.issubset(valid)

    def test_sorted_by_rate_descending(self, admissions, patients):
        result = calculate_readmission_risk(admissions, patients)
        rates = result["readmission_rate"].tolist()
        assert rates == sorted(rates, reverse=True)


class TestDepartmentPerformance:

    def test_returns_all_departments(self, admissions):
        result = calculate_department_performance(admissions)
        assert len(result) == 10

    def test_avg_satisfaction_within_range(self, admissions):
        result = calculate_department_performance(admissions)
        assert result["avg_satisfaction"].between(1, 5).all()

    def test_avg_cost_positive(self, admissions):
        result = calculate_department_performance(admissions)
        assert (result["avg_cost"] > 0).all()

    def test_readmission_rate_within_range(self, admissions):
        result = calculate_department_performance(admissions)
        assert result["readmission_rate"].between(0, 1).all()


class TestOutcomeAnalysis:

    def test_returns_dataframe(self, admissions, patients):
        result = calculate_outcome_analysis(admissions, patients)
        assert isinstance(result, pd.DataFrame)

    def test_avg_cost_positive(self, admissions, patients):
        result = calculate_outcome_analysis(admissions, patients)
        assert (result["avg_cost"] > 0).all()

    def test_has_required_columns(self, admissions, patients):
        result = calculate_outcome_analysis(admissions, patients)
        required = ["diagnosis", "total_cases", "avg_los",
                    "avg_cost", "readmission_rate"]
        for col in required:
            assert col in result.columns


class TestMedicationErrors:

    def test_returns_dataframe(self, medications):
        result = detect_medication_errors(medications)
        assert isinstance(result, pd.DataFrame)

    def test_error_rate_within_range(self, medications):
        result = detect_medication_errors(medications)
        assert result["error_rate"].between(0, 1).all()

    def test_high_risk_flag_is_boolean(self, medications):
        result = detect_medication_errors(medications)
        assert result["high_risk"].dtype == bool


class TestDataQuality:

    def test_returns_dict(self, patients, admissions):
        result = calculate_data_quality_score(patients, admissions)
        assert isinstance(result, dict)

    def test_completeness_within_range(self, patients, admissions):
        result = calculate_data_quality_score(patients, admissions)
        assert 0 <= result["completeness_pct"] <= 100

    def test_no_duplicate_patients(self, patients, admissions):
        result = calculate_data_quality_score(patients, admissions)
        assert result["duplicate_patients"] == 0

    def test_overall_quality_score_within_range(self, patients, admissions):
        result = calculate_data_quality_score(patients, admissions)
        assert 0 <= result["overall_quality_score"] <= 1


class TestSQLQueries:

    def test_all_query_keys_returned(self, db):
        results = run_sql_queries(db)
        expected = ["top_diagnoses", "department_summary",
                    "high_cost_admissions", "readmission_by_insurance",
                    "medication_errors_summary", "outcomes_by_age_group"]
        for key in expected:
            assert key in results

    def test_top_diagnoses_returns_10(self, db):
        results = run_sql_queries(db)
        assert len(results["top_diagnoses"]) == 10

    def test_department_summary_returns_all(self, db):
        results = run_sql_queries(db)
        assert len(results["department_summary"]) == 10

    def test_readmission_by_insurance_not_empty(self, db):
        results = run_sql_queries(db)
        assert len(results["readmission_by_insurance"]) > 0
