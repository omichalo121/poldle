from cs50 import SQL
import csv

db = SQL("sqlite:///miasta.db")
db.execute("DELETE FROM miasta")
with open('kopia.csv', 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)
    for row in rows:
        row = eval(row[0])
        db.execute("INSERT INTO miasta (id, nazwa, powiat, wojewodztwo, ludnosc, powierzchnia, szerokosc, dlugosc) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", row['id'], row['nazwa'], row['powiat'], row['wojewodztwo'], row['ludnosc'], row['powierzchnia'], row['szerokosc'], row['dlugosc'])