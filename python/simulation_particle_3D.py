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
# for the cables and other things we write,
# let's make it so we don't need to use the module name
from cable_models import *
from body_models import *

# Parameters for the cables are going to be a dict.
# Assume that each cable will interpret its dict correctly (polymorphically.)
# Each cable will have a tag associated with it.
# Makes it easier than numbering.

cable_tags = ['top', 'bottom', 'left', 'right']

# Let's do top bottom left right, like the spine frame, for 
# a tetrahedral convex hull.
params_top = {'k':300, 'c':50}
params_bottom = {'k':100, 'c':50}
params_left = {'k':150, 'c':50}
params_right = {'k':350, 'c':50}

# Put the parameters into a nested dict.
cable_params = {'top':params_top, 'bottom':params_bottom, 
                'left':params_left, 'right':params_right}

# Anchor points for each cable.
# These are all in three dimensions.
# Force floating point numbers.
# (check these later.)
anchor_top = np.array([0., 10., 10.])
anchor_bottom = np.array([0., 10., -10.])
anchor_left = np.array([-10., -10., 0.])
anchor_right = np.array([10., -10., 0.])

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


# For feedback control, declare some proportionality constants.
# One for each cable, for now (two distributed controllers.)
# kappa = np.array([15, 15])

# Also, for controller, we need to specify a point to stabilize around.
# Assuming the anchors below (8 and 2), stabilizing around 6.5 (within [5 7])
# leads to equilibrium cable lengths of
# l_eq = [1.5, 4.5]

# TO-DO here: make the controller a class, instantiate controllers
# for each cable.

# something to start for now: open loop, setpoint, fully retracted.
controllers = {}
for tag in cable_tags:
    controllers[tag] = 0.

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
m = 1.45
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
pm_pos_initial = [0.1, 0.5, 2.]
pm_vel_initial = [0.5, .8, -.1]

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
#num_timesteps = 500
num_timesteps = 1000
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
        # open loop for now.
        control_i = controllers[tag]

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

# Let's plot the results!
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# REMEMBER THAT PYTHON INDEXES FROM 0
# 3D:
ax.plot(pm_state_history[:,0], pm_state_history[:,1], pm_state_history[:,2])
# Add a green point for the initial position,
# and a purple point for the final
t0 = pm_state_history[0,:]
tf = pm_state_history[-1,:]
ax.scatter(pm_state_history[0,0], pm_state_history[0,1], pm_state_history[0,2],
        color='green', marker='o')
ax.scatter(pm_state_history[-1,0], pm_state_history[-1,1], pm_state_history[-1,2],
        color='m', marker='o')
# To-do here: annotate initial and final timesteps.
ax.text(t0[0], t0[1], t0[2], 't0')
ax.text(tf[0], tf[1], tf[2], 'tf')
# labels
ax.set(xlabel='Pos, X (m)', ylabel='Pos, Y (m)', zlabel='Pos, Z (m)',
    title='Open-loop slack cable control results')
#ax.grid()
# make a line at the equilibrium position
#ax.axhline(y=6.5, label='Equilibrium position')
plt.show()
