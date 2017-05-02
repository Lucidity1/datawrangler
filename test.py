

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.misc import imread


img = imread('raw/NSEWL_updated-1.png')

# Create figure and axes
fig,ax = plt.subplots(1)

# Display the image
ax.imshow(img)

# Create a Rectangle patch
rect = patches.FancyBboxPatch((5000,5000),500,500,linewidth=2)

# Add the patch to the Axes
ax.add_patch(rect)

plt.savefig('output/plot/test.png')
print 'output generated'