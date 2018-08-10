# Class for a single point mass.
# Should be polymorphic with respect to dimensionality (1D, 2D, 3D.)

# need to do linear alg
import numpy as np

class PointMass:
    # point masses have a mass, a gravitational constant under which
    # the mass exists (assumed to work in the (-) direction of the last 
    # dimension, e.g. the Z for either 2D or the Z for 3D), and a 
    # position/velocity (which an initial condition is assigned at 
    # time of instantiation.)
    # Later, we will assume that 1D cases are "horizontal" and don't
    # have a gravitational offset (this is for convenience of testing.)
    # TO-DO: will it be better to create this functionality by either...
    # 1) having gravity passed in as a 3-vector, like in the NASA Tensegrity
    #    Robotics Toolkit?
    # 2) and thus having zero gravity just eliminate the "mg" terms automatically?
    # Position and velocity are n-dimensional vectors.

    def __init__(self, m, g, initial_pos, initial_vel):
        # just keep track of all these, nothing special (yet)
        # TO-DO: lots of checks here.
        self.m = m
        self.g = g
        self.pos = initial_pos
        self.vel = initial_vel

    # a helper, to get the dimensionality of this point mass.
    # We assume that the initial position / velocity are in R^d
    # (TO-DO: many checks here!), and so assume that all other 
    # computations are in the same dimensionality.
    def get_dimensionality(self):
        # choose position as the thing to check (arbitrarily)
        # you better be good and make sure pos and vel are same size!!
        return np.size(self.pos)

    # Point masses can have their position/velocity assigned,
    # and can return their position/velocity and state (which is just the
    # two concatenated.)
    def get_pos(self):
        return self.pos
    
    def get_vel(self):
        return self.vel

    def get_state(self):
        return np.concatenate((self.pos, self.vel))

    def set_pos(self, pos):
        self.pos = pos

    def set_vel(self, vel):
        self.vel = vel

    def set_state(self, state):
        # As with the cables, we need to check the dimensionality
        # here. 
        d = self.get_dimensionality()
        # ...because we can then figure out how to split up state.
        # A point mass has d positions and d velocities for a d-dimensional space.
        self.pos = state[0 : d]
        self.vel = state[d : (2*d)]
