
# ASTRA AI - GOCHAR / TRANSIT ENGINE

from engine.planetary_positions import calculate_planets


def calculate_transits(julian_day):
    """
    Calculate planetary positions for a selected date.
    """

    transit_planets = calculate_planets(julian_day)

    return {
        "chart_type": "Gochar Transit Chart",
        "zodiac_system": "Sidereal",
        "ayanamsa": "Lahiri",
        "planets": transit_planets
    }


SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]


def calculate_transit_houses(
    transit_planets,
    natal_moon_sign,
    natal_ascendant_sign
):
    """
    Calculate transit houses from natal Moon
    and natal Ascendant using Whole Sign houses.
    """

    moon_index = SIGNS.index(natal_moon_sign)
    ascendant_index = SIGNS.index(natal_ascendant_sign)

    results = {}

    for planet_name, data in transit_planets.items():

        transit_index = SIGNS.index(data["sign"])

        house_from_moon = (
            (transit_index - moon_index) % 12
        ) + 1

        house_from_lagna = (
            (transit_index - ascendant_index) % 12
        ) + 1

        results[planet_name] = {
            "sign": data["sign"],
            "degree": data["degree"],
            "house_from_moon": house_from_moon,
            "house_from_lagna": house_from_lagna
        }

    return results
