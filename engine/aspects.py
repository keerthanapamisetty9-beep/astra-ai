# Classical Parashari Graha Drishti rules.

PLANET_ASPECTS = {
    "Sun": [7],
    "Moon": [7],
    "Mars": [4, 7, 8],
    "Mercury": [7],
    "Jupiter": [5, 7, 9],
    "Venus": [7],
    "Saturn": [3, 7, 10],
}


def get_aspected_houses(planet_house, planet):
    """
    Return the houses aspected by a planet in a whole-sign D1 chart.
    House positions are counted inclusively from the planet's house.
    """

    if planet not in PLANET_ASPECTS:
        raise ValueError(f"Unsupported planet: {planet}")

    if (
        isinstance(planet_house, bool)
        or not isinstance(planet_house, int)
        or not 1 <= planet_house <= 12
    ):
        raise ValueError("Planet house must be an integer from 1 to 12.")

    return [
        ((planet_house + aspect - 2) % 12) + 1
        for aspect in PLANET_ASPECTS[planet]
    ]


def get_chart_aspects(chart):
    """
    Calculate house and planet-to-planet aspects in a D1 chart.

    Only the seven classical planets are included.
    """

    if not isinstance(chart, dict) or "houses" not in chart:
        raise ValueError("Invalid D1 chart structure.")

    houses = chart["houses"]
    planet_houses = {}

    for house_number, house_data in houses.items():
        if (
            isinstance(house_number, bool)
            or not isinstance(house_number, int)
            or not 1 <= house_number <= 12
        ):
            raise ValueError("Invalid house number in chart.")

        if not isinstance(house_data, dict):
            raise ValueError("Invalid house data.")

        for planet_data in house_data.get("planets", []):
            planet = planet_data["name"]

            if planet not in PLANET_ASPECTS:
                continue

            if planet in planet_houses:
                raise ValueError(f"{planet} appears more than once in chart.")

            planet_houses[planet] = house_number

    results = {}

    for planet, house in planet_houses.items():
        aspected_houses = get_aspected_houses(house, planet)

        aspected_planets = {}

        for other_planet, other_house in planet_houses.items():
            if other_planet == planet:
                continue

            if other_house in aspected_houses:
                aspected_planets[other_planet] = other_house

        results[planet] = {
            "planet_house": house,
            "aspected_houses": aspected_houses,
            "aspected_planets": aspected_planets,
        }

    return results
