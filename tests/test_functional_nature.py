import pytest

from engine.functional_nature import get_planet_house_ownership, get_planet_house_groups, get_yogakaraka_planets, get_functional_nature, get_kendradhipati_dosha
from engine.d1_chart import SIGNS


def make_chart(ascendant_sign):
    ascendant_index = SIGNS.index(ascendant_sign)

    houses = {}

    for house_number in range(1, 13):
        sign_index = (ascendant_index + house_number - 1) % 12

        houses[house_number] = {
            "sign": SIGNS[sign_index],
            "planets": [],
        }

    return {"houses": houses}


def test_leo_ascendant_ownership():
    chart = make_chart("Leo")

    result = get_planet_house_ownership(chart)

    assert result == {
        "Sun": [1],
        "Moon": [12],
        "Mars": [4, 9],
        "Mercury": [2, 11],
        "Jupiter": [5, 8],
        "Venus": [3, 10],
        "Saturn": [6, 7],
    }


def test_aries_ascendant_ownership():
    chart = make_chart("Aries")

    result = get_planet_house_ownership(chart)

    assert result == {
        "Mars": [1, 8],
        "Venus": [2, 7],
        "Mercury": [3, 6],
        "Moon": [4],
        "Sun": [5],
        "Jupiter": [9, 12],
        "Saturn": [10, 11],
    }


def test_every_planet_owns_at_least_one_house():
    chart = make_chart("Taurus")

    result = get_planet_house_ownership(chart)

    assert len(result) == 7

    for houses in result.values():
        assert len(houses) >= 1


def test_invalid_chart():
    with pytest.raises(ValueError):
        get_planet_house_ownership({})


def test_leo_ascendant_kendra_and_trikona_ownership():
    chart = make_chart("Leo")

    result = get_planet_house_groups(chart)

    assert result["Sun"]["kendra_houses"] == [1]
    assert result["Sun"]["trikona_houses"] == [1]

    assert result["Mars"]["kendra_houses"] == [4]
    assert result["Mars"]["trikona_houses"] == [9]

    assert result["Jupiter"]["kendra_houses"] == []
    assert result["Jupiter"]["trikona_houses"] == [5]


def test_yogakaraka_house_ownership_pattern():
    chart = make_chart("Taurus")

    result = get_planet_house_groups(chart)

    # Saturn owns the 9th and 10th houses for Taurus ascendant.
    assert result["Saturn"]["kendra_houses"] == [10]
    assert result["Saturn"]["trikona_houses"] == [9]


def test_taurus_saturn_is_yogakaraka():
    chart = make_chart("Taurus")

    result = get_yogakaraka_planets(chart)

    assert len(result) == 1
    assert result[0]["planet"] == "Saturn"
    assert result[0]["kendra_houses"] == [10]
    assert result[0]["trikona_houses"] == [9]


def test_leo_mars_is_yogakaraka():
    chart = make_chart("Leo")

    result = get_yogakaraka_planets(chart)

    mars = next(
        planet for planet in result
        if planet["planet"] == "Mars"
    )

    assert mars["kendra_houses"] == [4]
    assert mars["trikona_houses"] == [9]


def test_first_house_ownership_alone_is_not_yogakaraka():
    chart = make_chart("Leo")

    result = get_yogakaraka_planets(chart)

    # Sun owns only the 1st house, which belongs to both groups.
    assert all(
        planet["planet"] != "Sun"
        for planet in result
    )


def test_leo_ascendant_functional_classification():
    chart = make_chart("Leo")

    result = get_functional_nature(chart)

    assert result["Sun"]["functional_category"] == "Benefic"
    assert result["Mars"]["functional_category"] == "Benefic"
    assert result["Jupiter"]["functional_category"] == "Mixed"
    assert result["Mercury"]["functional_category"] == "Malefic"
    assert result["Saturn"]["functional_category"] == "Malefic"


def test_taurus_saturn_functional_classification():
    chart = make_chart("Taurus")

    result = get_functional_nature(chart)

    assert result["Saturn"]["functional_category"] == "Benefic"
    assert result["Saturn"]["is_yogakaraka"] is True


def test_maraka_ownership_is_reported_separately():
    chart = make_chart("Leo")

    result = get_functional_nature(chart)

    assert result["Mercury"]["maraka_houses"] == [2]
    assert result["Saturn"]["maraka_houses"] == [7]

    assert result["Mercury"]["is_maraka_lord"] is True
    assert result["Saturn"]["is_maraka_lord"] is True


def test_neutral_functional_classification():
    chart = make_chart("Aries")

    result = get_functional_nature(chart)

    # Moon owns only the 4th house.
    assert result["Moon"]["functional_category"] == "Neutral"


def test_leo_venus_triggers_potential_kendradhipati_dosha():
    chart = make_chart("Leo")

    result = get_kendradhipati_dosha(chart)

    venus = next(
        planet for planet in result
        if planet["planet"] == "Venus"
    )

    assert venus["owned_kendra_houses"] == [10]
    assert venus["potential_kendradhipati_dosha"] is True


def test_libra_moon_triggers_potential_kendradhipati_dosha():
    chart = make_chart("Libra")

    result = get_kendradhipati_dosha(chart)

    moon = next(
        planet for planet in result
        if planet["planet"] == "Moon"
    )

    assert moon["owned_kendra_houses"] == [10]


def test_aries_moon_triggers_potential_kendradhipati_dosha():
    chart = make_chart("Aries")

    result = get_kendradhipati_dosha(chart)

    assert {
        "planet": "Moon",
        "owned_kendra_houses": [4],
        "potential_kendradhipati_dosha": True,
    } in result


def test_natural_malefics_are_excluded_from_kendradhipati_check():
    chart = make_chart("Aries")

    result = get_kendradhipati_dosha(chart)

    detected_planets = [
        item["planet"] for item in result
    ]

    assert "Mars" not in detected_planets
    assert "Saturn" not in detected_planets
    assert "Sun" not in detected_planets
