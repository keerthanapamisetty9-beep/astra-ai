
NAKSHATRAS = [
    "Ashwini", "Bharani", "Krittika", "Rohini",
    "Mrigashira", "Ardra", "Punarvasu", "Pushya",
    "Ashlesha", "Magha", "Purva Phalguni",
    "Uttara Phalguni", "Hasta", "Chitra",
    "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha",
    "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada",
    "Revati"
]

NAKSHATRA_SIZE = 360 / 27
PADA_SIZE = NAKSHATRA_SIZE / 4


def calculate_nakshatra(longitude):
    longitude = longitude % 360

    nakshatra_index = int(longitude / NAKSHATRA_SIZE)

    position_in_nakshatra = (
        longitude - nakshatra_index * NAKSHATRA_SIZE
    )

    pada = int(position_in_nakshatra / PADA_SIZE) + 1

    return {
        "nakshatra": NAKSHATRAS[nakshatra_index],
        "pada": pada,
        "longitude": longitude
    }
