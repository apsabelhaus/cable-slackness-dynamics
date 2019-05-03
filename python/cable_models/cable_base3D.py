#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 12:37:38 2018

@author: Andrew P. Sabelhaus

Module for Cables, used (for now) with only one body,
so there's one (not-moving) anchor point and one moving 
attachment point.

This class works in \mathbb{E}^3, currently with a Cartesian coordinate system.
Easier than trying to go full polymorphic with cross and dot in n-dimensions.

The assumed model herein is

F_i(\br, \bv) = \Phi_i(\ell_i(\br), \dot \ell_i(\bv)) \hat \bell_i

where \br is 'point_pos' and 'bv' is 'point_vel', as if connected at a point.

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
class Cable3D(ABC):
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
    def scalar_force(self, ell, dot_ell, control_input):
        """ Outputs force based on the control input and
            the cable length, ell, and stretch rate, dot ell."""
        pass

    # ...however, this base class CAN project the force into its
    # n-dimensional space. Since scalar_force outputs a scalar.
    # Note that here, the position and velocity of the anchor need to be
    # passed in, so the unit vector can be calculated.
    def force_3d(self, point_pos, point_vel, control_input):
        # first, get the current length and stretch rate
        ell = self.get_length(point_pos)
        # importantly, here, we need to dot velocity with \hat \bell,
        # requiring anchor position to be passed in also.
        dot_ell = self.get_dot_length(point_pos, point_vel)
        # scalar force is then
        Phi = self.scalar_force(ell, dot_ell, control_input)
        # Direction along which this cable acts is
        unit_vec = self.get_dir_vec(point_pos)
        # and finally, dot the two.
        return unit_vec * Phi

    # a helper. Gets the unit vector between the two anchors,
    # used for calculating the n-dimensional force (scalar times unit vec.)
    # and as part of the chain rule for velocity.
    def get_dir_vec(self, point_pos):
        # unit vector is \hat r  = r / ||r||
        ell_vec = point_pos - self.anchor_pos
        ell = self.get_length(point_pos)
        # \hat ell  = \ell / ||\ell||
        return ell_vec / ell

    # a helper. Calulates the cable's scalar length.
    def get_length(self, point_pos):
        # \ell = || r - b_i ||
        return np.linalg.norm(point_pos - self.anchor_pos)
    
    # a helper. Cable's rate-of-length-change. Still don't know a 
    # good term to use here... stretch rate would be \dot \epsilon not \dot \ell
    def get_dot_length(self, point_pos, point_vel):
        # \dot \ell = \bv \cdot \hat \ell
        return np.dot(point_vel, self.get_dir_vec(point_pos))
    
    # For use when calculating the value of the Lyapunov function,
    # we also want the scalar conservative force little \mathbf{f}.
    # By definition, that's the scalar force with zero velocity, so
    def scalar_conservative_force(self, ell, control_input):
        # working in three dimensions
        vel = np.array([0, 0, 0])
        return self.scalar_force(ell, vel, control_input)

