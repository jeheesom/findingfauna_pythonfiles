# import os

# names =[]



# for file in os.listdir("/home/james/wfa_sorted_model/"):
#     print(file)
#     names.append(file)

# names=sorted(names)
# print(names)

# import os
# from pathlib import Path

# paths = sorted(Path("/home/james/wfa_sorted_model/").iterdir(), key=os.path.getmtime)
# print(paths)
# i=0
# for i in range(len(paths)):
#     a=paths[i]
#     print(a[+44:-16])

directory=("/home/james/wfa_sorted_model/100-199/")
import os 

os.chdir(directory)
names=sorted(filter(os.path.isfile, os.listdir('.')), key=os.path.getmtime)
for i in range(len(names)):
    a=names[i]
    print(a[+21:-16])