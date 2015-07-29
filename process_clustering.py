from __future__ import print_function

import openmc
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", "--save",
                  action="store_true", dest="save", default=False,
                  help="write to movie, supress window")

(options, args) = parser.parse_args()


# set number of batches to read
n_batches = 200 

# processes a given statepoint and returns xy data
def process_statepoint(i):

    print("Processing statepoint.{0:03d}.binary".format(i+1))

    # open statepoint file
    sp = openmc.statepoint.StatePoint("statepoint.{0:03d}.binary".format(i+1))

    # read source points
    sp.read_source()

    # allocate xyz arrays
    xy = np.zeros((sp.n_particles, 2))
    for j in xrange(sp.n_particles):
        xy[j, 0] = sp.source[j].xyz[0]
        xy[j, 1] = sp.source[j].xyz[1]

    return xy

# updates scatter plot with new xy offsets
def animate(i):

    xy = process_statepoint(i)
    scat.set_offsets(xy)
    return scat,

# write out starting data
xy = process_statepoint(0)
fig, ax = plt.subplots()
scat = ax.scatter(xy[:, 0], xy[:, 1])

# perform animation
ani = animation.FuncAnimation(fig, animate, np.arange(1, n_batches))

# either save or show during processing
if options.save:
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    ani.save("clustering.mp4", writer=writer)
else:
    plt.show()
