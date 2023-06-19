import csv


with open('kopia.csv', 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)
    for row in rows:
        print(row[5])