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
    
    def get_Uf(self, point_pos, control_input):
        """ It would be hard to implement the exact eqn from my notes,
            since that already has the loop closed.
            Instead, this should be the same as 1/2 k vareps^2, i.e., 
            square the amount of stretch, which is vareps = ell - u.
            So just throw an error for negative stretch (undefined.)"""
        ############# TO-DO:
        ############# make cables closed-loop and see if this changes!!!!
        stretch = self.get_length(point_pos) - control_input
        if stretch <= 0:
            raise Exception('Negative stretch length, Uf is undefined, exiting.')
        else:
            Uf = 0.5 * self.params['k'] * stretch**2
            # print(Uf)
            return Uf
    
    def get_Uf_affine(self, point_pos, controller):
        """ HACKY """
        # This function returns the Uf with the closed-loop affine control law.
        # Pull out the controller's constants
        kappa = controller.get_kappa()
        bar_ell = controller.get_bar_ell()
        bar_v = controller.get_bar_v()
        ell = self.get_length(point_pos)
        # From Drew's notes, this should be
        # 1/2 kappa_i alpha_i ell^2 + kappa_i beta_i ell
        # with
        # alpha_i = (1 - kappa_i)
        # beta_i = kappa_i bar_ell_i - bar_u
        alpha = 1 - kappa
        beta = kappa * bar_ell -  bar_v
        k = self.params['k']
        return 0.5 * k * alpha * ell**2 + k * beta * ell

    ##################### THIS IS INCORRECT
    def get_Uf_adjusted(self, point_pos, controller):
        """ HACKY """
        # This function returns the Uf with the closed-loop affine control law,
        # WITH THE ADJUSTMENTS for integrating with the control input included!
        # Pull out the controller's constants
        kappa = controller.get_kappa()
        ell = self.get_length(point_pos)
        # amount of stretch applied is
        stretch = controller.v(ell)
        # From Drew's notes, this should be
        # 1/2 k_i / (1 - kappa) stretch^2
        Uf_i = 0.5 * (self.params['k'] / (1 - kappa)) * stretch**2
        return Uf_i