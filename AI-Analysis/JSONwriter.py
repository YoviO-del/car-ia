import csv

name = ""
with open('listings.csv','r') as file:
    csv_reader = csv.DictReader(file)

    # csv reader is an object so you must loop through it
    for row in csv_reader:
        name = (row['firstName'])
        break
print(f"Name of the linkedin user is: {name}")