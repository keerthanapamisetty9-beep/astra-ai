import pytest

from engine.panchadha_maitri import get_panchadha_relationship


@pytest.mark.parametrize(
    "natural, temporary, expected",
    [
        ("Friend", "Friend", "Great Friend"),
        ("Friend", "Enemy", "Neutral"),
        ("Neutral", "Friend", "Friend"),
        ("Neutral", "Enemy", "Enemy"),
        ("Enemy", "Friend", "Neutral"),
        ("Enemy", "Enemy", "Great Enemy"),
    ],
)
def test_all_panchadha_combinations(natural, temporary, expected):
    from engine.panchadha_maitri import COMPOUND_RELATIONSHIPS

    assert COMPOUND_RELATIONSHIPS[(natural, temporary)] == expected


def test_sun_moon_relationship():
    result = get_panchadha_relationship("Sun", "Moon", 1, 2)

    assert result["natural_relationship"] == "Friend"
    assert result["temporary_relationship"] == "Friend"
    assert result["panchadha_relationship"] == "Great Friend"


def test_same_planet_is_rejected():
    with pytest.raises(ValueError):
        get_panchadha_relationship("Sun", "Sun", 1, 2)


def test_rahu_is_not_supported():
    with pytest.raises(ValueError):
        get_panchadha_relationship("Rahu", "Sun", 1, 2)


def test_chart_panchadha_relationships():
    from engine.panchadha_maitri import get_chart_panchadha_relationships

    chart = {
        "houses": {
            1: {
                "planets": [
                    {"name": "Sun"},
                    {"name": "Mercury"},
                ]
            },
            2: {"planets": [{"name": "Moon"}]},
            3: {"planets": [{"name": "Mars"}]},
            4: {"planets": [{"name": "Rahu"}, {"name": "Ketu"}]},
        }
    }

    result = get_chart_panchadha_relationships(chart)

    assert result["Sun"]["Moon"]["panchadha_relationship"] == "Great Friend"
    assert result["Sun"]["Mercury"]["panchadha_relationship"] == "Enemy"
    assert result["Sun"]["Mars"]["panchadha_relationship"] == "Great Friend"

    assert "Rahu" not in result
    assert "Ketu" not in result


def test_chart_relationships_are_directional():
    from engine.panchadha_maitri import get_chart_panchadha_relationships

    chart = {
        "houses": {
            1: {"planets": [{"name": "Sun"}]},
            2: {"planets": [{"name": "Mercury"}]},
        }
    }

    result = get_chart_panchadha_relationships(chart)

    assert result["Sun"]["Mercury"]["natural_relationship"] == "Neutral"
    assert result["Mercury"]["Sun"]["natural_relationship"] == "Friend"
