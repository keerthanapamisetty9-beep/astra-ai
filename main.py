
from engine.planetary_positions import calculate_planets
from engine.ascendant import calculate_ascendant
from engine.nakshatra import calculate_nakshatra
from engine.d1_chart import calculate_d1_chart
from engine.d9_chart import generate_d9_chart

from engine.transits import (
    calculate_transits,
    calculate_transit_houses
)


from datetime import datetime

from engine.vimshottari import (
    calculate_birth_dasha,
    generate_mahadasha_timeline,
    find_current_dasha
)

# ==========================================
# ASTRA AI - TEST BIRTH DETAILS
# ==========================================

# Date: 7 May 2000
# Time: 1:10 PM IST
# Location: Anantapur, Andhra Pradesh

# Converted to UTC
YEAR = 2000
MONTH = 5
DAY = 7

HOUR_UTC = 7
MINUTE_UTC = 40

LATITUDE = 14.6819
LONGITUDE = 77.6006


# ==========================================
# STEP 1 - CALCULATE JULIAN DAY
# ==========================================

import swisseph as swe

julian_day = swe.julday(
    YEAR,
    MONTH,
    DAY,
    HOUR_UTC + MINUTE_UTC / 60.0
)


# ==========================================
# STEP 2 - PLANETARY POSITIONS
# ==========================================

planets = calculate_planets(julian_day)

print("\n===== ASTRA AI - PLANETARY POSITIONS =====")

for planet_name, data in planets.items():

    print(f"\n{planet_name}")
    print(f"Sign: {data['sign']}")
    print(f"Degree: {data['degree']:.6f}")
    print(f"Longitude: {data['longitude']:.6f}")
    print(f"Speed: {data['speed']:.8f}")
    print(f"Retrograde: {data['retrograde']}")


# ==========================================
# STEP 3 - ASCENDANT / LAGNA
# ==========================================

ascendant = calculate_ascendant(
    julian_day,
    LATITUDE,
    LONGITUDE
)

print("\n===== ASTRA AI - ASCENDANT =====")

print(f"Lagna: {ascendant['sign']}")
print(f"Degree: {ascendant['degree']:.6f}")
print(f"Longitude: {ascendant['longitude']:.6f}")


# ==========================================
# STEP 4 - NAKSHATRA ANALYSIS
# ==========================================

print("\n===== ASTRA AI - NAKSHATRA ANALYSIS =====")

moon_nakshatra = calculate_nakshatra(
    planets["Moon"]["longitude"]
)

lagna_nakshatra = calculate_nakshatra(
    ascendant["longitude"]
)

print("\nMoon:")
print(f"Nakshatra: {moon_nakshatra['nakshatra']}")
print(f"pada: {moon_nakshatra['pada']}")
print(f"Longitude: {moon_nakshatra['longitude']:.6f}")

print("\nLagna:")
print(f"Nakshatra: {lagna_nakshatra['nakshatra']}")
print(f"Pada: {lagna_nakshatra['pada']}")
print(f"Longitude: {lagna_nakshatra['longitude']:.6f}")


# ==========================================
# STEP 5 - D1 RASHI CHART
# ==========================================

d1_chart = calculate_d1_chart(
    planets,
    ascendant
)

print("\n===== ASTRA AI - D1 RASHI CHART =====")

print(
    f"Ascendant: {d1_chart['ascendant']} "
    f"{d1_chart['ascendant_degree']:.6f}°"
)

print(f"House System: {d1_chart['house_system']}")

for house_number, house_data in d1_chart["houses"].items():

    print(
        f"\nHouse {house_number} - {house_data['sign']}"
    )

    if house_data["planets"]:

        for planet in house_data["planets"]:

            print(
                f"  {planet['name']} - "
                f"{planet['degree']:.6f}° "
                f"(Retrograde: {planet['retrograde']})"
            )

    else:
        print("  No planets")


print("\n===== ASTRA AI - CALCULATION COMPLETE =====")

# ==========================================
# STEP 6 - D9 NAVAMSA CHART
# ==========================================

d9_chart = generate_d9_chart(
    planets,
    ascendant
)

print("\n===== ASTRA AI - D9 NAVAMSA CHART =====")

print(
    f"Ascendant: {d9_chart['ascendant']['sign']} "
    f"{d9_chart['ascendant']['degree']:.6f}°"
)

print(f"House System: {d9_chart['house_system']}")

for house_number, house_data in d9_chart["houses"].items():
    print(f"\nHouse {house_number} - {house_data['sign']}")

    if house_data["planets"]:
        for planet in house_data["planets"]:
            print(
                f"  {planet['name']} - "
                f"{planet['degree']:.6f}° "
                f"(Retrograde: {planet['retrograde']})"
            )
    else:
        print("  No planets")



# ==========================================
# STEP 7 - VIMSHOTTARI DASHA
# ==========================================

birth_datetime = datetime(2000, 5, 7, 13, 10)

# Calculate birth Mahadasha
birth_dasha = calculate_birth_dasha(
    planets["Moon"]["longitude"]
)

# Generate Mahadasha timeline
mahadasha_timeline = generate_mahadasha_timeline(
    birth_datetime,
    birth_dasha
)

print("\n===== ASTRA AI - VIMSHOTTARI DASHA =====")

print("\nBirth Mahadasha:")
print(f"Planet: {birth_dasha['nakshatra_lord']}")
print(
    f"Balance: {birth_dasha['balance_years']:.4f} years"
)

print("\nMahadasha Timeline:")

for period in mahadasha_timeline:
    print(
        f"{period['planet']}: "
        f"{period['start'].date()} - "
        f"{period['end'].date()}"
    )

# Find current Dasha for test date
target_date = datetime(2026, 11, 13)

current_dasha = find_current_dasha(
    mahadasha_timeline,
    target_date
)

print("\nCurrent Dasha:")

if current_dasha:
    print(f"Mahadasha: {current_dasha['mahadasha']}")
    print(f"Antardasha: {current_dasha['antardasha']}")
    print(
        f"Antardasha End: "
        f"{current_dasha['antardasha_end'].date()}"
    )
else:
    print("No active Dasha found for this date.")


# ==========================================
# STEP 8 - GOCHAR / PLANETARY TRANSITS
# ==========================================

# Transit date: 13 November 2026
# Transit time: 12:00 UTC

TRANSIT_YEAR = 2026
TRANSIT_MONTH = 11
TRANSIT_DAY = 13
TRANSIT_HOUR_UTC = 12

transit_julian_day = swe.julday(
    TRANSIT_YEAR,
    TRANSIT_MONTH,
    TRANSIT_DAY,
    TRANSIT_HOUR_UTC
)

# Calculate transit planetary positions
transits = calculate_transits(transit_julian_day)

# Calculate houses from natal Moon and Lagna
transit_houses = calculate_transit_houses(
    transits["planets"],
    planets["Moon"]["sign"],
    ascendant["sign"]
)

print("\n===== ASTRA AI - GOCHAR TRANSITS =====")

print(f"Transit Date: {TRANSIT_YEAR}-{TRANSIT_MONTH:02d}-{TRANSIT_DAY:02d}")
print("Zodiac: Sidereal")
print("Ayanamsa: Lahiri")

print(f"Natal Moon Sign: {planets['Moon']['sign']}")
print(f"Natal Lagna: {ascendant['sign']}")

for planet_name, data in transit_houses.items():

    print(f"\n{planet_name}")
    print(f"Transit Sign: {data['sign']}")
    print(f"Degree: {data['degree']:.4f}°")
    print(f"House from Moon: {data['house_from_moon']}")
    print(f"House from Lagna: {data['house_from_lagna']}")
