import docx
import csv

def convert(input_file, output_file):
    doc = docx.Document(input_file)
    word_list = []
    row = []

    for paragraph in doc.paragraphs:
        words = paragraph.text.split()

        for word in words:
            if word.lower() == "km²" or word.lower() == "-":
                if row:
                    row.append(word)
                    word_list.append(row)
                    row = []
                    continue

            row.append(word)

    if row:
        word_list.append(row)

    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for row in word_list:
            writer.writerow(row)


input_file = 'miasta.docx'
output_file = 'miasta2.csv'

convert(input_file, output_file)