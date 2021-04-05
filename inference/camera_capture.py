import jetson.inference
import jetson.utils
import numpy as np
import argparse
import sys
import os, os.path
import time


#image_in = "/home/james/test_input/"
#image_out = "/home/james/camera_in/image_%i.jpg"
image_out = "/home/james/camera_in/image_%i.jpg"
# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.")

parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default=image_out, nargs='?', help="URI of the output stream")

try:
	opt = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv)

# process frames until the user exits
while True:
	while True:
		# capture the next image
		img = input.Capture()
		output.Render(img)
		time.sleep(2)

		# exit on input/output EOS
		if not input.IsStreaming() or not output.IsStreaming():
			break