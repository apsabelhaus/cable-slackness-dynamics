"""
Linear model(s) of cable.
(there's only one type of 'linear' cable, 
so this module is a single class.)
Andrew P. Sabelhaus 2018
"""

from cable_models import cable_base

# simplest example: linear spring-damper.
class LinearCable(cable_base.Cable):

    def calculate_force(self, cable_state, input):
        """ linear spring force, linear damping force. Input is rest length."""
        pass


