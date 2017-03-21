#!/usr/bin/env python3
# maths_module.py

#------------------------------------------------------------------------------------------------#
# This software was written in 2016/17                                                           #
# by Michael P. Allen <m.p.allen@warwick.ac.uk>/<m.p.allen@bristol.ac.uk>                        #
# and Dominic J. Tildesley <dominic.tildesley@epfl.ch> ("the authors"),                          #
# to accompany the book "Computer Simulation of Liquids", second edition, 2017 ("the text"),     #
# published by Oxford University Press ("the publishers").                                       #
#                                                                                                #
# LICENCE                                                                                        #
# Creative Commons CC0 Public Domain Dedication.                                                 #
# To the extent possible under law, the authors have dedicated all copyright and related         #
# and neighboring rights to this software to the PUBLIC domain worldwide.                        #
# This software is distributed without any warranty.                                             #
# You should have received a copy of the CC0 Public Domain Dedication along with this software.  #
# If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.                               #
#                                                                                                #
# DISCLAIMER                                                                                     #
# The authors and publishers make no warranties about the software, and disclaim liability       #
# for all uses of the software, to the fullest extent permitted by applicable law.               #
# The authors and publishers do not recommend use of this software for any purpose.              #
# It is made freely available, solely to clarify points made in the text. When using or citing   #
# the software, you should not imply endorsement by the authors or publishers.                   #
#------------------------------------------------------------------------------------------------#

"""Routines for maths, random numbers, order parameters."""

# Routines associated with random number generation

def random_vector():
    """Returns a random unit vector as a numpy array of 3 elements."""

    import numpy as np

    zeta = np.random.rand(2) # Two uniformly sampled random numbers in range (0,1)
    c = 2.0*zeta[0] - 1.0    # Random cos(theta) uniformly sampled in range (-1,+1)
    if c >= 1.0:             # Guard against very small chance of roundoff error
        s = 0.0              # Set sin(theta) to zero
    else:
        s = np.sqrt(1.0-c**2) # Calculate sin(theta) from cos(theta), always positive

    phi = zeta[1] * 2.0*np.pi # Random angle uniformly sampled in range (0,2*pi)

    return np.array ( ( s*np.cos(phi), s*np.sin(phi), c ), dtype=np.float_ ) # Random unit vector

def random_translate_vector ( dr_max, old ):
    """Returns a vector translated by a random amount."""

    import numpy as np

    # A randomly chosen vector is added to the old one

    zeta = np.random.rand(3)   # Three uniform random numbers in range (0,1)
    zeta = 2.0*zeta - 1.0      # Now in range (-1,+1)
    return old + zeta * dr_max # Move to new position

def metropolis ( delta ):
    """Conduct Metropolis test, with safeguards."""

    import numpy as np
    
    exponent_guard = 75.0

    if delta > exponent_guard: # Too high, reject without evaluating
        return False
    elif delta < 0.0: # Downhill, accept without evaluating
        return True
    else:
        zeta = np.random.rand() # Uniform random number in range (0,1)
        return np.exp(-delta) > zeta # Metropolis test

# Low-level mathematical operations

def rotate_vector ( angle, axis, old ):

    """Returns a vector rotated from the old one by specified angle about specified axis."""

    import numpy as np
    from math import isclose
    
    # Note that the axis vector should be normalized and we test for this
    # In general, the old vector need not be normalized, and the same goes for the result
    # although quite often in our applications they will be

    assert old.size == 3, 'Incorrect size of old'
    assert axis.size == 3, 'Incorrect size of axis'
    assert isclose(np.sum(axis**2),1.0), 'Non-unit vector {} {} {}'.format(*axis)

    c    = np.cos ( angle )
    s    = np.sin ( angle )
    proj = np.dot ( axis, old ) # The two vectors need not be perpendicular

    # Standard (Goldstein) rotation formula
    e = c * old + ( 1.0 - c ) * proj * axis + s * np.cross ( axis, old )

    return e
