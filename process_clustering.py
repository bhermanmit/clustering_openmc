from __future__ import print_function

import openmc
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# set number of batches to read
n_batches = 200 

def process_statepoint(i):

    print("Processing statepoint.{0:03d}.binary".format(i+1))

    # open statepoint file
    sp = openmc.statepoint.StatePoint("statepoint.{0:03d}.binary".format(i+1))

    # read source points
    sp.read_source()

    # allocate xyz arrays
    xy = np.zeros((sp.n_particles, 2))
    z = np.zeros((sp.n_particles))
    for j in xrange(sp.n_particles):
        xy[j, 0] = sp.source[j].xyz[0]
        xy[j, 1] = sp.source[j].xyz[1]
        z[j] = sp.source[j].xyz[2]

    return xy, z

def animate(i):

    xy, _ = process_statepoint(i)
    scat.set_offsets(xy)
    return scat,

xy, z = process_statepoint(0)
fig, ax = plt.subplots()
scat = ax.scatter(xy[:, 0], xy[:, 1])

ani = animation.FuncAnimation(fig, animate, np.arange(1, n_batches))
plt.show()
