# Traditional Parashari sign rulers.

SIGN_LORDS = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter",
}


def get_sign_lord(sign):
    """Return the traditional planetary ruler of a zodiac sign."""

    if sign not in SIGN_LORDS:
        raise ValueError(f"Unsupported zodiac sign: {sign}")

    return SIGN_LORDS[sign]


def get_house_lords(chart):
    """Identify the ruling planet of each house in a whole-sign D1 chart."""

    if not isinstance(chart, dict) or "houses" not in chart:
        raise ValueError("Invalid D1 chart structure.")

    houses = chart["houses"]
    results = {}

    for house_number in range(1, 13):
        if house_number not in houses:
            raise ValueError(f"House {house_number} is missing from chart.")

        house_data = houses[house_number]

        if not isinstance(house_data, dict):
            raise ValueError("Invalid house data.")

        sign = house_data.get("sign")
        lord = get_sign_lord(sign)

        results[house_number] = {
            "house": house_number,
            "sign": sign,
            "lord": lord,
        }

    return results


def get_house_lord_placements(chart):
    """
    Identify each house lord and the house occupied by that lord.

    Uses the planetary placements already present in the D1 chart.
    """

    if not isinstance(chart, dict) or "houses" not in chart:
        raise ValueError("Invalid D1 chart structure.")

    house_lords = get_house_lords(chart)

    planet_houses = {}

    for house_number, house_data in chart["houses"].items():
        if not isinstance(house_data, dict):
            raise ValueError("Invalid house data.")

        for planet_data in house_data.get("planets", []):
            planet = planet_data["name"]

            if planet in planet_houses:
                raise ValueError(f"{planet} appears more than once in chart.")

            planet_houses[planet] = house_number

    results = {}

    for house_number, details in house_lords.items():
        lord = details["lord"]

        results[house_number] = {
            "house": house_number,
            "sign": details["sign"],
            "lord": lord,
            "lord_placed_in_house": planet_houses.get(lord),
        }

    return results
