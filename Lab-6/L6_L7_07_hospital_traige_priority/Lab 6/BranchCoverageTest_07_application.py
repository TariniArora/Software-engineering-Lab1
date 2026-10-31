
from hospital_triage_priority import (
    process_triage_wards,
    monitor_oxygen_manifolds
)


def test_ward_accepting_and_not_accepting():
    assert process_triage_wards(
        [{"is_accepting": False}],
        10
    )["status"] == "NO_URGENT_CASES"


def test_patient_vitals_or_condition_branches():
    wards = [
        {
            "is_accepting": True,
            "patients": [
                {"spo2": 0, "hr": 80},
                {"spo2": 95, "hr": 0},
                {"spo2": 89, "hr": 80},
                {"spo2": 98, "hr": 121},
                {"spo2": 98, "hr": 80, "unconscious": True}
            ]
        }
    ]

    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 220


def test_outpatient_unconscious_branch():
    wards = [
        {
            "is_accepting": True,
            "tier": "outpatient",
            "patients": [
                {"spo2": 98, "hr": 70, "unconscious": True}
            ]
        }
    ]

    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0


def test_icu_standby_branches():
    wards = [
        {"is_accepting": True, "icu_standby": False},
        {"is_accepting": True, "icu_standby": True}
    ]

    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 25


def test_ward_alert_and_stable_branches():
    wards = [
        {
            "is_accepting": True,
            "patients": [
                {"spo2": 0, "hr": 80},
                {"spo2": 0, "hr": 80},
                {"spo2": 0, "hr": 80},
                {"spo2": 0, "hr": 80},
                {"spo2": 0, "hr": 80}
            ]
        }
    ]

    assert process_triage_wards(wards, 10)["status"] == "WARD_ALERT"
    assert process_triage_wards([], 10)["status"] == "NO_URGENT_CASES"


def test_oxygen_no_data_and_normal_branches():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"
    assert monitor_oxygen_manifolds([[5.0, 3.0, 5.0]]) == "PRESSURE_NORMAL"


def test_oxygen_pressure_failure_branch():
    assert monitor_oxygen_manifolds([[3.0, 3.5]]) == "PRESSURE_FAILURE"
