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
        # first element is pos, second is velocity (of anchor point)
        other_anchor_pos = anchor_state[0]
        other_anchor_vel = anchor_state[1]
        # calculate the spring term. 
        # we often use 'stretch' to be \delta length.
        # input is a scalar
        stretch = self.calculate_length(other_anchor_pos) - control_input
        # spring force is
        Fs = self.params['k'] * stretch
        # damping force is
        Fd = self.params['c'] * self.calculate_d_length_dt(
            other_anchor_pos, other_anchor_vel)
        # the sum is the total force from this cable.
        return Fs + Fd                                                 



