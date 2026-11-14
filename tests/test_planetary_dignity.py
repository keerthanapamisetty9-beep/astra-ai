import pytest

from engine.planetary_dignity import get_planetary_dignity


@pytest.mark.parametrize(
    "planet, sign, degree, expected_dignity, expected_mt",
    [
        ("Sun", "Aries", 10, "Exaltation sign", False),
        ("Moon", "Taurus", 3, "Exaltation sign", False),
        ("Mars", "Capricorn", 28, "Exaltation sign", False),
        ("Mercury", "Virgo", 17, "Exaltation sign", True),
        ("Jupiter", "Cancer", 5, "Exaltation sign", False),
        ("Venus", "Pisces", 27, "Exaltation sign", False),
        ("Saturn", "Libra", 20, "Exaltation sign", False),
    ],
)
def test_exaltation(
    planet, sign, degree, expected_dignity, expected_mt
):
    result = get_planetary_dignity(planet, sign, degree)

    assert result["sign_dignity"] == expected_dignity
    assert result["moolatrikona"] == expected_mt


@pytest.mark.parametrize(
    "planet, sign, degree",
    [
        ("Sun", "Leo", 10),
        ("Moon", "Taurus", 10),
        ("Mars", "Aries", 5),
        ("Mercury", "Virgo", 18),
        ("Jupiter", "Sagittarius", 5),
        ("Venus", "Libra", 10),
        ("Saturn", "Aquarius", 10),
    ],
)
def test_moolatrikona(planet, sign, degree):
    result = get_planetary_dignity(planet, sign, degree)

    assert result["moolatrikona"] is True


@pytest.mark.parametrize(
    "planet, sign, degree",
    [
        ("Sun", "Libra", 10),
        ("Moon", "Scorpio", 10),
        ("Mars", "Cancer", 10),
        ("Mercury", "Pisces", 10),
        ("Jupiter", "Capricorn", 10),
        ("Venus", "Virgo", 10),
        ("Saturn", "Aries", 10),
    ],
)
def test_debilitation(planet, sign, degree):
    result = get_planetary_dignity(planet, sign, degree)

    assert result["sign_dignity"] == "Debilitation sign"


def test_own_sign():
    result = get_planetary_dignity("Mars", "Scorpio", 15)

    assert result["sign_dignity"] == "Own sign"


def test_invalid_planet():
    with pytest.raises(ValueError):
        get_planetary_dignity("Rahu", "Aries", 10)


def test_invalid_sign():
    with pytest.raises(ValueError):
        get_planetary_dignity("Sun", "Ophiuchus", 10)


@pytest.mark.parametrize("degree", [-1, 30, float("nan")])
def test_invalid_degree(degree):
    with pytest.raises(ValueError):
        get_planetary_dignity("Sun", "Aries", degree)
