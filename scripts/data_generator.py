import pandas as pd
import numpy as np
import sqlite3
import os

def generate_patients(n):
    return pd.DataFrame({
        "patient_id": [f"P{str(i).zfill(5)}" for i in range(1, n+1)],
        "age": np.random.randint(18, 100, n),
        "insurance": np.random.choice(["Medicare", "Medicaid", "Private", "Uninsured"], n),
        "age_group": np.random.choice(["18-35", "36-50", "51-65", "65+"], n)
    })

def generate_admissions(patients_df, n):
    patient_ids = patients_df["patient_id"].tolist()
    return pd.DataFrame({
        "admission_id": [f"A{str(i).zfill(5)}" for i in range(1, n+1)],
        "patient_id": np.random.choice(patient_ids, n),
        "length_of_stay": np.random.randint(1, 30, n),
        "total_cost": np.random.uniform(100.0, 150000.0, n),
        "is_readmission": np.random.choice([0, 1], n, p=[0.8, 0.2]),
        "mortality_risk": np.random.uniform(0.0, 1.0, n),
        "insurance": np.random.choice(["Medicare", "Medicaid", "Private", "Uninsured"], n),
        "department": np.random.choice([
            "Emergency", "Cardiology", "Neurology", "Oncology", "Pediatrics", 
            "Orthopedics", "Surgery", "ICU", "Psychiatry", "Radiology"
        ], n),
        "patient_satisfaction": np.random.randint(1, 6, n),
        "medication_errors": np.random.choice([0, 1, 2], n, p=[0.9, 0.08, 0.02]),
        "diagnosis": np.random.choice([
            "Heart Failure", "Stroke", "Pneumonia", "Sepsis", "Diabetes", 
            "Cancer", "Trauma", "COVID-19", "Asthma", "CKD"
        ], n),
        "outcome": np.random.choice(["Discharged", "Transferred", "Deceased", "AMA"], n)
    })

def generate_medications(admissions_df):
    admission_ids = admissions_df["admission_id"].tolist()
    n = len(admission_ids) * 2
    return pd.DataFrame({
        "med_id": [f"M{str(i).zfill(6)}" for i in range(1, n+1)],
        "admission_id": np.random.choice(admission_ids, n),
        "medication": np.random.choice([
            "Aspirin", "Metoprolol", "Lisinopril", "Metformin", "Atorvastatin", 
            "Albuterol", "Omeprazole", "Gabapentin", "Amlodipine", "Losartan"
        ], n),
        "is_error": np.random.choice([0, 1], n, p=[0.95, 0.05])
    })

def save_to_sqlite(patients_df, admissions_df, medications_df, db_path="data/healthcare.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    patients_df.to_sql("patients", conn, if_exists="replace", index=False)
    admissions_df.to_sql("admissions", conn, if_exists="replace", index=False)
    medications_df.to_sql("medications", conn, if_exists="replace", index=False)
    conn.close()
