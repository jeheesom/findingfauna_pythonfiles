import os
import time
path_to_csv="/home/james/processed_input/csv_files/"
files_processed=[]
# def files(path):
#     for file in os.listdir(path):
#         if os.path.isfile(os.path.join(path, file)):
#             yield file

# for file in files(path):
#     print(file)

files_in=os.listdir(path_to_csv)

def Diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

while True:
    time.sleep(2)
    files_in=os.listdir(path_to_csv)
    to_be_processed=(Diff(files_in, files_processed))

    for x in range(len(to_be_processed)):
        

        files_processed.append(to_be_processed[x])
    # for x in range(len(files_in)):
        
    #     print(x)



# def Diff(li1, li2):
#     return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

#print(Diff(files_in, files_processed))
        