"""
Simulation script for the particle with viscoelastic cables,
particle inside a box (not just a pyramid like earlier.)
This goes with the controller derived in Drew's dissertation.
(C) Andrew P. Sabelhaus, 2019
"""

# import everything we need
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
# for nicer plots / animations,
import plotly.offline as plyoff
import plotly.graph_objs as go
# for the cables and other things we write,
# let's make it so we don't need to use the module name
from cable_models import *
from body_models import *
from controllers import *

# Parameters for the cables are going to be a dict.
# Assume that each cable will interpret its dict correctly (polymorphically.)
# Each cable will have a tag associated with it.
# Makes it easier than numbering.

# cable_tags = ['top', 'bottom', 'left', 'right']
cable_tags = ['A','B','C','D','E','F','G','H']

# Box is labelled A...H as nodes.
# Cable parameters:
# back face
pA = {'k':300, 'c':10}
pB = {'k':1500, 'c':10}
pC = {'k':150, 'c':10}
pD = {'k':80, 'c':10}
# front face
pE = {'k':180, 'c':10}
pF = {'k':900, 'c':10}
pG = {'k':1000, 'c':10}
pH = {'k':470, 'c':10}

# Put the parameters into a nested dict.
cable_params = {'A':pA, 'B':pB, 'C':pC, 'D':pD, 
                'E':pE, 'F':pF, 'G':pG, 'H':pH}

# Anchor points for each cable.
# These are all in three dimensions.
# Force floating point numbers.

# box (cube dimension)
bn = 1.
# back face
aA = np.array([0., 0., 0.])
aB = np.array([0., 0., bn])
aC = np.array([0., bn, bn])
aD = np.array([0., bn, 0.])
# front face
aE = np.array([bn, 0., 0.])
aF = np.array([bn, 0., bn])
aG = np.array([bn, bn, bn])
aH = np.array([bn, bn, 0.])

# Anchors in a nested dict too.
cable_anchors = {'A':aA, 'B':aB, 'C':aC, 'D':aD, 
                'E':aE, 'F':aF, 'G':aG, 'H':aH}

# create the cables
# important that each tag has a set of parameters and an anchor!
cables = {}
for tag in cable_tags:
    cables[tag] = cable_piecewise3D.PiecewiseLinearCable3D(
                        params = cable_params[tag],
                        anchor_pos = cable_anchors[tag])                                                                      


# For feedback control, declare the required controller constants.

# back face
ccA = {'kappa':0.95, 'bar_ell':0.743303437365925, 'bar_v':0.69186683950129}
ccB = {'kappa':0.92, 'bar_ell':0.390512483795333, 'bar_v':0.335517912410296}
ccC = {'kappa':0.85, 'bar_ell':0.867467578644874, 'bar_v':0.705540297302958}
ccD = {'kappa':0.93, 'bar_ell':1.07354552767919, 'bar_v':0.912513698505512}
# front face
ccE = {'kappa':0.97, 'bar_ell':1.11915146427997, 'bar_v':1.04454136665865}
ccF = {'kappa':0.995, 'bar_ell':0.923309265630969, 'bar_v':0.910998475422311}
ccG = {'kappa':0.995, 'bar_ell':1.20519707931939, 'bar_v':1.19073471436736}
ccH = {'kappa':0.985, 'bar_ell':1.36106575888162, 'bar_v':1.32631514376099}

controller_consts = {'A':ccA, 'B':ccB, 'C':ccC, 'D':ccD, 
                'E':ccE, 'F':ccF, 'G':ccG, 'H':ccH}

# Affine, output feedback controllers.
controllers = {}
for tag in cable_tags:
    controllers[tag] = linear.AffineFeedback(kappa = controller_consts[tag]['kappa'],
                                             bar_ell = controller_consts[tag]['bar_ell'],
                                             bar_v = controller_consts[tag]['bar_v'])

# Open-loop setpoint controllers.
# Affine, output feedback controllers.
# controllers = {}
# for tag in cable_tags:
#     controllers[tag] = linear.OpenLoop(bar_v = controller_consts[tag]['bar_v'])

# something to start for now: open loop, setpoint, fully retracted.
# controllers = {}
# for tag in cable_tags:
#     controllers[tag] = 0.

# For consistency with more general simulations,
# make a list of cables
# cables = [cable1, cable2]
# testing: one hybrid cable
#cables = [cable2]

# Pre-calculated values for the equilibrium cable forces at a 
# desired x_eq. Use (for example) inverse kinematics here for larger N-D
# tensegrities.
# pretensions = [300.0, 300.0]
# For the gravity case, with m=1.45, we can calculate
# the new required pretension to stabilize at the lengths/postions
# spec'd above:
#pretensions = [300.0, 285.8]

# Now, for the mass: in kilograms and SI units,
m = 4.
g = 9.8
# 1D:
# example: for a cable anchor at x=2,
# an initial position of 0, 
# and a control input of 1, then the system equilibrizes around 1
# NOTE: With the control law as of 2018-08-17, actuator saturation occurs
# outside of the interval [5, 7] in point mass position (e.g., the controller
# would command a negative rest length outside those bounds.)
# In future: need to check 
#pm_pos_initial = np.array([5.5])
# pm_pos_initial = np.array([5.2])
#pm_pos_initial = np.array([6.9])
# pm_vel_initial = np.array([0.])
#pm_vel_initial = np.array([-15])
#pm_vel_initial = np.array([-5])
#pm_vel_initial = np.array([10])
# 2D:
#pm_pos_initial = np.array([0,0])
#pm_vel_initial = np.array([0,0])

# Initial condition: must be within box.
pm_pos_initial = [0.5, 0.3, .8]
# pm_pos_initial = [0.5, 0.3, .3] # this one exits the box, for example
pm_vel_initial = [-1, .3, -6]

# The body itself:
pm = point_mass3D.PointMass3D(m, g, pm_pos_initial, pm_vel_initial)

# Let's create a range of timesteps for the simulation.
# really, don't change the start time from 0, that's meaningless unless
# it's easier than doing some offset after another simulation.
t_start = 0.0 
# let's specify a dt and number of timesteps, in sec
# (let's do maybe 1/100th of a sec, 100 Hz for integration is fine for now)
# Then, the range of times will be:
dt = 0.01
num_timesteps = 200
# num_timesteps = 50000
#timesteps = np.linspace(t_start, t_end, num_timesteps)
# For later (numerical integration), we need the timestep itself.
# Maybe there's a better way to do this in the future.
#dt = t_end / num_timesteps
# NOTE: we're vaguely off-by-one here. Drew is more used to MATLAB, so
# dt isn't an even number (needs to be num_timesteps+1 for even division)

# for use later when plotting, make a big vector of all the timesteps
# like described above, this includes 0, so we need to increment
timesteps = np.arange(t_start, dt*(num_timesteps+1), dt)

# We need to save the results of the system state, over time.
# This needs to be a 2*d-dimensional by timestep problem
# (we're saving both positions and velocities)
# 'shape' of ndarray is (first axis -> row), (second axis -> column)
# so we're looking at row vectors here.
# ALSO, we're storing the initial state as the first element,
# so for num_timesteps of data, we need to be recording in a num_timesteps+1
# array.
pm_state_history = np.zeros((num_timesteps+1, 6))
# Something like pm_state_history[1] returns
# a d-dimensional vector.
# Insert the initial state into the ndarray.
pm_state_history[0] = pm.get_state()

# Also going to save the applied cable forces.
# This will allow us to test for slackness, in addition to 
# checking the Lyapunov function.
# We want to save according to timestep. So, do a list indexed by time,
# with a dict by tag.
force_history = []

### Run the simulation.

# The "pythonic" way of iterating over both timesteps and history
# would be to use the 'zip' function, but unsure if that's best here...
# default to a more MATLAB-ian syntax.
for t in range(num_timesteps):
    # ...note that this will have t from 0 to num_timesteps-1.
    print('Timestep ' + str(t))

    # At a specific timestep, we have a control input for each cable.
    # Later, we calculate this closed-loop.
    # Though it's inefficient to re-declare every iteration,
    # placing the control declaration here reminds us that it goes here
    # also later when the control law is implemented.

    # TO-DO: use controller objects.
    
    # hard coded for now: for n cables, need n inputs.
    # do it as an ndarray so we can index into it.
    # rest length of 0, for example
    #control = np.array([4, 4])

    # Get the current point mass state, for use in calculating the
    # cable force(s).
    pm_pos = pm.get_pos()
    pm_vel = pm.get_vel()
    # for numerical integration below
    pm_state = pm.get_state()

    # Have each cable calculate its force.
    # Importantly, the "other anchor point" for any cable,
    # when we're simulating only a single point mass,
    # will be that point mass' position and velocity!!
    forces_list = []
    # ...need a list for calculating the pointmass state,
    # but we want a dict for recording and referencing the SCALAR force!
    forces_dict = {}
    # The "pythonic" way of iterating over both cables and control inputs
    # would be to use the 'zip' function, but unsure if that's best here...
    # default to a more MATLAB-ian syntax.
    for tag in cable_tags:

        # calculate the control input for this cable based on its length.
        # length calulated by cable. All are connected to the point mass.
        ell_i = cables[tag].get_length(pm_pos)
        
        # CONTROL LAW
        # open loop:
        # control_i = controllers[tag]

        # Affine output feedback:
        control_i = controllers[tag].v(ell_i)

        #debugging
        # print('Length and control input for cable ' + tag)
        # print(l_i)
        # print(control_i)
        
        ### IMPORTANT: 
        # Here is where the sign is flipped for cable forces.
        # The equations of motion, as written usually, would have
        # the output of calculate_force be negative. 
        # However, in order to be consistent with passivity,
        # we apply the negative sign here.
        # See, for example, the nonlinear passive spring proof
        # in Sastry's Nonlinear Systems textbook, where the spring
        # force is g(x), and the equations of motion include -g(x).
        # CHECK THIS
        force_i = -cables[tag].force_3d(pm_pos, pm_vel, control_i)
        #print(force_i)
        forces_list.append(force_i)
        
        # For the recording of the force, we want the SCALAR force!
        # This is *not* the norm of the force, it's signed according to the
        # unit vector along the cable, etc.
        # need d \ell
        dot_ell_i = cables[tag].get_dot_length(pm_pos, pm_vel)
        # then the scalar function call is
        force_i_scalar = cables[tag].scalar_force(ell_i, dot_ell_i, control_i)
        forces_dict[tag] = force_i_scalar
    
    #debugging
    # print('Forces at timestep ' + str(t))
    # print(forces_list)
    # The point mass can then calculate its \dot x
    # (as in, \dot x = f(x, u), really just the vel and accel in one vec.)
    pm_state_deriv = pm.state_deriv(forces_list)

    # We can then integrate to get state(t+1).
    # later, do something more intelligent (Runge-Kutta, or solve_ivp in numpy)
    # but for now a simple forward-euler is fine enough
    pm_state_tp1 = pm_state + dt * pm_state_deriv

    # Record everything, set up for next iteration.
    # Set the new point mass state:
    pm.set_state(pm_state_tp1)
    pm_state_history[t+1] = pm_state_tp1
    force_history.append(forces_dict)
    # end.

# An analysis at the end.
# First, check to see if the particle ever exited the box.
# no dimension should be less than 0 or greater than bn.
print('Did particle exit the box? < 0, > 1?')
print(np.any(pm_state_history[:,0:3] < 0))
print(np.any(pm_state_history[:,0:3] > 1))

# Add a green point for the initial position,
# and a purple point for the final
t0 = pm_state_history[0,:]
tf = pm_state_history[-1,:]

print('Equilibrium position should be:')
# ...from MATLAB's calculations,
bar_r = np.array([0.15, 0.2, 0.7])
print(bar_r)
print('Point mass position at final timestep:')
print(tf[0:3])
print('Error is:')
print(tf[0:3] - bar_r)

# Let's plot the results!
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# Change the azimuth and elevation for better viewing
# az = -47.
# elev = 36.
az = -62.
elev = 13.
# REMEMBER THAT PYTHON INDEXES FROM 0
# 3D:
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
ax.scatter(pm_state_history[0,0], pm_state_history[0,1], pm_state_history[0,2],
        color='blue', marker='o', s=60)
ax.text(t0[0], t0[1], t0[2], 't0')

# Setting the plot limits:
# For the box:
ax.set_xlim(-0.1, bn+0.1)
ax.set_ylim(-0.1, bn+0.1)
ax.set_zlim(-0.1, bn+0.1)

# # labels
ax.set(xlabel='Pos, X (m)', ylabel='Pos, Y (m)', zlabel='Pos, Z (m)',
    title='Cable-driven robot (particle) position, closed-loop control')

# plot the anchor points
for tag in cable_tags:
        anch = cable_anchors[tag]
        ax.scatter(anch[0], anch[1], anch[2], s=60, color='black', marker='v')
        # ax.text(anch[0], anch[1], anch[2], )

# For use below:
# It's sometimes bad practice to compare with zero, when we know we're setting to
# zero for slackness. Instead, less than a small constant.
eps = 1E-10

# A function to return the desired color for the cable.
def cable_color_chooser(frameno, tag, force_history, bound):
        # This cable's force. Index into a list then the dict
        force = force_history[frameno][tag]
        # Check if it's slack or not
        if force <= bound:
                return 'r'
        else:
                return 'g'

# Initialize the dictionary of lines per anchor.
cable_lines_dict = {}
for tag in cable_tags:
        anch = cable_anchors[tag]
        # Organize cable lines into three, 2-element np arrays
        clx = np.array([pm_state_history[0,0], anch[0]])
        cly = np.array([pm_state_history[0,1], anch[1]])
        clz = np.array([pm_state_history[0,2], anch[2]])
        # Get the right color for this cable
        color_i = cable_color_chooser(0, tag, force_history, eps)
        # Actually plot the line
        cable_line_i = ax.plot(clx, cly, clz, color=color_i)[0]
        # and save it to the dict, so we can continue to update it later
        cable_lines_dict[tag] = cable_line_i

# Plot the box's edges.
edge_color = 'b'
# The box's edges that should be connected.
# A list of lists.
box_edges = [['A','B'],
             ['B','C'],
             ['C','D'],
             ['D','A'],
             ['E','F'],
             ['F','G'],
             ['G','H'],
             ['H','E'],
             ['A','E'],
             ['B','F'],
             ['C','G'],
             ['D','H']]

# then plot each edge
# this is not pythonic, sorry.
for edge in range(len(box_edges)):
        # get the anchor points for these two that form an edge
        anch1 = cable_anchors[box_edges[edge][0]]
        anch2 = cable_anchors[box_edges[edge][1]]
        # Organize lines into three, 2-element np arrays
        clx = np.array([anch1[0], anch2[0]])
        cly = np.array([anch1[1], anch2[1]])
        clz = np.array([anch1[2], anch2[2]])
        # Actually plot the line
        edge_line = ax.plot(clx, cly, clz, color=edge_color)[0]

# # #ax.grid()

# # The easiest way to do things here are a few functions inside this script.
############# THIS FUNCTION UNUSED
# def ani_init():
#         # initialize/reset the image for the animation.
#         ax.set_xlim(-0.15, 0.3)
#         ax.set_ylim(-0.6, 0.15)
#         ax.set_zlim(-0.2, 0.5)
#         return line,

#############
############# UNCOMMENT to get animation
#############

# Used to update the lines used to represent the cables, 
# from anchors to point mass.
def update_cable_lines(frameno, pm_state_history, cable_lines_dict, 
                       cable_tags, cable_anchors, force_history, bound):
        # As with the initialization,
        for tag in cable_tags:
                anch = cable_anchors[tag]
                # Organize cable lines into three, 2-element np arrays
                clx = np.array([pm_state_history[frameno-1,0], anch[0]])
                cly = np.array([pm_state_history[frameno-1,1], anch[1]])
                clz = np.array([pm_state_history[frameno-1,2], anch[2]])
                # Pull out this line
                cable_line_i = cable_lines_dict[tag]
                # Get the right color for this cable
                color_i = cable_color_chooser(frameno-1, tag, force_history, eps)
                # Update it appropriately
                cable_line_i.set_data(clx, cly)
                cable_line_i.set_color(color_i)
                cable_line_i.set_3d_properties(clz)

# Update the animation - this is passed to FuncAnimation
# Need to pass in all the arguments to update_cable_lines too,
# messy.
def ani_update(frameno, pm_state_history, ln, handles, cable_lines_dict, 
               cable_tags, cable_anchors, force_history, bound):
        # First, clear out all the scatterplots from prev calls.
        # The guard evaluates to true if handles is not empty
        while len(handles) != 0:
                h = handles.pop()
                h.remove()
        # Given a timestep (that's 'frame'),
        # plot all the data from zero until now.
        ln.set_data(pm_state_history[0:frameno, 0], pm_state_history[0:frameno, 1])
        ln.set_3d_properties(pm_state_history[0:frameno, 2])
        next_h = ax.scatter(pm_state_history[frameno-1,0], pm_state_history[frameno-1,1], pm_state_history[frameno-1,2],
                color='blue', marker='o', s=60)
        handles.append(next_h)
        # Also update the lines from the pointmass to the cable anchors
        update_cable_lines(frameno, pm_state_history, cable_lines_dict, 
                           cable_tags, cable_anchors, force_history, bound)
        return ln

# One way to pass around the handles to the updated positions
# is to store in a list of those handles,
# and pass it around
position_handles_list = []

# finally, run the animation if specified
run_ani = 1

if run_ani:
        ani = FuncAnimation(fig=fig, func=ani_update, frames=num_timesteps, 
                        fargs=(pm_state_history, pm_path_line, position_handles_list,
                                cable_lines_dict, cable_tags, cable_anchors, 
                                force_history, eps), 
                        interval=50, blit=False)

#############
############# FINISH UNCOMMENT to get animation
#############

ax.scatter(bar_r[0], bar_r[1], bar_r[2],
        color='m', marker='o')
ax.text(bar_r[0], bar_r[1], bar_r[2], 'eq')

############# Comment this out to save the video. Can't see and save at same time.
plt.show()

# ani.save('simulation_particle_3d_test.mp4', writer=writer)