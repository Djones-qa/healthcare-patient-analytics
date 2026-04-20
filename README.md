# Healthcare Patient Analytics

![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

A comprehensive Python analytics engine for healthcare patient outcomes, readmission risk assessment, and quality metrics analysis.

## Overview

This project analyzes healthcare data to provide actionable insights on:
- **Readmission Risk**: Calculate patient readmission probabilities and risk levels
- **Department Performance**: Track departmental efficiency, satisfaction, and outcomes
- **Outcome Analysis**: Analyze treatment outcomes by diagnosis and patient demographics
- **Medication Safety**: Detect medication errors and flag high-risk scenarios
- **Data Quality**: Assess data completeness and integrity
- **Visual Analytics**: Generate comprehensive charts and reports

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd healthcare-patient-analytics
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running Tests

Execute the full test suite:
```bash
pytest tests/ -v
```

Generate an HTML test report:
```bash
pytest tests/ --html=reports/test_report.html
```

Run specific test class:
```bash
pytest tests/test_analytics.py::TestReadmissionRisk -v
```

## Project Structure

```
healthcare-patient-analytics/
├── scripts/                      # Analytics and data generation modules
│   ├── analytics.py             # Core analytics functions
│   ├── data_generator.py        # Patient data generation
│   └── visualizations.py        # Chart generation
├── tests/                        # Test suite
│   ├── test_analytics.py        # Analytics module tests
│   └── test_visualizations.py   # Visualization tests
├── data/                         # Generated datasets (CSV, SQLite)
├── visuals/                      # Generated charts (PNG)
├── reports/                      # Test and analysis reports
├── conftest.py                  # Pytest configuration and fixtures
├── pytest.ini                   # Pytest settings
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Core Modules

### `scripts/analytics.py`

**Key Functions:**
- `calculate_readmission_risk(admissions_df, patients_df)` - Compute readmission risk scores
- `calculate_department_performance(admissions_df)` - Department performance metrics
- `calculate_outcome_analysis(admissions_df, patients_df)` - Treatment outcomes by diagnosis
- `detect_medication_errors(medications_df)` - Identify medication safety issues
- `calculate_data_quality_score(patients_df, admissions_df)` - Data quality assessment
- `run_sql_queries(db_path)` - Execute analytical SQL queries

### `scripts/data_generator.py`

Generates realistic synthetic healthcare data:
- `generate_patients(n)` - Generate patient records
- `generate_admissions(patients_df, n)` - Generate admission records
- `generate_medications(admissions_df)` - Generate medication records
- `save_to_sqlite(patients, admissions, medications)` - Persist to SQLite database

### `scripts/visualizations.py`

Creates publication-ready visualizations:
- Admissions by diagnosis distribution
- Length of stay analysis
- Readmission rates by department
- Cost analysis by insurance type
- Patient outcomes heatmap
- Age vs. cost correlation
- Medication error tracking
- Patient satisfaction scores

## Test Coverage

The project includes 32 comprehensive tests covering:
- ✅ Readmission risk calculations (4 tests)
- ✅ Department performance metrics (4 tests)
- ✅ Outcome analysis (3 tests)
- ✅ Medication error detection (3 tests)
- ✅ Data quality scoring (4 tests)
- ✅ SQL query execution (4 tests)
- ✅ Visualization generation (10 tests)

All tests pass successfully with 100% coverage of core functionality.

## Requirements

- Python 3.8+
- pandas 2.2.2
- numpy 1.26.4
- matplotlib 3.8.3
- seaborn 0.13.2
- scikit-learn 1.4.1
- faker 24.0.0
- pytest 8.1.1
- sqlalchemy 2.0.28

## Usage Examples

### Basic Analysis

```python
from scripts.data_generator import generate_patients, generate_admissions
from scripts.analytics import calculate_readmission_risk

# Generate sample data
patients = generate_patients(500)
admissions = generate_admissions(patients, 1000)

# Calculate readmission risk
risk_df = calculate_readmission_risk(admissions, patients)
print(risk_df.head())
```

### Department Performance

```python
from scripts.analytics import calculate_department_performance

# Analyze department metrics
dept_performance = calculate_department_performance(admissions)
print(dept_performance[['department', 'avg_satisfaction', 'readmission_rate']])
```

### Generate Visualizations

```python
from scripts.visualizations import create_all_visualizations

# Generate all charts
create_all_visualizations(admissions, patients)
```

## Data Flow

```
generate_patients()
        ↓
generate_admissions()
        ↓
generate_medications()
        ↓
save_to_sqlite()
        ↓
[analytics functions]
        ↓
[visualizations]
        ↓
reports/
```

## Contributing

1. Ensure all tests pass: `pytest tests/`
2. Follow PEP 8 style guidelines
3. Add tests for new functionality
4. Update documentation as needed

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions, please open an issue in the repository.

---

**Last Updated:** April 2026  
**Test Status:** ✅ All 32 tests passing  
**Python Version:** 3.14.3
