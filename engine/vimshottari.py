from datetime import datetime, timedelta

# ASTRA AI - VIMSHOTTARI DASHA ENGINE

# Standard Vimshottari Mahadasha sequence

DASHA_SEQUENCE = [
    ("Ketu", 7),
    ("Venus", 20),
    ("Sun", 6),
    ("Moon", 10),
    ("Mars", 7),
    ("Rahu", 18),
    ("Jupiter", 16),
    ("Saturn", 19),
    ("Mercury", 17)
]

TOTAL_DASHA_YEARS = 120

# Average Gregorian year for date calculations
DAYS_PER_YEAR = 365.25



# Nakshatra lords follow the Vimshottari sequence.
NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon",
    "Mars", "Rahu", "Jupiter", "Saturn",
    "Mercury"
]


def calculate_birth_dasha(moon_longitude):
    """
    Calculate the birth Mahadasha and its remaining balance
    using the Moon's sidereal longitude.
    """

    nakshatra_size = 360.0 / 27.0

    moon_longitude = moon_longitude % 360

    nakshatra_index = int(
        moon_longitude / nakshatra_size
    )

    position_in_nakshatra = (
        moon_longitude - nakshatra_index * nakshatra_size
    )

    fraction_completed = (
        position_in_nakshatra / nakshatra_size
    )

    fraction_remaining = 1 - fraction_completed

    dasha_lord = NAKSHATRA_LORDS[
        nakshatra_index % 9
    ]

    dasha_years = dict(DASHA_SEQUENCE)[dasha_lord]

    balance_years = (
        dasha_years * fraction_remaining
    )

    return {
        "nakshatra_index": nakshatra_index,
        "nakshatra_lord": dasha_lord,
        "fraction_completed": fraction_completed,
        "fraction_remaining": fraction_remaining,
        "mahadasha_years": dasha_years,
        "balance_years": balance_years
    }


def generate_mahadasha_timeline(birth_datetime, birth_dasha):
    """
    Generate the nine Mahadasha periods starting from birth.
    """

    birth_lord = birth_dasha["nakshatra_lord"]
    balance_years = birth_dasha["balance_years"]

    sequence_names = [
        planet for planet, years in DASHA_SEQUENCE
    ]

    birth_index = sequence_names.index(birth_lord)

    timeline = []

    current_start = birth_datetime

    # First period: remaining balance of birth Mahadasha
    first_end = current_start + timedelta(
        days=balance_years * DAYS_PER_YEAR
    )

    timeline.append({
        "planet": birth_lord,
        "duration_years": balance_years,
        "start": current_start,
        "end": first_end
    })

    current_start = first_end

    # Remaining eight Mahadashas
    for i in range(1, 9):
        planet_index = (
            birth_index + i
        ) % len(DASHA_SEQUENCE)

        planet, duration = DASHA_SEQUENCE[planet_index]

        current_end = current_start + timedelta(
            days=duration * DAYS_PER_YEAR
        )

        timeline.append({
            "planet": planet,
            "duration_years": duration,
            "start": current_start,
            "end": current_end
        })

        current_start = current_end

    return timeline


def generate_antardashas(mahadasha):
    """
    Generate the nine Antardashas within a Mahadasha.
    """

    sequence_names = [
        planet for planet, years in DASHA_SEQUENCE
    ]

    years_map = dict(DASHA_SEQUENCE)

    maha_lord = mahadasha["planet"]
    maha_duration = years_map[maha_lord]

    maha_index = sequence_names.index(maha_lord)

    antardashas = []
    current_start = mahadasha["start"]

    for i in range(9):
        antar_index = (
            maha_index + i
        ) % 9

        antar_lord = sequence_names[antar_index]

        antar_duration = (
            maha_duration
            * years_map[antar_lord]
            / TOTAL_DASHA_YEARS
        )

        current_end = current_start + timedelta(
            days=antar_duration * DAYS_PER_YEAR
        )

        antardashas.append({
            "mahadasha": maha_lord,
            "antardasha": antar_lord,
            "duration_years": antar_duration,
            "start": current_start,
            "end": current_end
        })

        current_start = current_end

    return antardashas



def find_current_dasha(mahadasha_timeline, target_date):
    """
    Find the active Mahadasha and Antardasha
    for a given date.
    """

    for mahadasha in mahadasha_timeline:

        if mahadasha["start"] <= target_date < mahadasha["end"]:

            antardashas = generate_antardashas(mahadasha)

            for antardasha in antardashas:

                if (
                    antardasha["start"]
                    <= target_date
                    < antardasha["end"]
                ):
                    return {
                        "mahadasha": mahadasha["planet"],
                        "mahadasha_start": mahadasha["start"],
                        "mahadasha_end": mahadasha["end"],
                        "antardasha": antardasha["antardasha"],
                        "antardasha_start": antardasha["start"],
                        "antardasha_end": antardasha["end"]
                    }

    return None
