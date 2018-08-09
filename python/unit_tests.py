"""
Not strictly 'unit testing', since not in python's unit testing framework,
but a handful of calculations so we can check the output from 
various classes.
Andrew P. Sabelhaus 2018
"""

# start off same as simulation script
# import everything we need
import numpy as np
# for the cables and other things we write,
# let's make it so we don't need to use the module name
from cable_models import *

# Parameters for the cables are going to be a dict.
linear_cable_params = {'k':1, 'c':1}
# anchor point for cable 1 at origin.
cable1_anchor = np.array([0, 0])

cable1 = cable_linear.LinearCable(params = linear_cable_params, 
                                  anchor_pos = cable1_anchor)

"""
Tests:
"""

# cable length change.
# a test position and velocity of point:
other_anchor1 = np.array([3, 4])
# with the other anchor point moving along the vector of the
# cable (e.g. 'pulling directly outward',) the cable length
# change (velocity) should be equal to 1.
other_anchor_vel1 = np.array([0.6, 0.8])
cable1_vel = cable1.calculate_d_length_dt(other_anchor1, 
                                          other_anchor_vel1)

print(cable1_vel)

# similarly, if we keep that 'pulling directly outward'
# but with a larger velocity, should scale:
cable1_vel_faster = cable1.calculate_d_length_dt(other_anchor1,
                                                 2*other_anchor_vel1)

print(cable1_vel_faster)

# we can also think through what the length change
# should be if the cable is being pulled at a 45 degree angle.
# ...do this later

# To-do: test dimensionality here. 
# Do the cable functions work generally enough for 1D through 3D?

# Let's do a force.
anchor1_state = np.concatenate((other_anchor1, other_anchor_vel1))
# zero rest length for now.
control_input = 0
cable1_force = cable1.calculate_force(anchor1_state, control_input)
