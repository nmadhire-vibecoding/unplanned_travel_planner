import pytest
from unplanned_travel_planner import main


def test_compute_num_days_basic():
    assert main._compute_num_days('2025-01-01', '2025-01-05') == 4


def test_compute_num_days_same_day():
    assert main._compute_num_days('2025-01-01', '2025-01-01') == 1


def test_compute_num_days_invalid_order():
    with pytest.raises(ValueError):
        main._compute_num_days('2025-01-05', '2025-01-01')


def test_build_inputs_overrides_and_num_days():
    inputs = main._build_inputs({'departure_date': '2025-02-01', 'return_date': '2025-02-04', 'party_size': 5, 'total_budget_usd': 4200})
    assert inputs['num_days'] == 3
    assert inputs['party_size'] == 5
    assert inputs['departure_date'] == '2025-02-01'
    assert inputs['total_budget_usd'] == 4200


def test_build_inputs_invalid_date_format():
    with pytest.raises(ValueError):
        main._compute_num_days('2025/02/01', '2025-02-04')
