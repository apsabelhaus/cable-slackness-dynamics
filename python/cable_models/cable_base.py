#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 12:37:38 2018

@author: Andrew P. Sabelhaus

Module for Cables, used (for now) with only one body,
so there's one (not-moving) anchor point and one moving 
attachment point.
The superclass specifies inputs and outputs:
    Constructor takes parameters and anchor point
    The calculate_force_scalar function takes in the moving anchor point state
        (e.g. position and velocity) and uses calculate_length etc. 
        as helpers. Returns force.
    Various helper functions return e.g. lengths, change in lengths (in continuous
        time, since the velocity is passed in, not "next state".)
"""

# let's enforce that we can't create an instance of the superclass.
from abc import ABC, abstractmethod
# need to do linear alg
import numpy as np

# make it abstract
class Cable(ABC):
    """
    Superclass for cables. Don't create one of these. Right now, for 
    one stationary anchor point and one moving anchor point.
    """

    def __init__(self, params, anchor_pos):
        """ something numpy? Constructor can be done in super.
            We want params to be a dictionary, and anchor_pos 
            to be a 2-element numpy array. """
        self.params = params
        self.anchor_pos = anchor_pos

    # the force calculation must be done per-cable.
    @abstractmethod
    def calculate_force_scalar(self, anchor_state, control_input):
        """ Outputs force based on the control input and
            the state of the moving anchor (the attachment point),
            which implies that this function should (almost certainly)
            be calling calculate_length etc. to do its calculations.
            In: anchor_state is a 2-vec, first elem pos, second elem
            vel. Each component is in \mathbb{R}^1, 2, or 3 depending on
            if we're simulating 1D, 2D, 3D cable.
            ALSO, note we're doing this 'passivity-style', as in,
            a positive force returned, not a negative. 
            Example, F = k \delta x, not F = -k \delta x
            Is abstract, must implement."""
        pass

    # ...however, this base class CAN project the force into its
    # n-dimensional space. Since calculate_force_scalar returns a scalar.
    def calculate_force_nd(self, anchor_state, control_input):
        # first, get the scalar force
        F = self.calculate_force_scalar(anchor_state, control_input)
        # Then, pull out the position from the anchor state.
        # LinearCable has more info about this calculation.
        d = self.get_dimensionality()
        other_anchor_pos = anchor_state[0:d]
        # now, we can get the unit vec:
        unit_vec = self.get_dir_vec(other_anchor_pos)
        # and finally, dot the two.
        return np.dot(unit_vec, F)

    # a helper method: in order to determine the dimensionality of the 
    # problem (a 1D, 2D, or 3D cable), we can calculate the size of
    # the anchor_state variable. Since each dimension has pos and vel,
    # the dimensionality has to be either 2, 4, or 6. This function
    # returns just the constant 2, 4, 6 with a bit of checking.
    # Can be done just with self, actually, since anchor_pos is exactly
    # the dimensionality of the problem!
    def get_dimensionality(self):
        return np.size(self.anchor_pos)

    # a helper. Gets the unit vector between the two anchors,
    # used for calculating the n-dimensional force (scalar times unit vec.)
    # and as part of the chain rule for velocity.
    def get_dir_vec(self, other_anchor_pos):
        # unit vector is \hat r  = r / ||r||
        pos_net_vec = other_anchor_pos - self.anchor_pos
        pos_net_vec_norm = np.linalg.norm(pos_net_vec, 2)
        # \hat r  = r / ||r||
        return pos_net_vec / pos_net_vec_norm

    # a helper. Takes in state and parses according to dimensionality,
    # so the caller doesn't have to bother with indexing into the state to
    # get the cable position.
    def calculate_length_from_state(self, other_anchor_state):
        # we need to check the dimensionality
        # here. 
        d = self.get_dimensionality()
        # ...because we can then figure out how to index into the state
        # A point mass has d positions and d velocities for a d-dimensional space.
        return other_anchor_state[0 : d]

    def calculate_length(self, other_anchor_pos):
        """ A geometric calculation of the cable's length
            based on anchor (saved in object) and other_anchor
            (passed in.) Cables always attach at two nodes (anchors.)
            Pass in position only.
            Is implemented here, in super! """
        # length is just the 2-norm of the net vector b/w points.
        # NOTE that this is NOT a signed distance! Magnitude!
        pos_net_vec = other_anchor_pos - self.anchor_pos
        return np.linalg.norm(pos_net_vec, 2)
    
    def calculate_d_length_dt(self, other_anchor_pos, other_anchor_vel):
        """ Same as calculate_length, but for cable length change.
            Needs both the position and change-in-position of the
            other anchor point
            Is implemented here, in super."""
        # By using chain rule and partial deriv of 2-norm,
        # change in length (d ||r|| / dt) is net velocity dotted
        # with unit vector of position. (n-dim vec \dot n-dim vec => scalar).
        # First, get unit vec of position:
        #pos_net_vec = other_anchor_pos - self.anchor_pos
        #pos_net_vec_norm = np.linalg.norm(pos_net_vec, 2)
        # \hat r  = r / ||r||
        #pos_unit_vec = pos_net_vec / pos_net_vec_norm
        pos_unit_vec = self.get_dir_vec(other_anchor_pos)
        # Since self.anchor_pos is not moving, it has zero
        # velocity, therefore net velocity is just the velocity
        # of the other anchor point.
        return np.dot(pos_unit_vec, other_anchor_vel)

