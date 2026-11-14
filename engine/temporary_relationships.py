# Parashari Tatkalika Maitri (temporary planetary relationships).

TEMPORARY_FRIEND_POSITIONS = {2, 3, 4, 10, 11, 12}
TEMPORARY_ENEMY_POSITIONS = {1, 5, 6, 7, 8, 9}


def get_temporary_relationship(planet_house, other_planet_house):
    """
    Determine the temporary relationship between two planets.

    House positions are counted inclusively from the first planet.
    """

    for house in (planet_house, other_planet_house):
        if (
            isinstance(house, bool)
            or not isinstance(house, int)
            or not 1 <= house <= 12
        ):
            raise ValueError("House numbers must be integers from 1 to 12.")

    relative_position = (
        (other_planet_house - planet_house) % 12
    ) + 1

    if relative_position in TEMPORARY_FRIEND_POSITIONS:
        return "Friend"

    if relative_position in TEMPORARY_ENEMY_POSITIONS:
        return "Enemy"

    raise ValueError("Unable to determine temporary relationship.")


def get_chart_temporary_relationships(chart):
    """
    Calculate temporary relationships between all planets in a D1 chart.

    Uses the existing calculate_d1_chart() output structure.
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

        for planet in house_data.get("planets", []):
            planet_name = planet["name"]

            if planet_name in planet_houses:
                raise ValueError(
                    f"Planet {planet_name} appears more than once."
                )

            planet_houses[planet_name] = house_number

    results = {}

    for planet, house in planet_houses.items():
        results[planet] = {}

        for other_planet, other_house in planet_houses.items():
            if planet == other_planet:
                continue

            results[planet][other_planet] = (
                get_temporary_relationship(house, other_house)
            )

    return results
