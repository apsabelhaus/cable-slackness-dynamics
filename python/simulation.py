"""
Primary script for cable slackness dynamics simulations.
(C) Andrew P. Sabelhaus, 2018
"""

# import everything we need
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
# for the cables and other things we write,
# let's make it so we don't need to use the module name
from cable_models import *
from body_models import *

# Parameters for the cables are going to be a dict.
linear_cable_params = {'k':100, 'c':5}
# anchor point for cable 1 at some offset.
# 1D:
cable1_anchor = np.array([2])
# 2D:
#cable1_anchor = np.array([2,2])
# create the cable
cable1 = cable_linear.LinearCable(params = linear_cable_params, 
                                  anchor_pos = cable1_anchor)

# For consistency with more general simulations,
# make a list of cables (though we only have one right now.)
cables = [cable1]

# create the point mass.
m = 1.45
#g = 9.8
g = 0.0
# 1D:
# example: for a cable anchor at x=2,
# an initial position of 0, 
# and a control input of 1, then the system equilibrizes around 1
pm_pos_initial = np.array([1.5])
pm_vel_initial = np.array([0])
# 2D:
#pm_pos_initial = np.array([0,0])
#pm_vel_initial = np.array([0,0])
pm = point_mass.PointMass(m, g, pm_pos_initial, pm_vel_initial)

# Let's create a range of timesteps for the simulation.
# really, don't change the start time from 0, that's meaningless unless
# it's easier than doing some offset after another simulation.
t_start = 0.0 
# let's specify a dt and number of timesteps, in sec
# (let's do maybe 1/100th of a sec, 100 Hz for integration is fine for now)
# Then, the range of times will be:
dt = 0.01
num_timesteps = 500
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
d = pm.get_dimensionality()
# 'shape' of ndarray is (first axis -> row), (second axis -> column)
# so we're looking at row vectors here.
# ALSO, we're storing the initial state as the first element,
# so for num_timesteps of data, we need to be recording in a num_timesteps+1
# array.
pm_state_history = np.zeros((num_timesteps+1, 2*d))
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

    # At a specific timestep, we have a control input for each cable.
    # Later, we calculate this closed-loop.
    # Though it's inefficient to re-declare every iteration,
    # placing the control declaration here reminds us that it goes here
    # also later when the control law is implemented.
    
    # hard coded for now: one cable, one input.
    # do it as an ndarray so we can index into it.
    # rest length of 0, for example
    control = np.array([0])

    # Get the current point mass state, for use in calculating the
    # cable force(s).
    pm_pos = pm.get_pos()
    pm_vel = pm.get_vel()
    pm_state = pm.get_state()

    # Have each cable calculate its force.
    # Importantly, the "other anchor point" for any cable,
    # when we're simulating only a single point mass,
    # will be that point mass' position and velocity!!
    forces_list = []
    # The "pythonic" way of iterating over both cables and control inputs
    # would be to use the 'zip' function, but unsure if that's best here...
    # default to a more MATLAB-ian syntax.
    for i in range(np.size(cables)):
        # append the force from this cable.
        # BE CAREFUL that the control input vector is the same size
        # as the number of cables!
        
        ### IMPORTANT: 
        # Here is where the sign is flipped for cable forces.
        # The equations of motion, as written usually, would have
        # the output of calculate_force be negative. 
        # However, in order to be consistent with passivity,
        # we apply the negative sign here.
        # See, for example, the nonlinear passive spring proof
        # in Sastry's Nonlinear Systems textbook, where the spring
        # force is g(x), and the equations of motion include -g(x).
        force_i = -cables[i].calculate_force_nd(pm_state, control[i])
        forces_list.append(force_i)
    
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
# The timesteps are:

fig, ax = plt.subplots()
# REMEMBER THAT PYTHON INDEXES FROM 0
# 2D:
#ax.plot(pm_state_history[:,0], pm_state_history[:,1])
# 1D:
ax.plot(timesteps, pm_state_history[:,0])
plt.show()
# as of 2018-08-10:
# the 1D case works as expected, with the observation that
#   there are multiple equilibria in this model, technically:
#   if the point mass starts on "one side" of the anchor, it 
#   converges to that "side's" equiibrium with the offset in rest
#   position from the control input. If "other side," then opposite.
#   Example: at anchor = 2, and control_input = 4, two behaviors:
#   if initial_pos > 2, then converges to x = 6, 
#   but if initial_pos < 2, then converges to x = -2.
#   There's an odd behavior in 1D where the cable "flips around."
#   That doesn't apply to 2D or 3D, where there is no concept
#   of "the other side of the cable," so this is really just
#   expected behavior. A spring-damper can be a nonlinear system,
#   who'd have thought?
# But doesn't work for 2D case just yet.
# two observations: (is pm_history the right size? seems wrong.)
# (1) without gravity, system converges.
# (2) system converges to the *wrong* equilibrium position?
#       seems like it converges to [2,0] not [2,2].
#       this might be occurring in 1D also...