import csv
import os

my_list=["1", "2", "3"]

i=0

for x in range(0, 5):
    while os.path.exists(f"/home/james/processed_input/names_{i}.csv"):
        i += 1

    with open(f"/home/james/processed_input/names_{i}.csv", 'w', newline='') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerows(my_list)