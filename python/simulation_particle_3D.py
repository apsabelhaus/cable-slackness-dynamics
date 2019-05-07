"""
Simulation script for the particle with viscoelastic cables.
This goes with the controller derived in Drew's dissertation.
(C) Andrew P. Sabelhaus, 2019
"""

# import everything we need
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
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

cable_tags = ['top', 'bottom', 'left', 'right']

# Let's do top bottom left right, like the spine frame, for 
# a tetrahedral convex hull.
params_top = {'k':300, 'c':10}
params_bottom = {'k':100, 'c':10}
params_left = {'k':150, 'c':10}
params_right = {'k':350, 'c':10}

# Put the parameters into a nested dict.
cable_params = {'top':params_top, 'bottom':params_bottom, 
                'left':params_left, 'right':params_right}

# Anchor points for each cable.
# These are all in three dimensions.
# Force floating point numbers.
# (check these later.)
anchor_top = np.array([0., .2, .2])
anchor_bottom = np.array([0., .2, -.2])
anchor_left = np.array([-.2, -.2, 0.])
anchor_right = np.array([.2, -.2, 0.])

# Anchors in a nested dict too.
cable_anchors = {'top':anchor_top, 'bottom':anchor_bottom,
                 'left':anchor_left, 'right':anchor_right}

# create the cables
# important that each tag has a set of parameters and an anchor!
cables = {}
for tag in cable_tags:
    cables[tag] = cable_piecewise3D.PiecewiseLinearCable3D(
                        params = cable_params[tag],
                        anchor_pos = cable_anchors[tag])                                                                      


# For feedback control, declare the required constants.
# As with the cables, assume that each controller will have a tag,
# and do a nested dictionary.
controller_consts_top = {'kappa':0.88, 'bar_ell':0.217944947177034, 'bar_v': 0.186851770747656}
controller_consts_bottom = {'kappa':0.995, 'bar_ell':0.295803989154981, 'bar_v': 0.292845949263251}
controller_consts_left = {'kappa':0.98, 'bar_ell':0.357071421427142, 'bar_v': 0.346645035107927}
controller_consts_right = {'kappa':0.95, 'bar_ell':0.295803989154981, 'bar_v': 0.277295287050143}

controller_consts = {'top':controller_consts_top, 'bottom':controller_consts_bottom,
                 'left':controller_consts_left, 'right':controller_consts_right}

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
m = 0.495
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

# Initial condition:
# CHANGE THIS - NEEDS TO BE INSIDE CONVEX HULL OF POINTS
pm_pos_initial = [0.1, 0.1, .08]
pm_vel_initial = [.3, .3, 15]

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
    # The "pythonic" way of iterating over both cables and control inputs
    # would be to use the 'zip' function, but unsure if that's best here...
    # default to a more MATLAB-ian syntax.
    for tag in cable_tags:

        # calculate the control input for this cable based on its length.
        # length calulated by cable. All are connected to the point mass.
        l_i = cables[tag].get_length(pm_pos)
        
        # CONTROL LAW
        # open loop:
        # control_i = controllers[tag]

        # Affine output feedback:
        control_i = controllers[tag].v(l_i)

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
    # end.

# An analysis at the end.
# Add a green point for the initial position,
# and a purple point for the final
t0 = pm_state_history[0,:]
tf = pm_state_history[-1,:]

print('Equilibrium position should be:')
# ...from MATLAB's calculations,
bar_r = np.array([0.05, 0.05, 0.05])
print(bar_r)
print('Point mass position at final timestep:')
print(tf[0:3])
print('Error is:')
print(tf[0:3] - bar_r)

# Let's plot the results!
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# REMEMBER THAT PYTHON INDEXES FROM 0
# 3D:
line, = ax.plot(pm_state_history[0:1,0], pm_state_history[0:1,1], pm_state_history[0:1,2])
# ax.plot(pm_state_history[:,0], pm_state_history[:,1], pm_state_history[:,2])

# The starting point
ax.scatter(pm_state_history[0,0], pm_state_history[0,1], pm_state_history[0,2],
        color='green', marker='o', s=60)
ax.text(t0[0], t0[1], t0[2], 't0')

# plot the anchor points
for tag in cable_tags:
        anch = cable_anchors[tag]
        ax.scatter(anch[0], anch[1], anch[2], s=60, color='black', marker='v')
        # ax.text(anch[0], anch[1], anch[2], )

# Setting the plot limits:
# ax.set_xlim(-0.7, 0.7)
# ax.set_ylim(-0.2, 0.6)
# ax.set_zlim(-0.6, 2.5)
ax.set_xlim(-0.15, 0.3)
ax.set_ylim(-0.6, 0.15)
ax.set_zlim(-0.2, 0.5)
# # To-do here: annotate initial and final timesteps.

# ax.text(tf[0], tf[1], tf[2], 'tf')
# # labels
ax.set(xlabel='Pos, X (m)', ylabel='Pos, Y (m)', zlabel='Pos, Z (m)',
    title='Cable-driven robot (particle) position, closed-loop control')
# #ax.grid()

# # The easiest way to do things here are a few functions inside this script.
# def ani_init():
#         # initialize/reset the image for the animation.
#         ax.set_xlim(-0.15, 0.3)
#         ax.set_ylim(-0.6, 0.15)
#         ax.set_zlim(-0.2, 0.5)
#         return line,

def ani_update(frameno, pm_state_history, ln, handles):
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
        return ln,

# One way to pass around the handles to the updated positions
# is to store in a list of those handles,
# and pass it around
position_handles_list = []

# finally, run
ani = FuncAnimation(fig=fig, func=ani_update, frames=num_timesteps, 
                    fargs=(pm_state_history, line, position_handles_list), interval=50, blit=False)

plt.show()

ax.scatter(pm_state_history[-1,0], pm_state_history[-1,1], pm_state_history[-1,2],
        color='m', marker='o')
