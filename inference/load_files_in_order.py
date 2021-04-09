import jetson.inference
import jetson.utils
import os
import time
import sys
import csv
import pandas

i = 0
image_in = "/home/james/camera_in/"
image_out = "/home/james/processed_input/detected_images/"

processed_image_in = []
my_Header = ["ClassID", "Confidence", "Left", "Top", "Right", "Bottom", "Width", "Height"]
#my_Biglist = [my_Header]



def Diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

def check_number_of_files(path):
    return(len(os.listdir(path)))

def get_names_of_files():
    for files in os.walk(image_in, topdown=True):
        return(files[2])

def get_names_of_new_files():
    for files in os.walk(image_in, topdown=True):
        print(files[2])
        to_be_processed=(Diff(processed_image_in,files[2]))
        return(to_be_processed)

def get_names_of_new_files_alt():
    for files in os.walk(image_in, topdown=True):
        all_files=(sorted(files[2]))
        new_files = all_files[+(len(processed_image_in)):]
        if len(new_files) != 0:
            print(new_files)
        print(f"The code has processed {len(processed_image_in)} files and has {len(new_files)} new files")
        return(new_files)

def detect_files(new_input_files):
    if len(new_input_files) == 0:
        print("No new files to process")
    else:
        for image_name in new_input_files:
            print("Processing",image_name)
            processed_image_in.append(f"{image_name}")
            detection(image_name)
            print("Image has been processed")
            
        
def detection(image_name):
    print("Detection")
    img_2_path = (f"{image_in}{image_name}")
    img_2 = jetson.utils.loadImage(img_2_path)
    net = jetson.inference.detectNet(argv=['--model=/home/james/jetson-inference/python/training/detection/ssd/models/whale_openimages/1/ssd-mobilenet.onnx', '--labels=/home/james/jetson-inference/python/training/detection/ssd/models/whale_openimages/1/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes', '--threshold=0.26'])
    detections = net.Detect(img_2, overlay="none")
    global i
    while os.path.exists(f"/home/james/processed_input/detected_images/anomaly_{i}.jpg"):
        i += 1
    image_out_path=str((f"{image_out}anomaly_{i}.jpg"))
    print("The detected image will be saves as ",image_out_path)
    #jetson.utils.saveImage(image_out_path,img_2)
    my_Biglist = [my_Header]
    for detection in detections:
		#print(detection)
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
        jetson.utils.saveImage(image_out_path,img_2)
        while os.path.exists(f"/home/james/processed_input/csv_files/anomaly_{i}.csv"):
            i += 1

        with open(f"/home/james/processed_input/csv_files/anomaly_{i}.csv", 'w', newline='') as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerows(my_Biglist)

while True:
    number_of_input_images=check_number_of_files(image_in)
    if number_of_input_images == 0:
        print("No Images in File")
        time.sleep(5)
    else:
        print(f"{number_of_input_images} images in file")
        new_input_files=get_names_of_new_files_alt()
        detect_files(new_input_files)
        time.sleep(5)
        
        
        
        
