
import swisseph as swe

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]


def calculate_ascendant(
    julian_day,
    latitude,
    longitude
):
    # Set Lahiri ayanamsa
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    # Calculate sidereal ascendant
    cusps, ascmc = swe.houses_ex(
        julian_day,
        latitude,
        longitude,
        b'P',
        swe.FLG_SIDEREAL
    )

    ascendant = ascmc[0] % 360

    sign_index = int(ascendant // 30)
    degree = ascendant % 30

    return {
        "longitude": ascendant,
        "sign": SIGNS[sign_index],
        "degree": degree
    }
