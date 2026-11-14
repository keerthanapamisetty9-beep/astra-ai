"""
Planetary combustion (Asta) calculations.

Uses sidereal planetary longitudes and configurable
traditional combustion thresholds.
"""

COMBUSTION_LIMITS = {
    "Moon": {"direct": 12.0, "retrograde": 12.0},
    "Mars": {"direct": 17.0, "retrograde": 17.0},
    "Mercury": {"direct": 14.0, "retrograde": 12.0},
    "Jupiter": {"direct": 11.0, "retrograde": 11.0},
    "Venus": {"direct": 10.0, "retrograde": 8.0},
    "Saturn": {"direct": 15.0, "retrograde": 15.0},
}


def get_sun_distance(sun_longitude, planet_longitude):
    """Calculate the shortest angular distance from the Sun."""

    for longitude in (sun_longitude, planet_longitude):
        if (
            isinstance(longitude, bool)
            or not isinstance(longitude, (int, float))
            or not 0 <= longitude < 360
        ):
            raise ValueError("Longitude must be between 0 and 360.")

    difference = abs(sun_longitude - planet_longitude)

    return min(difference, 360 - difference)


def get_planetary_combustion(planet, sun_longitude,
                             planet_longitude, retrograde=False):
    """Determine whether a planet is combust."""

    if planet not in COMBUSTION_LIMITS:
        raise ValueError(f"Unsupported planet for combustion: {planet}")

    if not isinstance(retrograde, bool):
        raise ValueError("Retrograde must be True or False.")

    distance = get_sun_distance(sun_longitude, planet_longitude)

    motion = "retrograde" if retrograde else "direct"
    limit = COMBUSTION_LIMITS[planet][motion]

    return {
        "planet": planet,
        "sun_distance": distance,
        "combustion_limit": limit,
        "retrograde": retrograde,
        "is_combust": distance <= limit,
    }


def get_chart_combustion(planets):
    """Calculate combustion status for all supported planets in a chart."""

    if not isinstance(planets, dict) or "Sun" not in planets:
        raise ValueError("Planetary data must contain the Sun.")

    sun_longitude = planets["Sun"].get("longitude")

    results = {}

    for planet, limits in COMBUSTION_LIMITS.items():
        if planet not in planets:
            raise ValueError(f"{planet} is missing from planetary data.")

        planet_data = planets[planet]

        results[planet] = get_planetary_combustion(
            planet=planet,
            sun_longitude=sun_longitude,
            planet_longitude=planet_data.get("longitude"),
            retrograde=planet_data.get("retrograde", False),
        )

    return results
