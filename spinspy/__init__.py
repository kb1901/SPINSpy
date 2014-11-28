# Initialization file for package. Does nothing.

# Import required packages
import numpy as np
import sys
import collections
import os
import warnings

# Read in the defined functions. Not strictly necessary,
# but makes usage nicer. i.e. now we can use
# matpy.cheb(5) instead of matpy.cheb.cheb(5).
from grid_readers import get_data
from grid import grid
from readers import reader
from spinspy_classes import Grid

# Define what happens when someone uses
# from matpy import *
__all__ = ["grid_readers", "grid", "readers", "spinspy_classes"]