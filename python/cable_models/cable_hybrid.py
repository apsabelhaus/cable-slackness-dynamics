"""
Hybrid models of the cable.
Should include everything from the hybrid-linear cable, to the various
hybrid nonlinear cables. "Hybrid" here means that the the cable
force is passed through the max(force, 0) function, or equivalently,
that the cable characterization function is the Heaviside step.
Andrew P. Sabelhaus 2018
"""

from cable_models import cable_base
import numpy as np

# Linear spring-damper that cannot "push".
# This model implements a check on the final output force, similar to how
# the NASA Tensegrity Robotics Toolkit (and the Skelton book) rectify their
# forces. This is NOT the model that Drew will eventually claim is realistic...
class HybridLinearCable(cable_base.Cable):

    def calculate_force_scalar(self, anchor_state, control_input):
        """ linear spring force, linear damping force. 
            Input is rest length.
            But, passed through max(force, 0) to rectify the (final)
            output force.
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
        # For the hybrid cable, an easy way to do max(force, 0)
        # is to use the ternary operator that "shrinks" an if-statement
        # into a single line.
        Fc = (Fs + Fd) if np.greater_equal(Fs + Fd, 0) else 0
        #print(Fc)
        # debugging
        # if Fc >= 0:
        #     print(1)
        # else:
        #     print(0)
        return Fc

# Linear spring-cable that splits its max( , 0) check for the spring
# force and cable force. THIS is the one that we can check for passivity:
# since the HybridLinearCable has its rectification at the end, e.g.
# Fc = H(Fs + Fd)*(Fs + Fd) : R^2 -> R,
# the dimensions aren't conformal for the u^\top y passivity check.
# Instead, the following class implements
# Fc = H(Fs)*Fs + H(Fs)F(Fd)*Fd
# where we have INDIVIDUAL nonlinearities! 
# The claim on the controller we develop is that the control will GUARANTEE
# that Fs > 0 always, via feedback, so that H(Fs) = 1 always, so the controller
# simplifies this statement to
# Fc = Fs + H(Fd)*Fd
# ...and since Fs : R -> R and also H(Fd)*Fd : R -> R, we can verify passivity!
# Below is the generic version (does *not* close the loop in this class, you
# gotta do that elsewhere), so it implements the first equation.
class HybridSplitLinearCable(cable_base.Cable): 

    def calculate_force_scalar(self, anchor_state, control_input):
        """ linear spring force, linear damping force. 
            Input is rest length.
            But, various components passed through max(force, 0). 
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
        # For the hybrid cable, an easy way to do max(force, 0)
        # is to use the ternary operator that "shrinks" an if-statement
        # into a single line.
        # Let's recify as per (where H(x) = unit step)
        # Fc = H(Fs)*Fs + H(Fs)H(Fd)*Fd
        Fs_rect = Fs if np.greater_equal(Fs, 0) else 0
        # This comparison uses an 'and' so write out the full if, easier to read.
        Fd_rect = 0
        if np.greater_equal(Fs, 0) and np.greater_equal(Fd, 0):
            Fd_rect = Fd
        # else:
        #     Fd_rect = 0
        #Fd_rect = Fd if np.greater_equal(Fs + Fd, 0) else 0
        #print(Fc)
        # debugging
        # if Fc >= 0:
        #     print(1)
        # else:
        #     print(0)
        return Fs_rect + Fd_rect


