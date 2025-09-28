#!/usr/bin/env python
import sys
import warnings
from datetime import datetime, date
from typing import Dict, Any

from unplanned_travel_planner.crew import UnplannedTravelPlanner

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def _compute_num_days(start: str, end: str) -> int:
    try:
        start_d = datetime.strptime(start, "%Y-%m-%d").date()
        end_d = datetime.strptime(end, "%Y-%m-%d").date()
    except ValueError as ve:
        raise ValueError(f"Dates must be in YYYY-MM-DD format: {ve}")
    if end_d < start_d:
        raise ValueError("return_date must be on or after departure_date")
    # Include arrival day; itinerary length is difference in days
    return (end_d - start_d).days or 1


def _build_inputs(overrides: Dict[str, Any] | None = None) -> Dict[str, Any]:
    base = {
        'origin': 'SFO',
        'destination': 'Tokyo',
        'departure_date': '2025-11-10',
        'return_date': '2025-11-20',
        'party_size': 3,
        'currency': 'USD',
        'lodging_style': 'boutique + convenient transit',
        'budget_tier': 'mid',
        'interests': 'culture, food, tech, hidden neighborhoods',
        'total_budget_usd': 6000
    }
    if overrides:
        base.update({k: v for k, v in overrides.items() if v is not None})
    base['num_days'] = _compute_num_days(base['departure_date'], base['return_date'])
    return base


def _prompt(question: str, default: str | None = None, validator=None):
    prompt_text = f"{question}" + (f" [{default}]" if default is not None else "") + ": "
    while True:
        val = input(prompt_text).strip()
        if not val and default is not None:
            val = default
        if validator:
            try:
                validator(val)
            except Exception as e:
                print(f"Invalid value: {e}")
                continue
        if val:
            return val
        print("A value is required.")


def _validate_date(ds: str):
    datetime.strptime(ds, "%Y-%m-%d")  # raises if invalid


def _validate_positive_int(v: str):
    if int(v) < 1:
        raise ValueError("Must be >= 1")


def _validate_positive_float(v: str):
    if float(v) <= 0:
        raise ValueError("Must be > 0")


def gather_inputs_interactive() -> Dict[str, Any]:
    """Interactively prompt user for trip parameters."""
    origin = _prompt("Origin airport code (IATA)", "SFO")
    destination = _prompt("Destination city or airport code", "Tokyo")
    departure_date = _prompt("Departure date YYYY-MM-DD", "2025-11-10", _validate_date)
    return_date = _prompt("Return date YYYY-MM-DD", "2025-11-20", _validate_date)
    party_size = int(_prompt("Party size (number of travelers)", "2", _validate_positive_int))
    currency = _prompt("Currency code", "USD")
    lodging_style = _prompt("Preferred lodging style", "boutique + convenient transit")
    budget_tier = _prompt("Budget tier (low/mid/premium)", "mid")
    interests = _prompt("Interests (comma separated)", "culture, food, tech, hidden neighborhoods")
    total_budget_usd = float(_prompt("Total trip budget in USD (overall, not per person)", "6000", _validate_positive_float))

    overrides = {
        'origin': origin,
        'destination': destination,
        'departure_date': departure_date,
        'return_date': return_date,
        'party_size': party_size,
        'currency': currency,
        'lodging_style': lodging_style,
        'budget_tier': budget_tier,
        'interests': interests,
        'total_budget_usd': total_budget_usd
    }
    inputs = _build_inputs(overrides)
    return inputs


def run():
    """Run the crew with optional CLI args.

    Usage:
        python -m unplanned_travel_planner.main run SFO Tokyo 2025-11-10 2025-11-20 2
    (Only origin destination depart return party_size are positional optional overrides.)
    """
    use_cli = len(sys.argv) >= 7 and sys.argv[1] == 'run'
    if use_cli:
        try:
            overrides = {
                'origin': sys.argv[2],
                'destination': sys.argv[3],
                'departure_date': sys.argv[4],
                'return_date': sys.argv[5],
                'party_size': int(sys.argv[6])
            }
            if len(sys.argv) >= 8:
                overrides['total_budget_usd'] = float(sys.argv[7])
        except (IndexError, ValueError):
            raise ValueError("Invalid CLI arguments for run. Expected: run ORIGIN DESTINATION DEPART_DATE RETURN_DATE PARTY_SIZE [TOTAL_BUDGET_USD]")
        inputs = _build_inputs(overrides)
    else:
        print("\nInteractive Travel Planner Setup (press Enter to accept defaults)\n")
        inputs = gather_inputs_interactive()

    try:
        UnplannedTravelPlanner().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """Train the crew for a given number of iterations.

    Usage:
        python -m unplanned_travel_planner.main train <iterations> <outfile>
    """
    # Training typically uses deterministic inputs; allow optional interactive flag
    if len(sys.argv) > 3 and sys.argv[-1] == '--interactive':
        inputs = gather_inputs_interactive()
    else:
        inputs = _build_inputs()
    try:
        UnplannedTravelPlanner().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        UnplannedTravelPlanner().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """Test the crew execution and returns the results.

    Usage:
        python -m unplanned_travel_planner.main test <iterations> <eval_llm>
    """
    if len(sys.argv) > 3 and sys.argv[-1] == '--interactive':
        inputs = gather_inputs_interactive()
    else:
        inputs = _build_inputs()
    try:
        UnplannedTravelPlanner().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
