"""
Planetary conjunction detection for a Whole Sign D1 chart.
"""


def get_angular_distance(degree1, degree2):
    """Return the shortest angular distance between two zodiac longitudes."""

    if not isinstance(degree1, (int, float)) or isinstance(degree1, bool):
        raise ValueError("Planetary degrees must be numeric.")

    if not isinstance(degree2, (int, float)) or isinstance(degree2, bool):
        raise ValueError("Planetary degrees must be numeric.")

    if not 0 <= degree1 < 360 or not 0 <= degree2 < 360:
        raise ValueError("Planetary degrees must be between 0 and 360.")

    difference = abs(degree1 - degree2)

    return min(difference, 360 - difference)


def get_chart_conjunctions(chart):
    """
    Identify planets occupying the same house in a Whole Sign D1 chart.

    Returns every pair of planets sharing a house, along with
    their degrees and angular distance.
    """

    if not isinstance(chart, dict) or "houses" not in chart:
        raise ValueError("Invalid D1 chart structure.")

    conjunctions = []

    for house_number in range(1, 13):
        if house_number not in chart["houses"]:
            raise ValueError(f"House {house_number} is missing from chart.")

        house_data = chart["houses"][house_number]

        if not isinstance(house_data, dict):
            raise ValueError("Invalid house data.")

        sign = house_data.get("sign")
        planets = house_data.get("planets", [])

        for i in range(len(planets)):
            for j in range(i + 1, len(planets)):
                planet1 = planets[i]
                planet2 = planets[j]

                degree1 = planet1["degree"]
                degree2 = planet2["degree"]

                conjunctions.append({
                    "house": house_number,
                    "sign": sign,
                    "planet1": planet1["name"],
                    "planet2": planet2["name"],
                    "planet1_degree": degree1,
                    "planet2_degree": degree2,
                    "angular_distance": get_angular_distance(
                        degree1, degree2
                    ),
                })

    return conjunctions
