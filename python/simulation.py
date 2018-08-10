"""
Primary script for cable slackness dynamics simulations.
(C) Andrew P. Sabelhaus, 2018
"""


# import everything we need
import numpy as np
# for the cables and other things we write,
# let's make it so we don't need to use the module name
from cable_models import *

# Parameters for the cables are going to be a dict.
linear_cable_params = {'k':1, 'c':1}
# anchor point for cable 1 at some offset.
cable1_anchor = np.array([2])
# create the cable
cable1 = cable_linear.LinearCable(params = linear_cable_params, 
                                  anchor_pos = cable1_anchor)

# 
