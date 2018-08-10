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
        # IMPORTANT: we assume that 'g' is an absolute value.
        # example, pass in g = 9.8, NOT g = -9.8
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

    # "The Big One:"
    # Calculates the acceleration of this point mass given the 
    # list of forces acting upon it. m \ddot x = \sum F - m*g,
    # in any number of dimensions.
    # Note that this formulation implies that the list of F does NOT include
    # the gravitational force: the point mass calculates and adds that 
    # force itself.
    # YOU BETTER MAKE SURE that each force has the same dimensionality
    # when you call this function! It's very polymorphic!
    def calculate_accel(self, forces_list):
        # The forces vectors are in R^d.
        # The helper function will sum them up:
        sum_forces = self.calculate_sum_forces(forces_list)
        # Since linear algebra, each dimension accel from external 
        # forces is (1/m) * F_i, for i = 1 : d
        accel = (1 / (self.m)) * sum_forces
        # Next, check if dimensionality is greater than 2, 
        # and add g to the second dimension if so (since (1/m)*mg = g).
        if np.greater_equal(self.get_dimensionality(), 2):
            # Add g to the second element (that's index 1.)
            # here's where gravity acts in the 'negative' direction, (-) not (+)
            accel[1] -= self.g
        # now done
        return accel

    # A helper function that's used in calculate_accel.
    # Takes in a list of forces and adds them element-wise
    # (this is \sum F).
    def calculate_sum_forces(self, forces_list):
        # preallocate the sum.
        # Remember that each force in forces_list should be the 
        # same dimensionality as the rest of the problem
        # (e.g., if in 3D, then position is a 3-vector, so is velocity,
        # so is acceleration, so is each force.)
        d = self.get_dimensionality()
        sum_forces = np.zeros(d)
        # iterate over the list of forces.
        for force in forces_list:
            # add this one
            sum_forces += force
        # that's all!
        return sum_forces

    # A function to interface with the outside world:
    # Returns the \dot x for the point mass (e.g. the velocities
    # and accelerations.) Useful for doing forward integration.
    def state_deriv(self, forces_list):
        # get the acceleration
        accel = self.calculate_accel(forces_list)
        # concatenate to the velocities
        return np.concatenate((self.vel, accel))
