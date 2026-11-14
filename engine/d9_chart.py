
from engine.navamsa import calculate_navamsa_position

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]


def generate_d9_chart(planets, ascendant):
    """
    Generate the Vedic D9 Navamsa chart.

    Planet positions are calculated from their
    original sidereal longitudes.
    """

    # Calculate D9 Ascendant
    d9_ascendant = calculate_navamsa_position(
        ascendant["longitude"]
    )

    d9_lagna_index = SIGNS.index(
        d9_ascendant["sign"]
    )

    # Create 12 Whole Sign houses
    houses = {}

    for house_number in range(1, 13):

        sign_index = (
            d9_lagna_index + house_number - 1
        ) % 12

        houses[house_number] = {
            "sign": SIGNS[sign_index],
            "planets": []
        }

    # Calculate D9 positions for all planets
    d9_planets = {}

    for planet_name, planet_data in planets.items():

        navamsa = calculate_navamsa_position(
            planet_data["longitude"]
        )

        d9_planets[planet_name] = navamsa

        planet_sign_index = SIGNS.index(
            navamsa["sign"]
        )

        house_number = (
            (planet_sign_index - d9_lagna_index) % 12
        ) + 1

        houses[house_number]["planets"].append({
            "name": planet_name,
            "sign": navamsa["sign"],
            "degree": navamsa["degree"],
            "longitude": navamsa["longitude"],
            "retrograde": planet_data["retrograde"]
        })

    return {
        "chart_type": "D9 Navamsa Chart",
        "house_system": "Whole Sign",
        "ascendant": d9_ascendant,
        "houses": houses,
        "planet_positions": d9_planets
    }
