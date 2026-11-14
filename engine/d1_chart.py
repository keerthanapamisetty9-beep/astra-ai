
SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]


def calculate_d1_chart(planets, ascendant):
    """
    Build a D1 Rashi chart using Whole Sign Houses.

    planets: Output from calculate_planets()
    ascendant: Output from calculate_ascendant()
    """

    lagna_sign = ascendant["sign"]
    lagna_index = SIGNS.index(lagna_sign)

    houses = {}

    # Create all 12 houses
    for house_number in range(1, 13):
        sign_index = (lagna_index + house_number - 1) % 12

        houses[house_number] = {
            "sign": SIGNS[sign_index],
            "planets": []
        }

    # Assign planets to houses based on their zodiac signs
    for planet_name, planet_data in planets.items():
        planet_sign = planet_data["sign"]
        planet_sign_index = SIGNS.index(planet_sign)

        house_number = (
            (planet_sign_index - lagna_index) % 12
        ) + 1

        houses[house_number]["planets"].append({
            "name": planet_name,
            "degree": planet_data["degree"],
            "retrograde": planet_data["retrograde"]
        })

    return {
        "chart_type": "D1 Rashi Chart",
        "house_system": "Whole Sign",
        "ascendant": lagna_sign,
        "ascendant_degree": ascendant["degree"],
        "houses": houses
    }
