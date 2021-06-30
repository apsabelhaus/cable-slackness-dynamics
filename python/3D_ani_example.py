"""
3D visualization of a point mass moving over time, cables attached.
This goes with the controller derived in Drew's dissertation.
(C) Andrew P. Sabelhaus, 2019
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import pickle

#############
############# A few hard-coded variables
#############

cable_color = 'r'
# One way to pass around the handles to the updated positions is to store in a list of those handles and pass it around
position_handles_list = []

#############
############# Functions used during animation
#############

# Used to update the lines used to represent the cables, 
# from anchors to point mass.
def update_cable_lines(frameno, pm_state_history, cable_lines_dict, 
                       cable_tags, cable_anchors):
        # As with the initialization,
        for tag in cable_tags:
                anch = cable_anchors[tag]
                # Organize cable lines into three, 2-element np arrays
                clx = np.array([pm_state_history[frameno-1,0], anch[0]])
                cly = np.array([pm_state_history[frameno-1,1], anch[1]])
                clz = np.array([pm_state_history[frameno-1,2], anch[2]])
                # Pull out this line
                cable_line_i = cable_lines_dict[tag]
                # Update it appropriately
                cable_line_i.set_data(clx, cly)
                cable_line_i.set_color(cable_color)
                cable_line_i.set_3d_properties(clz)

# Update the animation - this is passed to FuncAnimation
# Need to pass in all the arguments to update_cable_lines too, messy.
def ani_update(frameno, pm_state_history, ln, handles, cable_lines_dict, 
               cable_tags, cable_anchors):
        # First, clear out all the scatterplots from prev calls.
        # The guard evaluates to true if handles is not empty
        while len(handles) != 0:
                h = handles.pop()
                h.remove()
        # Given a timestep (that's 'frame'),
        # plot the time history of the point mass up until now.
        ln.set_data(pm_state_history[0:frameno, 0], pm_state_history[0:frameno, 1])
        ln.set_3d_properties(pm_state_history[0:frameno, 2])
        next_h = ax.scatter(pm_state_history[frameno-1,0], pm_state_history[frameno-1,1], pm_state_history[frameno-1,2],
                color='blue', marker='o', s=60)
        handles.append(next_h)
        # Also update the lines from the pointmass to the cable anchors
        update_cable_lines(frameno, pm_state_history, cable_lines_dict, 
                           cable_tags, cable_anchors)
        return ln

############
############ Load example data
############

# N.B. you'll want to pause here to debug and see these data structures. Roughly speaking:

# num_timesteps = we simulated the point mass moving forward for this many steps
# pm_state_history = a num_timesteps x 6 array of the particle's state, [x, y, z, \dot x, \dot y, \dot z]
# cable_tags = dictionary with labels for each cable. Made it easier to pick out which lines are which.
# force_history = unused
# eps = unused

pfile = "example_particlewithcables.pickle"
with open(pfile, "rb") as f:
    (num_timesteps, pm_state_history, cable_tags, cable_anchors, force_history, eps) = pickle.load(f)

############
############ Set up the plot
############

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# Change the azimuth and elevation for better viewing
az = -47.
elev = 36.

# 3D: plot the path of the point mass over its trajectory. 
# This line will get updated during animation to show the history of the particle's position up until a point in time.
pm_path_line = ax.plot(pm_state_history[0:1,0], pm_state_history[0:1,1], pm_state_history[0:1,2])[0]
ax.view_init(elev=elev, azim=az)

# change the density of ticks
numticksx = 5
xloc = plt.MaxNLocator(numticksx)
ax.xaxis.set_major_locator(xloc)

numticksy = 5
yloc = plt.MaxNLocator(numticksy)
ax.yaxis.set_major_locator(yloc)

numticksz = 4
zloc = plt.MaxNLocator(numticksz)
ax.zaxis.set_major_locator(zloc)

# Setup the moviewriter to save the animation
Writer = animation.writers['ffmpeg']
writer = Writer(fps=15, metadata=dict(artist='Andrew P. Sabelhaus'), bitrate=1800)

# The starting point
t0 = pm_state_history[0,:]
ax.scatter(pm_state_history[0,0], pm_state_history[0,1], pm_state_history[0,2],
        color='blue', marker='o', s=60)
ax.text(t0[0], t0[1], t0[2], 't0')

# plot the anchor points
for tag in cable_tags:
        anch = cable_anchors[tag]
        ax.scatter(anch[0], anch[1], anch[2], s=60, color='black', marker='v')

# Setting the plot limits:
ax.set_xlim(-0.15, 0.3)
ax.set_ylim(-0.6, 0.15)
ax.set_zlim(-0.2, 0.5)

# labels
ax.set(xlabel='Pos, X (m)', ylabel='Pos, Y (m)', zlabel='Pos, Z (m)',
    title='Cable-driven robot (particle) position, closed-loop control')

# Create the lines from anchor points to the point mass.
# Will be updated on-the-fly during animation.
cable_lines_dict = {}
for tag in cable_tags:
        anch = cable_anchors[tag]
        # Organize cable lines into three, 2-element np arrays
        clx = np.array([pm_state_history[0,0], anch[0]])
        cly = np.array([pm_state_history[0,1], anch[1]])
        clz = np.array([pm_state_history[0,2], anch[2]])
        # Get the right color for this cable
        color_i = cable_color
        # Actually plot the line
        cable_line_i = ax.plot(clx, cly, clz, color=color_i)[0]
        # and save it to the dict, so we can update it later
        cable_lines_dict[tag] = cable_line_i

# finally, run
ani = FuncAnimation(fig=fig, func=ani_update, frames=num_timesteps, 
                    fargs=(pm_state_history, pm_path_line, position_handles_list,
                           cable_lines_dict, cable_tags, cable_anchors), 
                    interval=50, blit=False)

#############
############# FINISH UNCOMMENT to get animation
#############


############# Comment this out to save the video. Can't see and save at same time.
plt.show()

# ani.save('3D_ani_example.mp4', writer=writer)