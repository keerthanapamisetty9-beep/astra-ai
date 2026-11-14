"""
Ascendant-based planetary house ownership and classification.

Uses traditional Parashari sign rulership and Whole Sign houses.
"""

from engine.house_lordship import get_house_lords


KENDRA_HOUSES = [1, 4, 7, 10]
TRIKONA_HOUSES = [1, 5, 9]

DUSTHANA_HOUSES = [6, 8, 12]

MARAKA_HOUSES = [2, 7]

UPACHAYA_HOUSES = [3, 6, 10, 11]

NATURAL_BENEFICS = ["Moon", "Mercury", "Jupiter", "Venus"]

KENDRADHIPATI_CHECK_HOUSES = [4, 7, 10]


def get_planet_house_ownership(chart):
    """
    Return the houses owned by each planet for the chart's ascendant.
    """

    house_lords = get_house_lords(chart)

    results = {}

    for house_number, details in house_lords.items():
        planet = details["lord"]

        if planet not in results:
            results[planet] = []

        results[planet].append(house_number)

    return results


def get_planet_house_groups(chart):
    """
    Identify each planet's Kendra and Trikona house ownership.
    """

    ownership = get_planet_house_ownership(chart)

    results = {}

    for planet, houses in ownership.items():
        results[planet] = {
            "owned_houses": houses,
            "kendra_houses": [
                house for house in houses
                if house in KENDRA_HOUSES
            ],
            "trikona_houses": [
                house for house in houses
                if house in TRIKONA_HOUSES
            ],
        }

    return results


def get_yogakaraka_planets(chart):
    """
    Identify planets owning both a Kendra and a distinct Trikona house.

    This detects the traditional Yogakaraka ownership pattern.
    """

    house_groups = get_planet_house_groups(chart)

    results = []

    for planet, details in house_groups.items():
        kendra_houses = details["kendra_houses"]
        trikona_houses = details["trikona_houses"]

        distinct_kendra = [
            house for house in kendra_houses
            if house not in trikona_houses
        ]

        distinct_trikona = [
            house for house in trikona_houses
            if house not in kendra_houses
        ]

        if distinct_kendra and distinct_trikona:
            results.append({
                "planet": planet,
                "kendra_houses": kendra_houses,
                "trikona_houses": trikona_houses,
            })

    return results


FUNCTIONAL_BENEFIC_HOUSES = [1, 5, 9]

FUNCTIONAL_CHALLENGING_HOUSES = [3, 6, 8, 11, 12]


def get_functional_nature(chart):
    """
    Classify planets by their house ownership.

    This is an initial configurable Parashari classification policy.
    Maraka ownership and Yogakaraka status are reported separately.
    """

    ownership = get_planet_house_ownership(chart)
    house_groups = get_planet_house_groups(chart)
    yogakaraka_planets = {
        item["planet"] for item in get_yogakaraka_planets(chart)
    }

    results = {}

    for planet, houses in ownership.items():

        favourable_houses = [
            house for house in houses
            if house in FUNCTIONAL_BENEFIC_HOUSES
        ]

        challenging_houses = [
            house for house in houses
            if house in FUNCTIONAL_CHALLENGING_HOUSES
        ]

        maraka_houses = [
            house for house in houses
            if house in MARAKA_HOUSES
        ]

        if favourable_houses and challenging_houses:
            category = "Mixed"
        elif favourable_houses:
            category = "Benefic"
        elif challenging_houses:
            category = "Malefic"
        else:
            category = "Neutral"

        results[planet] = {
            "owned_houses": houses,
            "kendra_houses": house_groups[planet]["kendra_houses"],
            "trikona_houses": house_groups[planet]["trikona_houses"],
            "favourable_houses": favourable_houses,
            "challenging_houses": challenging_houses,
            "maraka_houses": maraka_houses,
            "functional_category": category,
            "is_yogakaraka": planet in yogakaraka_planets,
            "is_maraka_lord": bool(maraka_houses),
        }

    return results


def get_kendradhipati_dosha(chart):
    """
    Identify natural benefics owning the 4th, 7th, or 10th house.

    This is a configurable, preliminary Kendradhipati Dosha check.
    The 1st house is excluded because it is also a Trikona.

    Interpretations vary across Jyotish traditions. This function
    identifies a potential condition; it does not judge its strength
    or predict its results.
    """

    ownership = get_planet_house_ownership(chart)

    results = []

    for planet, houses in ownership.items():

        if planet not in NATURAL_BENEFICS:
            continue

        relevant_kendra_houses = [
            house for house in houses
            if house in KENDRADHIPATI_CHECK_HOUSES
        ]

        if relevant_kendra_houses:
            results.append({
                "planet": planet,
                "owned_kendra_houses": relevant_kendra_houses,
                "potential_kendradhipati_dosha": True,
            })

    return results
