import pytest

from engine.combustion import (
    get_sun_distance,
    get_planetary_combustion,
    get_chart_combustion,
)


def test_sun_distance():
    assert get_sun_distance(100, 110) == 10
    assert get_sun_distance(359, 1) == 2
    assert get_sun_distance(0, 180) == 180


def test_invalid_longitude():
    with pytest.raises(ValueError):
        get_sun_distance(-1, 100)

    with pytest.raises(ValueError):
        get_sun_distance(100, 360)


def test_mercury_combustion_direct_and_retrograde():
    direct = get_planetary_combustion("Mercury", 100, 110, False)
    retrograde = get_planetary_combustion("Mercury", 100, 113, True)

    assert direct["is_combust"] is True
    assert retrograde["is_combust"] is False


def test_venus_combustion_direct_and_retrograde():
    direct = get_planetary_combustion("Venus", 100, 109, False)
    retrograde = get_planetary_combustion("Venus", 100, 109, True)

    assert direct["is_combust"] is True
    assert retrograde["is_combust"] is False


def test_planet_outside_combustion_limit():
    result = get_planetary_combustion("Saturn", 100, 116)

    assert result["is_combust"] is False
    assert result["sun_distance"] == 16


def test_complete_chart_combustion():
    planets = {
        "Sun": {"longitude": 100},
        "Moon": {"longitude": 108, "retrograde": False},
        "Mars": {"longitude": 125, "retrograde": False},
        "Mercury": {"longitude": 110, "retrograde": False},
        "Jupiter": {"longitude": 150, "retrograde": False},
        "Venus": {"longitude": 107, "retrograde": True},
        "Saturn": {"longitude": 130, "retrograde": False},
    }

    result = get_chart_combustion(planets)

    assert result["Moon"]["is_combust"] is True
    assert result["Mercury"]["is_combust"] is True
    assert result["Venus"]["is_combust"] is True

    assert result["Mars"]["is_combust"] is False
    assert result["Jupiter"]["is_combust"] is False
    assert result["Saturn"]["is_combust"] is False


def test_missing_planet():
    planets = {
        "Sun": {"longitude": 100},
    }

    with pytest.raises(ValueError):
        get_chart_combustion(planets)


def test_unsupported_planet():
    with pytest.raises(ValueError):
        get_planetary_combustion("Rahu", 100, 105)
