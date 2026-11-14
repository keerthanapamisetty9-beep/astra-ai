# Natural planetary relationships based on
# classical Parashari Naisargika Maitri.

NATURAL_RELATIONSHIPS = {
    "Sun": {
        "friends": ["Moon", "Mars", "Jupiter"],
        "enemies": ["Venus", "Saturn"],
        "neutral": ["Mercury"],
    },
    "Moon": {
        "friends": ["Sun", "Mercury"],
        "enemies": [],
        "neutral": ["Mars", "Jupiter", "Venus", "Saturn"],
    },
    "Mars": {
        "friends": ["Sun", "Moon", "Jupiter"],
        "enemies": ["Mercury"],
        "neutral": ["Venus", "Saturn"],
    },
    "Mercury": {
        "friends": ["Sun", "Venus"],
        "enemies": ["Moon"],
        "neutral": ["Mars", "Jupiter", "Saturn"],
    },
    "Jupiter": {
        "friends": ["Sun", "Moon", "Mars"],
        "enemies": ["Mercury", "Venus"],
        "neutral": ["Saturn"],
    },
    "Venus": {
        "friends": ["Mercury", "Saturn"],
        "enemies": ["Sun", "Moon"],
        "neutral": ["Mars", "Jupiter"],
    },
    "Saturn": {
        "friends": ["Mercury", "Venus"],
        "enemies": ["Sun", "Moon", "Mars"],
        "neutral": ["Jupiter"],
    },
}


CLASSICAL_PLANETS = list(NATURAL_RELATIONSHIPS.keys())


def get_natural_relationship(planet, other_planet):
    """
    Return the natural relationship between two classical planets.
    """

    if planet not in NATURAL_RELATIONSHIPS:
        raise ValueError(f"Unsupported planet: {planet}")

    if other_planet not in NATURAL_RELATIONSHIPS:
        raise ValueError(f"Unsupported planet: {other_planet}")

    if planet == other_planet:
        return "Same planet"

    relationships = NATURAL_RELATIONSHIPS[planet]

    if other_planet in relationships["friends"]:
        return "Friend"

    if other_planet in relationships["enemies"]:
        return "Enemy"

    if other_planet in relationships["neutral"]:
        return "Neutral"

    raise ValueError(
        f"Relationship not defined between {planet} and {other_planet}"
    )


def get_all_natural_relationships(planet):
    """
    Return all natural relationships for a given planet.
    """

    if planet not in NATURAL_RELATIONSHIPS:
        raise ValueError(f"Unsupported planet: {planet}")

    return {
        "planet": planet,
        "friends": NATURAL_RELATIONSHIPS[planet]["friends"].copy(),
        "enemies": NATURAL_RELATIONSHIPS[planet]["enemies"].copy(),
        "neutral": NATURAL_RELATIONSHIPS[planet]["neutral"].copy(),
    }
