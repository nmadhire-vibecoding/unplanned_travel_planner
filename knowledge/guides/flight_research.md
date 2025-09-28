# Flight Research Guidelines

Purpose: Support `flight_researcher` agent in producing high-quality, budget-aware flight option analysis.

## Heuristics
- Balance total travel time vs. savings: flag when savings > 18% but adds > 5 hours.
- Prefer layovers >= 60 min (domestic) / 90 min (international).
- Consider nearby alternate airports (example: HND vs NRT, OAK vs SFO) if savings/time justify.
- Highlight at most 8 curated options.

## Data Points To Include Per Option
- Airline + alliance (if relevant for status/miles)
- Route (airport codes) and cabin class
- Departure/arrival times (local) + duration
- Layover location(s) + layover duration(s)
- Price (currency from inputs) and approximate price per traveler
- Notable pros/cons (e.g. "fastest", "cheapest", "best schedule", "overnight layover risk")

## Budget / Trade-Off Commentary
- Provide quick comparison table: price vs duration vs stops.
- Call out if a premium cabin splurge might still fit total budget.
- Always list a sensible baseline economy option.

## Output Structure
1. Summary paragraph of pricing landscape (range, patterns).
2. Ranked list of recommended options with bullet details.
3. Comparative insights (why top 2 stand out).
4. Edge cases / alternatives (e.g., shift date +/-1 day).
