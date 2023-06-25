import requests
import csv

# funkcja pozyskiwania współrzędnych geograficzncyh
def get_coordinates(place):
    url = f"https://nominatim.openstreetmap.org/search?q={place}&format=json"
    response = requests.get(url)
    data = response.json()
    if len(data) > 0:
        latitude = float(data[0]['lat'])
        latitude = round(latitude, 5)
        longitude = float(data[0]['lon'])
        longitude = round(longitude, 5)
        return latitude, longitude
    else:
        return None
    # puste listy do nadpisania
geog = []
miasta = []

# otwóz plik, stwóz listę miast
with open('miasta.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        miasta.append(row[1])
c = 1
# dla każdego miasta znajdź współrzędne i wrzuć je do listy
for miejsce in miasta:
    geography = {}
    coordinates = get_coordinates(miejsce)
    if coordinates:
        latitude, longitude = coordinates
        geography['miasto'] = miejsce
        geography['latitude'] = latitude
        geography['longitude'] = longitude
        geog.append(geography)
        print(f"LP.: {c}, Nazwa: {miejsce}, Współrzędne: {latitude}, {longitude}")
        c += 1
    else:
        print(f"Nie można znaleźć współrzędnych dla {miejsce}")

with open('miasta.csv', 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)

    for row in rows:
        miasto = row[1]
        for miejsce in geog:
            if miejsce['miasto'] == miasto:
                row.append(miejsce['longitude'])
                row.append(miejsce['latitude'])
                break

with open('geograf.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)