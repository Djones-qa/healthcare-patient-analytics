"""
Tests for healthcare visualizations.
"""
import pytest
import os
import sys
import matplotlib
matplotlib.use("Agg")
sys.path.insert(0, os.path.abspath("."))
from scripts.data_generator import (
    generate_patients, generate_admissions, generate_medications
)
from scripts.visualizations import (
    plot_admissions_by_diagnosis, plot_length_of_stay,
    plot_readmission_rates, plot_cost_by_insurance,
    plot_patient_outcomes, plot_age_vs_cost,
    plot_medication_errors, plot_satisfaction_by_dept
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


class TestVisualizations:

    def test_admissions_by_diagnosis_created(self, admissions):
        path = plot_admissions_by_diagnosis(admissions)
        assert os.path.exists(path)
        assert os.path.getsize(path) > 0

    def test_length_of_stay_chart_created(self, admissions):
        path = plot_length_of_stay(admissions)
        assert os.path.exists(path)

    def test_readmission_rates_chart_created(self, admissions):
        path = plot_readmission_rates(admissions)
        assert os.path.exists(path)

    def test_cost_by_insurance_chart_created(self, admissions):
        path = plot_cost_by_insurance(admissions)
        assert os.path.exists(path)

    def test_patient_outcomes_chart_created(self, admissions):
        path = plot_patient_outcomes(admissions)
        assert os.path.exists(path)

    def test_age_vs_cost_chart_created(self, admissions, patients):
        path = plot_age_vs_cost(admissions, patients)
        assert os.path.exists(path)

    def test_medication_errors_chart_created(self, medications):
        path = plot_medication_errors(medications)
        assert os.path.exists(path)

    def test_satisfaction_chart_created(self, admissions):
        path = plot_satisfaction_by_dept(admissions)
        assert os.path.exists(path)

    def test_all_charts_are_png(self):
        charts = [f for f in os.listdir("visuals") if f.endswith(".png")]
        assert len(charts) >= 8

    def test_all_charts_non_empty(self):
        for f in os.listdir("visuals"):
            if f.endswith(".png"):
                assert os.path.getsize(f"visuals/{f}") > 0
