
import swisseph as swe
import os

# Configure Swiss Ephemeris data directory
EPHE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "ephe")
)
swe.set_ephe_path(EPHE_PATH)

# Vedic astrology configuration
swe.set_sid_mode(swe.SIDM_LAHIRI)

# Planet identifiers
PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.TRUE_NODE,
}

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]


def calculate_planets(julian_day):
    results = {}

    flags = (
        swe.FLG_SWIEPH
        | swe.FLG_SIDEREAL
        | swe.FLG_SPEED
    )

    for name, planet_id in PLANETS.items():

        position, ret_flags = swe.calc_ut(
            julian_day,
            planet_id,
            flags
        )

        # Prevent silent fallback to Moshier
        if not (ret_flags & swe.FLG_SWIEPH):
            raise RuntimeError(
                f"Swiss Ephemeris data unavailable for {name}"
            )

        longitude = position[0] % 360
        speed = position[3]

        sign_index = int(longitude // 30)
        degree = longitude % 30

        results[name] = {
            "longitude": longitude,
            "sign": SIGNS[sign_index],
            "degree": degree,
            "speed": speed,
            "retrograde": speed < 0
        }

    # Ketu is always 180 degrees opposite Rahu
    rahu = results["Rahu"]

    ketu_longitude = (rahu["longitude"] + 180) % 360

    results["Ketu"] = {
        "longitude": ketu_longitude,
        "sign": SIGNS[int(ketu_longitude // 30)],
        "degree": ketu_longitude % 30,
        "speed": rahu["speed"],
        "retrograde": rahu["speed"] < 0
    }

    return results
