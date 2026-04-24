import pandas as pd
from src.metrics import (
    attrition_rate,
    attrition_by_department,
    attrition_by_overtime,
    average_income_by_attrition,
    satisfaction_summary,
)


# ---------------------------------------------------------------------------
# attrition_rate
# ---------------------------------------------------------------------------

def test_attrition_rate_returns_expected_percent():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "department": ["Sales", "Sales", "HR", "HR"],
            "attrition": ["Yes", "No", "No", "Yes"],
        }
    )
    assert attrition_rate(df) == 50.0


# ---------------------------------------------------------------------------
# attrition_by_department
# ---------------------------------------------------------------------------

def test_attrition_by_department_returns_expected_columns():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "department": ["Sales", "Sales", "HR", "HR"],
            "attrition": ["Yes", "No", "No", "Yes"],
        }
    )
    result = attrition_by_department(df)
    assert list(result.columns) == ["department", "employees", "leavers", "attrition_rate"]


def test_attrition_by_department_correct_rates():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4, 5, 6],
            "department": ["Sales", "Sales", "HR", "HR", "HR", "HR"],
            "attrition": ["Yes", "No", "Yes", "No", "No", "No"],
        }
    )
    result = attrition_by_department(df)
    sales = result[result["department"] == "Sales"].iloc[0]
    hr = result[result["department"] == "HR"].iloc[0]
    assert sales["attrition_rate"] == 50.0   # 1 leaver / 2 employees
    assert hr["attrition_rate"] == 25.0      # 1 leaver / 4 employees


def test_attrition_by_department_sorted_descending_by_rate():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4, 5, 6],
            "department": ["Sales", "Sales", "HR", "HR", "HR", "HR"],
            "attrition": ["Yes", "No", "Yes", "No", "No", "No"],
        }
    )
    result = attrition_by_department(df)
    # Sales (50%) should appear before HR (25%)
    assert result.iloc[0]["department"] == "Sales"
    assert result.iloc[1]["department"] == "HR"


# ---------------------------------------------------------------------------
# attrition_by_overtime
# ---------------------------------------------------------------------------

def test_attrition_by_overtime_correct_rates():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4, 5],
            "overtime": ["Yes", "Yes", "No", "No", "No"],
            "attrition": ["Yes", "No", "Yes", "No", "No"],
        }
    )
    result = attrition_by_overtime(df)
    yes_row = result[result["overtime"] == "Yes"].iloc[0]
    no_row = result[result["overtime"] == "No"].iloc[0]
    assert yes_row["attrition_rate"] == 50.0    # 1 leaver / 2 employees
    assert no_row["attrition_rate"] == 33.33    # 1 leaver / 3 employees


# ---------------------------------------------------------------------------
# average_income_by_attrition
# ---------------------------------------------------------------------------

def test_average_income_by_attrition_correct_values():
    df = pd.DataFrame(
        {
            "attrition": ["Yes", "Yes", "No", "No"],
            "monthly_income": [3000.0, 5000.0, 6000.0, 8000.0],
        }
    )
    result = average_income_by_attrition(df)
    yes_row = result[result["attrition"] == "Yes"].iloc[0]
    no_row = result[result["attrition"] == "No"].iloc[0]
    assert yes_row["avg_monthly_income"] == 4000.0   # (3000 + 5000) / 2
    assert no_row["avg_monthly_income"] == 7000.0    # (6000 + 8000) / 2


# ---------------------------------------------------------------------------
# satisfaction_summary
# ---------------------------------------------------------------------------

def test_satisfaction_summary_uses_group_headcount_as_denominator():
    # satisfaction=1: 1 leaver / 2 employees = 50%
    # satisfaction=2: 2 leavers / 4 employees = 50%
    # The old bug divided by total leavers (3), giving 33.33% and 66.67%.
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4, 5, 6],
            "job_satisfaction": [1, 1, 2, 2, 2, 2],
            "attrition": ["Yes", "No", "Yes", "Yes", "No", "No"],
        }
    )
    result = satisfaction_summary(df)
    sat1 = result[result["job_satisfaction"] == 1].iloc[0]
    sat2 = result[result["job_satisfaction"] == 2].iloc[0]
    assert sat1["attrition_rate"] == 50.0
    assert sat2["attrition_rate"] == 50.0


def test_satisfaction_summary_sorted_ascending_by_satisfaction():
    df = pd.DataFrame(
        {
            "employee_id": [1, 2, 3, 4],
            "job_satisfaction": [3, 1, 4, 2],
            "attrition": ["No", "Yes", "No", "No"],
        }
    )
    result = satisfaction_summary(df)
    assert list(result["job_satisfaction"]) == [1, 2, 3, 4]
