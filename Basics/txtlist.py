import os

outputfile = "/home/james/jetson-inference/python/training/detection/ssd/data/smallpenguin/inventory.txt"
folder ="/home/james/jetson-inference/python/training/detection/ssd/data/smallpenguin/JPEGImages"
exclude =['.tmp']
pathsep ="/"

with open(outputfile, "w") as txtfile:
	for path,dirs,files in os.walk(folder):
		#sep = "\n---------- " + path.split(pathsep)[len(path.split(pathsep))-1] + " ----------"
		#print(sep)
		#txtfile.write("%s\n" % sep)

		for fn in sorted(files):
			if not any(x in fn for x in exclude):
				filename = os.path.splitext(fn)[0]
				
				print(filename)
				txtfile.write("%s\n" % filename)

txtfile.close()