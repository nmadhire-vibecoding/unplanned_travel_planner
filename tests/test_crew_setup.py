from unplanned_travel_planner.crew import UnplannedTravelPlanner


def test_crew_agents_and_tasks():
    crew_instance = UnplannedTravelPlanner()
    crew = crew_instance.crew()

    # Agent names created by decorators follow attribute order; we can inspect configs
    agent_roles = {a.role for a in crew.agents}
    expected_role_keywords = {
        'Flight Options Research Specialist',
        'Accommodation Scouting Analyst',
        'Local Experience Curator',
        'Integrated Trip Architect'
    }
    for keyword in expected_role_keywords:
        assert any(keyword in role for role in agent_roles), f"Missing agent role containing: {keyword}"

    task_descriptions = [t.description for t in crew.tasks]
    expected_description_snippets = [
        'Research 5-8 viable flight options',
        'Identify 5-7 lodging options',
        'Curate 10-15 activities',
        'Using the researched flights, hotels, and activities'
    ]
    for snippet in expected_description_snippets:
        assert any(snippet in d for d in task_descriptions), f"Missing task with snippet: {snippet}"
