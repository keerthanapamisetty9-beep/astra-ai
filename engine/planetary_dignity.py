import math


# Classical Parashari planetary dignity data.
# Degrees are measured within the sidereal sign (0 to less than 30).

PLANETARY_DIGNITY = {
    "Sun": {
        "exaltation": "Aries",
        "debilitation": "Libra",
        "exaltation_degree": 10,
        "own_signs": ["Leo"],
        "moolatrikona": {
            "sign": "Leo",
            "start": 0,
            "end": 20
        }
    },

    "Moon": {
        "exaltation": "Taurus",
        "debilitation": "Scorpio",
        "exaltation_degree": 3,
        "own_signs": ["Cancer"],
        "moolatrikona": {
            "sign": "Taurus",
            "start": 4,
            "end": 30
        }
    },

    "Mars": {
        "exaltation": "Capricorn",
        "debilitation": "Cancer",
        "exaltation_degree": 28,
        "own_signs": ["Aries", "Scorpio"],
        "moolatrikona": {
            "sign": "Aries",
            "start": 0,
            "end": 12
        }
    },

    "Mercury": {
        "exaltation": "Virgo",
        "debilitation": "Pisces",
        "exaltation_degree": 15,
        "own_signs": ["Gemini", "Virgo"],
        "moolatrikona": {
            "sign": "Virgo",
            "start": 16,
            "end": 20
        }
    },

    "Jupiter": {
        "exaltation": "Cancer",
        "debilitation": "Capricorn",
        "exaltation_degree": 5,
        "own_signs": ["Sagittarius", "Pisces"],
        "moolatrikona": {
            "sign": "Sagittarius",
            "start": 0,
            "end": 10
        }
    },

    "Venus": {
        "exaltation": "Pisces",
        "debilitation": "Virgo",
        "exaltation_degree": 27,
        "own_signs": ["Taurus", "Libra"],
        "moolatrikona": {
            "sign": "Libra",
            "start": 0,
            "end": 15
        }
    },

    "Saturn": {
        "exaltation": "Libra",
        "debilitation": "Aries",
        "exaltation_degree": 20,
        "own_signs": ["Capricorn", "Aquarius"],
        "moolatrikona": {
            "sign": "Aquarius",
            "start": 0,
            "end": 20
        }
    }
}


VALID_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]


def get_planetary_dignity(planet, sign, degree):
    """
    Determine a classical planet's sign dignity and
    whether it occupies its Moolatrikona degree range.

    Args:
        planet: Classical planet name.
        sign: Sidereal zodiac sign.
        degree: Degree within the sign (0 <= degree < 30).

    Returns:
        Dictionary containing dignity information.
    """

    if planet not in PLANETARY_DIGNITY:
        raise ValueError(
            f"Unsupported planet: {planet}. "
            "Rahu and Ketu are handled separately."
        )

    if sign not in VALID_SIGNS:
        raise ValueError(f"Invalid zodiac sign: {sign}")

    if (
        isinstance(degree, bool)
        or not isinstance(degree, (int, float))
        or not math.isfinite(degree)
        or not 0 <= degree < 30
    ):
        raise ValueError(
            "Degree must be a number between 0 and less than 30."
        )

    rules = PLANETARY_DIGNITY[planet]

    if sign == rules["exaltation"]:
        sign_dignity = "Exaltation sign"

    elif sign == rules["debilitation"]:
        sign_dignity = "Debilitation sign"

    elif sign in rules["own_signs"]:
        sign_dignity = "Own sign"

    else:
        sign_dignity = "Other sign"

    mt = rules["moolatrikona"]

    is_moolatrikona = (
        sign == mt["sign"]
        and mt["start"] <= degree < mt["end"]
    )

    return {
        "planet": planet,
        "sign": sign,
        "degree": degree,
        "sign_dignity": sign_dignity,
        "exaltation_degree": rules["exaltation_degree"],
        "moolatrikona": is_moolatrikona,
        "moolatrikona_sign": mt["sign"],
        "moolatrikona_range": (
            mt["start"],
            mt["end"]
        )
    }
