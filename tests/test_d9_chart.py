
from engine.d9_chart import generate_d9_chart


def sample_planets():
    return {
        "Sun": {"longitude": 23.193980, "retrograde": False},
        "Moon": {"longitude": 66.410695, "retrograde": False},
        "Mars": {"longitude": 38.606644, "retrograde": False},
        "Mercury": {"longitude": 20.998534, "retrograde": False},
        "Jupiter": {"longitude": 23.816484, "retrograde": False},
        "Venus": {"longitude": 13.777070, "retrograde": False},
        "Saturn": {"longitude": 26.130771, "retrograde": False},
        "Rahu": {"longitude": 93.260744, "retrograde": True},
        "Ketu": {"longitude": 273.260744, "retrograde": True},
    }


def sample_ascendant():
    return {
        "sign": "Leo",
        "degree": 5.206341,
        "longitude": 125.206341
    }


def test_d9_chart_has_12_houses():
    chart = generate_d9_chart(sample_planets(), sample_ascendant())
    assert len(chart["houses"]) == 12


def test_d9_ascendant_is_taurus():
    chart = generate_d9_chart(sample_planets(), sample_ascendant())
    assert chart["ascendant"]["sign"] == "Taurus"


def test_d9_house_sign_sequence():
    chart = generate_d9_chart(sample_planets(), sample_ascendant())

    expected = [
        "Taurus", "Gemini", "Cancer", "Leo",
        "Virgo", "Libra", "Scorpio", "Sagittarius",
        "Capricorn", "Aquarius", "Pisces", "Aries"
    ]

    actual = [
        chart["houses"][house]["sign"]
        for house in range(1, 13)
    ]

    assert actual == expected


def test_d9_rahu_is_in_third_house():
    chart = generate_d9_chart(sample_planets(), sample_ascendant())

    rahu = chart["houses"][3]["planets"]

    assert any(planet["name"] == "Rahu" for planet in rahu)


def test_d9_ketu_is_in_ninth_house():
    chart = generate_d9_chart(sample_planets(), sample_ascendant())

    ketu = chart["houses"][9]["planets"]

    assert any(planet["name"] == "Ketu" for planet in ketu)


def test_all_nine_planets_are_assigned_once():
    chart = generate_d9_chart(sample_planets(), sample_ascendant())

    assigned = [
        planet["name"]
        for house in chart["houses"].values()
        for planet in house["planets"]
    ]

    assert len(assigned) == 9
    assert len(set(assigned)) == 9
