import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import numpy as np
from PIL import Image
import os
path="/home/james/findingfauna_docs/for_write_up/dataset_writeup_whalefromabove/diff_angle/"

im1 = np.arange(100).reshape((10, 10))
im2 = im1.T
im3 = np.flipud(im1)
#im4 = np.fliplr(im2)#

no_of_images=len(os.listdir(path))
print(no_of_images)


im0 = Image.open(f"{path}0000.jpg")
im1 = Image.open(f"{path}0001.jpg")
im2 = Image.open(f"{path}0002.jpg")
im3 = Image.open(f"{path}0003.jpg")
# im4 = Image.open(f"{path}0004.jpg")
# im5 = Image.open(f"{path}0005.jpg")
# im6 = Image.open(f"{path}0006.jpg")
# im7 = Image.open(f"{path}0007.jpg")
# im8 = Image.open(f"{path}0008.jpg")

fig = plt.figure(figsize=(8., 8.))
grid = ImageGrid(fig, 111,  # similar to subplot(111)
                 nrows_ncols=(2, 2),  # creates 2x2 grid of axes
                 axes_pad=0.27,  # pad between axes in inch.
                 )
extension=0
for ax, im in zip(grid, [im0,im1, im2, im3]):
    #ax.set_title(f"{extension}.jpg", fontdict=None, loc='center', color = "k")
    extension += 1
    # Iterating over the grid returns the Axes.
    ax.imshow(im)



plt.show()
