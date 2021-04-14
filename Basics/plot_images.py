import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import numpy as np
from PIL import Image
import os
path="/home/james/inference_test/working/ordered_working/working_ordered_detections/"

im1 = np.arange(100).reshape((10, 10))
im2 = im1.T
im3 = np.flipud(im1)
#im4 = np.fliplr(im2)#

no_of_images=len(os.listdir(path))
print(no_of_images)


im0 = Image.open(f"{path}0.jpg")
im1 = Image.open(f"{path}1.jpg")
im2 = Image.open(f"{path}2.jpg")
im3 = Image.open(f"{path}3.jpg")
im4 = Image.open(f"{path}4.jpg")
im5 = Image.open(f"{path}5.jpg")
im6 = Image.open(f"{path}6.jpg")
im7 = Image.open(f"{path}7.jpg")
im8 = Image.open(f"{path}8.jpg")

fig = plt.figure(figsize=(8., 8.))
grid = ImageGrid(fig, 111,  # similar to subplot(111)
                 nrows_ncols=(3, 3),  # creates 2x2 grid of axes
                 axes_pad=0.27,  # pad between axes in inch.
                 )
extension=0
for ax, im in zip(grid, [im0,im1, im2, im3, im4,im5,im6,im7,im8]):
    ax.set_title(f"{extension}.jpg", fontdict=None, loc='center', color = "k")
    extension += 1
    # Iterating over the grid returns the Axes.
    ax.imshow(im)



plt.show()
