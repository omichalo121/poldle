from cs50 import SQL
import csv
import json

db = SQL("sqlite:///miasta.db")
db.execute("DELETE FROM miasta")
with open('kopia.csv', 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)
    for row in rows:
        city_data = json.loads(row[0].replace("'", '"'))
        db.execute(
            "INSERT INTO miasta (id, nazwa, powiat, wojewodztwo, ludnosc, powierzchnia, szerokosc, dlugosc) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            city_data['id'], city_data['nazwa'], city_data['powiat'], city_data['wojewodztwo'], city_data['ludnosc'],
            city_data['powierzchnia'], city_data['szerokosc'], city_data['dlugosc']
        )