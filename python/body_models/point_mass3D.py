# Class for a single point mass.
# This class is for 3D models.
# (C) Andrew Sabelhaus 2019

# need to do linear alg
import numpy as np

class PointMass3D:
    # point masses have a mass, a gravitational constant under which
    # the mass exists, assumed to work in the (-) direction of coordinate 3, and a 
    # position/velocity (which an initial condition is assigned at 
    # time of instantiation.)

    def __init__(self, m, g, initial_pos, initial_vel):
        # just keep track of all these, nothing special (yet)
        # TO-DO: lots of checks here.
        self.m = m
        # IMPORTANT: we assume that 'g' is an absolute value.
        # example, pass in g = 9.8, NOT g = -9.8
        self.g = g
        self.pos = initial_pos
        self.vel = initial_vel

    # Point masses can have their position/velocity assigned,
    # and can return their position/velocity and state (which is just the
    # two concatenated.) <- Not going to be used here, since we derived
    # all our control stuff in terms of \br and \bv separately.
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
        # three dimensions
        self.pos = state[0 : 3]
        self.vel = state[3 : 6]

    # "The Big One:"
    # Calculates the acceleration of this point mass given the 
    # list of forces acting upon it. m \ddot x = \sum F - m*g \mathbf{E}^3,
    # Equivalently: \ddotx = \sum F/m - g \mathbf{E}^3.
    # Note that this formulation implies that the list of F does NOT include
    # the gravitational force: the point mass calculates and adds that 
    # force itself.
    # YOU BETTER MAKE SURE that each force has the same dimensionality
    # when you call this function!
    # Takes in a list of 1D ndarrays, each with three elements,
    # and returns a single 1D ndarray with three elements.
    def calculate_accel(self, forces_list):
        # The forces vectors are in R^3.
        # The helper function will sum them up:
        sum_forces = self.calculate_sum_forces(forces_list)
        # Since linear algebra,
        accel = (1 / (self.m)) * sum_forces
        # For the adding of gravity, we assume that the final dimension
        # is the direction of gravity.
        # E.g., in 3D, is -Z (if X,Y,Z).
        accel[-1] += -self.g
        # now done
        return accel

    # A helper function that's used in calculate_accel.
    # Takes in a list of forces and adds them element-wise
    # (this is \sum F).
    # The input is a list of 1D, three-element ndarrays
    def calculate_sum_forces(self, forces_list):
        # preallocate the sum.
        sum_forces = np.zeros(3)
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
