
from datetime import datetime

from engine.vimshottari import (
    calculate_birth_dasha,
    generate_mahadasha_timeline,
    generate_antardashas,
    find_current_dasha
)


BIRTH_DATE = datetime(2000, 5, 7, 13, 10)
MOON_LONGITUDE = 66.410695


def test_birth_dasha_is_mars():
    result = calculate_birth_dasha(MOON_LONGITUDE)

    assert result["nakshatra_lord"] == "Mars"
    assert result["mahadasha_years"] == 7


def test_birth_dasha_balance_is_valid():
    result = calculate_birth_dasha(MOON_LONGITUDE)

    assert 0 <= result["balance_years"] <= 7


def test_mahadasha_timeline_has_nine_periods():
    birth = calculate_birth_dasha(MOON_LONGITUDE)
    timeline = generate_mahadasha_timeline(BIRTH_DATE, birth)

    assert len(timeline) == 9


def test_mahadasha_sequence_is_correct():
    birth = calculate_birth_dasha(MOON_LONGITUDE)
    timeline = generate_mahadasha_timeline(BIRTH_DATE, birth)

    expected = [
        "Mars", "Rahu", "Jupiter", "Saturn",
        "Mercury", "Ketu", "Venus", "Sun", "Moon"
    ]

    actual = [period["planet"] for period in timeline]

    assert actual == expected


def test_antardasha_sequence_is_correct():
    birth = calculate_birth_dasha(MOON_LONGITUDE)
    timeline = generate_mahadasha_timeline(BIRTH_DATE, birth)

    jupiter = next(
        period for period in timeline
        if period["planet"] == "Jupiter"
    )

    antardashas = generate_antardashas(jupiter)

    expected = [
        "Jupiter", "Saturn", "Mercury", "Ketu",
        "Venus", "Sun", "Moon", "Mars", "Rahu"
    ]

    actual = [
        period["antardasha"]
        for period in antardashas
    ]

    assert actual == expected


def test_current_dasha_detection():
    birth = calculate_birth_dasha(MOON_LONGITUDE)
    timeline = generate_mahadasha_timeline(BIRTH_DATE, birth)

    result = find_current_dasha(
        timeline,
        datetime(2026, 11, 13)
    )

    assert result["mahadasha"] == "Jupiter"
    assert result["antardasha"] == "Venus"
