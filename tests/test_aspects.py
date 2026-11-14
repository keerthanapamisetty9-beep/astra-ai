import pytest

from engine.aspects import get_aspected_houses


@pytest.mark.parametrize(
    "planet, expected",
    [
        ("Sun", [7]),
        ("Moon", [7]),
        ("Mars", [4, 7, 8]),
        ("Mercury", [7]),
        ("Jupiter", [5, 7, 9]),
        ("Venus", [7]),
        ("Saturn", [3, 7, 10]),
    ],
)
def test_planet_aspects_from_first_house(planet, expected):
    assert get_aspected_houses(1, planet) == expected


def test_mars_aspects_wrap_around():
    assert get_aspected_houses(10, "Mars") == [1, 4, 5]


def test_jupiter_aspects_wrap_around():
    assert get_aspected_houses(10, "Jupiter") == [2, 4, 6]


def test_saturn_aspects_wrap_around():
    assert get_aspected_houses(10, "Saturn") == [12, 4, 7]


@pytest.mark.parametrize("house", [0, 13, -1, 2.5, True])
def test_invalid_house(house):
    with pytest.raises(ValueError):
        get_aspected_houses(house, "Mars")


def test_unsupported_planet():
    with pytest.raises(ValueError):
        get_aspected_houses(1, "Rahu")


def test_chart_aspects():
    from engine.aspects import get_chart_aspects

    chart = {
        "houses": {
            1: {"planets": [{"name": "Sun"}, {"name": "Mars"}]},
            4: {"planets": [{"name": "Moon"}]},
            5: {"planets": [{"name": "Jupiter"}]},
            7: {"planets": [{"name": "Saturn"}]},
            8: {"planets": [{"name": "Mercury"}]},
            9: {"planets": [{"name": "Rahu"}, {"name": "Ketu"}]},
        }
    }

    result = get_chart_aspects(chart)

    assert result["Sun"]["aspected_houses"] == [7]
    assert result["Sun"]["aspected_planets"] == {"Saturn": 7}

    assert result["Mars"]["aspected_planets"] == {
        "Moon": 4,
        "Saturn": 7,
        "Mercury": 8,
    }

    assert result["Jupiter"]["aspected_planets"] == {
        "Sun": 1,
        "Mars": 1,
    }

    assert "Rahu" not in result
    assert "Ketu" not in result


def test_duplicate_planet_in_chart_is_rejected():
    from engine.aspects import get_chart_aspects

    chart = {
        "houses": {
            1: {"planets": [{"name": "Sun"}]},
            2: {"planets": [{"name": "Sun"}]},
        }
    }

    with pytest.raises(ValueError):
        get_chart_aspects(chart)
