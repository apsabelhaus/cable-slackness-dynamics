"""
Piecewise slackness model of the cable.
The the cable force is passed through the max(force, 0) function, or equivalently,
that the cable characterization function is the Heaviside step.
Three dimensional cable.
Andrew P. Sabelhaus 2019
"""

from cable_models import cable_base3D
import numpy as np

# Linear spring-damper that cannot "push".
# This model implements a check on the final output force, similar to how
# the NASA Tensegrity Robotics Toolkit (and the Skelton book) rectify their
# forces.
class PiecewiseLinearCable3D(cable_base3D.Cable3D):

    def scalar_force(self, ell, dot_ell, control_input):
        """ linear spring force, linear damping force. 
            Input is rest length.
            But, passed through max(force, 0) to rectify the (final)
            output force."""
        # NEED TO DO: MODEL ACTUATOR SATURATION!!!!!!
        # WE CAN'T ACT ON A control_input < 0 !!!!
        # calculate the spring term. 
        # we often use 'stretch' to be \delta length.
        # TO-DO: for other cable models, enforce actuator saturation,
        # and reset a control_input < 0 to = 0.
        stretch = ell - control_input
        # spring force is (from our parameters dict)
        Fs = self.params['k'] * stretch
        # damping force is
        Fd = self.params['c'] * dot_ell
        # their sum
        F = Fs + Fd
        # For the the piecewise cable, an easy way to do max(force, 0)
        # is to use the ternary operator that "shrinks" an if-statement
        # into a single line.
        F_rect = (F) if np.greater_equal(F, 0) else 0
        return F_rect