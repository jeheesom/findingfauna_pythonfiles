import csv
import math
import os
import time
from PIL import Image 
import jetson.inference
import jetson.utils
from datetime import datetime


now = datetime.now()
dt_string = str(now.strftime("%d:%m:%Y %H:%M:%S"))
mydate=(dt_string[:-9])

mytime=(dt_string[+11:])
dateandtime=str(mydate+"_"+mytime)
outputfile_path=(f"/home/james/processed_input/classification_{dateandtime}.csv")
output_header=["Image_Name","Class_Name","Class_ID","Confidence"]

with open(outputfile_path, 'w') as new_file:
    csv_writer = csv.writer(new_file)
    csv_writer.writerow(output_header)


path_to_csv="/home/james/processed_input/csv_files/"
path_to_images="/home/james/processed_input/detected_images/"
path_to_cropped_output="/home/james/processed_input/cropped_images/"
files_processed=[]

classify_input="/home/james/processed_input/cropped_images/anomaly_1_0.jpg"
classifymodelpath="/home/james/jetson-inference/python/training/classification/models/class_hump_blue/"
classifymodelname="resnet18.onnx"
classifylabelspath="/home/james/jetson-inference/python/training/classification/models/class_hump_blue/"
labelsname="labels.txt"

image_resolution=[1280, 720]
drone_height_m = float(25)
size_scaler = float(0.822)
average_whale_size = float(24)
whale_min=float("%.1f" % (average_whale_size * 0.8))
whale_max=float("%.1f" % (average_whale_size * 1.2))
fov_width = "%.1f" % (image_resolution[0] * drone_height_m * size_scaler / 1000)
fov_height = "%.1f" % (image_resolution[1] * drone_height_m * size_scaler / 1000)

files_in=os.listdir(path_to_csv)

def Diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

def Crop_Image(path,Left,Top,Right,Bottom,counter):
    
    name=(path[+44:-4])
    im = Image.open(f"{path}")
    im_cropped = im.crop((Left,Top,Right,Bottom))
    print("counter= ",counter)
    im_cropped.save(f"{path_to_cropped_output}{name}_{counter}.jpg")
    return(f"{path_to_cropped_output}{name}_{counter}.jpg")
    
def Surrounding_Images(path):
    print(path)
    dir_name=(path[:-13])
    dir_length=len(os.listdir(dir_name))

    name_int=int(path[+52:-4])
    pre_name=str(name_int-1)
    post_name=str(name_int+1)

    pre_path=(path[:52]+(pre_name)+".jpg")
    post_path=(path[:52]+(post_name)+".jpg")


    if name_int == 0 or name_int == dir_length-1:
        #print("Surrounding images do not contain whales")
        return False
    else:
        currentfile_time=os.path.getmtime(path)
        prefile_time=os.path.getmtime(pre_path)
        postfile_time=os.path.getmtime(post_path)
        pre_dif=float("%.1f" % (currentfile_time-prefile_time))
        pro_dif=float("%.1f" % (postfile_time-currentfile_time))

        if pre_dif <=5 and pro_dif <=5:
            #print("This is definatly a whale")
            return True
        else:
            #print("This probabaly isnt a whale")
            return False

def Classify_Images(path):
    img_name=str(path[+43:])
    img = jetson.utils.loadImage(path)
    net = jetson.inference.imageNet(argv=[f'--model={classifymodelpath}{classifymodelname}', f'--labels={classifylabelspath}{labelsname}', '--input-blob=input_0', '--output-blob=output_0'])
    class_idx, confidence = net.Classify(img)
    class_desc = net.GetClassDesc(class_idx)
    class_list=[img_name,class_desc, str(class_idx), str("%.3f" % (confidence))]
    print("class list",class_list)

    with open(f"{outputfile_path}", 'a') as output:
        csv_writer = csv.writer(output)
        csv_writer.writerow(class_list)

def Scale_Check(current):
    with open(f"{path_to_csv}{current}", 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        global counter
        counter = 0
        for line in csv_reader:
            width_pixels=float(line[6])
            height_pixels=float(line[7])
            c=float("%.1f" % math.sqrt((height_pixels ** 2)+(width_pixels ** 2)))
            width_meters =float("%.2f" % (width_pixels * drone_height_m * size_scaler / 1000))
            height_meters =float("%.2f" % (height_pixels * drone_height_m * size_scaler / 1000))
            c_meters = float("%.2f" % (c * drone_height_m * size_scaler / 1000))
            width_and_height = [width_meters, height_meters]
            min_length_m =float(max(width_and_height))
            max_length_m =float(c_meters)

            path_to_current_image = path_to_images+current[:-3]+"jpg"

            my_Left=int(float(line[2]))
            my_Top=int(float(line[3]))
            my_Right=int(float(line[4]))
            my_Bottom=int(float(line[5]))
            
            if min_length_m >= whale_min and min_length_m <= whale_max:
                #return True,path_to_current_image,my_Left,my_Top,my_Right,my_Bottom
                scale_check_2=True
            elif max_length_m >= whale_min and max_length_m <= whale_max:
                #return True,path_to_current_image,my_Left,my_Top,my_Right,my_Bottom
                scale_check_2=True
            else:
                #return False,path_to_current_image,my_Left,my_Top,my_Right,my_Bottom
                scale_check_2=True

            if scale_check_2==True:
                print("The detection is the correct size")
                print("Counter is ",counter)
                are_there_whales=Surrounding_Images(path_to_current_image)
                if are_there_whales==True:
                    print("There are whales in the surrounding images")
                    print("Cropping image")
                    cropped_img_path=Crop_Image(path_to_current_image,my_Left,my_Top,my_Right,my_Bottom,counter)
                    Classify_Images(cropped_img_path)
                else:
                    print("There are not whales in the surrounding images")
            else:
                print("The detection is not the correct size")
            counter += 1



while True:
    time.sleep(2)
    files_in=os.listdir(path_to_csv)
    to_be_processed=(sorted(Diff(files_in, files_processed)))

    for x in range(len(to_be_processed)):
        files_processed.append(to_be_processed[x])
        current=to_be_processed[x]
        #scale_check_result,path_to_current_image,my_Left,my_Top,my_Right,my_Bottom=Scale_Check(current)
        Scale_Check(current)
        # print("Is the checked detection the correct size to be a whale ", scale_check_result)
        # if scale_check_result == True:
        #     print("Detection is the size of a whale")
        #     #are_there_whales=Surrounding_Images(path_to_current_image)
        #     Surrounding_Images(path_to_current_image)
        #     print("Are there whales",are_there_whales)
        #     print("================")
            # if are_there_whales ==True:
            #     cropped_img_path=Crop_Image(path_to_current_image,my_Left,my_Top,my_Right,my_Bottom,counter)
            #     Classify_Images(cropped_img_path)
            # else:
            #     print("There are no surrounding whales")
            #     print("============")
            #counter += 1

                






