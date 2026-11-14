
# ==========================================
# ASTRA AI - VEDIC INTERPRETATION ENGINE
# ==========================================

# Traditional planetary significations (Karakatvas)

PLANET_MEANINGS = {

    "Sun": [
        "Authority", "Leadership", "Confidence",
        "Father", "Recognition", "Vitality"
    ],

    "Moon": [
        "Mind", "Emotions", "Mother",
        "Mental comfort", "Public connection"
    ],

    "Mars": [
        "Courage", "Energy", "Action",
        "Siblings", "Property", "Competition"
    ],

    "Mercury": [
        "Communication", "Intelligence", "Learning",
        "Business", "Analytical thinking"
    ],

    "Jupiter": [
        "Wisdom", "Knowledge", "Teachers",
        "Children", "Expansion", "Spirituality"
    ],

    "Venus": [
        "Relationships", "Marriage", "Beauty",
        "Comforts", "Creativity", "Luxury"
    ],

    "Saturn": [
        "Discipline", "Responsibility", "Patience",
        "Hard work", "Delays", "Long-term results"
    ],

    "Rahu": [
        "Ambition", "Material desires",
        "Unconventional experiences",
        "Foreign connections", "Obsession"
    ],

    "Ketu": [
        "Detachment", "Spirituality",
        "Introspection", "Past-life themes",
        "Liberation"
    ]
}


# ==========================================
# 12 HOUSES - BHAVA SIGNIFICATIONS
# ==========================================

HOUSE_MEANINGS = {

    1: [
        "Personality", "Physical appearance",
        "Health and vitality", "Self and identity"
    ],

    2: [
        "Wealth and savings", "Family",
        "Speech", "Food and possessions"
    ],

    3: [
        "Courage", "Communication", "Younger siblings",
        "Efforts and skills", "Short journeys"
    ],

    4: [
        "Mother", "Home and property", "Education",
        "Vehicles", "Emotional happiness"
    ],

    5: [
        "Children", "Intelligence", "Creativity",
        "Education", "Romance", "Purva Punya"
    ],

    6: [
        "Debts", "Diseases", "Enemies",
        "Competition", "Service", "Daily work"
    ],

    7: [
        "Marriage", "Spouse", "Partnerships",
        "Business relationships", "Public dealings"
    ],

    8: [
        "Longevity", "Transformation", "Sudden events",
        "Research", "Secrets", "Inheritance"
    ],

    9: [
        "Fortune", "Dharma", "Higher education",
        "Father", "Teachers and gurus",
        "Long-distance journeys"
    ],

    10: [
        "Career", "Profession", "Reputation",
        "Authority", "Actions and responsibilities"
    ],

    11: [
        "Income and gains", "Fulfilment of desires",
        "Elder siblings", "Social networks", "Achievements"
    ],

    12: [
        "Expenses", "Foreign residence", "Isolation",
        "Sleep", "Spiritual liberation", "Moksha"
    ]
}


# ==========================================
# HUMAN-WRITTEN PLANET-HOUSE INTERPRETATIONS
# ==========================================

PLANET_HOUSE_INTERPRETATIONS = {

    ("Jupiter", 9): {
        "title": "Jupiter in the 9th House",

        "overview": (
            "Jupiter in the 9th house is traditionally "
            "considered a supportive placement in Vedic "
            "astrology. This house is connected with "
            "higher education, beliefs, teachers and "
            "the way we understand life."
        ),

        "daily_life": (
            "You may find yourself naturally interested "
            "in learning new things, exploring different "
            "ideas and understanding why things happen "
            "the way they do. You might also value advice "
            "from experienced people and learn a lot "
            "through teachers, mentors or life experiences."
        ),

        "opportunities": (
            "Education, teaching, travelling or exploring "
            "different cultures and philosophies may become "
            "important areas of interest. Over time, these "
            "experiences can help you develop your own "
            "understanding of life."
        ),

        "things_to_consider": (
            "Jupiter's results depend on more than its house "
            "placement. Its sign, strength, house lordship, "
            "aspects and conjunctions can change how this "
            "placement works in your chart."
        )
    }

}


# ==========================================
# PLANET IN HOUSE CONTEXT
# ==========================================

def get_planet_house_context(planet, house):
    """
    Collect traditional astrological information
    about a planet placed in a particular house.
    """

    if planet not in PLANET_MEANINGS:
        raise ValueError(f"Unknown planet: {planet}")

    if house not in HOUSE_MEANINGS:
        raise ValueError(f"Invalid house number: {house}")

    return {
        "planet": planet,
        "house": house,
        "planet_themes": PLANET_MEANINGS[planet],
        "house_themes": HOUSE_MEANINGS[house]
    }


# ==========================================
# NATURAL-LANGUAGE INTERPRETATION
# ==========================================

def interpret_planet_in_house(planet, house):
    """
    Return a human-written interpretation when available.

    Other placements return their traditional context
    until a complete interpretation has been written.
    """

    context = get_planet_house_context(planet, house)

    interpretation = PLANET_HOUSE_INTERPRETATIONS.get(
        (planet, house)
    )

    return {
        **context,
        "interpretation": interpretation
    }
