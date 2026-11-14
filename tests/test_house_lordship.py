import pytest

from engine.house_lordship import get_sign_lord, get_house_lords


def test_all_sign_lords():
    expected = {
        "Aries": "Mars",
        "Taurus": "Venus",
        "Gemini": "Mercury",
        "Cancer": "Moon",
        "Leo": "Sun",
        "Virgo": "Mercury",
        "Libra": "Venus",
        "Scorpio": "Mars",
        "Sagittarius": "Jupiter",
        "Capricorn": "Saturn",
        "Aquarius": "Saturn",
        "Pisces": "Jupiter",
    }

    for sign, lord in expected.items():
        assert get_sign_lord(sign) == lord


def test_leo_ascendant_house_lords():
    signs = [
        "Leo", "Virgo", "Libra", "Scorpio",
        "Sagittarius", "Capricorn", "Aquarius",
        "Pisces", "Aries", "Taurus", "Gemini", "Cancer",
    ]

    chart = {
        "houses": {
            i: {"sign": sign, "planets": []}
            for i, sign in enumerate(signs, start=1)
        }
    }

    result = get_house_lords(chart)

    assert result[1]["lord"] == "Sun"
    assert result[4]["lord"] == "Mars"
    assert result[7]["lord"] == "Saturn"
    assert result[10]["lord"] == "Venus"


def test_invalid_sign():
    with pytest.raises(ValueError):
        get_sign_lord("Invalid")


def test_missing_house():
    chart = {
        "houses": {
            1: {"sign": "Leo", "planets": []}
        }
    }

    with pytest.raises(ValueError):
        get_house_lords(chart)


def test_house_lord_placements():
    from engine.house_lordship import get_house_lord_placements

    signs = [
        "Leo", "Virgo", "Libra", "Scorpio",
        "Sagittarius", "Capricorn", "Aquarius",
        "Pisces", "Aries", "Taurus", "Gemini", "Cancer",
    ]

    chart = {
        "houses": {
            i: {"sign": sign, "planets": []}
            for i, sign in enumerate(signs, start=1)
        }
    }

    chart["houses"][6]["planets"] = [{"name": "Venus"}]
    chart["houses"][9]["planets"] = [{"name": "Sun"}]

    result = get_house_lord_placements(chart)

    assert result[10]["lord"] == "Venus"
    assert result[10]["lord_placed_in_house"] == 6

    assert result[1]["lord"] == "Sun"
    assert result[1]["lord_placed_in_house"] == 9

    assert result[4]["lord"] == "Mars"
    assert result[4]["lord_placed_in_house"] is None


def test_duplicate_planet_placement_is_rejected():
    from engine.house_lordship import get_house_lord_placements

    signs = [
        "Leo", "Virgo", "Libra", "Scorpio",
        "Sagittarius", "Capricorn", "Aquarius",
        "Pisces", "Aries", "Taurus", "Gemini", "Cancer",
    ]

    chart = {
        "houses": {
            i: {"sign": sign, "planets": []}
            for i, sign in enumerate(signs, start=1)
        }
    }

    chart["houses"][1]["planets"] = [{"name": "Sun"}]
    chart["houses"][2]["planets"] = [{"name": "Sun"}]

    with pytest.raises(ValueError):
        get_house_lord_placements(chart)
