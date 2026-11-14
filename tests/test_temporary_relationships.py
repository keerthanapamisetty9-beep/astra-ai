import pytest

from engine.temporary_relationships import (
    get_temporary_relationship,
    get_chart_temporary_relationships,
)


@pytest.mark.parametrize(
    "position",
    [2, 3, 4, 10, 11, 12],
)
def test_temporary_friends(position):
    assert get_temporary_relationship(1, position) == "Friend"


@pytest.mark.parametrize(
    "position",
    [1, 5, 6, 7, 8, 9],
)
def test_temporary_enemies(position):
    assert get_temporary_relationship(1, position) == "Enemy"


def test_relationship_counting_wraps_around():
    assert get_temporary_relationship(11, 1) == "Friend"


@pytest.mark.parametrize("house", [0, 13, -1])
def test_invalid_house(house):
    with pytest.raises(ValueError):
        get_temporary_relationship(1, house)


def test_chart_temporary_relationships():
    chart = {
        "houses": {
            1: {"planets": [{"name": "Sun"}]},
            2: {"planets": [{"name": "Moon"}]},
            3: {"planets": [{"name": "Mars"}]},
        }
    }

    result = get_chart_temporary_relationships(chart)

    assert result["Sun"]["Moon"] == "Friend"
    assert result["Sun"]["Mars"] == "Friend"
    assert result["Moon"]["Mars"] == "Friend"


def test_same_house_planets_are_temporary_enemies():
    chart = {
        "houses": {
            1: {
                "planets": [
                    {"name": "Sun"},
                    {"name": "Mercury"},
                ]
            }
        }
    }

    result = get_chart_temporary_relationships(chart)

    assert result["Sun"]["Mercury"] == "Enemy"
    assert result["Mercury"]["Sun"] == "Enemy"
