"""
Healthcare analytics visualizations.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

sns.set_theme(style="darkgrid")
os.makedirs("visuals", exist_ok=True)

COLORS = {
    "blue": "#1B4F8A",
    "green": "#2ECC71",
    "red": "#E74C3C",
    "orange": "#F39C12",
    "purple": "#9B59B6",
    "gray": "#95A5A6",
    "teal": "#1ABC9C",
}


def save(fig, name):
    path = f"visuals/{name}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def plot_admissions_by_diagnosis(admissions_df):
    """Bar chart — admissions by diagnosis."""
    diag_counts = admissions_df["diagnosis"].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(13, 6))
    bars = ax.barh(diag_counts.index, diag_counts.values,
                   color=COLORS["blue"], alpha=0.85)
    for bar, val in zip(bars, diag_counts.values):
        ax.text(val + 1, bar.get_y() + bar.get_height() / 2,
                str(val), va="center", fontsize=9, fontweight="bold")
    ax.set_title("Top 10 Diagnoses by Admission Count",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Number of Admissions")
    return save(fig, "01_admissions_by_diagnosis")


def plot_length_of_stay(admissions_df):
    """Box plot — length of stay by department."""
    fig, ax = plt.subplots(figsize=(13, 7))
    dept_order = admissions_df.groupby("department")[
        "length_of_stay"].median().sort_values(ascending=False).index
    sns.boxplot(data=admissions_df, x="department",
                y="length_of_stay", order=dept_order,
                hue="department", palette="Blues", ax=ax, legend=False)
    ax.set_title("Length of Stay by Department",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Department")
    ax.set_ylabel("Days")
    plt.xticks(rotation=30, ha="right")
    return save(fig, "02_length_of_stay")


def plot_readmission_rates(admissions_df):
    """Bar chart — readmission rate by department."""
    dept_readmit = admissions_df.groupby("department")[
        "is_readmission"].mean().sort_values(ascending=False) * 100
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = [COLORS["red"] if r > 20 else COLORS["orange"]
              if r > 15 else COLORS["green"]
              for r in dept_readmit.values]
    bars = ax.bar(dept_readmit.index, dept_readmit.values,
                  color=colors, alpha=0.85)
    ax.axhline(y=15, color=COLORS["gray"], linestyle="--",
               linewidth=2, label="Target <15%")
    ax.set_title("Readmission Rate by Department (%)",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_ylabel("Readmission Rate (%)")
    plt.xticks(rotation=30, ha="right")
    ax.legend()
    return save(fig, "03_readmission_rates")


def plot_cost_by_insurance(admissions_df):
    """Bar chart — average cost by insurance type."""
    cost_by_ins = admissions_df.groupby("insurance")[
        "total_cost"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(cost_by_ins.index, cost_by_ins.values,
                  color=COLORS["teal"], alpha=0.85)
    for bar, val in zip(bars, cost_by_ins.values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 200,
                f"${val:,.0f}", ha="center",
                fontsize=9, fontweight="bold")
    ax.set_title("Average Admission Cost by Insurance Type",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_ylabel("Average Cost ($)")
    return save(fig, "04_cost_by_insurance")


def plot_patient_outcomes(admissions_df):
    """Pie chart — patient outcome distribution."""
    outcomes = admissions_df["outcome"].value_counts()
    colors = [COLORS["green"], COLORS["blue"],
              COLORS["orange"], COLORS["red"]]
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.pie(outcomes.values, labels=outcomes.index,
           colors=colors[:len(outcomes)],
           autopct="%1.1f%%", startangle=90,
           wedgeprops={"edgecolor": "white", "linewidth": 2})
    ax.set_title("Patient Outcome Distribution",
                 fontsize=14, fontweight="bold", pad=20)
    return save(fig, "05_patient_outcomes")


def plot_age_vs_cost(admissions_df, patients_df):
    """Scatter — patient age vs admission cost."""
    merged = admissions_df.merge(patients_df, on="patient_id")
    fig, ax = plt.subplots(figsize=(12, 7))
    scatter = ax.scatter(merged["age"], merged["total_cost"],
                         c=merged["length_of_stay"],
                         cmap="Blues", alpha=0.5, s=30)
    plt.colorbar(scatter, label="Length of Stay (days)")
    z = np.polyfit(merged["age"], merged["total_cost"], 1)
    p = np.poly1d(z)
    x_line = np.linspace(merged["age"].min(), merged["age"].max(), 100)
    ax.plot(x_line, p(x_line), "--", color=COLORS["red"],
            linewidth=2, label="Trend line")
    ax.set_title("Patient Age vs Admission Cost",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Patient Age")
    ax.set_ylabel("Total Cost ($)")
    ax.legend()
    return save(fig, "06_age_vs_cost")


def plot_medication_errors(medications_df):
    """Bar chart — medication error rates."""
    error_rates = medications_df.groupby("medication")[
        "is_error"].mean().sort_values(ascending=False) * 100
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = [COLORS["red"] if r > 5 else COLORS["orange"]
              if r > 3 else COLORS["green"]
              for r in error_rates.values]
    ax.bar(error_rates.index, error_rates.values,
           color=colors, alpha=0.85)
    ax.axhline(y=3, color=COLORS["gray"], linestyle="--",
               linewidth=2, label="Acceptable threshold 3%")
    ax.set_title("Medication Error Rate by Drug",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_ylabel("Error Rate (%)")
    plt.xticks(rotation=30, ha="right")
    ax.legend()
    return save(fig, "07_medication_errors")


def plot_satisfaction_by_dept(admissions_df):
    """Horizontal bar — patient satisfaction by department."""
    satisfaction = admissions_df.groupby("department")[
        "patient_satisfaction"].mean().sort_values()
    fig, ax = plt.subplots(figsize=(11, 7))
    colors = [COLORS["green"] if s >= 3.5 else COLORS["orange"]
              if s >= 2.5 else COLORS["red"]
              for s in satisfaction.values]
    bars = ax.barh(satisfaction.index, satisfaction.values,
                   color=colors, alpha=0.85)
    ax.axvline(x=3.5, color=COLORS["gray"], linestyle="--",
               linewidth=2, label="Target 3.5/5.0")
    for bar, val in zip(bars, satisfaction.values):
        ax.text(val + 0.02, bar.get_y() + bar.get_height() / 2,
                f"{val:.2f}", va="center", fontsize=9,
                fontweight="bold")
    ax.set_title("Patient Satisfaction Score by Department",
                 fontsize=14, fontweight="bold", pad=15)
    ax.set_xlabel("Satisfaction Score (1-5)")
    ax.legend()
    return save(fig, "08_satisfaction_by_dept")
