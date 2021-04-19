import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
from PIL import Image
from datetime import datetime

# defining global variable path
image_path = "/home/james/whale_for_preprcessing/input/"
image_path_length=int(len(image_path))

def MakeDirs():
    now = datetime.now()
    dt_string = str(now.strftime("%d:%m:%Y %H:%M:%S"))
    mydate=(dt_string[:-9])

    mytime=(dt_string[+11:])
    dateandtime=str(mydate+"_"+mytime)
    global outputfile_path
    outputfile_path=(f"/home/james/whale_for_preprcessing/output_{dateandtime}")
    os.makedirs(outputfile_path)
    os.makedirs(f"{outputfile_path}/no_noise")
    global no_noise_path
    no_noise_path=(f"{outputfile_path}/no_noise/")
    os.makedirs(f"{outputfile_path}/segmented")
    global segmented_path
    segmented_path=(f"{outputfile_path}/segmented/")
    os.makedirs(f"{outputfile_path}/segmented_background")
    global segmented_background_path
    segmented_background_path=(f"{outputfile_path}/segmented_background/")
    os.makedirs(f"{outputfile_path}/markers")
    global markers_path
    markers_path=(f"{outputfile_path}/markers/")
    os.makedirs(f"{outputfile_path}/grey")
    global grey_path
    grey_path=(f"{outputfile_path}/grey/")
    os.makedirs(f"{outputfile_path}/adaptive_threshold")
    global adapthresh_path
    adapthresh_path=(f"{outputfile_path}/adaptive_threshold/")

def loadImages(path):
    # Put files into lists and return them as one list of size 4
    image_files = sorted([os.path.join(path, file)
         for file in os.listdir(path) if      file.endswith('.jpg')])
 
    return image_files

def display(a, b, title1 = "Original", title2 = "Edited"):
    plt.subplot(121), plt.imshow(a), plt.title(title1)
    plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(b), plt.title(title2)
    plt.xticks([]), plt.yticks([])
    plt.show()

# Display one image
def display_one(a, title1 = "Original"):
    plt.imshow(a), plt.title(title1)
    plt.show()

def processing(data):
    print(data)
    file_num=int(len(data))
    # Reading 3 images to work
    img = [cv2.imread(i, cv2.IMREAD_UNCHANGED) for i in data[:file_num]]
    

    try:
        print('Original size',img[0].shape)
        myshape=img[0].shape
        
    except AttributeError:
        print("shape not found")
    
    # --------------------------------
    # setting dim of the resize
    height = myshape[0]
    width = myshape[1]
    dim = (width, height)
    res_img = []
    for i in range(len(img)):
        res = cv2.resize(img[i], dim, interpolation=cv2.INTER_LINEAR)
        res_img.append(res)

    # Checcking the size
    try:
        print('RESIZED', res_img[1].shape)
    except AttributeError:
        print("shape not found")
    # Visualizing one of the images in the array
    #original = res_img[1]
    #display_one(original)
    # ----------------------------------
    # Remove noise
    # Using Gaussian Blur
    no_noise = []
    
    for i in range(len(res_img)):
        #blur = cv2.GaussianBlur(res_img[i], (5, 5), 0)
        blur = cv2.bilateralFilter(res_img[i],5,100,100)
        no_noise.append(blur)


    for i in range(len(res_img)):

        original = res_img[i]
        image = no_noise[i]
        


        #display(original, image, 'Original', 'Blured')
        im=Image.fromarray(image)
        myname=data[i]
        mynamestring=str(myname[+image_path_length:])
        print("no_noise_path", no_noise_path)
        print("my_name",mynamestring)
        #im.save(f"{no_noise_path}{mynamestring}")

        #---------------------------------
        # Segmentation
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        im5=Image.fromarray(gray)
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV)
        ret, thresh2 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
        ret, thresh3 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

        th4 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,11,4)
        #increasing to 4 keeps features but removes noise
 
        #display(thresh, thresh2, "Their thresh", "My Thresh")

        im2=Image.fromarray(thresh)

        # Further noise removal (Morphology)
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        

        im6=Image.fromarray(th4)
        # sure background area
        sure_bg = cv2.dilate(opening, kernel, iterations=3)

        # Displaying sure background
        #display(original, sure_bg, 'Original', 'Sure background')

        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)
        #Displaying unknown
        #display(original, unknown, 'Original', 'Unknown')

        #Displaying segmented back ground
        #display(original, sure_bg, 'Original', 'Segmented Background')
        im3=Image.fromarray(sure_bg)
        # Marker labelling
        ret, markers = cv2.connectedComponents(sure_fg)

        # Add one to all labels so that sure background is not 0, but 1
        markers = markers + 1

        # Now, mark the region of unknown with zero
        markers[unknown == 255] = 0
        

        markers = cv2.watershed(image, markers)
        image[markers == -1] = [0, 0, 255]

        im4= cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        im4=Image.fromarray(im4)

        im.save(f"{no_noise_path}{mynamestring}")
        im2.save(f"{segmented_path}{mynamestring}")
        im3.save(f"{segmented_background_path}{mynamestring}")
        im4.save(f"{markers_path}{mynamestring}")
        im5.save(f"{grey_path}{mynamestring}")
        im6.save(f"{adapthresh_path}{mynamestring}")

def main():
    MakeDirs()
    # calling global variable
    global image_path
    '''The var Dataset is a list with all images in the folder '''
    dataset = loadImages(image_path)
    
    # sending all the images to pre-processing
    processing(dataset)
   

  
main()