import matplotlib.pyplot as plt
import imageio
from scipy import ndimage
from scipy import misc
import numpy as np
from PIL import Image, ImageOps
import skimage


# f = misc.face(gray=True)
# imageio.imsave('/home/james/image_preprocessing/face.png', f) # uses the Image module (PIL)
# face = imageio.imread('/home/james/image_preprocessing/face.png')
# type(face)
# #import matplotlib.pyplot as plt
# plt.imshow(f)
# plt.show()


# im2 = imageio.imread("/home/james/inference_test/hump0066.jpg")
# #im2 = Image.open("/home/james/inference_test/hump0066.jpg")
# im2 = ndimage.gaussian_filter(im2, 8)
# sx = ndimage.sobel(im2, axis=0, mode='constant')
# sy = ndimage.sobel(im2, axis=1, mode='constant')
# sob = np.hypot(sx, sy)

# plt.imshow(sob)
# plt.show()

from skimage import data
from skimage import filters
camera = data.camera()
val = filters.threshold_otsu(camera)
mask = camera < val