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
    The calculate_force function takes in the moving anchor point state
        (e.g. position and velocity) and uses calculate_length etc. 
        as helpers. Returns force.
    Various helper functions return e.g. lengths, change in lengths (in continuous
        time, since the velocity is passed in, not "next state".)
"""

# let's enforce that we can't create an instance of the superclass.
from abc import ABC, abstractmethod

# make it abstract
class Cable(ABC):
    """
    Superclass for cables. Don't create one of these. Right now, for 
    one stationary anchor point and one moving anchor point.
    """

    def __init__(self, params, anchor_pos):
        """ something numpy? Constructor can be done in super."""
        self.params = params
        self.anchor_pos = anchor_pos

    # the force calculation must be done per-cable.
    @abstractmethod
    def calculate_force(self, cable_state, input):
        """ Outputs force based on the control input and
            calculated cable state (length, d_length, calc'd elsewhere).
            Is abstract, must implement."""
        pass

    def calculate_length(self, other_anchor_pos):
        """ A geometric calculation of the cable's length
            based on anchor (saved in object) and other_anchor
            (passed in.) Cables always attach at two nodes (anchors.)
            Pass in position only.
            Is implemented here, in super! """
        pass
    
    def calculate_d_length_dt(self, other_anchor_pos, other_anchor_vel):
        """ Same as calculate_length, but for cable length change.
            Needs both the position and change-in-position of the
            other anchor point (I think? do this later?)
            Is implemented here, in super."""
        pass

# simplest example: linear spring-damper.
class LinearCable(Cable):

    def calculate_force(self, cable_state, input):
        """ linear spring force, linear damping force. Input is rest length."""
        pass

