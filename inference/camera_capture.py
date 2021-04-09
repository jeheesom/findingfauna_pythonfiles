import jetson.inference
import jetson.utils
import os, os.path
import time

i = 0

image_out = "/home/james/camera_in/"
input = jetson.utils.videoSource()

while True:	
	img = input.Capture()
	while os.path.exists(f"{image_out}image_{i}.jpg"):
		i += 1
	image_out_path=str((f"{image_out}image_{i}.jpg"))	
	jetson.utils.saveImage(image_out_path,img)
	time.sleep(2)

	
