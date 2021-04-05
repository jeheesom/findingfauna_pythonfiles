import csv

#reader

# with open('/home/james/processed_input/data.csv', 'r') as csv_file:
#     csv_reader = csv.reader(csv_file)
#     #next(csv_reader)
#     for line in csv_reader:
#         print(line)
#         print(line[2])

#reads then writes

# with open('/home/james/processed_input/data.csv', 'r') as csv_file:
#     csv_reader = csv.reader(csv_file)

#     with open('/home/james/processed_input/mew_data.csv', 'w') as new_file:
#         csv_writer = csv.writer(new_file, delimiter=',')

#         for line in csv_reader:
#             csv_writer.writerow(line)

#dictionary reader
# with open('/home/james/processed_input/data.csv', 'r') as csv_file:
#      csv_reader = csv.DictReader(csv_file)

#      for line in csv_reader:
#          print(line['Month'])

with open('/home/james/processed_input/data.csv', 'r') as csv_file:
     csv_reader = csv.DictReader(csv_file)

     with open('/home/james/processed_input/mew_data.csv', 'w') as new_file:
        fieldnames=['Name', 'Department', 'Month']
        csv_writer = csv.DictWriter(new_file,fieldnames=fieldnames, delimiter=',')
        csv_writer.writeheader()
        for line in csv_reader:
            csv_writer.writerow(line)