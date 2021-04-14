
from PIL import Image
import os, sys

path="/home/james/whale_for_inference_test/"
output_path="/home/james/test_output/"
dirs = os.listdir( path )


def resize_no_black():
    for item in dirs:
        if item == '.DS_Store':
            continue
        if os.path.isfile(path+item):
            basewidth=1280
            img = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            wpercent = (basewidth/float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            new_im = Image.new("RGB",(basewidth,hsize))
            new_im.paste(img)
            print("f is",f)
            print("e is",e)
            new_im.save(f+'.jpg','JPEG',quality=90)
            #img.save(output_path+item, 'JPEG')


resize_no_black()