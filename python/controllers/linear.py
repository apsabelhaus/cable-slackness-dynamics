# Class for a single input, single output,
# affine-feedback controller.
# Implements linear/affine/open-loop controllers
# (C) Andrew Sabelhaus 2019

# need to do linear alg
import numpy as np

class AffineFeedback:
    # A controller that implements
    # v = \kappa (\ell - \bar \ell) + \bar v
    # Is stateless, and SISO.

    def __init__(self, kappa, bar_ell, bar_v):
        # just keep track of all these, nothing special (yet)
        # TO-DO: lots of checks here.
        # Kappa is the controller gain, \bar \ell is the equilibrium
        # length of (for example) this cable, and \bar v is the
        # equilibrium rest length (equilibrium input) calculated
        # via whatever other methodology.
        self.kappa = kappa
        self.bar_ell = bar_ell
        self.bar_v = bar_v

    # Only one function needed.
    # Controller goes from y to v, since we're using
    # different notation (u is needed for system-wide passivity notation)
    # so just keep with the notation.
    def v(self, ell):
        # Here's the calculation
        return self.kappa * (ell - self.bar_ell) + self.bar_v

class OpenLoop:
    # A controller that returns a set value at each timestep: is open-loop.

    def __init__(self, bar_v):
        # just return bar v each time.
        self.bar_v = bar_v

    # Only one function needed.
    # Controller goes from y to v, since we're using
    # different notation (u is needed for system-wide passivity notation)
    # so just keep with the notation.
    def v(self, ell):
        # not using the feedback information.
        return self.bar_v