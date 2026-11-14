import pytest

from engine.conjunctions import (
    get_angular_distance,
    get_chart_conjunctions,
)


def create_sample_chart():
    signs = [
        "Leo", "Virgo", "Libra", "Scorpio",
        "Sagittarius", "Capricorn", "Aquarius",
        "Pisces", "Aries", "Taurus", "Gemini", "Cancer",
    ]

    return {
        "houses": {
            i: {"sign": sign, "planets": []}
            for i, sign in enumerate(signs, start=1)
        }
    }


def test_angular_distance():
    assert get_angular_distance(10, 15) == 5
    assert get_angular_distance(15, 10) == 5
    assert get_angular_distance(359, 1) == 2
    assert get_angular_distance(0, 180) == 180


def test_invalid_degrees():
    with pytest.raises(ValueError):
        get_angular_distance(-1, 10)

    with pytest.raises(ValueError):
        get_angular_distance(10, 360)

    with pytest.raises(ValueError):
        get_angular_distance(True, 10)


def test_sun_mercury_conjunction():
    chart = create_sample_chart()

    chart["houses"][1]["planets"] = [
        {"name": "Sun", "degree": 10, "retrograde": False},
        {"name": "Mercury", "degree": 15, "retrograde": False},
    ]

    chart["houses"][5]["planets"] = [
        {"name": "Mars", "degree": 20, "retrograde": False},
    ]

    result = get_chart_conjunctions(chart)

    assert len(result) == 1
    assert result[0]["planet1"] == "Sun"
    assert result[0]["planet2"] == "Mercury"
    assert result[0]["house"] == 1
    assert result[0]["sign"] == "Leo"
    assert result[0]["angular_distance"] == 5


def test_multiple_planets_in_same_house():
    chart = create_sample_chart()

    chart["houses"][1]["planets"] = [
        {"name": "Sun", "degree": 10},
        {"name": "Mercury", "degree": 15},
        {"name": "Venus", "degree": 18},
    ]

    result = get_chart_conjunctions(chart)

    assert len(result) == 3


def test_no_conjunctions():
    chart = create_sample_chart()

    chart["houses"][1]["planets"] = [
        {"name": "Sun", "degree": 10},
    ]

    chart["houses"][2]["planets"] = [
        {"name": "Moon", "degree": 12},
    ]

    assert get_chart_conjunctions(chart) == []


def test_missing_house():
    chart = create_sample_chart()
    del chart["houses"][12]

    with pytest.raises(ValueError):
        get_chart_conjunctions(chart)
