
import pytest

from hospital_triage_priority import (
    process_triage_wards,
    monitor_oxygen_manifolds
)


def test_invalid_input():
    with pytest.raises(ValueError):
        process_triage_wards("invalid", 10)

    with pytest.raises(ValueError):
        process_triage_wards([], -1)


def test_non_accepting_ward_and_default_values():
    wards = [
        {"is_accepting": False, "patients": [{"spo2": 50}]},
        {"is_accepting": True},
        {
            "is_accepting": True,
            "patients": [{}]
        }
    ]

    result = process_triage_wards(wards, 10)

    assert result == {
        "acuity_score": 10,
        "status": "TRIAGE_STABLE"
    }


def test_invalid_patient_vitals():
    wards = [
        {
            "is_accepting": True,
            "patients": [
                {"spo2": 0, "hr": 80},
                {"spo2": 95, "hr": 0}
            ]
        }
    ]

    result = process_triage_wards(wards, 10)

    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_unconscious_patient_in_outpatient_ward():
    wards = [
        {
            "is_accepting": True,
            "tier": "outpatient",
            "patients": [
                {"spo2": 98, "hr": 75},
                {"spo2": 98, "hr": 75, "unconscious": True},
                {"spo2": 80, "hr": 130}
            ]
        }
    ]

    result = process_triage_wards(wards, 10)

    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_unconscious_patient_in_general_ward():
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "patients": [
                {"spo2": 98, "hr": 75, "unconscious": True}
            ]
        }
    ]

    result = process_triage_wards(wards, 10)

    assert result["acuity_score"] == 100
    assert result["status"] == "TRIAGE_STABLE"


def test_abnormal_oxygen_and_heart_rate():
    wards = [
        {
            "is_accepting": True,
            "patients": [
                {"spo2": 89, "hr": 80},
                {"spo2": 98, "hr": 121}
            ]
        }
    ]

    result = process_triage_wards(wards, 10)

    assert result["acuity_score"] == 120
    assert result["status"] == "TRIAGE_STABLE"


def test_icu_standby_adds_acuity():
    wards = [
        {
            "is_accepting": True,
            "icu_standby": True,
            "patients": [{"spo2": 98, "hr": 75}]
        }
    ]

    result = process_triage_wards(wards, 10)

    assert result["acuity_score"] == 35
    assert result["status"] == "TRIAGE_STABLE"


def test_ward_alert_after_more_than_four_flagged_entries():
    wards = [
        {
            "is_accepting": True,
            "patients": [
                {"spo2": 0, "hr": 75},
                {"spo2": 0, "hr": 75},
                {"spo2": 0, "hr": 75},
                {"spo2": 0, "hr": 75},
                {"spo2": 0, "hr": 75}
            ]
        }
    ]

    result = process_triage_wards(wards, 10)

    assert result["acuity_score"] == 0
    assert result["status"] == "WARD_ALERT"


def test_monitor_oxygen_no_data():
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_monitor_oxygen_pressure_failure():
    sensor_streams = [
        [5.0, 3.5, 3.0]
    ]

    assert monitor_oxygen_manifolds(sensor_streams) == "PRESSURE_FAILURE"


def test_monitor_oxygen_pressure_normal():
    sensor_streams = [
        [5.0, 3.5, 4.5, 3.8],
        [5.0, 5.0]
    ]

    assert monitor_oxygen_manifolds(sensor_streams) == "PRESSURE_NORMAL"
