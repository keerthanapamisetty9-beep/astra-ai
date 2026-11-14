
import swisseph as swe

from engine.nakshatra import calculate_nakshatra
from engine.planetary_positions import calculate_planets
from engine.d1_chart import calculate_d1_chart


# ==========================================
# NAKSHATRA TESTS
# ==========================================

def test_moon_nakshatra():
    result = calculate_nakshatra(66.410823)

    assert result["nakshatra"] == "Mrigashira"
    assert result["pada"] == 4


def test_lagna_nakshatra():
    result = calculate_nakshatra(125.206341)

    assert result["nakshatra"] == "Magha"
    assert result["pada"] == 2


def test_zero_longitude():
    result = calculate_nakshatra(0)

    assert result["nakshatra"] == "Ashwini"
    assert result["pada"] == 1


def test_360_degree_longitude():
    result = calculate_nakshatra(360)

    assert result["nakshatra"] == "Ashwini"
    assert result["pada"] == 1


# ==========================================
# PLANETARY POSITION TESTS
# ==========================================

def test_all_planets_are_present():
    jd = swe.julday(2000, 1, 1, 12.0)

    result = calculate_planets(jd)

    expected = [
        "Sun", "Moon", "Mars", "Mercury",
        "Jupiter", "Venus", "Saturn",
        "Rahu", "Ketu"
    ]

    for planet in expected:
        assert planet in result


def test_planet_longitudes_are_valid():
    jd = swe.julday(2000, 1, 1, 12.0)

    result = calculate_planets(jd)

    valid_signs = [
        "Aries", "Taurus", "Gemini", "Cancer",
        "Leo", "Virgo", "Libra", "Scorpio",
        "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]

    for planet, data in result.items():
        assert 0 <= data["longitude"] < 360
        assert data["sign"] in valid_signs


def test_rahu_and_ketu_are_opposite():
    jd = swe.julday(2000, 1, 1, 12.0)

    result = calculate_planets(jd)

    difference = (
        result["Ketu"]["longitude"]
        - result["Rahu"]["longitude"]
    ) % 360

    assert abs(difference - 180) < 0.000001


def test_ephemeris_date_range():
    test_dates = [
        (1800, 1, 1),
        (1900, 1, 1),
        (2000, 1, 1),
        (2100, 1, 1),
        (2200, 12, 31),
    ]

    for year, month, day in test_dates:
        jd = swe.julday(year, month, day, 12.0)

        result = calculate_planets(jd)

        assert len(result) == 9

        for planet, details in result.items():
            assert 0 <= details["longitude"] < 360


# ==========================================
# D1 RASHI CHART TEST DATA
# ==========================================

def create_test_planets():
    return {
        "Sun": {
            "sign": "Aries",
            "degree": 23.193980,
            "retrograde": False
        },
        "Moon": {
            "sign": "Gemini",
            "degree": 6.410695,
            "retrograde": False
        },
        "Mars": {
            "sign": "Taurus",
            "degree": 8.606644,
            "retrograde": False
        },
        "Mercury": {
            "sign": "Aries",
            "degree": 20.998534,
            "retrograde": False
        },
        "Jupiter": {
            "sign": "Aries",
            "degree": 23.816484,
            "retrograde": False
        },
        "Venus": {
            "sign": "Aries",
            "degree": 13.777070,
            "retrograde": False
        },
        "Saturn": {
            "sign": "Aries",
            "degree": 26.130771,
            "retrograde": False
        },
        "Rahu": {
            "sign": "Cancer",
            "degree": 3.260744,
            "retrograde": True
        },
        "Ketu": {
            "sign": "Capricorn",
            "degree": 3.260744,
            "retrograde": True
        }
    }


def create_test_ascendant():
    return {
        "sign": "Leo",
        "degree": 5.206341,
        "longitude": 125.206341
    }


# ==========================================
# D1 RASHI CHART TESTS
# ==========================================

def test_d1_chart_has_12_houses():
    chart = calculate_d1_chart(
        create_test_planets(),
        create_test_ascendant()
    )

    assert len(chart["houses"]) == 12


def test_d1_ascendant_is_first_house():
    chart = calculate_d1_chart(
        create_test_planets(),
        create_test_ascendant()
    )

    assert chart["ascendant"] == "Leo"
    assert chart["houses"][1]["sign"] == "Leo"


def test_d1_house_sign_sequence():
    chart = calculate_d1_chart(
        create_test_planets(),
        create_test_ascendant()
    )

    assert chart["houses"][1]["sign"] == "Leo"
    assert chart["houses"][6]["sign"] == "Capricorn"
    assert chart["houses"][9]["sign"] == "Aries"
    assert chart["houses"][12]["sign"] == "Cancer"


def test_d1_rahu_and_ketu_placement():
    chart = calculate_d1_chart(
        create_test_planets(),
        create_test_ascendant()
    )

    house_6_planets = [
        planet["name"]
        for planet in chart["houses"][6]["planets"]
    ]

    house_12_planets = [
        planet["name"]
        for planet in chart["houses"][12]["planets"]
    ]

    assert "Ketu" in house_6_planets
    assert "Rahu" in house_12_planets


def test_d1_all_nine_planets_assigned_once():
    chart = calculate_d1_chart(
        create_test_planets(),
        create_test_ascendant()
    )

    assigned_planets = []

    for house in chart["houses"].values():
        for planet in house["planets"]:
            assigned_planets.append(planet["name"])

    assert len(assigned_planets) == 9
    assert len(set(assigned_planets)) == 9

    assert set(assigned_planets) == set(create_test_planets())


from engine.navamsa import calculate_navamsa_position


def test_navamsa_aries_first_division():
    result = calculate_navamsa_position(0)

    assert result["original_sign"] == "Aries"
    assert result["navamsa_number"] == 1
    assert result["sign"] == "Aries"


def test_navamsa_aries_seventh_division():
    result = calculate_navamsa_position(23.193980)

    assert result["original_sign"] == "Aries"
    assert result["navamsa_number"] == 7
    assert result["sign"] == "Libra"


def test_navamsa_fixed_sign_start():
    # Taurus is fixed; its first Navamsa starts in Capricorn.
    result = calculate_navamsa_position(30)

    assert result["original_sign"] == "Taurus"
    assert result["navamsa_number"] == 1
    assert result["sign"] == "Capricorn"


def test_navamsa_dual_sign_start():
    # Gemini is dual; its first Navamsa starts in Libra.
    result = calculate_navamsa_position(60)

    assert result["original_sign"] == "Gemini"
    assert result["navamsa_number"] == 1
    assert result["sign"] == "Libra"


def test_navamsa_longitude_is_valid():
    test_longitudes = [
        0, 23.193980, 66.410695,
        125.206341, 180, 270, 359.999
    ]

    for longitude in test_longitudes:
        result = calculate_navamsa_position(longitude)

        assert 0 <= result["longitude"] < 360
        assert 0 <= result["degree"] < 30
        assert 1 <= result["navamsa_number"] <= 9
