
from engine.transits import calculate_transit_houses


def test_transit_house_from_moon():
    transit_planets = {
        "Jupiter": {
            "sign": "Leo",
            "degree": 1.4158
        }
    }

    result = calculate_transit_houses(
        transit_planets,
        "Gemini",
        "Leo"
    )

    assert result["Jupiter"]["house_from_moon"] == 3


def test_transit_house_from_lagna():
    transit_planets = {
        "Jupiter": {
            "sign": "Leo",
            "degree": 1.4158
        }
    }

    result = calculate_transit_houses(
        transit_planets,
        "Gemini",
        "Leo"
    )

    assert result["Jupiter"]["house_from_lagna"] == 1


def test_all_nine_planets_transit_houses():
    transit_planets = {
        "Sun": {"sign": "Libra", "degree": 26.88},
        "Moon": {"sign": "Sagittarius", "degree": 13.43},
        "Mars": {"sign": "Leo", "degree": 0.40},
        "Mercury": {"sign": "Libra", "degree": 10.80},
        "Jupiter": {"sign": "Leo", "degree": 1.41},
        "Venus": {"sign": "Virgo", "degree": 28.63},
        "Saturn": {"sign": "Pisces", "degree": 14.36},
        "Rahu": {"sign": "Aquarius", "degree": 1.09},
        "Ketu": {"sign": "Leo", "degree": 1.09}
    }

    result = calculate_transit_houses(
        transit_planets,
        "Gemini",
        "Leo"
    )

    assert len(result) == 9
    assert "Rahu" in result
    assert "Ketu" in result


def test_transit_house_range():
    transit_planets = {
        "Saturn": {
            "sign": "Pisces",
            "degree": 14.36
        }
    }

    result = calculate_transit_houses(
        transit_planets,
        "Gemini",
        "Leo"
    )

    assert 1 <= result["Saturn"]["house_from_moon"] <= 12
    assert 1 <= result["Saturn"]["house_from_lagna"] <= 12
