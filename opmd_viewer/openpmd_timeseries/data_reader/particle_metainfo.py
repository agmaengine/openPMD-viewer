"""
This file is part of the openPMD-viewer.

It defines the main ParticleMetaInformation class, which
is returned by `get_particle` along with the array of field values,
and gathers information collected from the openPMD file.

Copyright 2015-2016, openPMD-viewer contributors
Author: Chatchai Sirithipvanich
License: 3-Clause-BSD-LBNL
"""

import numpy as np
from .utilities import get_data, get_bpath, join_infile_path


class ParticleMetaInformation(object):
    """
    An object that is typically returned along with an array of selected quantity
    values (eg. position/x, momentum/x), and which contains meta-information
    about the selected quantity of the selected particle.

    Attributes
    ----------
    - mass: double
        species' mass in SI unit
    - charge: double
        species' charge in SI unit
    - quantity_unit: dict
        The units return '.particle_reader.read_species_data'
    - unitSI: dict
        A conversation factor to multiply data with to be represented in SI
    """

    def __init__(self, file_handle, species, var_list):
        """
        Create a FieldMetaInformation object

        The input arguments correspond to their openPMD standard definition
        """
        # access file
        base_path = get_bpath(f)
        particles_path = file_handle.attrs['particlesPath'].decode()
        species_grp = file_handle[
            join_infile_path(base_path, particles_path, species,)]
        # Register important initial information
        mass = species_grp['mass'].attrs['value']
        mass *= species_grp['mass'].attrs['unitSI']
        self.mass = mass
        charge = species_grp['charge'].attrs['value']
        charge *= species_grp['charge'].attrs['unitSI']
        self.charge = charge
        # units return by according to '.particle_reader.read_species_data'
        self.quantity_unit = {'x' : 'um',
                                 'y' : 'um',
                                 'z' : 'um',
                                 'ux': 'p/mc',
                                 'uy': 'p/mc',
                                 'uz': 'p/mc'}
        self.unitSI = {'x' : np.float64(1e-6),
                       'y' : np.float64(1e-6),
                       'z' : np.float64(1e-6),
                       'ux': np.float64(mass*charge),
                       'uy': np.float64(mass*charge),
                       'uz': np.float64(mass*charge)}
