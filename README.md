# UnplannedTravelPlanner Crew

Welcome to the UnplannedTravelPlanner Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/unplanned_travel_planner/config/agents.yaml` to define your agents
- Modify `src/unplanned_travel_planner/config/tasks.yaml` to define your tasks
- Modify `src/unplanned_travel_planner/crew.py` to add your own logic, tools and specific args
- Modify `src/unplanned_travel_planner/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the unplanned_travel_planner Crew, assembling the agents and assigning them tasks as defined in your configuration.

This updated project now generates an `itinerary.md` file containing a multi-day travel plan synthesized from flight, lodging and sightseeing research.

## Understanding Your Crew

The unplanned_travel_planner Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Travel Planner Agents

| Agent | Purpose | Key Output |
|-------|---------|------------|
| flight_researcher | Finds 5–8 smart flight options (price vs duration vs routing) | Flight options list |
| hotel_researcher | Curates 5–7 lodging recommendations across tiers | Lodging table + analysis |
| sightseeing_researcher | Discovers attractions, food spots, experiences (clustered) | Grouped activity list |
| itinerary_planner | Synthesizes into day-by-day schedule with rationale | `itinerary.md` |

### Default Inputs
Defined in `main.py` and can be overridden when invoking programmatically:

```
origin: SFO
destination: Tokyo
departure_date: 2025-11-10
return_date: 2025-11-20
party_size: 2
total_budget_usd: 6000
currency: USD
lodging_style: boutique + convenient transit
budget_tier: mid
interests: culture, food, tech, hidden neighborhoods
num_days: 8
```

### Running with Custom Inputs
You can edit the `inputs` dict in `main.py` or adapt a small runner:

```python
from unplanned_travel_planner.crew import UnplannedTravelPlanner

inputs = {
	'origin': 'JFK',
	'destination': 'Lisbon',
	'departure_date': '2025-05-04',
	'return_date': '2025-05-12',
	'party_size': 3,
	'total_budget_usd': 7500,
	'currency': 'EUR',
	'lodging_style': 'historic + walkable',
	'budget_tier': 'mid',
	'interests': 'food, architecture, history, coastal views',
	'num_days': 7
}

UnplannedTravelPlanner().crew().kickoff(inputs=inputs)
```

### CLI Positional Override (Run Only)

You can pass minimal positional overrides when running directly:

```bash
python -m unplanned_travel_planner.main run JFK LIS 2025-05-04 2025-05-12 3
```

Format: `run ORIGIN DESTINATION DEPARTURE_DATE RETURN_DATE PARTY_SIZE`

Optionally append TOTAL_BUDGET_USD as a 7th value:

```bash
python -m unplanned_travel_planner.main run JFK LIS 2025-05-04 2025-05-12 3 7500
```

`num_days` is calculated automatically from the date range (inclusive of start day; a same-day trip yields 1).

### Interactive Mode (Default)

If you run the module without the positional override pattern (or via the script entry point), you'll be prompted for each input with sensible defaults:

```bash
python -m unplanned_travel_planner.main
# or
python -m unplanned_travel_planner.main run
```

Press Enter to accept defaults or type a new value. Dates are validated (YYYY-MM-DD). `party_size` must be >=1.
You'll also be prompted for an overall `total_budget_usd` which is used to contextualize flight, lodging and itinerary recommendations.

For `train` and `test`, you can opt into interactive prompting by appending `--interactive`:

```bash
python -m unplanned_travel_planner.main train 2 model_eval.json --interactive
python -m unplanned_travel_planner.main test 1 gpt-4o-mini --interactive
```

### Output
`itinerary.md` will be created in the project root (or current working directory when run). It contains:
1. Overview summary
2. Day-by-day schedule (Morning / Midday / Afternoon / Evening)
3. Lodging recap & transit tips
4. Optional alternatives

## Tests
Basic structural test: `tests/test_crew_setup.py` validates that four agents and four tasks are loaded.

Run (if you have pytest available):

```bash
pytest -q
```

## Next Ideas
* Add real flight search API integration
* Add hotel and activity APIs or scraping tools
* Introduce cost aggregation & budget validation
* Add weather-aware daily rearrangement
* Introduce user preference persistence in `knowledge/`

