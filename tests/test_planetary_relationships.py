import pytest

from engine.planetary_relationships import (
    NATURAL_RELATIONSHIPS,
    get_natural_relationship,
    get_all_natural_relationships,
)


def test_all_seven_planets_are_defined():
    assert len(NATURAL_RELATIONSHIPS) == 7


@pytest.mark.parametrize(
    "planet",
    list(NATURAL_RELATIONSHIPS.keys()),
)
def test_every_planet_classifies_all_other_planets(planet):
    relationships = get_all_natural_relationships(planet)

    friends = relationships["friends"]
    enemies = relationships["enemies"]
    neutral = relationships["neutral"]

    classified = friends + enemies + neutral

    assert len(classified) == 6
    assert len(set(classified)) == 6
    assert planet not in classified
    assert set(classified) == set(NATURAL_RELATIONSHIPS.keys()) - {planet}


def test_sun_jupiter_friendship():
    assert get_natural_relationship("Sun", "Jupiter") == "Friend"


def test_sun_saturn_enmity():
    assert get_natural_relationship("Sun", "Saturn") == "Enemy"


def test_venus_mercury_friendship():
    assert get_natural_relationship("Venus", "Mercury") == "Friend"


def test_moon_has_no_natural_enemies():
    result = get_all_natural_relationships("Moon")

    assert result["enemies"] == []


def test_same_planet():
    assert get_natural_relationship("Jupiter", "Jupiter") == "Same planet"


def test_invalid_planet():
    with pytest.raises(ValueError):
        get_natural_relationship("Rahu", "Sun")


def test_invalid_other_planet():
    with pytest.raises(ValueError):
        get_natural_relationship("Sun", "Ketu")
