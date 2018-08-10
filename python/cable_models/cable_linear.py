"""
Linear model(s) of cable.
(there's only one type of 'linear' cable, 
so this module is a single class.)
Andrew P. Sabelhaus 2018
"""

from cable_models import cable_base

# simplest example: linear spring-damper.
class LinearCable(cable_base.Cable):

    def calculate_force(self, anchor_state, control_input):
        """ linear spring force, linear damping force. 
            Input is rest length.
            See super for anchor_state discussion."""
        # Split the anchor state up according to the dimensionality
        # of the problem: 1,2,3D means anchor state has 2,4,6 vars
        # (assuming the x...z positions come first.)
        d = self.get_dimensionality()
        # since numpy indexing is [first_elem : n+1 elem],
        # an operation like somearray[0:2] actually returns elements
        # 0 and 1.
        # So, 0:d gets the first d elements, and d:2d gets the last.
        other_anchor_pos = anchor_state[0 : d]
        other_anchor_vel = anchor_state[d : (2*d)]
        # calculate the spring term. 
        # we often use 'stretch' to be \delta length.
        # input is a nonnegative scalar, result is a signed scalar.
        # TO-DO: for other cable models, enforce actuator saturation,
        # and reset a control_input < 0 to = 0.
        stretch = self.calculate_length(other_anchor_pos) - control_input
        # spring force is
        Fs = self.params['k'] * stretch
        # damping force is
        Fd = self.params['c'] * self.calculate_d_length_dt(
            other_anchor_pos, other_anchor_vel)
        # the sum is the total force from this cable.
        # THIS IS A SCALAR, SIGNED QUANTITY
        # (result < 0 if ||r|| < control_input.)
        return Fs + Fd                                                 



