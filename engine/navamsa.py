
# ASTRA AI - NAVAMSA CALCULATION ENGINE

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

SIGN_SIZE = 30.0
NAVAMSA_SIZE = 30.0 / 9.0


def calculate_navamsa_position(longitude):
    """
    Calculate the D9 Navamsa position from
    a sidereal zodiac longitude.

    Movable signs: start from the same sign.
    Fixed signs: start from the 9th sign.
    Dual signs: start from the 5th sign.
    """

    longitude = longitude % 360

    # Identify original zodiac sign
    sign_index = int(longitude // SIGN_SIZE)

    # Position within the original sign
    degree_in_sign = longitude % SIGN_SIZE

    # Identify Navamsa division (1 to 9)
    navamsa_number = int(
        degree_in_sign / NAVAMSA_SIZE
    ) + 1

    # Starting sign based on sign modality
    if sign_index % 3 == 0:
        # Movable sign
        starting_sign_index = sign_index

    elif sign_index % 3 == 1:
        # Fixed sign: 9th from itself
        starting_sign_index = (sign_index + 8) % 12

    else:
        # Dual sign: 5th from itself
        starting_sign_index = (sign_index + 4) % 12

    # Determine Navamsa zodiac sign
    navamsa_sign_index = (
        starting_sign_index + navamsa_number - 1
    ) % 12

    # Convert position within Navamsa into D9 degree
    position_in_navamsa = (
        degree_in_sign
        - (navamsa_number - 1) * NAVAMSA_SIZE
    )

    navamsa_degree = position_in_navamsa * 9

    navamsa_longitude = (
        navamsa_sign_index * SIGN_SIZE
        + navamsa_degree
    )

    return {
        "original_sign": SIGNS[sign_index],
        "navamsa_number": navamsa_number,
        "sign": SIGNS[navamsa_sign_index],
        "degree": navamsa_degree,
        "longitude": navamsa_longitude
    }
