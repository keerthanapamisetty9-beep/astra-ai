from engine.planetary_relationships import get_natural_relationship
from engine.temporary_relationships import get_temporary_relationship


COMPOUND_RELATIONSHIPS = {
    ("Friend", "Friend"): "Great Friend",
    ("Friend", "Enemy"): "Neutral",
    ("Neutral", "Friend"): "Friend",
    ("Neutral", "Enemy"): "Enemy",
    ("Enemy", "Friend"): "Neutral",
    ("Enemy", "Enemy"): "Great Enemy",
}


CLASSICAL_PLANETS = [
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
]


def get_panchadha_relationship(
    planet,
    other_planet,
    planet_house,
    other_planet_house,
):
    """Calculate the five-fold relationship between two classical planets."""

    if planet not in CLASSICAL_PLANETS:
        raise ValueError(f"Unsupported classical planet: {planet}")

    if other_planet not in CLASSICAL_PLANETS:
        raise ValueError(f"Unsupported classical planet: {other_planet}")

    if planet == other_planet:
        raise ValueError("A planet cannot have a relationship with itself.")

    natural = get_natural_relationship(planet, other_planet)

    temporary = get_temporary_relationship(
        planet_house,
        other_planet_house,
    )

    compound = COMPOUND_RELATIONSHIPS[(natural, temporary)]

    return {
        "planet": planet,
        "other_planet": other_planet,
        "natural_relationship": natural,
        "temporary_relationship": temporary,
        "panchadha_relationship": compound,
    }


def get_chart_panchadha_relationships(chart):
    """
    Calculate Panchadha Maitri for all seven classical planets in a D1 chart.

    Rahu and Ketu are excluded.
    """

    if not isinstance(chart, dict) or "houses" not in chart:
        raise ValueError("Invalid D1 chart structure.")

    planet_houses = {}

    for house_number, house_data in chart["houses"].items():
        if not isinstance(house_data, dict):
            raise ValueError("Invalid house data.")

        for planet_data in house_data.get("planets", []):
            planet = planet_data["name"]

            if planet not in CLASSICAL_PLANETS:
                continue

            if planet in planet_houses:
                raise ValueError(f"{planet} appears more than once in chart.")

            planet_houses[planet] = house_number

    results = {}

    for planet, house in planet_houses.items():
        results[planet] = {}

        for other_planet, other_house in planet_houses.items():
            if planet == other_planet:
                continue

            results[planet][other_planet] = get_panchadha_relationship(
                planet,
                other_planet,
                house,
                other_house,
            )

    return results
