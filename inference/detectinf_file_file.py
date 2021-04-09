import jetson.inference
import jetson.utils
import numpy as np
import argparse
import sys
import os, os.path
import csv
import pandas

i=0
j=0

# while os.path.exists(f"/home/james/processed_input/processed_images/anomaly_{i}.jpg"):
# 	i += 1

#image_in = "/home/james/test_input/"
image_in = "/home/james/camera_in/"
image_out = (f"/home/james/processed_input/detected_images/anomaly_{i}.jpg")
#image_out = "/home/james/processed_input/processed_images/anomaly_%i.jpg"
#detect_data_out = "/home/james/processed_input/anomaly_%i.csv"
model_path = "ssd-mobilenet-v2"
custom_model_path = "/home/james/jetson-inference/python/training/detection/ssd/models/whale_openimages/1/ssd-mobilenet.onnx"
custom_labels_path = "/home/james/jetson-inference/python/training/detection/ssd/models/whale_openimages/1/labels.txt"

my_Header = ["ClassID", "Confidence", "Left", "Top", "Right", "Bottom", "Width", "Height"]
# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.")

parser.add_argument("input_URI", type=str, default=image_in, nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default=image_out, nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default=model_path, help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 


try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# load the object detection network
#net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)
net = jetson.inference.detectNet(argv=['--model=/home/james/jetson-inference/python/training/detection/ssd/models/whale_openimages/1/ssd-mobilenet.onnx', '--labels=/home/james/jetson-inference/python/training/detection/ssd/models/whale_openimages/1/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes', '--threshold=0.26'])

# create video sources & outputs
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
#output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv)

# process frames until the user exits
while True:
	path, dirs, files = next(os.walk("/home/james/test_input/"))
	file_count = len(files)
	#print("file count is ", file_count)
	while True:
		while os.path.exists(f"/home/james/processed_input/detected_images/anomaly_{i}.jpg"):
			i += 1
		
		image_out = (f"/home/james/processed_input/detected_images/anomaly_{i}.jpg")
		output_URI = (image_out)
		print(jetson.utils.videoOutput.Usage())
		output = jetson.utils.videoOutput(output_URI, argv=sys.argv)
		#output = jetson.utils.videoOutput(argv=['output_URI','--headless'])
		img = input.Capture()
		detections = net.Detect(img, overlay=opt.overlay)
		my_Biglist = [my_Header]
		for detection in detections:
			print(detection)
			my_ClassID = detection.ClassID
			my_Confidence = "%.2f" % detection.Confidence
			my_Left = "%.2f" % detection.Left
			my_Top = "%.2f" % detection.Top
			my_Right = "%.2f" % detection.Right
			my_Bottom = "%.2f" % detection.Bottom
			my_Width = "%.2f" % detection.Width
			my_Height = "%.2f" % detection.Height
			my_list = [my_ClassID, my_Confidence, my_Left, my_Top, my_Right, my_Bottom, my_Width, my_Height]
			my_Biglist.append(my_list)

		if len(detections) >= 1:

			output.Render(img)
			while os.path.exists(f"/home/james/processed_input/csv_files/anomaly_{i}.csv"):
				i += 1

			with open(f"/home/james/processed_input/csv_files/anomaly_{i}.csv", 'w', newline='') as new_file:
		 		csv_writer = csv.writer(new_file)
		 		csv_writer.writerows(my_Biglist)
		# update the title bar
		#output.SetStatus("{:s} | Network {:.0f} FPS".format(opt.network, net.GetNetworkFPS()))

		# print out performance info
		#net.PrintProfilerTimes()
		#exit on input/output EOS
		if not input.IsStreaming() or not output.IsStreaming():
			break

