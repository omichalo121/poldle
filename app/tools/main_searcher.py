from cs50 import SQL
import random
import sys
import math

db = SQL("sqlite:///miasta.db")
idOTD = random.randint(1, 979)

# Wybierz random miasto dnia

def main():

    info = []
    info = db.execute("SELECT * FROM miasta WHERE id = ?", idOTD)
    cityOTD_info = []

    longOTD = info[0]['dlugosc']
    latOTD = info[0]['szerokosc']
    cityOTD_info.append(info[0]['nazwa'])
    cityOTD_info.append(info[0]['powiat'])
    cityOTD_info.append(info[0]['wojewodztwo'])
    cityOTD_info.append(info[0]['ludnosc'])
    cityOTD_info.append(info[0]['powierzchnia'])
    print(info[0]['nazwa'])
    city_info = get_name()

    search = main_engine(longOTD, city_info[5], latOTD, city_info[6])
    angle = calculate_angle(latOTD, longOTD, city_info[6], city_info[5])
    dir = angle_to_direction(angle)

    # city of the day
    print(cityOTD_info)

    # given city
    print(city_info[:5])

    # way and distance
    print(f"Odległość: {search}, Kierunek: {dir}")


def get_name():

    CI = []
    count = 0
    while True:
        city = input("Podaj nazwę miasta: ")
        city = city.title()
        for znak in city:
            if znak == ' ' or znak.isalpha() or znak == '-':
                count += 1


        if count == len(city):
            check = db.execute("SELECT * FROM miasta where nazwa = ?", city)
            if len(check) > 0:
                CI.append(check[0]['nazwa'])
                CI.append(check[0]['powiat'])
                CI.append(check[0]['wojewodztwo'])
                CI.append(check[0]['ludnosc'])
                CI.append(check[0]['powierzchnia'])
                CI.append(check[0]['dlugosc'])
                CI.append(check[0]['szerokosc'])
                return CI
            else:
                print("Nie ma takiego miasta.")
                continue
        else:
            print("Niepoprawna nazwa miasta.")
            continue


def main_engine(longDAY, longGIVEN, latDAY, latGIVEN):

    diff = []
    longDAY = float(longDAY)
    longGIVEN = float(longGIVEN)
    latDAY = float(latDAY)
    latGIVEN = float(latGIVEN)
    diff.append(latDAY - latGIVEN)
    diff.append(longDAY - longGIVEN)


    # distance calculator
    R = 6371
    lat2_rad = math.radians(latDAY)
    long2_rad = math.radians(longDAY)
    lat1_rad = math.radians(latGIVEN)
    long1_rad = math.radians(longGIVEN)

    dlat = lat2_rad - lat1_rad
    dlon = long2_rad - long1_rad

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return distance


def calculate_angle(lat2, lon2, lat1, lon1):
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Calculate the differences in coordinates
    delta_lon = lon2_rad - lon1_rad

    # Calculate the angle using the haversine formula
    y = math.sin(delta_lon) * math.cos(lat2_rad)
    x = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(delta_lon)
    angle_rad = math.atan2(y, x)

    # Convert radians to degrees
    angle_deg = math.degrees(angle_rad)

    # Ensure the angle is within the range of 0 to 360 degrees
    angle_deg = (angle_deg + 360) % 360

    return angle_deg


def angle_to_direction(angle):

    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']
    index = round(angle / 45) % 8
    return directions[index]

main()